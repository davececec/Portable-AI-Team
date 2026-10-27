"""External LLM dispatcher for Portable AI Team.

Reads LLM配置.json, checks model availability, dispatches tasks to the best
model per role, and returns only summaries + file paths.  Falls back to
"codex_builtin" when API is unreachable.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "LLM配置.json"


def load_config(path: Path | None = None) -> dict:
    source = path or CONFIG_PATH
    if not source.exists():
        return {"enabled": False, "fallback": "codex_builtin"}
    try:
        return json.loads(source.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"enabled": False, "fallback": "codex_builtin"}


def validate_config(cfg: object) -> list[str]:
    """Return offline structural errors; never include secret values."""
    if not isinstance(cfg, dict):
        return ["LLM配置必须是 JSON 对象"]
    errors: list[str] = []
    enabled = cfg.get("enabled")
    if not isinstance(enabled, bool):
        errors.append("enabled 必须是布尔值")

    models = cfg.get("models")
    if not isinstance(models, dict) or not models:
        errors.append("models 必须是非空对象")
        models = {}
    else:
        for role, model in models.items():
            if not isinstance(role, str) or not role or not isinstance(model, str) or not model.strip():
                errors.append("models 中的角色和模型名必须是非空字符串")
                break

    routing = cfg.get("routing", {})
    if not isinstance(routing, dict):
        errors.append("routing 必须是对象")
    else:
        for name, role in routing.items():
            if not isinstance(name, str) or not name or not isinstance(role, str) or role not in models:
                errors.append("routing 中的每项必须指向 models 已定义的角色")
                break

    if enabled:
        base_url = cfg.get("base_url")
        if not isinstance(base_url, str) or base_url.strip() != base_url or not base_url.startswith(("http://", "https://")):
            errors.append("base_url 必须以 http:// 或 https:// 开头")
        api_key = cfg.get("api_key")
        if not isinstance(api_key, str) or not api_key.strip():
            errors.append("api_key 必须是非空字符串")

    timeout = cfg.get("timeout_seconds", 120)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
        errors.append("timeout_seconds 必须是正数")

    max_parallel = cfg.get("max_parallel", 3)
    if isinstance(max_parallel, bool) or not isinstance(max_parallel, int) or not 1 <= max_parallel <= 4:
        errors.append("max_parallel 必须是 1 到 4 的整数")

    fallback = cfg.get("fallback", "codex_builtin")
    if not isinstance(fallback, str) or not fallback.strip():
        errors.append("fallback 必须是非空字符串")
    return errors


def probe_model(cfg: dict, model_id: str) -> dict:
    """Send a minimal ping to check if a model responds."""
    url = cfg.get("base_url", "").rstrip("/") + "/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg.get('api_key', '')}",
    }
    body = json.dumps({
        "model": model_id,
        "messages": [{"role": "user", "content": "回复OK"}],
        "max_tokens": 5,
    }).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {"model": model_id, "ok": True, "reply": data["choices"][0]["message"]["content"]}
    except Exception as exc:
        return {"model": model_id, "ok": False, "error": str(exc)[:200]}


def probe_all(cfg: dict) -> dict:
    results = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(probe_model, cfg, model_id): model_id
            for model_id in cfg.get("models", {}).values()
        }
        for future in as_completed(futures):
            result = future.result()
            results[result["model"]] = {
                "ok": result["ok"],
                "reply": result.get("reply", result.get("error", "")),
            }
    return results


def run_test_mode(cfg: dict) -> dict:
    """Offline-testable implementation of the --test output."""
    if not cfg.get("enabled"):
        return {"mode": "codex_builtin", "reason": "LLM配置 disabled or missing"}
    results = probe_all(cfg)
    all_ok = all(item["ok"] for item in results.values())
    return {"mode": "external_api" if all_ok else "partial_fallback", "results": results}


def dispatch_single(cfg: dict, role: str, prompt: str, context_files: list[str] | None = None) -> dict:
    """Send a task to the model assigned to the given role. Returns summary only."""
    if not cfg.get("enabled"):
        return {"status": "fallback", "role": role, "mode": "codex_builtin"}

    models = cfg.get("models", {})
    model_id = models.get(role) or models.get("fast") or next(iter(models.values()), None)
    if not model_id:
        return {"status": "no_model", "role": role, "fallback": cfg.get("fallback", "codex_builtin")}

    system = (
        "你是 Portable AI Team 的执行者。只返回：修改了哪些文件、测试结果、遗留风险。"
        "不要输出完整代码文件内容，只返回摘要。"
    )
    user_parts = [prompt]
    if context_files:
        user_parts.append("相关文件：" + ", ".join(context_files))

    url = cfg.get("base_url", "").rstrip("/") + "/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg.get('api_key', '')}",
    }
    body = json.dumps({
        "model": model_id,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": "\n".join(user_parts)},
        ],
        "max_tokens": 2000,
    }).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    timeout = cfg.get("timeout_seconds", 120)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            reply = data["choices"][0]["message"]["content"]
            return {"status": "ok", "role": role, "model": model_id, "summary": reply}
    except Exception as exc:
        return {
            "status": "error",
            "role": role,
            "model": model_id,
            "error": str(exc)[:500],
            "fallback": cfg.get("fallback", "codex_builtin"),
        }


def dispatch_parallel(cfg: dict, tasks: list[dict]) -> list[dict]:
    """Dispatch multiple tasks in parallel. Each task: {role, prompt, files?}."""
    if not isinstance(tasks, list):
        raise TypeError("tasks 必须是列表")
    max_parallel = min(int(cfg.get("max_parallel", 3)), len(tasks))
    if max_parallel <= 0:
        return []
    results = []
    with ThreadPoolExecutor(max_workers=max_parallel) as pool:
        futures = {
            pool.submit(dispatch_single, cfg, task["role"], task["prompt"], task.get("files")): task
            for task in tasks
        }
        for future in as_completed(futures):
            results.append(future.result())
    return results


def main():
    args = sys.argv[1:]
    cfg = load_config()

    if "--test" in args:
        print(json.dumps(run_test_mode(cfg), ensure_ascii=False, indent=2))
    elif "--dispatch" in args:
        role = _argument_value(args, "--role", "fast")
        prompt = _argument_value(args, "--prompt", "")
        files_value = _argument_value(args, "--files", None)
        files = files_value.split(",") if files_value else None
        result = dispatch_single(cfg, role, prompt, files)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif "--dispatch-parallel" in args:
        tasks_file = _argument_value(args, "--tasks", "tasks.json")
        tasks = json.loads(Path(tasks_file).read_text(encoding="utf-8"))
        print(json.dumps(dispatch_parallel(cfg, tasks), ensure_ascii=False, indent=2))
    else:
        output = {
            "available_models": list(cfg.get("models", {}).values()),
            "mode": cfg.get("fallback", "codex_builtin"),
        }
        print(json.dumps(output, ensure_ascii=False))


def _argument_value(args: list[str], name: str, default: str | None) -> str | None:
    if name not in args:
        return default
    index = args.index(name) + 1
    return args[index] if index < len(args) else default


if __name__ == "__main__":
    main()
