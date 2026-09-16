from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class TeamModeSkillContractTests(unittest.TestCase):
    def test_dispatch_contract_is_operational(self) -> None:
        skill = (ROOT / "skills" / "team-mode" / "SKILL.md").read_text(encoding="utf-8")
        for label in ("Outcome", "Benefit", "Sources", "Scope", "Checks", "Stop when", "Return"):
            with self.subTest(label=label):
                self.assertIn(f"`{label}`", skill)
        for label in ("Unresolved risk", "Evidence", "Checks already passed", "Do not repeat"):
            with self.subTest(label=label):
                self.assertIn(f"`{label}`", skill)
        self.assertIn("usable partial verdict", skill)
        self.assertIn("children never spawn descendants", skill)
        self.assertIn("request a partial verdict once, then interrupt it", skill)
        self.assertIn("`Executor`（Luna High）", skill)
        self.assertIn("Main thread: keep the critical slice", skill)
        self.assertIn("`Reviewer`（Terra Medium）", skill)
        self.assertNotIn("Complex Executor", skill)
        self.assertIn("执行检查点", skill)
        self.assertIn("一个或多个Executor", skill)
        self.assertIn("state the handoff", skill)
        self.assertIn("three independent lenses", skill)
        self.assertIn("references/interactive-testing.md", skill)

    def test_agent_type_dispatch_gate_is_explicit(self) -> None:
        skill = (ROOT / "skills" / "team-mode" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Dispatch Gate", skill)
        self.assertIn("Every `spawn_agent` call must explicitly pass `agent_type`", skill)
        self.assertIn("Never omit `agent_type` and never pass `default`", skill)
        self.assertIn("`default` profile is a fail-closed dispatch guard", skill)
        self.assertIn("only time Team Mode deliberately omits `agent_type`", skill)
        self.assertIn("## One-Time Onboarding", skill)
        self.assertIn("Do not inspect Agent files", skill)
        self.assertIn("skip onboarding without mentioning it", skill)

    def test_custom_agent_reference_matches_current_runtime_contract(self) -> None:
        reference = (ROOT / "skills" / "team-mode" / "references" / "custom-agents.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Current Codex releases enable subagent workflows by default", reference)
        self.assertIn("max_depth = 1", reference)
        self.assertIn("actual runtime trace", reference)
        self.assertIn("three working profiles plus one fail-closed `default` guard", reference)
        self.assertIn("gpt-5.6-terra", reference)
        self.assertIn("gpt-5.6-luna", reference)
        self.assertIn("## Run Onboarding Once", reference)
        self.assertIn("DISPATCH BLOCKED", reference)
        self.assertIn("## Explain How To Disable The Guard", reference)
        self.assertIn("~/.codex/agents-disabled/default.toml", reference)
        self.assertIn("Only when the parent is GPT-5.6 Sol", reference)
        self.assertIn("do not apply the workaround below", reference)
        self.assertNotIn("Complex Executor", reference)
        self.assertNotIn("features enable multi_agent_v2", reference)

    def test_interactive_testing_is_conditional_and_keeps_one_operator(self) -> None:
        reference = (
            ROOT / "skills" / "team-mode" / "references" / "interactive-testing.md"
        ).read_text(encoding="utf-8")
        self.assertIn("代码检查和自动化测试无法提供可信判断", reference)
        self.assertIn("同时只允许一个活动操作者", reference)
        self.assertIn("彼此隔离时，才并行执行", reference)
        self.assertIn("最终体验验收留在主线程", reference)

    def test_public_readmes_use_the_current_three_role_hero(self) -> None:
        for filename in ("README.md", "README.zh-CN.md"):
            with self.subTest(filename=filename):
                readme = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("./assets/readme/agent-map.webp", readme)
                self.assertNotIn("Complex Executor", readme)
                self.assertNotIn("Sol High", readme)
        self.assertTrue((ROOT / "assets" / "readme" / "agent-map.webp").is_file())
        self.assertFalse((ROOT / "assets" / "readme" / "agent-map.svg").exists())


if __name__ == "__main__":
    unittest.main()
