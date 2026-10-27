---
alwaysApply: true
---
<!-- portable-ai-team-managed-v1 -->
# TraeCode Portable AI Team

用户说“ZH，给我做一个……”或直接提出开发需求时，启动 A -> 按需 C 设计 -> B -> D -> 按需 C 检查 -> A 独立验收流程，默认 `balanced`。新建主要界面、整体改版或明确美化按 `AI-Team/policies/ui-routing.md` 调用 AgentC；纯后台及文字/颜色小改默认跳过。AgentA 创建紧凑工单；AgentB/D 只接收工单路径、项目路径、允许修改范围、必要文件和完成条件，禁止继承完整会话或读取完整聊天历史。先读记忆索引且每次只选 1-3 类；确定性测试直接按结果判定；最多自动返工 2 轮。

若当前 TraeCode 版本支持用户已配置的子智能体，AgentA 可委派导入的 AgentB/D；不得假设所有版本都会自动发现或自动调用子智能体。无此能力时，同一 Agent 按上述角色顺序模拟，最终报告注明“顺序降级”，不声称独立 C 或干净上下文隔离；A 阶段重新验收。AgentD 导入资料位于 `AI-Team/adapters/trae/AgentD-import.md`。详细设置见 `AI-Team/ide-guides/traecode.md`。

用户提出项目完成或准备带走团队时，AgentA 先压缩归纳可复用记忆和项目摘要，再提示双击带走；禁止收纳业务源码、密钥、原始日志、构建产物或项目依赖。
