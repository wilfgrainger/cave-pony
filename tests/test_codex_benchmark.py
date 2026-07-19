import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "benchmarks" / "run_codex.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("cave_pony_codex_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Codex benchmark runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CodexBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = load_runner()

    def test_manifest_uses_codex_with_chatgpt_login(self) -> None:
        manifest = self.runner.MANIFEST
        self.assertEqual(manifest["runner"], "codex-cli")
        self.assertEqual(manifest["authentication"], "chatgpt-login")
        self.assertEqual(manifest["runs_per_cell"], 10)
        self.assertEqual(
            manifest["arms"],
            ["baseline", "both-parents", "cave-pony", "yagni-control"],
        )

    def test_arm_snapshots_match_manifest(self) -> None:
        for _name, spec in self.runner.MANIFEST["arm_sources"].items():
            path = ROOT / spec["path"]
            self.assertTrue(path.is_file())
            self.assertEqual(self.runner.git_blob_sha(path), spec["blob_sha"])

    def test_command_is_ephemeral_and_ignores_user_config(self) -> None:
        self.runner.CODEX_BIN = "/usr/bin/codex"
        self.runner.MODEL_ID = "test-model"
        self.runner.REASONING_EFFORT = "high"
        command = self.runner.codex_command("do task", Path("last.txt"))
        self.assertEqual(command[:2], ["/usr/bin/codex", "exec"])
        for flag in (
            "--ephemeral",
            "--json",
            "--ignore-user-config",
            "--ignore-rules",
            "--sandbox",
            "workspace-write",
            "--model",
            "test-model",
        ):
            self.assertIn(flag, command)

    def test_arms_are_explicitly_activated(self) -> None:
        cave = self.runner.prompt_for("Implement it.", "cave-pony")
        parents = self.runner.prompt_for("Implement it.", "both-parents")
        baseline = self.runner.prompt_for("Implement it.", "baseline")
        self.assertTrue(cave.startswith("/cave-pony"))
        self.assertTrue(parents.startswith("/ponytail full\n/caveman full"))
        self.assertFalse(baseline.startswith("/"))

    def test_jsonl_parser_collects_usage_and_final_message(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            events = root / "events.jsonl"
            last = root / "last.txt"
            rows = [
                {"type": "thread.started", "thread_id": "t"},
                {
                    "type": "item.completed",
                    "item": {"type": "agent_message", "text": "Done."},
                },
                {
                    "type": "turn.completed",
                    "usage": {
                        "input_tokens": 100,
                        "cached_input_tokens": 40,
                        "output_tokens": 12,
                        "reasoning_output_tokens": 5,
                    },
                },
            ]
            events.write_text(
                "\n".join(json.dumps(row) for row in rows) + "\n",
                encoding="utf-8",
            )
            last.write_text("Done.\n", encoding="utf-8")
            parsed = self.runner.parse_jsonl(events, last)
        self.assertTrue(parsed["runner_ok"])
        self.assertEqual(parsed["in_tokens"], 100)
        self.assertEqual(parsed["cache_tokens"], 40)
        self.assertEqual(parsed["out_tokens"], 12)
        self.assertEqual(parsed["result_text"], "Done.")

    def test_stream_lag_warning_is_not_fatal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            events = root / "events.jsonl"
            last = root / "last.txt"
            rows = [
                {
                    "type": "item.completed",
                    "item": {
                        "type": "error",
                        "message": "in-process app-server event stream lagged; dropped 3 events",
                    },
                },
                {"type": "turn.completed", "usage": {"output_tokens": 1}},
            ]
            events.write_text(
                "\n".join(json.dumps(row) for row in rows) + "\n",
                encoding="utf-8",
            )
            last.write_text("OK\n", encoding="utf-8")
            parsed = self.runner.parse_jsonl(events, last)
        self.assertTrue(parsed["runner_ok"])
        self.assertEqual(len(parsed["runner_warnings"]), 1)
        self.assertEqual(parsed["runner_errors"], [])


if __name__ == "__main__":
    unittest.main()
