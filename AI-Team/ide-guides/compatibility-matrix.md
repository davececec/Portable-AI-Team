# 跨 IDE 兼容性矩阵

不同 IDE 的多智能体 API 并不相同，本分发包不承诺五者具有相同的自动委派能力；统一的是 AgentA 管理、按需 AgentC 设计、AgentB 实现、按需 C 实际视觉检查、AgentA 独立验收。新建主要界面、整体改版或明确美化调用 C，纯后台及文字/颜色小改默认跳过。缺少子智能体能力时明确角色顺序模拟，不声称独立 C 或干净上下文隔离；无截图能力标未验证。

团队主体位于单个 `Portable-AI-Team/` 胶囊。双击启用后生成的根桥接是 IDE 自动发现规则与 Agent 的必要条件；桥接只指向胶囊内部资料，可通过双击带走安全移除。

双击入口从胶囊根 `Python路径.txt` 读取默认 Python 绝对路径，不依赖 PATH。归一化路径会写入 Codex、Antigravity、TraeCode 和根 `AGENTS.md` 桥接，供 AgentB 运行 Python、安装依赖和测试时优先使用。

| 平台 | 自动规则加载 | 自动/专用 AgentB/C | 一次性设置 | 降级行为 | 验证方式 |
| --- | --- | --- | --- | --- | --- |
| Codex | 启用器创建根 `AGENTS.md` 区块 | `.codex/agents/*.toml` 可由 AgentA 委派 | 双击启用 | 宿主不支持自定义 Agent 时按角色顺序执行 | 胶囊校验、TOML 解析、发起“ZH”任务 |
| Google Antigravity | 启用器创建 `.agents/rules/*.md` | `.agents/agents/*/agent.md`，`subagent: true` | 双击启用；首次可能需确认工具权限 | 子智能体不可用时按角色顺序执行 | 胶囊校验、frontmatter 与工具名检查 |
| TraeCode | 启用器创建 `.trae/rules/*.md` | 不承诺所有版本自动发现；支持时可导入 B/C 提示词 | 双击启用；可选启用根 `AGENTS.md` 上下文 | 同一 Agent 按 A -> 按需 C -> B -> 按需 C -> A 执行并报告“顺序降级” | 胶囊校验、规则文件检查、发起“ZH”任务 |
| Claude Code | 根 `CLAUDE.md` 自动发现；启用器在检测到 CLAUDE.md 时把团队区块追加进去（与 AGENTS.md 区块内容一致） | Task 子代理可承担 B/D 并行实现（最小上下文） | 双击启用（若项目用 Claude Code 则自动写入 CLAUDE.md 区块） | 无 Task 子代理时按角色顺序执行并报告“顺序降级” | 胶囊校验、CLAUDE.md 区块检查、发起“ZH”任务 |
| WorkBuddy | 启用器创建 `.workbuddy/rules/portable-ai-team.md`（最保守的规则文件方案） | 不承诺子智能体；按角色顺序模拟 | 双击启用；规则目录若与你的 WorkBuddy 版本不一致，按 `ide-guides/workbuddy.md` 手动放置 | 始终按 A -> 按需 C -> B -> D -> 按需 C -> A 顺序执行并报告“顺序降级”（未官方验证） | 胶囊校验、规则文件检查、发起“ZH”任务 |

五平台都必须遵守 Low-Token V2：AgentB/C 只接收最小干净上下文，每次只读 1-3 类相关记忆，确定性测试直接按结果判定，反馈合并，最多自动返工 2 轮。C 默认只设计/检查；无授权不修改文件，不得与 B 并发编辑同一文件。规范和截图留在业务项目。

> **关于 WorkBuddy / Claude Code**：Codex、Antigravity、TraeCode 已在本团队生产环境验证；Claude Code 依赖其 `CLAUDE.md`/`AGENTS.md` 自动发现机制，规则加载可靠、子代理能力取决于版本；WorkBuddy 目前缺少公开的官方规则目录规范，本分发包采用 `.workbuddy/rules/*.md` 最保守方案并明确标注“未官方验证”，接入后请以实际行为为准，发现规则目录不同请在 `ide-guides/workbuddy.md` 记录并反馈。

项目完成或准备带走时，五平台的 AgentA 都必须先归纳可复用记忆和项目摘要，再提示双击带走。只允许稳定经验；禁止收纳业务源码、密钥、原始日志、构建产物或项目依赖。

胶囊内可运行 `python AI-Team/capsule.py validate` 检查当前桥接；源项目维护者运行 `python AI-Team/check_compatibility.py --build` 可重建并校验单文件夹分发目录与 ZIP。
