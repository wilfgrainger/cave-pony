# Gov Metrics field test — iteration 3

Date: 2026-07-19
Target: `wilfgrainger/gov-metrics` PR #255 after iteration 2
Mode: Cave Pony `build=full voice=full`

## Scope

Re-review the corrected discoverability path, focusing on whether each public claim is supported by the same status predicate used to select its data.

## Finding

`getBuildPublication` accepted both `source.status === "ok"` and `source.status === "stale"`. `publicationEntries` then placed either result in a feed titled “latest verified evidence.” A last-known fallback can remain useful on its evidence page, but its presence does not justify promoting it as a new current publication.

## Smallest correction

Gov Metrics PR #255:

- require `source.status === "ok"` for Dataset update metadata and latest-publication feed entries;
- leave stale or unavailable evidence out of the update feed instead of relabelling it;
- add one rejected-state regression assertion alongside the accepted discovery contract.

The correction changes one status predicate and one focused test. It adds no dependency, component, fallback mechanism or user-facing warning system.

## Feedback applied to Cave Pony

Added an explicit claim-eligibility gate:

- data or fallback presence is not permission for every public or API use;
- the predicate that makes a claim true must be the predicate that gates it;
- stale, partial, unverified, unauthorized and incompatible states remain unavailable or clearly qualified;
- withholding can be the smallest correct result;
- material status gates test one accepted state and the most plausible rejected state.

## Residual risk

The public section page can still describe last-verified or unavailable evidence through its existing status UI. This correction only prevents stale fallback data from being promoted through latest-update discovery metadata. Full exact-head quality and browser checks remain required before merge.
