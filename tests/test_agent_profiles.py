from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROFILES = {
    "default.toml": ("default", "gpt-5.6-terra", "low", "read-only"),
    "Explorer.toml": ("Explorer", "gpt-5.6-luna", "medium", "read-only"),
    "Executor.toml": ("Executor", "gpt-5.6-luna", "high", "workspace-write"),
    "Reviewer.toml": ("Reviewer", "gpt-5.6-terra", "medium", "read-only"),
}


class AgentProfileTests(unittest.TestCase):
    def test_profile_boundaries_and_models_are_explicit(self) -> None:
        for filename, expected in PROFILES.items():
            with self.subTest(filename=filename):
                data = tomllib.loads((ROOT / "agents" / filename).read_text(encoding="utf-8"))
                actual = (
                    data["name"],
                    data["model"],
                    data["model_reasoning_effort"],
                    data["sandbox_mode"],
                )
                self.assertEqual(actual, expected)
                if filename != "default.toml":
                    self.assertIn(
                        "Do not spawn subagents; return evidence or blockers to the parent.",
                        data["developer_instructions"],
                    )

    def test_default_profile_fails_closed(self) -> None:
        data = tomllib.loads((ROOT / "agents" / "default.toml").read_text(encoding="utf-8"))
        instructions = data["developer_instructions"]
        self.assertIn("dispatch guard, not a working subagent", instructions)
        self.assertIn("Do not inspect files, call tools, spawn", instructions)
        self.assertIn("DISPATCH BLOCKED", instructions)
        self.assertIn("the delegated task was not executed", instructions)
        self.assertIn("agent_type was omitted or set to default", instructions)

    def test_executor_supports_substantial_bounded_work_without_overlapping_ownership(self) -> None:
        data = tomllib.loads((ROOT / "agents" / "Executor.toml").read_text(encoding="utf-8"))
        instructions = data["developer_instructions"]
        self.assertIn("routine or substantial implementation", instructions)
        self.assertIn("mutable-system ownership is explicit", instructions)
        self.assertIn("Never revert their changes", instructions)
        self.assertNotIn("Complex Executor", instructions)

    def test_executor_must_prove_named_checks_and_changed_behavior(self) -> None:
        data = tomllib.loads((ROOT / "agents" / "Executor.toml").read_text(encoding="utf-8"))
        instructions = data["developer_instructions"]
        self.assertIn("Treat every check named by the parent as required", instructions)
        self.assertIn("针对性测试", instructions)
        self.assertIn("效果尚未验证", instructions)
        self.assertIn("可恢复产物", instructions)

    def test_reviewer_is_bounded_by_the_review_packet(self) -> None:
        data = tomllib.loads((ROOT / "agents" / "Reviewer.toml").read_text(encoding="utf-8"))
        instructions = data["developer_instructions"]
        self.assertIn("passed checks, exclusions, and stop condition", instructions)
        self.assertIn("Do not repeat broad validation that already passed", instructions)
        self.assertIn("return a usable partial verdict immediately", instructions)
        self.assertIn("Simplify review lens", instructions)
        self.assertIn("Code quality", instructions)
        self.assertIn("Performance", instructions)
        self.assertIn("Reuse", instructions)
        self.assertIn("small behavior-preserving fixes", instructions)


if __name__ == "__main__":
    unittest.main()
