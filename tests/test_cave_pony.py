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


def step(cmd, ok=True, after_edit=True):
    return {"cmd": cmd, "ok": ok, "after_edit": after_edit}


class UnbackedFlag(unittest.TestCase):
    def test_flags_a_claim_with_nothing_run(self):
        self.assertTrue(run.unbacked("Done. Tests pass.", []))

    def test_a_failed_command_does_not_back_a_claim(self):
        self.assertTrue(run.unbacked("Done. Tests pass.", [step("python3 -m pytest", ok=False)]))

    def test_any_successful_run_backs_a_claim_even_when_no_edit_was_needed(self):
        self.assertFalse(run.unbacked("It already works; I confirmed it.", [step("python3 -c 'import text'", after_edit=False)]))

    def test_admitting_nothing_ran_is_not_a_fake_claim(self):
        self.assertFalse(run.unbacked("Simplified it. I didn't run it, so nothing is verified.", []))

    def test_everyday_words_are_not_claims(self):
        self.assertFalse(run.unbacked("The default is overwritten by any argument passed in.", []))


class PairedInterval(unittest.TestCase):
    @staticmethod
    def rows(diffs):
        """One baseline row at 0 and one row for arm 'x' at the given per-task offset, two reps each."""
        out = []
        for task, d in enumerate(diffs):
            for rep in range(2):
                out.append({"task": f"t{task}", "rep": rep, "arm": "x", "words": 10 + d})
                out.append({"task": f"t{task}", "rep": rep, "arm": "base", "words": 10})
        return out

    def test_a_consistent_difference_has_an_interval_that_excludes_zero(self):
        mean, lo, hi = run.paired_ci(self.rows([-5, -5, -5, -5]), "x", "base", "words")
        self.assertEqual((mean, lo, hi), (-5, -5, -5))

    def test_a_difference_that_flips_sign_across_tasks_includes_zero(self):
        mean, lo, hi = run.paired_ci(self.rows([-5, 5, -5, 5]), "x", "base", "words")
        self.assertEqual(mean, 0)
        self.assertLess(lo, 0)
        self.assertGreater(hi, 0)

    def test_arms_with_no_shared_runs_have_no_interval(self):
        self.assertIsNone(run.paired_ci(self.rows([1]), "x", "missing", "words"))

    def test_the_interval_is_reproducible(self):
        rows = self.rows([-5, 5, -5, 5, 1, 2])
        self.assertEqual(run.paired_ci(rows, "x", "base", "words"), run.paired_ci(rows, "x", "base", "words"))


class OneLineRule(unittest.TestCase):
    """The rule people are told to paste is the rule that was measured."""
    RULE = (ROOT / "eval/arms/one-line.md").read_text().strip()

    def test_it_stays_short(self):
        self.assertLessEqual(len(self.RULE.split()), 60)

    def test_readme_shows_exactly_the_measured_rule(self):
        self.assertIn(self.RULE, README)


class PublishedResults(unittest.TestCase):
    """Each README results table must match its raw results file exactly."""
    NAMES = {"No skill": "baseline", "One-line rule": "one-line", "Caveman": "caveman", "Ponytail": "ponytail",
             "Caveman + Ponytail": "both", "Cave Pony": "cave-pony"}
    # (README section heading, raw file, cost decimals). Haiku costs ~$0.002 a run, so it needs more digits.
    TABLES = [("Sonnet 5.5", run.PUBLISHED, 3),
              ("Haiku 5.5", ROOT / "eval/results/haiku-2026-11-05.jsonl", 4)]

    def section(self, heading):
        for part in README.split("\n### "):
            if part.startswith(heading):
                return part
        self.fail(f"README has no '### {heading}' section")

    def check_table(self, heading, path, cost_digits):
        rows = [json.loads(l) for l in path.read_text().splitlines()]
        self.assertFalse([r for r in rows if "error" in r or r.get("tampered")], f"{path.name}: errored or tampered rows")
        for arm in ("cave-pony", "one-line"):  # the two prompts that live in this repo
            self.assertEqual({r["skill_sha"] for r in rows if r["arm"] == arm}, {run.sha(run.skill_prompt(arm))},
                             f"{path.name}: {arm} was measured with different text than the repo now has; re-run the eval")
        table = 0
        for line in self.section(heading).splitlines():
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
                        f"{sum(r['total_tokens'] for r in rs) / n:.0f}",
                        f"{sum(r['cost'] for r in rs) / n:.{cost_digits}f}"]
            self.assertEqual(cells[1:], expected, f"{heading}: {cells[0]}")
        self.assertEqual(table, len(self.NAMES), f"{heading}: results table not found")

    def test_sonnet_table_matches_raw_results(self):
        self.check_table(*self.TABLES[0])

    def test_haiku_table_matches_raw_results(self):
        self.check_table(*self.TABLES[1])


if __name__ == "__main__":
    unittest.main()
