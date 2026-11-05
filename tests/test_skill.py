"""Guards that keep Cave Pony small and the eval honest. No dependencies."""
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/cave-pony/SKILL.md"
TASKS = ROOT / "eval/tasks"
WORD_BUDGET = 450  # the skill is the product; growth needs a measured reason


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "missing frontmatter"
    return m.group(1)


class SkillTests(unittest.TestCase):
    text = SKILL.read_text()

    def test_frontmatter(self):
        fm = frontmatter(self.text)
        self.assertRegex(fm, r"(?m)^name: cave-pony$")
        self.assertRegex(fm, r"(?m)^description: ")
        self.assertRegex(fm, r'(?m)^  version: "\d+\.\d+\.\d+"$')

    def test_word_budget(self):
        body = self.text.split("---", 2)[2]
        self.assertLessEqual(len(body.split()), WORD_BUDGET)

    def test_safety_rules_present(self):
        for phrase in ["Never cut", "input validation", "irreversible", "force-push",
                       "Never say a check passed unless it ran", "Never drop not/no/never/only"]:
            self.assertIn(phrase, self.text)

    def test_readme_version_matches(self):
        version = re.search(r'version: "([\d.]+)"', self.text).group(1)
        self.assertTrue(f"version-{version}-" in (ROOT / "README.md").read_text(), f"README badge != {version}")


class EvalTaskTests(unittest.TestCase):
    """Each hidden check must reject the untouched repo, unless no change is the right answer."""
    PASS_ON_BASE = {"already-works", "keep-validation"}

    def test_checks_discriminate(self):
        empty = Path(tempfile.mkstemp()[1])
        for task in sorted(TASKS.iterdir()):
            with self.subTest(task=task.name):
                self.assertTrue((task / "prompt.txt").read_text().strip())
                env = dict(os.environ, PYTHONPATH=str(task / "repo"), PYTHONDONTWRITEBYTECODE="1")
                r = subprocess.run([sys.executable, str(task / "check.py"), str(empty)],
                                   cwd=task / "repo", env=env, capture_output=True)
                self.assertEqual(r.returncode == 0, task.name in self.PASS_ON_BASE, r.stderr.decode()[-300:])


if __name__ == "__main__":
    unittest.main()
