#!/usr/bin/env python3
"""Paired eval for coding-agent skills.

Every task runs through headless Claude Code once per arm: the same model, tools and
prompt, with only the appended skill text changing. Each run is scored on:

  pass      hidden check passes (an errored run counts as a failure)
  verified  ran python/pytest successfully after editing (code-changing runs only)
  unbacked  reply claims success ("tests pass", "verified") but nothing ran; rough regex flag
  diff      lines added + removed, new files included
  words     words in the final reply
  out tok   output tokens across the whole session
  $/run     cost reported by Claude Code

Usage:
  eval/fetch-arms.sh                       # once: pinned Caveman and Ponytail
  python3 eval/run.py                      # all tasks x all arms x 3 reps (~$2)
  python3 eval/run.py --tasks dedupe --arms baseline,cave-pony --reps 1
  python3 eval/run.py --summary-only       # re-print eval/results/published.jsonl

Not a sandbox: the agent gets file tools plus python, and python can reach the host.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
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
    "caveman": [CAVEMAN],
    "ponytail": [PONYTAIL],
    "both": [CAVEMAN, PONYTAIL],
    "cave-pony": [ROOT.parent / "skills/cave-pony/SKILL.md"],
}

TOOLS = "Read,Edit,Write,Glob,Grep,Bash"
ALLOWED = "Read,Edit,Write,Glob,Grep,Bash(python3:*),Bash(python:*)"

EDIT_CMD = re.compile(r"(^|[^0-9&])>>?\s*[\w./-]|\btee\b|\bsed\s+-i|\.write(_text)?\(")
RUNS_CODE = re.compile(r"\b(python3?|pytest)\b")
CLAIM = re.compile(r"\b(tests? pass(es|ed)?|passes|passed|verified|confirmed|works now)\b", re.I)


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
        cmds = verified_runs(events)
        tokens = sum(m.get("outputTokens", 0) for m in result.get("modelUsage", {}).values()) \
            or result.get("usage", {}).get("output_tokens", 0)
        return {
            **base,
            "pass": checked.returncode == 0,
            "fail_reason": (checked.stderr.strip().splitlines() or [""])[-1] if checked.returncode else "",
            "diff": diff_lines(repo),
            "out": tokens,
            "cost": round(result.get("total_cost_usd", 0), 4),
            "words": len(reply.split()),
            "verified_cmds": cmds,
            "unbacked_claim": bool(CLAIM.search(reply)) and not cmds,
            "tampered": tree_sha(TASKS) != before,
            "skill_sha": sha(system),
            "bash": bash_trace(events),
            "reply": reply,
        }
    except Exception as e:  # one bad run must not sink the whole eval
        return {**base, "error": f"{type(e).__name__}: {e}"[:500]}
    finally:
        shutil.rmtree(work, ignore_errors=True)


# --- reporting -------------------------------------------------------------------

def summarise(rows):
    print(f"\n{'arm':<10} {'pass':>7} {'err':>4} {'verified':>9} {'unbacked':>9} "
          f"{'diff':>6} {'words':>6} {'out tok':>8} {'$/run':>7}")
    for arm in dict.fromkeys(r["arm"] for r in rows):
        every = [r for r in rows if r["arm"] == arm]
        ok = [r for r in every if "error" not in r]
        if not ok:
            print(f"{arm:<10} all {len(every)} runs errored")
            continue
        n, code = len(ok), [r for r in ok if r["diff"]]
        print(f"{arm:<10} {sum(r['pass'] for r in ok):>3}/{len(every):<3} {len(every) - n:>4} "
              f"{sum(bool(r['verified_cmds']) for r in code):>5}/{len(code):<3} "
              f"{sum(r['unbacked_claim'] for r in ok):>9} "
              f"{sum(r['diff'] for r in ok) / n:>6.1f} {sum(r['words'] for r in ok) / n:>6.0f} "
              f"{sum(r['out'] for r in ok) / n:>8.0f} {sum(r['cost'] for r in ok) / n:>7.3f}")
    if any(r.get("tampered") for r in rows):
        print("WARNING: task files changed during a run; see rows with tampered=true")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--tasks", default="", help="comma-separated task names (default: all)")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out", default="", help="default: eval/results/run-<timestamp>.jsonl")
    ap.add_argument("--summary-only", action="store_true")
    a = ap.parse_args()

    if a.summary_only:
        summarise([json.loads(l) for l in Path(a.out or PUBLISHED).read_text().splitlines()])
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
