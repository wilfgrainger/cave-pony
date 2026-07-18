#!/usr/bin/env python3
"""Build a deterministic Cave Pony .skill archive using stdlib only."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT = DIST / "cave-pony.skill"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)

sys.path.insert(0, str(ROOT / "tools"))
from validate import validate  # noqa: E402

FILES = (
    (ROOT / "skills" / "cave-pony" / "SKILL.md", "cave-pony/SKILL.md"),
    (ROOT / "skills" / "cave-pony" / "README.md", "cave-pony/README.md"),
    (ROOT / "THIRD_PARTY_NOTICES.md", "cave-pony/THIRD_PARTY_NOTICES.md"),
)


def build(output: Path = OUTPUT) -> Path:
    errors = validate()
    if errors:
        raise RuntimeError("validation failed:\n" + "\n".join(f"- {error}" for error in errors))

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.unlink(missing_ok=True)

    with ZipFile(temporary, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for source, archive_name in sorted(FILES, key=lambda item: item[1]):
            info = ZipInfo(archive_name, FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())

    shutil.move(temporary, output)
    return output


def main() -> int:
    try:
        output = build()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
