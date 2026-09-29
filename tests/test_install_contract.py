from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github/workflows/ci.yml"
README = ROOT / "README.md"
HOST_VERIFICATION = ROOT / "docs/HOST_VERIFICATION.md"
PROTOCOL = ROOT / "docs/CODEX_BEHAVIOUR_PROTOCOL.md"
FIELD_TEMPLATE = ROOT / "field-tests/TEMPLATE.md"


class InstallContractTests(unittest.TestCase):
    def test_first_use_distinguishes_host_invocation_and_primary_modes(self) -> None:
        readme = README.read_text(encoding="utf-8")
        self.assertLess(readme.index("## Quick start"), readme.index("## How it works"))
        self.assertLess(readme.index("### Full"), readme.index("### Audit"))
        self.assertLess(readme.index("### Audit"), readme.index("## Advanced controls"))
        for host, invocation in (("Codex CLI or IDE", "$cave-pony"), ("ChatGPT", "@cave-pony"), ("Claude Code", "/cave-pony")):
            self.assertIn(host, readme)
            self.assertIn(invocation, readme)
        self.assertIn("Installation does not prove agent behavior", readme)

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

    def test_behavior_protocol_records_comparable_outcomes_and_losses(self) -> None:
        protocol = PROTOCOL.read_text(encoding="utf-8")
        template = FIELD_TEMPLATE.read_text(encoding="utf-8")
        for scenario in (
            "No-change decision",
            "Native reuse",
            "Shared root cause",
            "Permission or migration boundary",
            "Destructive clarity",
            "Audit of an overbuilt diff",
        ):
            self.assertIn(scenario, protocol)
        for required in ("same starting commit", "baseline run", "skill run", "independent reviewer", "neutral or losing"):
            self.assertIn(required, protocol.lower())
        for required in ("Comparison", "Baseline run", "Skill run", "Neutral or losing"):
            self.assertIn(required, template)


if __name__ == "__main__":
    unittest.main()
