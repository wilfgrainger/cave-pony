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

It is **not a token saver.** Nothing in this category is (see below). What it buys is a change you can trust at a glance: small, checked, and reported in a few lines.

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

Measured, not claimed. [`eval/`](eval/) gives 12 coding tasks to headless Claude Code with no skill, Caveman, Ponytail, both stacked, and Cave Pony. Four tasks are built to catch the failures minimal-change skills are known for: a quoted-CSV edge case, a return-shape change whose caller must be updated, the same bug duplicated in a second file, and a two-part requirement where one half is easy to drop. Each hidden check rejects the plausible-but-incomplete fix.

Two models, 3 runs per task per arm, 180 runs each, on 5 November 2026. Raw results, including every command run: [Sonnet 5.5](eval/results/published.jsonl) and [Haiku 5.5](eval/results/haiku-2026-11-05.jsonl).

### Sonnet 5.5

| Arm | Correct | Verified its change | Diff lines | Reply words | Total tokens | $/run |
|---|---|---|---|---|---|---|
| No skill | 36/36 | 15/30 | 14.4 | 87 | 30039 | 0.017 |
| Caveman | 36/36 | 18/30 | 12.8 | 76 | 38468 | 0.019 |
| Ponytail | 36/36 | 23/30 | 11.6 | 93 | 33940 | 0.018 |
| Caveman + Ponytail | 36/36 | 24/30 | 12.1 | 79 | 42310 | 0.019 |
| **Cave Pony** | 35/36 | **30/30** | **10.7** | **69** | 35728 | 0.020 |

### Haiku 5.5

| Arm | Correct | Verified its change | Diff lines | Reply words | Total tokens | $/run |
|---|---|---|---|---|---|---|
| No skill | 36/36 | 30/30 | 17.4 | 138 | 47930 | 0.0020 |
| Caveman | 36/36 | 29/30 | 13.9 | 87 | 58177 | 0.0020 |
| Ponytail | 36/36 | 29/30 | 13.7 | 145 | 52855 | 0.0022 |
| Caveman + Ponytail | 36/36 | 30/30 | 14.1 | 105 | 60274 | 0.0021 |
| **Cave Pony** | 36/36 | 30/30 | **13.4** | **109** | 52949 | 0.0022 |

"Verified" counts code-changing runs where the agent successfully ran Python or pytest after editing. Total tokens are input + cache + output for the whole session, which is what the bill is made of. The other columns are means per run.

What the two models show:

- **Smaller changes and shorter replies hold on both models.** Against no skill, Cave Pony changes 25% fewer lines and writes 21% fewer reply words on Sonnet, and 23% fewer lines and 21% fewer words on Haiku.
- **Checking its work is a Sonnet effect.** On Sonnet, Cave Pony verified 30 of 30 changes against 15 of 30 with no skill. On Haiku, no skill already verified 30 of 30, so there is no gain to claim there.
- **No skill saves tokens.** Every skill raised total tokens on both models: on Sonnet, Cave Pony +19%, Caveman +28%, both together +41%; on Haiku, Cave Pony +10%, Caveman +21%, both together +26%. This matches [an independent 140-run study](https://www.stet.sh/blog/gpt-56-token-saving-modes) on GPT 5.6, where no token-saving method cut total tokens in both runs.
- **Correctness does not separate the arms yet.** On Haiku every arm passed all 36 runs, including the four hard tasks. On Sonnet, Cave Pony's one miss was a date parser that accepted an ISO week date (`2026-W10-6`) the task ruled out. With 3 runs per task, treat gaps of a few runs as noise.
- **Haiku costs about 1/8 of Sonnet per run** ($0.002 against $0.017), though it used more tokens and tool calls to get there.

Reproduce Sonnet with `make eval` (about $3.50), or Haiku with `python3 eval/run.py --model claude-haiku-5-5` (about $0.40). `make test` fails if this table drifts from the raw results.

## Contributing

The skill should stay small and earn every word.

1. **Show a failure:** the prompt, what the agent did, and what it should have done. Best of all, add it as an eval task: `eval/tasks/<name>/` with `repo/`, `prompt.txt` and a hidden `check.py`.
2. **Measure it:** run `make eval` before and after your change, and paste both summary tables in the PR.
3. **The bar:** a change that adds words must win on the eval. A change that removes words only has to not lose.

Tasks where Cave Pony loses are the most useful contribution.

## Credits

Built on ideas from Caveman and Ponytail. It is independently written and not endorsed by either project; see [NOTICE](NOTICE.md). The earlier 0.1 contract is at tag [`v0.1.1`](https://github.com/wilfgrainger/cave-pony/tree/v0.1.1). MIT licensed.
