<!-- portable-ai-team-capsule-v1 -->
# Portable AI Team 桥接

团队主体位于 `Portable-AI-Team/`。用户说“ZH，给我做一个……”时，主 Agent 读取 `Portable-AI-Team/AI-Team/agents/AgentA.md`，按互不依赖边界委派 AgentB/AgentD 实现并在返回后独立验收。AgentB/D 只接收最小干净上下文，最多自动返工 2 轮。

新建主要界面、整体改版或明确美化按 `Portable-AI-Team/AI-Team/policies/ui-routing.md` 调用团队 AgentC 设计和实际视觉检查；纯后台及文字/颜色小改默认跳过。没有子智能体能力时明确报告顺序降级：角色顺序模拟，A -> 按需 C -> B -> D -> 按需 C -> A，不声称独立 C 或干净上下文隔离。

本项目默认 Python 解释器是 `{{PYTHON_PATH}}`。AgentB/D 运行 Python、安装依赖和测试时优先使用该绝对路径。用户提出项目完成或准备带走团队时，AgentA 必须先归纳可复用记忆，再提示双击带走；禁止把业务源码、密钥、原始日志、构建产物或项目依赖收入胶囊。
