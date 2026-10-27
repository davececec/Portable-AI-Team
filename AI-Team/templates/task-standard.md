# 标准任务

## 成员模型（按参与成员列出，来源：policies/model-routing.md）

- AgentA（ZH）验收：宿主（具体模型由 ZH 决定）
- AgentB 实现：default/deepseek-v4-flash
- AgentC 设计：default/deepseek-v4-flash；视觉检查：default/qwen3-vl-30b-a3b-instruct
- AgentD 实现：default/deepseek-v4-flash（单独执行）；与 B 并行时=default/qwen38-27b
- 测试生成（fast）：default/qwen38-27b

> 派单时必须写清“XX 当前使用 YY 模型”。B 和 D 禁止同时用同一个模型；模型可由 ZH 临时改派。

## 目标与范围

- 最终需求：
- 项目路径：
- 允许修改：
- 不在范围：
- 必要文件：

## 完成条件

- 验收标准：
- 交付物：
- 回归范围：

## 变更

- 日期 / 增量需求：

仅保留实现所需结论，不重复完整对话。
