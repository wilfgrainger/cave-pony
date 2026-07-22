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
- [ ] At least three independent users have used Cave Pony on real repository work.
- [ ] At least one public field record shows no material improvement or a losing case.
- [ ] Repeated user confusion has been tested against the clarity override.

## Evidence and claims

- [x] Comparative protocol preregistered in [`BENCHMARK_PLAN.md`](BENCHMARK_PLAN.md).
- [x] README makes no unsupported numerical performance claim.
- [ ] Baseline, Ponytail, Caveman, stacked parents, and Cave Pony runs complete under equivalent conditions.
- [ ] Correctness and safety gates independently reviewed.
- [ ] Raw artefacts and reproduction instructions published.
- [ ] Limitations and losing cases visible beside headline results.
- [ ] Every launch claim traced to committed evidence.

## Legal, attribution, and ethics

- [x] Parent projects named and linked prominently.
- [x] Non-affiliation and non-endorsement language present.
- [x] Reviewed parent snapshots pinned in `THIRD_PARTY_NOTICES.md`.
- [x] Full parent MIT notices retained in `licenses/`.
- [x] Independent Cave Pony contributions listed specifically.
- [x] Original logo does not reuse parent brand assets.
- [ ] Name and relevant software classes searched in UK, EU, and US trademark databases.
- [ ] Licensing and branding reviewed by a suitably qualified person before commercial use.
- [ ] Courtesy note sent privately to each parent maintainer.
- [ ] Any requested attribution correction resolved before launch.

Suggested courtesy note:

```text
Subject: Courtesy note: Cave Pony, inspired by Ponytail/Caveman

I built Cave Pony, an independently authored coding-agent skill inspired by
Ponytail's implementation discipline and Caveman's communication discipline.
It coordinates implementation footprint, attention cost, and proof under one
safety contract.

Your project is prominently credited and linked. The reviewed source snapshot,
full MIT notice, and exact influence are documented. Cave Pony does not claim
affiliation or endorsement and does not reuse your visual identity.

I am preparing a public release and wanted to give you a heads-up. I would
welcome corrections to the attribution or positioning. This is not a request
for endorsement.
```

Do not publish a maintainer's private reply without permission.

## Repository and release

- [x] Standalone repository declared canonical.
- [x] Skill synced from the latest `agent-skills/skills/cave-pony/SKILL.md` source available during launch preparation.
- [x] README front door includes logo, outcome, example, installation, safety, evidence, origins, and status.
- [x] CI validates Python 3.10 and 3.12.
- [x] No runtime or development dependency required.
- [ ] Working tree and default branch contain no obsolete release artefacts.
- [ ] Version updated consistently across skill and documentation.
- [ ] Immutable `v1.0.0` tag created from a verified commit.
- [ ] GitHub Release created with concise notes and migration information.
- [ ] Install command pinned to immutable release rather than moving `main`.
- [ ] Release archive installation tested from a clean environment.
- [ ] Upgrade and uninstall instructions tested.
- [ ] Repository social preview configured using the original logo.
- [ ] Repository description and topics set for discovery.

## Installation coverage

Do not claim support merely because a file format appears compatible.

- [ ] `npx skills add` tested from a clean environment.
- [ ] Claude Code installation documented and tested.
- [ ] Codex installation documented and tested.
- [ ] Hermes installation documented and tested.
- [ ] OpenClaw installation documented and tested.
- [ ] Generic manual installation documented and tested.
- [ ] Activation, level switching, audit, and stop behaviour checked in each claimed host.
- [ ] Host-specific limitations recorded.

Add new adapters only after a named user or launch channel requires them.

## Security and operations

- [x] Destructive-operation clarity rules covered by behavioural probes.
- [x] No network call or secret required by the skill itself.
- [x] CI permissions restricted to repository read.
- [ ] Dependency and workflow actions re-reviewed at release commit.
- [ ] Recovery steps tested for install and uninstall failure.
- [ ] Security reporting route added before broad promotion.
- [ ] Release commit and tag verified after publication.

## Community readiness

- [x] Contribution rules require concrete failures and evidence.
- [x] Numerical claims policy documented.
- [ ] Issue templates added only if actual issue volume justifies them.
- [ ] Code of conduct added if an external contributor community begins forming.
- [ ] Three launch examples prepared: no change, native reuse, destructive clarity.
- [ ] One short terminal recording or image prepared using a real reproducible task.
- [ ] FAQ reviewed by someone unfamiliar with Ponytail and Caveman.
- [ ] README tested at desktop and mobile widths.

## Launch communication

The launch story is:

> Cave Pony makes coding agents produce the smallest trustworthy change: less implementation, less narration, and proof proportional to risk.

It is not:

> We combined two famous skills and made them better.

Required launch materials:

- [ ] Technical launch article centred on the coordination problem and evidence.
- [ ] Hacker News submission with reproducible benchmark, not star solicitation.
- [ ] Concise GitHub, LinkedIn, and X examples tailored to each audience.
- [ ] Relevant skill registries and curated lists identified.
- [ ] Private testers told the release is available; no coordinated artificial starring.
- [ ] Response prepared for fair criticism and corrections.

Prepared response to “Is this a copy?”:

> Cave Pony is explicitly inspired by Ponytail and Caveman, which are credited
> with pinned source snapshots and retained MIT notices. It is independently
> authored and addresses the coordination problem between implementation
> footprint, communication footprint, and proof. It is not affiliated with or
> endorsed by either project.

## Go/no-go decision

Launch `v1.0.0` only when all of these are true:

- comparative claims are reproducible or omitted;
- critical installation paths work from clean environments;
- parent attribution and licence retention are complete;
- branding is independently recognisable;
- safety probes and CI pass at the exact release commit;
- an immutable tag and release exist;
- material residual risks are written down.

A smaller honest launch is better than a large launch built on claims the repository cannot yet prove.
