# 缺陷模式

记录已复现、可能再次出现的缺陷及触发条件。

预算：每条不超过 300 字；最多 40 条且不超过 8,000 字符。

- 2026-09-20 Android 代码 UI 易踩点：布局参数必须 `new LinearLayout.LayoutParams(w,h)` 不能直接 new LinearLayout；lambda 引用局部按钮须 effectively final；Spinner 首次布局必触发 onItemSelected，用 skipFirstCallback 跳过；搜索框等控件若嵌入卡片，不能再靠遍历根视图查找，须持有字段引用；白色矢量图标放进浅色按钮要用 tint 着色，否则不可见；手录 vector pathData 易损坏，复杂图标改描边弧线画法。
- 2026-09-28 事件式报警 + 窗口评分的"满分假象"：health_score 只对分析时刻状态扣分（活跃越限 -18、反复越限≥3 次 -7），报警刚恢复即回到接近满分，巡检误导。教训：设计"当前健康分"时必须同时考虑窗口内刚恢复的越限（1h 内有过 High/Low 的参数应保留 warning），否则"刚出完事"和"一直没事"在分数上无法区分。
- 2026-09-28 远程接口 404 误判：用不存在 ID（99999）探测"单条删除接口"时把业务 404（记录不存在）误当路由 404。正确判别：先用 OPTIONS 探测同一 URL，看 Allow 头是否含目标方法（如 `Allow: DELETE, OPTIONS`）——Allow 含方法=路由在、进程已加载新代码；再配合真实 ID 复测。GET 存在 + DELETE 404 时优先怀疑探测数据而非部署。
- 2026-09-28 pip 升级 snap7 后新旧混装：旧版 1.x 留下 `client/__init__.py` 文件夹，新版覆盖了 `common.py`（`check_error` 挪进 error.py），旧 client import 新 common 即 ImportError。修复：`pip uninstall snap7 -y` 后必须确认 site-packages/snap7 文件夹已消失，残留手动删，再装固定版本 2.0.2；无外网机器可整文件夹拷贝（DLL 捆绑包内）。教训：pip 升级不保证清掉旧包文件夹，import 报"cannot import name"先查混合残留。
- 2026-09-28 Flask sqlite 连接 URI 只读参数：`connect_args` 里直接传 `{'mode': 'ro'}` 会 TypeError（不是 sqlite3.connect 的关键字），正确写法 `'uri': True` + URL 追加 `?mode=ro`。Flask-SQLAlchemy 相对路径 sqlite:/// 指向 instance/ 目录，跨入口文件共享同库时用绝对路径拼接最稳。
- 2026-09-28 需求确认缺失导致连环返工：用户说"再设计一个网页（浅色+手机版）"未追问形态，做了精简总览版被否（"功能和效果差很多"）；补齐功能后被否（"我要电脑版手机版两个都要"——实为响应式单页已满足，属沟通误解）。教训：页面类需求动手前用 AskUserQuestion 冻结「形态（独立/响应式）+ 功能范围（对齐/精简）」两个维度，一次做对。
- 2026-09-29 CSS 未闭合大括号导致整段规则失效：一处重复的 `.card {` 未闭合，会让后续 `metric-grid`、`robot-grid` 等规则不生效，表面症状变成"桌面/手机布局退化为单列"，容易被误判为响应式断点问题。修复 CSS 新增规则后，收工前务必用括号计数（`{` 数 == `}` 数）或格式化器复查；不能只看浏览器不报错。
- 2026-10-08 批量查最新状态的 SQL 陷阱：`WHERE VIN IN (...) AND Pass_Time IN (SELECT MAX(Pass_Time)...GROUP BY VIN)` 外层未按 VIN 分组，两辆车同秒过点或同车同秒多工位时返回多余行，Python dict 后写覆盖先写导致工位张冠李戴。正确写法：`ROW_NUMBER() OVER (PARTITION BY VIN ORDER BY Pass_Time DESC)` 取 rn=1。
- 2026-10-08 S7 String 解析不一致导致 VIN 带垃圾前缀：snap7 `db_read` 返回的 S7 String 前 2 字节是（最大长度+实际长度）头部，`decode('utf-8').strip('\x00')` 不处理头部；多个脚本读写同一 PLC 时必须统一用 `snap7.util.get_string`/`set_string`，否则中继脚本会写入含控制字符的错误 VIN。
- 2026-10-08 PLC 报警防抖断线不重置：连接断开时 `connected=False` 但 `last_alarm_state` 未清空，重连后状态未变则跳过写入，可能漏写报警位。正确做法：断线重连成功后强制重置防抖状态，至少写一次当前状态。
- 2026-10-08 Vue 嵌套功能页相对导入陷阱：`src/features/<domain>/*.vue` 引用 `src/api/*` 或 `src/components/*` 时，正确路径是 `../../api/*`、`../../components/*`，不是 `../api/*`。Vite 会直接报 `Failed to resolve import`，表面像页面坏了，其实只是相对层级算错。新增跨目录页面时先核对当前文件到 `src/` 的层级。
- 2026-09-20 KeyVault（纯框架 android.app，无 AndroidX）：① `android:style/TextAppearance.Material.Light.Body1/Headline/Title` 等非公开资源，aapt 链接报错；style 父级用 `@android:style/TextAppearance` 即可。② `Context.getDrawable(int)` 只接受单参，双参 `(int,Theme)` 在 `Resources` 上；代码中统一走自封装 `drw(res)`。③ 通用 `vertical()` 容器不要带背景色，否则嵌进白卡片会露灰块；灰底只在页面/弹窗根容器显式设置。
- 2026-10-10 启动链路配置漂移：Vite 硬编码 8002、脚本硬编码 8001 时，只改 JSON 配置不会生效，`-Status`/`-Stop` 还会看错端口。所有端口必须从同一配置源读取，启动/状态/停止共用；配置变更后重启并用真实 HTTP 探活确认。
