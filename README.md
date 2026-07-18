# Cave Pony

**Do less. Say less. Prove enough.**

Cave Pony is an open-source coding-agent skill that combines two excellent ideas:

- [Ponytail](https://github.com/DietrichGebert/ponytail) reduces the amount of code an agent creates.
- [Caveman](https://github.com/JuliusBrussee/caveman) reduces the amount of prose an agent emits.
- Cave Pony coordinates both, then requires the smallest decisive proof that the change works.

> “The best code is the code never written.” — [Ponytail `SKILL.md`](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md)
>
> “All technical substance stay. Only fluff die.” — [Caveman `SKILL.md`](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md)

This project is a respectful combination inspired by both skills because each solves a different half of the same problem. It is independently authored, is not an official successor to either project, and is not endorsed by their maintainers. Both source projects are MIT licensed; see [Third-party notices](THIRD_PARTY_NOTICES.md).

## What is novel here

Installing two skills side by side does not define what happens when brevity conflicts with correctness. Cave Pony adds a coordination layer:

- **Two budgets:** implementation footprint and reader attention are controlled independently.
- **Complexity toll:** every new dependency, abstraction, file, config option, or persistent state must pay for itself with a present requirement.
- **Smallest decisive proof:** non-trivial work leaves one runnable check that would fail if the change broke.
- **Root-cause bias:** fix the shared cause instead of applying repeated symptom patches.
- **Clarity override:** terse output switches off for security, destructive operations, migrations, legal risk, or any sequence where compressed grammar could change meaning.
- **Audit mode:** review an existing change for avoidable code and avoidable narration without modifying it.

## The Cave Pony loop

1. **Understand deeply.** Read the task, affected code, callers, tests, and trust boundaries before choosing a small solution.
2. **Pass the footprint gate.** Prefer no change, deletion, reuse, standard library, native platform, or an installed dependency before new code.
3. **Charge the complexity toll.** Reject new owned surface that lacks a concrete current need.
4. **Fix once.** Put the correction at the narrowest shared root cause.
5. **Prove enough.** Run the smallest meaningful check; add one small test for non-trivial new logic.
6. **Report tightly.** State what changed, proof, deliberate omissions, and material risk. Nothing else.

## Install

For tools that support the community skills installer:

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

Manual installation:

```bash
git clone https://github.com/wilfgrainger/cave-pony.git
cp -R cave-pony/skills/cave-pony /path/to/your/agent/skills/
```

The distributable archive can also be built locally:

```bash
make build
# dist/cave-pony.skill
```

## Use

```text
/cave-pony
/cave-pony lite
/cave-pony ultra
/cave-pony build=ultra voice=lite
/cave-pony audit
stop cave-pony
```

A single level sets both axes. Advanced users can tune them independently:

| Axis | `lite` | `full` (default) | `ultra` |
|---|---|---|---|
| `build` | Build requested scope, identify a smaller option | Enforce footprint gate and complexity toll | Challenge speculative scope; prefer deletion or no change |
| `voice` | Tight full sentences | Short, direct report | Minimum unambiguous words |

## Example

Request: “Add a retry framework for one HTTP call.”

A Cave Pony agent first checks the runtime, codebase, installed dependencies, failure semantics, and idempotency. If the existing client already supports retries, it configures that. Otherwise it may add a bounded local retry around the one safe call, plus one test proving the retry limit.

Expected report:

```text
Done: Used existing client retry policy for the idempotent GET.
Proof: Retry-limit test passes; existing suite passes.
Skipped: New retry dependency and wrapper hierarchy; no current need.
Risk: POST calls remain non-retrying by design.
```

## Development and testing

No runtime package is required. Validation and packaging use only the Python standard library.

```bash
make test      # repository and behavioural-contract tests
make build     # validated, deterministic .skill archive
make validate  # fast static contract check
```

CI runs the same test and build commands. See [Design and implementation](docs/DESIGN.md) for the behavioural model, packaging contract, and extension rules.

## Repository layout

```text
skills/cave-pony/SKILL.md   Agent-facing behaviour
skills/cave-pony/README.md  Install and command reference
tools/validate.py           Static contract validation
tools/build.py              Deterministic skill packaging
tests/                      Repository contract tests
docs/DESIGN.md              Design and implementation details
```

## Licence

Cave Pony is released under the [MIT License](LICENSE). Attribution for Ponytail and Caveman is preserved in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
