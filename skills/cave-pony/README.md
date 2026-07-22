# Cave Pony skill

Cave Pony `0.1.0` is a standalone coding-agent skill for the smallest trustworthy change: less implementation, less narration, and proof proportional to risk.

## Install

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

The development command tracks `main`. See the repository [installation guide](../../docs/INSTALLATION.md) for manual installation, upgrade, removal, recovery, and support status.

## Commands

```text
/cave-pony                         # build=full voice=full
/cave-pony lite                    # both axes lite
/cave-pony ultra                   # both axes ultra
/cave-pony build=ultra voice=lite  # independent controls
/cave-pony audit                   # read-only review
stop cave-pony                     # disable Cave Pony only
```

Cave Pony is intended to be activated instead of Ponytail and Caveman in the same session. It cannot unload another host-managed skill; disable overlapping skills through the host when needed.

## Contract

The agent reads the complete affected path, climbs the no-change/reuse/stdlib/native/installed/local-code ladder, fixes the shared root cause, leaves one runnable check for non-trivial logic, and reports only useful result, proof, skipped surface, and risk.

Voice removes filler, hedging, self-reference, and routine narration. Full voice may use fragments and drop articles where meaning stays obvious. Exact code, commands, identifiers, errors, language, commits, PR bodies, and documentation remain intact or use normal grammar.

Compression stops for destructive, security-sensitive, and order-dependent content. Preconditions, consequences, preservation, and recovery stay explicit.

See the repository [README](../../README.md), [design notes](../../docs/DESIGN.md), [origins and differences](../../docs/ORIGINS_AND_DIFFERENCES.md), [FAQ](../../docs/FAQ.md), [launch checklist](../../docs/LAUNCH_CHECKLIST.md), [field record](../../field-tests/2026-07-19-gov-metrics-publication-diagnostics.md), and [third-party notices](../../THIRD_PARTY_NOTICES.md).
