# UI Design Kit（三风格标准包）

一套可拷贝到任意项目的 UI 设计标准 + 参考实现。下一个项目开始前，把本文件夹整个拷过去即可。

## 文件清单

| 文件 | 用途 | 拷到新项目？ |
| --- | --- | --- |
| `UI-DESIGN-STANDARD.md` | 单文件设计规范，含三种风格的完整标准 | 必拷 |
| `AGENTS.md` | 让 CODEX 自动读取规范并按风格执行 | 必拷 |
| `design-tokens.css` | 亮/暗双主题 CSS 变量包 | 按需 |
| `shopeers-ui.css` | 现成组件样式（卡片/按钮/表格/进度条等） | 按需 |
| `shopeers-echarts-theme.js` | ECharts 主题（注册 `shopeers`） | 按需 |
| `echarts.min.js` | 本地图表库（演示页依赖） | 按需 |
| `shopeers-demo.html` | 风格 01 浅色 SaaS 参考实现 | 按需 |
| `shopeers-demo-dark.html` | 风格 02 暗色 SaaS 参考实现 | 按需 |
| `index.html` | 风格 03 科技大屏参考实现 | 按需 |

## RZNY 2026-10-24 全局重构基准

- 该基准由 2026-10-24 设计系统演示页确认后提炼而来，是 RZNY 全局 UI 改造的最高优先级规范。
- 文件：`RZNY-2026-10-24-BASELINE.md`
- 说明：完整基准不设行数限制，覆盖 token、字体、灰阶、对比度、语义色、数据色、控件、表格、KPI、图表、状态标签、暗亮双主题、迁移规则、兼容要求和验收清单。
- 可视化对比：`rzny-2026-10-24-current-vs-improved.html`
- 适用范围：RZNY 的 8002 开发页和 8000 展示页；8000 仍遵守展示页白名单，不新增设计系统入口。
- 核心变化：正文 15px/500、meta 12px/500、AA 灰阶、等宽数字、统一控件/表格/KPI/图表/状态标签与暗亮双主题 token。
- 归档资产：`design-system-demo-2026-10-24/` 保留源码快照与独立展示效果；该页面已从 RZNY 8002 移除，只作为跨项目参考，不进入 RZNY 项目路由。

## 新项目使用方式

1. 把整个 `ui-design-kit` 文件夹拷到新项目根目录（或至少拷 `UI-DESIGN-STANDARD.md` + `AGENTS.md`）。
2. 对 CODEX 说，例如：
   - 「按 AGENTS.md，用浅色 SaaS 风格做一个订单管理页」→ 走规范第 3 章
   - 「用暗色 SaaS 风格做」→ 第 4 章
   - 「用科技大屏风格做」→ 第 5 章
   - 不指定风格时默认浅色 SaaS。
3. 参考实现是静态 HTML，双击或用本地服务器打开均可；图表渲染依赖同目录的 `echarts.min.js`。
4. 数据可视化项目（能源/生产/运营监控）配色按规范第 8 章「数据配色系统」执行：色板集中定义（JS palette + CSS `--kind-*`/`--ws-*` token）、同实体同色、矩阵 √比例色阶、log10 轴、负值红字等规则。参考实现：RZNY `apps/web/src/features/energy/palette.js`。

## 三种风格速查

| 风格 | 章节 | 主色 | 参考实现 |
| --- | --- | --- | --- |
| 01 Light SaaS | 第 3 章 | #2563EB | `shopeers-demo.html` |
| 02 Dark SaaS | 第 4 章 | #3B82F6 | `shopeers-demo-dark.html` |
| 03 Dark Screen | 第 5 章 | #10B981 | `index.html` |
