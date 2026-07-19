from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"


class ClaimGateTests(unittest.TestCase):
    def test_presence_is_not_eligibility(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("### 5. Gate the claim", text)
        self.assertIn("Data, output or a fallback being present does not make it eligible for every use.", text)
        self.assertIn("gate on that same predicate", text)

    def test_invalid_status_is_withheld_or_qualified(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("Stale, partial, unverified, unauthorized or incompatible state stays unavailable or clearly qualified.", text)
        self.assertIn("Withholding is often the smallest correct result.", text)

    def test_status_gate_proves_accept_and_reject(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("test one accepted state and the most plausible rejected state", text)
        self.assertIn("A happy-path presence check is not decisive proof.", text)


if __name__ == "__main__":
    unittest.main()
