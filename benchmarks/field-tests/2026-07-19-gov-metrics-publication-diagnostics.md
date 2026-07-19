# Gov Metrics proof — publication diagnostics

Date: 2026-07-19
Target: `wilfgrainger/gov-metrics` issue #253 and PR #261
Mode: Cave Pony `build=full voice=full`
Cave Pony commit: `a4b280ffbee3c6ec943c040427380454ea226e21`
Gov Metrics tested head: `2a211c92972e02a3dccda1de076a3c72d0f1e0d5`
Gov Metrics merge: `fedf9cc723d4aa0873f4db81f170ece921c9a8f2`

## Present requirement

Issue #253 required machine-readable, non-secret section diagnostics that distinguish upstream fetch failure, parser or contract rejection, stale observation, missing history and snapshot delivery failure. The production canary had to report exact failing sections and reasons without changing metric values.

## Existing surface reused

Gov Metrics already had:

- a same-origin `/data/metrics-snapshot.json` publication contract;
- source `status`, `cacheState`, `fetchedAt` and bounded error metadata;
- bounded reuse of a still-current, history-complete prior section;
- a production snapshot canary;
- repository policy, unit, Worker, static-export and browser gates.

The change reused those surfaces. It did not add an endpoint, UI component, service, dependency, store, framework or metric-value transformation.

## Smallest correction

PR #261 added:

- one five-code public diagnostic contract;
- one deterministic generator that writes `meta.publicationDiagnostics` into the final snapshot after all section merges;
- one deployment step invoking the generator;
- one canary extension requiring every unavailable section to have a valid public reason;
- deterministic fixtures and focused tests.

Public codes:

- `upstream_fetch_failure`;
- `parser_contract_rejection`;
- `stale_observation`;
- `missing_history`;
- `snapshot_delivery_failure`.

Raw upstream or connector error strings are inputs to classification but are not copied into the public diagnostic object.

## Footprint pressure

The first implementation contained 178 lines in the classifier and the PR showed 552 additions. Cave Pony rejected that as too large to call evidence of minimalism without another pass.

The second pass reduced the classifier to 116 lines: 62 lines removed, or about 35%, without dropping a required code or proof case. The final PR changed eight files with 490 additions and eight deletions. Most additions are deterministic fixtures and tests; production integration is one contract, one generator, one canary extension, one package command and one four-line workflow step.

This is a focused correctness change, not a tiny change. Cave Pony minimised owned runtime surface rather than chasing the lowest raw line count at the expense of five required categories and decisive proof.

## Proof executed

Exact-head GitHub Actions run:

`https://github.com/wilfgrainger/gov-metrics/actions/runs/29681870798`

Passed on `2a211c92972e02a3dccda1de076a3c72d0f1e0d5`:

- text and lockfile policy;
- static architecture;
- source-repair and source-ownership contracts;
- focused-change complexity policy;
- PR-description evidence policy;
- lint;
- full unit and Worker suite;
- deterministic static export;
- deterministic Playwright smoke tests;
- aggregate quality gate.

Focused tests prove:

- all five required categories;
- byte-identical output when the snapshot is unchanged;
- raw internal errors are absent from the public diagnostics;
- unknown diagnostic codes are rejected;
- the canary rejects an unavailable section with no reason;
- the existing bounded seed-reuse policy remains unchanged.

PR #261 was squash-merged only after the exact tested head passed.

## Operational correction

While setting up the branch, a connector mistake created a one-word placeholder file on `main`. It was immediately deleted in the next commit before the feature branch was created. No product code, data contract or metric value changed. The mistake is recorded because proof includes recovery behaviour, not only successful steps.

## Production status

Production deployment is pending. Gov Metrics deliberately permits deployment only through the manual `workflow_dispatch` workflow. The connected GitHub capability in this session can inspect and rerun Actions but cannot start a new manual workflow. The deployment safeguard was not weakened and no temporary push-triggered deployment path was added.

Therefore this field test proves implementation, repository integration and exact-head assurance. It does not yet claim that `public-data.org` serves `meta.publicationDiagnostics` until the manual deployment workflow runs and the production canary observes it.

## What this proves

This field test is evidence that Cave Pony can:

- select a real P0 defect rather than inventing a feature;
- discover and reuse existing architecture;
- reject a first implementation as too large;
- reduce owned runtime surface before merge;
- preserve safety and evidence requirements while compressing;
- require exact-head policy, test, build and browser proof;
- report a deployment blocker instead of bypassing a guardrail or claiming success.

## What this does not prove

This is one real-repository field test, not the preregistered comparative benchmark. It does not measure input tokens, output tokens, cost or performance against baseline, Ponytail plus Caveman, and the YAGNI control. The 480-cell comparative protocol remains not run, and no superiority claim follows from this result.
