# Portable AI Team

**A portable, multi-agent AI coding team that lives inside a single folder.**

[English](#english) | [中文](#中文)

---

## English

Portable AI Team is a low-token multi-agent coding framework that works across
IDEs (Codex, Google Antigravity, TraeCode). Copy one folder into any project,
double-click to enable, and a team of agents starts working with minimal
context overhead: AgentA (orchestrator), AgentB/AgentD (implementers),
and AgentC (on-demand designer).

### Why Low-Token V2?

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
| Cross-IDE | Codex, Google Antigravity, TraeCode (graceful degradation) |
| Multi-agent | A (orchestrator) + B (main impl) + C (design) + D (parallel impl) |
| Memory system | 9-category experience memory with merge and version tracking |
| External LLM | Optional API-based dispatch with fallback to built-in |
| Conflict-safe | Enable/carry never overwrites user-modified files |
| Stdlib only | No third-party Python dependencies; tests run offline |

### Quick Start

1. Copy the `Portable-AI-Team/` folder to your project root.
2. Edit `Python路径.txt` to your Python executable path.
3. Double-click `双击启用团队.cmd` (or run `python AI-Team/capsule.py enable`).
4. Open your IDE and say: "ZH, build me a ..."
5. When done, double-click `双击带走团队.cmd` to carry the team away.

### Modes

| Mode | Use case | Strategy |
| --- | --- | --- |
| `economy` | Simple, low-risk tasks | Minimal context, small/fast models first |
| `balanced` | Default, most tasks | Cost-quality balance; upgrade for complex work |
| `quality` | High-risk or subjective | More analysis; stronger acceptance |

### Configuration

Copy `LLM配置.example.json` to `LLM配置.json` and fill in your API details.
This file is git-ignored and must never be committed.

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

## 中文

Portable AI Team 是一个可携带的多 Agent AI 编码团队框架，支持跨 IDE
（Codex、Google Antigravity、TraeCode）运行。把一个文件夹复制到任何项目，
双击启用，AgentA（调度）、AgentB/AgentD（实现）、AgentC（按需设计）
即刻协同工作，上下文开销极低。

### 为什么更省 Token？

- AgentA 不传完整聊天历史给 AgentB/AgentD，只派发工单路径、
  项目路径、允许修改范围和完成条件。
- 工单、交付和缺陷使用紧凑模板；实现者直接修改共享文件，
  不在聊天里重复输出完整代码。
- 先读记忆索引，每次仅加载相关的 1-3 类记忆，
  并对单条记录、文件条目数和字符数设上限。
- 编译、单元测试、文件存在性由工具结果直接判定，
  不消耗模型复述。
- 自动返工最多 2 轮，避免无上限循环。

### 核心特性

| 特性 | 说明 |
| --- | --- |
| 跨 IDE | Codex、Google Antigravity、TraeCode（无子智能体时顺序降级） |
| 多 Agent | A（调度）+ B（主实现）+ C（按需设计）+ D（并行实现） |
| 记忆系统 | 9 类经验记忆，支持合并和版本追踪 |
| 外部模型 | 可选 API 调度，失败自动回退内置 |
| 冲突安全 | 启用/带走绝不覆盖用户修改过的文件 |
| 纯标准库 | 无第三方 Python 依赖；测试离线运行 |

### 快速开始

1. 把 `Portable-AI-Team/` 文件夹整体复制到业务项目根目录。
2. 编辑 `Python路径.txt`，填入你的 Python 可执行文件路径。
3. 双击 `双击启用团队.cmd`（或运行 `python AI-Team/capsule.py enable`）。
4. 用 IDE 打开项目，说"ZH，给我做一个……"。
5. 完成时双击 `双击带走团队.cmd`。

### 模式

| 模式 | 适用场景 | 策略 |
| --- | --- | --- |
| `economy` | 简单、低风险任务 | 最小上下文，小型/快速模型优先 |
| `balanced` | 默认，大多数开发任务 | 成本与质量平衡，复杂实现才升级模型 |
| `quality` | 高风险或强主观任务 | 允许更多必要分析，优先强化主观验收 |

### 配置

把 `LLM配置.example.json` 复制为 `LLM配置.json` 并填入你的 API 信息。
该文件已被 .gitignore 排除，绝不能提交到版本控制。

### 测试

```bash
python -m unittest discover -s tests -v
python AI-Team/check_compatibility.py --build
```

### 许可证

[Apache License 2.0](LICENSE)

### 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。
