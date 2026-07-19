# Cave Pony

[![CI](https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml/badge.svg)](https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Do less. Say less. Prove enough.**

Cave Pony is an open-source coding-agent skill combining two ideas:

- [Ponytail](https://github.com/DietrichGebert/ponytail): reduce unnecessary implementation.
- [Caveman](https://github.com/JuliusBrussee/caveman): reduce unnecessary prose.
- Cave Pony: coordinate both and keep proof proportional to risk.

> “The best code is the code never written.” — [Ponytail `SKILL.md`](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md)
>
> “All technical substance stay. Only fluff die.” — [Caveman `SKILL.md`](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md)

This is independently authored, not an official successor to either project and not endorsed by their maintainers. Both source projects are MIT licensed; see [Third-party notices](THIRD_PARTY_NOTICES.md).

## See it in 30 seconds

Request: “Add a flexible retry framework for this one HTTP call.”

### Bad

Add a dependency, retry interface, provider adapters, configuration schema, and logging hooks before a second caller exists.

### Better

Check whether the existing client already retries. If it does, configure the idempotent GET. Otherwise add one bounded local retry and one regression check.

```text
Done: Used the existing retry policy for the idempotent GET.
Proof: Retry-limit test passes; existing suite passes.
Skipped: New dependency and wrapper hierarchy; revisit when a second caller needs shared policy.
Risk: POST calls remain non-retrying by design.
```

### Why

Ponytail’s ladder rejects unnecessary owned surface. Caveman removes unrequested explanation. Cave Pony keeps the proof needed to trust the result.

## Parent contract retained

From Ponytail:

- understand the complete affected path before choosing a small diff;
- ask whether the change needs to exist;
- reuse the codebase, standard library, native platform, and installed dependencies before adding code;
- prefer deletion, boring code, few files, and one root-cause fix;
- leave one runnable check for non-trivial logic;
- build the broader safe version when the user insists, without repeated argument.

From Caveman:

- remove filler, hedging, pleasantries, self-reference, and routine narration;
- use fragments and drop articles only where meaning stays obvious;
- preserve code, commands, identifiers, errors, and the user’s language;
- avoid invented abbreviations, prose arrows, decorative tables, emoji, and raw-log dumps;
- suspend compression for destructive, security-sensitive, or order-dependent work;
- write code, commits, PRs, and documentation in normal grammar unless asked otherwise.

Cave Pony’s main coordination additions are independent `build` and `voice` controls, explicit activation, a shared clarity override, and a compact proof report.

## Behaviour

1. Understand the affected flow and trust boundaries.
2. Climb the least-owned-surface ladder and stop at the first correct rung.
3. Fix the narrowest shared root cause.
4. Run the smallest decisive proof, expanded by material risk.
5. Put the result first and report only useful Done, Proof, Skipped, and Risk lines.

YAGNI decides whether work is presently needed. KISS selects the simplest correct design. DRY centralises stable repeated knowledge, not merely similar syntax. Correctness and trust boundaries come first.

## More examples

### No change beats a new feature

Request: “Add a formatter option so dates display in the user’s locale.”

**Bad:** add a formatting service and configuration object before checking the runtime.

**Better:** use the existing locale-aware platform formatter when it already meets the requirement.

### Similar code is not automatically shared knowledge

Request: “These two functions look alike. Build a generic processing framework.”

**Bad:** introduce callbacks, generic types, and extension points solely because the syntax is similar.

**Better:** keep two clear local implementations until the repeated rule, lifecycle, and callers are semantically aligned.

### Stop a debugging spiral

Situation: two attempted fixes produce the same failure.

**Bad:** add a third guard around the same symptom.

**Better:** name the assumption now in doubt and run one decisive diagnostic before editing again.

```text
Failure: request still returns 401.
Cause in doubt: the test token may not reach the handler.
Next diagnostic: inspect the parsed authorization header at the handler boundary.
```

### Compression stops at destructive work

Request: “Reset my branch to match the remote.”

**Bad:** output only the destructive reset command.

**Better:** state that uncommitted work will be lost, offer a preservation step, then provide the command and recovery path.

## Real-world field evidence

Cave Pony was used on [Gov Metrics](https://github.com/wilfgrainger/gov-metrics) publication diagnostics. It rejected a new service, endpoint, store, and UI; reused the existing snapshot and canary; reduced the first classifier implementation; and required exact-head repository proof.

Read the [field record](field-tests/2026-07-19-gov-metrics-publication-diagnostics.md). It is one practical example, not a guarantee that every host model will follow the skill.

## Install

Current development version: `0.1.0`.

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

This tracks `main` until an immutable tag and GitHub Release exist.

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

| Axis | `lite` | `full` (default) | `ultra` |
|---|---|---|---|
| `build` | Build requested scope; name a smaller option | Enforce the ladder | Challenge speculative scope; prefer deletion or no change |
| `voice` | Tight full sentences | Short direct sentences or fragments | Minimum unambiguous words |

## Activation and coexistence

Cave Pony activates after explicit invocation or a clear minimalism, brevity, bloat, or audit request within coding or agent work. Generic brevity requests outside that context do not activate it.

It replaces rather than stacks with Ponytail and Caveman. `stop cave-pony` disables only Cave Pony; each parent retains its own stop command. Cave Pony does not claim a global `normal mode` command.

## Safety under compression

Commands that delete, overwrite, reset, force-push, drop, revoke, or rotate state trigger explicit prose. Preconditions, ordering, consequences, preservation, and recovery stay visible. The probes in [`tests/behavioral_cases.json`](tests/behavioral_cases.json) protect the written contract.

## Development and testing

No runtime package or third-party development dependency is required.

```bash
make validate
make test
```

CI runs Python 3.10 and 3.12. Static checks protect the committed contract; they cannot guarantee the behaviour of every host model.

## Repository layout

```text
skills/cave-pony/SKILL.md    Agent-facing behaviour
tools/validate.py            Small static contract validator
tests/                       Validator regressions and safety cases
field-tests/                 One real-repository field record
docs/DESIGN.md               Design decisions
```

## Presentation influence

The concrete Bad, Better, and Why teaching pattern was influenced by [`i-have-adhd`](https://github.com/ayghri/i-have-adhd). Cave Pony does not adopt that skill’s universal activation, compulsory time estimates, or compulsory state repetition.

## Licence

Cave Pony is released under the [MIT License](LICENSE). Attribution for Ponytail and Caveman is preserved in [Third-party notices](THIRD_PARTY_NOTICES.md).
