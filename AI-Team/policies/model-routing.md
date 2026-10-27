# 模型路由

此建议适用于 Codex、Trae、Antigravity 及其他支持多模型的 IDE。胶囊根目录 `LLM配置.json` 定义外部 API 模型池。

## 派单时成员模型清单（ZH 建单必带）

ZH 每张工单都带“成员模型”一栏，按参与成员直接引用下表；该表是成员模型的唯一事实源，`LLM配置.json` 与模板默认值都必须与本表同步。**建单和派单时必须明确显示当前模型，例如“AgentB 当前使用 default/deepseek-v4-flash”。**

| 成员/职责 | 优先模型 | 当前生效模型 | 说明 |
| --- | --- | --- | --- |
| AgentA（ZH）决策验收 | 宿主 | 宿主 | 显示“宿主”；模型选择由 ZH 决定 |
| AgentB 实现 | default/deepseek-v4-flash | default/deepseek-v4-flash | 默认实现模型 |
| AgentC 设计 | default/deepseek-v4-flash | default/deepseek-v4-flash | 复杂设计可由 ZH 临时改派 default/glm5-3-flash |
| AgentC 视觉检查 | default/qwen3-vl-30b-a3b-instruct | default/qwen3-vl-30b-a3b-instruct | 多模态专用 |
| AgentD 实现 | default/deepseek-v4-flash（单独执行） | default/qwen38-27b | 与 AgentB 并行时必须错开模型；本配置用 qwen38-27b 防冲突 |
| 测试生成（fast） | default/qwen38-27b | default/qwen38-27b | 独立测试槽位 |
| 批量读取/排查（fast） | default/glm5-3-flash | default/glm5-3-flash | 大批量文件/日志/CSV/点位表读取、定位与摘录；仅限新建短会话并只传工单路径+文件清单，禁止携带长历史（2026-10-09 会话过大事故）或用于代码实现/验收 |

> B/D 并行冲突规则：B 和 D 不得同时使用同一个模型。B 保持 `default/deepseek-v4-flash` 时，D 默认切换到 `default/qwen38-27b`。ZH 可以临时改派，但必须在工单里写清。

> 模型变更时：先改本表与 `LLM配置.json`，再同步 `templates/task-standard.md`、`templates/task-micro.md` 的默认值。所有具体模型分配最终由 ZH 决定。

## 启动检查

胶囊启用后 AgentA 首次派单前，运行：

```powershell
python AI-Team/llm_dispatch.py --test
```

结果决定运行模式：

- 全部可用，外部 API 多模型并行。
- 部分可用，按可用模型路由，不可用任务回退内置执行。
- 全不可用，纯内置子代理或顺序模拟模式。

## 内置子代理模型路由

| 角色 | 建议 override 模型 | 理由 |
| --- | --- | --- |
| AgentB 实现 | default/deepseek-v4-flash | 快、便宜、擅长代码生成 |
| AgentC 设计 | default/deepseek-v4-flash | UI 方案可先走统一实现模型；复杂设计由 ZH 改派 strong |
| AgentC 视觉检查 | default/qwen3-vl-30b-a3b-instruct | 多模态，能看截图 |
| AgentD 实现 | default/qwen38-27b | 与 B 并行时强制错开模型，降低调用冲突 |
| AgentA 决策验收 | 继承宿主模型 | 需要最强推理和全局上下文 |

> 测试生成默认走 `LLM配置.json`：`routing.test_generation = fast` → `models.fast = default/qwen38-27b`（外部 API，不占宿主上下文）。

## 外部 API 路由

按 `LLM配置.json` 的 `routing` 字段分配。单发命令：

```powershell
python AI-Team/llm_dispatch.py --dispatch --role agent_b --prompt "工单摘要" --files "a.py,b.py"
```

并行任务文件用：

```powershell
python AI-Team/llm_dispatch.py --dispatch-parallel --tasks tasks.json
```

返回只包含：修改文件列表、测试结果、遗留风险。禁止返回完整代码。失败结果标记错误和 `fallback: codex_builtin`；AgentA 必须决定重试、换角色或内置执行。

## Token 控制铁律

- 任何子代理（内置或外部）只接收：工单路径、项目路径、允许修改范围、文件列表、完成条件。
- 只返回：修改文件、测试结果、风险。禁止返回完整代码或完整对话。
- 外部 API Token 走代理额度，不占 Codex 上下文；因此重活尽量路由到外部模型。
- 并行上限按 `LLM配置.json` 的 `max_parallel` 控制，最大 4，防止并发风暴。
- 确定性检查（编译/测试/退出码）由工具直接执行，不使用任何模型判断。
- AgentB 和 AgentD 禁止并发编辑同一文件；存在交叉时必须先拆清边界。

## 降级规则

1. 外部模型不可用时回退内置子代理，并在工单标注 `fallback=codex_builtin`。
2. 内置子代理不可用时，不得静默改由 AgentA 亲自实现。
3. 同一任务连续 2 次失败，可更换模型或角色重试。
4. 同一任务连续 3 次失败，AgentA 停止派单，向用户报告并等待决策。
5. 降级进入“顺序降级：角色顺序模拟”时，必须在工单和最终答复标注：降级方式、各角色实际模型、是否缺少独立上下文隔离、未验证项；若 AgentB 没有真实交付，不得写成“AgentB 已完成”。
