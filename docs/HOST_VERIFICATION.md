# Host verification

Cave Pony separates install-path evidence from model-behaviour claims.

## Codex project installation

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

A one-off clean remote-install probe then exercised the public development command against `main`:

```bash
DISABLE_TELEMETRY=1 npx --yes skills@1.5.9 add \
  https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony \
  --agent codex \
  --copy \
  --yes
```

GitHub Actions pull-request run [#200](https://github.com/wilfgrainger/cave-pony/actions/runs/30134001186) passed `make test`, the checked-out Codex install, and `Verify public remote install command` at commit `f89628412f72e408474ddeed4d0de7429c57e9ce`. The temporary remote probe was then removed so ordinary CI does not perform a redundant second clone.

Every later merge or release candidate must rerun the recurring checks at its exact commit. These records do not transfer a green result to changed content.

## Claim boundary

The evidence proves that `skills@1.5.9` discovered and copied Cave Pony to the documented Codex project path in the tested GitHub-hosted Ubuntu environment, both from the checked-out directory and from the public `main` URL. It does not prove universal network reliability, other CLI versions, other operating systems, global installation, or that every Codex model invocation will activate, persist, switch levels, audit, stop, or obey the written contract.

Full Codex behaviour support requires a fresh authenticated Codex session to exercise:

1. explicit `/cave-pony` activation;
2. default `build=full voice=full` behaviour;
3. `lite` and `ultra` level switching;
4. independent build and voice controls;
5. `/cave-pony audit` remaining read-only;
6. destructive-operation clarity override;
7. `stop cave-pony` disabling Cave Pony only.

Until that evidence is committed, the repository claims verified Codex project-installation paths in the recorded environment, not complete Codex behavioural support.
