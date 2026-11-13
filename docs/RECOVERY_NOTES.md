# 恢复记录

## 方法

- 静态镜像：`_re/static_rebased.exe`，其中 `.text.PointerToRawData`
  改为 `0x5000400`，原始大小改为 `0x353d600`。这样真实的
  Nuitka 代码就能按其原始 RVA 映射。该镜像仅用于分析，从未
  执行。
- 模块/类/函数清单：关机前采集的运行时模块字典，加上静态
  `src.py.com.yun.mao.*` 符号。
- 函数体：通过 `ida-domain` / IDALib 使用 IDA 9.5 / Hex-Rays，
  设置 `auto_analysis=False`，并在已知入口处手工创建函数。
- 本轮恢复不包含目标执行、Frida attach 或动态插桩。

## 覆盖情况

- 357 个加载表 app/resource 条目都有源文件（`357/357`）。
- 368 个源 Python 文件通过 `compileall`。
- 源码 AST：3,127 个函数 / 262 个类；323 个模块至少包含一个
  真实函数或类体。
- `module_index.json`：357 个条目；315 个正文、31 个包、11 个常量、0 个空条目。
- 47 个模块具有详细的运行时元数据（常量/类/函数）。
- 解析出 2777 个 Nuitka 加载器条目；其中 346 个是 app 模块。
- 从 app 模块初始化函数中提取出 2443 个 function-init 引用。
- 286 个函数引用已有名称；10 个模块具有 verified-order 映射。
- 102 个 pytest 文件 / 388 个测试函数离线通过；pytest 报告 455 个用例。
- `MainWindow.init_view` 现在针对已恢复的 `gen_session`、`tab`、`tools`
  和 `api_fun` 页面实例化四个核心 tab 控制器
  （`SessionFunTab`、`AutoYunYinTab`、`ToolBoxTab`、`ApiConfigTab`）。
  AI employee、AI test 和 premium 控制器在 `addTab` 之前被加载到
  专用 `QWidget` 页面，而不是直接传给 `QTabWidget`。
- `MainWindow.bring_window_to_front` 已从运行时全局清单和模块常量
  恢复；`CommonCode.process_text_to_obj` 和
  `safe_with_append_tail` 现在有分支级离线测试。
- 仍有八个空函数体钩子；它们是回退/日志/信号/监控空操作，
  并不是缺失翻译。
- 钩子集合由 `tests/test_stub_allowlist.py` 固定。
- `MANIFEST.json` 固定每个源文件的 SHA-256 和行数。
- `agent-notes/dyna_ui_text_inventory.json` 保留已恢复的八个
  `retranslateUi` 文本池。
- `agent-notes/dyna_setupui_trees.json` 保留已恢复的
  `ai_employee_item` 布局树（511 个 qword 引用）。
- `ai_employee_item` 使用嵌套树；`label_em_*` 兼容名称
  仍作为隐藏控件保留。
- `src.py.com.yun.mao.cd.TaskHardStop` 已按静态函数清单
  对齐 `_poster_lock`、`Qt.QueuedConnection`、`_ghost_snapshot` 和
  `_teardown_worker_loop`；其余调度分支仍为推断。
- `_fds_rt` 现在遵循反编译得到的探测槽位：`fs_dt_mk` 是
  随机分支探测，不是模块解析器；其他包装器使用已恢复的
  方法/阈值映射。`_dtdm_gl.dt_hq_fn` 从 `DtdmJz.dt_hq_hc` 解析 worker
  函数；`AutoWorker.inner_working` 负责私域/全局广告发布，
  `foreachToSend` 不再重复该逻辑。
- `bz_uc` 入口校验现在固定五条已恢复的分发链：
  `aq_22_rt_78` 加密信号扇出、`ya_p1_xz_o4` 封口/中止路径、
  `bd_s8_mo_d9` 提权加隐藏命令，以及延迟执行的
  `km_74_qs_60`/`pr_43_qs_39` 两步分发。
  `rm_qh.zc_q8_wy_n9.rt_i8_rx` 入口已修正为零参数函数；
  `_g/_o/_fn/_p` 是局部别名，不是参数。
- `bz_uc` 校验集现在还覆盖 `fi_49_qs_87`、
  `nq_23_vy_24`、`gi_x9_hk_y8` 和 `ya_p1_fh_w2`。
  `fi_49_qs_87` 的导入路径已从重复的
  `kv_nx.kv_nx` 包修正为 `kv_nx.fh_w2_il_z7`；内部导入
  契约现在以空 allowlist 运行。
- `uw_l7_ln_c2` 已固定为中止消息路径，两个五段式
  隐藏命令入口 `hk_y0_ce_t5` / `jm_a6_kn_b3` 由参数化
  分发测试固定。
- 纯字符串分发目标清单现在覆盖全部四个混淆包中的 16 个名称；
  `tests/test_obfuscated_dispatch_targets.py`
  断言它们不存在于加载表中且没有源文件。
- 全部 22 个 `bz_uc` 入口模块现在都在
  `tests/test_bz_uc_dispatch.py` 中有离线分发覆盖，包括五段式命令、
  动态行命令、中止消息、终端 `gc/_exit`、WinDLL 和
  `os.system` 回退路径。
- `kv_nx.be_s0_ij_z5` 已修正为仅在全局窗口可见时显示中止提示，
  用 `\n\n` 连接解码片段，并按关键字传递
  `error_msg=`。`kv_nx.cf_44_ps_55` 现在调用已恢复的
  `rm_qh.jm_a2_sv_j7` 目标名称，而不是扫描公开可调用对象。
- `dv_r4_uw_l7` 收到同样的中止提示修正。
  `aq_m7_ln_c2` 提权回退现在由 fake-WinDLL
  测试固定，该测试断言五段式 `Popen` 命令和 `CREATE_NO_WINDOW`。
- `hk_y8_gi_x9` 收到同样的中止提示修正，现在调用已恢复的
  `bz_uc.ya_p1_fh_w2.aq_m7_rx` 目标。延迟执行的 `pr_40_oq_84`
  分发器现在使用已恢复的 `rm_qh.bx_n2_yb_p7` 目标名称，
  而不是扫描公开可调用对象。
- `_re/audit_obfuscated_signatures.py` 现在对照 Hex-Rays 签名检查每个
  单入口混淆模块：90 个模块、0 个发现、
  0 个缺失证据。仅暴露 thread-state 参数的 C 函数体
  被视为零 Python 参数函数；这修正了
  `rm_qh` 终端/ctypes 入口和两个 `bz_uc` 定时器入口。
- `AutoBeanXXX.parse_wire` 现在遵循 `0x5478800` 常量顺序：
  批次签名、逐条 `_ticket_from_wire`/`_exec_from_wire`、
  `compute_af` 比较、条目签名、`ensure_valid` 和
  `gy_wc_hx`。`tests/test_autobeanxxx_wire.py` 固定成功、坏批次、
  af 不匹配和截断条目路径。
- Ruff `F401` 现在在整个恢复源码树中干净：diff 复核后
  移除了 92 个未使用导入，包括冗余的 `rm_qh._ops`
  包导入。第三方清单现在为 15 个包；`mautrix`
  仅被一个未使用的 `FastTelethon` 导入引用。
- `wp_jt` 中止模板现在由
  `tests/test_wp_jt_dispatch.py` 固定：`gj_x5_ft_v6`、`kn_b9_rt_i8` 和
  `or_f3_df_u0` 在不加载 Qt 或 ctypes 的情况下校验封口/显示/目标顺序。
- `wp_jt` 分发覆盖现在扩展到 11 个入口，包括五段式
  隐藏命令、提权加命令变体、动态行命令、
  `os.system` 回退和 CDLL/WinDLL 终端路径。
- `rm_qh` 分发覆盖现在扩展到 14 个入口：`os.system`/`Popen`、
  信号扇出、定时器分发、CDLL 终端路径和 `fi_w8_rx`。
- `kv_nx` 分发覆盖现在扩展到全部 23 个入口模块，包括
  终端、WinDLL、Popen、信号扇出和定时器组。
- `wp_jt` 分发覆盖现在扩展到全部 23 个入口模块。跨四个
  混淆包，全部 91 个入口模块都有离线分发测试。
- `_sq_jqm` 的公开 union-code 包装器（`zh_jz_xx`、`zh_sc_wj`、
  `zh_zw_uc`）现在在既有
  `_zh_rd_code`/`_zh_bc_uc`/legacy-migration 覆盖之上有往返测试。
- `_re/audit_dispatch_coverage.py` 现在强制执行 91/91 个混淆入口
  分发覆盖；任何包入口丢失测试引用时 `validate_all.py` 会失败。
- 隐藏命令链现在有静态 argv 形状测试，覆盖
  `_dr_vx_file`、`_qf_rn_file`、`_hb_yt_file`、`_cw_jm_file`、
  `_lk_ps_file` 和 `_yg_bn_file`；`Popen`/`os.system`/`WinDLL` 均已伪造，
  因此不会执行任何命令或 DLL 路径。
- `_cmd_ops`/`rm_qh._ops`/`wp_jt._ops` 不再从模块名中剥离 `src.py.` 前缀；
  `load_attr`/`call_entry` 现在解析恢复源码树的实际包路径。
  `tests/test_cmd_ops.py` 固定这些辅助函数和提权失败路径。
- `_dtdm_jz.dt_jz_xy` 现在在缓存/解码路径前运行
  `_fds_tan.wb_dt_zx` 探测，匹配 `co_names`/varnames 顺序。`bz_uc`
  加密/链接/中间探测信号入口现在扇出到各自的目录处理器，
  而不是只发出信号。
- `SchedulerThreadClass.my_job` 现在导入并调用 `_fds_rt.fs_by_pf`，
  而不是丢弃引用；已恢复的 varnames 为
  `fs_by_pf, h, e, error_msg, self`。
- `_dtdm_jz._decode_and_decompress` 现在在回退到原始 payload 前
  上报 `dt_jz_gz_fail_tpl_14` 消息。
- 大型 `setupUi` 恢复仍卡在 Hex-Rays：将
  `MAX_FUNCSIZE` 提高到 1024 后，542.8/180.5 KiB 的
  `auto_flow`/`down_load` 函数体在 12/6 分钟内仍未完成。IDA 配置已
  恢复。Ghidra 12 headless（JDK 21、`-noanalysis`、900 秒反编译器
  限制）对 180.5 KiB 的 `down_load` 函数体也超时；下一次尝试
  应使用函数拆分或手工块级分析。
- 一次 Capstone 常量池扫描重建出的 UI 树与已知
  `ai_employee_item` 树完全一致（30 个控件，无缺失/多余节点），但
  七个大型模块仅产出 17-31 个控件节点，而 `WIDGET_NAMES` 有 40-103
  个。部分树保存在
  `agent-notes/dyna_capstone_trees.json`；它们没有被注入到
  字段正确的生成表单中。
- UI 资源审计发现 27 个被引用的 `.ui` 文件和 5 个孤立文件。
  这 5 个孤立文件名不在 `static_hybrid.exe` 字符串表中，
  而所有被引用的 `.ui` 文件名都存在。它们属于遗留
  资源，不是缺失的加载器模块；不应凭空编造源码归属。
- `AiTextGenFlow` 现在暴露已恢复的 `check_sensitive`、
  `no_semantic` 和 `_detect_api_refusal` API，并使用编译后的
  敏感词模式。`TextProcessLogic` 现在导入该类（而不是
  同名模块），并遵循调用方的 `(text, auto, bean)`
  字符串返回契约。
- `TextProcessLogic.process_text_by_ai_if_need` 现在检查账号 AI
  能力、解析 AI employee/API key、校验 `xai-` 前缀，并在
  生成失败/被拒绝时重试，最多到 `AI_GEN_MAX_TRY_COUNT`。
- `CommonCode.MessageMyObj` 现在恢复为普通三字段对象：
  `for_mat: str`、`text: str`、`ai_refused: bool`，其 `__init__`
  按该顺序赋值。类字段来自
  `CommonCode` 注解字典，赋值顺序来自
  `sub_145D5A150`。拒绝路径记录
  `MessageMyObj(obj.for_mat, tart, ai_refused=True)`，而不是追加
  源 bean；生成失败仍追加源 bean。
  `process_text_by_ai_if_need` 现在执行前置检查并转发到
  `process_text_inner(obj, aiBean, api_key)`，后者负责生成循环。
  证据：`agent-notes/message_my_obj_evidence.md`。
- `CommonCode` 现在还有从精确 init 槽位恢复的小型工具函数体：
  `boolToStr`、`current_time`、`geneRamdomId`、
  `message_has_button`、`container_at_links`、`sleepTime`、
  `isProtectContent`、`is_broadcast_comment_channel` 和
  `is_key_word_in_text`，以及已恢复的 `parse_text` 和 `contain_word`
  辅助函数、`messages_has_button`、`messages_has_exclude_words` 和
  `messages_has_contain_words`，还有通过已恢复的
  `utils.is_video_message` 辅助函数实现的 `messages_has_video`；
  `is_super_group` 现在使用已恢复的异步 `(client, entity)` 结构。
  `auto_correct_step_length` 数值修正辅助函数已恢复，
  `YunYinMaoConfig.LOG_KEY_WORDS` 现在包含四个已恢复的日志关键词。
  媒体 `getVideoDuration`/`mediaSize` 辅助函数和两个最大选择函数
  现在都已存在。
- 精确名称映射现在从 57 个 module-init 常量槽位解析出 492 个函数名
  （`agent-notes/function_name_map_exact.json`）；覆盖率
  审计报告 492 个已存在、0 个缺失定义
  （`agent-notes/exact_function_coverage.json`）。新增名称包括
  `_build_item_sign_payload`、`_verify_sign_item`、`_verify_sign_batch`、
  `_ticket_from_wire` 和 `_exec_from_wire`。
- `AutoBeanXXX._build_item_sign_payload` 现在用 `|` 连接已恢复的
  十一字段 payload；`_verify_sign_item` 通过
  `jm_yq_qm(jm_jz_r_pk(), payload, signature)` 校验十六进制签名，
  `_verify_sign_batch` 校验
  `batch_id|exp|server_nonce|kid1,kid2,...`。`_lk_gy_w._gy_rs`
  现在按已恢复的 `(kid, auto_type, ticket)` 顺序调用校验器。
- 类方法 qualnames 现在通过跨模块继承解析出 1167 个 `Class.method`
  常量，包括 Qt mixin 和 item-widget 基类；覆盖率审计报告
  1167 个已存在、0 个缺失
  （`agent-notes/class_method_coverage.json`）。
- Ruff `F821/F811/F405` 现在是门禁；恢复源码树中没有未定义
  名称、星号导入绑定冲突或导入遮蔽发现。
- `SuperFlowBean.printFailedTips` 现在使用精确的 `NewConfig`
  重试上限，输出已恢复的随机/增量采集失败提示。
- 最后一组 `CommonCode` 缺口已关闭：时长/大小过滤器、water
  辅助函数、消息分组、任务分发包装器、权限检查、
  评论主题探测、文本转换和追加尾部处理现在都有
  已恢复的函数体。`BaseFilterBean` 和 `AdvancedFilterBean` 的归属
  已按反编译模型修正，包括嵌套的时长/大小过滤器和
  八个通用高级过滤字段。
- `src.py.com.yun.mao.monitor.MonitorSchedulerReport` 现在使用已恢复的
  `sync_start_report` 名称和 `asyncio.run(_sq_ks.start_report_inner())`
  契约；APScheduler 回退仍停留在行为级。
- `src.py.com.yun.mao.util.XAIKeyValidator.__init__` 现在遵循已恢复的
  `api_key.strip()` 契约，不再凭空创建 `self.parent` 属性。
- `src.py.com.yun.mao.log.glog` 现在遵循已恢复的构造器字段、
  待处理 UI 队列、感知重叠的尾部合并和清理边界。异步
  `LogWorker`/`QThread` 启动器在离线环境中仍有意保持不活动。
- `InnerAppIdConfig` 和 `net_config` 现在通过可调用的
  `tabl_cache.INSTANCE().read_cache` 读取；`get_proxy_config` 返回已恢复的
  `("socks5", ip, port)` 元组。
- `login.NetTest` 现在遵循已恢复的协程函数体，包括
  生成的网络测试会话路径、连接提示文本和
  `safe_disconnect`/`safe_del_file` 清理。
- `login.SessionLoader` 现在遵循已恢复的 `os.walk` 扫描、
  `generate_random_chinese(10)` 问候、FloodGuard 隐私请求和
  `(None, None, None, None, False)` 自动登录参数默认值。其
  网络/认证/GetState/已停用/被封禁状态机已重建，并使用
  fake-telethon 离线测试。已恢复的 `sendAtName` 启动问候
  分支现在仅在账号暴露目标时发送随机消息。
- `record.PublishIdRecord` 现在导入已恢复的 NewConfig/DTopClass
  常量，并提供卷命名、消息链接和发布成功
  日志。高层 `append_if_complete(auto, parse, group_result,
  convert_mode)` 委托给 `_append_if_complete_inner`，后者仅在配置的
  目标列表完整后才构建
  `time/mode/source/dest[/preview]` 映射器。其后台写入器存储包装后的 JSONL
  记录、轮换 `data-XXXX.jsonl`、原子更新 `meta.json` 并
  应用保留策略；查询同时读取内存和磁盘。
- `record.CommentCopyLedger` 现在重建了惰性卷索引、队列
  写入器、原子 meta 文件和 id-key 辅助函数，并有重载测试。
- `auto.AutoWorker` 现在具备已恢复的停止前置检查、执行日志和
  固定结果契约，以及速率初始化，并有离线契约
  测试。包装器现在在 worker 前运行 `_sq_ks.check_account_without_loop`，
  接入了按 bean 执行的 `BizSleeper.biz_sleep(2, 5)` 间隔，且
  `inner_working` 现在在 `foreachToSend` 前运行 `obtainMessageAndParse`，
  传递已恢复的解析列表和共享结果，直接调用私域/全局
  广告发布，并以 `completeItemSummery` /
  `print_summery` 收尾。非空 `convert_mode` 会调用已恢复的批量
  转换辅助函数；`obtainMessageAndParse` 覆盖动态获取/解析、
  停止/None/终端处理、增量 start-id 回写和随机桶
  重试上报。
- `GenSegmentVideoOnePass` 现在处理已恢复的字符串形式
  `abs_cache_only_multi_dir`，用于 filter_complex 脚本放置。
- `BanYunUnProtect` 现在在成功发送频道消息后调用已恢复的
  `log_publish_success` 记录器，并在成功发送评论后调用
  `CommentCopyLedger.mark_after_send`。
- `BanYunProtect` 现在通过同一发布成功钩子记录成功发送的
  文本/文件。
- `FlowProcess` 和 `YunProcess` 现在通过同一发布成功钩子记录
  成功发送的文本。
- 检查真实函数体常量后，`CMCode._send_to_dest_with_retry` 的相册账本块
  已被移除；`log_publish_success` 保留。
- `AutoWorkerWrapper` 现在从 `PublishIdRecord` 解析私域广告发布成功
  记录器，而不是无关的 `AdIdMapManager`；全局广告
  成功现在使用同一记录器。`foreachToSend` 还在
  `totals.apply_group_result` 后记录每个分组的发布映射，并在
  映射错误时继续，匹配已恢复的 `append_if_complete` 调用点。
- `cd.TaskHardStop` 现在从取消的待处理集合中排除当前 teardown 任务，
  使用带可取消循环失效保护的 `_teardown`/`_done`，并
  关闭显式回退事件循环。其余 ghost-worker
  调度分支仍为推断。
- `remember.RandomBucketManager` 现在提供已恢复的桶布局、
  会话 tried-range、持久化耗尽和重启加载 API。精确
  名称/注解来自模块常量；步进取整、
  边界和未加密持久化回退为推断。
- `ad.AdIdMapManager` 现在使用已恢复的 `ADMAP_INFO_KEY` 字节常量
  进行加密 ad-id 映射持久化；空键回退已移除，
  离线往返测试覆盖加载/更新/读取。
- `remember.RememberManager` 现在包含已恢复的 remember-map 密钥和
  加密/解密路径，并有源/目标密钥持久化的往返测试。
- `PublishIdRecord.log_publish_success` 现在同时接受旧式
  `(channel, msg_id)` 形式和 `CMCode` 的四参数/关键字形式。
- `recovered_src/semantic/` 下有 20 份语义文档。
- 当前机器可读计数：`agent-notes/source_stats.json`。
- 加载器/文件审计：`agent-notes/source_recovery_audit.json`。
- 依赖清单：`agent-notes/dependency_inventory.json` 和
  `requirements-recovered.txt`。

## 界面/资源恢复

- `_re/extract_dyna_layout.py` 现在从 `setupUi` 指令常量引用中重建真实的
  `addWidget` / `addLayout` 边。
  七个编辑表单根据该嵌套树重新生成，而不是沿用之前的
  扁平字段布局；`tests/test_dyna_layout_edges.py` 固定每条
  已恢复的边。主窗口保留其专用渲染器。
- `_re/decode_dyna_ui.py` 解码九个 `src.resource.ui.dyna.*` 块，
  这些块曾被早先的常量处理步骤过滤掉。
- `_re/generate_dyna_ui_modules.py` 生成包和八个表单模块。
- 控件名称和 `_TYPE_MAP` 键与七个编辑对话框的
  `WIDGET_NAMES` 元组完全匹配。
- `yun_yin_mao_main.Ui_MainWindow` 提供 `MainWindow` 使用的主窗口界面
  （`tabWidget_important`、`text_brow_log`、日志按钮、菜单
  动作）。
- 原始 Designer XML 缺失。几何、文本位置和 tab 顺序
  均为行为级重建；参见
  `semantic/ui-resource-reconstruction.md`。
- 四个 `wp_jt` 名称只存在于分发表字符串中（`fi_w8_wy_n9`、
  `lo_c8_qt_h9`、`ru_i0_gj_x5`、`xa_o0_ad_r5`），不是加载器条目。
- 已写回的核心模块体：
  - `_sq_chk.py`：`is_success`、`parse_report`、`hy_jx_bc`。
  - `_sq_jqm.py`：`SqJqm`、`SqJqmEnc`、账号辅助函数。
  - `_fds_sj.py`：解码后的反调试目录和密钥。
  - `_fds_jm.py`：XOR/base64 解码器和线程安全消息缓存。
  - `_fds_h_x.py`：行为级 `FdsHhx` 重建。
  - `_fdg_*`：隐藏进程、令牌、`os.system` 和命令包装器。
  - `_tw_ctx.py`、`_tw_ceng.py`、`_jmpz_cy.py`：Fernet/RSA 配置层。
  - `_sq_r_bao.py`：授权 payload JSON 构建器。
  - `ade/_ade_sing.py`、`ade/ad_t.py`：文件系统扫描/AES-GCM 链
    （默认 dry-run）。
  - `FakeUniqueMachineCode`、`ClientCacheHelper`、`InnerAppIdConfig`：
    机器码/配置辅助函数。
  - `fea/_pl_wd_file.py`：SHA-256/HMAC 证明帧、`_Cap` 封口/解封、
    kid 环、失败队列和状态映射。`_tg` 掩码顺序
    明确为推断。
  - `jm/_my_r_gk.py`、`link/_lk_gy_w.py`、`link/_lk_gy_r.py`、
    `link/_xb_ms.py`：RSA 公钥加载和 ticket 校验/重试
    链。
  - `auto/CMCode.py`、`TopicUtils.py`、`VideoProcessingIds.py`、
    `ProcessCache.py`、`GlobalWorkingLock.py`、`BizSleeper.py`、
    `down_load_config.py`。
  - 全部六个 `mthread` 模块：调度器/单任务/QThread 生命周期、
    接收代码、HTML 生成和广告发布。
  - `telefast/RateLimiterClass.py`、`RateTempClass.py`、
    `RateLimiterHelper.py`、`CallBack.py`。
  - `util/FloodGuard.py`、`util/ResourcePath.py`、`util/EnumClass.py`、
    `src/resource/__init__.py`。
- 已用 Hex-Rays 反编译 40 个函数：
  - `_sq_chk.parse_report`
  - `_sq_chk.hy_jx_bc`
  - `SqJqm.has_ai_ability`
  - `SqJqm.has_bot_ability`
  - `SqJqm.is_multi_permission`
  - `SqJqm.gen_grade_card_str`
  - `SqJqm.gen_ka_info`
  - 10 个 `SqJqm` range 候选和 15 个 `_sq_chk` range 候选，保存在
    `decompiled/c_pseudocode/sq_jqm_candidates/` 和
    `decompiled/c_pseudocode/sq_chk_candidates/` 下。

函数地址映射位于 `agent-notes/function_map_full.json`；
已验证的反调试映射位于 `agent-notes/anti_debug_function_map.json`。
已知名称在标记处为精确名称；`__candidate_0x...` 标签由
地址推导而来，仍需行为匹配。

## 运行时映射突破

- EXE 包含两个代码层。`_re/static_rebased.exe` 只映射
  内层 app 块。
- `_re/static_hybrid.exe` 将内层 app 块映射到 RVA `0x1000`，并让
  外层运行时尾部保留在原始 RVA。该镜像仅用于分析，
  绝不能执行。
- `compiled_function` 类型对象位于 RVA `0x8540080`。其对象大小为
  `0xE0`；`+0x18` 保存 code/state，`+0x78` 是 C 函数指针，
  `+0xB8` 是名称，`+0xC8` 是哈希，`+0xD0` 是闭包计数，
  `+0xD8` 是闭包 cell 数组。
- RVA `0x7F8F600` 处的 `tp_call` 调用 `(*(function_object + 0x78))(tstate,
  function_object, args)`。这确认了 C 函数指针偏移。
- RVA `0x7F4A350` 处的 `tp_repr` 使用 `+0xB8` 处的名称
  格式化 `<compiled_function %U at %p>`。
- RVA `0x7F51120` 处的 `tp_dealloc` 对 `+0x18`、`+0xB8`、`+0x88`、`+0x98`、
  `+0x28`、`+0xA8`、`+0xB0` 和 `+0xD8` 处的闭包 cell 执行 decref。

## 加载表突破

- 二进制在 `.data` 中包含 `Nuitka_MetaPathBasedLoaderEntry` 记录。
  表从 RVA `0x854E100` 开始；每条记录 32 字节：
  `name`、`python_init_func`、`bytecode_index`、`bytecode_size`、`flags`。
- 已解析 2777 个条目。编译模块的 `flags=0x10`；包使用
  `0x12`。app 有 346 个条目，包括未出现在运行时模块
  dump 中的混淆子模块 `bz_uc`、`kv_nx`、
  `rm_qh` 和 `wp_jt`。
- 模块初始化函数地址是精确的。init 函数使用
  `Nuitka_Function_New` 风格辅助函数
  `0x80EE3A0` 和 `0x80EE620` 创建
  `compiled_function` 对象；函数指针表现为 RIP 相对
  `lea rcx, [rip+...]` 目标。
- `_sq_chk` 按运行时顺序精确映射到七个函数；`_fds_rt`
  映射到十二个；`_fds_jm` 映射到五个；`_fdg_*` 各映射到一个。

## 置信度

- `exact`：在运行时字典、静态符号表中观察到，或从 init
  qword 槽位映射到模块常量表中的模块名、类名、函数名和常量。
- `high`：匹配多次观察的字段映射和简单方法，
  例如 `SqJqm.aiAbility == 1`、`mul` -> 多开权限、游客等级 -> `游客`。
- `inferred`：UI 事件顺序、CMC 媒体管线、ticket 重试细节，
  以及 `_pl_wd_file._tg` 内部的乘法/xor/and 操作数顺序。
- `unknown`：大多数 UI 函数体、四个混淆包，以及隐藏的
  `_dr_vx_file`/`_qf_rn_file` 命令链的完整语义。

## 优先级队列

1. 剩余 UI/业务外壳：`MainWindow`、`tab.*`、`dialog.*`、
   `tgaccount.*`、`comment.*`、`water.*`、`ad.*`、`monitor.*` 以及
   `util.need` 控件模块。
2. 混淆包：`bz_uc`、`kv_nx`、`rm_qh`、`wp_jt`（约 95 个文件）。
3. 隐藏命令链：`_dr_vx_file`、`_qf_rn_file`、`_hb_yt_file`、
   `_cw_jm_file`、`_lk_ps_file`、`_yg_bn_file` —— 仅做静态语义，
   绝不执行目标或重建的 `Popen` 路径。
4. 资源：将 `ui/static/*.ui` XML 映射到重建的控件中。

## 剩余缺口

- 内部模块对象导入已修正：`config.YunYinMaoConfig`、
  `dialog.ImageDialogHelper`、`remember.RememberManager`、
  `remember.RandomBucketManager`、`telefast.RateLimiterHelper`、
  `tgaccount.TGAuthAccountSetting`、`util.TracePrinterHelper` 和
  `dclass.DTopClassHelper`；源码现在导入模块而不是
  同名类。`tests/test_internal_import_contracts.py` 将
  其余未解决导入固定到已复核的 allowlist。
- `DTopClass.convertDest`、`DTopClass.convertDestTopic` 和
  `AutoBeanXXX.mem_auto_for_writeback` 现在有可读函数体。其
  参数/返回结构来自 Nuitka code-object 元数据；
  `convertDest`/`convertDestTopic` 的拆分遵循已恢复的
  `dest/channel_part/topic_part` varnames。
- `DTopClass` 字段集合已按编译后的 `__init__`
  varnames 修正：`CommentRuleBean` 是完整的评论流 payload
  （`copyComment`、`wantCount`、`dtype`、`forWardAction`、`baseFilter`、
  `advancedFilterBean`、`tail`、`replace`、`water`、`selfAdWrapper`、
  `yuLanResOp`、`aiEmployee`、`aiRefusedOpt`、`grid`、`randomCover`），而
  `SuperFlowBean` 增加了 `huiYuanLink`/`youKeLink`/`yuLanModeBean`/
  `durationInfo`，`AutoBean` 增加了 `completeVersionOp`/`botBean`。
  `ConfigCommentRuleDialog` 现在使用 `Tail(tail_text=...)`、
  `AdWrapper(adEnable=..., ades=...)`、`AiRefusedOption(action=...)`、
  `GridOpt(number=...)` 和真实的 `CommentRuleBean` 关键字集合。
- 构造器审计现在会解析继承的 dataclass 字段并校验
  关键字名称，而不只是位置参数数量；在 208 个直接实例化中
  报告零发现。
- `LoadDataClass` 现在将持久化的 `autoMap` 条目交给
  `DTopClassHelper.dic_to_Auto_obj`，因此嵌套的 `modelWrapper`、`tail`、
  `water`、`commentRule` 和其他 bean 字典会被重建为真实的
  dataclass，而不是保留为原始字典。
- `DTopClassHelper` 现在包含已恢复的 auto-bean 工厂链。
  `dic_to_Auto_obj` 根据 `auto_type` 分发到
  `parse_ban_yun_flow`/`parse_auto_flow_or_yulan_flow`/`parse_down_load`/
  `parse_yun_auto`/`parse_yun_preview`，并在应用嵌套转换器前解包
  传输层 `beanLike` payload。
- 常量池还固定了第一轮遗漏的五个较小 `DTopClassHelper` 辅助函数：
  `dic_to_Comment_obj`、`dic_to_modelWrapper`、
  `gen_default_base_filter_bean`、`gen_yulan_des` 和
  `ai_info`。
- `dic_to_modelWrapper` 将模式相关的 `startId`/`endId`/
  `wantCount`/`numberMode` 键保留为属性，因此 `AutoBean` 的随机/循环/
  增量访问器读取真实值，而不是回退为零。
- `AutoBeanXXX.ensure_valid` 已根据编译后的 varnames
  （`self, ucode, now, uc_hash, raw_kid`）和常量顺序
  （`time`、`hashlib`、`sha256`、`hexdigest`、`lower`、`exp`、`uc_hash`、
  `_verify_sign_item`）扩展；它现在检查过期、账号哈希绑定、
  execution-kid 一致性和条目签名。
- `_lk_gy_w` 的 HMAC 链现在有回归测试：`A|`/`B|`/`C|`
  payload 布局、`_g0`/`_g1` 切片赋值和
  `gy_jc_a1..a8` 接受/拒绝顺序。
- `_fds_sj` 消息目录已从常量块恢复并
  移入 `link/_fds_msgs.py`：308 个解码后的 `SEC_MSGS` 条目和
  六段式中止消息（`ABORT_PARTS_ENC`）。`sec()` 现在直接返回解码后的
  文本，包括 `md5` 等纯 ASCII 条目。
- 四个检测目录也已与常量块重新对齐：
  `link/_fds_catalogs.py` 现在包含 `STEMS`（71）、`PREFIXES`（9）、
  `MODULE_STEMS`（27）和 `WINDOW_KEYWORDS`（29）。之前的 9/21/29/29
  元组错位了一个槽位，漏掉了 62 个进程 stem 和若干
  模块名 stem。
- `FdsHhx` 时间常量已按类体常量修正：
  `DEEP_SCAN_MIN_INTERVAL_SEC=300.0`、`STARTUP_PROBE_WAIT_SEC=5.0`、
  `CONT_FAST_SCAN_MIN/MAX=10/12`、`CONT_FULL_SCAN_MIN/MAX=18/180`。
  `fh_ht_jk(interval=5.0, min_interval=None, max_interval=None)` 和
  `wait_startup_probe(timeout=0.5)` 现在匹配编译后的签名。
- `FdsHhx.fh_cj` 现在遵循已恢复的响应选择：记录
  `fd_log_CJ`，启动 UI/连续探测，然后根据
  `random() < 0.55`（`fh_qing`）、`< 0.92`（`fh_zhong`）或 `fh_quan` 分支。
- `tests/test_sec_key_coverage.py` 保持解码目录与所有
  字面量 `sec("...")` 调用点对齐；仅空键和
  `cloud item decode fail` 在 allowlist 中。
- `_fds_rt` 已对照真实 module-init RVA 检查：`fs_http` 分支为
  `<0.55 → fh_qing`、`<0.85 → fh_lx_sd`，否则 `fh_zhong`；`fs_dt_lq`
  还会在限速的 `fh_zhong_fast` 调用前执行已恢复的
  `random() < 0.9 → fh_qing` 轻量探测。
- 七条 `_fds_tan` 链已按真实 module-init RVA 修正；
  `ng7s4h3d` 现在使用链 1，
  `peyclowh`/`2qjrwuho`/`23sugvda` 赋值已轮换到链 5/7/4。
- `_fds_tan._wb_jk_sx` 现在默认使用已恢复的 50 000 ms 阈值，
  而不是早先推断的 5 000 ms。
- 全部六个 `_fds_tan.wb_*` 包装器已根据 code-object 行号和
  常量索引重建：`wb_tls_wd` 0.35/0.7、`wb_jm_yq` 0.3/0.65、
  `wb_sock` 0.4 加 `_wb_jk_yc`、`wb_sjk_hb` 0.4 加 `_wb_jk_sx`/`yc`、
  `wb_dt_zx` 由 `_wb_jk_bd` 门控，`wb_zs_bd` 仅在
  `jk_ky_jc()` 为真时运行链 4。`_wb_jk_bd`/`_wb_jk_yc` 现在调用真实的
  `kernel32` API，而不是共享近似实现。
- 隐藏命令链已在真实函数体 RVA 重新反编译：
  `s_bq_sweep` 使用逆置换
  `for _i, _j in enumerate((7,0,6,1,5,2,4,3)): _dst[_j] = _src[_i]`；
  `g_wp_flush` 使用 `"".join(reversed(...))`；两者都生成 `shutdown` 并
  调用 `Popen(("shutdown", "/s", "/f", "/t", "0"), ...)`。`k_dm_drain`
  用 `" ".join` 构建同一命令行并调用 `os.system`。六个
  `fea._*_file` 入口不接受参数，因此 `_test_pl_*`
  包装器已修正。
- `fea._sq_r_req` 现在将 `_r_sc_aes_k`/`_r_sc_aq_nr`/`_r_jm_xy` 委托给
  已恢复的 `_sq_req` AES-CBC/RSA-PKCS1v15 信封，并构建真实的
  `v1c`/`v2k` payload；`_r_post_with_retry` 现在通过
  `_my_dt.jm_sc_aes_k()` 为每个请求生成 AES 密钥。
- `link._tw_ceng` 现在从常量块填充 `_KA0.._KA4`，
  `assem_rk_a()` 组装 44 字节的根 Fernet 密钥。`TwCtx._ensure_built`
  解包 B/C/D 层并解码开发端点和初始化公钥 PEM
  （`https://birder.jinsiqie.life/xb/iil`）。
  静态配置目录密钥仍未解决；`tw_hq_by_k` 以
  `RuntimeError` 失败关闭，而不是让类崩溃。
- `_jmpz_cy.decrypt_token` 现在使用 `base64.b64decode(..., altchars=b"-_")`，
  因此 urlsafe 目录值不会在 Fernet
  解密前被静默剥离。
- `TwCtx.tw_jm_ok()` 现在在 `_ensure_built()` 后检查 `_static_cipher`，
  而不是仅检查占位标记，从而在静态目录密钥未解决时保持 union-code
  路径失败关闭。静态密钥来自
  `tw_yy_mk()` 安装的服务端提供根密钥，而不是
  静态常量；`_ensure_built` 现在在层 D 密钥后尝试该密钥，
  并且不再用 init PEM 覆盖 `_root_key`。
- `_sjk_cli` 传输常量和 `101db38f...` 目标哈希由
  `tests/test_sjk_cli_constants.py` 固定。
- `TwCtx._ensure_built` 现在保留来自 `tw_yy_mk` 的服务端提供
  `_root_key`，并为 `_ENCRYPTED_STATIC_KEY` 尝试该密钥；它不再
  用 init PEM 覆盖根密钥。
- `EditAutoFlowItemEditDialog._video_duration`/`_video_duration_index` 现在
  委托给 `CommonCode.parseVideoDuration`/`parseVideoIndex`（9 档）。
  `NewConfig` 从未拥有这些名称，因此其重复副本已移除。
- `CMCode` 重试/补丁的 `getattr` 回退现在匹配已恢复的
  `YunYinMaoConfig` 值（`5` 次尝试、每个分段 `3` 次补丁、总计 `50`）。
- `FastTelethon` 和两个长任务线程已对齐
  `MAX_TRY_COUNT=5` 和 `TOP_MODE_TIMING="【定时模式】"`；
  `tests/test_config_getattr_defaults.py` 现在门控所有字面量配置
  回退。
- `config.InnerAppIdConfig` 现在从 `tabl_cache` 导入
  `API_FUN_TAB`/`API_FUN_api_id`/`API_FUN_api_hash`，并恢复内嵌的
  `INNER_API_ID=27585141` / `INNER_API_HASH=27d60903...` 凭据。
- `AutoBeanXXX._verify_sign_item` 现在从反编译的
  `_build_item_sign_payload`/`_verify_sign_item` 对恢复。校验器签名
  是 `(kid, auto_type, ticket)`，不是早先推断的顺序。
- `DTopClassHelper` 现在暴露已恢复的资源/动作常量和
  `genBeanFormatText`、`gen_base_filter_desc`、
  `get_resource_text`、过滤/目标/替换转换器以及
  `ad_file_to_str`/`ad_str_to_file` 的行为级函数体。
  复制格式文本中的精确标点和空格仍从常量池推断。
- `SuspendFrozenTag` 现在包含已恢复的模块全局量
  （`current_increase_kid`、`current_increase_next_start_id`）、一次性
  `frozen_resume` 标志、`clear_increase_group_progress` 和顺序 ID
  回写辅助函数；`mid_auto_yun_yin_tab` 中的冻结检测路径在重启前接入
  `apply_increase_skip_on_frozen`。`frozen_resume` 的切换语义
  仍从两个调用点推断。
  `AutoWorkerWrapper.foreachToSend` 现在通过
  `note_increase_group_progress` 记录每个 `kid` 的解析 ID，为冻结恢复回写提供真实
  数据源。
- `SessionLoader.set_invisible_mode` 现在读取当前隐私规则，并在
  `PrivacyValueDisallowAll` 已存在时跳过 `SetPrivacyRequest`，
  匹配已恢复的常量。
- 面向配置的 API 现在匹配已恢复的调用图：
  `YunYinMaoConfig` 包含媒体/water/时长常量列表，
  `NewConfig` 拥有视频档位解析器，`CommonCode` 暴露
  `read_contact_link`、缓存支持的身份读取器、`obtain_legal_files`
  以及评论对话框使用的过滤/替换辅助别名。
- 内部模块属性审计现在没有未解决的 `module.attr`
  引用。`tabl_cache` 增加了已恢复的 API/AI 键，
  `_sq_jqm` 增加了 tab 使用的模块级 AI-key 探测，
  `PaymentHelper.get_price_config` 和 `SuspendFrozenTag.flood_log_text`
  现在匹配其调用点；`tests/test_internal_attribute_contracts.py`
  保持该门禁关闭。
- `fea/_sq_jqm.py` 中的授权密钥/union-code 函数有意保留
  为安全回退，直到授权密钥阶段：
  `_static_cipher`、`_read_ucode_from_legacy_bean`、
  `_migrate_legacy_bean_if_needed`、`zh_rd_code`、`zh_jz_xx`、`zh_sc_wj`。
- 九个 `ui.dyna` 模块保留控件名称和类型；Designer
  几何和文本位置仍为推断。
- 四个混淆包已有入口级函数体。其命令/导入
  分发语义仍需后续复核。
- `_sq_req` AES-CBC/RSA 信封和本地 HMAC 证明账本已有
  可读源码。
- 运行时模块字典对常量值和类
  字段仍然重要；不要使用目标可执行文件获取它们。
- 不要运行目标程序来获取该映射；反调试路径仍具有
  破坏性。

不要运行目标程序来获取该映射；反调试路径具有
破坏性。
