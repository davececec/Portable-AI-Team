# 技术决策

记录仍然有效的架构、依赖和重要取舍。

预算：每条不超过 300 字；最多 40 条且不超过 8,000 字符。

- 2026-09-20 KeyVault：坚持零 AndroidX，Activity 继承 `android.app.Activity`，全部界面纯 Java 代码构建（无 XML 布局）。因此系统指纹只能用 FingerprintManager（BiometricPrompt 需 FragmentActivity 且新版 android.jar 无 PromptInfo）；波纹/圆角/阴影全部自绘 drawable。
- 2026-09-20 KeyVault 安全设计：主密码不存库，PBKDF2 120000 轮派生密钥 + AES-GCM；salt/iterations 随备份文件 .kvb 自带；SQLite 只存密文，v1→v2 迁移须在解锁后把 crypto 注入 DB 再开库；自动锁定时取消指纹信号并关闭所有登记弹窗。
- 2026-09-20 KeyVault UI：设计令牌集中在 res/values（颜色/间距/文字样式），组件一律 drawable 化（bg_*）、图标矢量化（ic_*），代码侧通过统一视图工厂装配；通用容器不带背景色，灰底只在页面根设置，保证白卡嵌套干净。
- 2026-09-22 TZ Enc 复刻：第一阶段优先沿用 SQL Server，以复用原有表结构、pyodbc、能源 SQL、AI 采集及报表逻辑；在新项目中新增 Service/Repository 边界，禁止页面或路由直接依赖数据库细节。核心接口稳定后再评估迁移 MySQL，避免同时重写数据库、业务口径和 UI。
- 2026-09-22 TZ Enc UI：新版采用 AgentC 的 `VECTOR GRID` 工业能源指挥舱方向：近黑石墨底、实体层板、精细分隔、电青主信号，状态色固定；圆角不超过 8px。顶栏承载环境/数据新鲜度/数据库状态，侧栏可折叠并按运营/设备/系统分组，AI 使用右侧可停靠洞察面板。
- 2026-09-22 TZ Enc 重建结构：不沿用旧项目混合目录作为新骨架。新项目先确定前端、后端、数据库迁移、测试、部署、文档的一级边界；源码、运行数据、临时文件、离线依赖、构建产物和部署包必须分离。旧项目仅作为功能和行为参考，按模块选择性重写，不做整目录复制。
- 2026-09-24 TZ Enc 双库：本地和远程 SQL Server 必须作为可同时存在的显式命名数据源，不能用单一 dev/prod 开关冒充双库。普通业务默认写一个主库；跨库同步走独立任务，并具备幂等键、状态、重试、补偿、冲突规则和审计。凭据只从环境变量或密钥管理器注入。
- 2026-09-24 TZ Enc 数据责任：生产事实表原则上由 EMS/MES/ANDON/PLC/OPC 上游写入，本仓库未包含完整现场采集驱动。新系统先建立数据契约、原始层、标准层和业务事实层，再实现页面；AI 采集副本不能替代生产源数据。
- 2026-09-27 RZNY 能源总览第一版直接从 EMS_DATEHOUR/MES_Pro_log/ENE_Difference/ENE_DAY_END 实时聚合，不预建汇总表；四接口共用 `_window()`（range→起止时间）和 `_ws_filter()`（车间过滤）两个辅助，SQL 全参数化。单位能耗的分母取 MES_Pro_log 计划产量合计，与实际产量口径待生产环境确认。
- 2026-09-29 Codex 桌面 app 与 Trae 的能力差异：Codex 不提供图形化"添加 Python 解释器/右键运行/断点调试"，工作方式是对话 + 终端 + 脚本。需要 IDE 体验时用 PyCharm 或 VS Code 打开项目；在 Codex 内直接用绝对路径解释器（如 `D:\00-python\python\python.exe app.py`）或生成一键 `run.cmd` 即可，不必强行模仿 Trae。
- 2026-10-08 RZNY 进度管理：把 `docs/RZNY_PROJECT_TIMELINE.md` 定为唯一进度总账，计划书只讲怎么排期，开发说明书讲怎么做，工单讲本次做了什么；完成、阻塞、风险必须回写到时间线。新功能想法先入 `docs/RZNY_FEATURE_IDEAS.md`，成熟后再进周计划，不直接开工。
- 2026-10-09 RZNY 时间口径：`EMS_DATA_METERREADACCU.type=2` 的 `time` 当前按“小时开始”执行，`state_time` 按“小时结束/同步时间”执行。依据是真实库中大量 `state_time - time = 3600`，但这仍是可回滚标记，不是最终现场确认。若反证出现，先改 `docs/EMS_DATA_METERREADACCU_DATA_SOURCE_AUDIT.md` 的 `4.1`、`docs/DATA_CONTRACT_V1_DRAFT.md` 的 `4.3.1`，再同步本条。
  关联提示：`docs/EMS_DATEHOUR_DATA_SOURCE_AUDIT.md` 的 `STIME` 口径也按此临时执行。
- 2026-10-09 RZNY 能源同步：上游 `INTERNAL-IP-REMOVED.10/xopenshdb.EMS_DATA_METERREADACCU` 只读；本地 RZNY 建同名镜像表。首同步按 120 天，后续默认 30 分钟、回看 72 小时，按 `id+type+kind+time` MERGE 幂等写入。源库查询按 11 个车间 x 4 个周期 x 9 种能源分组走主键 seek，避免按 time 全表扫描。凭据只在 .env/SYNC_CONFIG，不进文档和团队记忆。
- 2026-10-09 RZNY 同步补充：真实数据证明 `EMS_DATA_METERREADACCU.type=1` 不是单行总累计，而是高频累计/快照，时间间隔抽样可达 600 秒。因此首次全量、之后统一按 72 小时回看；`type=1` 本地保留 90 天，月数据永久。此结论可回滚，等现场确认后修订数据契约。
- 2026-10-09 RZNY 同步参数：开发阶段首次同步从 120 天改为 15 天，type=1 不再首次全量。pyodbc Decimal 转 float 在驱动层丢精度，修复为 value 转字符串传给 SQL Server。本地数据经 90 天保留期清理后从 354K 降至 130K 行。
- 2026-10-09 RZNY 能源总览真数据切换：新增 `MirrorEnergyRepository` 读本地镜像表 `EMS_DATA_METERREADACCU`，接口与旧 `EnergyRepository` 完全兼容。通过环境变量 `RZNY_ENERGY_DATA_SOURCE` 控制（mirror/legacy），测试环境设 legacy 保证 FakeRepository 生效。镜像表当前 129,991 行，KPI 返回真实 158,633.63 kWh。
- 2026-10-10 RZNY 配置边界：`config/rzny.config.json` 是 app/databases/sync/ai 的唯一配置源；启动、Vite、状态与停止都读同一端口配置。开发期用户要求同步页账号密码明文显示，属临时决策；后续 W3 必须做页面权限，不能把密钥写进团队记忆或文档。
