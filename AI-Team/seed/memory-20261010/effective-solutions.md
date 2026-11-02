# 有效方案

记录经验证可复用的实现或排障方案。

预算：每条不超过 300 字；最多 40 条且不超过 8,000 字符。

- 2026-09-20 本机 Android 命令行构建：JAVA_HOME 指 PyCharm 自带 JBR17，JAVA_TOOL_OPTIONS 设 `-Duser.language=en -Duser.country=US` 消除 javac 中文乱码，用缓存的 gradle.bat 跑 `:app:assembleDebug --offline`（aapt2 首次在线拉取后即可离线）。PowerShell 执行策略红字是噪音，不影响构建。
- 2026-09-20 框架 Activity 指纹解锁：`FingerprintManager.authenticate(null, CancellationSignal, 0, callback, null)` + 自绘 AlertDialog；弹窗入 openDialogs 登记表，锁定时遍历 dismiss 并 cancel 信号；回调在主线程直接切 UI。
- 2026-09-20 纯代码 UI 复用模式：设计令牌（colors/dimens/styles）+ drawable 组件库 + Activity 内视图工厂（input/primaryButton/iconButton/drw/color）三件套；图标着色用 setColorFilter，按钮内图标用 setCompoundDrawableTintList，无边框图标按钮用 obtainStyledAttributes 取 selectableItemBackgroundBorderless 后 recycle。
- 2026-09-22 旧系统复刻法：先做源码地图与运行观察，分别记录功能/API/数据表/页面/部署及代码位置；再新建干净项目，按“基础设施→能源主链路→报表模板→AI→设备防错→运维生产化”逐模块实现。每阶段保持接口契约、字段映射、演示数据和验收用例，旧工程只作为行为参照，不直接携带密钥、日志、构建产物或历史耦合。
- 2026-09-22 Vue 理解与改造：`.vue` 单文件组件由 `<template>` HTML、`<script setup>` 逻辑、`<style scoped>` CSS 组成。全局令牌放统一样式文件，布局拆 Navbar/Sidebar/Main，业务按 feature/views/api/components 分层；新增功能依次补页面、路由、菜单、前端 API、后端路由/服务/Repository 和测试。
- 2026-09-27 演示数据灌库模式：脚本幂等（先 DELETE 演示窗口再 INSERT），随机种子固定保证可重复；主表曲线按"车间基线+小时系数+噪声"生成，另算均值回写 ENE_AVE/ENE_DIFF；今明两天强制工作日，否则默认"今日"视图无生产数据；异常演示靠注入尖峰（ENE×1.6~2.2）触发派生规则。pyodbc 灌数用 `fast_executemany=True` + `executemany`。
- 2026-09-27 Flask 能源接口契约要点：响应统一 `success(data)` 包成 `{code,msg,data,requestId}`；趋势接口必须返回 `series` 或 `points` 字段，否则前端 store 判为 empty；KPI 无数据返回 `{}` 让前端显示空态，绝不造 0；趋势当日序列去掉尾部无数据小时，未来时段不画 0；异常由数据派生（超均值 1.5 倍预警/2 倍严重 + 空耗/延时 TopN），不依赖单独告警表。
- 2026-09-27 事件式报警去重实现：内存活跃表以 (工位, 机器人, 参数) 为键；开报警时 `db.session.flush()` 取自增 id 存入表；恢复时回填原记录 `duration_seconds` 并另写一条 `Recover` 记录；配置被停用/删除时关闭其遗留活跃报警；进程启动时把遗留 `is_active` 且超时的记录直接关闭，避免重启后报警卡死。
- 2026-09-27 可切换 AI 分析接口模式：定义 `AnalysisProvider` 抽象，`RuleBasedProvider` 用本地规则 + 工艺经验库离线兜底，`LLMProvider` 走 OpenAI Chat Completions 协议（stdlib urllib，无新增依赖）；按环境变量选择，大模型异常自动降级并回写 `fallback_reason`。返回固定 schema（health_score / findings / severity / suggestions），将来换模型只改一处，前端零改动。
- 2026-09-27 历史趋势图性能方案：默认时间跨度 8 小时，前端按「工作站 + 机器人 + 时间段」做浏览器内存缓存，先渲染缓存旧数据再后台静默刷新；参数切换时瞬时重绘，避免每次重新拉取大数据导致卡顿。历史查询配组合索引 (station_name, robot_id, timestamp)。
- 2026-09-28 远程服务器部署与验证流程：本地开发 → UNC 共享直拷（`\\服务器\d$\progect\...`，445 通即可）→ MD5 逐文件比对确认一致 → 模板改动 Flask 热载立即生效，.py 改动必须重启进程 → OPTIONS 探 Allow 头验证路由加载。Windows 服务器侧 Flask 必须 `python app.py` 直跑（`app.run(host='0.0.0.0')`），用 `flask run` 会只绑 127.0.0.1 导致局域网访问不到。
- 2026-09-28 DELETE 接口设计约定：集合资源 `DELETE /api/xxx?station=` 按工位清空（无参=全部），单条 `DELETE /api/xxx/<id>`；状态机数据（如活跃报警 is_active=1）禁止物理删除，清空只删已结束记录，避免状态机对不上账；前端所有删除操作必须 confirm 且明示"不可恢复"与保护范围。
- 2026-09-29 SQLite `database disk image is malformed` 修复路径：先 `PRAGMA integrity_check` 定位错误页/索引；若报 `Rowid out of order` 且 `REINDEX` / 重建索引后仍在，说明页级损坏超出索引范围。安全做法：先备份原 DB（如 `instance/robot_data_pre_rebuild.db`），再单事务内 `CREATE TABLE xxx_new`、`INSERT ... SELECT` 复制数据、`DROP` 原表、`RENAME` 新表、重建索引，最后 `PRAGMA integrity_check` 确认为 `ok`。若原表有重复 id 导致唯一键冲突，改为不带原 id 复制让新表重新分配 rowid，旧记录仍可全部保留。
- 2026-09-29 Windows 下停 Flask 开发服务：`Ctrl+C` 在 Codex 会话里可能不生效，服务仍 5058 等 LISTENING。先用 `netstat -ano | Select-String ':<端口>'` 查 LISTENING 行拿到 PID，再用 `Stop-Process -Id <PID> -Force` 结束；`taskkill /PID ... /F` 在同机可能报 Access denied，而 `Stop-Process` 成功。最后用 `netstat` 复查端口释放，避免误判。
- 2026-10-08 RZNY 后端模块分层：业务域统一放 `backend/modules/<domain>/`，路由只做参数解析和响应；service 负责业务口径；repository 是唯一 SQL 层。列表/分析接口统一用 `workshop / type / range | start+end / page / page_size` 解析。生产事实表只读，空数据返回空结构，不用 0 冒充。
- 2026-10-10 Windows 开发启动器模式：Vite/后端从 JSON/环境变量读端口；后端和前端用 `.NET ProcessStartInfo` + `UseShellExecute=true` 启动，日志交给 cmd 重定向到文件，避免父进程句柄被子进程继承导致管道挂起；退出路径显式 exit，停止用带超时 taskkill 并按项目路径/命令行兜底复查。
