<p align="center">
  <img src="./assets/cave-pony-logo.png" width="360" alt="Cave Pony logo">
</p>

<h1 align="center">Cave Pony</h1>

<p align="center"><strong>Write less code. Say less. Never fake proof.</strong></p>

<p align="center">
  <a href="https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml"><img src="https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT licence"></a>
  <img src="https://img.shields.io/badge/version-0.2.0-blue.svg" alt="Version 0.2.0">
</p>

[Caveman](https://github.com/JuliusBrussee/caveman) makes your agent talk less. [Ponytail](https://github.com/DietrichGebert/ponytail) makes it build less. Cave Pony does both in **one ~350-word skill**, and adds one rule neither has: *never say a check passed unless it ran.*

```bash
npx skills add wilfgrainger/cave-pony
```

Then say `/cave-pony` in Claude Code, or `$cave-pony` in Codex. Say `stop cave-pony` to turn it off.

## What it does

- **Build less:** read the touched code, then take the first rung that works: no change, delete, reuse, stdlib, installed dependency, new code. Fix the root cause once.
- **Say less:** answer first, no filler, exact code and errors. Plain sentences for anything risky or irreversible.
- **Prove enough:** run the check that would catch a regression. Never claim a check ran when it didn't. End with `Done` / `Proof` / `Skipped` / `Risk`, using only the lines that apply.

The whole contract is [`skills/cave-pony/SKILL.md`](skills/cave-pony/SKILL.md). It takes a minute to read.

## Does it work?

Measured, not claimed. [`eval/`](eval/) runs the same 8 tasks through headless Claude Code with no skill, Caveman, Ponytail, both stacked, and Cave Pony. It scores hidden-test correctness first, then whether the agent verified its change, diff size, reply length and cost.

<!-- results -->
Run on 5 November 2026: Claude Sonnet 5.5, 8 tasks × 3 runs per arm ([raw results with every command run](eval/results/published.jsonl)).

| Arm | Correct | Verified its change | Diff lines | Reply words | Output tokens | $/run |
|---|---|---|---|---|---|---|
| No skill | 24/24 | 10/18 | 14.5 | 85 | 641 | 0.015 |
| Caveman | 24/24 | 8/18 | 14.4 | 68 | 688 | 0.016 |
| Ponytail | 24/24 | 13/18 | 12.5 | 85 | 673 | 0.016 |
| Caveman + Ponytail | 24/24 | 13/18 | 11.4 | 73 | 709 | 0.017 |
| **Cave Pony** | 24/24 | **16/18** | **10.9** | **56** | 704 | 0.016 |

"Verified" means the agent successfully ran Python or pytest after editing, on runs that changed code. Diff lines, words and tokens are means per run; output tokens cover the whole session.

What this shows:

- **Shortest replies:** 34% fewer words than no skill, and 18% fewer than Caveman alone.
- **Smallest diffs:** 25% below no skill; level with Caveman + Ponytail stacked.
- **Verifies most often:** 16 of 18 code changes, against 10 with no skill and 8 with Caveman alone.
- **Costs about the same:** output tokens are about 10% above no skill, and cost per run is level with Caveman and Ponytail.
- **No correctness difference:** every arm solved every task, so these tasks are too easy to separate the arms on correctness. Harder tasks are needed.
- **Small sample:** 3 runs per task. Treat gaps of one or two lines, or a couple of runs, as noise.

Earlier runs on the same day are kept in [`eval/results/`](eval/results/). An independent review found that their verification and token metrics were too loose, so they are not comparable with this table.
<!-- /results -->

Reproduce: `make eval` (about $2 for 120 runs). Eval tasks where Cave Pony loses are the most welcome contribution. See [CONTRIBUTING](CONTRIBUTING.md).

## Rules it never breaks

It never cuts input validation, auth, secrets handling, error handling that prevents data loss, or accessibility. Anything irreversible (delete, reset, force-push, drop, migrate) gets full plain sentences. Commits, docs and code comments use normal grammar.

## Credits

Built on ideas from Caveman and Ponytail. It is independently written and not endorsed by either project; see [Third-party notices](THIRD_PARTY_NOTICES.md). The previous, longer 0.1.x contract lives at tag [`v0.1.1`](https://github.com/wilfgrainger/cave-pony/tree/v0.1.1). MIT licensed.
