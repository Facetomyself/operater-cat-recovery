# 源码恢复计划

## 当前状态

- 357/357 个加载表 app/resource 条目都有 Python 文件或包
  `__init__.py`。
- 368 个源文件通过 `compileall`；离线 pytest 套件有 102 个文件 /
  388 个测试函数（455 个用例）。
- 源码 AST：3,127 个函数、262 个类；323 个模块至少有一个真实
  函数体。
- `module_index.json`：357 个条目；315 个正文、31 个包、11 个常量、
  0 个空条目。
- 从 `.data` RVA `0x854E100` 解析出 2777 个 Nuitka 加载器条目。
- 提取出 2443 个 function-init 引用；286 个引用已有名称。
- `_sq_req` 不再使用 `_unsupported`；它已有可读的
  AES-CBC/RSA-PKCS1v15 请求信封和响应校验路径。
- 六个 `_fds_tan.wb_*` 包装器和三个 `_wb_jk_*` kernel32 探测已根据
  code-object 行号加常量索引重建；七条探测链现在在
  `try_begin_abort()`/`seal_abort()` 门禁后使用显式的 `importlib`
  模块/方法分发（`try_begin_abort()` 返回 false 时立即返回，finally 中执行
  `seal_abort()`）。
- 九个 `src.resource.ui.dyna.*` 模块已根据解码后的常量块和对话框控件映射
  重建。
- 静态门禁现在包括构造器调用、tab/page UI 引用、静态 `.ui` 引用和同类方法
  调用审计；四项均为零发现。
- 构造器调用门禁现在会解析 dataclass 继承并校验关键字名称；`DTopClass`
  字段集合已与编译后的 `__init__` varnames（`CommentRuleBean`、
  `SuperFlowBean`、`AutoBean`）重新对齐，并由
  `tests/test_dclass_field_signatures.py` 固定。
- `DTopClassHelper.dic_to_Auto_obj` 现在分发到已恢复的 `parse_*`
  工厂链并解包 `beanLike`；这消除了持久化/传输字典与具体 `AutoBean`
  子类之间的缺口。
- `MainWindow` 接入了四个核心 tab，并将动态 AI/premium tab 加载到
  专用 `QWidget` 页面；`SuspendFrozenTag` 恢复流程和
  `SessionLoader` 隐私去重已恢复并通过回归测试。
- `MainWindow` 现在将四个核心 tab 控制器接入已恢复的
  `gen_session`/`tab`/`tools`/`api_fun` 页面，并将动态 AI/premium
  控制器加载到专用 `QWidget` 页面。
- `bring_window_to_front` 已从运行时全局清单恢复；
  `CommonCode.process_text_to_obj` 已存在并由分支测试覆盖。
- 语义文档位于 `semantic/`（18 份文档）。
- init-slot 映射现在属于方法的一部分：以
  `sub_1480F7CC0(..., a2: &unk_...)` 为基址，然后使用
  `constants[(qword_addr - base) // 8]`。
- 机器可读证据：`agent-notes/source_stats.json` 和
  `agent-notes/source_recovery_audit.json`。
- 精确函数名映射：`agent-notes/function_name_map_exact.json`
  （来自 57 个 module-init 文件的 492 个名称）；当前源码覆盖率见
  `agent-notes/exact_function_coverage.json`。
- `AutoBeanXXX` 现在包含已恢复的 `_build_item_sign_payload`、
  `_verify_sign_item`、`_verify_sign_batch`、`_ticket_from_wire` 和
  `_exec_from_wire` 函数体；`_lk_gy_w._gy_rs` 使用已恢复的
  `(kid, auto_type, ticket)` 调用顺序。
- 依赖清单：`agent-notes/dependency_inventory.json` 和
  `requirements-recovered.txt`。
- 源码哈希清单：`recovered_src/MANIFEST.json`。
- UI 文本清单：`agent-notes/dyna_ui_text_inventory.json`。
- UI setup 树证据：`agent-notes/dyna_setupui_trees.json`。
- `TaskHardStop` 现在包含静态观察到的 `_poster_lock`、
  `Qt.QueuedConnection`、`_ghost_snapshot` 和 `_teardown_worker_loop`
  结构。其更丰富的 ghost-worker 调度仍停留在行为级。
- `glog` 现在包含已恢复的构造器字段、待处理 UI 队列、
  感知重叠的尾部合并和清理边界。
- `InnerAppIdConfig` 和 `net_config` 现在使用已恢复的可调用
  `tabl_cache.INSTANCE().read_cache` 路径；代理配置是三元
  SOCKS5 元组。
- `NetTest` 现在遵循已恢复的协程函数体：随机网络测试会话
  路径、精确的成功/失败提示、安全断开/删除清理以及
  `FastNetTest(finish_call)` 调用。
- `SessionLoader` 现在遵循已恢复的会话扫描、随机问候、
  FloodGuard 隐私请求和自动登录参数默认值；大型
  自动登录状态机现在覆盖连接/网络/认证/GetState 以及
  已停用/被封禁/登录失败列表。静态 `sendAtName` 问候分支已
  接入为非致命的登录后动作。
- `PublishIdRecord` 现在使用已恢复的 NewConfig/DTopClass 常量，并
  提供卷命名、消息链接构造和成功日志；高层
  `append_if_complete`/`_append_if_complete_inner` 映射链、
  写入队列、包装后的 JSONL 记录、原子 meta 文件、保留策略和卷
  轮换均已重建。渠道键、ID 列表、类型映射、磁盘+内存
  查询和对齐 cfg 的辅助函数也已具备。
- `CommentCopyLedger` 现在重建了惰性卷索引、队列写入器、
  原子 meta 文件和 id-key 辅助函数。
- `AutoWorker` 现在具备已恢复的停止前置检查、执行日志和固定
  结果契约，以及速率初始化。`inner_working` 现在将
  `obtainMessageAndParse` 接入 `foreachToSend`，传递解析/共享结果，
  直接调用私域/全局广告发布并完成汇总。
  包装器在进入 worker 前执行已恢复的本地账号检查，并接入了
  按 bean 执行的 `biz_sleep(2, 5)`。`convert_mode` 驱动已恢复的
  `_sq_r_ca.convert_batch_with_retry` bean 转换。
  `obtainMessageAndParse` 覆盖动态获取/解析、停止/None/终端
  处理、增量回写和随机桶重试上报。
- `GenSegmentVideoOnePass` 现在同时接受字符串和可调用
  `abs_cache_only_multi_dir` 值，用于 filter_complex 脚本放置。
- `BanYunUnProtect` 现在通过已恢复的 `log_publish_success` 钩子记录
  成功发送的频道消息，并通过
  `CommentCopyLedger.mark_after_send` 记录已复制的评论。
- `BanYunProtect` 现在通过同一发布成功钩子记录成功发送的
  文本/文件。
- `FlowProcess` 和 `YunProcess` 现在通过同一发布成功钩子记录
  成功发送的文本。
- `CMCode._send_to_dest_with_retry` 不再调用无关的相册账本
  路径；真实函数体只包含发布成功日志。
- `AutoWorkerWrapper` 现在从 `PublishIdRecord` 解析私域广告发布成功
  记录器，与已恢复的模块常量一致；全局广告
  成功现在使用同一记录器，`foreachToSend` 在应用分组结果后记录每个
  分组的发布映射。
- `CommonCode.MessageMyObj` 现在包含已恢复的三字段
  `for_mat/text/ai_refused` 结构；拒绝记录使用该对象，失败
  记录保留源 bean。参见
  `agent-notes/message_my_obj_evidence.md`。
- `TextProcessLogic` 现在具有静态函数边界：
  `process_text_by_ai_if_need(text, auto, bean)` 执行前置检查并
  转发到 `process_text_inner(obj, aiBean, api_key)`，后者负责
  重试循环和拒绝/失败上报。
- `TaskHardStop` 现在排除当前 teardown 任务，恢复
  `_teardown`/`_done` 失效保护结构并关闭回退事件循环。
- `RandomBucketManager` 现在提供已恢复的桶布局、会话
  tried-range、持久化耗尽和重启加载 API；推断出的边界
  记录在源码头部和证据笔记中。
- `PublishIdRecord.log_publish_success` 现在同时接受旧式
  `(channel, msg_id)` 结构和 `CMCode` 的 `(target, comment_to_id, sent,
  album_size)` 结构。
- 剩余七个大型 `setupUi` 函数体会让 Hex-Rays 报
  `MERR_FUNCSIZE`；这是反编译器容量限制，不是缺失
  函数指针。2026-11-11 使用 `MAX_FUNCSIZE=1024` 重试时，
  `auto_flow_item`（542.8 KiB）和 `down_load_flow_item`
  （180.5 KiB）在 12/6 分钟内仍未完成；`ai_employee_item`（55.4 KiB）
  可以正常反编译。Ghidra 12 headless 对 180.5 KiB 的
  `down_load_flow_item` 函数体也在 900 秒后超时。应使用函数拆分或手工
  块级分析，不要重复整函数反编译。生成的表单仍保持字段正确，并采用
  推断的扁平布局。

## 事实依据

- `agent-notes/nuitka_module_table.json`：模块名、init RVA、flags。
- `agent-notes/function_map_full.json`：全部引用及已命名/候选状态。
- `agent-notes/anti_debug_function_map.json`：已验证的反调试引用。
- `agent-notes/pdata_functions_full.json`：精确函数边界。
- `agent-notes/enc_blocks_decoded.txt`：解码后的反调试目录。
- `recovered_src/decompiled/`：可读的行为重建。

## 下一优先级

1. 对已存在的 UI/业务函数体做语义细化：
   `MainWindow`、`tab.*`、`dialog.*`、`tgaccount.*`、`comment.*`、`water.*`、
   `ad.*`、`monitor.*` 和 `util.need` 控件。
2. ~~恢复 `CommonCode.process_text_to_obj`~~ —— 已完成；该函数和
   `safe_with_append_tail` 已存在并通过回归测试。
3. 混淆包：`bz_uc`、`kv_nx`、`rm_qh`、`wp_jt`；入口点已
   存在，但命令/导入分发语义仍需复核。
4. 隐藏 Windows 命令链：`_dr_vx_file`、`_qf_rn_file`、`_hb_yt_file`、
   `_cw_jm_file`、`_lk_ps_file`、`_yg_bn_file`；仅做静态语义。
5. 将 `ui/static/*.ui` 列表项控件与其 Q* Python 类对齐；
   `_re/audit_item_widget_refs.py` 现在强制执行此检查，并记录
   `label_*`/`dl_label_*` 双布局兼容边界。
6. 在可用时用静态字符串和运行时字典校验重建的协议字段；保留
   推断行为的标记。
7. 只有在源码恢复通过验收后，才进入恶意程序和
   授权密钥分析。

## 方法

- 只使用 `static_hybrid.exe`；绝不执行它。
- 对新伪代码，在干净的 `temp/ida_work` 工作目录中运行
  `_re/ida_decompile_idat.py RVA[:LABEL]`；`IDA_TARGET` 可以指向
  分析副本。
- 先读取 `pdata_functions_full.json` 边界，再用
  `_re/ida_decompile_targets.py` 强制函数识别。
- 将已验证映射与顺序推断候选分开保存。
- 源码修改后重新运行 `python -m compileall -q recovered_src`。
- 在 `recovered_src` 中重新运行 `python -m pytest -q`。

## 安全

目标程序会记录反调试检测，并具有 `shutdown.exe` 响应路径。
本轮恢复不包含目标执行、Frida attach 或动态插桩。
