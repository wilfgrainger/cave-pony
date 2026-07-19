# Gov Metrics field test — YAGNI, KISS and DRY

Date: 2026-07-19
Target: `wilfgrainger/gov-metrics` issue #253 and merged PR #261
Mode: Cave Pony `build=full voice=full`

## Question

Should Cave Pony explicitly include YAGNI, KISS and DRY without becoming a larger instruction framework?

## Evidence from Gov Metrics

Issue #253 required five stable, machine-readable publication failure reasons, deterministic proof, exact canary reporting and no metric-value change.

### YAGNI

The implementation did not add a diagnostics service, public endpoint, database, persistent store, UI component, dependency, extension mechanism or generic event system. None was required to satisfy the current publication contract.

### KISS

Gov Metrics already had a final same-origin snapshot, source metadata, bounded last-verified reuse, a publication workflow and a snapshot canary. The correction added diagnostics to the existing snapshot metadata and taught the existing canary to verify them.

The first classifier was 178 lines. A second footprint pass reduced it to 116 lines before merge while retaining all five failure classes and proof cases.

### DRY

The five codes, summaries, classifier and validator live in one shared contract: `contracts/publication-diagnostics.js`.

Both `scripts/generate-publication-diagnostics.mjs` and `scripts/snapshot-canary.mjs` import that contract. The material publication rule therefore has one authoritative implementation rather than separate generator and canary interpretations.

This is stable repeated knowledge: public reason codes and their classification meaning. It is not merely similar-looking syntax.

## Counterexample rejected

A blanket “never duplicate code” rule would encourage generic error orchestration whenever two local branches look alike. That would conflict with Cave Pony's footprint gate and could hide distinct failure semantics.

Small local duplication remains acceptable until the repeated meaning, callers and lifecycle are stable.

## Skill correction

YAGNI, KISS and DRY are now named inside the existing footprint and root-cause loop rather than added as new workflow steps.

Precedence:

1. correctness and trust boundaries;
2. YAGNI and KISS;
3. DRY for stable repeated knowledge.

The skill explicitly states that repeated syntax alone is not a reason to abstract and that small local duplication is better than premature abstraction.

## Proof

Gov Metrics tested head: `2a211c92972e02a3dccda1de076a3c72d0f1e0d5`

Gov Metrics exact-head Actions run: `29681870798`

Gov Metrics merge: `fedf9cc723d4aa0873f4db81f170ece921c9a8f2`

The run passed repository policy, focused-complexity enforcement, lint, the full unit and Worker suite, static production export, deterministic Playwright smoke tests and the aggregate quality gate.

## Boundary

This field test supports the design and precedence of the three principles. It does not prove comparative token or source-line superiority; the preregistered four-arm benchmark remains not run.
