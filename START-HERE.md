# 从这里开始 (v3.1.0)

1. 把整个 `Portable-AI-Team/` 文件夹复制到业务项目根目录。
2. 把 `Python路径.txt.example` 复制为 `Python路径.txt`：确认第一行是你当前使用的 Python 可执行文件的绝对路径（例如 `C:\Python311\python.exe`）。
3. 双击 `双击启用团队.cmd`。
4. 接入模型：把 `LLM配置.example.json` 复制为 `LLM配置.json`，填入你自己的 `base_url` / `api_key` / `models`，再运行 `python AI-Team/capsule.py doctor` 自检。30 秒上手见 `AI-Team/references/llm-接入指南.md`。
5. 在 Codex、Google Antigravity、TraeCode、Claude Code 或 WorkBuddy 的业务项目里说："ZH，帮我做一个……"。
6. 项目完成或准备交接时，让 AgentA 沉淀可复用经验，再双击 `双击带走团队.cmd`，确认经验已带走且工作文件未动。
7. 需要合并两个团队经验时，在较早一个已带走的 `Portable-AI-Team/` 文件夹上的 `双击合并团队.cmd` 上。V3.1 可安全合并 v2.3+ 胶囊，空、缺失或无效版本会被拒绝。

团队经验始终留在胶囊文件夹内；双击脚本只改业务项目里的 IDE 自动加载文件（规则、子代理）。多个 IDE 共存时找到团队的必要内容都落在前面团队胶囊的散落到根目录。

## V3.1 执行方式

- AgentA 负责需求、工单、派单和独立验收；AgentB 为主实现，AgentD 负责并行模块。
- AgentB 与 AgentD 只接收工单路径、项目路径、允许修改的范围、必要文件列表与验收条件，禁止继承完整对话历史。
- 外部 API 路由由 `AI-Team/llm_dispatch.py` 执行。AgentA 可用 `python AI-Team/llm_dispatch.py --test` 探测模型。
- 并行派单时用 `--dispatch-parallel --tasks <任务文件>` 发送，`max_parallel` 上限 4。
- 外部 API 未配置、超时或返回失败时走失败降级流程：不重试、不阻塞，退回 `codex_builtin`。AgentA 按内置流程，不能把外部模型回复当作最终结果。
- 自检：`python AI-Team/capsule.py doctor` 依次校验 Python 路径、团队版本、LLM 配置结构与每个模型的最小连通性，全部通过才算可开工。
- 本地测试：`python -m unittest discover -s tests -v`；有外部测试桩的测试离线可跑，不依赖真实密钥。

## 状态与合并

- `团队状态.json` 在胶囊根目录保存启用状态、团队版本、当前项目名、启用时间和项目路径。
- `AI-Team/memory/记忆账本.json` 记录每次带走的项目、时间、团队版本和变更文件。
- 已启用的胶囊复制到新项目会被阻止：请回原项目双击带走。
- 合并只同步记忆账本与经验，不碰业务源码、工单、交付物、IDE 或用户配置。
- 无冲突时直接自动合并；同路径不同内容进入 `AI-Team/memory/merge-inbox/`，不覆盖当前文件。
- 合并前自动备份；重复合并会确认经验基线一致。

## 平台备注

- **Codex**：规则进 `AGENTS.md` 与 `.codex/agents/*.toml`，实际角色以胶囊内置为准。
- **Google Antigravity**：规则进 `.agents/rules/` 与 `.agents/agents/`，Agent 子代理 AgentB/AgentD 和按需 AgentC 独立验收。
- **TraeCode**：规则进 `.trae/rules/`；当前版本没有子代理入口，按同一顺序顺序降级使用。
- **Claude Code**：团队区块镜像进 `CLAUDE.md`（仅当项目中已存在该文件；追加带标记区块，可逆）。未官方验证。
- **WorkBuddy**：规则进 `.workbuddy/rules/portable-ai-team.md`；按 A->C->B->D->C 顺序模拟角色。未官方验证。

任何文件都不会被覆盖；冲突时生成合规的并行文件。带走时只删除指定未改动文件并确完整校验，用户修改过的文件会保留并告警。平台说明见 `AI-Team/ide-guides/compatibility-matrix.md`。

新建需要设计、视觉版、确切界面时走：C 设计 -> B/D 实现 -> C 实现后视觉审查 -> A 独立验收。后台设计稿/角色小样默认交给 C；没有设计稿时确认角色顺序模拟，没有移动则 C 不删文件不改动；无截图则视觉未验证。

老胶囊升级：回原项目用旧版双击带走并确认经验已带走 `AI-Team/memory/` 与 `Python路径.txt`，把新版放入后合并经验、恢复 Python 路径配置。不要直接覆盖启用的旧胶囊，不要把旧 `state/` 复制/覆盖到新版；不支持原路径自动迁移。见 README。

双击脚本使用 Windows PowerShell 读取 `Python路径.txt`，再调用唯一 `AI-Team/capsule.py`；不需要 Python 位于 PATH。该文件只读第一行，容忍 BOM、前缀、空白和不可见 Unicode 字符；有效路径请修改第一行。

启用后规则与子代理记得默认 Python 路径，AgentB/AgentD 需要 Python 时安装依赖和测试时尽量使用同一解释器。当前只记录稳定可复用的偏好；不要沉淀项目摘要、业务源码、密钥、原始日志；经验只进项目目录规则与团队胶囊。`AI-Team/seed/memory-20261010/` 是脱敏后的恢复种子数据，不进入分发包 ZIP；团队 V3.1 稳定确认后再纳入。
