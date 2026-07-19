#!/usr/bin/env python3
"""Validate Cave Pony's durable repository contract."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/cave-pony/SKILL.md"
README = ROOT / "README.md"
CI = ROOT / ".github/workflows/ci.yml"

FILES = (
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "skills/cave-pony/SKILL.md",
    "skills/cave-pony/README.md",
    "docs/DESIGN.md",
    "tools/validate.py",
    "tests/test_repository.py",
    "tests/behavioral_cases.json",
    "field-tests/2026-07-19-gov-metrics-publication-diagnostics.md",
)

SECTIONS = (
    "## Core contract",
    "## Activation and persistence",
    "## Execution loop",
    "## Build levels",
    "## Voice levels",
    "## Audit mode",
    "## Clarity override",
    "## Non-negotiable boundaries",
)

ROOT_TERMS = (
    "Build like Ponytail. Speak like Caveman.",
    "Climb the footprint ladder",
    "standard library",
    "native browser",
    "already-installed dependency",
    "Deletion over addition",
    "Fewest files possible",
    "Fix the root once",
    "one runnable check",
    "drop articles where meaning stays obvious",
    "Do not invent prose abbreviations",
    "normal grammar",
    "Ties between brevity and clarity always break toward clarity",
)

PINS = {
    "actions/checkout": "11bd71901bbe5b1630ceea73d27597364c9af683",
    "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
}


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with frontmatter")
    _, block, _ = text.split("---\n", 2)
    values: dict[str, str] = {}
    active = ""
    for line in block.splitlines():
        if line.startswith("  ") and active:
            values[active] += " " + line.strip()
        elif ":" in line:
            active, value = line.split(":", 1)
            active = active.strip()
            values[active] = value.strip().strip('"')
    return values


def validate_cases(errors: list[str], skill: str) -> None:
    path = ROOT / "tests/behavioral_cases.json"
    if not path.is_file():
        return
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid behavioral cases: {exc}")
        return
    required = {"reset-hard": "resets", "rotate-key": "rotates", "delete-branches": "deletes"}
    found: dict[str, str] = {}
    for case in cases if isinstance(cases, list) else []:
        if not isinstance(case, dict):
            errors.append("behavioral case must be an object")
            continue
        case_id = case.get("id")
        trigger = case.get("trigger")
        prompt = case.get("prompt")
        rules = case.get("required_contract")
        if not all(isinstance(value, str) and value.strip() for value in (case_id, trigger, prompt)):
            errors.append("behavioral case requires id, trigger, and prompt")
            continue
        found[case_id] = trigger
        if trigger not in skill:
            errors.append(f"behavioral trigger missing from skill: {trigger}")
        if not isinstance(rules, list) or len(rules) < 2:
            errors.append(f"behavioral case needs two rules: {case_id}")
    for case_id, trigger in required.items():
        if found.get(case_id) != trigger:
            errors.append(f"required behavioral case missing: {case_id}")


def validate() -> list[str]:
    errors: list[str] = []
    for relative in FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing file: {relative}")
    if not SKILL.is_file():
        return errors

    skill = SKILL.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    try:
        meta = frontmatter(skill)
    except ValueError as exc:
        errors.append(str(exc))
        meta = {}

    if meta.get("name") != "cave-pony" or meta.get("license") != "MIT":
        errors.append("frontmatter name and licence must be stable")
    if not re.fullmatch(r"\d+\.\d+\.\d+", meta.get("version", "")):
        errors.append("frontmatter version must be semantic")
    description = meta.get("description", "")
    if "/cave-pony" not in description or "coding or agent-work" not in description:
        errors.append("activation must remain explicit and coding-scoped")

    for text in SECTIONS + ROOT_TERMS:
        if text.lower() not in skill.lower():
            errors.append(f"skill missing root contract: {text}")
    steps = re.findall(r"^###\s+(\d+)\.", skill, re.MULTILINE)
    if steps != ["1", "2", "3", "4", "5"]:
        errors.append("execution loop must contain exactly five steps")
    for number in range(1, 6):
        if not re.search(rf"^{number}\.\s+", readme, re.MULTILINE):
            errors.append(f"README missing behaviour step {number}")

    active_docs = readme + (ROOT / "docs/DESIGN.md").read_text(encoding="utf-8") + (ROOT / "skills/cave-pony/README.md").read_text(encoding="utf-8")
    if "benchmark" in active_docs.lower():
        errors.append("active documentation contains removed research roadmap")
    for url in ("https://github.com/DietrichGebert/ponytail", "https://github.com/JuliusBrussee/caveman"):
        if url not in readme:
            errors.append(f"README missing parent attribution: {url}")

    workflow = CI.read_text(encoding="utf-8") if CI.is_file() else ""
    if workflow.count("branches: [main]") != 2 or "cancel-in-progress: true" not in workflow:
        errors.append("CI must be main-scoped and cancel superseded runs")
    for action, commit in PINS.items():
        if f"{action}@{commit}" not in workflow:
            errors.append(f"CI action must use immutable commit: {action}")

    validate_cases(errors, skill)
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".py", ".yml", ".yaml", ".json", ".txt"} and path.name not in {"Makefile", ".gitignore", "LICENSE"}:
            continue
        text = path.read_text(encoding="utf-8")
        if any(line.endswith(" ") for line in text.splitlines()):
            errors.append(f"trailing whitespace: {path.relative_to(ROOT)}")
        if text and not text.endswith("\n"):
            errors.append(f"missing final newline: {path.relative_to(ROOT)}")
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
