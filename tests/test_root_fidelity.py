from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cave-pony" / "SKILL.md"
SKILL_README = ROOT / "skills" / "cave-pony" / "README.md"
README = ROOT / "README.md"
DESIGN = ROOT / "docs" / "DESIGN.md"


class RootFidelityTests(unittest.TestCase):
    def test_intentional_parent_divergences_are_documented(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("## Intentional parent divergences", design)
        self.assertIn("Uncertainty does not activate the skill", design)
        self.assertIn("The clarity override is broader", design)

    def test_ceiling_comment_is_durable_and_conditional(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("# cave-pony: global lock", skill)
        self.assertIn("Name the ceiling and concrete upgrade trigger", skill)
        self.assertIn("Do not comment obvious choices or hypothetical futures", skill)

    def test_voice_rules_prevent_fake_compression(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Compress by deletion, not shorthand",
            "Do not invent prose abbreviations",
            "do not use arrows as prose",
            "No decorative tables or emoji",
            "dumping raw logs",
        ):
            self.assertIn(phrase, skill)

    def test_debug_spiral_and_failure_shape_are_explicit(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        skill_readme = SKILL_README.read_text(encoding="utf-8")
        self.assertIn("same failure survives two attempted corrections", skill)
        self.assertIn("one decisive diagnostic", skill)
        self.assertIn(
            "exact failure, known cause, smallest correction, and proof or next diagnostic",
            skill,
        )
        self.assertIn("Repeated failures stop the patch loop", skill_readme)

    def test_next_action_and_estimates_are_conditional(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("When the user still has work to do", skill)
        self.assertIn("Do not manufacture homework", skill)
        self.assertIn("Give time estimates only when grounded", skill)
        self.assertIn("do not recap every turn", skill)

    def test_readme_teaches_with_concrete_examples(self) -> None:
        readme = README.read_text(encoding="utf-8")
        for phrase in (
            "## See it in 30 seconds",
            "### Bad",
            "### Better",
            "### Why",
            "### Stop a debugging spiral",
            "## Real-world field evidence",
            "## Presentation influence",
        ):
            self.assertIn(phrase, readme)
        self.assertIn("universal activation", readme)
        self.assertIn("compulsory time estimates", readme)


if __name__ == "__main__":
    unittest.main()
