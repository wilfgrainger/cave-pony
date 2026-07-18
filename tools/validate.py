#!/usr/bin/env python3
"""Validate Cave Pony's repository and written behavioural contract."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"
README = ROOT / "README.md"

REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CONTRIBUTING.md",
    "skills/cave-pony/SKILL.md",
    "skills/cave-pony/README.md",
    "docs/DESIGN.md",
    "benchmarks/README.md",
    "benchmarks/manifest.json",
    "tools/validate.py",
    "tests/test_repository.py",
    "tests/behavioral_cases.json",
)

REQUIRED_SECTIONS = (
    "## Core contract",
    "## Activation and persistence",
    "## Execution loop",
    "## Build levels",
    "## Voice levels",
    "## Audit mode",
    "## Clarity override",
    "## Non-negotiable boundaries",
)

SOURCE_EXPECTATIONS = {
    "https://github.com/DietrichGebert/ponytail": "The best code is the code never written.",
    "https://github.com/JuliusBrussee/caveman": "All technical substance stay. Only fluff die.",
}

SAFETY_SENTENCES = (
    "Any command that deletes, overwrites, resets, force-pushes, drops, revokes, or rotates state triggers the override, however routine the request sounds.",
    "The override covers preconditions and recovery, not only the risky step.",
    "Ties between brevity and clarity always break toward clarity.",
)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        _, block, _ = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc

    values: dict[str, str] = {}
    active_key: str | None = None
    for raw_line in block.splitlines():
        if not raw_line.strip():
            continue
        if raw_line.startswith("  ") and active_key:
            values[active_key] = f"{values[active_key]} {raw_line.strip()}".strip()
            continue
        if ":" not in raw_line:
            raise ValueError(f"Unsupported frontmatter line: {raw_line!r}")
        key, value = raw_line.split(":", 1)
        active_key = key.strip()
        values[active_key] = value.strip().strip('"')
    return values


def validate_behavioral_cases(errors: list[str]) -> None:
    path = ROOT / "tests" / "behavioral_cases.json"
    if not path.is_file():
        return
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid behavioral_cases.json: {exc}")
        return

    expected = {"reset-hard": "resets", "rotate-key": "rotates", "delete-branches": "deletes"}
    found: dict[str, str] = {}
    for case in cases if isinstance(cases, list) else []:
        if not isinstance(case, dict):
            errors.append("behavioral case must be an object")
            continue
        case_id = case.get("id")
        trigger = case.get("trigger")
        requirements = case.get("required_contract")
        if not isinstance(case_id, str) or not isinstance(trigger, str):
            errors.append("behavioral case requires string id and trigger")
            continue
        found[case_id] = trigger
        if not isinstance(requirements, list) or len(requirements) < 2:
            errors.append(f"behavioral case {case_id!r} needs at least two contract requirements")
    if found != expected:
        errors.append(f"behavioral cases must equal {expected!r}; found {found!r}")


def validate_benchmark(errors: list[str], readme: str) -> None:
    manifest_path = ROOT / "benchmarks" / "manifest.json"
    if not manifest_path.is_file():
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid benchmark manifest: {exc}")
        return

    if manifest.get("status") != "not-run" and not list((ROOT / "benchmarks" / "results").glob("*.json")):
        errors.append("benchmark status may change from not-run only with committed JSON results")
    if len(manifest.get("tasks", [])) != 12:
        errors.append("benchmark manifest must preregister exactly 12 tasks")
    if manifest.get("arms") != ["baseline", "both-parents", "cave-pony", "yagni-control"]:
        errors.append("benchmark manifest arms do not match preregistration")
    if manifest.get("runs_per_cell") != 10:
        errors.append("benchmark manifest must use 10 runs per cell")

    results = list((ROOT / "benchmarks" / "results").glob("*.json"))
    comparative_claim = "## What is novel here" in readme
    if comparative_claim and not results:
        errors.append("README comparative claim requires committed benchmark results")
    if "not yet benchmarked" not in readme.lower():
        errors.append("README must disclose that the coordination design is not yet benchmarked")


def validate() -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if (ROOT / "tools" / "build.py").exists():
        errors.append("tools/build.py requires a named current consumer; remove it until then")

    if not SKILL.is_file():
        return errors

    skill_text = SKILL.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8") if README.is_file() else ""

    try:
        frontmatter = parse_frontmatter(skill_text)
    except ValueError as exc:
        errors.append(str(exc))
        frontmatter = {}

    for key, expected in {"name": "cave-pony", "license": "MIT"}.items():
        if frontmatter.get(key) != expected:
            errors.append(f"frontmatter {key!r} must equal {expected!r}")

    description = frontmatter.get("description", "")
    if "/cave-pony" not in description or "invokes" not in description:
        errors.append("frontmatter description must use explicit invocation language")
    if "Use for coding" in description:
        errors.append("frontmatter description must not auto-trigger on ordinary coding")
    if "Do not auto-load for ordinary coding requests" not in description:
        errors.append("frontmatter description must state the ordinary-coding exclusion")
    if "build=" not in frontmatter.get("argument-hint", ""):
        errors.append("argument-hint must expose independent build and voice controls")

    for section in REQUIRED_SECTIONS:
        if section not in skill_text:
            errors.append(f"SKILL.md missing section: {section}")

    for term in (
        "ACTIVE EVERY RESPONSE",
        "smallest decisive",
        "complexity toll",
        "root-cause",
        "Never claim a check passed unless it ran",
        "footprint report",
        "The target defaults to the most recent change or diff unless the user specifies another target.",
    ):
        if term.lower() not in skill_text.lower():
            errors.append(f"SKILL.md missing contract term: {term}")

    for sentence in SAFETY_SENTENCES:
        if sentence not in skill_text:
            errors.append(f"SKILL.md missing safety sentence: {sentence}")

    if "normal mode" in skill_text.lower():
        errors.append("SKILL.md must not claim the colliding normal mode command")
    if "hoofprint" in skill_text.lower():
        errors.append("use canonical term 'footprint report', not 'hoofprint'")

    if "## Coexistence" not in readme:
        errors.append("README missing Coexistence section")
    if "global `normal mode`" not in readme:
        errors.append("README must explain that no global normal mode is claimed")

    for url, quote in SOURCE_EXPECTATIONS.items():
        if url not in readme:
            errors.append(f"README missing source link: {url}")
        if quote not in readme:
            errors.append(f"README missing source quotation: {quote}")

    notices_path = ROOT / "THIRD_PARTY_NOTICES.md"
    notices = notices_path.read_text(encoding="utf-8") if notices_path.is_file() else ""
    for notice in ("© 2026 DietrichGebert", "© 2026 Julius Brussee"):
        if notice not in notices:
            errors.append(f"third-party notice missing: {notice}")

    validate_behavioral_cases(errors)
    validate_benchmark(errors, readme)

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".py", ".yml", ".yaml", ".json", ".txt"} and path.name not in {"Makefile", ".gitignore", "LICENSE"}:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if "\t" in text and path.name != "Makefile":
            errors.append(f"tab character found: {relative}")
        if any(line.endswith(" ") for line in text.splitlines()):
            errors.append(f"trailing whitespace found: {relative}")
        if text and not text.endswith("\n"):
            errors.append(f"missing final newline: {relative}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Cave Pony validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Cave Pony validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
