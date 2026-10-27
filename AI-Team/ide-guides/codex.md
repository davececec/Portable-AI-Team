# Codex

Codex 自动读取项目根 `AGENTS.md`。专用 AgentB 位于 `.codex/agents/agent-b.toml`，包含 `name`、`description` 和 `developer_instructions`，不绑定具体模型，继承宿主选择。

AgentA 应向 AgentB 发送工单路径、项目路径、允许修改范围、必要文件和完成条件；AgentB 返回后由 AgentA 独立验收。通常无需额外设置。若宿主版本暂不支持项目自定义 Agent，则按同一角色边界顺序执行并说明降级。

v2.3.0 增加 `.codex/agents/agent-c.toml`。新建主要界面、整体改版、明确美化时按需 C 设计 -> B 实现 -> C 实际截图/交互检查 -> A 独立验收；纯后台及文字/颜色小改默认跳过 C。角色和路由资料在胶囊 `AI-Team/agents/AgentC.md` 与 `AI-Team/policies/ui-routing.md`。无子智能体则明确角色顺序模拟，不声称独立 C 或干净上下文隔离；无截图能力标未验证。
