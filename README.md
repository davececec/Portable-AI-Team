# Portable AI Team (v3.1.0)
Current release: v3.1.0

**A portable, multi-agent AI coding team that lives inside a single folder.**

[English](#english) | [中文](#中文)

---

## English

Portable AI Team v3.1.0 supports five platforms: Codex, Google Antigravity,
TraeCode, Claude Code, and WorkBuddy.

Model routing is optional: when the 外部 API is unavailable or times out,
every dispatch falls back via 失败降级 to the built-in model
(`codex_builtin`). 并行派单 stays capped at `max_parallel = 4`.

Portable AI Team is a low-token multi-agent coding framework that works across
five platforms: Codex, Google Antigravity, TraeCode, Claude Code, and WorkBuddy.
Copy one folder into any project, double-click to enable, and a team of agents
starts working with minimal context overhead: AgentA (orchestrator),
AgentB/AgentD (implementers), and AgentC (on-demand designer).

A team, not a chatbot. Agents that ship code must also produce evidence:
tests run, endpoints probed, browsers walked. No evidence, no delivery.

### Why Low-Token?

- AgentA dispatches work orders (file paths, scope, completion criteria) --
  not full chat history -- to AgentB/AgentD.
- Work orders, deliveries, and defect reports use compact templates;
  implementers edit shared files directly instead of echoing code in chat.
- Memory loads only 1-3 relevant categories per task with strict
  per-file and per-entry caps.
- Compilation, unit tests, and file existence are judged by tool results,
  not by model re-narration.
- Automatic rework is capped at 2 rounds.

### Key Features

| Feature | Description |
| --- | --- |
| Cross-platform | Codex, Google Antigravity, TraeCode, Claude Code, WorkBuddy (graceful degradation; Claude Code and WorkBuddy marked "not officially verified") |
| Multi-agent | A (orchestrator) + B (main impl) + C (design) + D (parallel impl) |
| Memory system | 9-category experience memory with merge and version tracking |
| Model routing | Optional external API dispatch with automatic fallback to built-in |
| Self-check | `python AI-Team/capsule.py doctor` verifies install, config, and connectivity |
| Conflict-safe | Enable/carry never overwrites user-modified files |
| Stdlib only | No third-party Python dependencies; tests run offline |

### Quick Start

1. Copy the `Portable-AI-Team/` folder to your project root.
2. Copy `Python路径.txt.example` to `Python路径.txt`, then set it to your
   Python executable path.
3. Double-click `双击启用团队.cmd` (or run `python AI-Team/capsule.py enable`).
4. Bring up your LLM: copy `LLM配置.example.json` to `LLM配置.json`,
   fill in your own `base_url` / `api_key` / `models`, then run
   `python AI-Team/capsule.py doctor`.
   See [AI-Team/references/llm-接入指南.md](AI-Team/references/llm-接入指南.md)
   for the 30-second walkthrough.
5. Open your IDE and say: "ZH, build me a ..."
6. When done, double-click `双击带走团队.cmd` to carry the team away.

### Modes

| Mode | Use case | Strategy |
| --- | --- | --- |
| `economy` | Simple, low-risk tasks | Minimal context, small/fast models first |
| `balanced` | Default, most tasks | Cost-quality balance; upgrade for complex work |
| `quality` | High-risk or subjective | More analysis; stronger acceptance |

### Configuration

Copy `LLM配置.example.json` to `LLM配置.json` and fill in your API details.
This file is git-ignored and must never be committed. The example file uses
vendor-neutral placeholders only -- no real keys, no internal gateways.

### Platform Notes

Full matrix: [AI-Team/ide-guides/compatibility-matrix.md](AI-Team/ide-guides/compatibility-matrix.md)

- **Codex**: appends to `AGENTS.md` + `.codex/agents/*.toml`.
- **Google Antigravity**: `.agents/rules/` + `.agents/agents/`; AgentC/AgentD subagents.
- **TraeCode**: `.trae/rules/`; sequential role simulation (graceful degradation).
- **Claude Code**: mirrors the team block into `CLAUDE.md` (only when that file
  already exists in the project). Not officially verified.
- **WorkBuddy**: `.workbuddy/rules/portable-ai-team.md`; sequential role
  simulation A->C->B->D->C. Not officially verified.

### Seed Memory

`AI-Team/seed/memory-20261010/` ships a desensitized snapshot of the team's
experience base (error patterns, completion criteria, decisions, effective
solutions, feedback patterns) so the team starts with prior art instead of a
blank slate. It is never auto-merged into `AI-Team/memory/` and never included
in the cross-IDE distribution ZIP.

### Further reading

- [How We Run an AI Engineering Team](docs/articles/how-we-run-an-ai-engineering-team.md) —
  the operating methodology behind the framework: independent acceptance,
  work orders instead of chat history, model routing, and a memory that
  compounds.

### Testing

```bash
python -m unittest discover -s tests -v
python AI-Team/check_compatibility.py --build
```

### License

[Apache License 2.0](LICENSE)

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

### External API Dispatch
`LLM配置.json` holds the API endpoint, key, model pool, routing rules,
timeout, and parallel limit. AgentA can dispatch independent modules to
AgentD and AgentB in parallel (up to 4 tasks) with explicit file
boundaries. When an external API is unavailable, times out, or returns
an error, the result is marked as failed and falls back to
`codex_builtin`; AgentA must re-decide instead of treating the external
reply as acceptance.
For the practical operating rules, see
[Multi-Session Dispatch Playbook](AI-Team/policies/multi-session-dispatch.md).

## 中文

Portable AI Team 是一个可携带的多 Agent AI 编码团队框架，支持五平台
（Codex、Google Antigravity、TraeCode、Claude Code、WorkBuddy）。
复制一个文件夹到任何项目，双击启用，AgentA（调度）与
AgentB/AgentD（实现）、AgentC（按需设计）即开始协作，
上下文开销极低。

一句话：它不只是一个 AI，它是一支行过仗的队伍。

### 为什么省 Token？

- AgentA 派发工单而非完整聊天历史给 AgentB/AgentD：只含文件路径、
  项目路径、允许修改的范围、验收条件。
- 工单、交付、缺陷报告使用紧凑模板；实现者直接修改共享文件，
  不在聊天中重复粘贴代码。
- 经验记忆每次任务只加载相关的 1-3 个类别，
  有单文件字符数上限与单条目数上限。
- 编译、单元测试、文件存在性由工具结果直接判定，
  不依赖模型复述。
- 自动返工最多 2 轮，避免死循环。

### 核心能力

| 能力 | 说明 |
| --- | --- |
| 跨平台 | Codex、Google Antigravity、TraeCode、Claude Code、WorkBuddy（不支持时顺序降级；Claude Code 与 WorkBuddy 标注"未官方验证"） |
| 多 Agent | A（调度）+ B（主实现）+ C（按需设计）+ D（并行实现） |
| 记忆系统 | 9 类经验记忆，支持合并与版本追踪 |
| 模型路由 | 可选外部 API 路由，失败自动降级回内置 |
| 自检 | `python AI-Team/capsule.py doctor` 校验安装、配置与模型连通性 |
| 冲突安全 | 启用/带走都不会覆盖用户修改过的文件 |
| 纯标准库 | 无第三方 Python 依赖，测试离线可跑 |

### 快速开始

1. 把 `Portable-AI-Team/` 文件夹整体复制到业务项目根目录。
2. 把 `Python路径.txt.example` 复制为 `Python路径.txt`，写入你本机 Python 可执行文件路径。
3. 双击 `双击启用团队.cmd`（或运行 `python AI-Team/capsule.py enable`）。
4. 接入模型：把 `LLM配置.example.json` 复制为 `LLM配置.json`，
   填入你自己的 `base_url` / `api_key` / `models`，然后运行
   `python AI-Team/capsule.py doctor`。
   30 秒上手流程见 [AI-Team/references/llm-接入指南.md](AI-Team/references/llm-接入指南.md)。
5. 在 IDE 项目里说"ZH，帮我做一个……"。
6. 完成时双击 `双击带走团队.cmd`。

### 模式

| 模式 | 适用场景 | 策略 |
| --- | --- | --- |
| `economy` | 简单低风险任务 | 最小上下文，小/快模型优先 |
| `balanced` | 默认，多数任务 | 成本质量平衡，复杂实现升档 |
| `quality` | 高风险或主观任务 | 更多分析，更强验收 |

### 配置

把 `LLM配置.example.json` 复制为 `LLM配置.json` 并填入你的 API 信息。
该文件已被 .gitignore 排除，绝不能提交到版本控制。
示例文件只包含厂商中立占位符，无真实密钥、无内部网关。

### 外部 API 调度与并行派单
`LLM配置.json` 定义 API 地址、密钥、模型池、路由、超时和并行上限。
AgentA 可把互不依赖的模块按明确的文件边界并行派单给 AgentB 和 AgentD
（最多 4 路）。外部 API 不可用、超时或返回错误时进入失败降级：
结果标记失败并回退 `codex_builtin`，AgentA 必须重新决策，
不能把外部模型回复当作验收结果。
实战调度方法见
[多会话并行调度手册](AI-Team/policies/multi-session-dispatch.md)。

### 平台说明

完整矩阵：[AI-Team/ide-guides/compatibility-matrix.md](AI-Team/ide-guides/compatibility-matrix.md)

- **Codex**：追加到 `AGENTS.md` 与 `.codex/agents/*.toml`。
- **Google Antigravity**：`.agents/rules/` 与 `.agents/agents/`；AgentC/AgentD 子代理。
- **TraeCode**：`.trae/rules/`；顺序模拟角色（优雅降级）。
- **Claude Code**：把团队区块镜像到 `CLAUDE.md`（仅当该文件在项目中已存在）。未官方验证。
- **WorkBuddy**：`.workbuddy/rules/portable-ai-team.md`；顺序模拟 A->C->B->D->C。未官方验证。

### 种子记忆

`AI-Team/seed/memory-20261010/` 随包提供一份脱敏后的经验快照
（错误模式、完成标准、决策、有效解法、反馈模式），
让团队带着既有经验开工而不是从零开始。
它不会被自动合并进 `AI-Team/memory/`，也不会进入跨 IDE 分发包 ZIP。

### 延伸阅读

- [如何管理一支 AI 工程团队](docs/articles/how-we-run-an-ai-engineering-team.md) —
  框架背后的运作方法论：实现与验收分离、工单而非聊天记录、模型路由、
  会复利的经验记忆。

### 测试

```bash
python -m unittest discover -s tests -v
python AI-Team/check_compatibility.py --build
```

### 许可证

[Apache License 2.0](LICENSE)

### 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。
- AgentA 派发工单而非完整聊天历史给 AgentB/AgentD：只含文件路径、
  项目路径、允许修改的范围、验收条件。
- 工单、交付、缺陷报告使用紧凑模板；实现者直接修改共享文件，
  不在聊天中重复粘贴代码。
- 经验记忆每次任务只加载相关的 1-3 个类别，
  有单文件字符数上限与单条目数上限。
- 编译、单元测试、文件存在性由工具结果直接判定，
  不依赖模型复述。
- 自动返工最多 2 轮，避免死循环。
- 模型路由可选：外部 API 不可用或超时时，每次派单走失败降级回
  内置模型（`codex_builtin`）；并行派单上限 `max_parallel = 4`。
