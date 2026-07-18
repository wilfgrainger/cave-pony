# Cave Pony skill

Cave Pony coordinates minimal implementation with minimal narration.

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
stop cave-pony                     # disable persistent mode
```

## Contract

The agent must:

1. understand the complete affected path before shrinking the solution;
2. prefer no change, deletion, reuse, standard library, native features, and installed dependencies;
3. demand a present need for every new owned surface;
4. fix shared root causes rather than repeated symptoms;
5. run and accurately report the smallest risk-proportionate proof;
6. use explicit prose whenever compression could make risky work ambiguous.

See the repository [README](../../README.md), [design notes](../../docs/DESIGN.md), and [third-party notices](../../THIRD_PARTY_NOTICES.md).
