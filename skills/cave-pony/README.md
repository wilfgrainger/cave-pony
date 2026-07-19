# Cave Pony skill

Cave Pony `0.1.0` coordinates minimal implementation with minimal narration. It activates after explicit invocation or, within coding or agent work, a clear request for minimalism, terse output, or an audit. Generic brevity requests outside that context do not activate it.

## Install

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

This tracks `main` until the first immutable tag and GitHub Release exist. Or copy this directory into an Agent Skills-compatible skills folder.

## Commands

```text
/cave-pony                         # build=full voice=full
/cave-pony lite                    # both axes lite
/cave-pony ultra                   # both axes ultra
/cave-pony build=ultra voice=lite  # independent controls
/cave-pony audit                   # read-only review
stop cave-pony                     # disable Cave Pony only
```

Do not install it alongside Ponytail and Caveman unless you intentionally accept overlapping instructions and context overhead.

## Contract

The agent must understand the affected path, minimise owned surface, protect meaning, gate claims, fix shared causes, run risk-proportionate proof, and switch to explicit prose whenever compression could hide destructive consequences, prerequisites, ordering, or recovery.

YAGNI and KISS apply at the footprint gate: build only for the present requirement and choose the simplest correct design in the existing architecture. DRY applies to stable repeated knowledge, not similar syntax. Correctness comes first; YAGNI and KISS come before DRY so a speculative abstraction is not mistaken for simplification.

A non-obvious deliberate shortcut receives one local `cave-pony:` comment naming its ceiling and concrete upgrade trigger. Repeated failures stop the patch loop and trigger one decisive diagnostic. Failure reports state the exact failure, known cause, smallest correction, and proof or next diagnostic.

For changes it uses the four-field footprint report. `Skipped` includes the condition for revisiting the omitted surface. When the user still has work to do, the response ends with one concrete next action; completed work does not manufacture homework. For pure questions it answers directly. Audit defaults to the most recent change or diff and reports finding, evidence, consequence, and smallest correction.

See the repository [README](../../README.md), [design notes](../../docs/DESIGN.md), [field tests](../../field-tests/), [future comparative-research issue](https://github.com/wilfgrainger/cave-pony/issues/11), and [third-party notices](../../THIRD_PARTY_NOTICES.md).
