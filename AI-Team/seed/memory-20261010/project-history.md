# 项目历史

记录关键版本、里程碑和影响后续任务的变更。

预算：每条不超过 300 字；最多 40 条且不超过 8,000 字符。

- 2026-09-18：完成 `rizhao-weather-forecast`，Python 标准库本地服务 + Open-Meteo，指定 `D:\00-python\python\python.exe`；11 项测试及真实浏览器天气加载通过。
- 2026-09-20：完成 Android 密码管理器 KeyVault（纯 Java、零 AndroidX、纯代码 UI）。能力：PBKDF2+AES-GCM 加密库、Room 式 SQLite（v2 含历史密码与迁移）、指纹解锁、30 秒自动锁定、.kvb 备份合并/替换导入、七种记录模板与自定义字段。当日完成全站 UI 美化（白卡片设计系统），assembleDebug 通过；视觉效果未上机验证（无设备），等用户装机反馈，返工额度 2 轮。
- 2026-09-22：完成 TZ Enc 源码审计并建立未来复刻计划。原系统为 Vue 3 + Flask + SQL Server 的整车厂能源驾驶舱，含能源监控、报表模板、AI 分析、设备/防错、日志运维。当前项目保留两份依据：`doc/TZ_Enc_复制级功能与开发说明书.md`、`doc/改造观察与需求记录.md`。未来在新项目文件夹内按模块重新实现，不直接整体复制旧工程。
- 2026-09-24：完成 TZ Enc 数据来源、数据库需求和模块化重建资料体系，并生成面向 Trae 的根 `AGENTS.md`。交接明确区分 2026-08-06 Git 基线与大量未提交在途改动，旧仓库继续用于行为、数据口径和模板验证；正式新系统在新目录按数据层、API、前端和部署逐模块重建，要求桌面、平板、手机响应式验收。
- 2026-09-27：新项目 RZNY（`D:\00-python\Project\RZNY`）能源总览链路打通：本地 SQL Server `localhost\SQL_2019` 的 RZNY 库建好 10 张能源表（DDL 在 `database/sqlserver/001_create_energy_tables.sql`），`.env` 配置 Windows 认证，健康检查 db_ok=true。新增幂等灌数脚本 `scripts/seed_demo_data.py`（近 31 天演示数据，今明强制工作日，含异常尖峰）和能源总览蓝图 `apps/api/energy.py`（kpi/trend/anomalies/ranking 四接口从库实时聚合，无数据返回空结构）。前后端 8001/8002 经 `scripts/dev.ps1` 管理，浏览器已可见真实 KPI、趋势、异常和排名。
- 2026-09-27：新项目「机器人工艺参数」（`D:\00-python\01-py\INTERNAL-IP-REMOVED.66\机器人工艺参数`），ABB 涂装参数采集与报警监控（Flask + SQLite/WAL + snap7，端口 5058，2 工位 × 4 机器人）。完成：PLC 超时保护（读写 2s、TCP 预检 2s、失败退避 30s）、报警中心事件式去重、全工位顶部横幅 + 红色闪烁 + Web Audio 蜂鸣、参数中文名与单位、AI 分析接口（provider 抽象，规则引擎离线兜底）。遗留：40 条报警阈值全为 NULL 需现场标定；参数单位与部分工位全零数据待确认。
- 2026-09-28：机器人项目部署至车间服务器 INTERNAL-IP-REMOVED.61（`D:\progect\机器人工艺参数`，UNC 直拷 + MD5 校验），历史报警删除（单条/按工位清空）上线；服务器端修复 snap7 新旧混装（卸载清残留装 2.0.2）。实测真实报警出现：R12/R21 电流越上限、R12 流量越上限，事件式去重与恢复链路正确。用户决定 AI 评分机制暂不改（等报警量积累自然变真实）。移动浅色页面尝试两轮后用户放弃，已完整回退（文件零残留），教训入库。
- 2026-09-29：机器人项目交付浅色独立页面 `/light` 与 `/light/alarms`（Flask 只新增两条只读路由 + `templates/light/`、`static/css/light.css`、`static/js/light-*.js`），保留原深色 `/` 与 `/alarms` 不动；`/api/alarm_history?limit=100` 返回 200，桌面 1600px 与手机 390px 审计无横向溢出。同日修复 `instance/robot_data.db` 报警日志表索引损坏（重建后 `PRAGMA integrity_check=ok`，修复前备份）。
- 2026-10-08：完成「小修跳号车检测」项目审计（改进方向明确但未实施）。汽车总装 PBS/小修/TR03 车辆跟踪报警系统，Flask + MySQL + SQL Server + snap7，5 个独立进程（Web :5055、AVI 同步 2min、PBS 同步 10h⚠、VIN 中继 5s、TR03 监控 3s）。关键发现：PBS 同步 sleep(36000) 与注释 300s 不符致新车 10 小时不可见；批量状态查询 `Pass_Time IN (MAX)` 跨 VIN 误匹配致工位张冠李戴；参考车匹配失败退化返回前 50 条给错数据；凭据明文硬编码 + debug=True 上生产。现场反馈"数据不准"根因主要是同步间隔而非计算逻辑。
- 2026-10-08 RZNY W1 完成：能源模块拆成 `backend/modules/energy` 三层；新增 `/api/energy/detail/hourly` 与 `/api/energy/detail/summary`；pytest 10 passed，本地 SQL Server 真库验证通过。新增工程进度页 `/system/progress` 和 `/api/system/progress`。当前唯一进度总账为 `docs/RZNY_PROJECT_TIMELINE.md`；新功能想法先入 `docs/RZNY_FEATURE_IDEAS.md`。
- 2026-10-10 RZNY W2 暂停：真实数据同步、集中 JSON 配置、启动链路修复已验收；pytest 20 passed、build 通过，后端 8001/前端 8002 healthy。恢复入口：`docs/RZNY_PROJECT_TIMELINE.md` + `Portable-AI-Team/AI-Team/tasks/`；下一步是阶段能耗 API、`/analysis`、其余表审计和 W3 权限。
