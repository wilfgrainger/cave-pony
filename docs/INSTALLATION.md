# Installation, upgrade, and removal

Cave Pony is one skill directory containing Markdown. It has no executable installer of its own, no runtime package, and no network access.

## Development install

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

This follows moving `main` and is appropriate for evaluation, not an immutable production pin.

## Verified Codex project install

CI checks out the exact pull-request head or push commit, then verifies a clean, non-interactive, project-scoped Codex installation with the `skills` CLI pinned to `1.5.9`:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@1.5.9 add \
  "$GITHUB_WORKSPACE/skills/cave-pony" \
  --agent codex \
  --copy \
  --yes
```

The check verifies `.agents/skills/cave-pony/SKILL.md` and the expected frontmatter. See [Host verification](HOST_VERIFICATION.md) for the evidence boundary. The public development URL above remains a moving evaluation path until its own clean remote-install result is committed.

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

A compatible Markdown layout is not proof of host support. The repository currently claims a CI-verified Codex project-installation mechanism only. Full Codex behavioural support remains unclaimed until activation, persistence, level switching, audit mode, destructive-operation clarity, and stop behaviour are exercised in an authenticated fresh session and committed as evidence. Claude Code, Hermes, OpenClaw, and other hosts remain unclaimed until equivalent evidence exists.
