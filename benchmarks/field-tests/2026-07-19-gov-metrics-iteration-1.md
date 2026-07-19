# Gov Metrics field test — iteration 1

Date: 2026-07-19  
Target: `wilfgrainger/gov-metrics` at `bb2a6140f047633577a3305196dcff2bd781f2a7`  
Mode: Cave Pony `build=full voice=full`

## Scope

Review the repository's standing agent guidance as a real primary-skill test. No public application or evidence values were changed.

## Finding

The repository required a second 325-line master skill, two reference prompts totalling 438 lines, `AGENTS.md`, every `.agents` file and a standing review council before task work. The copied architecture reference had drifted from current steering: it still described scheduled GitHub Actions and an older Worker boundary.

Cave Pony found the files through its generic footprint gate and complexity toll, but the skill did not explicitly say that agent instructions and mandatory reading are owned context surface.

## Smallest correction

Gov Metrics PR #258:

- makes Cave Pony the sole primary skill;
- keeps a short repository domain profile in `AGENTS.md`;
- loads only affected code and the smallest authoritative guidance needed;
- deletes the layered master skill and both references;
- replaces tests that required the prompt stack with a bounded-context contract.

## Objective footprint

| Measure | Before | After |
| --- | ---: | ---: |
| Layered repository skill/reference lines | 763 | 0 |
| Standing guidance files required before task work | at least 5, plus every `.agents` file | 2 entry files, then task-relevant sources only |
| PR additions | — | 144 |
| PR deletions | — | 953 |
| Runtime dependencies added | — | 0 |
| Public output changed | — | no |

These are repository diff and instruction-surface measurements, not a model-token benchmark. Actual input-token, output-token and pass-rate comparisons remain governed by the separate preregistered benchmark.

## Feedback applied to Cave Pony

Added an explicit instruction-budget rule:

- standing prompts, skills, memory, personas and checklists count as owned surface;
- one primary skill plus a short repository profile is the default;
- overlapping skills and read-everything startup sequences are rejected;
- stale instruction copies are removed rather than reconciled on every future run;
- mandatory context sources must pay the complexity toll.

## Residual risk

The Gov Metrics pull request still requires exact-head CI before merge. This field test shows a concrete simplification result; it does not yet prove Cave Pony outperforms both parent skills across the preregistered coding benchmark.
