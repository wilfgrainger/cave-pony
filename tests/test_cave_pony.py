"""Keeps the skill small, the eval honest, and the README true. Standard library only."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/cave-pony/SKILL.md"
README = (ROOT / "README.md").read_text()
TASKS = ROOT / "eval/tasks"
WORD_BUDGET = 450  # the skill is the product; growing it needs a measured win

sys.path.insert(0, str(ROOT / "eval"))
import run  # noqa: E402


class Skill(unittest.TestCase):
    text = SKILL.read_text()

    def test_frontmatter(self):
        fm = re.match(r"^---\n(.*?)\n---\n", self.text, re.S)
        self.assertTrue(fm, "missing frontmatter")
        self.assertRegex(fm.group(1), r"(?m)^name: cave-pony$")
        self.assertRegex(fm.group(1), r"(?m)^description: ")
        self.assertRegex(fm.group(1), r'(?m)^  version: "\d+\.\d+\.\d+"$')

    def test_word_budget(self):
        self.assertLessEqual(len(self.text.split("---", 2)[2].split()), WORD_BUDGET)

    def test_safety_rules(self):
        for phrase in ["Never cut", "input validation", "irreversible", "go-ahead", "force-push",
                       "Never say a check passed unless it ran", "Never drop not/no/never/only"]:
            self.assertIn(phrase, self.text)

    def test_readme_version(self):
        version = re.search(r'version: "([\d.]+)"', self.text).group(1)
        self.assertIn(f"version-{version}-", README)


class Tasks(unittest.TestCase):
    PASS_ON_BASE = {"already-works", "keep-validation"}  # no change is a correct answer

    def test_each_task_is_complete(self):
        for task in sorted(TASKS.iterdir()):
            with self.subTest(task=task.name):
                self.assertTrue((task / "prompt.txt").read_text().strip())
                self.assertTrue((task / "check.py").is_file())
                self.assertTrue((task / "repo").is_dir())

    def test_checks_reject_the_untouched_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            reply = Path(tmp) / "reply.txt"
            reply.write_text("")
            for task in sorted(TASKS.iterdir()):
                with self.subTest(task=task.name):
                    env = dict(os.environ, PYTHONPATH=str(task / "repo"), PYTHONDONTWRITEBYTECODE="1")
                    r = subprocess.run([sys.executable, str(task / "check.py"), str(reply)],
                                       cwd=task / "repo", env=env, capture_output=True)
                    self.assertEqual(r.returncode == 0, task.name in self.PASS_ON_BASE, r.stderr.decode()[-300:])


def use(i, name, cmd=""):
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "id": i, "name": name, "input": {"command": cmd}}]}}


def results(*ids, failed=()):
    return {"type": "user", "message": {"content": [
        {"type": "tool_result", "tool_use_id": i, "is_error": i in failed} for i in ids]}}


class Scorer(unittest.TestCase):
    def test_only_successful_code_runs_after_an_edit_count(self):
        events = [use("a", "Bash", "python3 repro.py"), use("b", "Edit"), use("c", "Bash", "git diff"),
                  use("d", "Bash", "python3 -c 1"), use("e", "Bash", "pytest"), results(*"acde", failed="e")]
        self.assertEqual(run.verified_runs(events), ["python3 -c 1"])

    def test_heredoc_edit_and_check_in_one_command_counts(self):
        events = [use("f", "Bash", "cat >> cart.py <<'EOF'\nx = 1\nEOF\npython3 -c 'import cart'"), results("f")]
        self.assertEqual(len(run.verified_runs(events)), 1)

    def test_stderr_redirect_is_not_an_edit(self):
        self.assertFalse(run.EDIT_CMD.search("python3 t.py 2>&1"))

    def test_denied_command_does_not_count(self):
        events = [use("b", "Write"), use("g", "Bash", "python3 t.py"), results("g", failed="g")]
        self.assertEqual(run.verified_runs(events), [])


class PublishedResults(unittest.TestCase):
    """The README table must match eval/results/published.jsonl exactly."""
    NAMES = {"No skill": "baseline", "Caveman": "caveman", "Ponytail": "ponytail",
             "Caveman + Ponytail": "both", "Cave Pony": "cave-pony"}

    def test_readme_table_matches_raw_results(self):
        rows = [json.loads(l) for l in run.PUBLISHED.read_text().splitlines()]
        self.assertFalse([r for r in rows if "error" in r or r.get("tampered")], "errored or tampered rows")
        sha = run.sha(run.skill_prompt("cave-pony"))
        self.assertEqual({r["skill_sha"] for r in rows if r["arm"] == "cave-pony"}, {sha},
                         "published results were measured with a different SKILL.md; re-run the eval")
        table = 0
        for line in README.splitlines():
            cells = [c.strip().strip("*") for c in line.strip("|").split("|")]
            if len(cells) != 7 or cells[0] not in self.NAMES:
                continue
            table += 1
            rs = [r for r in rows if r["arm"] == self.NAMES[cells[0]]]
            code = [r for r in rs if r["diff"]]
            n = len(rs)
            expected = [f"{sum(r['pass'] for r in rs)}/{n}",
                        f"{sum(bool(r['verified_cmds']) for r in code)}/{len(code)}",
                        f"{sum(r['diff'] for r in rs) / n:.1f}",
                        f"{sum(r['words'] for r in rs) / n:.0f}",
                        f"{sum(r['out'] for r in rs) / n:.0f}",
                        f"{sum(r['cost'] for r in rs) / n:.3f}"]
            self.assertEqual(cells[1:], expected, cells[0])
        self.assertEqual(table, len(self.NAMES), "README results table not found")


if __name__ == "__main__":
    unittest.main()
