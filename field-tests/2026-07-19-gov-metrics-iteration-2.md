# Gov Metrics field test — iteration 2

Date: 2026-07-19
Target: `wilfgrainger/gov-metrics` PR #255
Mode: Cave Pony `build=full voice=full`

## Scope

Review the active evidence-page discoverability change for the smallest correctness and determinism defects. Keep the existing feature scope intact.

## Finding

The branch exposed upstream retrieval time (`source.fetchedAt`) as Dataset and RSS `dateModified`. It also generated RSS `<lastBuildDate>` from the wall clock. Retrieval time is not the public-data.org publication edition, and unchanged evidence therefore produced different feed bytes between builds.

Exact-head CI then exposed a separate stale test that froze one steering sentence even though the current steering preserved the same public-money accountability intent.

## Smallest correction

Gov Metrics PR #255:

- use `snapshot.meta.generatedAt` as the public-data.org snapshot edition;
- derive RSS build time from the sorted publication entries;
- remove wall-clock output from the static feed;
- add one focused semantic/determinism regression test;
- replace one exact-prose steering assertion with a durable intent assertion.

No dependency, schema package, new abstraction or new output surface was added.

## Feedback applied to Cave Pony

Added an explicit semantic ownership rule:

- values and labels must come from the event or authority they claim to describe;
- observation, publication, retrieval, validation, build and display time stay distinct;
- generated output is deterministic when inputs are unchanged;
- wall-clock, randomness, unstable ordering and environment-specific values require a present need;
- tests protect behaviour and invariants rather than incidental prose or implementation shape.

## Residual risk

The discoverability pull request is materially larger than the three-line correction because it predates this field test. Its full exact-head quality and browser gates must pass before merge. This field test does not claim a controlled cross-model or token comparison.
