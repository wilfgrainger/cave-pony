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

## Field testing

Independent real-repository records are especially useful before `v1.0.0`. Start from [`field-tests/TEMPLATE.md`](field-tests/TEMPLATE.md) and keep neutral, losing, failed, and ambiguous results visible.

A useful record pins the repository and Cave Pony commits, names the host and model, preserves the prompt, distinguishes checks that ran from checks that did not, and states what Cave Pony improved, failed to improve, or made worse. Do not infer a numerical superiority claim from an individual record or a small convenience sample.

Authenticated Codex behaviour testing follows [`docs/CODEX_BEHAVIOUR_PROTOCOL.md`](docs/CODEX_BEHAVIOUR_PROTOCOL.md). A prepared protocol is not proof; publish the observed result.

## Development

On Unix-like systems:

```bash
make validate
make test
```

On Windows without GNU Make, run the same target commands directly in PowerShell:

```powershell
python tools/validate.py
if (-not (Test-Path "tests/test_profile_artwork.py")) { throw "missing tests/test_profile_artwork.py" }
python -m unittest discover -s tests -v
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

## Comparative claims

Do not add numerical claims from anecdotes, cherry-picked prompts, or mismatched environments. Any future comparison must be preregistered before final runs and publish equivalent conditions, correctness and safety gates, all runs, scoring rules, limitations, losing cases, and reproduction material.

Benchmark machinery does not belong in the repository until a concrete claim, release channel, or customer decision requires it. A result showing no advantage is useful evidence.

## Documentation and branding

Finished documentation uses normal grammar. Keep the README focused on observable user value. Claims must be traceable to committed evidence.

The Cave Pony logo is original project artwork. Do not imitate the logos, mascots, typography, or distinctive presentation of Ponytail or Caveman.

## Changes

Explain the observed failure, smallest correction, and checks run. Large rewrites need stronger evidence than focused edits. New dependencies require a present need and a rejected standard-library or existing-project alternative.
