# Host verification

Cave Pony separates installation-path evidence from model-behaviour claims.

## Recurring Codex project installation

The CI workflow checks out the exact pull-request head or push commit, then performs a clean project-scoped installation from that checked-out skill directory:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@1.5.9 add \
  "$GITHUB_WORKSPACE/skills/cave-pony" \
  --agent codex \
  --copy \
  --yes
```

The CLI version is pinned to `1.5.9`. The check verifies that Codex receives `.agents/skills/cave-pony/SKILL.md` and that the installed frontmatter contains the expected name and version. Using the checked-out path removes branch movement and remote-clone ambiguity from the recurring installation proof.

## Observed installation evidence

GitHub Actions pull-request run [#193](https://github.com/wilfgrainger/cave-pony/actions/runs/30133587016) completed successfully at commit `ed172c6a5bffcc9a540bda628d72e10f8a498995` on 2026-07-25. Both `make test` and `Verify clean Codex installation` passed.

A one-off clean remote-install probe exercised the public development command against `main`:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@1.5.9 add \
  https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony \
  --agent codex \
  --copy \
  --yes
```

GitHub Actions pull-request run [#200](https://github.com/wilfgrainger/cave-pony/actions/runs/30134001186) passed `make test`, the checked-out Codex install, and `Verify public remote install command` at commit `f89628412f72e408474ddeed4d0de7429c57e9ce`. The temporary remote probe was then removed so ordinary CI does not perform a redundant second clone.

A second one-off probe installed the same public URL into four documented project layouts in one clean GitHub-hosted Ubuntu workspace using `skills@1.5.9`, copy mode, and non-interactive confirmation:

| Host target | Verified installed path |
|---|---|
| Claude Code | `.claude/skills/cave-pony/SKILL.md` |
| Codex | `.agents/skills/cave-pony/SKILL.md` |
| Hermes Agent | `.hermes/skills/cave-pony/SKILL.md` |
| OpenClaw | `skills/cave-pony/SKILL.md` |

GitHub Actions pull-request run [#207](https://github.com/wilfgrainger/cave-pony/actions/runs/30134217101) passed `make test`, the recurring Codex installation, and `Verify documented host install paths` at commit `c1dacebae070c6a13324edbbc813b423b5edb6a2`. Each installed copy retained the expected `name: cave-pony` and `version: 0.1.0` frontmatter. The temporary cross-host probe was then removed from recurring CI.

## Observed lifecycle evidence

A third one-off Codex probe tested update, removal, and manual recovery in a clean temporary workspace:

1. install from the public development URL using copy mode;
2. back up the installed skill;
3. deliberately change the installed version marker to `9.9.9`;
4. run `skills update cave-pony --project --yes` and require restoration to `0.1.0`;
5. run `skills remove cave-pony --agent codex --yes` and require the installed path to disappear;
6. restore the backup and require valid `0.1.0` metadata.

GitHub Actions pull-request run [#216](https://github.com/wilfgrainger/cave-pony/actions/runs/30134550258) passed `make test`, the recurring Codex installation, and `Verify Codex update, removal, and recovery` at commit `9261819906d3f877037c5e37dcfa73422cdd4363`. The temporary lifecycle probe was then removed from recurring CI.

Every later merge or release candidate must rerun the recurring checks at its exact commit. These records do not transfer a green result to changed content.

## Claim boundary

The evidence proves that `skills@1.5.9` discovered, copied, updated, and removed Cave Pony in the recorded GitHub-hosted Ubuntu project runs, and that the documented manual backup restoration recovered a valid installed copy. It does not prove universal network reliability, other CLI versions, other operating systems, global installation, host discovery after restart, every possible failed-upgrade state, or model behaviour.

Full Codex behaviour support still requires a fresh authenticated Codex session. A host is not claimed as behaviourally supported until a fresh authenticated session exercises its actual discovery and activation model, level switching, audit mode, destructive-operation clarity, repeated-question clarity, and stop behaviour. Installation layout alone is not behavioural support.

Codex behavioural verification is part of the independent evidence gate in [issue #21](https://github.com/wilfgrainger/cave-pony/issues/21). Equivalent behaviour evidence remains required before making Claude Code, Hermes Agent, or OpenClaw behavioural-support claims.
