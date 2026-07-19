#!/usr/bin/env python3
"""Run the pinned Ponytail agentic benchmark through Codex CLI."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BENCH = Path(__file__).resolve().parent
MANIFEST = json.loads((BENCH / "manifest.json").read_text(encoding="utf-8"))
RUNS_DIR = BENCH / "runs"
CELL_TIMEOUT = 900
MODEL_ID = ""
REASONING_EFFORT = "high"
CODEX_BIN = ""

NEUTRAL = """Benchmark constraints:
- Edit only the supplied workspace.
- Implement the requested task.
- Include tests only if you normally would for a change like this.
- Do not install dependencies, start a development server, open a browser, or use network access.
- Finish after writing the implementation. The harness scores the resulting files independently.
"""

ARM_PATHS = {
    "ponytail": BENCH / "arms" / "ponytail-SKILL.md",
    "caveman": BENCH / "arms" / "caveman-SKILL.md",
    "cave-pony": ROOT / "skills" / "cave-pony" / "SKILL.md",
}
ARM_ACTIVATION = {
    "baseline": "",
    "both-parents": "/ponytail full\n/caveman full",
    "cave-pony": "/cave-pony",
    "yagni-control": "Follow YAGNI principles and answer briefly.",
}
STREAM_LAG = re.compile(
    r"^in-process app-server event stream lagged; dropped \d+ events?$",
    re.IGNORECASE,
)


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def verify_inputs(upstream_root: Path) -> None:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=upstream_root,
        capture_output=True,
        text=True,
        check=False,
    )
    actual = proc.stdout.strip()
    expected = MANIFEST["upstream_harness"]["commit"]
    if proc.returncode or actual != expected:
        raise SystemExit(
            f"Ponytail checkout must be exactly {expected}; found {actual or 'unreadable'}"
        )
    for name, spec in MANIFEST["arm_sources"].items():
        path = ROOT / spec["path"]
        if not path.is_file():
            raise SystemExit(f"missing arm snapshot: {path}")
        actual_blob = git_blob_sha(path)
        if actual_blob != spec["blob_sha"]:
            raise SystemExit(
                f"{name} arm drifted: expected {spec['blob_sha']}, got {actual_blob}"
            )


def load_upstream(upstream_root: Path):
    agentic = upstream_root / MANIFEST["upstream_harness"]["path"]
    run_py = agentic / "run.py"
    if not run_py.is_file():
        raise SystemExit(f"upstream harness not found: {run_py}")
    sys.path.insert(0, str(agentic))
    spec = importlib.util.spec_from_file_location("ponytail_agentic_run", run_py)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot import upstream harness: {run_py}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module._selftest_plugin_dir = lambda: 0
    module.RUNS_DIR = RUNS_DIR
    return module


def arm_document(arm: str) -> str:
    if arm == "baseline":
        return NEUTRAL
    if arm == "yagni-control":
        return f"{NEUTRAL}\n{ARM_ACTIVATION[arm]}\n"
    if arm == "cave-pony":
        return f"{NEUTRAL}\n{ARM_PATHS['cave-pony'].read_text(encoding='utf-8')}"
    if arm == "both-parents":
        return (
            f"{NEUTRAL}\n"
            f"{ARM_PATHS['ponytail'].read_text(encoding='utf-8')}\n\n"
            f"{ARM_PATHS['caveman'].read_text(encoding='utf-8')}"
        )
    raise ValueError(f"unknown arm: {arm}")


def prompt_for(task_prompt: str, arm: str) -> str:
    return "\n\n".join(
        part for part in (ARM_ACTIVATION[arm], task_prompt, NEUTRAL) if part
    )


def codex_command(prompt: str, last_message: Path) -> list[str]:
    return [
        CODEX_BIN,
        "exec",
        "--ephemeral",
        "--json",
        "--ignore-user-config",
        "--ignore-rules",
        "--sandbox",
        "workspace-write",
        "--color",
        "never",
        "--model",
        MODEL_ID,
        "-c",
        f"model_reasoning_effort={REASONING_EFFORT}",
        "--output-last-message",
        str(last_message),
        prompt,
    ]


def parse_jsonl(events_path: Path, last_message_path: Path) -> dict[str, Any]:
    usage = {
        "input_tokens": None,
        "cached_input_tokens": None,
        "output_tokens": None,
        "reasoning_output_tokens": None,
    }
    last_message = ""
    turns = 0
    errors: list[str] = []
    warnings: list[str] = []

    if events_path.is_file():
        for line in events_path.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                errors.append("invalid JSONL event")
                continue
            event_type = event.get("type")
            if event_type == "turn.completed":
                turns += 1
                event_usage = event.get("usage") or {}
                for key in usage:
                    if isinstance(event_usage.get(key), int):
                        usage[key] = event_usage[key]
            elif event_type in {"error", "turn.failed"}:
                errors.append(str(event.get("message") or event.get("error") or event_type))
            elif event_type == "item.completed":
                item = event.get("item") or {}
                if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
                    last_message = item["text"]
                elif item.get("type") == "error":
                    message = str(item.get("message") or "item error")
                    if STREAM_LAG.match(message):
                        warnings.append(message)
                    else:
                        errors.append(message)

    if last_message_path.is_file():
        saved = last_message_path.read_text(
            encoding="utf-8", errors="replace"
        ).strip()
        if saved:
            last_message = saved

    return {
        "runner_ok": turns > 0 and not errors,
        "turns": turns,
        "runner_errors": errors,
        "runner_warnings": warnings,
        "result_text": last_message,
        "output_chars": len(last_message),
        "in_tokens": usage["input_tokens"],
        "cache_tokens": usage["cached_input_tokens"],
        "out_tokens": usage["output_tokens"],
        "reasoning_output_tokens": usage["reasoning_output_tokens"],
    }


def seed_workspace(upstream, task_id: str, arm: str, workdir: Path) -> None:
    task = upstream.TASKS[task_id]
    if task.get("fixture"):
        fixture = Path(task["fixture"])
        if not fixture.is_absolute():
            fixture = Path(upstream.__file__).resolve().parent / "fixtures" / task["fixture"]
        shutil.copytree(
            fixture,
            workdir,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(
                "node_modules",
                ".git",
                "build",
                "dist",
                "dist-ssr",
                ".vite",
                "*.log",
                "__pycache__",
                "storage",
                ".venv",
                "venv",
                ".pytest_cache",
                "*.mp4",
                "*.mp3",
                "*.wav",
                "*.mov",
                "*service-account*.json",
                "nul",
                "con",
                "prn",
                "aux",
                "DatePicker*.tsx",
                "DatePicker*.jsx",
            ),
        )
        fixture_files = sorted(
            str(path.relative_to(workdir)).replace("\\", "/")
            for path in workdir.rglob("*")
            if path.is_file()
        )
        (workdir / "_fixture_files.json").write_text(
            json.dumps(fixture_files), encoding="utf-8"
        )
    for filename, content in task.get("seed", {}).items():
        target = workdir / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    for agents in workdir.rglob("AGENTS.md"):
        agents.unlink()
    (workdir / "AGENTS.md").write_text(arm_document(arm), encoding="utf-8")
    upstream._git_snapshot(workdir)


def score_workspace(upstream, task_id: str, arm: str, model: str, workdir: Path):
    parsed = parse_jsonl(workdir / "_codex.jsonl", workdir / "_codex.last.txt")
    result_text = parsed.pop("result_text")
    task = upstream.TASKS[task_id]
    surgical = not task.get("open") and not task.get("fixture")
    stats = (
        upstream.git_diff_stats(workdir)
        if task.get("fixture")
        else upstream.code_stats(workdir, selfcheck_as_test=surgical)
    )
    if task.get("open") and stats["total_loc"] == 0 and result_text:
        total, code = upstream.chat_code_loc(result_text)
        stats = {
            **stats,
            "total_loc": total,
            "src_loc": code,
            "src_files": 1 if total else 0,
        }
    if not parsed["runner_ok"]:
        scored = {"correct": 0, "safe": 0, "reason": "codex-runner-failed"}
    elif task.get("fixture"):
        scored = {
            "correct": 1 if stats.get("total_loc", 0) > 0 else 0,
            "safe": 1,
            "reason": "git-diff",
        }
    else:
        scored = task["score"](workdir)
    diff = subprocess.run(
        ["git", "diff", "--binary", "HEAD"],
        cwd=workdir,
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    (workdir / "_git.diff").write_text(diff, encoding="utf-8")
    meta_path = workdir / "_codex.meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    return {
        "task": task_id,
        "arm": arm,
        "model": MODEL_ID,
        **scored,
        **stats,
        **parsed,
        **meta,
        "cost": None,
        "result_sha256": hashlib.sha256(result_text.encode()).hexdigest(),
    }


def run_cell(upstream, task_id: str, arm: str, model: str, workdir: Path):
    seed_workspace(upstream, task_id, arm, workdir)
    command = codex_command(
        prompt_for(upstream.TASKS[task_id]["prompt"], arm),
        workdir / "_codex.last.txt",
    )
    (workdir / "_codex.command.json").write_text(
        json.dumps(command, indent=2) + "\n", encoding="utf-8"
    )
    started = time.monotonic()
    exit_code = -1
    with (workdir / "_codex.jsonl").open("wb") as stdout, (
        workdir / "_codex.stderr.txt"
    ).open("wb") as stderr:
        process = subprocess.Popen(
            command,
            cwd=workdir,
            stdout=stdout,
            stderr=stderr,
            start_new_session=(os.name != "nt"),
        )
        try:
            exit_code = process.wait(timeout=CELL_TIMEOUT)
        except subprocess.TimeoutExpired:
            upstream._tree_kill(process)
            stderr.write(f"\n[KILLED after {CELL_TIMEOUT}s]\n".encode())
    duration_ms = round((time.monotonic() - started) * 1000)
    (workdir / "_codex.meta.json").write_text(
        json.dumps(
            {
                "duration_ms": duration_ms,
                "exit_code": exit_code,
                "requested_model": MODEL_ID,
                "reasoning_effort": REASONING_EFFORT,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return score_workspace(upstream, task_id, arm, model, workdir)


def preflight() -> None:
    with tempfile.TemporaryDirectory(prefix="cave-pony-codex-") as temp:
        workdir = Path(temp)
        subprocess.run(["git", "init", "-q"], cwd=workdir, check=True)
        (workdir / "AGENTS.md").write_text(NEUTRAL, encoding="utf-8")
        last = workdir / "last.txt"
        with (workdir / "events.jsonl").open("wb") as stdout, (
            workdir / "stderr.txt"
        ).open("wb") as stderr:
            proc = subprocess.run(
                codex_command(
                    "Reply exactly CODEX_BENCHMARK_READY. Do not edit files.",
                    last,
                ),
                cwd=workdir,
                stdout=stdout,
                stderr=stderr,
                timeout=180,
                check=False,
            )
        parsed = parse_jsonl(workdir / "events.jsonl", last)
        if (
            proc.returncode != 0
            or not parsed["runner_ok"]
            or parsed["result_text"].strip() != "CODEX_BENCHMARK_READY"
        ):
            raise SystemExit(
                "Codex preflight failed. Run `codex login status`, verify the model, and retry."
            )


def rewrite_latest_result(started: float) -> None:
    candidates = [
        path
        for path in RUNS_DIR.glob("*")
        if path.is_dir() and path.stat().st_mtime >= started - 2
    ]
    if not candidates:
        return
    latest = max(candidates, key=lambda path: path.stat().st_mtime)
    results_path = latest / "results.json"
    if not results_path.is_file():
        return
    data = json.loads(results_path.read_text(encoding="utf-8"))
    version = subprocess.run(
        [CODEX_BIN, "--version"], capture_output=True, text=True, check=False
    )
    data["codex"] = {
        "version": (version.stdout or version.stderr).strip(),
        "model": MODEL_ID,
        "reasoning_effort": REASONING_EFFORT,
        "authentication": "ChatGPT login",
    }
    data.pop("claude", None)
    results_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    global MODEL_ID, REASONING_EFFORT, CODEX_BIN

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--codex-model")
    parser.add_argument(
        "--reasoning-effort", default=MANIFEST["codex"]["reasoning_effort"]
    )
    own, remaining = parser.parse_known_args()

    upstream_root = own.upstream.resolve()
    verify_inputs(upstream_root)
    upstream = load_upstream(upstream_root)
    upstream.ARMS = {
        "baseline": lambda: None,
        "both-parents": lambda: None,
        "cave-pony": lambda: None,
        "yagni-control": lambda: None,
    }
    upstream.PLUGIN_ARMS = ()
    upstream.score_workspace = lambda task, arm, model, workdir: score_workspace(
        upstream, task, arm, model, workdir
    )
    upstream.run_cell = lambda task, arm, model, workdir: run_cell(
        upstream, task, arm, model, workdir
    )

    live = "--selftest" not in remaining and "--rescore" not in remaining
    if live:
        MODEL_ID = own.codex_model or os.environ.get("CODEX_BENCH_MODEL", "")
        if not MODEL_ID:
            raise SystemExit(
                "set --codex-model or CODEX_BENCH_MODEL to the exact model identifier"
            )
        REASONING_EFFORT = own.reasoning_effort
        CODEX_BIN = shutil.which("codex") or ""
        if not CODEX_BIN:
            raise SystemExit("codex CLI not found on PATH")
        upstream.MODELS = {"codex": MODEL_ID}
        if not any(arg in {"--model", "--models"} for arg in remaining):
            remaining += ["--model", "codex"]
        if "--runs" not in remaining:
            remaining += ["--runs", str(MANIFEST["runs_per_cell"])]
        if "--workers" not in remaining:
            remaining += ["--workers", "1"]
        preflight()
        upstream._claude_version = lambda: f"codex {MODEL_ID}"
    else:
        upstream.MODELS = {"codex": own.codex_model or "codex"}
        upstream._claude_version = lambda: "codex offline-rescore"

    started = time.time()
    sys.argv = [sys.argv[0], *remaining]
    upstream.main()
    if live:
        rewrite_latest_result(started)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
