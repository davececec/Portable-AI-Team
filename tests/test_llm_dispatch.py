import importlib.util
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "AI-Team" / "llm_dispatch.py"


def load_module():
    spec = importlib.util.spec_from_file_location("llm_dispatch_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def api_payload(content: str = "修改: a.py\n测试: 通过\n") -> dict:
    return {"choices": [{"message": {"content": content}}]}


def base_config() -> dict:
    return {
        "enabled": True,
        "base_url": "https://dispatcher.invalid/v1",
        "api_key": "offline-stub-not-a-real-key",
        "models": {
            "fast": "stub-fast",
            "balanced": "stub-balanced",
        },
        "routing": {
            "implementation": "fast",
            "review": "balanced",
        },
        "fallback": "codex_builtin",
        "timeout_seconds": 0.01,
        "max_parallel": 2,
    }


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_missing_config_uses_builtin_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "不存在.json"
            self.assertEqual(
                self.module.load_config(missing),
                {"enabled": False, "fallback": "codex_builtin"},
            )

    def test_malformed_config_uses_builtin_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            broken = Path(tmp) / "配置.json"
            broken.write_text("{not-json", encoding="utf-8")
            self.assertEqual(
                self.module.load_config(broken),
                {"enabled": False, "fallback": "codex_builtin"},
            )

    def test_temp_config_loads_without_network_or_real_secret(self):
        config = base_config()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "配置.json"
            path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
            loaded = self.module.load_config(path)
        self.assertEqual(loaded["models"]["fast"], "stub-fast")
        self.assertEqual(self.module.validate_config(loaded), [])

    def test_structure_validation_reports_errors_without_secret(self):
        errors = self.module.validate_config({
            "enabled": "yes",
            "base_url": "ftp://bad.invalid",
            "models": {},
            "routing": {"bad": "missing"},
            "timeout_seconds": 0,
            "max_parallel": 9,
            "fallback": "",
        })
        joined = "\n".join(errors)
        for phrase in (
            "enabled 必须是布尔值",
            "models 必须是非空对象",
            "routing 中的每项必须指向",
            "base_url 必须以",
            "api_key 必须是非空字符串",
            "timeout_seconds 必须是正数",
            "max_parallel 必须是 1 到 4 的整数",
            "fallback 必须是非空字符串",
        ):
            self.assertIn(phrase, joined)
        self.assertNotIn("offline-stub-not-a-real-key", joined)


class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.config = base_config()

    def test_probe_model_uses_stubbed_http_response(self):
        captured = {}

        def fake_urlopen(request, timeout):
            captured["url"] = request.full_url
            captured["method"] = request.get_method()
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse(api_payload("OK"))

        with patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
            result = self.module.probe_model(self.config, "stub-fast")
        self.assertTrue(result["ok"])
        self.assertEqual(result["reply"], "OK")
        self.assertEqual(captured["url"], "https://dispatcher.invalid/v1/chat/completions")
        self.assertEqual(captured["method"], "POST")
        self.assertEqual(captured["body"]["model"], "stub-fast")

    def test_probe_failure_is_offline_and_compact(self):
        with patch.object(
            self.module.urllib.request,
            "urlopen",
            side_effect=urllib.error.URLError("offline stub"),
        ):
            result = self.module.probe_model(self.config, "stub-fast")
        self.assertFalse(result["ok"])
        self.assertIn("offline stub", result["error"])

    def test_test_mode_disabled_does_not_call_network(self):
        with patch.object(self.module, "probe_all") as probe:
            output = self.module.run_test_mode({"enabled": False, "fallback": "codex_builtin"})
        self.assertEqual(output["mode"], "codex_builtin")
        probe.assert_not_called()

    def test_test_mode_reports_partial_fallback(self):
        with patch.object(
            self.module,
            "probe_all",
            return_value={"stub-fast": {"ok": True}, "stub-balanced": {"ok": False}},
        ):
            output = self.module.run_test_mode(self.config)
        self.assertEqual(output["mode"], "partial_fallback")


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.config = base_config()

    def test_disabled_config_uses_builtin_fallback(self):
        result = self.module.dispatch_single({"enabled": False}, "fast", "离线任务")
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["mode"], "codex_builtin")

    def test_single_dispatch_sends_summary_prompt(self):
        captured = {}

        def fake_urlopen(request, timeout):
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse(api_payload("修改: a.py\n测试: 通过\n"))

        with patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
            result = self.module.dispatch_single(
                self.config,
                "fast",
                "修改一个函数",
                ["src/a.py", "tests/test_a.py"],
            )
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["model"], "stub-fast")
        self.assertIn("src/a.py", captured["body"]["messages"][1]["content"])
        self.assertEqual(captured["body"]["max_tokens"], 2000)

    def test_timeout_marks_error_and_builtin_fallback(self):
        with patch.object(self.module.urllib.request, "urlopen", side_effect=TimeoutError("stub timeout")):
            result = self.module.dispatch_single(self.config, "balanced", "任务")
        self.assertEqual(result["status"], "error")
        self.assertIn("stub timeout", result["error"])
        self.assertEqual(result["fallback"], "codex_builtin")

    def test_parallel_dispatch_returns_all_stubbed_results(self):
        payloads = {"stub-fast": api_payload("B 完成"), "stub-balanced": api_payload("D 完成")}

        def fake_urlopen(request, timeout):
            body = json.loads(request.data.decode("utf-8"))
            return FakeResponse(payloads[body["model"]])

        tasks = [
            {"role": "fast", "prompt": "B 模块"},
            {"role": "balanced", "prompt": "D 模块"},
        ]
        with patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
            results = self.module.dispatch_parallel(self.config, tasks)
        self.assertEqual(len(results), 2)
        self.assertEqual({item["model"] for item in results}, {"stub-fast", "stub-balanced"})

    def test_parallel_failure_does_not_hide_other_result(self):
        calls = 0

        def fake_urlopen(request, timeout):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise TimeoutError("one timed out")
            return FakeResponse(api_payload("另一个完成"))

        tasks = [
            {"role": "fast", "prompt": "任务 A"},
            {"role": "balanced", "prompt": "任务 B"},
        ]
        with patch.object(self.module.urllib.request, "urlopen", side_effect=fake_urlopen):
            results = self.module.dispatch_parallel(self.config, tasks)
        statuses = {item["status"] for item in results}
        self.assertEqual(statuses, {"ok", "error"})


if __name__ == "__main__":
    unittest.main()
