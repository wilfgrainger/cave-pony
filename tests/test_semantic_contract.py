from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"


class SemanticContractTests(unittest.TestCase):
    def test_values_come_from_the_event_they_name(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("### 4. Own the meaning", text)
        self.assertIn("Every field, label and public claim must come from the event or authority it names.", text)
        self.assertIn("Keep observation, publication, retrieval, validation, build and display times separate", text)

    def test_generated_output_is_stable_without_changed_inputs(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("Generated output should be deterministic when its inputs are unchanged.", text)
        self.assertIn("Do not inject the wall clock, randomness, unstable ordering or environment-specific values", text)

    def test_tests_protect_meaning_not_incidental_wording(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("Tests should protect behaviour, invariants and semantic contracts.", text)
        self.assertIn("Do not freeze incidental prose, formatting or implementation detail", text)


if __name__ == "__main__":
    unittest.main()
