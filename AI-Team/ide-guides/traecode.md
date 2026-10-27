# TraeCode

始终生效的项目规则是 `.trae/rules/portable-ai-team.md`。规则文件使用 Markdown，并以 `alwaysApply: true` frontmatter 表明项目范围内持续应用。

## 一次性设置

1. 可在“设置 > 规则 > 导入设置”开启“将 AGENTS.md 包含在上下文中”。这会补充根规则，但不是使用本包的前置条件，因为 `.trae/rules/portable-ai-team.md` 已提供核心流程。
2. 若当前 TraeCode 版本提供可配置的自定义 Agent/子智能体功能，可分别导入 `AI-Team/adapters/trae/AgentA-import.md`、`AgentB-import.md` 与 `AgentC-import.md`；胶囊部署时这些路径前加 `Portable-AI-Team/`。不同版本入口可能不同，本包不虚构自动发现能力。

## 顺序降级

新建主要界面、整体改版、明确美化时按需 C 设计 -> B 实现 -> C 实际截图/交互检查 -> A 独立验收；纯后台及文字/颜色小改默认跳过 C。没有子智能体功能时，同一 Agent 按上述角色顺序模拟，A 阶段重新运行验收，最终报告明确写出“顺序降级”，不声称独立 C 或干净上下文隔离。无截图能力标未验证。角色边界、低 Token 约束和最多两轮返工仍保持不变。
