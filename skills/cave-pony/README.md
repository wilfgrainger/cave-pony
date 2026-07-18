# Cave Pony skill

Cave Pony coordinates minimal implementation with minimal narration. It activates only when explicitly invoked or when the user clearly requests minimalism, terse output, or an audit.

## Install

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

Or copy this directory into an Agent Skills-compatible skills folder.

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

The agent must understand the affected path, minimise owned surface, fix shared causes, run risk-proportionate proof, and switch to explicit prose whenever compression could hide destructive consequences, prerequisites, ordering, or recovery.

For changes it uses the four-field footprint report. For pure questions it answers directly in the minimum unambiguous words. Audit defaults to the most recent change or diff unless another target is specified.

See the repository [README](../../README.md), [design notes](../../docs/DESIGN.md), [benchmark preregistration](../../benchmarks/README.md), and [third-party notices](../../THIRD_PARTY_NOTICES.md).
