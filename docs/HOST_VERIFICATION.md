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

## Observed evidence

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

Every later merge or release candidate must rerun the recurring checks at its exact commit. These records do not transfer a green result to changed content.

## Claim boundary

The evidence proves that `skills@1.5.9` discovered and copied Cave Pony into the listed project directories in the recorded GitHub-hosted Ubuntu runs. It does not prove universal network reliability, other CLI versions, other operating systems, global installation, host discovery after restart, or model behaviour.

A host is not claimed as behaviourally supported until a fresh authenticated session exercises its actual discovery and activation model, level switching, audit mode, destructive-operation clarity, repeated-question clarity, and stop behaviour. Installation layout alone is not behavioural support.

Codex behavioural verification is tracked in [issue #22](https://github.com/wilfgrainger/cave-pony/issues/22). Equivalent behaviour evidence remains required before making Claude Code, Hermes Agent, or OpenClaw behavioural-support claims.
