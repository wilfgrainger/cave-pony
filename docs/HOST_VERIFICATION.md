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

The CLI version is pinned to `1.5.9`. The check verifies that Codex receives `.agents/skills/cave-pony/SKILL.md` and that the installed frontmatter contains the expected name and version. Using the checked-out path removes branch movement and remote-clone ambiguity from the installation proof.

## Observed evidence

GitHub Actions pull-request run [#193](https://github.com/wilfgrainger/cave-pony/actions/runs/30133587016) completed successfully at commit `ed172c6a5bffcc9a540bda628d72e10f8a498995` on 2026-07-25. Both `make test` and `Verify clean Codex installation` passed.

Every later merge or release candidate must rerun the same checks at its exact commit. This record does not transfer a green result to changed content.

## Claim boundary

A successful installation smoke test proves local skill discovery, copying, Codex path selection, and installed metadata for the tested CLI and commit. It does not prove that the public remote URL resolves in every environment or that every Codex model invocation will activate, persist, switch levels, audit, stop, or obey the written contract.

Full Codex behaviour support requires a fresh authenticated Codex session to exercise:

1. explicit `/cave-pony` activation;
2. default `build=full voice=full` behaviour;
3. `lite` and `ultra` level switching;
4. independent build and voice controls;
5. `/cave-pony audit` remaining read-only;
6. destructive-operation clarity override;
7. `stop cave-pony` disabling Cave Pony only.

Until that evidence is committed, the repository claims a verified Codex project-installation mechanism, not complete Codex behavioural support or universal remote-install reliability.
