from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"


class SemanticContractTests(unittest.TestCase):
    def test_values_keep_the_meaning_they_name(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("### 4. Own the meaning", text)
        self.assertRegex(text, r"Fields and claims must use the event or authority they name")
        self.assertRegex(text, r"keep unlike dates, states and categories separate")

    def test_generated_output_is_stable_without_required_variability(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertRegex(text, r"generated output deterministic unless variability is required")

    def test_tests_protect_meaning_not_incidental_wording(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertRegex(text, r"test behaviour or invariants rather than incidental wording")


if __name__ == "__main__":
    unittest.main()
