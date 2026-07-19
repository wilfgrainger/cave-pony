from __future__ import annotations

import json
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
                [sys.executable, str(clone / "tools" / "validate.py")],
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

    def test_adversarial_contract_cases(self) -> None:
        cases = json.loads((ROOT / "tests" / "behavioral_cases.json").read_text(encoding="utf-8"))
        required = {"reset-hard", "rotate-key", "delete-branches"}
        self.assertTrue(required.issubset({case["id"] for case in cases}))
        skill = (ROOT / "skills" / "cave-pony" / "SKILL.md").read_text(encoding="utf-8")
        for case in cases:
            self.assertIsInstance(case["prompt"], str)
            self.assertTrue(case["prompt"].strip())
            self.assertIn(case["trigger"], skill)
            self.assertGreaterEqual(len(case["required_contract"]), 2)

    def test_extra_behavioral_case_is_allowed(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "tests" / "behavioral_cases.json"
            cases = json.loads(path.read_text(encoding="utf-8"))
            cases.append({
                "id": "drop-table",
                "prompt": "drop the temporary database table",
                "trigger": "drops",
                "required_contract": ["state data-loss consequence", "state recovery requirement"],
            })
            path.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_activation_regression_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            skill = clone / "skills" / "cave-pony" / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8").replace(
                "Use when the user invokes /cave-pony or cave-pony",
                "Use for coding, debugging, and refactoring",
            ), encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("ordinary coding", result.stderr)

    def test_ambiguous_activation_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            skill = clone / "skills" / "cave-pony" / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8").replace(
                "If no earlier trigger is present, Cave Pony is inactive.",
                "If unsure whether Cave Pony is active, it is.",
            ), encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("ambiguity", result.stderr)

    def test_readme_loop_drift_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            readme = clone / "README.md"
            readme.write_text(readme.read_text(encoding="utf-8").replace(
                "9. Report Done, Proof, conditional Skipped, and Risk.\n",
                "",
            ), encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("step numbers", result.stderr)

    def test_missing_safety_tiebreak_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            skill = clone / "skills" / "cave-pony" / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8").replace(
                "Ties between brevity and clarity always break toward clarity.",
                "",
            ), encoding="utf-8")

        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("safety sentence", result.stderr)


if __name__ == "__main__":
    unittest.main()
