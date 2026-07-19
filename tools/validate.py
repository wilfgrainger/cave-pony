#!/usr/bin/env python3
"""Validate Cave Pony's repository and written behavioural contract."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"
README = ROOT / "README.md"
DESIGN = ROOT / "docs" / "DESIGN.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"

REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CONTRIBUTING.md",
    ".github/workflows/ci.yml",
    "skills/cave-pony/SKILL.md",
    "skills/cave-pony/README.md",
    "docs/DESIGN.md",
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

SKILL_EXPECTATIONS = (
    "coding or agent-work request",
    "A generic request to be brief outside coding or agent work does not activate Cave Pony.",
    "ACTIVE EVERY RESPONSE",
    "only after one of the activation triggers above occurred earlier in this conversation",
    "correctness first, then YAGNI and KISS, then DRY",
    "Repeated syntax alone is not a reason to abstract",
    "standing instructions as owned surface",
    "one primary skill plus the shortest domain profile",
    "Fields and claims must use the event or authority they name",
    "generated output deterministic unless variability is required",
    "Presence is not eligibility",
    "Test one accepted state and the most plausible rejected state",
    "complexity toll",
    "root-cause",
    "# cave-pony: global lock",
    "Name the ceiling and concrete upgrade trigger",
    "Compress by deletion, not shorthand",
    "Do not invent prose abbreviations",
    "do not use arrows as prose",
    "No decorative tables or emoji",
    "dumping raw logs",
    "same failure survives two attempted corrections",
    "one decisive diagnostic",
    "exact failure, known cause, smallest correction, and proof or next diagnostic",
    "smallest decisive",
    "Never claim a check passed unless it ran",
    "footprint report",
    "Skipped: <thing>; revisit when <condition>",
    "Finding: <defect>",
    "Consequence: <why it matters>",
    "Smallest correction: <least change that fixes it>",
    "The target defaults to the most recent change or diff unless the user specifies another target.",
    "When the user still has work to do",
    "Do not manufacture homework",
    "Give time estimates only when grounded",
    "do not recap every turn",
)

README_EXPECTATIONS = (
    "## See it in 30 seconds",
    "### Bad",
    "### Better",
    "### Why",
    "### Stop a debugging spiral",
    "## Real-world field evidence",
    "## Presentation influence",
    "universal activation",
    "compulsory time estimates",
    "YAGNI and KISS before stable-knowledge DRY",
    "Correctness and trust boundaries come first",
)

DESIGN_EXPECTATIONS = (
    "## Intentional parent divergences",
    "Uncertainty does not activate the skill",
    "The clarity override is broader",
    "Similar syntax does not prove shared knowledge",
    "tools/validate.py` is the authoritative static contract checker",
)

REQUIRED_CASES = {
    "reset-hard": "resets",
    "rotate-key": "rotates",
    "delete-branches": "deletes",
}

PINNED_ACTIONS = {
    "actions/checkout": "11bd71901bbe5b1630ceea73d27597364c9af683",
    "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
}


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


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def require_terms(errors: list[str], label: str, text: str, terms: tuple[str, ...]) -> None:
    lowered = text.lower()
    for term in terms:
        if term.lower() not in lowered:
            errors.append(f"{label} missing contract term: {term}")


def validate_behavioral_cases(errors: list[str]) -> None:
    path = ROOT / "tests" / "behavioral_cases.json"
    if not path.is_file():
        return
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid behavioral_cases.json: {exc}")
        return
    if not isinstance(cases, list):
        errors.append("behavioral_cases.json must contain a list")
        return

    found: dict[str, str] = {}
    for case in cases:
        if not isinstance(case, dict):
            errors.append("behavioral case must be an object")
            continue
        case_id = case.get("id")
        prompt = case.get("prompt")
        trigger = case.get("trigger")
        requirements = case.get("required_contract")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append("behavioral case requires a non-empty string id")
            continue
        if case_id in found:
            errors.append(f"duplicate behavioral case id: {case_id!r}")
            continue
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"behavioral case {case_id!r} requires a string prompt")
        if not isinstance(trigger, str) or not trigger.strip():
            errors.append(f"behavioral case {case_id!r} requires a string trigger")
            continue
        found[case_id] = trigger
        if not isinstance(requirements, list) or len(requirements) < 2:
            errors.append(f"behavioral case {case_id!r} needs at least two contract requirements")
        elif not all(isinstance(item, str) and item.strip() for item in requirements):
            errors.append(f"behavioral case {case_id!r} requirements must be non-empty strings")

    for case_id, trigger in REQUIRED_CASES.items():
        if found.get(case_id) != trigger:
            errors.append(
                f"required behavioral case {case_id!r} must use {trigger!r}; "
                f"found {found.get(case_id)!r}"
            )


def validate_loop_sync(errors: list[str], skill_text: str, readme: str) -> None:
    skill_steps = re.findall(r"^###\s+(\d+)\.", section(skill_text, "## Execution loop"), re.MULTILINE)
    readme_steps = re.findall(r"^(\d+)\.\s+", section(readme, "## Behaviour"), re.MULTILINE)
    if not skill_steps:
        errors.append("SKILL.md execution loop has no numbered steps")
    elif skill_steps != readme_steps:
        errors.append(
            "README Behaviour step numbers must match SKILL.md execution loop; "
            f"skill={skill_steps!r}, readme={readme_steps!r}"
        )


def validate_ci(errors: list[str]) -> None:
    if not CI.is_file():
        return
    workflow = CI.read_text(encoding="utf-8")
    if workflow.count("branches: [main]") != 2:
        errors.append("CI must run only for pushes and pull requests targeting main")
    if "cancel-in-progress: true" not in workflow:
        errors.append("CI must cancel superseded runs")
    if "permissions:\n  contents: read" not in workflow:
        errors.append("CI must keep read-only repository permissions")

    for action, expected_sha in PINNED_ACTIONS.items():
        match = re.search(rf"uses:\s*{re.escape(action)}@([^\s#]+)", workflow)
        if not match:
            errors.append(f"CI missing action: {action}")
        elif match.group(1) != expected_sha:
            errors.append(f"CI action {action} must use immutable commit {expected_sha}")


def validate() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if not SKILL.is_file():
        return errors

    skill_text = SKILL.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8") if README.is_file() else ""
    design = DESIGN.read_text(encoding="utf-8") if DESIGN.is_file() else ""
    try:
        frontmatter = parse_frontmatter(skill_text)
    except ValueError as exc:
        errors.append(str(exc))
        frontmatter = {}

    for key, expected in {"name": "cave-pony", "license": "MIT"}.items():
        if frontmatter.get(key) != expected:
            errors.append(f"frontmatter {key!r} must equal {expected!r}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", frontmatter.get("version", "")):
        errors.append("frontmatter 'version' must use MAJOR.MINOR.PATCH")

    description = frontmatter.get("description", "")
    if "/cave-pony" not in description or "invokes" not in description:
        errors.append("frontmatter description must use explicit invocation language")
    if "coding or agent-work" not in description:
        errors.append("frontmatter description must limit implicit triggers to coding or agent work")
    if "Do not auto-load for ordinary coding or non-coding requests" not in description:
        errors.append("frontmatter description must exclude ordinary coding and non-coding requests")
    if "build=" not in frontmatter.get("argument-hint", ""):
        errors.append("argument-hint must expose independent build and voice controls")

    for required in REQUIRED_SECTIONS:
        if required not in skill_text:
            errors.append(f"SKILL.md missing section: {required}")

    require_terms(errors, "SKILL.md", skill_text, SKILL_EXPECTATIONS)
    require_terms(errors, "README.md", readme, README_EXPECTATIONS)
    require_terms(errors, "docs/DESIGN.md", design, DESIGN_EXPECTATIONS)

    if "If unsure whether Cave Pony is active, it is." in skill_text:
        errors.append("SKILL.md must not activate Cave Pony from ambiguity")
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
    validate_loop_sync(errors, skill_text, readme)
    validate_ci(errors)

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
