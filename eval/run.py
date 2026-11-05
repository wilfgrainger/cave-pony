#!/usr/bin/env python3
"""Paired eval: same tasks, same model, different skill text.

Each run copies a task repo into a fresh git dir, runs headless Claude Code
with one skill appended to the system prompt, then scores:
  pass      - hidden check passes (errored runs count as failures)
  verified  - code-changing runs that successfully ran python/pytest after the first edit
  unbacked  - replies claiming success ("tests pass", "verified"...) with no such command
  diff      - lines added + removed (including new files)
  words     - words in the final reply
  out tok   - output tokens, whole session
  $/run     - USD reported by Claude Code

Usage: python3 eval/run.py [--model M] [--reps N] [--arms a,b] [--tasks t] [--jobs J] [--out F]
Arms needing outside skills are fetched by eval/fetch-arms.sh into eval/.cache.
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

ARMS = {
    "baseline": [],
    "caveman": [CACHE / "caveman/skills/caveman/SKILL.md"],
    "ponytail": [CACHE / "ponytail/skills/ponytail/SKILL.md"],
    "both": [CACHE / "caveman/skills/caveman/SKILL.md", CACHE / "ponytail/skills/ponytail/SKILL.md"],
    "cave-pony": [ROOT.parent / "skills/cave-pony/SKILL.md"],
}


def system_prompt(arm):
    parts = [p.read_text() for p in ARMS[arm]]
    if not parts:
        return None
    return "These skills are active for this whole session. Follow them.\n\n" + "\n\n---\n\n".join(parts)


def sh(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kw)


def tree_hash(path):
    h = hashlib.sha256()
    for f in sorted(path.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            h.update(str(f.relative_to(path)).encode() + f.read_bytes())
    return h.hexdigest()[:12]


CLAIM = re.compile(r"\b(tests? pass(es|ed)?|passes|passed|verified|confirmed|works now)\b", re.I)


EDITS = re.compile(r"(^|[^0-9&])>>?\s*[\w./-]|\btee\b|\bsed\s+-i|\.write(_text)?\(")


def bash_trace(events):
    """Every Bash command in order, with whether it succeeded and whether the agent had edited by then."""
    results = {c.get("tool_use_id"): c for e in events if e.get("type") == "user"
               for c in (e.get("message", {}).get("content") or []) if isinstance(c, dict) and c.get("type") == "tool_result"}
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
                edited = edited or bool(EDITS.search(cmd))  # heredoc or redirect edits count too
                res = results.get(c.get("id"))
                trace.append({"cmd": cmd, "ok": bool(res) and not res.get("is_error"), "after_edit": edited})
    return trace


def verified_runs(events):
    """Successful python/pytest commands run after (or together with) the agent's first edit."""
    return [t["cmd"] for t in bash_trace(events)
            if t["ok"] and t["after_edit"] and re.search(r"\b(python3?|pytest)\b", t["cmd"])]


def run_one(task, arm, rep, model, sp):
    try:
        return _run_one(task, arm, rep, model, sp)
    except Exception as e:  # one bad run must not sink the whole eval
        return {"task": task.name, "arm": arm, "rep": rep, "error": f"{type(e).__name__}: {e}"[:500]}


def _run_one(task, arm, rep, model, sp):
    work = Path(tempfile.mkdtemp(prefix=f"cp-{task.name}-{arm}-"))
    try:
        repo = work / "repo"
        shutil.copytree(task / "repo", repo)
        # The hidden check runs from a private copy, so edits elsewhere cannot change scoring.
        check_py = work / "check.py"
        shutil.copy(task / "check.py", check_py)
        sh(["git", "init", "-q"], repo)
        sh(["git", "add", "-A"], repo)
        sh(["git", "-c", "user.name=eval", "-c", "user.email=eval@local", "commit", "-qm", "base", "--allow-empty"], repo)
        before = tree_hash(TASKS)

        cmd = ["claude", "-p", (task / "prompt.txt").read_text().strip(),
               "--model", model, "--output-format", "stream-json", "--verbose",
               # Not a sandbox: python can still touch the host. Tools are limited to
               # file edits plus python so every arm has the same narrow surface.
               "--permission-mode", "acceptEdits",
               "--tools", "Read,Edit,Write,Glob,Grep,Bash",
               "--allowedTools", "Read,Edit,Write,Glob,Grep,Bash(python3:*),Bash(python:*)",
               "--disable-slash-commands",
               "--strict-mcp-config", "--setting-sources", "project",
               "--no-session-persistence"]
        if sp:
            cmd += ["--append-system-prompt", sp]
        r = sh(cmd, repo, timeout=900)
        events = []
        for line in r.stdout.splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        data = next((e for e in events if e.get("type") == "result"), None)
        if data is None:
            return {"task": task.name, "arm": arm, "rep": rep, "error": (r.stderr or r.stdout)[-500:]}
        reply = data.get("result", "") or ""
        reply_file = work / "reply.txt"
        reply_file.write_text(reply)

        sh(["git", "add", "-A"], repo)
        numstat = sh(["git", "diff", "--cached", "--numstat", "--", ".", ":!*__pycache__*"], repo).stdout
        diff = sum(int(a) + int(d) for a, d, _ in (l.split("\t") for l in numstat.splitlines()) if a.isdigit())

        env = dict(os.environ, PYTHONPATH=str(repo), PYTHONDONTWRITEBYTECODE="1")
        check = sh([sys.executable, str(check_py), str(reply_file)], repo, env=env, timeout=60)
        cmds = verified_runs(events)
        # Session total across every model call, not just the last turn.
        out_tokens = sum(m.get("outputTokens", 0) for m in data.get("modelUsage", {}).values()) \
            or data.get("usage", {}).get("output_tokens", 0)
        return {
            "task": task.name, "arm": arm, "rep": rep,
            "pass": check.returncode == 0,
            "fail_reason": (check.stderr.strip().splitlines() or [""])[-1] if check.returncode else "",
            "diff": diff,
            "out": out_tokens,
            "cost": round(data.get("total_cost_usd", 0), 4),
            "words": len(reply.split()),
            "verified_cmds": cmds,
            "bash": bash_trace(events),  # full trace, so scoring can be revised without re-running
            "unbacked_claim": bool(CLAIM.search(reply)) and not cmds,
            "tampered": tree_hash(TASKS) != before,
            "skill_sha": hashlib.sha256((sp or "").encode()).hexdigest()[:12],
            "reply": reply,
        }
    finally:
        shutil.rmtree(work, ignore_errors=True)


def summarise(rows):
    arms = list(dict.fromkeys(r["arm"] for r in rows))
    print(f"\n{'arm':<10} {'pass':>7} {'err':>4} {'verified':>9} {'unbacked':>9} {'diff':>6} {'words':>6} {'out tok':>8} {'$/run':>7}")
    for arm in arms:
        allr = [r for r in rows if r["arm"] == arm]
        rs = [r for r in allr if "error" not in r]
        if not rs:
            continue
        n = len(rs)
        code = [r for r in rs if r["diff"]]
        new = all("verified_cmds" in r for r in rs)  # older result files lack these fields
        ver = f"{sum(bool(r['verified_cmds']) for r in code)}/{len(code)}" if new else "n/a"
        unb = f"{sum(r['unbacked_claim'] for r in rs)}" if new else "n/a"
        print(f"{arm:<10} {sum(r['pass'] for r in rs):>3}/{len(allr):<3} {len(allr) - n:>4} {ver:>9} {unb:>9} "
              f"{sum(r['diff'] for r in rs)/n:>6.1f} {sum(r['words'] for r in rs)/n:>6.0f} "
              f"{sum(r['out'] for r in rs)/n:>8.0f} {sum(r['cost'] for r in rs)/n:>7.3f}")
    if any(r.get("tampered") for r in rows):
        print("WARNING: task files changed during a run; see 'tampered' rows")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--tasks", default="")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out", default="", help="default: eval/results/run-<timestamp>.jsonl")
    ap.add_argument("--summary-only", action="store_true")
    a = ap.parse_args()
    if a.summary_only:
        out = Path(a.out or ROOT / "results" / "published.jsonl")
        summarise([json.loads(l) for l in out.read_text().splitlines()])
        return
    out = Path(a.out or ROOT / "results" / f"run-{time.strftime('%Y%m%d-%H%M%S')}.jsonl")
    arms = a.arms.split(",")
    for arm in arms:
        for p in ARMS[arm]:
            if not p.exists():
                sys.exit(f"missing {p}; run eval/fetch-arms.sh")
    prompts = {arm: system_prompt(arm) for arm in arms}  # read once: mid-run edits cannot mix versions
    tasks = [t for t in sorted(TASKS.iterdir()) if not a.tasks or t.name in a.tasks.split(",")]
    jobs = [(t, arm, rep) for rep in range(a.reps) for t in tasks for arm in arms]
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    tmp = out.with_suffix(".partial")
    with cf.ThreadPoolExecutor(a.jobs) as ex, tmp.open("w") as f:
        futs = [ex.submit(run_one, t, arm, rep, a.model, prompts[arm]) for t, arm, rep in jobs]
        for fut in cf.as_completed(futs):
            row = fut.result()
            rows.append(row)
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(row["task"], row["arm"], row.get("pass", "ERR"), row.get("diff"), row.get("words"),
                  len(row.get("verified_cmds", [])), row.get("error", "")[:200], flush=True)
    tmp.replace(out)
    print(f"\nwrote {out}")
    summarise(rows)


if __name__ == "__main__":
    main()
