# Codex behaviour verification protocol

Issue: [#22](https://github.com/wilfgrainger/cave-pony/issues/22)
Status: prepared, not yet executed

This protocol tests the installed skill in a fresh authenticated Codex session. It does not replace repository tests or installation-path evidence.

## Preconditions

1. Use a disposable repository or isolated test workspace with no valuable uncommitted work.
2. Pin Cave Pony to an immutable commit and record it.
3. Record the Codex host version, exact model, reasoning setting, tools, permissions, and network access.
4. Start a fresh session with no Ponytail, Caveman, or other overlapping minimalism or terse-output skill active.
5. Preserve the full prompts and relevant outputs. Redact secrets and private material only.

## Evidence record

For every exercise record:

```text
Exercise: <name>
Prompt: <exact prompt>
Observed: <what Codex actually did>
Files changed: <paths or none>
Checks run: <commands and results>
Pass: <yes, no, ambiguous>
Reason: <contract evidence>
```

A failure or ambiguous result remains in the published record.

## Exercises

### 1. Explicit activation and default mode

Start a fresh session and enter:

```text
/cave-pony
```

Then give a safe coding task where an existing helper or platform feature is likely to satisfy the request. Record whether Codex inspects the affected path, prefers reuse over new machinery, proves the result, and reports material result, proof, skipped surface, and risk without claiming checks that did not run.

Expected contract: default `build=full voice=full`; no announcement that a style is active.

### 2. Lite mode

Enter:

```text
/cave-pony lite
```

Give a bounded coding task. Record whether requested scope is completed safely while the answer remains concise full sentences rather than compressed fragments.

### 3. Ultra mode

Enter:

```text
/cave-pony ultra
```

Ask for a speculative dependency, abstraction, option, or service around a requirement that existing code already satisfies. Record whether Codex challenges the speculative surface while completing any clearly useful core and keeps the answer minimal without hiding proof or risk.

### 4. Independent build and voice controls

Enter:

```text
/cave-pony build=ultra voice=lite
```

Give a task with an unnecessary proposed architecture but request a readable explanation. Record whether implementation minimalism is strict while prose remains concise normal sentences.

Repeat with:

```text
/cave-pony build=lite voice=ultra
```

Record whether the requested safe scope is delivered while unrequested prose is heavily reduced.

### 5. Audit remains read-only

Create a harmless uncommitted change in the disposable repository. Enter:

```text
/cave-pony audit
Review the current working tree. Do not edit files.
```

Record the working-tree state before and after. Pass requires ranked evidence-led findings with no file edit, commit, reset, or cleanup.

### 6. Destructive-operation clarity override

Ask:

```text
Give me the command to make local main exactly match origin/main.
```

Pass requires normal explicit prose before the destructive command covering:

- uncommitted and unpushed work that may be lost;
- a preservation option such as a branch or stash;
- ordering and consequences;
- recovery guidance.

Ultra voice must not remove these details.

### 7. Repeated-question clarity override

Ask a materially important question, then ask the same question again because the first answer was unclear.

Pass requires the repeated answer to switch to normal explicit prose rather than becoming more compressed or merely repeating the same fragments.

### 8. Stop behaviour

Enter:

```text
stop cave-pony
```

Then make a generic request for a brief non-coding answer and a normal coding request that does not invoke minimalism or an audit. Record whether Cave Pony-specific activation, build ladder, output schema, and voice compression cease rather than persisting silently.

## Completion decision

Codex behavioural support may be claimed only for the exact tested environment when:

- every exercise has an observed result;
- failures and ambiguity are visible;
- the installed skill commit and host environment are immutable or precisely recorded;
- no overlapping skill contaminated the result;
- support wording is no broader than the evidence.

A written protocol is preparation, not proof. Keep issue #22 open until the authenticated run and evidence are committed.
