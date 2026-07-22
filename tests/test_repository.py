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

    def assert_mutation_fails(self, mutate, expected: str) -> None:
        result = self.run_clone_validation(mutate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn(expected.lower(), result.stderr.lower())

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

        self.assert_mutation_fails(mutate, "activation")

    def test_ponytail_ladder_regression_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "skills/cave-pony/SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "Deletion over addition. Boring over clever. Fewest files possible.",
                "Prefer maintainable solutions.",
            ), encoding="utf-8")

        self.assert_mutation_fails(mutate, "Deletion over addition")

    def test_caveman_voice_regression_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "skills/cave-pony/SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "drop articles where meaning stays obvious",
                "use short sentences",
            ), encoding="utf-8")

        self.assert_mutation_fails(mutate, "drop articles")

    def test_five_step_loop_drift_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "README.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "5. Put the result first and report only useful Done, Proof, Skipped, and Risk lines.\n",
                "",
            ), encoding="utf-8")

        self.assert_mutation_fails(mutate, "step 5")

    def test_mutable_action_reference_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / ".github/workflows/ci.yml"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683",
                "actions/checkout@v4",
            ), encoding="utf-8")

        self.assert_mutation_fails(mutate, "immutable commit")

    def test_ci_write_permission_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / ".github/workflows/ci.yml"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "contents: read",
                "contents: write",
            ), encoding="utf-8")

        self.assert_mutation_fails(mutate, "read-only")

    def test_missing_launch_asset_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            (clone / "docs/ORIGINS_AND_DIFFERENCES.md").unlink()

        self.assert_mutation_fails(mutate, "missing file")

    def test_version_drift_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "skills/cave-pony/README.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "Cave Pony `0.1.0`",
                "Cave Pony `9.9.9`",
            ), encoding="utf-8")

        self.assert_mutation_fails(mutate, "version drift")

    def test_safety_boundary_regression_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "skills/cave-pony/SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "authentication or authorisation",
                "basic access checks",
            ), encoding="utf-8")

        self.assert_mutation_fails(mutate, "authentication or authorisation")

    def test_standalone_statement_regression_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            path = clone / "CONTRIBUTING.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "This standalone repository is the canonical home of the skill.",
                "This repository may contain unrelated integrations.",
            ), encoding="utf-8")

        self.assert_mutation_fails(mutate, "standalone contract")

    def test_invalid_logo_is_caught(self) -> None:
        def mutate(clone: Path) -> None:
            (clone / "assets/cave-pony-logo.png").write_bytes(b"not a png")

        self.assert_mutation_fails(mutate, "asset must be a PNG")

    def test_invalid_social_preview_dimensions_are_caught(self) -> None:
        def mutate(clone: Path) -> None:
            source = clone / "assets/cave-pony-logo.png"
            target = clone / "assets/cave-pony-social-preview.png"
            target.write_bytes(source.read_bytes())

        self.assert_mutation_fails(mutate, "PNG dimensions")


if __name__ == "__main__":
    unittest.main()
