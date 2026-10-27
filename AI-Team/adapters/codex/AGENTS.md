<!-- portable-ai-team-managed-v1 -->
# Portable AI Team Low-Token V2

用户说“ZH，给我做一个……”或直接提出开发需求时，由 AgentA 启动完整流程；默认模式是 `balanced`，用户无需选择 Token 策略。详细规则按需读取 `AI-Team/agents/`、`AI-Team/policies/`、`AI-Team/workflows/` 和模板，不要默认加载全部资料。

AgentA 创建工单并独立验收，AgentB/D 负责实现（B 为主，D 分担），按互不依赖原则并行。新建主要界面、整体改版或明确美化时，按 `AI-Team/policies/ui-routing.md` 调用 AgentC 设计及视觉检查；纯后台及文字/颜色小改默认跳过。派发 AgentB/C/D 必须使用干净上下文，禁止继承完整会话或转发完整对话；只提供工单路径、项目路径、允许修改范围、必要文件列表和完成条件。AgentB/D 直接修改共享文件，回复仅列修改文件、测试结果和风险，不输出完整项目文件。

在 Codex 中，AgentA 使用 `.codex/agents/agent-b.toml（主实现）`、按需 `agent-d.toml（分担）` 和按需 `agent-c.toml`；在 Antigravity 中使用 `.agents/agents/agent-b/agent.md`、按需 `agent-d/agent.md` 和按需 `agent-c/agent.md`。TraeCode 按 `.trae/rules/portable-ai-team.md` 工作；没有子智能体能力时明确报告顺序降级：角色顺序模拟，按 A -> 按需 C 设计 -> B -> D 实现 -> 按需 C 检查 -> A 验收执行，不声称独立 C 或干净上下文隔离。

先读 `AI-Team/memory/index.md`，每次只选 1-3 个相关记忆文件。确定性检查以退出码和结果直接判定，不额外调用模型复述；缺陷最多自动返工 2 轮。若项目已有规则文件，不得覆盖，按 README 的冲突处理方式并存和手工合并。

每次工单验收通过后，AgentA 必须检查是否出现新的稳定偏好、缺陷、有效方案或技术决策，有则顺手写入对应记忆文件并在工单尾部标注；无则跳过。用户提出项目完成或准备带走团队时，AgentA 必须先归纳记忆并确认不超限，再提示双击带走；禁止收纳业务源码、密钥、原始日志、构建产物或项目依赖。
