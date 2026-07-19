# Design and implementation

## Problem

Coding agents can inflate two independent surfaces: implementation and narration. A terse agent can still build a framework; a minimal-code agent can still bury the result in prose. Cave Pony coordinates both without allowing either to weaken correctness.

## Activation model

Cave Pony activates after explicit invocation or, within coding or agent work, a request for minimal or least-over-engineered implementation, terse output, relief from bloat, or an audit. A generic request to be brief outside that context does not activate it. A preloaded skill or uncertainty about prior state does not activate it.

Once active, the selected levels apply on every response until `stop cave-pony`. There is no global `normal mode` alias because that collides with both parent skills.

## Intentional parent divergences

Cave Pony preserves the parents' implementation and communication goals but deliberately changes two rules:

1. **Uncertainty does not activate the skill.** Both parent skills resolve activation ambiguity by staying active. Cave Pony instead requires a trigger in the current conversation. This prevents a preloaded skill or missing conversation history from silently taking control.
2. **The clarity override is broader.** Caveman's automatic clarity rule is extended to privacy, destructive operations, migrations, recovery, legal or financial risk, ordered procedures, and repeated questions that signal the earlier compression failed.

These are intentional coordination choices, not accidental drift from the parent skills.

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

A deliberate simplification with a non-obvious known ceiling receives one local `cave-pony:` comment naming both the ceiling and the concrete upgrade trigger. This preserves the decision after the chat footprint report disappears. Obvious choices and hypothetical futures do not receive ceiling comments.

## YAGNI, KISS and DRY

The principles refine the footprint gate; they are not three extra workflow phases.

1. **YAGNI** rejects speculative requirements, options, extension points, compatibility layers and generality.
2. **KISS** selects the simplest correct design that fits the existing architecture and remains easy to explain.
3. **DRY** gives stable repeated knowledge one authoritative home after repetition is real and semantically aligned.

The precedence is deliberate: correctness and trust boundaries first, then YAGNI and KISS, then DRY. Similar syntax does not prove shared knowledge. Two clear local cases are preferable to a generic abstraction whose meaning, lifecycle or callers are not yet stable. Conversely, a repeated business rule, schema, permission decision or publication predicate should not drift across independent implementations once its shared meaning is established.

## Semantic and claim discipline

Minimal code is not useful when it preserves the wrong meaning. A field must describe the event or authority named by its label; observation, publication, retrieval, validation, build, and display times are therefore distinct. Deterministic output makes unchanged evidence reproducible, while semantic tests allow equivalent wording and implementation.

Presence is also separate from eligibility. A fallback may be valid for continuity but invalid for a claim such as “latest verified.” The same predicate that makes a claim true must gate its publication, with at least one accepted state and one plausible rejected state tested.

## Proof model

“Smallest decisive proof” means the cheapest check capable of falsifying the claimed behaviour at the relevant risk level. It is a starting point, not a one-test cap.

The repository's own tests are **static contract tests**. They can prove that required sections, triggers, invariants and adversarial cases are committed. They cannot prove that every host model follows those rules or that Cave Pony outperforms another skill. Comparative model research is deferred to [issue #11](https://github.com/wilfgrainger/cave-pony/issues/11).

## Output model

For completed changes, the canonical four-field artifact is the **footprint report**: Done, Proof, Skipped, Risk. Empty fields disappear. `Skipped` names the omitted surface and the condition that would justify revisiting it. Pure questions do not receive a footprint report.

Audit defaults to the most recent change or diff unless a target is specified. Each ranked finding states the defect, evidence, consequence, and smallest correction.

Voice compression removes greetings, filler, hedging, self-reference, repeated framing and decorative transitions before shortening technical language. Prose abbreviations and arrows are rejected because compact-looking notation can reduce clarity without reducing model tokens. Tables must improve comparison; emoji and raw log dumps are not default output.

Failures are reported as the exact failure, known cause, smallest correction, and proof or next diagnostic. If the same failure survives two attempted corrections, Cave Pony stops adding patches and challenges the assumption most likely to be wrong.

A next action appears only when the user still has work to do. Time estimates require grounded scope and are omitted rather than invented. Multi-step state is restated when needed to resume work, not as a compulsory recap on every turn.

The public README uses compact Bad, Better and Why examples so readers can learn the behaviour quickly. Those teaching examples stay outside `SKILL.md` unless they prevent a concrete model failure, because every active example consumes context.

## Clarity override

Compression is suspended for destructive or ordering-sensitive state changes. Trigger verbs include delete, overwrite, reset, force-push, drop, revoke, and rotate. The override includes preconditions and recovery, not only the command itself.

An ultra response containing only `git reset --hard origin/main` is unsafe. A compliant response first states the loss risk, offers a preservation step, then gives the command and recovery path.

A materially repeated question is treated as evidence that the previous compression failed. The next answer uses normal explicit prose rather than compressing harder.

## Evidence boundary

The release claim is structural: Cave Pony coordinates implementation minimalism, communication compression and risk-proportionate proof in one skill. Static tests protect that written contract, while `field-tests/` records practical repository use.

No comparative superiority or measured token-efficiency claim is made. The larger Codex experiment was removed from the release surface and preserved as future work in issue #11.

## Validation

`tools/validate.py` is the authoritative static contract checker. It verifies:

- explicit coding-context activation and anti-hijack persistence;
- execution-loop consistency between the skill and README;
- YAGNI, KISS and stable-knowledge DRY precedence;
- instruction-budget, semantic, claim-gate and root-fidelity invariants;
- safety override, failure shape and footprint-report wording;
- coexistence, version, attribution and field-evidence documentation;
- immutable CI action references, main-branch scoping and run cancellation;
- required behavioural probes plus schema-valid extensions;
- clean text formatting.

`tests/test_repository.py` exercises that validator through its Python API and command-line entry point, then mutates temporary repository copies to prove important regressions are rejected. Keeping the static contract in one validator avoids five small test files independently freezing the same prose.

The `prompt` field in each behavioural case records the scenario that exercises the written contract. Static validation checks its schema without requiring a model runner.

## Packaging and release decision

The original archive builder was removed. No confirmed consumer used `dist/cave-pony.skill`, so packaging did not pay the complexity toll. The absence of `tools/build.py` is documented here rather than enforced through a permanent filename ban.

The skill declares a semantic version in frontmatter. Installation remains explicitly unpinned until an immutable Git tag and GitHub Release are actually created; documentation must not imply otherwise.

## Extension rules

A proposal should show a concrete failure, explain why existing rules miss it, make the smallest wording change, and add or update a regression check. New behavioural cases are allowed when their schema is valid; the three destructive-operation probes remain required. Do not add provider-specific mirrors, packaging artifacts, or generated copies until a real integration requires them. Keep `SKILL.md` the single behavioural source of truth.
