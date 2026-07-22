# Contributing

Cave Pony welcomes small, evidence-backed improvements.

This standalone repository is the canonical home of the skill. Keep it focused on Cave Pony; do not add unrelated personas, team integrations, or provider copies without a demonstrated working consumer.

## Before opening a change

Show the concrete agent failure. Check whether the footprint ladder, proof model, audit mode, or clarity override already covers it. Prefer one correction in `skills/cave-pony/SKILL.md` over duplicated instructions.

```text
Observed: <concrete failure or unnecessary surface>
Expected: <smallest trustworthy behaviour>
Evidence: <prompt, diff, output, test, or reproduction>
Proposed: <smallest correction>
```

Sensitive reports follow [`SECURITY.md`](SECURITY.md).

## Development

```bash
make validate
make test
```

Python 3.10 or newer is sufficient. CI uses Python 3.12. No third-party Python package is required.

## Acceptance criteria

A contribution must:

- preserve independent build and voice controls;
- preserve correctness, trust boundaries, accessibility, compatibility, recovery, and explicit requirements;
- fix a demonstrated gap with the smallest complete change;
- update validation or static cases for durable contract changes;
- distinguish checks that ran from checks that did not run;
- retain attribution and provenance;
- avoid copied branding or generated repository clutter;
- avoid new dependencies, packaging, or host mirrors without a present need.

New cases may extend `tests/behavioral_cases.json` when they have a unique ID, concrete prompt, trigger, at least one exact contract term, and at least two written requirements.

## Comparative evidence

Do not add numerical claims from anecdotes, cherry-picked prompts, or mismatched environments. Comparisons must follow [`docs/BENCHMARK_PLAN.md`](docs/BENCHMARK_PLAN.md) or a stronger preregistered protocol and publish failures, losing cases, scoring rules, safety gates, limitations, and reproduction material.

A result showing no advantage is useful evidence.

## Documentation and branding

Finished documentation uses normal grammar. Keep the README focused on observable user value. Claims must be traceable to committed evidence.

The Cave Pony logo is original project artwork. Do not imitate the logos, mascots, typography, or distinctive presentation of Ponytail or Caveman.

## Changes

Explain the observed failure, smallest correction, and checks run. Large rewrites need stronger evidence than focused edits. New dependencies require a present need and a rejected standard-library or existing-project alternative.
