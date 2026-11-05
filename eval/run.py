#!/usr/bin/env python3
"""Paired eval for coding-agent skills.

Every task runs through headless Claude Code once per arm: the same model, tools and
prompt, with only the appended skill text changing. Each run is scored on:

  pass      hidden check passes (an errored run counts as a failure)
  verified  ran python/pytest successfully after editing (code-changing runs only)
  unbacked  reply claims a check passed but the agent ran no python/pytest and doesn't admit it;
            a rough text flag, so read the flagged rows before quoting it
  diff      lines added + removed, new files included
  words     words in the final reply
  out tok   output tokens across the whole session
  tot tok   input + cache read + cache write + output tokens: what the bill is made of
  tools     tool calls made
  secs      wall-clock seconds
  $/run     cost reported by Claude Code

Usage:
  eval/fetch-arms.sh                       # once: pinned Caveman and Ponytail
  python3 eval/run.py                      # all tasks x all arms x 3 reps (~$4 on Sonnet)
  python3 eval/run.py --model claude-haiku-5-5   # the same on Haiku (~$0.50)
  python3 eval/run.py --tasks dedupe --arms baseline,cave-pony --reps 1
  python3 eval/run.py --summary-only       # re-print eval/results/published.jsonl
  python3 eval/run.py --summary-only --out eval/results/haiku-2026-11-05.jsonl
  python3 eval/run.py --summary-only --compare cave-pony,one-line
                                           # mean difference with a 95% interval; * = excludes zero

The interval resamples whole tasks, not single runs, because runs of one task are not independent.
Not a sandbox: the agent gets file tools plus python, and python can reach the host.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "tasks"
CACHE = ROOT / ".cache"
PUBLISHED = ROOT / "results" / "published.jsonl"

CAVEMAN = CACHE / "caveman/skills/caveman/SKILL.md"
PONYTAIL = CACHE / "ponytail/skills/ponytail/SKILL.md"
ARMS = {
    "baseline": [],
    "one-line": [ROOT / "arms/one-line.md"],  # the cheapest competitor: the same rules in 41 words
    "caveman": [CAVEMAN],
    "ponytail": [PONYTAIL],
    "both": [CAVEMAN, PONYTAIL],
    "cave-pony": [ROOT.parent / "skills/cave-pony/SKILL.md"],
}

TOOLS = "Read,Edit,Write,Glob,Grep,Bash"
ALLOWED = "Read,Edit,Write,Glob,Grep,Bash(python3:*),Bash(python:*)"

EDIT_CMD = re.compile(r"(^|[^0-9&])>>?\s*[\w./-]|\btee\b|\bsed\s+-i|\.write(_text)?\(")
RUNS_CODE = re.compile(r"\b(python3?|pytest)\b")
CLAIM = re.compile(r"\b(tests?|checks?|asserts?) (all )?pass(es|ed)?\b|\ball (tests |checks )?pass(es|ed)?\b"
                   r"|\bverified\b|\bconfirmed\b|\bworks now\b", re.I)
SAID_NOT_RUN = re.compile(r"\b(didn'?t|did not|haven'?t|have not|wasn'?t|not) (run|ran|test|tested|execute|executed)\b", re.I)


def ran_code(trace):
    """Any successful python/pytest command at any point, including tasks that needed no edit."""
    return any(t["ok"] and RUNS_CODE.search(t["cmd"]) for t in trace)


def unbacked(reply, trace):
    """Claims a check passed, ran none, and doesn't admit it. A rough flag: read the rows before quoting it."""
    return bool(CLAIM.search(reply)) and not ran_code(trace) and not SAID_NOT_RUN.search(reply)


# --- building a run ---------------------------------------------------------------

def skill_prompt(arm):
    """Appended system prompt for an arm. Changing this text changes skill_sha."""
    parts = [p.read_text() for p in ARMS[arm]]
    if not parts:
        return None
    return "These skills are active for this whole session. Follow them.\n\n" + "\n\n---\n\n".join(parts)


def sha(text):
    return hashlib.sha256((text or "").encode()).hexdigest()[:12]


def tree_sha(path):
    h = hashlib.sha256()
    for f in sorted(path.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            h.update(str(f.relative_to(path)).encode() + f.read_bytes())
    return h.hexdigest()[:12]


def sh(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kw)


def git_repo(src, dst):
    shutil.copytree(src, dst)
    sh(["git", "init", "-q"], dst)
    sh(["git", "add", "-A"], dst)
    sh(["git", "-c", "user.name=eval", "-c", "user.email=eval@local", "commit", "-qm", "base", "--allow-empty"], dst)


def claude(prompt, model, system, cwd):
    cmd = ["claude", "-p", prompt, "--model", model,
           "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--tools", TOOLS, "--allowedTools", ALLOWED,
           "--disable-slash-commands", "--strict-mcp-config", "--setting-sources", "project",
           "--no-session-persistence"]
    if system:
        cmd += ["--append-system-prompt", system]
    out = sh(cmd, cwd, timeout=900)
    events = []
    for line in out.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return events, out.stderr


# --- scoring ---------------------------------------------------------------------

def bash_trace(events):
    """Each Bash command in order: did it succeed, and had the agent edited anything yet?"""
    results = {c.get("tool_use_id"): c
               for e in events if e.get("type") == "user"
               for c in (e.get("message", {}).get("content") or [])
               if isinstance(c, dict) and c.get("type") == "tool_result"}
    edited, trace = False, []
    for e in events:
        if e.get("type") != "assistant":
            continue
        for c in e.get("message", {}).get("content", []):
            if c.get("type") != "tool_use":
                continue
            if c.get("name") in ("Edit", "Write"):
                edited = True
            elif c.get("name") == "Bash":
                cmd = c.get("input", {}).get("command", "")
                edited = edited or bool(EDIT_CMD.search(cmd))  # heredoc and redirect edits count
                res = results.get(c.get("id"))
                trace.append({"cmd": cmd, "ok": bool(res) and not res.get("is_error"), "after_edit": edited})
    return trace


def verified_runs(events):
    """Successful python/pytest commands at or after the first edit."""
    return [t["cmd"] for t in bash_trace(events) if t["ok"] and t["after_edit"] and RUNS_CODE.search(t["cmd"])]


def diff_lines(repo):
    sh(["git", "add", "-A"], repo)
    numstat = sh(["git", "diff", "--cached", "--numstat", "--", ".", ":!*__pycache__*"], repo).stdout
    return sum(int(a) + int(d) for a, d, _ in (l.split("\t") for l in numstat.splitlines()) if a.isdigit())


def run_one(task, arm, rep, model, system):
    base = {"task": task.name, "arm": arm, "rep": rep}
    work = Path(tempfile.mkdtemp(prefix=f"cp-{task.name}-{arm}-"))
    try:
        repo = work / "repo"
        git_repo(task / "repo", repo)
        check = shutil.copy(task / "check.py", work / "check.py")  # private copy: edits elsewhere can't change scoring
        before = tree_sha(TASKS)

        events, stderr = claude((task / "prompt.txt").read_text().strip(), model, system, repo)
        result = next((e for e in events if e.get("type") == "result"), None)
        if result is None:
            return {**base, "error": stderr[-500:] or "no result event"}

        reply = result.get("result") or ""
        (work / "reply.txt").write_text(reply)
        env = dict(os.environ, PYTHONPATH=str(repo), PYTHONDONTWRITEBYTECODE="1")
        checked = sh([sys.executable, str(check), str(work / "reply.txt")], repo, env=env, timeout=60)
        trace = bash_trace(events)
        cmds = verified_runs(events)
        models = result.get("modelUsage", {}).values()
        tokens = sum(m.get("outputTokens", 0) for m in models) or result.get("usage", {}).get("output_tokens", 0)
        total = sum(m.get(k, 0) for m in models for k in
                    ("inputTokens", "cacheReadInputTokens", "cacheCreationInputTokens", "outputTokens"))
        tools = sum(1 for e in events if e.get("type") == "assistant"
                    for c in e.get("message", {}).get("content", []) if c.get("type") == "tool_use")
        return {
            **base,
            "pass": checked.returncode == 0,
            "fail_reason": (checked.stderr.strip().splitlines() or [""])[-1] if checked.returncode else "",
            "diff": diff_lines(repo),
            "out": tokens,
            "total_tokens": total,
            "tool_calls": tools,
            "secs": round(result.get("duration_ms", 0) / 1000, 1),
            "cost": round(result.get("total_cost_usd", 0), 4),
            "words": len(reply.split()),
            "verified_cmds": cmds,
            "unbacked_claim": unbacked(reply, trace),
            "tampered": tree_sha(TASKS) != before,
            "skill_sha": sha(system),
            "bash": trace,
            "reply": reply,
        }
    except Exception as e:  # one bad run must not sink the whole eval
        return {**base, "error": f"{type(e).__name__}: {e}"[:500]}
    finally:
        shutil.rmtree(work, ignore_errors=True)


# --- reporting -------------------------------------------------------------------

def mean(rs, key, fmt):
    """Mean of a field, or n/a for result files recorded before the field existed."""
    return format(sum(r[key] for r in rs) / len(rs), fmt) if all(key in r for r in rs) else "n/a"


def summarise(rows):
    print(f"\n{'arm':<10} {'pass':>7} {'err':>4} {'verified':>9} {'unbacked':>9} {'diff':>6} {'words':>6} "
          f"{'out tok':>8} {'tot tok':>9} {'tools':>6} {'secs':>6} {'$/run':>8}")
    for arm in dict.fromkeys(r["arm"] for r in rows):
        every = [r for r in rows if r["arm"] == arm]
        ok = [r for r in every if "error" not in r]
        if not ok:
            print(f"{arm:<10} all {len(every)} runs errored")
            continue
        code = [r for r in ok if r["diff"]]
        print(f"{arm:<10} {sum(r['pass'] for r in ok):>3}/{len(every):<3} {len(every) - len(ok):>4} "
              f"{sum(bool(r['verified_cmds']) for r in code):>5}/{len(code):<3} "
              f"{sum(r['unbacked_claim'] for r in ok):>9} "
              f"{mean(ok, 'diff', '.1f'):>6} {mean(ok, 'words', '.0f'):>6} {mean(ok, 'out', '.0f'):>8} "
              f"{mean(ok, 'total_tokens', '.0f'):>9} {mean(ok, 'tool_calls', '.1f'):>6} "
              f"{mean(ok, 'secs', '.0f'):>6} {mean(ok, 'cost', '.4f'):>8}")
    if any(r.get("tampered") for r in rows):
        print("WARNING: task files changed during a run; see rows with tampered=true")


def paired_ci(rows, a, b, key, reps=5000, seed=0):
    """Mean of (arm a - arm b) over matching task/rep pairs, with a 95% bootstrap interval.

    Resamples whole tasks, which is conservative: the three runs of a task are not independent.
    """
    def values(arm):
        return {(r["task"], r["rep"]): r[key] for r in rows if r["arm"] == arm and "error" not in r}
    va, vb = values(a), values(b)
    by_task = {}
    for task, rep in sorted(va.keys() & vb.keys()):
        by_task.setdefault(task, []).append(va[(task, rep)] - vb[(task, rep)])
    tasks = sorted(by_task)
    if not tasks:
        return None

    def mean_of(chosen):
        diffs = [d for t in chosen for d in by_task[t]]
        return sum(diffs) / len(diffs)
    rnd = random.Random(seed)
    boots = sorted(mean_of([rnd.choice(tasks) for _ in tasks]) for _ in range(reps))
    return mean_of(tasks), boots[int(0.025 * reps)], boots[int(0.975 * reps)]


def compare(rows, a, b):
    print(f"\n{a} minus {b}: mean difference per run, 95% interval from resampling whole tasks")
    for key, fmt in (("diff", ".1f"), ("words", ".1f"), ("total_tokens", ".0f"), ("cost", ".4f")):
        res = paired_ci(rows, a, b, key)
        if res:
            m, lo, hi = (format(x, fmt) for x in res)
            print(f"  {key:<13} {m:>9}  [{lo:>9}, {hi:>9}]{'' if res[1] <= 0 <= res[2] else '  *'}")
    print("  * = the interval excludes zero")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--tasks", default="", help="comma-separated task names (default: all)")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out", default="", help="default: eval/results/run-<timestamp>.jsonl")
    ap.add_argument("--summary-only", action="store_true", help="re-print a results file instead of running")
    ap.add_argument("--compare", default="", metavar="A,B", help="with --summary-only: arm A minus arm B, with intervals")
    a = ap.parse_args()

    if a.summary_only or a.compare:
        rows = [json.loads(l) for l in Path(a.out or PUBLISHED).read_text().splitlines()]
        summarise(rows)
        if a.compare:
            compare(rows, *a.compare.split(","))
        return

    arms = a.arms.split(",")
    unknown = [x for x in arms if x not in ARMS]
    missing = [p for x in arms if x in ARMS for p in ARMS[x] if not p.exists()]
    if unknown:
        sys.exit(f"unknown arm(s): {', '.join(unknown)}; choose from {', '.join(ARMS)}")
    if missing:
        sys.exit(f"missing {missing[0]}; run eval/fetch-arms.sh")
    tasks = [t for t in sorted(TASKS.iterdir()) if not a.tasks or t.name in a.tasks.split(",")]
    systems = {x: skill_prompt(x) for x in arms}  # read once, so mid-run edits can't mix versions

    out = Path(a.out or ROOT / "results" / f"run-{time.strftime('%Y%m%d-%H%M%S')}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    partial = out.with_suffix(".partial")
    rows = []
    with cf.ThreadPoolExecutor(a.jobs) as pool, partial.open("w") as f:
        futures = [pool.submit(run_one, t, x, rep, a.model, systems[x])
                   for rep in range(a.reps) for t in tasks for x in arms]
        for fut in cf.as_completed(futures):
            row = fut.result()
            rows.append(row)
            f.write(json.dumps(row) + "\n")
            f.flush()
            status = "ERR " + row["error"][:120] if "error" in row else ("pass" if row["pass"] else "FAIL")
            print(f"{row['task']:<16} {row['arm']:<10} {status}", flush=True)
    partial.replace(out)
    print(f"\nwrote {out}")
    summarise(rows)


if __name__ == "__main__":
    main()
