# LLM 接入指南（30 秒上手）

> 团队通过**一个 OpenAI 兼容网关**接入你公司的模型。不需要为每个模型写代码——改一个 JSON 就行。

## 你要准备什么

1. 一个**可用的 OpenAI 兼容端点**（`/v1/chat/completions` 协议）。常见来源：
   - 公司内部 LLM 网关（大多数企业已有）
   - 自建 vLLM / LiteLLM / one-api
   - 云厂商的 OpenAI 兼容模式（DeepSeek / 通义 / 智谱 / OpenRouter 等）
2. 一个 **API Key**
3. 网关里**实际可用的模型名列表**（`GET /v1/models` 能查到）

## 三步接入

### 第 1 步：复制配置模板
```powershell
Copy-Item .\LLM配置.example.json  .\LLM配置.json
```

### 第 2 步：填三个必填项
编辑 `LLM配置.json`，只改这三处：
```json
{
  "enabled": true,
  "base_url": "https://你的网关地址/v1",
  "api_key": "你的Key"
}
```

### 第 3 步：按路由表填模型名
`models` 里的 7 个角色对应团队的分工，填入你网关里实际存在的模型名：

| 角色 | 用途 | 选型建议 |
| --- | --- | --- |
| `fast` | 测试生成、批量读文件 | 便宜、快、长上下文（≥128K） |
| `agent_b` | 主实现 | 性价比高的代码模型 |
| `balanced` | 代码评审 | 中等推理能力 |
| `strong` | 架构、关键逻辑、DB 迁移、安全 | 最强推理档（高风险路径零容忍） |
| `vision` | 视觉验收、截图、图表 | **必须支持图像输入** |
| `agent_c` | 设计 | 强于 `agent_b` 的模型 |
| `agent_d` | 并行实现（与 B 错开模型防冲突） | 另一个代码模型 |

> 同一个模型可以填给多个角色（省事），但 **`agent_b` 和 `agent_d` 必须不同**，否则触发冲突规则。

`routing` 一般不用动，它只是把任务类型指向上面的角色。

## 验证接入
```powershell
# 离线结构检查（不发请求，只查 JSON 格式）
python AI-Team\llm_dispatch.py --test

# 或跑自检（含真实连通性探测）
python AI-Team\capsule.py doctor
```
`doctor` 会对 `models` 里每个模型发一条最小 ping，全绿即接入成功。

## 常见坑

- **模型名带前缀**：有些网关要求 `default/xxx`、`openai/xxx` 这种前缀。以 `GET /v1/models` 返回的名字为准，原样填。
- **视觉模型不通用**：`vision` 角色填的模型必须真的能吃图。纯文本模型填进去，视觉验收会静默失败。
- **`enabled: false`**：不开启时团队回退到宿主 IDE 的内置模型（`fallback: codex_builtin`），外部派单不生效。
- **Key 泄露**：`LLM配置.json` 已被 git-ignore，**永远不要提交**。泄露立即轮换。
- **闲时降价**：很多公司网关闲时是峰值价的 1/10。批量任务（测试、日志、构建）尽量排闲时跑。

## 不接外部模型也能用

`enabled: false` 时，团队完全跑在宿主 IDE 的模型上，按角色顺序模拟（A → C → B → D → A）。体验完整，只是没有"外部多模型 + 闲时降价"的成本优势。想省钱再开外部网关。

