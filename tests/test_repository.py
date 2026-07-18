from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import build  # noqa: E402
import validate  # noqa: E402


class RepositoryContractTests(unittest.TestCase):
    def test_static_validation(self) -> None:
        self.assertEqual([], validate.validate())

    def test_validator_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TOOLS / "validate.py")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("validation passed", result.stdout.lower())

    def test_archive_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "cave-pony.skill"
            build.build(output)
            with ZipFile(output) as archive:
                self.assertEqual(
                    [
                        "cave-pony/README.md",
                        "cave-pony/SKILL.md",
                        "cave-pony/THIRD_PARTY_NOTICES.md",
                    ],
                    archive.namelist(),
                )
                skill = archive.read("cave-pony/SKILL.md").decode("utf-8")
                self.assertIn("name: cave-pony", skill)
                self.assertIn("## Clarity override", skill)

    def test_archive_is_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.skill"
            second = Path(directory) / "second.skill"
            build.build(first)
            build.build(second)
            first_hash = hashlib.sha256(first.read_bytes()).hexdigest()
            second_hash = hashlib.sha256(second.read_bytes()).hexdigest()
            self.assertEqual(first_hash, second_hash)


if __name__ == "__main__":
    unittest.main()
