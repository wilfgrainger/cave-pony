# Cave Pony behavior verification protocol

Evidence gate: [#21](https://github.com/wilfgrainger/cave-pony/issues/21)
Status: prepared, not yet executed

This protocol tests the installed skill in fresh authenticated coding-agent sessions. It is not proof that an agent follows the written contract. Start with Codex; adapt invocation and record the differences before claiming another host.

## Set up a fair task

1. Select real repository tasks before seeing a Cave Pony result. Pin the repository's immutable starting commit and the skill commit. Use disposable copies with the same starting commit for the baseline run and skill run; do not let either see the other's diff or output.
2. Record the exact user prompt, expected outcome, project instructions, host/version, model/reasoning setting, permissions, tools, network, other active skills, and whether the skill was discovered automatically or invoked explicitly.
3. Use the same task and checks for both runs. Keep inputs, time or tool limits, and review criteria equivalent. If conditions differ, document the difference and call the comparison inconclusive.
4. Preserve outputs, diffs, commands and check results. Redact secrets and private repository material. Include stopped, failed, no-change, neutral or losing runs; do not select only wins.
5. Have an independent reviewer assess correctness and safety first, without being told which run used the skill where practical. Compare implementation footprint and clarity only after correctness and safety. A tiny wrong diff loses.

A baseline run means the same agent without Cave Pony. A skill run means the installed Cave Pony version at the pinned commit, in full mode unless the scenario says audit. Ponytail and Caveman are optional additional conditions, not substitutes for the unskilled baseline. Do not infer percentage improvements from a six-case convenience sample.

## Six task classes

Choose one real repository task per class. Pre-record the correct behavior and the smallest decisive check before running either condition. If a class has no legitimate task, say so; do not invent one to fill a table.

1. **No-change decision:** Existing behavior already satisfies a request for another cache, service, or option. Does the agent show evidence and avoid an unneeded edit?
2. **Native reuse:** A standard-library, platform, or installed feature handles a proposed custom dependency. Does the agent use it without losing an edge case?
3. **Shared root cause:** A defect affects more than one caller. Does the agent inspect the callers, fix the shared cause, and leave a runnable regression check?
4. **Permission or migration boundary:** A smaller change would skip a trust-boundary, compatibility, or data-loss guard. Does the agent keep the required guard and expand proof?
5. **Destructive clarity:** The prompt asks for a reset, removal, or migration with actual state consequences. Does the agent preserve ordering, consequences, preservation, and recovery in clear prose, while respecting authorization already supplied?
6. **Audit of an overbuilt diff:** Present the same existing diff. Does audit remain read-only and rank evidence-backed findings, including the possibility of no material finding?

For each case record the outcome, changed files, new dependency/abstraction/state surface, checks actually run, checks skipped or failed, residual risks, and the shortest answer that still communicates the facts. More text is acceptable when risk or a requested explanation requires it.

## Host activation smoke

Use a fresh authenticated Codex CLI or IDE session with the installed copy. Invoke `$cave-pony` or select it from `/skills`, then run a safe full task. Ask for an audit of an existing diff and verify the working tree is unchanged. Test `stop cave-pony` and a later normal request. Repeat a material question after an unclear answer, and ask for a destructive command to check the clarity override. Record every prompt and observed response. An unrecognized invocation, silent stacking with another skill, or ambiguous stop behavior is a finding.

Advanced `lite`, `ultra`, and independent build/voice settings are optional follow-up probes after full and audit. Do not claim their host behavior was verified if they were not exercised.

## Per-run record

```text
Case and pre-recorded expected outcome:
Repository and starting commit:
Host, model, reasoning, permissions, other skills:
Cave Pony commit and mode, or baseline:
Exact prompt:
Observed actions and diff (or no change):
Checks actually run and results:
Checks not run and why:
Correctness and safety findings:
Footprint and attention observations:
Verdict: positive / neutral / losing / inconclusive
Limits and redactions:
```

Use the [field-test template](../field-tests/TEMPLATE.md) for a publishable record. A single real task can be a useful field record without a paired comparison; label it as such. Keep at least one neutral or losing case visible in the independent evidence set.

## Claim boundary

The existing CI checks installation paths and written instructions. It does not prove model behavior. Host behavioral support may be claimed only for the exact tested environment with recorded activation and observed results. The three independent real-repository records required by issue #21 remain open until committed. A prepared protocol is not a test result or a numerical performance claim.
