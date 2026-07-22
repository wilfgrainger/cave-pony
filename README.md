<p align="center">
  <img src="assets/cave-pony-logo.png" width="320" alt="Cave Pony: an original 8-bit pony standing inside a cave">
</p>

<h1 align="center">Cave Pony</h1>

<p align="center"><strong>Do less. Say less. Prove enough.</strong></p>

<p align="center">
  <a href="https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml"><img src="https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT licence"></a>
  <img src="https://img.shields.io/badge/version-0.1.0-blue.svg" alt="Version 0.1.0">
</p>

Cave Pony is an open-source coding-agent skill for producing the **smallest trustworthy change**.

It coordinates two budgets under one hard constraint:

- **Footprint:** own as little new implementation surface as the task allows.
- **Attention:** consume as little human attention as clear communication allows.
- **Assurance:** never shrink away proof, safety, compatibility, or trust-boundary checks required by the risk.

This repository is the canonical home of Cave Pony. The copy in `wilfgrainger/agent-skills` may temporarily lag until it is synchronised.

## See it in 30 seconds

Request:

> Add a flexible retry framework for this one HTTP call.

A typical over-build adds a package, retry interface, adapters, configuration, logging hooks, and several files before a second caller exists.

Cave Pony first checks whether the existing client already retries. If it does, it configures the idempotent request. Otherwise it adds one bounded local retry and one decisive regression check.

```text
Done: Reused the existing retry policy for the idempotent GET.
Proof: Retry-limit test and existing suite pass.
Skipped: New dependency and wrapper hierarchy; revisit when a second caller needs shared policy.
Risk: POST requests remain non-retrying by design.
```

Small change. Small report. Enough evidence to trust both.

## Why it exists

[Ponytail](https://github.com/DietrichGebert/ponytail) challenges unnecessary implementation. [Caveman](https://github.com/JuliusBrussee/caveman) challenges unnecessary prose.

Using those ideas together is valuable, but two independent instruction sets do not automatically resolve their conflicts:

- terse output can hide missing proof;
- a small diff can be chosen before the affected path is understood;
- destructive or security-sensitive work can become dangerously compressed;
- separate activation rules can conflict;
- stacked instructions consume more context and can drift independently.

Cave Pony provides one independently authored coordination contract for deciding what must be built, how much must be said, and what must be proved.

It is not a fork, official successor, or endorsed project. Its influences, quotations, source snapshots, and licences are recorded in [Third-party notices](THIRD_PARTY_NOTICES.md) and [Origins and differences](docs/ORIGINS_AND_DIFFERENCES.md).

## Install

Current development version: `0.1.0`.

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

Manual installation:

```bash
git clone https://github.com/wilfgrainger/cave-pony.git
cp -R cave-pony/skills/cave-pony /path/to/your/agent/skills/
```

The command currently tracks `main`. A stable installation command pinned to an immutable tag will replace it before the public `v1.0.0` launch.

## Use

```text
/cave-pony
/cave-pony lite
/cave-pony ultra
/cave-pony build=ultra voice=lite
/cave-pony audit
stop cave-pony
```

| Axis | `lite` | `full` (default) | `ultra` |
|---|---|---|---|
| `build` | Build requested scope; name a smaller equivalent | Enforce the footprint ladder | Challenge speculative scope; prefer deletion or no change |
| `voice` | Concise full sentences | Short direct sentences or fragments | Minimum unambiguous words |

Cave Pony activates after explicit invocation or a clear request for minimalism, brevity, relief from bloat, or an audit within coding or agent work. Generic requests for a brief non-coding answer do not activate it.

It replaces rather than stacks with Ponytail and Caveman. `stop cave-pony` disables Cave Pony only.

## How it works

1. Understand the affected flow, callers, data, configuration, tests, and trust boundaries.
2. Stop at the first correct rung: no change, deletion, reuse, standard library, native platform, installed dependency, then the smallest local implementation.
3. Fix the narrowest shared root cause rather than guarding the same symptom repeatedly.
4. Run the smallest decisive proof, expanded for material risk.
5. Put the result first and report only useful Done, Proof, Skipped, and Risk lines.

YAGNI decides whether work is presently needed. KISS selects the simplest correct design. DRY centralises stable repeated knowledge, not merely similar syntax. Correctness comes first.

The full agent contract is in [`skills/cave-pony/SKILL.md`](skills/cave-pony/SKILL.md).

## Safety under compression

Commands that delete, overwrite, reset, force-push, drop, revoke, or rotate state trigger explicit prose. Preconditions, ordering, consequences, preservation, and recovery remain visible.

Cave Pony never minimises away:

- trust-boundary validation;
- authentication or authorisation;
- safe secrets handling;
- error handling needed to prevent corruption or data loss;
- accessibility;
- explicit compatibility guarantees;
- legal or operational obligations.

The behavioural probes in [`tests/behavioral_cases.json`](tests/behavioral_cases.json) protect the written contract. Static checks cannot guarantee how every host model will behave.

## Evidence

Cave Pony has been field-tested on [Gov Metrics](https://github.com/wilfgrainger/gov-metrics) publication diagnostics. It rejected a new service, endpoint, store, and UI; reused the existing snapshot and canary; reduced the first classifier implementation; and required exact-head repository proof.

Read the [field record](field-tests/2026-07-19-gov-metrics-publication-diagnostics.md). It is one practical case, not a universal performance claim.

Cave Pony does **not** yet publish a comparative benchmark claim. The preregistered launch protocol is in [Benchmark plan](docs/BENCHMARK_PLAN.md). Results, limitations, losing cases, and reproduction instructions must exist before numerical claims appear here.

## Why not install both parents?

You can. Stacking Ponytail and Caveman remains a valid choice.

Cave Pony is for users who want one smaller, coordinated contract with independent build and voice controls, one clarity override, one proof model, and explicit conflict resolution. See [Origins and differences](docs/ORIGINS_AND_DIFFERENCES.md) for the detailed comparison.

## Launch status

Cave Pony is usable today but is not yet presented as a stable `v1.0.0` release.

The launch gates cover:

- fair comparative evidence;
- immutable release and pinned installation;
- major-agent installation checks;
- attribution and branding review;
- maintainer courtesy outreach;
- external field testing;
- recovery and uninstall instructions.

Progress and release criteria are tracked in [Launch checklist](docs/LAUNCH_CHECKLIST.md).

## Development

No runtime package or third-party development dependency is required.

```bash
make validate
make test
```

CI runs the validator and tests once on Python 3.12.

```text
skills/cave-pony/SKILL.md    Agent-facing behaviour
assets/cave-pony-logo.png    Original Cave Pony identity
field-tests/                 Real-repository field records
docs/                        Design, origins, evidence, and launch gates
tests/                       Contract and safety probes
tools/validate.py            Small static contract validator
```

Contributions should demonstrate a concrete failure and the smallest evidence-backed correction. See [Contributing](CONTRIBUTING.md).

## Licence and attribution

Cave Pony is released under the [MIT License](LICENSE).

Ponytail and Caveman are MIT-licensed projects whose ideas influenced Cave Pony. Their full licence texts and copyright notices are retained in [`licenses/`](licenses/), with detailed provenance in [Third-party notices](THIRD_PARTY_NOTICES.md).

The Cave Pony name, wording, coordination model, documentation, and original 8-bit logo are independently authored for this project. No affiliation or endorsement is implied.
