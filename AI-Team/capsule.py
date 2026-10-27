"""Enable, validate, carry away, and merge a Portable AI Team capsule."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


MARKER = "portable-ai-team-capsule-v1"
BLOCK_START = "<!-- portable-ai-team-capsule:start -->"
BLOCK_END = "<!-- portable-ai-team-capsule:end -->"
CAPSULE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = CAPSULE_ROOT.parent
STATE_DIR = CAPSULE_ROOT / "state"
MANIFEST_PATH = STATE_DIR / "installation.json"
LAST_REPORT_PATH = STATE_DIR / "last-operation.json"
TEAM_PATH = CAPSULE_ROOT / "AI-Team" / "team.json"
STATUS_PATH = CAPSULE_ROOT / "团队状态.json"
MEMORY_DIR = CAPSULE_ROOT / "AI-Team" / "memory"
LEDGER_PATH = MEMORY_DIR / "记忆账本.json"
MEMORY_STATE_PATH = STATE_DIR / "memory.json"
BRIDGES = (
    ("codex-agent", ".codex/agents/agent-b.toml", "bridges/codex/agent-b.toml"),
    ("codex-agent", ".codex/agents/agent-c.toml", "bridges/codex/agent-c.toml"),
    ("codex-agent", ".codex/agents/agent-d.toml", "bridges/codex/agent-d.toml"),
    ("trae-rule", ".trae/rules/portable-ai-team.md", "bridges/trae/portable-ai-team.md"),
    ("antigravity-rule", ".agents/rules/portable-ai-team.md", "bridges/antigravity/portable-ai-team.md"),
    ("antigravity-agent", ".agents/agents/agent-b/agent.md", "bridges/antigravity/agent-b.md"),
    ("antigravity-agent", ".agents/agents/agent-c/agent.md", "bridges/antigravity/agent-c.md"),
    ("antigravity-agent", ".agents/agents/agent-d/agent.md", "bridges/antigravity/agent-d.md"),
)
INVISIBLE_CONTROLS = dict.fromkeys(map(ord, "\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069\ufeff"))
QUOTE_PAIRS = (("\"", "\""), ("'", "'"), ("“", "”"), ("‘", "’"))
MINIMUM_MERGE_VERSION = (2, 3, 0)


def configure_utf8_io() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="strict")


def digest_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def load_json(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def save_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def iso_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def normalize_python_path(value: str) -> Path:
    candidate = value.translate(INVISIBLE_CONTROLS).strip()
    for opening, closing in QUOTE_PAIRS:
        if len(candidate) >= 2 and candidate.startswith(opening) and candidate.endswith(closing):
            candidate = candidate[len(opening):-len(closing)].strip()
            break
    path = Path(candidate)
    if not path.is_absolute():
        raise ValueError("Python 路径必须是绝对路径")
    path = path.resolve()
    if not path.is_file():
        raise ValueError(f"Python 路径不存在: {path}")
    return path


def configured_python_path(value: str | None = None) -> Path:
    if value is not None:
        return normalize_python_path(value)
    config = CAPSULE_ROOT / "Python路径.txt"
    if not config.is_file():
        raise ValueError("缺少 Python路径.txt")
    for line in config.read_text(encoding="utf-8-sig").splitlines():
        cleaned = line.translate(INVISIBLE_CONTROLS).strip()
        if cleaned:
            return normalize_python_path(cleaned)
    raise ValueError("Python路径.txt 中没有有效路径")


def bridge_source(relative: str, python_path: Path) -> bytes:
    text = (Path(__file__).resolve().parent / relative).read_text(encoding="utf-8")
    value = str(python_path)
    if relative.endswith(".toml"):
        value = value.replace("\\", "\\\\")
    return text.replace("{{PYTHON_PATH}}", value).encode("utf-8")


def agents_block(python_path: Path) -> bytes:
    content = (
        f"{BLOCK_START}\n"
        "# Portable AI Team 桥接\n\n"
        "团队主体位于 `Portable-AI-Team/`。用户说“ZH，给我做一个……”时，"
        "请读取 `Portable-AI-Team/AI-Team/agents/AgentA.md`、相关策略与记忆索引。"
        "AgentA 通过根平台桥接委派 AgentB，并在返回后独立验收；最多自动返工 2 轮。\n"
        "新建主要界面、整体改版或明确美化时，按团队 `policies/ui-routing.md` 按需委派 AgentC 设计和视觉检查；纯后台及文字/颜色小改默认跳过 C。无子智能体时明确报告角色顺序模拟，不声称独立 C 或干净上下文隔离。\n"
        f"本项目默认 Python 解释器：`{python_path}`。AgentB 运行 Python、安装依赖和测试时优先使用该绝对路径。\n"
        "用户提出项目完成或准备带走团队时，AgentA 必须先把新且稳定的可复用经验压缩归纳到胶囊记忆，再提示双击带走；禁止收纳业务源码、密钥、原始日志、构建产物或项目依赖。\n"
        f"{BLOCK_END}\n"
    )
    return content.encode("utf-8")


def add_created_parents(target: Path, created_dirs: list[str]) -> None:
    missing: list[Path] = []
    parent = target.parent
    while parent != PROJECT_ROOT and not parent.exists():
        missing.append(parent)
        parent = parent.parent
    target.parent.mkdir(parents=True, exist_ok=True)
    for directory in reversed(missing):
        relative = directory.relative_to(PROJECT_ROOT).as_posix()
        if relative not in created_dirs:
            created_dirs.append(relative)


def alternative_target(kind: str, target: Path, number: int = 1) -> Path:
    suffix = "" if number == 1 else f"-{number}"
    if kind == "codex-agent":
        return target.with_name(f"portable-ai-team-{target.stem}{suffix}.toml")
    if kind in {"trae-rule", "antigravity-rule"}:
        return target.with_name(f"portable-ai-team-capsule{suffix}.md")
    if kind == "antigravity-agent":
        return target.parent.parent / f"portable-ai-team-{target.parent.name}{suffix}" / "agent.md"
    raise ValueError(kind)


def choose_target(kind: str, target: Path, source: bytes, conflicts: list[str]) -> Path:
    if not target.exists():
        return target
    if target.is_file() and digest(target) == digest_bytes(source) and MARKER.encode() in source:
        return target
    conflicts.append(f"保留已有文件: {target.relative_to(PROJECT_ROOT).as_posix()}")
    number = 1
    while True:
        candidate = alternative_target(kind, target, number)
        if not candidate.exists():
            return candidate
        if candidate.is_file() and digest(candidate) == digest_bytes(source):
            return candidate
        conflicts.append(f"保留已有文件: {candidate.relative_to(PROJECT_ROOT).as_posix()}")
        number += 1


def load_team_data() -> dict:
    data = load_json(TEAM_PATH)
    if not isinstance(data, dict) or not data.get("team_version"):
        raise ValueError("AI-Team/team.json 缺失或无效")
    return data


def capsule_id() -> str:
    value = load_team_data().get("capsule_id")
    if not value:
        raise ValueError("AI-Team/team.json 缺少 capsule_id")
    return str(value)


def memory_file_map() -> dict[str, str]:
    result: dict[str, str] = {}
    if not MEMORY_DIR.exists():
        return result
    root = MEMORY_DIR.resolve()
    for path in sorted(p for p in MEMORY_DIR.rglob("*") if p.is_file() and p.suffix.lower() == ".md"):
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            continue
        relative = path.relative_to(MEMORY_DIR).as_posix()
        if relative == "merge-inbox" or relative.startswith("merge-inbox/"):
            continue
        result[relative] = digest(path)
    return result


def memory_fingerprint(files: dict[str, str]) -> str:
    payload = json.dumps(files, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return digest_bytes(payload)


def refresh_memory_state() -> tuple[dict, list[str]]:
    # state/ is disposable; the ledger travels with memory.
    files = memory_file_map()
    fingerprint = memory_fingerprint(files)
    previous = load_json(MEMORY_STATE_PATH) or {}
    ledger = load_json(LEDGER_PATH) or {}
    fallback = max(
        (int(record.get("memory_revision", 0)) for record in ledger.get("records", []) if isinstance(record, dict)),
        default=0,
    )
    previous_revision = int(previous.get("memory_revision") or fallback or 0)
    if previous.get("memory_hash") == fingerprint and previous_revision:
        state = dict(previous)
        state["files"] = files
        changed: list[str] = []
    else:
        previous_files = previous.get("files") or {}
        changed = sorted(
            [name for name, digest_value in files.items() if previous_files.get(name) != digest_value]
            + sorted(set(previous_files) - set(files))
        )
        revision = previous_revision + 1
        state = {
            "memory_revision": revision,
            "memory_hash": fingerprint,
            "updated_at": iso_now(),
            "files": files,
        }
        save_json(MEMORY_STATE_PATH, state)
    state["memory_revision"] = int(state["memory_revision"])
    state["memory_hash"] = str(state["memory_hash"])
    return state, changed


def state_description(code: str) -> str:
    return {
        "enabled": "团队已启用，IDE 桥接生效",
        "carried": "团队已带走，可安全移动",
        "retained_modified": "团队已带走；用户修改过的桥接已保留",
        "blocked": "操作已阻止，请先处理原项目",
        "retained": "团队未启用，可安全移动",
    }.get(code, code)


def update_status(
    state: dict,
    current_state: str,
    project: Path | None = None,
    carry_time: str | None = None,
) -> dict:
    team = load_team_data()
    old = load_json(STATUS_PATH) or {}
    recent = [str(item) for item in old.get("recent_projects", []) if item]
    project_text = str(project.resolve()) if project is not None else None
    if project_text:
        recent = [project_text] + [item for item in recent if item != project_text]
    card = {
        "schema_version": 1,
        "team_version": team["team_version"],
        "capsule_id": team.get("capsule_id"),
        "memory_version": int(state.get("memory_revision", 0)),
        "memory_revision": int(state.get("memory_revision", 0)),
        "memory_hash": state.get("memory_hash"),
        "created_at": old.get("created_at") or f"{team.get('created', '1970-01-01')}T00:00:00",
        "updated_at": iso_now(),
        "current_state": current_state,
        "state_description": state_description(current_state),
        "current_project": None if current_state in {"carried", "retained_modified"} else project_text,
        "recent_projects": recent[:10],
        "recent_carry_time": carry_time or old.get("recent_carry_time"),
    }
    save_json(STATUS_PATH, card)
    return card


def append_carry_record(project: Path, state: dict, changed: list[str], status: str) -> None:
    ledger = load_json(LEDGER_PATH) or {"schema_version": 1, "capsule_id": capsule_id(), "records": []}
    if not isinstance(ledger, dict) or not isinstance(ledger.get("records"), list):
        raise ValueError("记忆账本无效，请人工检查 AI-Team/memory/记忆账本.json")
    ledger["schema_version"] = 1
    ledger["capsule_id"] = capsule_id()
    ledger["records"].append(
        {
            "carried_at": iso_now(),
            "project": str(project.resolve()),
            "status": status,
            "memory_revision": int(state["memory_revision"]),
            "memory_hash": state["memory_hash"],
            "changed_files": changed,
            "source_capsule_id": capsule_id(),
        }
    )
    save_json(LEDGER_PATH, ledger)


def enable_capsule(python_path: Path) -> tuple[int, dict]:
    old = load_json(MANIFEST_PATH)
    memory_state, memory_changed = refresh_memory_state()
    if old:
        old_project = Path(old.get("project_root", "")).resolve()
        if old_project == PROJECT_ROOT.resolve():
            update_status(memory_state, "enabled", old_project)
            report = {"operation": "enable", "status": "already_enabled", "created": [], "merged": [], "retained": [], "conflicts": [], "memory_changed": memory_changed}
            save_json(LAST_REPORT_PATH, report)
            return 0, report
        update_status(memory_state, "blocked", old_project)
        report = {"operation": "enable", "status": "blocked", "created": [], "merged": [], "retained": [], "conflicts": ["胶囊仍记录为在其他项目启用，请先在原项目双击带走团队"], "memory_changed": memory_changed}
        save_json(LAST_REPORT_PATH, report)
        return 2, report

    created_dirs: list[str] = []
    entries: list[dict] = []
    created: list[str] = []
    merged: list[str] = []
    conflicts: list[str] = []
    agents = PROJECT_ROOT / "AGENTS.md"
    block = agents_block(python_path)
    if agents.exists():
        original = agents.read_bytes()
        if BLOCK_START.encode() in original or BLOCK_END.encode() in original:
            report = {"operation": "enable", "status": "blocked", "created": created, "merged": merged, "retained": [], "conflicts": ["AGENTS.md 已含不受当前清单管理的团队标记区块，请先人工检查"], "memory_changed": memory_changed}
            save_json(LAST_REPORT_PATH, report)
            return 2, report
        separator = b"\n" if original.endswith((b"\n", b"\r")) else b"\n\n"
        appended = separator + block
        agents.write_bytes(original + appended)
        entries.append({"kind": "agents-block", "path": "AGENTS.md", "mode": "block", "block": base64.b64encode(appended).decode("ascii")})
        merged.append("AGENTS.md（追加可逆标记区块）")
    else:
        agents.write_bytes(block)
        entries.append({"kind": "agents-block", "path": "AGENTS.md", "mode": "file", "digest": digest(agents)})
        created.append("AGENTS.md")

    for kind, relative, source_relative in BRIDGES:
        source = bridge_source(source_relative, python_path)
        target = choose_target(kind, PROJECT_ROOT / relative, source, conflicts)
        if target != PROJECT_ROOT / relative and kind in {"codex-agent", "antigravity-agent"}:
            # The IDE identifies agents by name, not only by their file paths.
            if kind == "codex-agent":
                source = source.replace(f'name = "{Path(relative).stem}"'.encode(), f'name = "{target.stem}"'.encode())
            else:
                source = source.replace(f"name: portable-ai-team-{Path(relative).parent.name}".encode(), f"name: {target.parent.name}".encode())
        add_created_parents(target, created_dirs)
        if not target.exists():
            target.write_bytes(source)
            created.append(target.relative_to(PROJECT_ROOT).as_posix())
        entries.append({"kind": kind, "path": target.relative_to(PROJECT_ROOT).as_posix(), "mode": "file", "digest": digest(target)})

    manifest = {
        "marker": MARKER,
        "project_root": str(PROJECT_ROOT.resolve()),
        "capsule_root": str(CAPSULE_ROOT.resolve()),
        "enabled_at": iso_now(),
        "python_path": str(python_path),
        "entries": entries,
        "created_dirs": created_dirs,
    }
    save_json(MANIFEST_PATH, manifest)
    report = {"operation": "enable", "status": "enabled", "created": created, "merged": merged, "retained": [], "conflicts": conflicts, "memory_changed": memory_changed}
    save_json(LAST_REPORT_PATH, report)
    update_status(memory_state, "enabled", PROJECT_ROOT)
    return 0, report


def carry_capsule() -> tuple[int, dict]:
    manifest = load_json(MANIFEST_PATH)
    memory_state, memory_changed = refresh_memory_state()
    if not manifest:
        update_status(memory_state, "retained")
        report = {"operation": "carry", "status": "not_enabled", "removed": [], "retained": [], "conflicts": [], "memory_changed": memory_changed}
        save_json(LAST_REPORT_PATH, report)
        return 0, report
    enabled_project = Path(manifest.get("project_root", "")).resolve()
    if enabled_project != PROJECT_ROOT.resolve():
        update_status(memory_state, "blocked", enabled_project)
        report = {"operation": "carry", "status": "blocked", "removed": [], "retained": [], "conflicts": ["胶囊位置与启用项目不一致，请放回原项目后再带走"], "memory_changed": memory_changed}
        save_json(LAST_REPORT_PATH, report)
        return 2, report

    removed: list[str] = []
    retained: list[str] = []
    remaining: list[dict] = []
    for entry in manifest.get("entries", []):
        target = PROJECT_ROOT / entry["path"]
        if not target.exists():
            removed.append(entry["path"] + "（已不存在）")
            continue
        if entry["mode"] == "block":
            block = base64.b64decode(entry["block"])
            content = target.read_bytes()
            if content.count(block) == 1:
                target.write_bytes(content.replace(block, b"", 1))
                removed.append(entry["path"] + " 中的团队区块")
            else:
                retained.append(entry["path"] + "（团队区块已被修改）")
                remaining.append(entry)
        elif digest(target) == entry["digest"]:
            target.unlink()
            removed.append(entry["path"])
        else:
            retained.append(entry["path"] + "（文件已被修改）")
            remaining.append(entry)

    for relative in sorted(manifest.get("created_dirs", []), key=lambda value: len(Path(value).parts), reverse=True):
        directory = PROJECT_ROOT / relative
        if directory.exists() and directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()

    if remaining:
        manifest["entries"] = remaining
        save_json(MANIFEST_PATH, manifest)
        status = "retained_modified"
    else:
        MANIFEST_PATH.unlink(missing_ok=True)
        status = "carried"
    append_carry_record(enabled_project, memory_state, memory_changed, status)
    report = {"operation": "carry", "status": status, "removed": removed, "retained": retained, "conflicts": [], "memory_changed": memory_changed}
    save_json(LAST_REPORT_PATH, report)
    update_status(memory_state, status, project=enabled_project, carry_time=iso_now())
    return 0, report


def validate_capsule() -> tuple[int, dict]:
    manifest = load_json(MANIFEST_PATH)
    errors: list[str] = []
    if not manifest:
        errors.append("团队尚未启用")
    else:
        for entry in manifest.get("entries", []):
            target = PROJECT_ROOT / entry["path"]
            if not target.exists():
                errors.append(f"桥接缺失: {entry['path']}")
            elif entry["mode"] == "file" and digest(target) != entry["digest"]:
                errors.append(f"桥接已修改: {entry['path']}")
            elif entry["mode"] == "block" and base64.b64decode(entry["block"]) not in target.read_bytes():
                errors.append("AGENTS.md 团队区块已修改")
    return (1 if errors else 0), {"operation": "validate", "status": "failed" if errors else "valid", "errors": errors}


def version_tuple(value: str) -> tuple[int, int, int]:
    parts = value.split(".")
    if len(parts) < 2 or not all(part.isdigit() for part in parts[:3]):
        raise ValueError("团队版本无效")
    padded = parts + ["0"] * (3 - len(parts))
    return tuple(int(part) for part in padded[:3])


def load_other_identity(other_value: str) -> tuple[Path, dict]:
    other = Path(other_value).expanduser().resolve()
    if not other.is_dir():
        raise ValueError(f"待合并胶囊不存在或不是文件夹: {other}")
    team_path = other / "AI-Team" / "team.json"
    capsule_tool = other / "AI-Team" / "capsule.py"
    if not team_path.is_file() or not capsule_tool.is_file():
        raise ValueError("待合并对象不是 Portable AI Team 胶囊")
    try:
        data = load_json(team_path) or {}
    except json.JSONDecodeError as exc:
        raise ValueError("待合并胶囊 team.json 无法解析") from exc
    version = data.get("team_version")
    if not isinstance(version, str):
        raise ValueError("待合并胶囊缺少 team_version")
    other_version = version_tuple(version)
    if other_version < MINIMUM_MERGE_VERSION:
        raise ValueError(f"团队版本不兼容: {version}（当前支持 v2.3+）")
    return other, data


def safe_memory_files(memory_dir: Path) -> list[tuple[Path, str]]:
    if not memory_dir.exists():
        return []
    root = memory_dir.resolve()
    result: list[tuple[Path, str]] = []
    for path in sorted(p for p in memory_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".md"):
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f"记忆目录包含不安全链接: {path}")
        relative = path.relative_to(memory_dir).as_posix()
        if relative == "merge-inbox" or relative.startswith("merge-inbox/"):
            continue
        result.append((path, relative))
    return result


def conflict_already_staged(relative: str, content: bytes) -> bool:
    inbox = MEMORY_DIR / "merge-inbox"
    if not inbox.exists():
        return False
    for candidate in inbox.rglob("*"):
        if not candidate.is_file() or not candidate.name.endswith(Path(relative).name):
            continue
        if candidate.is_file() and candidate.read_bytes() == content:
            return True
    return False


def safe_target_path(relative: str) -> Path:
    target = MEMORY_DIR / relative
    resolved = target.resolve()
    if not resolved.is_relative_to(MEMORY_DIR.resolve()) or target.is_symlink():
        raise ValueError(f"合并目标越界: {relative}")
    return target


def write_merge_review(operations: list[dict], other_id: str) -> Path:
    review_dir = MEMORY_DIR / "merge-inbox"
    review_dir.mkdir(parents=True, exist_ok=True)
    review_path = review_dir / "merge-review.md"
    lines = [
        "# 团队记忆合并审查",
        "",
        f"- 合并来源胶囊 ID：{other_id}",
        f"- 生成时间：{iso_now()}",
        "",
        "同名记忆内容不同，当前文件未被覆盖。请逐项选择保留或合并内容。",
        "",
        "| 记忆文件 | 当前文件 | 来源文件 |",
        "| --- | --- | --- |",
    ]
    for operation in operations:
        lines.append(f"| `{operation['relative']}` | `{operation['destination']}` | `{operation['source']}` |")
    lines.extend(["", "处理完成后，可将选定内容写回对应记忆文件；来源文件保留在 merge-inbox 中。", ""])
    review_path.write_text("\n".join(lines), encoding="utf-8")
    return review_path


def merge_capsule(other_value: str) -> tuple[int, dict]:
    other, other_team = load_other_identity(other_value)
    self_id = capsule_id()
    if other.resolve() == CAPSULE_ROOT.resolve():
        raise ValueError("不能自我合并同一胶囊；请使用另一份独立的 Portable AI Team")
    other_id = str(other_team.get("capsule_id") or f"legacy-{other.name}")
    if MANIFEST_PATH.exists():
        raise ValueError("当前胶囊仍处于启用状态，请先双击带走后再合并")
    if (other / "state" / "installation.json").exists():
        raise ValueError("来源胶囊仍处于启用状态，请先在原项目带走后再合并")

    other_memory = other / "AI-Team" / "memory"
    other_ledger = other / "AI-Team" / "memory" / "记忆账本.json"
    source_files = safe_memory_files(other_memory)
    other_ledger_data = load_json(other_ledger) or {"schema_version": 1, "records": []}
    if not isinstance(other_ledger_data, dict) or not isinstance(other_ledger_data.get("records"), list):
        raise ValueError("来源记忆账本无效")
    if other_ledger_data.get("schema_version", 1) != 1:
        raise ValueError("来源记忆账本 schema 不兼容")

    copied: list[str] = []
    conflicts: list[str] = []
    unchanged: list[str] = []
    operations: list[dict] = []
    for source, relative in source_files:
        target = safe_target_path(relative)
        content = source.read_bytes()
        if target.exists():
            if digest_bytes(content) == digest(target):
                unchanged.append(relative)
                continue
            if conflict_already_staged(relative, content):
                unchanged.append(relative + "（冲突已在 merge-inbox）")
                continue
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            inbox_target = MEMORY_DIR / "merge-inbox" / f"{timestamp}-{relative}"
            operations.append({
                "relative": relative,
                "destination": target,
                "source": source,
                "inbox": inbox_target,
            })
            conflicts.append(relative)
        else:
            copied.append(relative)

    current_ledger = load_json(LEDGER_PATH) or {"schema_version": 1, "capsule_id": self_id, "records": []}
    if not isinstance(current_ledger, dict) or not isinstance(current_ledger.get("records"), list):
        raise ValueError("当前记忆账本无效")
    known_records = {
        json.dumps(record, ensure_ascii=False, sort_keys=True)
        for record in current_ledger["records"]
        if isinstance(record, dict)
    }
    ledger_imported: list[str] = []
    for record in other_ledger_data["records"]:
        if not isinstance(record, dict):
            continue
        normalized = dict(record)
        normalized.setdefault("source_capsule_id", other_id)
        serialized = json.dumps(normalized, ensure_ascii=False, sort_keys=True)
        if serialized not in known_records:
            known_records.add(serialized)
            current_ledger["records"].append(normalized)
            ledger_imported.append(str(normalized.get("carried_at") or "未记录时间"))

    changed_names = copied + conflicts
    if not changed_names and not ledger_imported:
        report = {
            "operation": "merge",
            "status": "already_merged",
            "source_capsule_id": other_id,
            "copied": [],
            "unchanged": unchanged,
            "conflicts": [],
            "ledger_imported": [],
            "backup": None,
            "review": None,
        }
        return 0, report

    backup_dir = CAPSULE_ROOT / "AI-Team" / "merge-backups" / datetime.now().strftime("merge-%Y%m%d-%H%M%S-%f")
    backup_dir.mkdir(parents=True, exist_ok=True)
    if MEMORY_DIR.exists():
        shutil.copytree(
            MEMORY_DIR,
            backup_dir / "memory",
            ignore=shutil.ignore_patterns("__pycache__"),
            symlinks=False,
        )
    (backup_dir / "backup.json").write_text(
        json.dumps({"created_at": iso_now(), "source_capsule_id": other_id}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for operation in operations:
        operation["inbox"].parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(operation["source"], operation["inbox"])
    for relative in copied:
        target = safe_target_path(relative)
        source = other_memory / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    current_ledger["schema_version"] = 1
    current_ledger["capsule_id"] = self_id
    current_ledger["last_merged_at"] = iso_now()
    current_ledger["last_merged_from"] = other_id
    save_json(LEDGER_PATH, current_ledger)

    review_path = write_merge_review(operations, other_id) if operations else None
    memory_state, _ = refresh_memory_state()
    old_status = (load_json(STATUS_PATH) or {}).get("current_state")
    merged_status = old_status if old_status in {"carried", "retained_modified", "retained"} else "retained"
    update_status(memory_state, merged_status)
    report_path = CAPSULE_ROOT / "AI-Team" / "merge-reports" / f"merge-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.json"
    report = {
        "operation": "merge",
        "status": "merged_with_review" if conflicts else "merged",
        "source_capsule_id": other_id,
        "copied": copied,
        "unchanged": unchanged,
        "conflicts": conflicts,
        "ledger_imported": ledger_imported,
        "backup": str(backup_dir),
        "review": str(review_path) if review_path else None,
        "memory_revision": memory_state["memory_revision"],
    }
    save_json(report_path, report)
    return 0, report


def print_report(report: dict) -> None:
    titles = {
        "copied": "已复制记忆",
        "unchanged": "内容一致",
        "ledger_imported": "已导入账本记录",
        "removed": "已移除",
        "retained": "已保留",
        "conflicts": "冲突/提示",
        "errors": "问题",
    }
    status_text = {
        "enabled": "团队启用成功",
        "already_enabled": "团队已经启用",
        "carried": "团队桥接已安全移除，可以带走 Portable-AI-Team 文件夹",
        "retained_modified": "带走操作完成，用户修改过的桥接已保留",
        "not_enabled": "未发现启用清单，无需移除",
        "valid": "团队桥接校验通过",
        "failed": "团队桥接校验失败",
        "blocked": "操作已阻止",
        "merged": "记忆合并完成",
        "merged_with_review": "记忆合并完成；同名不同内容已进入 merge-inbox，未覆盖当前文件",
        "already_merged": "两份团队记忆已完成合并或内容一致",
    }
    print(status_text.get(report.get("status"), report.get("status", "完成")))
    for key, title in titles.items():
        values = report.get(key) or []
        if values:
            print(f"{title}:")
            for value in values:
                print(f"- {value}")
    if report.get("backup"):
        print(f"备份位置: {report['backup']}")
    if report.get("review"):
        print(f"审查文件: {report['review']}")
    if report.get("memory_changed"):
        print("本次记忆变化:")
        for value in report["memory_changed"]:
            print(f"- {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Portable AI Team 团队胶囊")
    parser.add_argument("command", choices=("enable", "carry", "validate", "status", "merge"))
    parser.add_argument("--python", dest="python_path", help="本项目默认 Python 解释器绝对路径")
    parser.add_argument("--other", dest="other", help="待合并的另一个 Portable AI Team 文件夹路径")
    args = parser.parse_args()
    if args.command == "enable":
        try:
            python_path = configured_python_path(args.python_path)
        except ValueError as exc:
            report = {"operation": "enable", "status": "blocked", "created": [], "merged": [], "retained": [], "conflicts": [str(exc)]}
            print_report(report)
            return 2
        code, report = enable_capsule(python_path)
    elif args.command == "carry":
        code, report = carry_capsule()
    elif args.command == "validate":
        code, report = validate_capsule()
    elif args.command == "merge":
        if not args.other:
            report = {"operation": "merge", "status": "blocked", "conflicts": ["请把另一个 Portable-AI-Team 文件夹拖到双击合并团队.cmd 上"]}
            print_report(report)
            return 2
        try:
            code, report = merge_capsule(args.other)
        except (ValueError, OSError) as exc:
            report = {"operation": "merge", "status": "blocked", "conflicts": [str(exc)]}
            print_report(report)
            return 2
    else:
        report = load_json(LAST_REPORT_PATH) or {"status": "not_enabled"}
        code = 0
    print_report(report)
    return code


if __name__ == "__main__":
    configure_utf8_io()
    raise SystemExit(main())
    # state/ is disposable; the ledger travels with memory.
