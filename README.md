<p align="center">
  <img src="./assets/cave-pony-logo.png" width="320" alt="Cave Pony logo">
</p>

<h1 align="center">Cave Pony</h1>

<p align="center"><strong>The smallest change, checked, reported briefly.</strong></p>

<p align="center">
  <a href="https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml"><img src="https://github.com/wilfgrainger/cave-pony/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT licence"></a>
  <img src="https://img.shields.io/badge/version-0.2.0-blue.svg" alt="Version 0.2.0">
</p>

**You may only need one sentence.** On Sonnet, this 41-word rule took the share of code changes where the agent then ran Python or pytest from 15 of 30 to 28 of 30; the full skill below got 30. Haiku already did it 30 of 30 with no instruction at all. Paste the rule into your `CLAUDE.md` or `AGENTS.md`:

```text
Make the smallest correct change. Before reporting a change as working, run a check that would catch a regression. Never say a check passed unless you ran it. Report what you changed, what you ran, and what you did not check.
```

What the full skill (about 340 words) adds beyond that rule: **replies about 50 words shorter** on both models we tested, and on Sonnet **diffs about two lines smaller**. We could not measure any gain in correctness, total tokens or running code afterwards, and we have not shown that smaller diffs or shorter replies are better. The [evidence](#what-the-eval-shows) and its [limits](#what-we-have-not-shown) are below.

To install the full skill:

```bash
npx skills add wilfgrainger/cave-pony
```

Then type `/cave-pony` in Claude Code or `$cave-pony` in Codex. Say `stop cave-pony` to turn it off.

## The skill

It combines [Caveman](https://github.com/JuliusBrussee/caveman)'s short replies with [Ponytail](https://github.com/DietrichGebert/ponytail)'s smallest-change ladder, and adds a rule not to claim a check passed unless it ran.

- **Build less:** read the code the task touches, then take the first option that works: no change, delete, reuse, stdlib, installed dependency, new code. Fix the root cause once.
- **Say less:** answer first, no filler, exact code and errors. Plain sentences for warnings, ordered steps, and anything written to disk.
- **Prove enough:** run the check that would catch a regression, and say plainly what did and didn't run. Finish with `Done` / `Proof` / `Skipped` / `Risk`, using only the lines that apply.
- **Never cut:** input validation, auth, secrets handling, error handling that prevents data loss, accessibility. Before anything irreversible, explain the damage and the recovery, then wait for the user's go-ahead.

The whole contract is [`skills/cave-pony/SKILL.md`](skills/cave-pony/SKILL.md): 387 words including its header, against 744 for Caveman's file and 592 for Ponytail's.

## What the eval shows

[`eval/`](eval/) gives 12 small Python tasks to headless Claude Code under six conditions: no skill, the one-line rule, Caveman, Ponytail, Caveman and Ponytail together, and Cave Pony. Each hidden check decides pass or fail. Four tasks are built to catch the failures minimal-change skills are known for: `csv-quoting` (a quoted-field edge case), `partial-failure` (a return-shape change whose caller must be updated), `timestamp-z` (the same bug in two files) and `export-limit` (a two-part requirement where one half is easy to drop). A fifth, `keep-validation`, asks the agent to simplify a messy function without dropping its input checks.

Three runs per task per condition on 5 November 2026 (36 runs per row). Raw results, including every command the agent ran: [Sonnet 5.5](eval/results/published.jsonl) and [Haiku 5.5](eval/results/haiku-2026-11-05.jsonl). The one-line rule was run separately, after the other five conditions, with the same runner and tasks. The `late-binding` check was widened after the first runs to accept a correct phrasing (the earlier check is in git history at commit `1fc5077`); re-scoring changed no Sonnet verdict and one Haiku verdict, a correct no-skill answer that had been rejected.

### Sonnet 5.5

| Arm | Correct | Ran code after editing | Diff lines | Reply words | Total tokens | $/run |
|---|---|---|---|---|---|---|
| No skill | 36/36 | 15/30 | 14.4 | 87 | 30039 | 0.017 |
| One-line rule | 36/36 | 28/30 | 13.0 | 117 | 35913 | 0.023 |
| Caveman | 36/36 | 18/30 | 12.8 | 76 | 38468 | 0.019 |
| Ponytail | 36/36 | 23/30 | 11.6 | 93 | 33940 | 0.018 |
| Caveman + Ponytail | 36/36 | 24/30 | 12.1 | 79 | 42310 | 0.019 |
| **Cave Pony** | 35/36 | 30/30 | 10.7 | 69 | 35728 | 0.020 |

### Haiku 5.5

| Arm | Correct | Ran code after editing | Diff lines | Reply words | Total tokens | $/run |
|---|---|---|---|---|---|---|
| No skill | 36/36 | 30/30 | 17.4 | 138 | 47930 | 0.0020 |
| One-line rule | 36/36 | 30/30 | 13.4 | 161 | 55613 | 0.0023 |
| Caveman | 36/36 | 29/30 | 13.9 | 87 | 58177 | 0.0020 |
| Ponytail | 36/36 | 29/30 | 13.7 | 145 | 52855 | 0.0022 |
| Caveman + Ponytail | 36/36 | 30/30 | 14.1 | 105 | 60274 | 0.0021 |
| **Cave Pony** | 36/36 | 30/30 | 13.4 | 109 | 52949 | 0.0022 |

"Ran code after editing" counts code-changing runs where the agent successfully ran Python or pytest after its first edit (the tool's summary calls it `verified`). It shows the agent ran something, not that the check was a good one. Total tokens are input, cache and output for the whole session; cost is reported separately because cache tokens are priced differently. The other columns are means per run. Where the text below says something is larger or smaller, it rests on a 95% interval that excludes zero, from resampling whole tasks; "within noise" or "do not differ" means the interval includes zero. Reproduce any of it with `python3 eval/run.py --summary-only --compare cave-pony,one-line` (add `--out eval/results/haiku-2026-11-05.jsonl` for Haiku).

- **Telling the agent to check buys the checking, and one sentence is enough.** On Sonnet, changes followed by running code went from 15 of 30 with no skill to 28 with the one-line rule and 30 with Cave Pony; the last two are not distinguishable at this sample size. Haiku did it 30 of 30 with no skill, so there was nothing to gain.
- **The extra words buy shorter replies, and on Sonnet smaller diffs.** Against the one-line rule, Cave Pony wrote 48 fewer words per reply on Sonnet and 51 fewer on Haiku. Its diffs were 2.2 lines smaller on Sonnet; on Haiku the two do not differ. The one-line rule makes replies longer than no skill (30 and 23 words more), probably because it asks for a report. On Haiku, Caveman alone writes shorter replies than Cave Pony (87 words against 109).
- **Nothing reduced total tokens against no skill.** On Sonnet every condition used more, Cave Pony by 5,688 tokens (19%), with an interval that only just excludes zero. On Haiku only Caveman, alone and with Ponytail, clearly used more; the rest are within noise. Cost tells a slightly different story because cache tokens are cheaper: Cave Pony's extra cost over no skill is within noise on both models, while the one-line rule costs more on both ($0.0056 more per run on Sonnet, $0.0004 on Haiku), and on Sonnet Cave Pony cost $0.0032 less per run than the one-line rule. [A 140-run study](https://www.stet.sh/blog/gpt-56-token-saving-modes) of token-saving methods on GPT 5.6 models (ten tasks, each run twice), written by someone building an eval tool of their own, found the same pattern for tokens: none of its six methods cut them in both repetitions.
- **Correctness does not separate the conditions.** On Haiku every condition passed all 36 runs. On Sonnet, Cave Pony's one miss was a date parser that accepted an ISO week date the task ruled out; everything else passed.

## What we have not shown

- **That smaller diffs are better.** Nothing here grades quality beyond the hidden checks. The study above found Caveman and Ponytail took their biggest quality hits on robustness and scope discipline. Every condition passed our four hard tasks on both models, so they cannot detect that kind of loss.
- **That shorter replies help anyone.** There is no user study, and tokens did not fall.
- **That the safety rules matter.** `keep-validation` checks that input validation survives a "simplify it" request, and every condition passed it, no skill included, so it shows nothing about the rule. No task tests confirmation before an irreversible action, or auth and secrets handling.
- **Long sessions.** Runs average 3 to 6 tool calls (0 to 14 in a single run), so the cost of re-reading a skill of this size on every turn of a long session is not measured.
- **Anything wider.** This is 12 small Python tasks, written by us, on two Claude models, 3 runs each.

## Status

The skill is frozen at 0.2.0. The eval says its extra words buy little over the one-line rule, so more rules are not the next step. A grader for scope and robustness on real merged changes is.

## Reproduce and contribute

`make eval` runs everything on Sonnet (216 runs, about $4.20). Haiku is `python3 eval/run.py --model claude-haiku-5-5` (about $0.46). `make test` fails if either table, or the rule printed at the top, drifts from the raw results.

The bar for any change to the skill is the one-line rule, not no skill: show a failure, add it as a task in `eval/tasks/<name>/` (`repo/`, `prompt.txt`, a hidden `check.py`), and paste the `make eval` summaries before and after. A change that adds words must beat the rule on something that matters. Tasks where Cave Pony loses are the most useful contribution.

## Credits

Built on ideas from Caveman and Ponytail. It is independently written and not endorsed by either project; see [NOTICE](NOTICE.md). The earlier 0.1 contract is at tag [`v0.1.1`](https://github.com/wilfgrainger/cave-pony/tree/v0.1.1). MIT licensed.
