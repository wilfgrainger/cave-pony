# Origins and differences

Cave Pony is an independently authored coding-agent skill inspired by two MIT-licensed projects:

- [Ponytail](https://github.com/DietrichGebert/ponytail), which challenges unnecessary implementation;
- [Caveman](https://github.com/JuliusBrussee/caveman), which challenges unnecessary prose.

It is not a fork, official successor, affiliated project, or endorsed project.

## The coordination problem

Installing two useful instruction sets does not automatically create one coherent operating contract.

Implementation minimalism and communication minimalism can conflict:

- an agent can choose a tiny diff before understanding the complete affected path;
- a terse report can hide that no test ran;
- a compressed destructive command can omit preservation and recovery steps;
- two activation systems can both claim the conversation;
- two sets of levels and stop commands can produce ambiguous state;
- repeated parent instructions consume context and can drift separately;
- a minimal implementation can still create excessive proof theatre;
- a short answer can still defend an unnecessary abstraction.

Cave Pony addresses that coordination problem directly.

## What each project primarily controls

| Project | Primary control | Characteristic question |
|---|---|---|
| Ponytail | Implementation footprint | Does this need to exist, or can the project already do it more simply? |
| Caveman | Output verbosity | What technical substance remains after filler is removed? |
| Cave Pony | Coordinated footprint, attention, and assurance | What is the smallest trustworthy change and the shortest report that still proves it? |

The comparison describes project intent, not superiority. Each parent remains useful independently.

## Cave Pony's independent mechanism

Cave Pony coordinates two budgets under an assurance constraint.

### 1. Footprint budget

The agent reads the complete affected path, then stops at the first correct rung:

1. no change;
2. delete or simplify;
3. reuse the codebase;
4. use the standard library or runtime;
5. use a native platform capability;
6. use an installed dependency;
7. add the smallest local implementation;
8. add a dependency or abstraction only after simpler options fail a present requirement.

### 2. Attention budget

The agent removes filler, hedging, self-reference, repeated framing, routine narration, decorative output, invented abbreviations, and raw-log dumping while preserving exact technical meaning.

### 3. Assurance constraint

Neither budget may remove the proof and clarity justified by the risk. Checks expand for money, identity, permissions, security, destructive operations, concurrency, migrations, compatibility, and data loss.

Destructive and order-sensitive work temporarily returns to explicit prose.

## Independent controls

Cave Pony separates implementation pressure from communication pressure:

```text
/cave-pony build=ultra voice=lite
/cave-pony build=lite voice=ultra
```

This allows a user to challenge speculative architecture while keeping a full professional explanation, or accept a requested implementation while aggressively removing narration.

## One proof report

Completed work uses only relevant lines:

```text
Done: <result and location>
Proof: <checks actually run>
Skipped: <surface omitted and the trigger to revisit it>
Risk: <material residual risk or blocker>
```

The report exists to make small work auditable, not to force ceremonial sections into every answer.

## One clarity override

Security, privacy, destructive actions, migrations, recovery, legal or financial risk, and ordered procedures override compression. The user must still see prerequisites, ordering, consequences, preservation, and recovery.

A repeated question is treated as evidence that compression failed.

## One audit mode

`/cave-pony audit` reviews both implementation footprint and attention cost. It ranks real findings by impact and asks for the smallest correction. It does not manufacture a fixed number of findings.

## Why not install both parents?

You can. Stacking Ponytail and Caveman is a valid option when users prefer the original projects and accept overlapping instructions and context.

Cave Pony is useful when users want:

- one activation and persistence model;
- independent build and voice levels;
- explicit conflict resolution;
- one shared safety override;
- proportional proof requirements;
- one audit covering code surface and narration;
- a smaller coordinated instruction contract.

These claims are architectural descriptions. Numerical performance claims require the protocol in [`BENCHMARK_PLAN.md`](BENCHMARK_PLAN.md).

## What Cave Pony does not claim

Cave Pony does not claim:

- that Ponytail or Caveman is deficient;
- that stacking the parents is unsafe by default;
- that Cave Pony always produces fewer tokens, less code, lower cost, or faster execution;
- that static tests guarantee host-model behaviour;
- that either parent maintainer has reviewed or endorsed the project;
- ownership of either parent name, identity, or brand.

## Attribution and provenance

Exact reviewed snapshots, retained MIT notices, quotations, and conceptual influences are documented in [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

The Cave Pony skill wording, coordination model, tests, documentation, and original 8-bit logo are independently authored for this repository.
