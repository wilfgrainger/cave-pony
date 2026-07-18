# Contributing

Cave Pony welcomes small, evidence-backed improvements.

## Before opening a change

Show the concrete agent failure the change addresses. Check whether the existing footprint gate, complexity toll, proof model, audit mode, or clarity override already covers it. Prefer editing the single behavioural source, `skills/cave-pony/SKILL.md`, over adding provider-specific copies.

## Development

```bash
make test
make build
```

The project intentionally uses no third-party development dependencies. Python 3.10 or newer is sufficient.

## Acceptance criteria

A contribution should:

- preserve the two independent build and voice budgets;
- preserve correctness, security, privacy, accessibility, and data-integrity boundaries;
- add the smallest wording or tooling change that fixes the demonstrated gap;
- update validation or tests when it changes a durable contract;
- keep source attribution intact;
- avoid generated archives in commits.

## Pull requests

Explain the observed failure, the minimal correction, and the checks run. Large rewrites need stronger evidence than focused edits. New dependencies require a clear present need and a rejected standard-library alternative.
