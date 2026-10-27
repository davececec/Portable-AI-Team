import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def capsule_module():
    spec = importlib.util.spec_from_file_location("capsule_agent_d", ROOT / "AI-Team" / "capsule.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_workspace(parent: Path, name: str) -> tuple[Path, Path]:
    project = parent / name
    project.mkdir(parents=True, exist_ok=True)
    capsule = project / "Portable-AI-Team"
    ignore = shutil.ignore_patterns("__pycache__", "memory-backup-20261010", "state")
    shutil.copytree(ROOT / "AI-Team", capsule / "AI-Team", ignore=ignore)
    (capsule / "Python路径.txt").write_text(str(Path(sys.executable).resolve()), encoding="utf-8")
    (project / "业务.txt").write_text("业务内容\n", encoding="utf-8")
    return project, capsule


def run_capsule(capsule: Path, command: str, *extra: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    return subprocess.run(
        [sys.executable, str(capsule / "AI-Team" / "capsule.py"), command, *extra],
        cwd=capsule,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="strict",
        env=environment,
    )


def run_team(team: Path, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    return subprocess.run(
        [sys.executable, str(team), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="strict",
        env=environment,
    )


class AgentDCapsuleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project, self.capsule = copy_workspace(Path(self.tmp.name), "中文 业务 项目")

    def tearDown(self):
        self.tmp.cleanup()

    def test_enable_validate_carry_move_and_enable_again(self):
        self.assertEqual((self.project / "业务.txt").read_text(encoding="utf-8"), "业务内容\n")
        enabled = run_capsule(self.capsule, "enable")
        self.assertEqual(enabled.returncode, 0, enabled.stdout + enabled.stderr)
        for relative in (
            ".codex/agents/agent-d.toml",
            ".agents/agents/agent-d/agent.md",
            ".trae/rules/portable-ai-team.md",
        ):
            self.assertTrue((self.project / relative).is_file(), relative)
        self.assertIn("portable-ai-team-agent-d", (self.project / ".agents/agents/agent-d/agent.md").read_text(encoding="utf-8"))
        self.assertIn("AgentD", (self.project / ".trae/rules/portable-ai-team.md").read_text(encoding="utf-8"))
        manifest = json.loads((self.capsule / "state" / "installation.json").read_text(encoding="utf-8"))
        self.assertIn(".codex/agents/agent-d.toml", [entry["path"] for entry in manifest["entries"]])
        status = json.loads((self.capsule / "团队状态.json").read_text(encoding="utf-8"))
        self.assertEqual(status["team_version"], "3.0.0")
        self.assertEqual(status["current_state"], "enabled")

        validated = run_capsule(self.capsule, "validate")
        self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)

        carried = run_capsule(self.capsule, "carry")
        self.assertEqual(carried.returncode, 0, carried.stdout + carried.stderr)
        self.assertFalse((self.project / ".codex/agents/agent-d.toml").exists())
        self.assertFalse((self.project / ".agents/agents/agent-d/agent.md").exists())
        self.assertTrue((self.project / "业务.txt").is_file())

        second = Path(self.tmp.name) / "第二个 中文 项目"
        second.mkdir()
        moved = second / "Portable-AI-Team"
        shutil.move(str(self.capsule), moved)
        again = run_capsule(moved, "enable")
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertTrue((second / ".codex/agents/agent-d.toml").is_file())
        self.assertEqual(run_capsule(moved, "carry").returncode, 0)

    def test_agent_d_conflicts_keep_user_files_and_parallel_paths(self):
        owned = {
            ".codex/agents/agent-d.toml": "用户 Codex D",
            ".agents/agents/agent-d/agent.md": "用户 Antigravity D",
            ".trae/rules/portable-ai-team.md": "用户 Trae 规则",
        }
        for relative, content in owned.items():
            path = self.project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        enabled = run_capsule(self.capsule, "enable")
        self.assertEqual(enabled.returncode, 0, enabled.stdout + enabled.stderr)
        self.assertIn("保留已有文件", enabled.stdout)
        for relative, content in owned.items():
            self.assertEqual((self.project / relative).read_text(encoding="utf-8"), content)

        parallel = (
            ".codex/agents/portable-ai-team-agent-d.toml",
            ".agents/agents/portable-ai-team-agent-d/agent.md",
            ".trae/rules/portable-ai-team-capsule.md",
        )
        for relative in parallel:
            self.assertTrue((self.project / relative).is_file(), relative)

        carried = run_capsule(self.capsule, "carry")
        self.assertEqual(carried.returncode, 0, carried.stdout + carried.stderr)
        for relative, content in owned.items():
            self.assertEqual((self.project / relative).read_text(encoding="utf-8"), content)
        for relative in parallel:
            self.assertFalse((self.project / relative).exists(), relative)

    def test_modified_agent_d_bridge_is_retained_on_carry(self):
        self.assertEqual(run_capsule(self.capsule, "enable").returncode, 0)
        bridge = self.project / ".codex/agents/agent-d.toml"
        bridge.write_text(bridge.read_text(encoding="utf-8") + "\n# 用户修改\n", encoding="utf-8")
        result = run_capsule(self.capsule, "carry")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("文件已被修改", result.stdout)
        self.assertTrue(bridge.is_file())
        self.assertIn("# 用户修改", bridge.read_text(encoding="utf-8"))

    def test_enabled_capsule_copy_is_blocked_without_touching_second_project(self):
        self.assertEqual(run_capsule(self.capsule, "enable").returncode, 0)
        second = Path(self.tmp.name) / "复制阻断项目"
        second.mkdir()
        copied = second / "Portable-AI-Team"
        shutil.copytree(self.capsule, copied)
        (second / "业务.txt").write_text("不受影响\n", encoding="utf-8")
        blocked = run_capsule(copied, "enable")
        self.assertEqual(blocked.returncode, 2, blocked.stdout + blocked.stderr)
        self.assertIn("先在原项目双击带走团队", blocked.stdout)
        self.assertFalse((second / "AGENTS.md").exists())
        self.assertEqual((second / "业务.txt").read_text(encoding="utf-8"), "不受影响\n")


class AgentDLegacyInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project, self.workspace = copy_workspace(Path(self.tmp.name), "旧式 中文 项目")
        shutil.copytree(self.workspace / "AI-Team", self.project / "AI-Team", dirs_exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_agent_d_install_conflict_validate_and_uninstall(self):
        self.assertEqual(
            run_team(
                ROOT / "AI-Team" / "team.py",
                "init", "--project", self.project, "--name", "示例",
                cwd=self.workspace,
            ).returncode,
            0,
        )
        owned = {
            ".codex/agents/agent-d.toml": "用户 Codex D",
            ".agents/agents/agent-d/agent.md": "用户 Antigravity D",
        }
        for relative, content in owned.items():
            path = self.project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        installed = run_team(
            ROOT / "AI-Team" / "team.py", "install", "--project", self.project,
            cwd=self.workspace,
        )
        self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
        parallel = {
            ".codex/agents/agent-d-ai-team.toml",
            ".agents/agents/agent-d-ai-team/agent.md",
        }
        for relative in parallel:
            self.assertTrue((self.project / relative).is_file(), relative)
        for relative, content in owned.items():
            self.assertEqual((self.project / relative).read_text(encoding="utf-8"), content)

        codex_data = tomllib.loads(
            (self.project / ".codex/agents/agent-d-ai-team.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(codex_data["name"], "agent-d-ai-team")
        validated = run_team(
            ROOT / "AI-Team" / "team.py", "validate", "--project", self.project,
            cwd=self.workspace,
        )
        self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)

        tampered = self.project / ".codex/agents/agent-d-ai-team.toml"
        tampered.write_text(tampered.read_text(encoding="utf-8") + "\n# 用户修改\n", encoding="utf-8")
        removed = run_team(ROOT / "AI-Team" / "team.py", "uninstall", "--project", self.project, cwd=self.workspace)
        self.assertEqual(removed.returncode, 0, removed.stdout + removed.stderr)
        report = json.loads(removed.stdout)
        kept = {Path(item).as_posix() for item in report["kept"]}
        self.assertIn(".codex/agents/agent-d-ai-team.toml", kept)
        self.assertTrue(tampered.is_file())
        self.assertFalse((self.project / ".agents/agents/agent-d-ai-team/agent.md").exists(), removed.stdout)
        for relative, content in owned.items():
            self.assertEqual((self.project / relative).read_text(encoding="utf-8"), content)


class MergeCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.module = capsule_module()
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def prepare_other(self, version: str | None) -> Path:
        other = Path(self.tmp.name) / "来源 空格项目" / "Portable-AI-Team"
        other.mkdir(parents=True, exist_ok=True)
        (other / "AI-Team").mkdir(parents=True, exist_ok=True)
        (other / "AI-Team" / "capsule.py").write_bytes((ROOT / "AI-Team" / "capsule.py").read_bytes())
        team = {"capsule_id": "legacy-source"}
        if version is not None:
            team["team_version"] = version
        (other / "AI-Team" / "team.json").write_text(
            json.dumps(team, ensure_ascii=False), encoding="utf-8"
        )
        return other

    def test_v23_and_later_versions_are_accepted(self):
        for version in ("2.3.0", "2.4.0", "3.0.0"):
            other = self.prepare_other(version)
            path, data = self.module.load_other_identity(str(other))
            self.assertEqual(data["team_version"], version)
            self.assertEqual(path, other.resolve())

    def test_old_missing_and_invalid_versions_are_rejected(self):
        cases = [("2.2.0", "团队版本不兼容"), (None, "缺少 team_version"), ("三.0.0", "团队版本无效")]
        for version, expected in cases:
            other = self.prepare_other(version)
            with self.assertRaises(ValueError) as context:
                self.module.load_other_identity(str(other))
            self.assertIn(expected, str(context.exception))


if __name__ == "__main__":
    unittest.main()
