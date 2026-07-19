from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"


class InstructionBudgetContractTests(unittest.TestCase):
    def test_single_primary_skill_contract(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("### 3. Budget the instructions", text)
        self.assertRegex(text, r"standing instructions as owned surface")
        self.assertRegex(text, r"one primary skill plus the shortest domain profile")
        self.assertRegex(text, r"only the authoritative guidance needed")
        self.assertRegex(text, r"Delete stale or duplicate instructions")

    def test_instruction_surface_pays_the_complexity_toll(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("standing instruction or mandatory context source needs:", text)
        self.assertIn("maintenance, failure and context surface", text)
        self.assertIn("standing instructions", text)
        self.assertIn("mandatory context", text)


if __name__ == "__main__":
    unittest.main()
