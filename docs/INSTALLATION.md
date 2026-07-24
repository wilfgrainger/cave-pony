# Installation, upgrade, and removal

Cave Pony is one skill directory containing Markdown. It has no executable installer of its own, no runtime package, and no network access.

## Development install

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

This follows moving `main` and is appropriate for evaluation, not an immutable production pin. Clean GitHub-hosted Ubuntu runs verified this public URL with `skills@1.5.9`, copy mode, and non-interactive confirmation for the project layouts below:

| Host target | Installed project path |
|---|---|
| Claude Code | `.claude/skills/cave-pony/SKILL.md` |
| Codex | `.agents/skills/cave-pony/SKILL.md` |
| Hermes Agent | `.hermes/skills/cave-pony/SKILL.md` |
| OpenClaw | `skills/cave-pony/SKILL.md` |

See [Host verification](HOST_VERIFICATION.md) for exact runs and limitations. Installation layout evidence does not establish host discovery or model behaviour.

## Recurring Codex project-install check

CI checks out the exact pull-request head or push commit, then verifies a clean, non-interactive, project-scoped Codex installation with the `skills` CLI pinned to `1.5.9`:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@1.5.9 add \
  "$GITHUB_WORKSPACE/skills/cave-pony" \
  --agent codex \
  --copy \
  --yes
```

The check verifies `.agents/skills/cave-pony/SKILL.md` and the expected frontmatter. The local checked-out source keeps routine CI independent of a second remote clone while the one-off public URL and cross-host evidence remain recorded.

## Generic manual install

```bash
git clone https://github.com/wilfgrainger/cave-pony.git
cp -R cave-pony/skills/cave-pony /path/to/your/agent/skills/
```

Restart or reload the host if it caches skill discovery.

## Verify

Confirm that the installed directory contains `SKILL.md` with:

```yaml
name: cave-pony
version: 0.1.0
license: MIT
```

Then start a fresh session, invoke `/cave-pony audit`, and confirm the host loads the skill without silently stacking another minimalism or terse-output skill.

## Upgrade

1. Back up the installed `cave-pony` directory.
2. Replace it with the newer directory or rerun the host's supported installer.
3. Confirm the frontmatter version.
4. Start a fresh session and repeat the audit smoke check.
5. Restore the backup if discovery or activation regresses.

## Remove

1. End active sessions using Cave Pony.
2. Remove the installed `cave-pony` directory through the host's supported skill manager or filesystem.
3. Remove any host configuration that explicitly activates Cave Pony.
4. Restart or reload the host.
5. Start a fresh session and confirm `/cave-pony` is no longer available.

Deleting the skill directory does not revert code changes previously made while the skill was active.

## Recovery

If an upgrade or removal fails:

- restore the backed-up directory;
- restore the previous host configuration;
- restart the host;
- verify from a fresh session.

## Support claims

A compatible Markdown layout is not proof of host support. The repository claims verified project-installation layouts only for the recorded `skills@1.5.9` GitHub-hosted Ubuntu runs. Claude Code, Codex, Hermes Agent, and OpenClaw behavioural support remains unclaimed until each host's actual discovery, activation, level switching, audit, clarity override, and stop behaviour is exercised in a fresh authenticated session and committed as evidence.
