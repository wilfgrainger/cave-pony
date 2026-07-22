# Contributing

Cave Pony welcomes small, evidence-backed improvements.

This standalone repository is the canonical home of the skill. Do not edit a mirror first and assume it will be synchronised automatically.

## Before opening a change

Show the concrete agent failure. Check whether the footprint ladder, proof model, audit mode, or clarity override already covers it. Prefer one correction in `skills/cave-pony/SKILL.md` over provider-specific copies.

A useful report includes:

```text
Observed: <concrete failure or unnecessary surface>
Expected: <smallest trustworthy behaviour>
Evidence: <prompt, diff, output, test, or reproduction>
Proposed: <smallest correction>
```

## Development

```bash
make validate
make test
```

Python 3.10 or newer is sufficient. CI runs Python 3.10 and 3.12. No third-party development dependencies are required.

## Acceptance criteria

A contribution must:

- preserve independent build and voice controls;
- preserve correctness, trust boundaries, accessibility, compatibility, recovery, and explicit requirements;
- fix a demonstrated gap with the smallest complete change;
- update validation or behavioural probes for durable contract changes;
- distinguish checks that ran from checks that were not run;
- retain attribution and provenance;
- avoid copied branding or generated repository clutter;
- avoid new dependencies, packaging, or provider mirrors without a named working consumer.

New behavioural cases may extend `tests/behavioral_cases.json` when they have a unique id, a concrete scenario, a trigger, and at least two contract requirements. Required destructive-operation probes must remain.

## Comparative evidence

Do not add numerical claims from anecdotal sessions, cherry-picked prompts, or mismatched models and repositories.

Comparisons with baseline, Ponytail, Caveman, or stacked parents must follow [`docs/BENCHMARK_PLAN.md`](docs/BENCHMARK_PLAN.md) or document a stronger replacement protocol. Publish:

- task definitions before results;
- identical model and environment settings;
- all runs, including failures and losing cases;
- scoring rules and safety gates;
- limitations and reproduction instructions;
- raw artefacts when licensing and privacy allow.

A result that shows no advantage is still useful evidence.

## Documentation and branding

Finished documentation uses normal grammar. Keep the README focused on observable user value. Claims must be supportable by committed evidence.

The Cave Pony logo is original project artwork. Do not introduce assets that imitate the logos, mascots, typography, or distinctive presentation of Ponytail or Caveman.

## Changes

Explain the observed failure, smallest correction, and checks run. Large rewrites need stronger evidence than focused edits. New dependencies require a present need and a rejected standard-library or existing-project alternative.
