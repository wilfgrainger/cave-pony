# Design and implementation

## Problem

Coding agents can waste effort in two independent ways:

1. **Implementation inflation:** unnecessary code, dependencies, abstractions, services, configuration, and tests.
2. **Narration inflation:** greetings, plans, tool diaries, repeated summaries, and explanations the user did not request.

Reducing only one surface is incomplete. A terse agent can still build a framework. A minimal-code agent can still bury the result in prose. Cave Pony makes both surfaces explicit and coordinates them without allowing either to weaken correctness.

## Behavioural model

Cave Pony is a Markdown Agent Skill. It has no runtime process and changes no repository by itself. The host agent loads `skills/cave-pony/SKILL.md` and applies its rules to coding work.

Two independent state values govern behaviour:

```text
build ∈ {lite, full, ultra}
voice ∈ {lite, full, ultra}
```

A one-word level sets both. Axis assignments override one value without changing the other. Default state is `build=full voice=full`. Audit is a one-shot operation rather than a persistent fourth intensity.

## Coordination invariants

The following rules outrank both budgets:

1. Understand the affected flow before selecting a small implementation.
2. Preserve correctness, security, privacy, accessibility, data integrity, and explicit requirements.
3. Expand both implementation and explanation in proportion to material risk.
4. Never claim unexecuted proof.
5. Never shorten exact technical strings into altered forms.

These invariants prevent common failure modes: a tiny symptom patch, missing validation, unclear destructive instructions, and false test claims.

## Footprint gate

The gate is ordered from least to most owned surface. It is not a scoring algorithm and needs no external tooling. The agent stops at the first option that fully meets the requirement after understanding the flow.

The order distinguishes repository reuse, standard-library support, native platform capability, installed dependencies, local code, and new ecosystem surface. That distinction matters because each step changes maintenance ownership and failure modes.

## Complexity toll

The toll applies to durable surface: dependencies, files, abstractions, configuration, state, services, workers, schedules, and public APIs. Each item needs:

- a concrete present requirement;
- a named simpler alternative that does not meet it;
- a benefit larger than its maintenance and failure cost.

This is deliberately qualitative. A numeric complexity score would create fake precision and more machinery than the skill needs.

## Proof model

“Smallest decisive proof” means the cheapest check that can falsify the claimed behaviour at the relevant risk level. Examples:

- existing focused unit test before the full suite;
- one regression test for a changed branch;
- schema validation for a data contract;
- dry-run and rollback verification for a migration;
- permission-boundary tests for authorisation work.

The model does not cap testing at one test. It starts with one decisive check and expands when risk or repository convention requires it.

## Output model

The default completion shape is a four-field footprint report: Done, Proof, Skipped, Risk. Empty fields disappear. This is compact but auditable: the reader can distinguish delivered work, evidence, deliberate non-work, and residual uncertainty.

Requested documentation, analysis, teaching, or reports are exempt from aggressive compression because they are the product being requested.

## Clarity override

Compression is suspended when omitted grammar could change order, causality, scope, responsibility, or consequences. The override is automatic for destructive, security, privacy, migration, legal, financial, and other high-risk content. It ends after the risky section is clear.

## Packaging

`tools/build.py` creates `dist/cave-pony.skill`, a deterministic ZIP archive containing:

```text
cave-pony/SKILL.md
cave-pony/README.md
cave-pony/THIRD_PARTY_NOTICES.md
```

Files use a fixed archive timestamp and stable ordering so identical source produces identical bytes. The build uses only Python's standard library.

## Validation

`tools/validate.py` checks:

- required repository files;
- frontmatter name, licence, description, and argument hint;
- mandatory behavioural sections;
- safety and proof language;
- source links and exact short quotations in the main README;
- third-party copyright notices;
- clean Markdown whitespace and final newlines.

`tests/test_repository.py` runs validation, builds the archive, checks its contents, and verifies reproducibility by hashing two builds.

## Extension rules

Contributions should add rules only for observed failure modes. A proposal should show:

1. a concrete agent failure;
2. why the existing gate, toll, proof, or clarity rules do not cover it;
3. the smallest wording change that fixes it;
4. a repository test that prevents regression.

Do not add provider-specific mirrors until a real integration requires them. Keep `SKILL.md` the single behavioural source of truth.
