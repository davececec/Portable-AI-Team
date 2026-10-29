# Portable AI Team Low-Token V2

默认使用时，请把 `dist/Portable-AI-Team/` 整个文件夹放入业务项目根目录，再双击胶囊根部的中文启用入口。团队主体、状态和工具都留在胶囊中；根目录只生成 IDE 自动发现所需的最小桥接。

## 命令

在本目录运行：

```powershell
python team.py init --project . --name "我的项目" --tech Python
python team.py install --project .
python team.py status --project .
python team.py validate --project .
python team.py context --project .
python team.py uninstall --project .
```

安装会部署根 `AGENTS.md`、Codex AgentB/C、TraeCode 项目规则、Antigravity 规则与 AgentB/C。不会覆盖已有文件；冲突时创建仍可被目标 IDE 识别的并存文件。卸载只删除仍匹配管理指纹的文件，保留项目代码、历史和 AI-Team。

完成项目后双击胶囊根部的带走入口，再移走整个 `Portable-AI-Team/` 文件夹；不要只移动内部 `AI-Team/` 子目录。

## 团队胶囊

```powershell
python capsule.py enable
python capsule.py validate
python capsule.py status
python capsule.py carry
```

默认用户无需运行这些命令。中文双击入口由 Windows `powershell.exe` 读取胶囊根 `Python路径.txt`，完成路径净化和解释器预检后调用唯一 `capsule.py`；不依赖 Python PATH。带走时只删除指纹匹配的受管桥接或精确的 `AGENTS.md` 标记区块，用户修改过的桥接会保留并报告。根桥接是 Codex、Antigravity、TraeCode 自动发现团队的必要条件。

## 按需读取

常驻根规则只保留入口和核心约束。AgentA 根据任务读取：

- `agents/`：角色职责与最小上下文流程。
- `policies/token-budget.md`：`economy`、`balanced`、`quality` 和预算上限。
- `policies/model-routing.md`：跨 IDE、非厂商绑定的模型路由。
- `policies/multi-session-dispatch.md`：多会话并行调度、队列纪律和文件边界。
- `policies/ui-routing.md`：按需 C 设计与视觉检查，纯后台及文字/颜色小改跳过。
- `memory/index.md`：先索引后选择，每次只加载 1-3 类记忆。
- `templates/`：微型/标准工单及紧凑交付、测试、缺陷模板。
- `ide-guides/`：平台指南、一次性设置和兼容性矩阵。

默认模式为 `balanced`。任何模式都保留 AgentA 独立验收、必要测试和安装安全功能。
