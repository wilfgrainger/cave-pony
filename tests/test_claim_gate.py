from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"


class ClaimGateTests(unittest.TestCase):
    def test_presence_is_not_eligibility(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("### 5. Gate the claim", text)
        self.assertIn("Presence is not eligibility.", text)
        self.assertRegex(text, r"Gate public, API and UI claims on the predicate that makes them true")

    def test_invalid_status_is_withheld_or_qualified(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        for status in ("stale", "partial", "unverified", "unauthorized", "incompatible"):
            self.assertIn(status, text)
        self.assertRegex(text, r"unavailable or clearly qualified")

    def test_status_gate_proves_accept_and_reject(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertRegex(text, r"Test one accepted state and the most plausible rejected state")


if __name__ == "__main__":
    unittest.main()
