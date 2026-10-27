# UI Design Standard（三风格版 · 单文件规范）

> 把本文件拷到任意项目根目录。用户指名风格时，开发代理（CODEX/Cursor/Copilot）直接按对应章节执行。
> 配套可选引用：`design-tokens.css`（CSS 变量包）、`shopeers-echarts-theme.js`（ECharts 主题）。
> RZNY 全局 UI 重构以【第 10 章 RZNY 2026-10-24 UI Baseline】为准；第 2、3、4、5、7 章与其冲突时，RZNY 优先使用第 10 章。

## 0. 使用方式（代理先读）
- 用户说「浅色 SaaS / Light / SaaS / Shopeers 风格」→ 按【第 3 章】执行
- 用户说「暗色 SaaS / Dark SaaS / 深色后台 / 夜间模式」→ 按【第 4 章】执行
- 用户说「大屏 / 监控 / 能源 / 指挥 / 科技大屏」→ 按【第 5 章】执行
- 用户未指定 → 默认 Style 01（浅色 SaaS）
- 项目涉及数据可视化（能源/生产/运营监控）→ 数据配色一律按【第 8 章 数据配色系统】：同实体同色、色板集中定义
- 生成代码必须遵守【第 1、2、7 章】的公共规则；颜色一律走 CSS 变量
- 交付前用 Playwright（Edge/Chrome）截 1600 桌面 + 390 移动两张图自检：无溢出、无遮挡、图表非空白

## 1. 公共设计原则
1. **Clarity first（清晰优先）**：用留白、层级和颜色区分信息优先级，装饰不干扰数据。
2. **Human SaaS（克制的现代感）**：低饱和色块、小圆角、柔和阴影，界面可信且轻盈，不炫技。
3. **Data density（数据密度）**：表格、图表、KPI 紧凑，但每个区块保留呼吸感。
4. **Quiet motion（安静动效）**：只用 0.2s 轻量过渡，不做弹跳、发光或复杂特效。

### 公共技术规则（三种风格都遵守）
- 颜色、间距、圆角、阴影一律定义在 `:root` CSS 变量里，组件禁止写死颜色。
- 数字（KPI、金额、表格数值、图表标签）开启 `font-variant-numeric: tabular-nums`。
- 图标一律内联 SVG（stroke 1.8、round cap），禁止 emoji 当图标。
- 过渡统一 `0.2s ease`；按钮 hover 主色变一档；卡片 hover 只加深阴影或微提亮背景。
- 禁用：弹跳动画、毛玻璃 backdrop-filter、发光/荧光渐变边框、彩虹配色、DataV 式 2018 科技装饰。
- 布局：卡片圆角 12-16px；不卡片套卡片；页面区块用通栏，卡片只用于独立条目/弹窗/工具面板。
- 状态色成对使用：实色给小元素（点、条、图标），soft 浅色给标签底与背景。

## 2. 公共字体层级
字体族：`Inter, system-ui, -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif`

| 层级 | 字号 / 字重 | 用途 |
| --- | --- | --- |
| Display | 38px / 800 / letter-spacing -0.04em | 页面主标题或关键成果，一屏只出现一次 |
| Page title | 22px / 700 / -0.02em | 页面标题 |
| Section title | 16px / 600 | 卡片标题、面板标题 |
| Body | 14px / 400-500 | 默认正文与描述 |
| Label | 13px / 500 | 表单标签、KPI 名称、辅助导航 |
| Meta | 11px / 500（弱化色） | 说明、时间、表格表头、弱化信息 |

规则：不用 viewport 缩放字体；letter-spacing 默认 0（大标题可 -0.02 ~ -0.04em）；文字必须在容器内换行/自适应，禁止溢出压盖相邻内容。

## 3. Style 01 · Light SaaS（浅色 SaaS）
适用：后台管理、电商分析、订单/客户/营收报表、SaaS 产品。参考实现：`shopeers-demo.html`。

### 3.1 色彩 Token
```css
:root{
  --bg:#F7F8FA;            /* 页面背景 */
  --surface:#FFFFFF;       /* 卡片/侧边栏/按钮底 */
  --surface-muted:#F9FAFB; /* 表格 hover 行 */
  --surface-hover:#F4F6F9; /* 导航/图标按钮 hover */
  --track:#F0F2F5;         /* 进度条轨道 */
  --border:#ECEEF2;        /* 卡片边框 */
  --border-strong:#E4E7EC; /* 控件边框 */
  --text-1:#101828;  --text-2:#475467;  --text-3:#98A2B3;  --text-4:#667085;
  --primary:#2563EB; --primary-hover:#1D4ED8; --primary-active:#1949C0;
  --primary-soft:#EAF1FE; --primary-soft-2:#DCE9FD;
  --success:#12B76A;  --success-deep:#067647;  --success-soft:#ECFDF3;
  --warning:#F79009;  --warning-deep:#B54708;  --warning-soft:#FFF6E6;
  --danger:#F04438;   --danger-deep:#B42318;   --danger-soft:#FEF3F2;
  --info:#3B82F6;     --info-soft:#EFF6FF;
  --shadow-xs:0 1px 2px rgba(16,24,40,.05);
  --shadow-sm:0 2px 4px -1px rgba(16,24,40,.06);
  --shadow-md:0 4px 12px -2px rgba(16,24,40,.08);
  --shadow-lg:0 12px 28px -8px rgba(16,24,40,.16);
  --shadow-primary:0 4px 12px -3px rgba(37,99,235,.45);
}
```
- 品牌蓝 `#2563EB` 只用于主按钮、选中态、关键强调。
- 图表色板顺序：`#2563EB, #12B76A, #F79009, #F04438, #7C3AED, #06B6D4`。
- 唯一允许的渐变：logo 方块（135deg #3B82F6 → #1D4ED8）。

### 3.2 布局
- 结构：固定侧边栏 244px（白底，右边框 1px #ECEEF2）+ 吸顶工具栏 64px + 滚动内容区（padding 24px，max-width 1440px）。
- 间距基准 4px（4/8/12/16/20/24/32/40）；卡片间距 16px；卡片内边距 20px。
- KPI 区 grid 4 列 gap 16px。
- 圆角：卡片 16px；按钮/输入 8-10px；徽章/进度条 999px；禁止 20px 以上大圆角。

### 3.3 组件
- 主按钮：#2563EB 底白字，高 36px，圆角 10px，hover #1D4ED8，带主色软阴影。
- 次按钮：白底 + 1px #E4E7EC 边，hover 边 #D0D5DD 底 #FCFCFD。
- 输入/搜索：默认灰底 #F4F6F9 无边框；focus 白底 + 边 #2563EB + 外圈 3px #EAF1FE；搜索框内放 kbd 快捷键（白底 1px 边）。
- 图标按钮：36px 方形圆角 10px，hover 底 #F0F2F5。
- 侧边导航项：高 38px 圆角 10px，hover 底 #F4F6F9，active 底 #EAF1FE 字 #2563EB。
- 状态 pill：999px 圆角、11px/600、soft 底 + deep 字。
- 进度条：高 6px，轨道 #F0F2F5，填充语义色。
- 表格：表头 10.5-11px/600 大写 #98A2B3，行分隔线 #ECEEF2，hover 行底 #F9FAFB，数字右对齐。
- 缩略图 chip：30px 圆角 9px，soft 底 + 主色图标。

### 3.4 图表（ECharts）
- 背景透明；坐标轴不画轴线/刻度，标签 10.5-11px #98A2B3，分割线 #F2F4F7（横向细实线）。
- 折线：主线 2-2.4px #2563EB + 面积渐变 rgba(37,99,235,.16~.24) → 0；对比线 1.6px 虚线 #98A2B3。
- 柱状：宽 ≤20px，顶部圆角 4px，非高亮 #D0D5DD，高亮 #2563EB，高亮柱顶加 10px 数值标签。
- tooltip：白底、1px #ECEEF2 边、圆角 10px、阴影 0 8px 24px -6px rgba(16,24,40,.16)。
- legend：7px 圆点、11px 字 #475467。

### 3.5 响应式
| Breakpoint | Layout | 行为 |
| --- | --- | --- |
| ≥1280px | 4 列 | 完整侧边栏，KPI 四列，主图表占 2/3 宽 |
| 1024-1279px | 2-3 列 | 侧边栏收成 72px icon rail |
| 768-1023px | 2 列 | 侧边栏改抽屉 + 遮罩，表格可横向滚动 |
| <768px | 1 列 | KPI 堆叠，筛选器收起，操作按钮整行 |

## 4. Style 02 · Dark SaaS（暗色 SaaS）
适用：夜间模式后台、开发者工具、分析控制台。与 Style 01 同结构同间距，只换色彩与阴影。参考实现：`shopeers-demo-dark.html`。

### 4.1 色彩 Token
```css
:root, html[data-theme="dark"]{
  --bg:#0A0C10;            /* 近黑带蓝调，禁止纯黑 */
  --card:#13161E;          /* 卡片/顶栏 */
  --card-hover:#161A24;    /* hover 微提亮 */
  --bg-deep:#0D1017;       /* 侧边栏/输入底 */
  --track:#1B202B;
  --border:#1F2330;
  --border-strong:#2A2F3D;
  --text-1:#F4F6F8;  --text-2:#9CA3B4;  --text-3:#5C6373;
  --primary:#3B82F6;  --primary-hover:#2563EB;
  --primary-soft:rgba(59,130,246,.14); --primary-soft-2:rgba(59,130,246,.22);
  --success:#22C55E;  --success-deep:#86EFAC;  --success-soft:rgba(34,197,94,.12);
  --warning:#F59E0B;  --warning-deep:#FBBF24;  --warning-soft:rgba(245,158,11,.12);
  --danger:#EF4444;   --danger-deep:#FCA5A5;   --danger-soft:rgba(239,68,68,.12);
  --info:#3B82F6;     --info-soft:rgba(59,130,246,.12);
  --shadow-sm:0 1px 3px rgba(0,0,0,.3);
  --shadow-md:0 4px 12px rgba(0,0,0,.4);
  --shadow-lg:0 12px 32px rgba(0,0,0,.5);
}
```

### 4.2 与 Style 01 的差异要点
- 主色提亮到 `#3B82F6`，hover 反而变深 `#2563EB`（暗底上更深 = 更按下）。
- soft 底全部改用 rgba 低透明，禁止搬用亮色系的实色 soft。
- 阴影全部用纯黑投影（暗色下阴影要更重）。
- 卡片 hover：背景提亮 `#13161E → #161A24` + 阴影加深。
- 导航 active 字用 `#60A5FA`（比主色亮一档保对比度）。
- 图表：轴线 #2A2F3D、分割线 #1F2330、标签 #5C6373；tooltip 底 #1B202B 边 #2A2F3D 阴影纯黑；折线面积 rgba(59,130,246,.24)→0；数据点描边色用卡片底 #13161E（不是白）。
- 色板顺序：`#3B82F6, #22C55E, #F59E0B, #EF4444, #8B5CF6, #06B6D4`。
- 响应式断点与 Style 01 完全一致。
- 禁止：纯黑 #000000 背景；大面积高饱和色块。

## 5. Style 03 · Dark Screen（现代暗色科技大屏）
适用：能源监控、运维监控、指挥大屏、24h 值守控制台。参考实现：`index.html`。
要点：现代暗色大屏，不是 DataV 老式荧光绿大屏；翡翠绿主色 + 等宽数字 + 蓝黑底。

### 5.1 色彩 Token
```css
:root{
  --bg:#0A0C10;        --bg-sidebar:#0D1017;
  --card:#13161E;      --card-hover:#161A24;
  --border:#1F2330;    --border-hover:#262B3A;
  --axis:#2A2F3D;
  --primary:#10B981;   --primary-hover:#28C08E; /* hover 变亮 10% */
  --text:#F4F6F8;      --text-2:#9CA3B4;        --text-3:#5C6373;
  --success:#22C55E;   --warning:#F59E0B;       --danger:#EF4444;   --info:#3B82F6;
}
```
- 图表色板顺序（固定）：`#10B981, #3B82F6, #F59E0B, #EF4444, #8B5CF6, #06B6D4`。
- 翡翠绿 `#10B981` 只做品牌/正向强调，不铺满。

### 5.2 字体（大屏特殊规则）
- 正文 Inter（同第 2 章）；**数字一律 JetBrains Mono**（'JetBrains Mono', 'SF Mono', Consolas, monospace）。
- 大数字：28-36px / 700 / 等宽。
- 卡片标题：13px / 500 / #9CA3B4。小字标注：11px / #5C6373。

### 5.3 布局
- 左侧栏：宽 220px、固定定位、背景 #0D1017，导航分组（如 运营/智能/设备/系统）。
- 顶栏：高 56px、背景 #13161E、底部 1px #1F2330；面包屑 + 通知 + 头像。
- 内容区 padding 24px；KPI 4 列 gap 16px。
- 卡片：圆角 12px（比 SaaS 风格利落一档）、内边距 20px、间距 16px。
- 阴影：rest 0 1px 3px rgba(0,0,0,.3)；hover 0 4px 12px rgba(0,0,0,.4)。

### 5.4 组件
- 卡片 hover：背景提亮到 #161A24（0.2s ease），不只加阴影。
- 主按钮：#10B981 底，hover 变亮 10%（#28C08E）。
- 状态 pill：半透明底 + 语义色字（如 rgba(34,197,94,.12) + #4ADE80）。
- 排名进度条：轨道 #1F2330，高 6px，圆角 999px，填充主色或色板前几位。
- 告警列表：左侧 3px 语义色竖条，正文 13px，时间 11px #5C6373。
- 环形仪表盘（节能率）：gauge 描边 #10B981→#3B82F6 渐变，中心大数字等宽 32px。

### 5.5 图表（ECharts）
- 背景透明；轴线 #2A2F3D；分割线 #1F2330；文字 #5C6373（10-11px）。
- 折线：2px 主色，面积渐变主色 20% → 0。柱状：顶部圆角 4px。数据标签：10px 等宽。
- tooltip：底 #161A24、边 #2A2F3D、圆角 10px、阴影 0 4px 12px rgba(0,0,0,.5)。

### 5.6 大屏标配模块
1. 左侧导航（分组：运营/智能/设备/系统）
2. 顶栏（面包屑 + 通知 + 头像）
3. 4 个 KPI 卡（总能耗/空耗金额/延时异常/单耗）
4. 大折线图（24h 能耗趋势）
5. 车间排名列表（带进度条）
6. 柱状图（本周能耗）
7. 环形仪表盘（节能率）
8. 告警列表

### 5.7 响应式（大屏优先）
- ≥1440px：完整 4 列 KPI，大折线占 2/3 宽。
- 1024-1439px：KPI 2 列，图表两两堆叠。
- ≤768px：单列，侧边栏变抽屉，大数字缩到 28px。

## 6. 附录：可直接复制的 CSS 变量包
三套 `:root` 见 3.1 / 4.1 / 5.1；同一项目要亮暗切换时用 3.1 作 `:root` 默认值、4.1 放进 `html[data-theme="dark"]` 覆盖（与 `design-tokens.css` 内容一致）。

## 7. ECharts 通用主题（三种风格共用骨架）
```js
// echarts.registerTheme 骨架，具体颜色取对应风格的 token
{
  backgroundColor: 'transparent',
  textStyle: { fontFamily: 'Inter, system-ui, sans-serif' },
  grid: { left: 8, right: 10, top: 18, bottom: 0, containLabel: true },
  tooltip: {
    backgroundColor: '<card-hover 底>', borderColor: '<border-strong>', borderWidth: 1,
    padding: [10, 12],
    textStyle: { color: '<text-1>', fontSize: 12 },
    extraCssText: 'border-radius:10px; box-shadow:<shadow-lg>;'
  },
  // 折线：面积渐变 = 主色 .16~.24 → 0；柱状：barMaxWidth 18-20, 顶部圆角 4
}
```
- 系列色板必须按各风格规定的顺序取色，不许随机。
- 数据标签字号 10px；暗色风格的数据标签用等宽字体。

## 8. 数据配色系统（Data-Color System）
适用于：任何多系列/多类别维度的数据可视化（能源监控、生产监控、运营看板）。本章由 RZNY「能源监控暗色主题」实践提炼，三种风格通用——Style 01/02 可将色值换成对应品牌色系，但规则不变。

### 8.1 核心规则
1. **同实体同色**：同一类别（车间/产线/厂区…）或同一属性（介质/物料/类型…）固定一个颜色；跨全部页面、图表、图例、表格保持一致。禁止按当前排序索引从系列色板随机取色。
2. **语义色 + 类别色**：有语义的属性用语义色（电=绿、水=蓝、热/气=暖色）；无语义的实体用类别色板。两套色板独立，不可混用。
3. **颜色只用于识别**：数据强弱用透明度/亮度表达（见 8.4 矩阵色阶），不靠堆色相表达大小。
4. **0/负值/缺失不属于色板**：0 与负值→最低色阶 + 红字（#F87171）；缺失/未接入→灰。不用颜色美化坏数据。
5. **集中定义**：色板只在一处定义（JS palette 模块供 ECharts + CSS token 供 DOM 条/图例色块），页面一律 import，不散落 hex。

### 8.2 属性语义色（示例：能源 9 介质）
| kind | 属性 | 色值 | 色相语义 |
| --- | --- | --- | --- |
| 1 | 耗电量 | `#00D97A` | 绿=电 |
| 2 | 自来水 | `#3B82F6` | 蓝=水 |
| 3 | 压缩空气 | `#A78BFA` | 紫=气 |
| 4 | 制冷量 | `#22D3EE` | 青=冷 |
| 5 | 蒸汽 | `#EF4444` | 红=热 |
| 6 | 天然气 | `#F59E0B` | 琥珀=燃料 |
| 7 | 生活水 | `#60A5FA` | 浅蓝=水(生活) |
| 8 | 生产水 | `#14B8A6` | 青绿=水(工艺) |
| 9 | 纯水 | `#E879F9` | 品红=水(纯水) |

扩展到其他领域时：取对应语义的最近色相（水必蓝、热必暖、电必绿），相邻类别保持可区分。

### 8.3 实体类别色（示例：11 车间）
| # | 实体 | 色值 | # | 实体 | 色值 |
| --- | --- | --- | --- | --- | --- |
| 1 | 焊装车间 | `#00D97A` | 7 | 底盘车间 | `#14B8A6` |
| 2 | 总装车间 | `#22D3EE` | 8 | 座椅车间 | `#E879F9` |
| 3 | 整厂 | `#3B82F6` | 9 | 内饰车间 | `#84CC16` |
| 4 | 涂装车间 | `#A78BFA` | 10 | 外饰车间 | `#60A5FA` |
| 5 | 冲压车间 | `#F59E0B` | 11 | 食堂办公楼 | `#FB923C` |
| 6 | 联合站房 | `#EF4444` | | | |

- 按**实体名称**取色（palette 内 name→color 映射），不按当前排序：排名榜第 1 名不强制红色。
- 汇总行（整厂/合计）用不与任何个体冲突的颜色（示例用蓝 #3B82F6）。
- 前 6 个色必须在暗/浅背景下都可区分；超过 6 个靠色相族 + 明度区分。

### 8.4 图表应用规则
1. **多类别条形图**：每条 = 该实体/属性固定色 + 条尾数值标签；不用系列色板顺序取色。
2. **实体×属性矩阵（热力表）**：单元格底色=该属性色；强度在**同列（同属性）内**归一：`alpha = 0.07 + 0.34 × √(v / colMax)`，小值不被旁边大值压没；0/负值→最低色阶，负值红字；未接入→灰格 + 文字；列头放该属性色块图例。
3. **数量级差 ≥4**：条形图用 log10 轴（0/负值剔除并在脚注标注剔除数）；2~3 个数量级用线性轴即可。
4. **占比（饼/环）**：同属性各一张图保证可比；实体色取类别色板；负值不占角度（仅 tooltip）；合计 ≤0 显示空态而非空饼。
5. **趋势对比（今 vs 昨）**：语义双色——主线品牌色 + 面积渐变，对比线灰虚线；不用类别色。

### 8.5 参考实现
- RZNY 仓库：`apps/web/src/features/energy/palette.js` —— 单一模块导出 `KIND_COLORS` / `WORKSHOP_COLORS` / `workshopColor(name, fallbackIndex)`，总览排名、分布饼图、结构条形、矩阵、冲压/涂装车间页全部 import 同一份。
- CSS 侧：`design-tokens.css` 的 `--kind-*` / `--ws-*` / `--data-neg` 与 JS 色板一一对应（JS 供 ECharts，token 供 DOM 进度条/图例色块）。

## 9. 交付检查清单
- [ ] 所有颜色来自 CSS 变量，无写死色值
- [ ] 数字 tabular-nums（Style 03 用 JetBrains Mono）
- [ ] 无 emoji 图标、无毛玻璃、无发光边框、无彩虹色
- [ ] 卡片 12-16px 圆角，无卡片套卡片
- [ ] 过渡 0.2s ease
- [ ] 数据配色遵循第 8 章：色板集中定义、同实体同色、矩阵 √比例色阶/对数轴/负值红字等规则落地
- [ ] 1600 桌面 + 390 移动截图自检通过（无溢出/遮挡，图表非空白）

## 10. RZNY 2026-10-24 UI Baseline

RZNY 在 2026-10-24 确认新的全局 UI 基准，用于替代本项目旧的可读性规则。完整 token、组件、主题、迁移规则、兼容要求和验收清单见 `RZNY-2026-10-24-BASELINE.md`；该基准不设行数限制，以完整可执行为准。当前版/改善版预览见 `rzny-2026-10-24-current-vs-improved.html`。

**核心规则**
1. 正文 15px/500，表格正文 14px/500，meta 至少 12px/500；废弃 10px 业务文字。
2. 灰阶使用 `--ink / --body / --secondary / --tertiary / --disabled`，正文与表格达 AA；disabled 只用于禁用语义。
3. 数字一律 `--mono` + `tabular-nums`；KPI 主数字 34px/700，紧凑卡片不低于 28px。
4. 控件、表格、状态标签、图表文字按基准统一：控件目标 44px，表格行高 44px，轴字 12px，图例 13px，数据标签 11px/600。
5. 暗色和亮色都跟随 `data-theme`；soft 底暗色用语义色 8%-12% 透明，亮色用实色 pastel；保留旧 token 别名以兼容存量页面。

该基准不改变 RZNY 的后端、接口、数据库、业务逻辑和 8000 路由白名单；8000 仅同步基础样式提升，不新增设计系统入口。
