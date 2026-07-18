#!/usr/bin/env python3
"""Validate Cave Pony's repository and skill contract using stdlib only."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"

REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CONTRIBUTING.md",
    "skills/cave-pony/SKILL.md",
    "skills/cave-pony/README.md",
    "docs/DESIGN.md",
    "tools/build.py",
    "tools/validate.py",
    "tests/test_repository.py",
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


def validate() -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if not SKILL.is_file():
        return errors

    skill_text = SKILL.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(skill_text)
    except ValueError as exc:
        errors.append(str(exc))
        frontmatter = {}

    expected_frontmatter = {
        "name": "cave-pony",
        "license": "MIT",
    }
    for key, expected in expected_frontmatter.items():
        if frontmatter.get(key) != expected:
            errors.append(f"frontmatter {key!r} must equal {expected!r}")

    description = frontmatter.get("description", "")
    if len(description) < 120:
        errors.append("frontmatter description must explain the dual-budget behaviour")
    if "build=" not in frontmatter.get("argument-hint", ""):
        errors.append("argument-hint must expose independent build and voice controls")

    for section in REQUIRED_SECTIONS:
        if section not in skill_text:
            errors.append(f"SKILL.md missing section: {section}")

    contract_terms = (
        "smallest decisive",
        "complexity toll",
        "root-cause",
        "Never claim a check passed unless it ran",
        "security",
        "accessibility",
        "destructive",
    )
    for term in contract_terms:
        if term.lower() not in skill_text.lower():
            errors.append(f"SKILL.md missing contract term: {term}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
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

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "dist" in path.parts:
            continue
        if path.suffix not in {".md", ".py", ".yml", ".yaml", ".txt"} and path.name not in {"Makefile", ".gitignore"}:
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
