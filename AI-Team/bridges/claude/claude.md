# portable-ai-team-capsule-v1
# Portable AI Team 桥接（Claude Code 补充）

Claude Code 通过根 `CLAUDE.md`（自动发现）或根 `AGENTS.md`（启用器写入的团队区块）加载团队。本文件是 `CLAUDE.md` 模板：Claude Code 自动加载 `CLAUDE.md` 但不会自动加载 `AGENTS.md` 内的区块，启用器在检测到 Claude Code 环境（项目或全局 `CLAUDE.md` 存在）时，会把团队区块追加到 `CLAUDE.md`，与 `AGENTS.md` 区块内容一致。

团队主体位于 `Portable-AI-Team/`。用户说"ZH，给我做一个……"时，读取 `Portable-AI-Team/AI-Team/agents/AgentA.md` 和相关策略。Claude Code 的 Task 子代理可承担 AgentB/AgentD 并行实现（子代理 prompt 只含工单路径、项目路径、允许修改范围、必要文件列表和完成条件）；AgentA 独立验收，最多自动返工 2 轮。

本项目默认 Python 解释器是 `{{PYTHON_PATH}}`。运行 Python、安装依赖和测试时优先使用该绝对路径。用户提出项目完成或准备带走团队时，AgentA 必须先归纳可复用记忆，再提示双击带走；禁止把业务源码、密钥、原始日志、构建产物或项目依赖收入胶囊。
