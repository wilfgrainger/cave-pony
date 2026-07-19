# Cave Pony

[![CI](https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml/badge.svg)](https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Do less. Say less. Prove enough.**

Cave Pony is an open-source coding-agent skill combining two excellent ideas:

- [Ponytail](https://github.com/DietrichGebert/ponytail) reduces unnecessary implementation.
- [Caveman](https://github.com/JuliusBrussee/caveman) reduces unnecessary prose.
- Cave Pony coordinates both and requires risk-proportionate proof.

> “The best code is the code never written.” — [Ponytail `SKILL.md`](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md)
>
> “All technical substance stay. Only fluff die.” — [Caveman `SKILL.md`](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md)

This is an independently authored combination, not an official successor to either project and not endorsed by their maintainers. Both source projects are MIT licensed; see [Third-party notices](THIRD_PARTY_NOTICES.md).

## See it in 30 seconds

Request: “Add a flexible retry framework for this one HTTP call.”

### Bad

Add a dependency, retry-strategy interface, provider adapters, configuration schema and logging hooks before a second caller exists.

### Better

Check whether the existing client already retries. If it does, configure the idempotent GET. Otherwise add one bounded local retry and one regression test.

```text
Done: Used the existing retry policy for the idempotent GET.
Proof: Retry-limit test passes; existing suite passes.
Skipped: New dependency and wrapper hierarchy; revisit when a second caller needs shared policy.
Risk: POST calls remain non-retrying by design.
```

### Why

YAGNI rejects imagined requirements. KISS reuses the current architecture. DRY waits until repeated knowledge is real. The proof matches the risk.

## Coordination design

Cave Pony defines what happens when implementation minimalism and terse communication conflict:

- separate `build` and `voice` budgets;
- YAGNI and KISS before stable-knowledge DRY;
- a complexity toll for new owned surface;
- root-cause fixes instead of repeated symptom patches;
- the smallest decisive proof appropriate to the risk;
- an explicit clarity override for risky work;
- read-only audit mode.

Cave Pony makes no measured superiority claim over installing Ponytail and Caveman side by side. The current evidence is the committed behavioural contract, static regression tests and real-repository field records. A future comparative Codex study is deliberately deferred to [issue #11](https://github.com/wilfgrainger/cave-pony/issues/11).

### Context overhead

The skill text is loaded into model context when activated. Its exact token cost depends on the host and tokenizer. This overhead can be net-negative for small or already-terse tasks, so Cave Pony uses explicit activation rather than loading for every coding request.

## Coexistence

Cave Pony is intended to replace Ponytail and Caveman, not stack with them. Installing all three creates overlapping instructions and extra context cost. If all are present, Cave Pony's rules apply only while Cave Pony is active. `stop cave-pony` disables only Cave Pony; use each parent skill's own stop command for that skill. Cave Pony deliberately does not claim a global `normal mode` command.

## Behaviour

1. Understand the affected flow and trust boundaries.
2. Apply YAGNI and KISS at the footprint gate; use DRY only for stable repeated knowledge.
3. Budget standing instructions and load only needed authority.
4. Preserve semantic meaning and deterministic output.
5. Gate claims on the state that makes them true.
6. Charge every durable addition the complexity toll.
7. Fix the narrowest shared root cause.
8. Run the smallest decisive proof, expanded by risk.
9. Report Done, Proof, conditional Skipped, and Risk.

## YAGNI, KISS and DRY

Cave Pony uses these as ordered checks, not slogans:

- **YAGNI:** build only for a concrete present requirement.
- **KISS:** choose the simplest correct design that fits the existing architecture.
- **DRY:** centralise stable repeated knowledge, not merely similar-looking syntax.

Correctness and trust boundaries come first. YAGNI and KISS come before DRY because premature abstraction creates more owned surface than a small local duplication.

## More examples

### No change beats a new feature

Request: “Add a formatter option so dates display in the user's locale.”

**Bad:** add a formatting service and configuration object before checking the runtime.

**Better:** use the existing locale-aware platform formatter if it already meets the requirement.

**Why:** the footprint gate starts with existing behaviour, deletion and reuse before new code.

### Similar code is not automatically shared knowledge

Request: “These two functions look alike. Build a generic processing framework.”

**Bad:** introduce callbacks, generic types and extension points solely because the syntax is similar.

**Better:** keep two clear local implementations until the repeated rule, lifecycle and callers are semantically aligned.

**Why:** DRY protects stable knowledge from drifting; it does not reward premature abstraction.

### Stop a debugging spiral

Situation: two attempted fixes have produced the same failure.

**Bad:** add a third guard around the same symptom.

**Better:** state the assumption now in doubt and run one decisive diagnostic before editing again.

```text
Failure: request still returns 401.
Cause in doubt: the test token may not reach the handler.
Next diagnostic: log the parsed authorization header at the handler boundary.
```

**Why:** repeated failure is evidence that the working model may be wrong, not a request for more patches.

### Compression stops at destructive work

Request: “Reset my branch to `origin/main`.”

**Bad:** output only `git reset --hard origin/main`.

**Better:** state that uncommitted work will be lost, offer a preservation command, then provide the reset and recovery path.

**Why:** clarity, ordering and recovery outrank brevity at a destructive boundary.

## Real-world field evidence

Cave Pony has been used on the live [Gov Metrics](https://github.com/wilfgrainger/gov-metrics) repository. In the publication-diagnostics change it:

- rejected a new service, endpoint, store and UI;
- reused the existing publication snapshot and canary;
- reduced the first classifier implementation while retaining all required failure categories;
- left deterministic tests and passed the repository's validation stack.

Read the [publication-diagnostics field test](field-tests/2026-07-19-gov-metrics-publication-diagnostics.md) and the [YAGNI, KISS and DRY analysis](field-tests/2026-07-19-gov-metrics-yagni-kiss-dry.md).

These are practical field records, not controlled comparative results.

## Install

Current development version: `0.1.0`.

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

This tracks `main` until the first immutable tag and GitHub Release are cut. Do not describe it as a pinned release.

Manual installation:

```bash
git clone https://github.com/wilfgrainger/cave-pony.git
cp -R cave-pony/skills/cave-pony /path/to/your/agent/skills/
```

## Use

```text
/cave-pony
/cave-pony lite
/cave-pony ultra
/cave-pony build=ultra voice=lite
/cave-pony audit
stop cave-pony
```

A single level sets both axes. Advanced users can tune them independently:

| Axis | `lite` | `full` (default) | `ultra` |
|---|---|---|---|
| `build` | Build requested scope and identify a smaller option | Enforce footprint gate and complexity toll | Challenge speculative scope; prefer deletion or no change |
| `voice` | Tight full sentences | Short direct response | Minimum unambiguous words, except where clarity override applies |

## Safety under compression

Any command that deletes, overwrites, resets, force-pushes, drops, revokes, or rotates state must trigger explicit prose. Preconditions, ordering, consequences, and recovery stay visible. The committed probes in [`tests/behavioral_cases.json`](tests/behavioral_cases.json) verify the written contract and may be extended with new regression cases.

These static probes do not prove that every host model will comply. They prove the repository's intended contract and protect it from accidental drift.

## Development and testing

No runtime package or third-party development dependency is required.

```bash
make validate
make test
```

CI runs the same checks on Python 3.10 and 3.12. Static tests validate the skill contract and adversarial cases; they do not prove that every host model will obey the skill. See [Design and implementation](docs/DESIGN.md).

## Repository layout

```text
skills/cave-pony/SKILL.md    Agent-facing behaviour
skills/cave-pony/README.md   Install and command reference
tools/validate.py            Static contract validation
tests/                       Repository and adversarial contract tests
field-tests/                 Real-repository field records
docs/DESIGN.md               Design and implementation details
```

## Presentation influence

The README's concrete Bad, Better and Why teaching pattern was influenced by [`i-have-adhd`](https://github.com/ayghri/i-have-adhd). Cave Pony does not adopt that skill's universal activation, compulsory time estimates or compulsory state repetition.

## Licence

Cave Pony is released under the [MIT License](LICENSE). Attribution for Ponytail and Caveman is preserved in [Third-party notices](THIRD_PARTY_NOTICES.md).
