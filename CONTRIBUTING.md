# Contributing

Cave Pony is one small file. Keep it that way.

A change to `skills/cave-pony/SKILL.md` needs evidence, not taste:

1. Show the failure: a prompt, what the agent did, what it should have done.
2. If it fits, add it as an eval task in `eval/tasks/<name>/` (`repo/`, `prompt.txt`, `check.py`).
3. Run `make eval` before and after your change and paste both summary tables in the PR.

A change that adds words must win on the eval. A change that removes words only has to not lose. `make test` enforces the word budget.

New eval tasks are the most useful contribution, especially ones where Cave Pony loses.
