from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github/workflows/ci.yml"
README = ROOT / "README.md"
HOST_VERIFICATION = ROOT / "docs/HOST_VERIFICATION.md"


class InstallContractTests(unittest.TestCase):
    def test_ci_verifies_commit_pinned_codex_install(self) -> None:
        workflow = CI.read_text(encoding="utf-8")
        for required in (
            "DISABLE_TELEMETRY",
            "ref: ${{ github.event.pull_request.head.sha || github.sha }}",
            "skills@1.5.9",
            '"$GITHUB_WORKSPACE/skills/cave-pony"',
            "--agent codex",
            "--copy",
            ".agents/skills/cave-pony/SKILL.md",
            'cmp -s "$GITHUB_WORKSPACE/skills/cave-pony/SKILL.md" .agents/skills/cave-pony/SKILL.md',
        ):
            self.assertIn(required, workflow)

    def test_public_claim_links_to_evidence_boundary(self) -> None:
        readme = README.read_text(encoding="utf-8")
        evidence = HOST_VERIFICATION.read_text(encoding="utf-8")
        self.assertIn("[Host verification](docs/HOST_VERIFICATION.md)", readme)
        self.assertIn("does not prove", evidence)
        self.assertIn("authenticated Codex session", evidence)


if __name__ == "__main__":
    unittest.main()
