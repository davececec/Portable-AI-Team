"""Build and validate the Portable AI Team cross-IDE distribution."""
from __future__ import annotations

import argparse
import shutil
import sys
import tomllib
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_ROOT = PROJECT_ROOT / "dist"
DIST_DIR = DIST_ROOT / "Portable-AI-Team"
ZIP_PATH = DIST_ROOT / "Portable-AI-Team-Cross-IDE.zip"
TOP_LEVEL_FILES = ("START-HERE.md", "README.md", "requirements.txt", "Python路径.txt", "团队状态.json", "双击启用团队.cmd", "双击带走团队.cmd", "双击合并团队.cmd")
TOP_LEVEL_DIRS = ("AI-Team",)
EXCLUDED_PARTS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".git", "dist", "deliveries", "tasks", "state",
    "memory-backup-20261010", "merge-backups", "merge-inbox", "merge-reports",
}
ANTIGRAVITY_TOOLS = {"view_file", "replace_file_content", "grep_search", "run_command", "browser_subagent"}


def configure_utf8_io() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="strict")


def ignored(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDED_PARTS or name.endswith((".pyc", ".pyo"))}


def clean_destination() -> None:
    resolved_root = DIST_ROOT.resolve()
    resolved_dir = DIST_DIR.resolve()
    if resolved_dir.parent != resolved_root or resolved_dir.name != "Portable-AI-Team":
        raise RuntimeError("拒绝清理非预期分发目录")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()


def build_distribution() -> None:
    clean_destination()
    DIST_DIR.mkdir(parents=True)
    for relative in TOP_LEVEL_FILES:
        shutil.copy2(PROJECT_ROOT / relative, DIST_DIR / relative)
    for relative in TOP_LEVEL_DIRS:
        shutil.copytree(PROJECT_ROOT / relative, DIST_DIR / relative, ignore=ignored)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in DIST_DIR.rglob("*") if p.is_file()):
            archive.write(path, (Path(DIST_DIR.name) / path.relative_to(DIST_DIR)).as_posix())


def read_frontmatter(path: Path) -> tuple[dict[str, object], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: 缺少 YAML frontmatter 起始标记"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, [f"{path}: 缺少 YAML frontmatter 结束标记"]
    data: dict[str, object] = {}
    current_list: str | None = None
    for raw in lines[1:end]:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-") and current_list:
            value = line[1:].strip()
            cast = data.setdefault(current_list, [])
            if isinstance(cast, list):
                cast.append(value)
            continue
        if ":" not in line:
            errors.append(f"{path}: 无法解析 frontmatter 行: {line}")
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        if value:
            data[key] = value
            current_list = None
        else:
            data[key] = []
            current_list = key
    return data, errors


def require_text(path: Path, phrases: tuple[str, ...], errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"缺少文件: {path}")
        return
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in text:
            errors.append(f"{path}: 缺少关键内容 {phrase!r}")


def validate_designer(root: Path) -> list[str]:
    """Validate both deployable sources and their referenced capsule resources."""
    errors: list[str] = []
    for folder in ("adapters", "bridges"):
        for platform, relative in (("codex", "agent-c.toml"), ("antigravity", "agent-c.md")):
            path = root / "AI-Team" / folder / platform / relative
            if not path.is_file():
                errors.append(f"缺少 AgentC 配置: {path}")
                continue
            text = path.read_text(encoding="utf-8")
            if platform == "codex":
                try:
                    data = tomllib.loads(text)
                except tomllib.TOMLDecodeError as exc:
                    errors.append(f"{path}: TOML 解析失败: {exc}")
                    continue
                for key in ("name", "description", "developer_instructions"):
                    if not isinstance(data.get(key), str) or not data[key].strip():
                        errors.append(f"{path}: 缺少非空字段 {key}")
                if "model" in data:
                    errors.append(f"{path}: 不得绑定具体模型")
            else:
                data, parse_errors = read_frontmatter(path)
                errors.extend(parse_errors)
                if data.get("subagent") != "true" or not data.get("name") or not data.get("description"):
                    errors.append(f"{path}: 无效的 AgentC frontmatter")
                tools = data.get("tools")
                if not isinstance(tools, list) or not tools or set(tools) - ANTIGRAVITY_TOOLS:
                    errors.append(f"{path}: 无效工具列表")
            for reference in ("AI-Team/agents/AgentC.md", "AI-Team/policies/ui-routing.md"):
                expected = ("Portable-AI-Team/" if folder == "bridges" else "") + reference
                if f"`{expected}`" not in text or not (root / reference).is_file():
                    errors.append(f"{path}: 角色资料路径不可解析: {expected}")
            if folder == "bridges" and "{{PYTHON_PATH}}" not in text:
                errors.append(f"{path}: 缺少 Python 路径占位符")
            expected_name = "portable-ai-team-agent-c" if folder == "bridges" and platform == "antigravity" else "agent-c"
            if data.get("name") != expected_name:
                errors.append(f"{path}: AgentC name 必须为 {expected_name}")
    for relative in ("AI-Team/agents/AgentC.md", "AI-Team/policies/ui-routing.md",
                     "AI-Team/templates/design-spec.md", "AI-Team/templates/visual-review.md",
                     "AI-Team/adapters/trae/AgentC-import.md"):
        if not (root / relative).is_file():
            errors.append(f"缺少 AgentC 资料: {relative}")
    errors.extend(validate_agent_d(root))
    return errors


def validate_agent_d(root: Path) -> list[str]:
    """Validate AgentD adapter and bridge configurations."""
    errors: list[str] = []
    for folder in ("adapters", "bridges"):
        for platform, relative in (("codex", "agent-d.toml"), ("antigravity", "agent-d.md")):
            path = root / "AI-Team" / folder / platform / relative
            if not path.is_file():
                errors.append(f"缺少 AgentD 配置: {path}")
                continue
            text = path.read_text(encoding="utf-8")
            if platform == "codex":
                try:
                    data = tomllib.loads(text)
                except tomllib.TOMLDecodeError as exc:
                    errors.append(f"{path}: TOML 解析失败: {exc}")
                    continue
                for key in ("name", "description", "developer_instructions"):
                    if not isinstance(data.get(key), str) or not data[key].strip():
                        errors.append(f"{path}: 缺少非空字段 {key}")
                if "model" in data:
                    errors.append(f"{path}: 不得绑定具体模型")
            else:
                data, parse_errors = read_frontmatter(path)
                errors.extend(parse_errors)
                if data.get("subagent") != "true" or not data.get("name") or not data.get("description"):
                    errors.append(f"{path}: 无效的 AgentD frontmatter")
                tools = data.get("tools")
                if not isinstance(tools, list) or not tools or set(tools) - ANTIGRAVITY_TOOLS:
                    errors.append(f"{path}: 无效工具列表")

            reference = "AI-Team/agents/AgentD.md"
            expected_reference = ("Portable-AI-Team/" if folder == "bridges" else "") + reference
            if f"`{expected_reference}`" not in text or not (root / reference).is_file():
                errors.append(f"{path}: 角色资料路径不可解析: {expected_reference}")
            if folder == "bridges" and "{{PYTHON_PATH}}" not in text:
                errors.append(f"{path}: 缺少 Python 路径占位符")
            expected_name = "portable-ai-team-agent-d" if folder == "bridges" and platform == "antigravity" else "agent-d"
            if data.get("name") != expected_name:
                errors.append(f"{path}: AgentD name 必须为 {expected_name}")

    for relative in ("AI-Team/agents/AgentD.md", "AI-Team/adapters/trae/AgentD-import.md"):
        if not (root / relative).is_file():
            errors.append(f"缺少 AgentD 资料: {relative}")
    return errors


def validate_package(root: Path) -> list[str]:
    errors = validate_designer(root)
    for deployed, source in (
        (".codex/agents/agent-c.toml", "AI-Team/adapters/codex/agent-c.toml"),
        (".agents/agents/agent-c/agent.md", "AI-Team/adapters/antigravity/agent-c.md"),
        (".codex/agents/agent-d.toml", "AI-Team/adapters/codex/agent-d.toml"),
        (".agents/agents/agent-d/agent.md", "AI-Team/adapters/antigravity/agent-d.md"),
    ):
        path = root / deployed
        if not path.is_file() or not (root / source).is_file() or path.read_bytes() != (root / source).read_bytes():
            errors.append(f"AgentC 源平台配置未同步: {deployed}")
    codex = root / ".codex/agents/agent-b.toml"
    if not codex.is_file():
        errors.append(f"缺少 Codex AgentB: {codex}")
    else:
        try:
            data = tomllib.loads(codex.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, UnicodeError) as exc:
            errors.append(f"{codex}: TOML 解析失败: {exc}")
        else:
            for key in ("name", "description", "developer_instructions"):
                if not isinstance(data.get(key), str) or not data[key].strip():
                    errors.append(f"{codex}: 缺少非空字段 {key}")
            if "model" in data:
                errors.append(f"{codex}: 不得绑定具体模型")

    antigravity = root / ".agents/agents/agent-b/agent.md"
    if not antigravity.is_file():
        errors.append(f"缺少 Antigravity AgentB: {antigravity}")
    else:
        data, frontmatter_errors = read_frontmatter(antigravity)
        errors.extend(frontmatter_errors)
        if data.get("subagent") != "true":
            errors.append(f"{antigravity}: subagent 必须为 true")
        tools = data.get("tools")
        if not isinstance(tools, list) or not tools:
            errors.append(f"{antigravity}: tools 必须是非空列表")
        elif set(tools) - ANTIGRAVITY_TOOLS:
            errors.append(f"{antigravity}: 包含未确认的工具名 {sorted(set(tools) - ANTIGRAVITY_TOOLS)}")

    require_text(root / ".trae/rules/portable-ai-team.md", ("alwaysApply: true", "顺序降级", "完整聊天历史"), errors)
    require_text(root / "AGENTS.md", ("小A", "独立验收", "最多自动返工 2 轮", "干净上下文"), errors)
    require_text(root / ".agents/rules/portable-ai-team.md", ("小A", "独立验收", "最多自动返工 2 轮", "完整聊天历史"), errors)

    required = (
        "START-HERE.md",
        "AI-Team/agents/AgentA.md",
        "AI-Team/agents/AgentB.md",
        "AI-Team/agents/AgentD.md",
        "AI-Team/adapters/trae/AgentD-import.md",
        "AI-Team/policies/token-budget.md",
        "AI-Team/memory/index.md",
        "AI-Team/ide-guides/compatibility-matrix.md",
        "AI-Team/ide-guides/traecode.md",
        "AI-Team/adapters/trae/AgentA-import.md",
        "AI-Team/adapters/trae/AgentB-import.md",
        "AI-Team/check_compatibility.py",
    )
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"缺少公共团队文件: {relative}")
    return errors


def validate_capsule(root: Path) -> list[str]:
    errors = validate_designer(root)
    required = (
        "START-HERE.md",
        "README.md",
        "双击启用团队.cmd",
        "双击带走团队.cmd",
        "双击合并团队.cmd",
        "Python路径.txt",
        "团队状态.json",
        "AI-Team/capsule.py",
        "AI-Team/launch.ps1",
        "AI-Team/team.py",
        "AI-Team/check_compatibility.py",
        "AI-Team/bridges/codex/agent-b.toml",
        "AI-Team/bridges/codex/agent-d.toml",
        "AI-Team/bridges/antigravity/agent-d.md",
        "AI-Team/agents/AgentD.md",
        "AI-Team/adapters/trae/AgentD-import.md",
        "AI-Team/bridges/trae/portable-ai-team.md",
        "AI-Team/bridges/antigravity/portable-ai-team.md",
        "AI-Team/bridges/antigravity/agent-b.md",
        "AI-Team/agents/AgentA.md",
        "AI-Team/agents/AgentB.md",
        "AI-Team/memory/index.md",
    )
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"胶囊缺少文件: {relative}")
    for launcher in ("双击启用团队.cmd", "双击带走团队.cmd", "双击合并团队.cmd"):
        path = root / launcher
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if "D:\\00-python" in text or "D:/00-python" in text:
                errors.append(f"{launcher}: 不得依赖固定 Python 路径")
            if "powershell.exe" not in text or "launch.ps1" not in text:
                errors.append(f"{launcher}: 必须调用 Windows PowerShell 配置入口")
            if "python" in text.lower() or "where py" in text.lower():
                errors.append(f"{launcher}: 双击入口不得依赖 Python PATH")
    capsule_tool = root / "AI-Team/capsule.py"
    if capsule_tool.is_file():
        text = capsule_tool.read_text(encoding="utf-8")
        for phrase in ("installation.json", "portable-ai-team-capsule:start", "digest", "retained", "团队状态.json", "记忆账本.json", "merge-inbox"):
            if phrase not in text:
                errors.append(f"capsule.py 缺少安全约束: {phrase}")
    launcher_tool = root / "AI-Team/launch.ps1"
    if launcher_tool.is_file():
        text = launcher_tool.read_text(encoding="utf-8-sig")
        for phrase in ("Python路径.txt", "u202A", "IsPathRooted", "capsule.py", "--python"):
            if phrase not in text:
                errors.append(f"launch.ps1 缺少路径安全约束: {phrase}")
    config = root / "Python路径.txt"
    if config.is_file() and not config.read_text(encoding="utf-8-sig").strip():
        errors.append("Python路径.txt 不得为空")
    forbidden = ("AGENTS.md", ".codex", ".agents", ".trae")
    for relative in forbidden:
        if (root / relative).exists():
            errors.append(f"胶囊主体不应预先包含根桥接: {relative}")
    return errors


def distribution_files() -> dict[str, bytes]:
    return {
        path.relative_to(DIST_DIR).as_posix(): path.read_bytes()
        for path in DIST_DIR.rglob("*")
        if path.is_file()
    }


def validate_distribution() -> list[str]:
    errors: list[str] = []
    if not DIST_DIR.is_dir() or not ZIP_PATH.is_file():
        return ["分发目录或 ZIP 不完整；请运行 --build"]
    files = distribution_files()
    for name in files:
        parts = set(Path(name).parts)
        if parts & EXCLUDED_PARTS or name.endswith((".pyc", ".pyo")):
            errors.append(f"分发目录包含禁止项: {name}")
    try:
        with zipfile.ZipFile(ZIP_PATH) as archive:
            bad = archive.testzip()
            if bad:
                errors.append(f"ZIP 文件损坏: {bad}")
            zip_names = {name for name in archive.namelist() if not name.endswith("/")}
            expected = {f"{DIST_DIR.name}/{name}" for name in files}
            if zip_names != expected:
                errors.append("ZIP 文件清单与分发目录不一致")
            else:
                for name, content in files.items():
                    if archive.read(f"{DIST_DIR.name}/{name}") != content:
                        errors.append(f"ZIP 文件内容与分发目录不一致: {name}")
                        break
    except zipfile.BadZipFile as exc:
        errors.append(f"ZIP 无法打开: {exc}")
    errors.extend(validate_capsule(DIST_DIR))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="构建并检查 Portable AI Team 跨 IDE 分发包")
    parser.add_argument("--build", action="store_true", help="重建 dist 目录和 ZIP 后检查")
    args = parser.parse_args()
    if args.build:
        build_distribution()
    source_mode = (PROJECT_ROOT / ".codex/agents/agent-b.toml").is_file()
    errors = validate_package(PROJECT_ROOT) if source_mode else validate_capsule(PROJECT_ROOT)
    if args.build or DIST_DIR.exists() or ZIP_PATH.exists():
        errors.extend(validate_distribution())
    if errors:
        print("兼容性检查失败:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("兼容性检查通过")
    return 0


if __name__ == "__main__":
    configure_utf8_io()
    raise SystemExit(main())
