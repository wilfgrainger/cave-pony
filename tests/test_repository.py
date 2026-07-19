from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import validate  # noqa: E402


class RepositoryContractTests(unittest.TestCase):
    def run_clone_validation(self, mutate) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "repo"
            shutil.copytree(ROOT, clone)
            mutate(clone)
            return subprocess.run(
                [sys.executable, str(clone / "tools/validate.py")],
                cwd=clone,
                check=False,
                capture_output=True,
                text=True,
            )

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

    def test_activation_scope_regression_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "skills/cave-pony/SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "coding or agent-work",
                "any",
            ), encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("activation", result.stderr)

    def test_ponytail_ladder_regression_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "skills/cave-pony/SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "Deletion over addition. Boring over clever. Fewest files possible.",
                "Prefer maintainable solutions.",
            ), encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Deletion over addition", result.stderr)

    def test_caveman_voice_regression_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "skills/cave-pony/SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "drop articles where meaning stays obvious",
                "use short sentences",
            ), encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("drop articles", result.stderr)

    def test_five_step_loop_drift_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "README.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "5. Put the result first and report only useful Done, Proof, Skipped, and Risk lines.\n",
                "",
            ), encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("step 5", result.stderr)

    def test_mutable_action_reference_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / ".github/workflows/ci.yml"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683",
                "actions/checkout@v4",
            ), encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("immutable commit", result.stderr)


if __name__ == "__main__":
    unittest.main()
