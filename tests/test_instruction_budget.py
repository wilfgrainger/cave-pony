from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"


class InstructionBudgetContractTests(unittest.TestCase):
    def test_single_primary_skill_contract(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        for sentence in (
            "Standing instructions are owned surface too.",
            "Use one primary skill plus the shortest repository profile",
            "Do not stack overlapping skills or load every steering file by default.",
            "Remove or correct stale copies instead of asking future agents to reconcile them forever.",
        ):
            self.assertIn(sentence, text)

    def test_instruction_surface_pays_the_complexity_toll(self) -> None:
        text = SKILL.read_text(encoding="utf-8")

        self.assertIn("standing instruction or mandatory context source needs:", text)
        self.assertIn("maintenance, failure and context surface", text)
        self.assertIn("standing instructions, mandatory context", text)


if __name__ == "__main__":
    unittest.main()
