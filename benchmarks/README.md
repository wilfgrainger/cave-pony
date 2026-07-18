# Comparative benchmark preregistration

Status: **not run**.

This benchmark exists to test, not assume, the claim that Cave Pony's coordination layer is more useful than loading Ponytail and Caveman together.

## Source and comparability

The task names and agentic measurement approach are adapted from [Ponytail's published agentic benchmark](https://github.com/DietrichGebert/ponytail/tree/16f29800fd2681bdf24f3eb4ccffe38be3baec6b/benchmarks/agentic). Run against that pinned harness revision or record any deviation.

## Fixed protocol

- Model: Claude Haiku 4.5.
- Runs: 10 independent runs per task and arm.
- Summary: median per task and aggregate arm medians; retain every raw run.
- Arms:
  1. baseline — no skill;
  2. both-parents — Ponytail and Caveman loaded together;
  3. cave-pony — Cave Pony only;
  4. yagni-control — `Follow YAGNI principles and answer briefly.`
- Tasks: 10 published LOC-tier tasks plus `safe-path` and `critic-email`, as listed in [`manifest.json`](manifest.json).
- Metrics: source lines added, source files added, output tokens, input/context tokens, task pass rate, safety-guard retention, tests-written rate, cost, and duration.

## Preregistered kill criterion

If Cave Pony does not beat the both-parents arm on source lines added **or** output tokens, without reducing task pass rate or safety-guard retention, the coordination-performance claim is rejected. The root README must continue to describe Cave Pony as a convenience/coordination experiment rather than a proven improvement.

A win on fewer lines or tokens does not count when completeness or safety falls. Report negative and null results unchanged.

## Results contract

Commit raw machine-readable results under `benchmarks/results/`, plus a dated Markdown analysis naming model, harness commit, skill commits, task exclusions, failed cells, and measured context overhead. Do not add a comparative claim to the root README unless validation can find that committed result.

This repository does not contain a duplicate model runner. Use the pinned upstream harness and add the Cave Pony arm there for the run; duplicating the harness before a real run would add maintenance without evidence.
