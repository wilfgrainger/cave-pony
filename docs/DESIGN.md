# Design and implementation

## Problem

Coding agents can inflate two independent surfaces: implementation and narration. A terse agent can still build a framework; a minimal-code agent can still bury the result in prose. Cave Pony coordinates both without allowing either to weaken correctness.

## Activation model

Cave Pony activates only after a trigger in the current conversation: invocation, an explicit request for minimal or least-over-engineered code, terse output, a complaint about bloat, or an audit request. A preloaded skill or uncertainty about prior state does not activate it.

Once active, the selected levels apply on every response until `stop cave-pony`. There is no global `normal mode` alias because that collides with both parent skills.

## Behavioural model

Two independent values govern behaviour:

```text
build ∈ {lite, full, ultra}
voice ∈ {lite, full, ultra}
```

A one-word level sets both. Axis assignments override one value. Default state is `build=full voice=full`. Audit is a one-shot operation.

## Coordination invariants

1. Understand the affected flow before selecting a small implementation.
2. Preserve correctness, security, privacy, accessibility, data integrity, and explicit requirements.
3. Expand implementation and explanation with material risk.
4. Never claim unexecuted proof.
5. Never alter exact technical strings for terseness.
6. Ties between brevity and clarity break toward clarity.

## Footprint gate and complexity toll

The gate is ordered from least to most owned surface. The agent stops at the first option that fully meets the current requirement after understanding the flow.

Every durable addition needs a present requirement, a named simpler alternative that fails it, and a benefit larger than its maintenance and failure cost. Standing instructions count because they consume context and can conflict or drift.

## Semantic and claim discipline

Minimal code is not useful when it preserves the wrong meaning. A field must describe the event or authority named by its label; observation, publication, retrieval, validation, build, and display times are therefore distinct. Deterministic output makes unchanged evidence reproducible, while semantic tests allow equivalent wording and implementation.

Presence is also separate from eligibility. A fallback may be valid for continuity but invalid for a claim such as “latest verified.” The same predicate that makes a claim true must gate its publication, with at least one accepted state and one plausible rejected state tested.

## Proof model

“Smallest decisive proof” means the cheapest check capable of falsifying the claimed behaviour at the relevant risk level. It is a starting point, not a one-test cap.

The repository's own tests are **static contract tests**. They can prove that required wording, sections, triggers, and adversarial cases are committed. They cannot prove that a host model follows those rules. Agent behaviour requires comparative model runs.

## Output model

For completed changes, the canonical four-field artifact is the **footprint report**: Done, Proof, Skipped, Risk. Empty fields disappear. `Skipped` names the omitted surface and the condition that would justify revisiting it. Pure questions do not receive a footprint report.

Audit defaults to the most recent change or diff unless a target is specified. Each ranked finding states the defect, evidence, consequence, and smallest correction.

## Clarity override

Compression is suspended for destructive or ordering-sensitive state changes. Trigger verbs include delete, overwrite, reset, force-push, drop, revoke, and rotate. The override includes preconditions and recovery, not only the command itself.

An ultra response containing only `git reset --hard origin/main` is unsafe. A compliant response first states the loss risk, offers a preservation step, then gives the command and recovery path.

## Benchmark status

The coordination layer is not yet proven better than loading Ponytail and Caveman together. [`benchmarks/README.md`](../benchmarks/README.md) preregisters a falsifiable four-arm experiment and kill criterion. No comparative result may be claimed until a committed result file exists.

The benchmark is a present requirement because comparative performance is the project's central empirical question. Provider-specific runtime integration remains outside the core skill; the preregistration reuses Ponytail's published agentic harness rather than duplicating it here.

## Validation

`tools/validate.py` checks:

- explicit activation and anti-hijack persistence;
- execution-loop consistency between the skill and README;
- safety override and output-template wording;
- canonical footprint-report terminology;
- coexistence and version documentation;
- benchmark honesty and preregistration;
- source links, quotations, and copyright notices;
- required behavioural probes plus schema-valid extensions;
- clean text formatting.

The `prompt` field in each behavioural case is reserved for the comparative harness. Static validation checks its schema; model execution will consume it when the benchmark runs.

`tests/test_repository.py` runs validation and negative regression cases against temporary copies of the skill, README, and behavioural cases. CI runs the suite on Python 3.10 and 3.12.

## Packaging and release decision

The original archive builder was removed. No confirmed consumer used `dist/cave-pony.skill`, so packaging did not pay the complexity toll. The absence of `tools/build.py` is documented here rather than enforced through a permanent filename ban.

The skill declares a semantic version in frontmatter. Installation remains explicitly unpinned until an immutable Git tag and GitHub Release are actually created; documentation must not imply otherwise.

## Extension rules

A proposal should show a concrete failure, explain why existing rules miss it, make the smallest wording change, and add a regression test. New behavioural cases are allowed when their schema is valid; the three destructive-operation probes remain required. Do not add provider-specific mirrors, packaging artifacts, or generated copies until a real integration requires them. Keep `SKILL.md` the single behavioural source of truth.
