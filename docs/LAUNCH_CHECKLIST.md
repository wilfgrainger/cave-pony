# Launch checklist

Owner: Wilfred Grainger
Target: public `v1.0.0`
Current state: pre-release `0.1.0`

A checked item means committed evidence exists. Verbal confidence is not completion.

## Product truth

- [x] One-sentence outcome: produce the smallest trustworthy coding-agent change.
- [x] Independent mechanism documented: footprint budget, attention budget, assurance constraint.
- [x] Clear explanation of why a coordinated skill exists instead of silently stacking parents.
- [x] Activation, persistence, stop behaviour, audit mode, and safety override specified.
- [x] Real field record published with limitations.
- [ ] At least three independent users have used Cave Pony on real repository work. Tracked in [issue #21](https://github.com/wilfgrainger/cave-pony/issues/21).
- [x] A public neutral field record shows no demonstrated improvement to the core contract: [Cave Pony self-audit](../field-tests/2026-07-24-cave-pony-self-audit-neutral.md).
- [ ] Repeated user confusion has been tested against the clarity override.

## Evidence and claims

- [x] README makes no unsupported numerical performance claim.
- [x] Comparative benchmark work is deferred until a concrete numerical claim requires it.
- [x] Every current README claim is limited to committed documentation or published field records.
- [ ] Before any numerical claim, preregister equivalent conditions, correctness and safety gates, raw artefacts, scoring, limitations, losing cases, and reproduction instructions. Tracked in [issue #19](https://github.com/wilfgrainger/cave-pony/issues/19).
- [ ] Correctness and safety gates independently reviewed before any comparison is published.

## Legal, attribution, and ethics

- [x] Parent projects named and linked prominently.
- [x] Non-affiliation and non-endorsement language present.
- [x] Reviewed parent snapshots pinned in `THIRD_PARTY_NOTICES.md`.
- [x] Full parent MIT notices retained in `licenses/`.
- [x] Independent Cave Pony contributions listed specifically.
- [x] Original logo does not reuse parent brand assets.
- [x] Preliminary name, class and design-search scope recorded without claiming clearance in [Brand diligence](BRAND_CLEARANCE.md).
- [ ] Interactive name and relevant software-class searches completed in official UK, EU and US trade mark databases.
- [ ] Licensing and branding reviewed by a suitably qualified person before commercial use.
- [x] Courtesy messages prepared in [Maintainer outreach](MAINTAINER_OUTREACH.md).
- [ ] Courtesy note delivered to each parent maintainer. Tracked with brand diligence in [issue #24](https://github.com/wilfgrainger/cave-pony/issues/24).
- [ ] Any requested attribution correction resolved before launch.

Do not publish a maintainer's private reply without permission.

## Repository and release

- [x] Standalone repository declared canonical.
- [x] Repository contains no integration, persona, or unrelated-team references.
- [x] README front door includes logo, outcome, example, installation, safety, evidence, origins, and status.
- [x] CI runs the validator and tests once on Python 3.12.
- [x] No runtime package or third-party Python dependency required.
- [x] Default branch contains no obsolete release automation or benchmark artefacts.
- [x] Version `0.1.0` is consistent across skill and documentation.
- [x] Upgrade, removal, and recovery instructions documented.
- [x] Security reporting route documented.
- [ ] Immutable `v1.0.0` tag created from a verified commit.
- [ ] GitHub Release created with concise notes and migration information.
- [ ] Install command pinned to immutable release rather than moving `main`.
- [ ] Release archive installation tested from a clean environment.
- [ ] Upgrade and uninstall instructions tested from a clean environment.
- [ ] Repository social preview configured using the original logo.
- [ ] Repository description and topics set for discovery. Both metadata items are tracked in [issue #23](https://github.com/wilfgrainger/cave-pony/issues/23).

## Installation coverage

Do not claim support merely because a file format appears compatible.

- [x] Public remote `npx skills add` command passed on [CI run #200](https://github.com/wilfgrainger/cave-pony/actions/runs/30134001186) with `skills@1.5.9`, Codex project scope, copy mode, and a clean temporary directory.
- [ ] Claude Code installation documented and tested.
- [x] Codex project-installation mechanism passed with `skills@1.5.9` on [CI run #193](https://github.com/wilfgrainger/cave-pony/actions/runs/30133587016) at commit `ed172c6a5bffcc9a540bda628d72e10f8a498995`.
- [ ] The exact `v1.0.0` release commit repeats the Codex installation proof.
- [ ] Codex activation, level switching, audit, destructive clarity and stop behaviour tested in an authenticated fresh session. Tracked in [issue #22](https://github.com/wilfgrainger/cave-pony/issues/22).
- [ ] Hermes installation documented and tested.
- [ ] OpenClaw installation documented and tested.
- [x] Generic manual installation, verification, upgrade, removal, and recovery documented.
- [x] Host-specific limitations and support-claim policy recorded in [Host verification](HOST_VERIFICATION.md).

Add new adapters only after a named user or launch channel requires them.

## Security and operations

- [x] Destructive-operation clarity rules covered by static contract probes.
- [x] Authentication, authorisation, secrets, data-loss, accessibility, and repeated-question boundaries covered by static contract probes.
- [x] No network call or secret required by the skill itself.
- [x] CI permissions restricted to repository read.
- [x] Workflow actions pinned to immutable commits and re-reviewed on 2026-07-22.
- [ ] Recovery steps tested for install and uninstall failure.
- [x] Security reporting route added.
- [ ] Release commit and tag verified after publication.

## Community readiness

- [x] Contribution rules require concrete failures and evidence.
- [x] Numerical claims policy documented.
- [x] FAQ covers origin, stacking, guarantees, host support, destructive work, and commercial-use caution.
- [x] Three launch examples prepared: no change, native reuse, destructive clarity.
- [ ] Issue templates added only if actual issue volume justifies them.
- [ ] Code of conduct added if an external contributor community begins forming.
- [ ] One short terminal recording or image prepared using a real reproducible task.
- [ ] FAQ reviewed by someone unfamiliar with the parent projects.
- [ ] README tested at desktop and mobile widths.

## Go/no-go decision

Launch `v1.0.0` only when all of these are true:

- comparative claims are reproducible or omitted;
- critical installation paths work from clean environments;
- parent attribution and licence retention are complete;
- branding is independently recognisable and appropriately cleared;
- safety probes and CI pass at the exact release commit;
- an immutable tag and release exist;
- material residual risks are written down.

A smaller honest launch is better than a large launch built on claims the repository cannot yet prove.
