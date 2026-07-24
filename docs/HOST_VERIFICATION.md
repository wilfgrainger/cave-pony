# Host verification

Cave Pony separates install-path evidence from model-behaviour claims.

## Codex project installation

The CI workflow performs a clean project-scoped installation using:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@1.5.9 add \
  https://github.com/wilfgrainger/cave-pony/tree/<commit>/skills/cave-pony \
  --agent codex \
  --copy \
  --yes
```

The source is pinned to the exact commit under test. The CLI version is pinned to `1.5.9`. The check verifies that Codex receives `.agents/skills/cave-pony/SKILL.md`, that the installed frontmatter contains the expected name and version, and that the CLI lists the installed skill.

## Claim boundary

A successful installation smoke test proves repository discovery, copying, path selection, and installed metadata for the tested CLI and commit. It does not prove that every Codex model invocation will activate, persist, switch levels, audit, stop, or obey the written contract.

Full Codex behaviour support requires a fresh authenticated Codex session to exercise:

1. explicit `/cave-pony` activation;
2. default `build=full voice=full` behaviour;
3. `lite` and `ultra` level switching;
4. independent build and voice controls;
5. `/cave-pony audit` remaining read-only;
6. destructive-operation clarity override;
7. `stop cave-pony` disabling Cave Pony only.

Until that evidence is committed, the repository claims a verified Codex installation path, not complete Codex behavioural support.
