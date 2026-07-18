# Contributing

Cave Pony welcomes small, evidence-backed improvements.

## Before opening a change

Show the concrete agent failure. Check whether the footprint gate, complexity toll, proof model, audit mode, or clarity override already covers it. Prefer editing `skills/cave-pony/SKILL.md` over adding copies.

## Development

```bash
make validate
make test
```

Python 3.10 or newer is sufficient. No third-party development dependencies are required.

## Acceptance criteria

A contribution should preserve the independent build and voice budgets; preserve correctness and safety boundaries; make the smallest change that fixes the demonstrated gap; update validation or tests for durable contracts; keep attribution intact; and avoid generated artifacts.

Do not add packaging machinery or provider-specific mirrors until a named, working consumer requires them. Document the consumer and rejected simpler distribution method in the same change.

## Pull requests

Explain the observed failure, minimal correction, and checks run. Large rewrites need stronger evidence than focused edits. New dependencies require a present need and rejected standard-library alternative.
