---
alwaysApply: true
---
<!-- portable-ai-team-capsule-v1 -->
# Portable AI Team 桥接

团队主体位于 `Portable-AI-Team/`。用户说“ZH，给我做一个……”时，读取 `Portable-AI-Team/AI-Team/agents/AgentA.md` 和相关策略。AgentB/D 只接收最小干净上下文并分担实现；AgentA 独立验收，最多自动返工 2 轮。新建主要界面、整体改版或明确美化按 `Portable-AI-Team/AI-Team/policies/ui-routing.md` 调用 C 设计和实际视觉检查；纯后台及文字/颜色小改默认跳过。无子智能体能力则顺序降级：角色顺序模拟，A -> 按需 C -> B -> D -> 按需 C -> A，不声称独立 C 或干净上下文隔离。C 导入资料位于 `Portable-AI-Team/AI-Team/adapters/trae/AgentC-import.md`，D 导入资料位于 `Portable-AI-Team/AI-Team/adapters/trae/AgentD-import.md`。

本项目默认 Python 解释器是 `{{PYTHON_PATH}}`。AgentB/D 运行 Python、安装依赖和测试时优先使用该绝对路径。用户提出项目完成或准备带走团队时，AgentA 必须先归纳可复用记忆，再提示双击带走；禁止把业务源码、密钥、原始日志、构建产物或项目依赖收入胶囊。
