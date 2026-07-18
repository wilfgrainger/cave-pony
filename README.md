# Cave Pony

**Do less. Say less. Prove enough.**

Cave Pony is an open-source coding-agent skill combining two excellent ideas:

- [Ponytail](https://github.com/DietrichGebert/ponytail) reduces unnecessary implementation.
- [Caveman](https://github.com/JuliusBrussee/caveman) reduces unnecessary prose.
- Cave Pony coordinates both and requires risk-proportionate proof.

> “The best code is the code never written.” — [Ponytail `SKILL.md`](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md)
>
> “All technical substance stay. Only fluff die.” — [Caveman `SKILL.md`](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md)

This is an independently authored combination, not an official successor to either project and not endorsed by their maintainers. Both source projects are MIT licensed; see [Third-party notices](THIRD_PARTY_NOTICES.md).

## Coordination design — not yet benchmarked

Cave Pony defines what happens when implementation minimalism and terse communication conflict:

- separate `build` and `voice` budgets;
- a complexity toll for new owned surface;
- root-cause fixes instead of repeated symptom patches;
- the smallest decisive proof appropriate to the risk;
- an explicit clarity override for risky work;
- read-only audit mode.

These are design claims, not performance results. Cave Pony has **not yet been shown to outperform installing Ponytail and Caveman side by side**. Until the preregistered benchmark in [`benchmarks/`](benchmarks/) is run and published, treat Cave Pony as a convenience and coordination experiment, not a proven improvement.

### Context overhead

The skill text is loaded into model context when activated. Its exact token cost depends on the host and tokenizer; the current file is roughly in the high-one-thousands of input tokens. This overhead can be net-negative for small or already-terse tasks. Cave Pony therefore uses explicit activation rather than loading for every coding request.

## Coexistence

Cave Pony is intended to replace Ponytail and Caveman, not stack with them. Installing all three creates overlapping instructions and extra context cost. If all are present, Cave Pony's rules apply only while Cave Pony is active. `stop cave-pony` disables only Cave Pony; use each parent skill's own stop command for that skill. Cave Pony deliberately does not claim a global `normal mode` command.

## Behaviour

1. Understand the affected flow and trust boundaries.
2. Prefer no change, deletion, reuse, standard library, native features, or installed dependencies before new owned code.
3. Require a present need and rejected simpler alternative for every new durable surface.
4. Fix the narrowest shared root cause.
5. Run the smallest meaningful proof and expand it with risk.
6. For changes, report Done, Proof, Skipped, and Risk. For questions, answer directly.

## Install

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

Manual installation:

```bash
git clone https://github.com/wilfgrainger/cave-pony.git
cp -R cave-pony/skills/cave-pony /path/to/your/agent/skills/
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
| `build` | Build requested scope and identify a smaller option | Enforce footprint gate and complexity toll | Challenge speculative scope; prefer deletion or no change |
| `voice` | Tight full sentences | Short direct response | Minimum unambiguous words, except where clarity override applies |

## Safety under compression

Any command that deletes, overwrites, resets, force-pushes, drops, revokes, or rotates state must trigger explicit prose. Preconditions, ordering, consequences, and recovery stay visible. Three adversarial contract probes are committed in [`tests/behavioral_cases.json`](tests/behavioral_cases.json).

These static probes verify the written contract, not model compliance. Real compliance belongs in the comparative agent benchmark.

## Example

Request: “Add a retry framework for one HTTP call.”

A Cave Pony agent checks the existing client, failure semantics, and idempotency. If the client already supports retries, it configures that. Otherwise it may add one bounded local retry around the safe call and one regression test.

Footprint report:

```text
Done: Used the existing retry policy for the idempotent GET.
Proof: Retry-limit test passes; existing suite passes.
Skipped: New dependency and wrapper hierarchy; no current need.
Risk: POST calls remain non-retrying by design.
```

## Development and testing

No runtime package or third-party development dependency is required.

```bash
make validate
make test
```

CI runs the same checks. Static tests validate the skill contract and adversarial cases; they do not prove that every host model will obey the skill. See [Design and implementation](docs/DESIGN.md).

## Repository layout

```text
skills/cave-pony/SKILL.md    Agent-facing behaviour
skills/cave-pony/README.md   Install and command reference
tools/validate.py            Static contract validation
tests/                       Repository and adversarial contract tests
benchmarks/                  Preregistered comparative benchmark
docs/DESIGN.md               Design and implementation details
```

## Licence

Cave Pony is released under the [MIT License](LICENSE). Attribution for Ponytail and Caveman is preserved in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
