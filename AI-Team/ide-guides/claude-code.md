# Claude Code

Claude Code 自动加载项目根 `CLAUDE.md`，也支持通过 `CLAUDE.md` 里 `@path` 语法引用其他文件；它**不会**自动读取 `AGENTS.md` 内的区块。因此本分发包对 Claude Code 的桥接策略是"镜像 AGENTS.md 区块到 CLAUDE.md"。

## 启用时发生什么

1. 启用器始终把团队区块写入根 `AGENTS.md`（与其他 IDE 一致）。
2. 若项目根存在 `CLAUDE.md`，启用器把 `bridges/claude/claude.md` 模板（含 `{{PYTHON_PATH}}` 替换后的内容）作为**可逆标记区块**追加到 `CLAUDE.md`，digest 记入清单。
3. 若不存在 `CLAUDE.md`，不主动创建——Claude Code 用户可自行新建并把 `AGENTS.md` 区块 `@` 引用进来，或再跑一次启用。

## 能力边界

- **规则加载**：`CLAUDE.md` 是 Claude Code 的一等公民，团队规则随会话自动生效，可靠性高。
- **并行实现**：Claude Code 的 Task 子代理可承担 AgentB/AgentD 的并行实现。子代理 prompt 只包含工单路径、项目路径、允许修改范围、必要文件列表和完成条件，遵守 Low-Token 最小上下文纪律。
- **视觉检查**：无专用视觉子代理时，由主代理按角色顺序执行视觉走查并明确报告"顺序降级"，不声称独立 C 或干净上下文隔离。
- **冲突规则**：B/D 仍遵守不同模型、不同文件的硬边界。

## 验证方式

- `python AI-Team/capsule.py validate` 确认 CLAUDE.md 区块未被改动。
- 发起"ZH，给我做一个……"任务，确认 Claude Code 读取了团队规则。
- `python AI-Team/capsule.py doctor` 自检。

## 备注

Claude Code 的自动发现行为随版本演进。若某版本不再自动加载 `CLAUDE.md`，请把 `AGENTS.md` 的团队区块手动 `@` 引入 `CLAUDE.md`，并在本文件记录版本与现象。
