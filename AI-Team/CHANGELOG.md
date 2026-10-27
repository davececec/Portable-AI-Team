# 团队变更记录（CHANGELOG）

本文件是 Portable AI Team 升级、改动、新增功能的唯一溯源记录。凡是团队自身（胶囊、`AI-Team/`、桥接、规则、模板、配置、脚本、记忆）的变更，都必须记录在这里；业务项目代码变更不记入。

## 记录规则

- 每次升级/改动/新增功能，在“最新在上”的位置追加一条。
- 每条必含：日期、版本或标记、改动类型（新增/修改/修复/移除/升级）、涉及文件、原因与影响、验证方式。
- 修改了 `LLM配置.json`、`team.json`、角色资料、模板或路由策略时，同步核对引用一致性。
- 版本号变更时同步更新 `AI-Team/team.json` 与 `团队状态.json` 的版本字段。
- ZH 每次完成团队自身变更后，收尾时必须更新本文件，并在对应工单尾部追加：`变更记录：已更新 CHANGELOG`。

## 2026-10-13 UI kit 入位 + 数据配色系统（第 8 章）

- 类型：新增 / 修改
- 内容：①三风格 UI 设计标准包入 `AI-Team/ui-design-kit/`（规范 + design-tokens.css + shopeers-ui.css + shopeers-echarts-theme.js + echarts.min.js + 3 风格 demo + AGENTS/README），修复 `memory/index.md` 失效指向 `../UI/UI-DESIGN-STANDARD.md`，注明优先级（项目自有标准 > kit 默认，未指定默认 Light SaaS）。②`UI-DESIGN-STANDARD.md` 新增「第 8 章 数据配色系统」（同实体同色、语义色+类别色、矩阵 √比例色阶、log10 轴、负值红字 #F87171、占比空态、趋势语义双色、参考实现），原第 8 章交付检查清单顺延为第 9 章并新增配色检查项。③`design-tokens.css` 新增 `--kind-1..9` / `--ws-1..11` / `--data-neg` token；README 新增第 4 条使用方式。
- 涉及文件：`AI-Team/ui-design-kit/*`、`AI-Team/memory/index.md`（RZNY 业务侧 palette.js 不入本文件，见 RZNY 项目时间线）。
- 原因与影响：UI 规范与配色体系可供后续项目直接复用；新页面派单 C 时 spec 必读 kit 对应风格章。
- 验证：kit 10 文件齐、index.md 指向有效；RZNY 浏览器实测（排名多色、9 色介质图、√色阶矩阵、log10 轴）console 零报错，见 RZNY 时间线 2026-10-13。

## 2026-10-12 桥接清单字节对齐

- 类型：修复
- 内容：`state/installation.json` 中签约给项目 AGENTS.md 的团队区块原以 LF 存储，磁盘文件为 CRLF，导致 `capsule.py validate` 持续报“AGENTS.md 团队区块已修改”、`carry` 无法移除区块完成复位。按磁盘原始字节重建 stored block（前导/结尾换行一并对齐）。
- 涉及文件：`state/installation.json`；项目 `AGENTS.md` 未改动。
- 验证：`capsule.py validate` 返回“团队桥接校验通过”。

## 2026-10-12 公司大模型网关参考文档

- 类型：新增文档
- 内容：新增 `AI-Team/references/gwm-chat-api.md`，整理 `llmproxy.gwm.cn` 三接口速查（Chat 文本生成 / Chat 图像理解含思考模式 / Completions 纯文本补全），含请求字段、响应解析、LangChain/LlamaIndex/HTTP 示例与实测核对结论。
- 涉及文件：`AI-Team/references/gwm-chat-api.md`（新增）；`AI-Team/memory/index.md`、`AI-Team/templates/task-standard.md`、`AI-Team/templates/task-micro.md`（加入引用入口，直连网关任务先查本参考，避免重复探测）。
- 影响：团队编写直连网关的脚本/业务代码时可直接复用已验证的调用格式，减少测试消耗与试错。
- 验证：文档内端到端实测 `default/qwen3-vl-30b-a3b-instruct` 图像理解、`default/minicpm-v-2-6` 图像可用；`default/glm-4v-9b` 网关不存在（403），保留为参考资料说明。

## 2026-10-12 子代理通道降级规则 + 视觉接口配方

- 类型：修复 / 新增规则
- 背景：Codex 内置子代理在当前环境（Codex++ 中继 → `llmproxy.gwm.cn`，仅支持 Chat Completions）派发稳定报 `unsupported_encrypted_agent_content`；此前团队会盲目重试 3 轮后卡死。
- 涉及文件：
  - `AI-Team/policies/model-routing.md`：新增“内置子代理通道可用性告警”“故障与降级”章节；首次派单只探针 1 次，命中该协议错误即判定环境限制并顺序降级，禁止盲目重试；补充第 5 条“降级标注”规则。
  - `AI-Team/agents/AgentA.md`：多模型并行派单节新增探针与降级判定；无子智能体能力节新增降级任务标注要求。
  - `AI-Team/adapters/codex/AGENTS.md`：Codex 桥接同步探针、降级与禁止重试规则。
  - `AI-Team/capsule.py`：启用器生成的新项目 AGENTS.md 区块加入探针+降级句，新部署即生效。
  - `README.md` / `START-HERE.md`：新增“已知平台限制与排障”说明。
  - `AI-Team/memory/effective-solutions.md`：新增已验证的视觉接口配方（`/chat/completions` 图片理解格式）。
- 影响：子代理不可用时团队不再卡死，自动按角色顺序模拟执行（对话+工单各标一次，收尾 A 独立验收再标一次）；视觉理解可走外部 Chat Completions 通道。
- 验证：`py_compile` 通过；`llm_dispatch.py --test` 全模型可用；视觉接口实测 `default/qwen3-vl-30b-a3b-instruct`、`default/minicpm-v-2-6` 成功，`default/glm-4v-9b` 不存在（403）。

## 2026-10-10 v3.0.0 基线

- 类型：版本基线
- 内容：团队胶囊 v3.0.0 首发。AgentB 与 AgentD 并行分担；`LLM配置.json` 外部 API 多模型调度（`llm_dispatch.py` 探测/单发/并行/失败降级）；`capsule.py` enable/validate/carry/merge；Codex、Google Antigravity、TraeCode 三端桥接与兼容矩阵；记忆合并兼容 v2.3+。
- 详细说明见 `README.md` 的“V3.0 变更”“外部模型与并行派单”章节。
