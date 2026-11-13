# 语义层

本目录是重建后的 `operater-cat 9.6.3` 源码树的可读语义层。

它回答原始模块树本身无法回答的三个问题：

1. 领域对象及其所有权/生命周期是什么？
2. 每条业务路径由哪些模块实现，证据等级是什么？
3. 哪些行为被有意保留为重建边界，或在宿主机上执行不安全？

本文档使用的证据等级：

- `exact`：名称、字段、常量和签名已由 Nuitka loader metadata、运行时字典
  或静态字符串确认。
- `high`：控制流或字段映射已由多项静态观察确认，包括 Hex-Rays 输出和
  序列化样本。
- `inferred`：基于名称、常量、varnames 和状态转换得到的可读行为重建；
  它不是逐字节一致的原始源码。

目标程序**不属于**验证循环的一部分。它包含反调试路径，会记录
`反调试: 禁止调试 X` 并调用 `shutdown.exe`。本树中的所有检查均为离线、
静态或纯 Python 检查。

## 文档

- [domain-model.md](domain-model.md)：账户、远端心跳、条目快照、flow、
  订单和解析实体。
- [license-flow.md](license-flow.md)：启动、机器码、授权报告、账户刷新
  和条目 bootstrap。
- [card-key-analysis.md](card-key-analysis.md)：已归档的卡密代码块、
  HMAC A/B/C 链、账户绑定和离线中和。
- [order-and-item-flow.md](order-and-item-flow.md)：订单创建/检查、迁移、
  激活和条目脏数据生成协议。
- [parse-pipeline.md](parse-pipeline.md)：Telegram 消息摘要组装、
  频道/评论解析请求和 `ParseBean` 输出。
- [proof-ledger.md](proof-ledger.md)：本地 SHA-256/HMAC 证明帧、
  `_Cap` 封装/解封、kid ring 以及 `fea._pl_wd_file` 中的状态映射。
- [risk-boundaries.md](risk-boundaries.md)：反调试/关停链、动态 `exec`、
  文件系统隐藏和静态分析安全规则。
- [malicious-logic-analysis.md](malicious-logic-analysis.md)：已归档的
  反调试、关停、隐藏命令和勒索代码块，以及离线中和映射。
- [anti-debug-catalogs.md](anti-debug-catalogs.md)：已解码的检测和消息
  catalog、探测节奏、响应包装器以及七条 `_fds_tan` 链。
- [auto-flow-and-workers.md](auto-flow-and-workers.md)：worker 结果契约、
  flow/ban-yun/yun/download 家族以及首帧封面解析。
- [monitor-and-telefast.md](monitor-and-telefast.md)：Telegram 监控跟进
  规则、watchdog 调度器、限速器和快速传输。
- [obfuscated-packages.md](obfuscated-packages.md)：`bz_uc`、`kv_nx`、
  `rm_qh` 和 `wp_jt` 的分派/辅助模式以及仅限静态的命令边界。
- [ui-resource-reconstruction.md](ui-resource-reconstruction.md)：生成的
  `Ui_Form`/`Ui_MainWindow` 模块及其推断边界。
- [engineering.md](engineering.md)：测试、依赖清单和重建检查表。
- [ui-controllers-and-tabs.md](ui-controllers-and-tabs.md)：标签页控制器、
  业务对话框以及账户/代理/广告/水印/评论家族。
- [coverage-matrix.md](coverage-matrix.md)：模块家族到文档/测试/证据的
  映射，以及置信度边界。
- [runtime-services.md](runtime-services.md)：mthread/login/proxy/record/
  remember/config/log 服务契约。
- [ui-text-inventory.md](ui-text-inventory.md)：已恢复的 retranslate 文本池
  及其配对边界。
- [recovery-status.md](recovery-status.md)：精确与推断范围、已知缺口以及
  当前门禁状态。

源模块仍位于 `../src/py/com/yun/mao/` 下；本层不会替代它们。

## 当前恢复状态

- 368 个源文件，3,127 个函数，262 个类。
- Loader 覆盖率 `357/357`；精确函数名 `492/492`；类方法
  `1167/1167`。
- 混淆包：90/90 签名匹配，91/91 分派测试覆盖。
- 离线套件：455 个测试；`validate_all.py` 会运行编译、manifest、UI、
  导入、签名和分派审计。
- 仍处于推断范围的区域：非破坏性的 Telethon/UI 适配器；卡密与
  恶意路径已归档，并由 `sanitized/neutralize.py` 中和。
