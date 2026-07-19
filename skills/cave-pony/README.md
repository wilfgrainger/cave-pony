# Cave Pony skill

Cave Pony `0.1.0` builds like Ponytail and speaks like Caveman. It activates after explicit invocation or, within coding or agent work, a clear request for minimalism, terse output, relief from bloat, or an audit. Generic brevity requests outside that context do not activate it.

## Install

```bash
npx skills add https://github.com/wilfgrainger/cave-pony/tree/main/skills/cave-pony
```

This tracks `main` until an immutable tag and GitHub Release exist. Or copy this directory into an Agent Skills-compatible skills folder.

## Commands

```text
/cave-pony                         # build=full voice=full
/cave-pony lite                    # both axes lite
/cave-pony ultra                   # both axes ultra
/cave-pony build=ultra voice=lite  # independent controls
/cave-pony audit                   # read-only review
stop cave-pony                     # disable Cave Pony only
```

Do not stack it with Ponytail and Caveman unless overlapping instructions and context overhead are intentional.

## Contract

The agent reads the complete affected path, climbs the no-change/reuse/stdlib/native/installed/local-code ladder, fixes the shared root cause, leaves one runnable check for non-trivial logic, and reports only useful result, proof, skipped surface, and risk.

Voice removes filler, hedging, self-reference, and routine narration. Full voice may use fragments and drop articles where meaning stays obvious. Exact code, commands, identifiers, errors, language, commits, PR bodies, and documentation remain intact or use normal grammar.

Compression stops for destructive, security-sensitive, and order-dependent content. Preconditions, consequences, preservation, and recovery stay explicit.

See the repository [README](../../README.md), [design notes](../../docs/DESIGN.md), [field record](../../field-tests/2026-07-19-gov-metrics-publication-diagnostics.md), and [third-party notices](../../THIRD_PARTY_NOTICES.md).
