<p align="center">
  <img src="./assets/cave-pony-logo.png" width="320" alt="Cave Pony logo">
</p>

<h1 align="center">Cave Pony</h1>

<p align="center"><strong>Write less code. Say less. Never fake proof.</strong></p>

<p align="center">
  <a href="https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml"><img src="https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT licence"></a>
  <img src="https://img.shields.io/badge/version-0.2.0-blue.svg" alt="Version 0.2.0">
</p>

[Caveman](https://github.com/JuliusBrussee/caveman) makes your agent talk less. [Ponytail](https://github.com/DietrichGebert/ponytail) makes it build less. **Cave Pony does both in one ~350-word skill**, and adds the rule neither has: *never say a check passed unless it ran.*

```bash
npx skills add wilfgrainger/cave-pony
```

Then type `/cave-pony` in Claude Code or `$cave-pony` in Codex. Say `stop cave-pony` to turn it off.

## What it does

- **Build less:** read the code the task touches, then take the first option that works: no change, delete, reuse, stdlib, installed dependency, new code. Fix the root cause once.
- **Say less:** answer first, no filler, exact code and errors. Plain sentences for warnings, ordered steps, and anything written to disk.
- **Prove enough:** run the check that would catch a regression, and say plainly what did and didn't run. Finish with `Done` / `Proof` / `Skipped` / `Risk`, using only the lines that apply.
- **Never cut:** input validation, auth, secrets handling, error handling that prevents data loss, accessibility. Before anything irreversible, it explains the damage and the recovery, then waits for your go-ahead.

That's the whole product: [`skills/cave-pony/SKILL.md`](skills/cave-pony/SKILL.md). It takes a minute to read.

## Does it work?

Measured, not claimed. [`eval/`](eval/) gives the same 8 coding tasks to headless Claude Code with no skill, Caveman, Ponytail, both stacked, and Cave Pony. It scores hidden-test correctness first, then whether the agent verified its change, diff size, reply length and cost.

Results from 5 November 2026: Claude Sonnet 5.5, 3 runs per task per arm ([raw results, including every command run](eval/results/published.jsonl)).

| Arm | Correct | Verified its change | Diff lines | Reply words | Output tokens | $/run |
|---|---|---|---|---|---|---|
| No skill | 24/24 | 10/18 | 14.5 | 85 | 641 | 0.015 |
| Caveman | 24/24 | 8/18 | 14.4 | 68 | 688 | 0.016 |
| Ponytail | 24/24 | 13/18 | 12.5 | 85 | 673 | 0.016 |
| Caveman + Ponytail | 24/24 | 13/18 | 11.4 | 73 | 709 | 0.017 |
| **Cave Pony** | 24/24 | **16/18** | **10.9** | **56** | 704 | 0.016 |

"Verified" counts the code-changing runs where the agent successfully ran Python or pytest after editing. The other columns are means per run.

- **Shortest replies:** 34% fewer words than no skill, and 18% fewer than Caveman alone.
- **Verifies most often:** it checked 16 of 18 code changes, against 10 with no skill.
- **Smallest diffs:** 25% below no skill, level with Caveman and Ponytail stacked.
- **Costs the same:** cost is level with the other skills. Output tokens are about 10% above no skill, which pays for the checks.
- **Not yet shown:** a correctness difference. Every arm solved every task, so harder tasks are needed. With 3 runs per task, treat small gaps as noise.

Reproduce it with `make eval` (about $2). `make test` fails if this table drifts from the raw results.

## Contributing

The skill should stay small and earn every word.

1. **Show a failure:** the prompt, what the agent did, and what it should have done. Best of all, add it as an eval task: `eval/tasks/<name>/` with `repo/`, `prompt.txt` and a hidden `check.py`.
2. **Measure it:** run `make eval` before and after your change, and paste both summary tables in the PR.
3. **The bar:** a change that adds words must win on the eval. A change that removes words only has to not lose.

Tasks where Cave Pony loses are the most useful contribution.

## Credits

Built on ideas from Caveman and Ponytail. It is independently written and not endorsed by either project; see [NOTICE](NOTICE.md). The earlier 0.1 contract is at tag [`v0.1.1`](https://github.com/wilfgrainger/cave-pony/tree/v0.1.1). MIT licensed.
