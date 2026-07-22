# Comparative benchmark plan

Status: preregistered protocol. No numerical results are claimed.

## Release relationship

A comparative benchmark is required before Cave Pony makes numerical claims about code size, tokens, cost, speed, or safety relative to another condition. It is not required for an honest release that describes only the committed mechanism, limitations, and field records.

## Question

Does Cave Pony preserve correctness and safety while reducing unnecessary implementation surface and visible narration compared with the same coding agent using no skill, either parent, or both parents stacked?

## Arms

Use the same model and harness under five conditions:

1. no skill;
2. Ponytail;
3. Caveman;
4. Ponytail and Caveman stacked;
5. Cave Pony.

Pin every skill to an immutable commit and record the exact injected instructions.

## Controls

Keep constant:

- model, version, and reasoning setting;
- repository commit and task prompt;
- tools, permissions, network access, and test commands;
- time and token limits;
- temperature, seed, or equivalent controls where available;
- a fresh working tree and conversation for every run.

Start with at least five runs per task and arm. Increase repetitions when variance prevents a narrow claim. Do not discard failed, expensive, verbose, or inconvenient runs.

## Task set

Use real repositories whose licences allow publication of diffs and results. Define tasks before running them. Cover at least:

1. no change;
2. existing helper reuse;
3. native-platform reuse;
4. shared root-cause bug;
5. necessary small local implementation;
6. premature abstraction trap;
7. authentication or authorisation boundary;
8. destructive operation and recovery;
9. user-insisted broader safe scope;
10. already-minimal work where Cave Pony may offer no benefit.

Include losing and neutral cases deliberately.

## Eligibility gates

A run enters efficiency comparison only after it passes correctness and safety.

Correctness requires the requested behaviour, relevant tests, preserved compatibility, no unrelated removal, and no fabricated execution claim.

Safety requires preserved trust-boundary validation, authentication, authorisation, secret handling, accessibility, data-integrity guards, destructive consequences, ordering, preservation, and recovery.

A smaller unsafe solution is a failure, not an efficiency win.

## Measurements

Publish raw dimensions separately.

### Implementation footprint

- added, removed, and net lines;
- changed and new files;
- dependencies, abstractions, options, state, services, jobs, and public APIs;
- duplicated rules introduced or removed;
- reviewer-rated necessity of each added surface.

### Attention footprint

- visible and total tokens where available;
- repeated facts, unrequested narration, and raw-log volume;
- time for a blinded reader to find result, proof, risk, and next action.

### Assurance

- checks actually run;
- regression-check quality;
- false pass claims;
- residual risks disclosed;
- destructive prerequisites and recovery;
- blinded reviewer confidence.

### Operations

Where available, record elapsed time, model cost, tool calls, failed edits, retries, and instruction-context size.

## Review and publication

Use at least two reviewers blinded to the arm for subjective scoring. Publish the rubric, disagreements, and inter-rater agreement.

A public numerical claim requires immutable task definitions, exact prompts and skill text, all runs and diffs, test evidence, scoring scripts, exclusions, per-task results, distributions or confidence intervals, limitations, losing cases, and reproduction instructions.

Publish raw measurements before any composite score. Correctness and safety remain pass/fail gates and may not be averaged away.

## Claims policy

Use the narrowest statement supported by the evidence.

Acceptable:

> In this pinned benchmark of N tasks using model M, Cave Pony changed X fewer files on median while all eligible runs passed the published safety gates.

Unacceptable:

> Cave Pony always writes less code, saves tokens, and is safer.

Do not transfer results between models, harnesses, languages, or task classes without new evidence.

## Publication decision

Move a numerical claim into the README only when the protocol was fixed before final results, every arm ran equivalently, gates were enforced, raw artefacts reproduce, losing cases are visible, and the headline is no stronger than the data.
