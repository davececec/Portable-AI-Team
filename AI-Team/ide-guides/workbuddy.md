# WorkBuddy

> **状态：未官方验证。** WorkBuddy 目前没有公开的官方规则目录规范。本分发包采用**最保守**的方案：把团队规则写进 `.workbuddy/rules/portable-ai-team.md`，其余行为按角色顺序模拟，并在回复中明确报告"顺序降级"。

## 为什么标注未验证

团队在调研 GitHub 上的 WorkBuddy 生态时，发现公开资料大多集中在"把 WorkBuddy/CodeBuddy 账号转成 OpenAI 兼容 API"的反代工具，以及面向 Claude Code/Codex 的请求兼容排障手册；**没有找到官方的项目级 rules 目录约定**。为避免承诺无法保证的能力，本分发包对 WorkBuddy 只做三件事：

1. 写入规则文件 `.workbuddy/rules/portable-ai-team.md`（带胶囊标记，可逆移除）。
2. 始终按 `A -> 按需 C -> B -> D -> 按需 C -> A` 顺序执行，不声称独立子代理或干净上下文隔离。
3. 在兼容矩阵与本文件中明确标注"未官方验证"。

## 启用时发生什么

- 双击启用（或 `python AI-Team/capsule.py enable`）会创建 `.workbuddy/rules/portable-ai-team.md`。
- 若你的 WorkBuddy 版本使用的规则目录不是 `.workbuddy/rules/`，请把规则文件手动放到你的规则目录，路径保持 `portable-ai-team.md`，并更新 `AI-Team/capsule.py` 的 `BRIDGES` 中 `workbuddy-rule` 一行（或反馈给维护者统一改）。

## 能力边界

- **规则加载**：取决于 WorkBuddy 版本是否识别 `.workbuddy/rules/`。若不识别，团队规则不会自动生效，需手动粘贴规则内容到 WorkBuddy 的项目规则设置。
- **并行实现**：无子代理，顺序执行。
- **视觉检查**：无专用视觉通道，主代理按角色顺序走查并报告降级。
- **冲突规则**：不适用（无并发 B/D）。

## 验证方式

- `python AI-Team/capsule.py validate` 确认规则文件存在且未改动。
- 发起"ZH，给我做一个……"任务，观察 WorkBuddy 是否加载了规则；未加载则按上文手动放置。
- 把你的 WorkBuddy 版本号和实际规则目录反馈到本文件，逐步把"未验证"改成"已验证"。

## 待办（社区反馈后）

- 确认 WorkBuddy 官方项目规则目录后，更新 `BRIDGES` 与本文。
- 若 WorkBuddy 支持子代理或专用视觉通道，补充能力行并去掉"顺序降级"。
