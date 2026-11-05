#!/usr/bin/env python3
"""Paired eval: same tasks, same model, different skill text.

Each run copies a task repo into a fresh git dir, runs headless Claude Code
with one skill appended to the system prompt, then scores:
  pass   - hidden check passes
  diff   - lines added + removed (including new files)
  out    - output tokens
  cost   - USD reported by Claude Code
  words  - words in the final reply

Usage: python3 eval/run.py [--model M] [--reps N] [--arms a,b] [--jobs J]
Arms needing outside skills are fetched by eval/fetch-arms.sh into eval/.cache.
"""
import argparse
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys
import tempfile
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


def run_one(task, arm, rep, model):
    work = Path(tempfile.mkdtemp(prefix=f"cp-{task.name}-{arm}-"))
    repo = work / "repo"
    shutil.copytree(task / "repo", repo)
    sh(["git", "init", "-q"], repo)
    sh(["git", "add", "-A"], repo)
    sh(["git", "-c", "user.name=eval", "-c", "user.email=eval@local", "commit", "-qm", "base", "--allow-empty"], repo)

    cmd = ["claude", "-p", (task / "prompt.txt").read_text().strip(),
           "--model", model, "--output-format", "stream-json", "--verbose",
           # Sandboxed: file tools plus python only, inside a throwaway dir.
           "--permission-mode", "acceptEdits",
           "--tools", "Read,Edit,Write,Glob,Grep,Bash",
           "--allowedTools", "Read,Edit,Write,Glob,Grep,Bash(python3:*),Bash(python:*)",
           "--disable-slash-commands",
           "--strict-mcp-config", "--setting-sources", "project",
           "--no-session-persistence"]
    sp = system_prompt(arm)
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
    ran = sum(1 for e in events if e.get("type") == "assistant"
              for c in e.get("message", {}).get("content", [])
              if c.get("type") == "tool_use" and c.get("name") == "Bash")
    reply = data.get("result", "") or ""
    (work / "reply.txt").write_text(reply)

    sh(["git", "add", "-A"], repo)
    numstat = sh(["git", "diff", "--cached", "--numstat", "--", ".", ":!*__pycache__*"], repo).stdout
    diff = sum(int(a) + int(d) for a, d, _ in (l.split("\t") for l in numstat.splitlines()) if a.isdigit())

    env = dict(os.environ, PYTHONPATH=str(repo), PYTHONDONTWRITEBYTECODE="1")
    check = sh([sys.executable, str(task / "check.py"), str(work / "reply.txt")], repo, env=env, timeout=60)
    shutil.rmtree(work, ignore_errors=True)
    return {
        "task": task.name, "arm": arm, "rep": rep,
        "pass": check.returncode == 0,
        "fail_reason": (check.stderr.strip().splitlines() or [""])[-1] if check.returncode else "",
        "diff": diff,
        "out": data.get("usage", {}).get("output_tokens", 0),
        "cost": round(data.get("total_cost_usd", 0), 4),
        "words": len(reply.split()),
        "ran": ran,
        "reply": reply,
    }


def summarise(rows):
    arms = list(dict.fromkeys(r["arm"] for r in rows))
    # verified: share of code-changing runs where the agent executed anything
    print(f"\n{'arm':<10} {'pass':>7} {'verified':>9} {'diff':>6} {'words':>6} {'out tok':>8} {'cost $':>7}")
    for arm in arms:
        rs = [r for r in rows if r["arm"] == arm and "error" not in r]
        if not rs:
            continue
        n = len(rs)
        code = [r for r in rs if r["diff"]]
        ver = f"{sum(r.get('ran', 0) > 0 for r in code)}/{len(code)}"
        print(f"{arm:<10} {sum(r['pass'] for r in rs):>3}/{n:<3} {ver:>9} {sum(r['diff'] for r in rs)/n:>6.1f} "
              f"{sum(r['words'] for r in rs)/n:>6.0f} {sum(r['out'] for r in rs)/n:>8.0f} {sum(r['cost'] for r in rs):>7.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--arms", default=",".join(ARMS))
    ap.add_argument("--tasks", default="")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out", default=str(ROOT / "results" / "latest.jsonl"))
    ap.add_argument("--summary-only", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    if a.summary_only:
        summarise([json.loads(l) for l in out.read_text().splitlines()])
        return
    arms = a.arms.split(",")
    for arm in arms:
        for p in ARMS[arm]:
            if not p.exists():
                sys.exit(f"missing {p}; run eval/fetch-arms.sh")
    tasks = [t for t in sorted(TASKS.iterdir()) if not a.tasks or t.name in a.tasks.split(",")]
    jobs = [(t, arm, rep) for rep in range(a.reps) for t in tasks for arm in arms]
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with cf.ThreadPoolExecutor(a.jobs) as ex, out.open("w") as f:
        for fut in cf.as_completed([ex.submit(run_one, t, arm, rep, a.model) for t, arm, rep in jobs]):
            row = fut.result()
            rows.append(row)
            f.write(json.dumps(row) + "\n")
            f.flush()
            print(row["task"], row["arm"], row.get("pass", "ERR"), row.get("diff"), row.get("words"), row.get("error", "")[:200], flush=True)
    summarise(rows)


if __name__ == "__main__":
    main()
