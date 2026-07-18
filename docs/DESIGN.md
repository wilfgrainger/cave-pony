# Design and implementation

## Problem

Coding agents can inflate two independent surfaces: implementation and narration. A terse agent can still build a framework; a minimal-code agent can still bury the result in prose. Cave Pony coordinates both without allowing either to weaken correctness.

## Activation model

Cave Pony is explicitly activated. The frontmatter and body use the same trigger contract: invocation, an explicit request for minimal or least-over-engineered code, terse output, a complaint about bloat, or an audit request. It must not auto-load for ordinary coding tasks.

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

Every durable addition needs a present requirement, a named simpler alternative that fails it, and a benefit larger than its maintenance and failure cost. This applies to repository tooling too.

## Proof model

“Smallest decisive proof” means the cheapest check capable of falsifying the claimed behaviour at the relevant risk level. It is a starting point, not a one-test cap.

The repository's own tests are **static contract tests**. They can prove that required wording, sections, triggers, and adversarial cases are committed. They cannot prove that a host model follows those rules. Agent behaviour requires comparative model runs.

## Output model

For completed changes, the canonical four-field artifact is the **footprint report**: Done, Proof, Skipped, Risk. Empty fields disappear. Pure questions do not receive a footprint report.

Audit defaults to the most recent change or diff unless a target is specified.

## Clarity override

Compression is suspended for destructive or ordering-sensitive state changes. Trigger verbs include delete, overwrite, reset, force-push, drop, revoke, and rotate. The override includes preconditions and recovery, not only the command itself.

## Benchmark status

The coordination layer is not yet proven better than loading Ponytail and Caveman together. [`benchmarks/README.md`](../benchmarks/README.md) preregisters a falsifiable four-arm experiment and kill criterion. No comparative result may be claimed until a committed result file exists.

The benchmark is a present requirement because comparative performance is the project's central empirical question. Provider-specific runtime integration remains outside the core skill; the preregistration reuses Ponytail's published agentic harness rather than duplicating it here.

## Validation

`tools/validate.py` checks:

- explicit and consistent activation language;
- anti-drift persistence;
- safety override wording;
- canonical footprint-report terminology;
- coexistence documentation;
- benchmark honesty and preregistration;
- source links, exact quotations, and copyright notices;
- adversarial contract-case schema;
- clean text formatting.

`tests/test_repository.py` runs validation and negative regression cases against temporary copies of the skill and README.

## Packaging decision

The original archive builder was removed. No confirmed consumer or release process used `dist/cave-pony.skill`, so packaging did not pay the project's own complexity toll. Add packaging only when a named consumer requires it, and document that consumer before adding machinery.

## Extension rules

A proposal should show a concrete failure, explain why existing rules miss it, make the smallest wording change, and add a regression test. Do not add provider-specific mirrors, packaging artifacts, or generated copies until a real integration requires them. Keep `SKILL.md` the single behavioural source of truth.
