# Comparative benchmark preregistration

Status: **not run**.

This benchmark tests, rather than assumes, that Cave Pony coordinates implementation minimalism and terse communication better than loading Ponytail and Caveman together.

## Preregistration change before first run

The original protocol named Claude Haiku 4.5 because Ponytail's published harness used Claude Code. Before any Cave Pony comparative cell was run, the execution engine was changed to Codex CLI authenticated with ChatGPT. There are no discarded or pilot comparative results behind this change.

The tasks, arms, run count, metrics and kill criterion remain fixed. The exact Codex CLI version, explicit model identifier and reasoning effort must be recorded with the results.

## Source and comparability

The task definitions, seeded workspaces, deterministic safety checks, code-size scoring and aggregation are reused from [Ponytail's agentic benchmark](https://github.com/DietrichGebert/ponytail/tree/16f29800fd2681bdf24f3eb4ccffe38be3baec6b/benchmarks/agentic) at commit `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`.

[`run_codex.py`](run_codex.py) is an adapter, not a second scoring implementation. It imports that pinned harness, replaces only the agent invocation and result parsing, and refuses a different upstream commit.

## Fixed protocol

- Runner: `codex exec`, authenticated through ChatGPT login.
- Model: one explicit Codex model identifier for every cell, supplied with `--codex-model` or `CODEX_BENCH_MODEL` and retained in the raw results.
- Reasoning effort: `high`.
- Runs: 10 independent runs per task and arm.
- Summary: median per task and aggregate arm medians; retain every raw run.
- Arms:
  1. `baseline` — neutral benchmark constraints only;
  2. `both-parents` — pinned Ponytail and Caveman skill snapshots, explicitly activated;
  3. `cave-pony` — the pinned Cave Pony skill, explicitly activated;
  4. `yagni-control` — `Follow YAGNI principles and answer briefly.`
- Tasks: 10 published LOC-tier tasks plus `safe-path` and `critic-email`, exactly as listed in [`manifest.json`](manifest.json).
- Metrics: source lines and files added, input/cached/output tokens, output characters, correctness, safety retention, tests-written rate, duration and runner-failure rate.
- Cost: not reported because ChatGPT-plan Codex runs do not expose a reliable per-cell dollar cost.

Each cell gets a fresh git workspace and fresh Codex session. The adapter removes inherited `AGENTS.md` files, writes exactly one arm-specific `AGENTS.md`, then runs Codex with:

```text
--ephemeral --json --ignore-user-config --ignore-rules --sandbox workspace-write
```

Raw JSONL, stderr, final message, command, git diff and scored workspace remain under `benchmarks/runs/<timestamp>/`.

## Preregistered kill criterion

If Cave Pony does not beat the `both-parents` arm on source lines added **or** output tokens, without reducing task pass rate or safety-guard retention, reject the coordination-performance claim. The root README must continue to describe Cave Pony as a convenience and coordination experiment rather than a proven improvement.

A win on fewer lines or tokens does not count when completeness or safety falls. Publish negative and null results unchanged.

## Setup

Install the current Codex CLI and sign in with the ChatGPT account that will fund the runs:

```bash
npm install -g @openai/codex
codex login
codex login status
```

Prepare the pinned upstream harness and its real-repository fixture:

```bash
git clone https://github.com/DietrichGebert/ponytail.git
cd ponytail
git checkout 16f29800fd2681bdf24f3eb4ccffe38be3baec6b

cd ..
git clone https://github.com/fastapi/full-stack-fastapi-template.git
cd full-stack-fastapi-template
git checkout cd83fc1
export PONYTAIL_TMPL="$PWD"
cd ..
```

Validate the deterministic instruments without using Codex:

```bash
python cave-pony/benchmarks/run_codex.py \
  --upstream ./ponytail \
  --selftest
```

Run a one-cell smoke test before committing to the full matrix:

```bash
python cave-pony/benchmarks/run_codex.py \
  --upstream ./ponytail \
  --codex-model '<exact model identifier accepted by your Codex CLI>' \
  --task safe-path \
  --arms cave-pony \
  --runs 1 \
  --workers 1
```

Run the preregistered 480-cell matrix:

```bash
python cave-pony/benchmarks/run_codex.py \
  --upstream ./ponytail \
  --codex-model '<same exact model identifier>' \
  --task tmpl-fe-datepicker,tmpl-fe-colorpicker,tmpl-fe-command,tmpl-fe-dropzone,tmpl-fe-wizard,tmpl-fe-rating,tmpl-be-duplicate,tmpl-be-search,tmpl-be-bulkdelete,tmpl-be-csv,safe-path,critic-email \
  --arms baseline,both-parents,cave-pony,yagni-control \
  --runs 10 \
  --workers 1
```

The adapter performs a live `CODEX_BENCHMARK_READY` preflight before starting cells. It treats a completed turn as success even when Codex emits the known non-fatal app-server stream-lag warning, but top-level errors, failed turns and other item errors fail the cell.

## Results contract

Commit machine-readable `results.json` and `summary.json` under `benchmarks/results/`, plus a dated Markdown analysis naming:

- Codex CLI version, exact model identifier and reasoning effort;
- upstream harness and skill snapshot hashes;
- task exclusions or failed cells;
- measured context overhead;
- any deviation from this protocol.

Retain the full raw run directory and publish its archive or durable location with a SHA-256 digest. Do not add a comparative claim to the root README unless validation can find committed results and the kill criterion passes.
