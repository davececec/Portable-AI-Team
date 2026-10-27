# 从这里开始 (v3.0.0)

1. 把完整的 `Portable-AI-Team/` 文件夹复制到业务项目根目录。
2. 打开 `Python路径.txt`，确认第一条非空内容是当前电脑的 Python 可执行文件绝对路径。当前默认是 `D:\00-python\python\python.exe`。
3. 双击 `双击启用团队.cmd`。
4. 用 Codex、Google Antigravity 或 TraeCode 打开业务项目，说：“ZH，给我做一个……”。
5. 项目完成或准备带走时，先让 AgentA 归纳可复用记忆，再双击 `双击带走团队.cmd`，确认报告后移走整个文件夹。
6. 需要合并两份团队经验时，把另一份已带走的 `Portable-AI-Team/` 文件夹拖到 `双击合并团队.cmd` 上。V3.0 可安全合并 v2.3+ 胶囊；更旧、缺失或无效版本会被拒绝。

团队主体始终留在单个文件夹内。双击启用只会在业务项目根生成 IDE 自动发现所必需的最小桥接；这是 IDE 能在打开项目时找到团队的必要条件，不是把团队主体重新散落到根目录。

## V3.0 执行方式

- AgentA 负责需求、工单、派单和独立验收；AgentB 为主实现，AgentD 分担独立模块。
- AgentB 和 AgentD 只接收工单路径、项目路径、允许修改范围、必要文件列表和完成条件；禁止继承完整对话或互相读取输出。
- 外部 API 调度由 `AI-Team/llm_dispatch.py` 执行。AgentA 可先运行 `python AI-Team/llm_dispatch.py --test` 探测模型。
- 并行派单时，互不依赖任务可通过 `--dispatch-parallel --tasks <任务文件>` 分发；`max_parallel` 上限是 4。
- 外部 API 不可用、超时或返回错误时进入失败降级流程，结果标记失败并回退 `codex_builtin`。AgentA 必须重新决策，不能把外部模型回复当作验收结果。
- 本地测试入口是 `python -m unittest discover -s tests -v`；所有调度测试离线打桩，不访问网络，不输出真实密钥。

## 状态卡和合并

- `团队状态.json` 在胶囊根目录，能看当前状态、记忆版本、当前项目、最近项目和最近带走时间。
- `AI-Team/memory/记忆账本.json` 记录每次带走的项目、时间、记忆版本和变化记忆文件。
- 仍启用的胶囊复制到新项目会被阻止；请先回原项目双击带走。
- 合并只处理记忆和账本，不处理业务源码、依赖、构建产物、IDE 配置或桥接。
- 无冲突记忆自动合并；同名不同内容进入 `AI-Team/memory/merge-inbox/`，不会覆盖当前文件。
- 合并前自动备份；重复合并会明确报告已完成或内容一致。

## 平台备注

- **Codex**：桥接根 `AGENTS.md` 和 `.codex/agents/*.toml`，实际角色资料仍在胶囊内。
- **Google Antigravity**：桥接 `.agents/rules/` 和 `.agents/agents/`，主 Agent 调用 AgentB/AgentD 和按需 AgentC 后独立验收。
- **TraeCode**：桥接 `.trae/rules/`。如当前版本没有子智能体能力，按同一规则顺序降级，不阻塞使用。

已有文件不会被覆盖；冲突时生成合法并存桥接。带走时只删除指纹未变的受管文件或精确受管区块，用户修改过的文件会保留并报告。完整说明位于 `AI-Team/ide-guides/compatibility-matrix.md`。

新建主要界面、整体改版、明确美化时按需 C 设计 -> B/D 实现 -> C 实际视觉检查 -> A 独立验收；纯后台及文字/颜色小改默认跳过 C。无子智能体时明确角色顺序模拟，不声称独立 C 或干净上下文隔离；无截图能力标未验证。

旧版升级：先在原项目用旧版双击带走并确认清理，备份旧 `AI-Team/memory/` 和 `Python路径.txt`，换上新版胶囊后合并记忆、恢复 Python 配置再启用。禁止直接覆盖仍启用的旧胶囊，禁止把旧 `state/` 复制或覆盖到新版；不支持原地自动迁移。详见 README。

中文双击入口使用 Windows PowerShell 读取 `Python路径.txt`，再调用唯一 `AI-Team/capsule.py`，不要求 Python 位于 PATH。配置兼容 BOM、引号、空白和不可见方向字符；无效路径不会修改项目。

启用后根桥接会记录默认 Python 路径。AgentB/AgentD 运行 Python、安装依赖和测试时优先使用它。带走前只归纳稳定可复用的偏好、技术与项目摘要；不要把业务源码、密钥、原始日志、构建产物或项目依赖放进胶囊。`AI-Team/memory-backup-20261010/` 是恢复备份，不会进入分发 ZIP；保留到 V3.0 稳定确认后再处理。
