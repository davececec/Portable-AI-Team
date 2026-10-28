import json
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_unique_json(path: Path) -> dict:
    def object_pairs_hook(pairs):
        keys = [key for key, _ in pairs]
        if len(keys) != len(set(keys)):
            duplicates = sorted({key for key in keys if keys.count(key) > 1})
            raise ValueError(f"重复 JSON 键: {', '.join(duplicates)}")
        return dict(pairs)

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=object_pairs_hook)


class ReleaseMetadataTests(unittest.TestCase):
    def test_version_is_unified_to_300(self):
        team = json.loads((ROOT / "AI-Team" / "team.json").read_text(encoding="utf-8"))
        team_py = (ROOT / "AI-Team" / "team.py").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        start = (ROOT / "START-HERE.md").read_text(encoding="utf-8")
        self.assertEqual(team["team_version"], "3.0.0")
        self.assertIn('TEAM_VERSION = "3.0.0"', team_py)
        self.assertIn("v3.0.0", readme)
        self.assertIn("v3.0.0", start)

    def test_local_status_card_version_matches_when_present(self):
        status_path = ROOT / "团队状态.json"
        if not status_path.is_file():
            self.skipTest("团队状态.json is machine-local; nothing to check in a fresh clone")
        status = json.loads(status_path.read_text(encoding="utf-8"))
        self.assertEqual(status["team_version"], "3.0.0")

    def test_status_card_and_team_json_capsule_ids_match(self):
        team = load_unique_json(ROOT / "AI-Team" / "team.json")
        status_path = ROOT / "团队状态.json"
        if not status_path.is_file():
            self.skipTest("团队状态.json is machine-local; nothing to check in a fresh clone")
        status = load_unique_json(status_path)
        self.assertEqual(status["capsule_id"], team["capsule_id"])
        self.assertEqual(status["capsule_id"], "portable-ai-team-20261010-v3")

    def test_agent_d_sources_and_bridges_are_registered(self):
        team_py = (ROOT / "AI-Team" / "team.py").read_text(encoding="utf-8")
        capsule_py = (ROOT / "AI-Team" / "capsule.py").read_text(encoding="utf-8")
        for phrase in (
            ".codex/agents/agent-d.toml",
            ".agents/agents/agent-d/agent.md",
        ):
            self.assertIn(phrase, team_py)
            self.assertIn(phrase, capsule_py)
        self.assertTrue((ROOT / "AI-Team/bridges/codex/agent-d.toml").is_file())
        self.assertTrue((ROOT / "AI-Team/bridges/antigravity/agent-d.md").is_file())
        self.assertTrue((ROOT / "AI-Team/adapters/trae/AgentD-import.md").is_file())
        with (ROOT / "AI-Team/bridges/codex/agent-d.toml").open("rb") as stream:
            data = tomllib.load(stream)
        self.assertEqual(data["name"], "agent-d")
        self.assertNotIn("model", data)

    def test_documents_describe_v3_features_without_real_keys(self):
        phrases = ("AgentD", "外部 API", "并行派单", "失败降级", "codex_builtin")
        checked = 0
        for name in ("README.md", "START-HERE.md", "PROGRESS.md"):
            path = ROOT / name
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in phrases:
                self.assertIn(phrase, text, f"{name}: {phrase}")
            self.assertNotIn("Bearer ", text)
            checked += 1
        self.assertGreaterEqual(checked, 1)

    def test_llm_config_has_only_structural_fields_checked(self):
        # Read only the expected structure, not the secret value.
        config_path = ROOT / "LLM配置.json"
        if not config_path.is_file():
            self.skipTest("LLM配置.json is a local-only config; nothing to check in a fresh clone")
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertIsInstance(config.get("enabled"), bool)
        self.assertIsInstance(config.get("models"), dict)
        self.assertIsInstance(config.get("routing"), dict)
        self.assertGreaterEqual(config.get("max_parallel"), 1)
        self.assertLessEqual(config.get("max_parallel"), 4)
        self.assertEqual(config.get("fallback"), "codex_builtin")
        self.assertGreater(config.get("timeout_seconds"), 0)
        # Deliberately do not inspect, copy, or print api_key.


if __name__ == "__main__":
    unittest.main()
