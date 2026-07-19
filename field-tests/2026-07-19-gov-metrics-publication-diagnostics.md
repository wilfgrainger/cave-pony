# Gov Metrics proof — publication diagnostics

Date: 2026-07-19
Target: `wilfgrainger/gov-metrics` issue #253 and PR #261
Mode: Cave Pony `build=full voice=full`
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

## Production status at the test date

Production deployment was pending. Gov Metrics permits deployment only through its manual `workflow_dispatch` workflow. The available GitHub capability could inspect and rerun Actions but could not start that workflow, so the safeguard was not weakened and no temporary push-triggered deployment path was added.

This field test therefore proves implementation, repository integration and exact-head assurance. It does not claim that `public-data.org` served `meta.publicationDiagnostics` on the test date.

## What this proves

This field record shows Cave Pony used on one real repository to:

- select a real defect rather than invent a feature;
- discover and reuse existing architecture;
- reject a first implementation as too large;
- reduce owned runtime surface before merge;
- preserve safety and evidence requirements while compressing;
- require exact-head policy, test, build and browser proof;
- report a deployment blocker instead of bypassing a guardrail or claiming success.

It is one practical example. It does not guarantee that every host model or task will follow the skill correctly.
