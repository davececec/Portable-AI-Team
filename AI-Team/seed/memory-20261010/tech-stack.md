# 技术栈

记录已确认的语言、框架、运行环境和兼容要求。

预算：每条不超过 300 字；最多 40 条且不超过 8,000 字符。

- 2026-09-18：Windows 项目默认优先使用 `D:\00-python\python\python.exe` 运行、测试和启动；仅在该环境不可用或项目明确要求其他环境时调整。
- 2026-09-20 KeyVault UI 为纯 Java 代码构建（无 XML 布局、零 AndroidX、android.app.Activity）。设计系统：teal 品牌色（brand_50/100/500/600/700，主色 #14B8A6/#0F766E）、ink_900→300 文字灰阶、bg_app #F4F6F8、白卡片 12dp 圆角 + 2dp 阴影；令牌在 res/values 的 colors/dimens/styles，组件 drawable 前缀 bg_、图标前缀 ic_；改 UI 时优先复用这些令牌和 MainActivity 的视图工厂（input/primaryButton/outlineButton/iconButton/drw/color）。
- 2026-09-20 本机 Android 工具链：SDK 在 `D:\Android\sdk`（platform android-35、build-tools 34.0.0/35.0.0、platform-tools），JDK 用 PyCharm JBR17（`D:\00-python\PyCharm Community Edition 2023.2.1\jbr`），Gradle 9.2.0 + AGP 8.5.2（默认要求 build-tools 34.0.0），minSdk 26；local.properties 已配 sdk.dir。
