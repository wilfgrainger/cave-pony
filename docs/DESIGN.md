# Design and implementation

## Problem

Coding agents can inflate implementation and narration independently. Ponytail challenges the first. Caveman challenges the second. Cave Pony coordinates both without allowing either to weaken correctness.

## Independent mechanism

Cave Pony controls:

- a build budget for owned implementation surface;
- an attention budget for human reading cost;
- an assurance constraint that preserves proof and safety justified by risk.

The two axes can be tuned independently. A shared clarity override wins whenever compression conflicts with security, privacy, destructive actions, migrations, recovery, legal or financial risk, or ordered procedures.

## Execution model

The loop has five steps:

1. understand before shrinking;
2. climb the footprint ladder;
3. fix the root once;
4. prove enough;
5. report tersely.

The ladder is ordered by owned surface: no change, deletion, reuse, standard library, native platform, installed dependency, smallest local implementation, then a dependency or abstraction only when simpler options fail a present requirement.

YAGNI decides whether work is needed. KISS chooses the simplest correct design. DRY centralises stable repeated knowledge rather than similar syntax.

## Proof model

The smallest decisive proof is the cheapest existing check capable of falsifying the claimed behaviour. Non-trivial changed logic leaves one runnable regression check. Proof expands for money, identity, permissions, security boundaries, destructive operations, concurrency, migrations, compatibility, and data loss.

Static repository tests protect the written contract. They do not guarantee that every model or host will obey it.

## Output model

Result or code comes first. Completed work uses only relevant Done, Proof, Skipped, and Risk lines. Requested reports and documentation remain complete deliverables.

Normal explicit prose temporarily overrides compression for risk, ordering, consequences, preservation, and recovery. A repeated question is evidence that earlier compression failed.

## Activation and coexistence

Activation is explicit or coding-scoped. Generic non-coding requests for brevity do not activate Cave Pony.

Cave Pony is intended to be active instead of overlapping minimalism or terse-output skills. It cannot unload a host-managed skill; hosts must disable overlap themselves.

## Validation

`tools/validate.py` protects durable repository contracts:

- the complete launch-critical file inventory and PNG logo;
- skill frontmatter, activation scope, five-step loop, and parent-root terms;
- authentication, authorisation, secrets, data-loss, accessibility, compatibility, legal, and operational boundaries;
- destructive and repeated-question static cases, including exact contract terms;
- version consistency across the skill and public documentation;
- parent attribution and standalone repository separation;
- one-job, main-scoped, read-only CI with immutable action commits;
- clean text formatting.

`tests/test_repository.py` proves that high-impact regressions are rejected, including missing launch files, version drift, CI write permission, mutable actions, unsafe boundary removal, invalid branding assets, and unrelated integration references.

## Packaging and extension

No package builder exists because no confirmed consumer requires one. The skill directory is the installable unit.

A proposal should show a concrete failure, explain why the current rules miss it, make the smallest correction, and add one regression when the durable contract would otherwise drift. `SKILL.md` remains the behavioural source of truth.
