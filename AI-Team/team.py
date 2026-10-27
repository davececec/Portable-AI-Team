"""Portable AI Team management CLI; Python standard library only."""
from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import date, datetime
from pathlib import Path

MARKER = "portable-ai-team-managed-v1"
TEAM_VERSION = "3.0.0"
ADAPTERS = {
    "codex-rules": ("AGENTS.md", "adapters/codex/AGENTS.md"),
    "codex-agent-b": (".codex/agents/agent-b.toml", "adapters/codex/agent-b.toml"),
    "codex-agent-c": (".codex/agents/agent-c.toml", "adapters/codex/agent-c.toml"),
    "codex-agent-d": (".codex/agents/agent-d.toml", "adapters/codex/agent-d.toml"),
    "trae-rules": (".trae/rules/portable-ai-team.md", "adapters/trae/portable-ai-team.md"),
    "antigravity-rules": (".agents/rules/portable-ai-team.md", "adapters/antigravity/portable-ai-team.md"),
    "antigravity-agent-b": (".agents/agents/agent-b/agent.md", "adapters/antigravity/agent-b.md"),
    "antigravity-agent-c": (".agents/agents/agent-c/agent.md", "adapters/antigravity/agent-c.md"),
    "antigravity-agent-d": (".agents/agents/agent-d/agent.md", "adapters/antigravity/agent-d.md"),
}

def configure_utf8_io():
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="strict")

def root_of(): return Path(__file__).resolve().parent
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load_json(p): return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
def save_json(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
def identity(project): return project / ".ai-team-project.json"
def adapter_content(relative): return (root_of()/relative).read_text(encoding="utf-8")
def conflict_path(target):
    if target.name == "AGENTS.md": return target.with_name("AGENTS.md.ai-team")
    if target.name == "agent.md" and target.parent.parent.name == "agents":
        return target.parent.with_name(f"{target.parent.name}-ai-team") / target.name
    return target.with_name(f"{target.stem}-ai-team{target.suffix}")
def numbered_path(target, number):
    if target.name == "agent.md" and target.parent.parent.name == "agents":
        return target.parent.with_name(f"{target.parent.name}-{number}") / target.name
    if target.name == "AGENTS.md.ai-team": return target.with_name(f"{target.name}.{number}")
    return target.with_name(f"{target.stem}-{number}{target.suffix}")

def init(args):
    p=Path(args.project).resolve(); f=identity(p); old=load_json(f)
    if old:
        print(json.dumps({"status":"existing","project_id":old["project_id"]}, ensure_ascii=False)); return
    obj={"project_id": hashlib.sha256(str(p).encode()).hexdigest()[:16], "project_name":args.name, "created":date.today().isoformat(), "tech_stack":args.tech, "original_path":str(p), "current_path":str(p), "last_updated":date.today().isoformat(), "team_version":TEAM_VERSION, "token_mode":"balanced"}
    save_json(f,obj); print("已初始化项目身份: "+obj["project_id"])

def install(args):
    p=Path(args.project).resolve(); init(argparse.Namespace(project=p,name=p.name,tech="")) if not identity(p).exists() else None
    previous=load_json(p/".ai-team-install.json") or {}; manifest=dict(previous.get("files",{})); paths=[]
    for kind, (rel, source) in ADAPTERS.items():
        target=p/rel
        if target.exists():
            if MARKER in target.read_text(encoding="utf-8", errors="ignore"):
                manifest.setdefault(str(target.relative_to(p)), digest(target)); continue
            target=conflict_path(target)
        if target.exists():
            existing = target.read_text(encoding="utf-8", errors="ignore")
            managed_rel = str(target.relative_to(p)) in manifest
            if MARKER in existing and managed_rel:
                continue
            if target.exists():
                # Keep the tampered managed file visible to validate/uninstall and
                # create a fresh non-conflicting adapter beside it.
                n = 2
                while target.exists():
                    target = numbered_path(target, n)
                    n += 1
        content = adapter_content(source)
        if target != p/rel and kind.startswith("codex-agent-"):
            content = content.replace(f'name = "{Path(rel).stem}"', f'name = "{target.stem}"')
        if target != p/rel and kind.startswith("antigravity-agent-"):
            content = content.replace(f"name: {Path(rel).parent.name}", f"name: {target.parent.name}")
        target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content,encoding="utf-8"); manifest[str(target.relative_to(p))]=digest(target); paths.append(str(target))
    save_json(p/".ai-team-install.json", {"marker":MARKER,"files":manifest,"installed_at":datetime.now().isoformat(timespec="seconds")}); print("已安装: "+", ".join(paths) if paths else "已安装（幂等，无需覆盖）")

def status(args):
    p=Path(args.project).resolve(); ident=load_json(identity(p)); man=load_json(p/".ai-team-install.json")
    print(json.dumps({"project":ident,"installed":bool(man),"files":list((man or {}).get("files",{}))},ensure_ascii=False,indent=2))

def validate(args):
    p=Path(args.project).resolve(); errors=[]; ident=load_json(identity(p)); man=load_json(p/".ai-team-install.json")
    if not ident: errors.append("缺少项目身份文件")
    elif ident.get("current_path") and Path(ident["current_path"]).resolve() != p: errors.append("项目身份路径不匹配，请确认团队放回了正确项目")
    team=p/"AI-Team"
    if not team.exists(): errors.append("当前项目缺少 AI-Team 目录")
    for rel,h in (man or {}).get("files",{}).items():
        f=p/rel
        if not f.exists(): errors.append("适配文件缺失: "+rel)
        elif digest(f)!=h: errors.append("适配文件已被修改: "+rel)
    print("校验通过" if not errors else "校验失败: "+"；".join(errors)); return 0 if not errors else 1

def uninstall(args):
    p=Path(args.project).resolve(); man=load_json(p/".ai-team-install.json"); removed=[]; kept=[]
    for rel,h in (man or {}).get("files",{}).items():
        f=p/rel
        if f.exists() and digest(f)==h and MARKER in f.read_text(encoding="utf-8",errors="ignore"): f.unlink(); removed.append(rel)
        else: kept.append(rel)
    if man: (p/".ai-team-install.json").unlink()
    print(json.dumps({"removed":removed,"kept":kept},ensure_ascii=False))

def context(args):
    p=Path(args.project).resolve(); ident=load_json(identity(p)); print("项目上下文"); print(json.dumps(ident or {},ensure_ascii=False,indent=2))
    for d in ["memory","tasks","deliveries","test-reports","defects"]:
        folder=p/"AI-Team"/d
        if folder.exists(): print(f"\n[{d}]\n"+"\n".join(x.name for x in folder.iterdir()))

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    for n,fn in [("init",init),("install",install),("status",status),("validate",validate),("uninstall",uninstall),("context",context)]:
        sp=sub.add_parser(n); sp.add_argument("--project",default=".");
        if n=="init": sp.add_argument("--name",required=True); sp.add_argument("--tech",default="")
        sp.set_defaults(fn=fn)
    a=ap.parse_args(); raise SystemExit(a.fn(a) or 0)
if __name__=="__main__":
    configure_utf8_io()
    main()
