# Google Antigravity

项目规则位于 `.agents/rules/portable-ai-team.md`。自定义 AgentB 位于 `.agents/agents/agent-b/agent.md`，使用 YAML frontmatter、`subagent: true`，并仅声明 Antigravity 工具名 `view_file`、`replace_file_content`、`grep_search`、`run_command`。

主 Agent 始终承担 AgentA 职责：创建工单、发送最小干净上下文、调用 AgentB，并在返回后独立验收。若当前环境无法调用子智能体，则按角色顺序降级执行并说明原因。

v2.3.0 增加 `.agents/agents/agent-c/agent.md`，C 的工具列表额外声明 `browser_subagent`，以当前宿主实际能力为准。新建主要界面、整体改版、明确美化时按需 C 设计 -> B 实现 -> C 实际截图/交互检查 -> A 独立验收；纯后台及文字/颜色小改默认跳过。无子智能体则明确角色顺序模拟，不声称独立 C 或干净上下文隔离；无截图能力标未验证。
