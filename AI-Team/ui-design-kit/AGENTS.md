# AGENTS.md

本项目内置一套包含三种 UI 风格的单文件设计规范。开发代理在生成/修改任何前端页面**之前**必须先读取 `UI-DESIGN-STANDARD.md` 第 0 章「使用方式」，确定风格后严格按对应章节执行。

## 风格速查
| 风格 | 章节 | 参考实现 | 触发关键词 |
| --- | --- | --- | --- |
| 01 Light SaaS（浅色） | UI-DESIGN-STANDARD.md 第 3 章 | `shopeers-demo.html` | 浅色 / Light / SaaS / Shopeers |
| 02 Dark SaaS（暗色） | 第 4 章 | `shopeers-demo-dark.html` | 暗色后台 / Dark SaaS / 夜间模式 |
| 03 Dark Screen（科技大屏） | 第 5 章 | `index.html` | 大屏 / 监控 / 能源 / 指挥 |

用户未指定风格时默认 Style 01。CSS 变量可引用 `design-tokens.css`，ECharts 主题可引用 `shopeers-echarts-theme.js`。

## 交付
- 用 Playwright（Edge/Chrome）对 1600 桌面 + 390 移动两个视口截图自检：无溢出、无遮挡、图表非空白、文字不互相压盖，再交付。
