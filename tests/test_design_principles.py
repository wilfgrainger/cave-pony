from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"
README = ROOT / "README.md"
DESIGN = ROOT / "docs" / "DESIGN.md"


class DesignPrincipleTests(unittest.TestCase):
    def test_skill_names_and_orders_the_principles(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        for principle in ("YAGNI", "KISS", "DRY"):
            self.assertIn(principle, skill)
        self.assertIn(
            "correctness first, then YAGNI and KISS, then DRY",
            skill,
        )

    def test_dry_targets_knowledge_not_similar_syntax(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn(
            "Repeated syntax alone is not a reason to abstract",
            skill,
        )
        self.assertIn(
            "Do not create generic machinery merely because two blocks look alike",
            skill,
        )

    def test_public_docs_match_the_contract(self) -> None:
        readme = README.read_text(encoding="utf-8")
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("YAGNI and KISS before stable-knowledge DRY", readme)
        self.assertIn("Correctness and trust boundaries come first", readme)
        self.assertIn("Similar syntax does not prove shared knowledge", design)


if __name__ == "__main__":
    unittest.main()
