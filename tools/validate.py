#!/usr/bin/env python3
"""Validate Cave Pony's durable standalone repository contract."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/cave-pony/SKILL.md"
README = ROOT / "README.md"
NESTED_README = ROOT / "skills/cave-pony/README.md"
LAUNCH = ROOT / "docs/LAUNCH_CHECKLIST.md"
CI = ROOT / ".github/workflows/ci.yml"
LOGO = ROOT / "assets/cave-pony-logo.png"

FILES = (
    ".github/workflows/ci.yml",
    ".gitignore",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "assets/cave-pony-logo.png",
    "assets/cave-pony-social-preview.png",
    "docs/BENCHMARK_PLAN.md",
    "docs/DESIGN.md",
    "docs/EXAMPLES.md",
    "docs/FAQ.md",
    "docs/GITHUB_METADATA.md",
    "docs/INSTALLATION.md",
    "docs/LAUNCH_CHECKLIST.md",
    "docs/ORIGINS_AND_DIFFERENCES.md",
    "field-tests/2026-07-19-gov-metrics-publication-diagnostics.md",
    "licenses/caveman-MIT.txt",
    "licenses/ponytail-MIT.txt",
    "skills/cave-pony/README.md",
    "skills/cave-pony/SKILL.md",
    "tests/behavioral_cases.json",
    "tests/test_repository.py",
    "tools/validate.py",
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

SAFETY_TERMS = (
    "trust-boundary validation",
    "authentication or authorisation",
    "safe secrets handling",
    "error handling needed to prevent corruption or data loss",
    "accessibility",
    "legal or operational obligations",
    "existing compatibility guarantees",
)

FORBIDDEN_STANDALONE_TERMS = (
    "silicon" + " valley",
    "silicon-valley" + "-dev-team",
    "gilfoyle" + " persona",
)

PINS = {
    "actions/checkout": "11bd71901bbe5b1630ceea73d27597364c9af683",
    "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
}

REQUIRED_CASES = {
    "reset-hard",
    "rotate-key",
    "delete-branches",
    "authorization-boundary",
    "secret-handling",
    "data-loss",
    "accessibility",
    "repeated-question",
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


def text_files() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix in {".md", ".py", ".yml", ".yaml", ".json", ".txt"}:
            result.append(path)
        elif path.name in {"Makefile", ".gitignore", "LICENSE"}:
            result.append(path)
    return result


def validate_cases(errors: list[str], skill: str) -> None:
    path = ROOT / "tests/behavioral_cases.json"
    if not path.is_file():
        return
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid behavioral cases: {exc}")
        return
    if not isinstance(cases, list):
        errors.append("behavioral cases must be a list")
        return

    found: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("behavioral case must be an object")
            continue
        case_id = case.get("id")
        trigger = case.get("trigger")
        prompt = case.get("prompt")
        rules = case.get("required_contract")
        terms = case.get("contract_terms")
        if not all(isinstance(value, str) and value.strip() for value in (case_id, trigger, prompt)):
            errors.append("behavioral case requires id, trigger, and prompt")
            continue
        if case_id in found:
            errors.append(f"duplicate behavioral case id: {case_id}")
        found.add(case_id)
        if trigger.lower() not in skill.lower():
            errors.append(f"behavioral trigger missing from skill: {trigger}")
        if not isinstance(rules, list) or len(rules) < 2 or not all(isinstance(rule, str) and rule.strip() for rule in rules):
            errors.append(f"behavioral case needs two written rules: {case_id}")
        if not isinstance(terms, list) or not terms or not all(isinstance(term, str) and term.strip() for term in terms):
            errors.append(f"behavioral case needs contract terms: {case_id}")
            continue
        for term in terms:
            if term.lower() not in skill.lower():
                errors.append(f"behavioral contract term missing for {case_id}: {term}")

    for case_id in sorted(REQUIRED_CASES - found):
        errors.append(f"required behavioral case missing: {case_id}")


def validate_versions(errors: list[str], version: str) -> None:
    if not version:
        return
    checks = {
        "README version badge": (README, f"version-{version}-blue.svg"),
        "README development version": (README, f"Current development version: `{version}`."),
        "nested README version": (NESTED_README, f"Cave Pony `{version}`"),
        "launch status version": (LAUNCH, f"Current state: pre-release `{version}`"),
    }
    for label, (path, expected) in checks.items():
        if not path.is_file() or expected not in path.read_text(encoding="utf-8"):
            errors.append(f"version drift: {label} must match {version}")


def validate_ci(errors: list[str]) -> None:
    workflow = CI.read_text(encoding="utf-8") if CI.is_file() else ""
    if workflow.count("branches: [main]") != 2 or "cancel-in-progress: true" not in workflow:
        errors.append("CI must be main-scoped and cancel superseded runs")
    if not re.search(r"(?m)^permissions:\n  contents: read\n", workflow):
        errors.append("CI permissions must be repository read-only")
    if re.search(r"(?m)^\s+[\w-]+:\s+write\s*$", workflow):
        errors.append("CI must not grant write permissions")
    if workflow.count("runs-on:") != 1 or "matrix:" in workflow:
        errors.append("CI must contain one job without a matrix")
    if 'python-version: "3.12"' not in workflow or workflow.count("python-version:") != 1:
        errors.append("CI must use Python 3.12 once")
    if workflow.count("- run: make test") != 1:
        errors.append("CI must run the repository test target once")
    for action, commit in PINS.items():
        if f"{action}@{commit}" not in workflow:
            errors.append(f"CI action must use immutable commit: {action}")


def validate() -> list[str]:
    errors: list[str] = []
    for relative in FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing file: {relative}")
    if not SKILL.is_file():
        return errors

    skill = SKILL.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8") if README.is_file() else ""
    try:
        meta = frontmatter(skill)
    except ValueError as exc:
        errors.append(str(exc))
        meta = {}

    if meta.get("name") != "cave-pony" or meta.get("license") != "MIT":
        errors.append("frontmatter name and licence must be stable")
    version = meta.get("version", "")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("frontmatter version must be semantic")
    description = meta.get("description", "")
    if "/cave-pony" not in description or "coding or agent-work" not in description:
        errors.append("activation must remain explicit and coding-scoped")

    for text in SECTIONS + ROOT_TERMS + SAFETY_TERMS:
        if text.lower() not in skill.lower():
            errors.append(f"skill missing root contract: {text}")
    steps = re.findall(r"^###\s+(\d+)\.", skill, re.MULTILINE)
    if steps != ["1", "2", "3", "4", "5"]:
        errors.append("execution loop must contain exactly five steps")
    for number in range(1, 6):
        if not re.search(rf"^{number}\.\s+", readme, re.MULTILINE):
            errors.append(f"README missing behaviour step {number}")

    for url in ("https://github.com/DietrichGebert/ponytail", "https://github.com/JuliusBrussee/caveman"):
        if url not in readme:
            errors.append(f"README missing parent attribution: {url}")

    validate_versions(errors, version)
    validate_ci(errors)
    validate_cases(errors, skill)

    if not LOGO.is_file() or LOGO.stat().st_size < 8:
        errors.append("logo must exist and be non-empty")
    elif not LOGO.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        errors.append("logo must be a PNG")

    for path in text_files():
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for term in FORBIDDEN_STANDALONE_TERMS:
            if term in lowered:
                errors.append(f"standalone repository contains forbidden reference in {path.relative_to(ROOT)}: {term}")
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
