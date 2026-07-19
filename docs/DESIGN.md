# Design and implementation

## Problem

Coding agents can inflate two independent surfaces: implementation and narration. Ponytail attacks the first. Caveman attacks the second. Cave Pony coordinates both without allowing either to weaken correctness.

## Parent fidelity

Cave Pony keeps Ponytail’s core behaviour:

1. understand the complete affected path;
2. ask whether the change needs to exist;
3. reuse the codebase, standard library, native platform, and installed dependencies before new code;
4. prefer deletion, boring code, few files, and the smallest root-cause fix;
5. leave one runnable check for non-trivial logic;
6. stop re-arguing when the user knowingly insists on broader safe scope.

It keeps Caveman’s core behaviour:

1. remove filler, hedging, pleasantries, self-reference, and routine narration;
2. use short words, fragments, and omitted articles only where meaning remains obvious;
3. preserve exact technical strings and the user’s language;
4. avoid invented abbreviations, prose arrows, decorative output, and raw-log dumps;
5. suspend compression when risk or ordering needs normal prose;
6. keep code, commits, PRs, documentation, and quoted material in normal grammar unless the user asks otherwise.

## Intentional parent divergences

Cave Pony changes only the coordination rules needed to combine the parents safely:

- **Explicit activation:** uncertainty or preloading does not activate the skill. Implicit triggers apply only within coding or agent work.
- **Two axes:** `build` and `voice` can be tuned independently.
- **One clarity override:** destructive, security-sensitive, legal, financial, recovery, and ordering-sensitive content uses explicit prose.
- **One compact report:** completed changes may state Done, Proof, conditional Skipped, and Risk; empty lines disappear.
- **One-shot audit:** audit mode reviews without editing unless fixes are requested.

There is no global `normal mode` alias because both parent skills claim it independently.

## Behavioural model

```text
build ∈ {lite, full, ultra}
voice ∈ {lite, full, ultra}
```

A one-word level sets both. Axis assignments override one value. Default state is `build=full voice=full`.

The execution loop has five steps:

1. understand before shrinking;
2. climb the footprint ladder;
3. fix the root once;
4. prove enough;
5. report tersely.

YAGNI decides whether work is presently needed. KISS chooses the simplest correct design. DRY centralises stable repeated knowledge, not merely similar syntax. They refine the ladder rather than add workflow phases.

## Footprint ladder

The ladder is ordered by owned surface: no change, deletion, reuse, standard library, native platform, installed dependency, one line or local code, then a new dependency or abstraction.

A durable addition pays a small complexity toll: a present requirement, a named simpler alternative that fails, and a benefit larger than its maintenance and failure surface. Standing instructions count because they consume context and can conflict.

A non-obvious deliberate shortcut gets one local `cave-pony:` comment naming its ceiling and concrete upgrade trigger. Obvious choices and hypothetical futures do not.

## Proof model

“Smallest decisive proof” means the cheapest existing check capable of falsifying the claimed behaviour. Non-trivial changed logic leaves one runnable regression check. Higher-risk work expands proof; trivial one-liners do not gain ceremonial tests.

The repository tests are static contract checks. They prove that the written rules and safety cases remain committed. They cannot guarantee that every host model will obey them.

## Output model

Result or code comes first. Unrequested explanation stays shorter than the work it explains. Requested reports, walkthroughs, and documentation remain complete deliverables.

Full voice uses short direct sentences or fragments, drops articles only when safe, and preserves standard technical acronyms. Ultra voice removes more words but never sequence, cause, scope, responsibility, or recovery.

The clarity override always wins ties. A repeated question is evidence that earlier compression failed and receives one normal, explicit answer.

## Validation

`tools/validate.py` checks only durable repository contracts:

- required files and frontmatter;
- explicit coding-context activation;
- the five-step loop and parent-root terms;
- destructive-operation safety language and behavioural-case schema;
- source attribution;
- immutable, read-only, main-scoped CI;
- clean text formatting.

`tests/test_repository.py` runs the validator and proves a small set of high-impact regressions are rejected. The validator deliberately does not freeze every sentence in the skill.

## Packaging and extension rules

No package builder exists because no confirmed consumer requires one. Installation tracks the skill directory directly.

A proposal should show a concrete failure, explain why the current rules miss it, make the smallest correction, and add or update one regression check when the contract would otherwise drift. Keep `SKILL.md` the single behavioural source of truth.
