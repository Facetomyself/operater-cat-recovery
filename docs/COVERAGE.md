# 还原覆盖率

- loader 表中的应用/资源条目：357（346 个应用模块 + 11 个资源条目）
- 有源码文件的 loader 条目：357 / 357
- 模块索引：357 个条目；315 body、31 package、11 constants、0 empty
- 已产出的源文件：368
- 源码 AST：3127 个函数 / 262 个类
- 详细运行时元数据：47
- 有静态符号的模块：242
- 未分配静态符号：0
- 已解析的 Nuitka loader 条目：2777
- 已验证顺序的模块：10
- 函数 init 引用：2443
- 已命名引用：286
- 剩余空体 hook：8（fallback/logging/signal/monitor 的空操作方法）
- 剩余 stub 类：0
- semantic 文档：20
- 离线 pytest：102 个文件 / 388 个测试函数（455 个参数化用例）
- 至少有一个真实函数体/类体的模块：323
- 仅在字符串中出现的 `wp_jt` 引用：4 个名字，不是 loader 条目

原先的 `_sq_req._unsupported` 边界已替换为可读的 AES-CBC/RSA-PKCS1v15
请求信封还原。剩余工作是语义细化（已存在的 UI/业务体与推断出的协议细节），
不是缺文件或显式 `NotImplementedError` 空壳。还原体是行为级源码恢复，
不是逐字节原始源码。当前计数也写入 `agent-notes/source_stats.json`；
loader/文件审计在 `agent-notes/source_recovery_audit.json`。

- 第三方 import 记录在 `agent-notes/dependency_inventory.json` 和
  `requirements-recovered.txt`。
- 八个空体 hook 由 `tests/test_stub_allowlist.py` 固定；新增 stub 必须显式
  走 allowlist 审核。
- `MANIFEST.json` 固定每个源文件的 SHA-256 和行数。
- 精确函数名覆盖：492 个名字检查，492 个存在，0 缺失
  （`agent-notes/exact_function_coverage.json`）。
- 类方法名覆盖：1167 个限定方法检查，1167 个存在，0 缺失
  （`agent-notes/class_method_coverage.json`）。
- 未定义名审计：Ruff `F821/F811/F405` 通过，零发现。
- 构造调用审计：211 个直接类实例化检查，包含 dataclass 关键字/参数校验和
  继承字段解析；0 发现（`agent-notes/constructor_call_audit.json`）。
- `DTopClass` 的 dataclass 字段已按 Nuitka code-object varnames 对齐：
  `CommentRuleBean` 带完整 15 字段流 payload，`SuperFlowBean` 带
  link/mode/duration 字段，`AutoBean` 带 `completeVersionOp`/`botBean`。
  `tests/test_dclass_field_signatures.py` 固定字段顺序并拒绝未知构造关键字。
- `DTopClassHelper` 现在暴露还原出的 auto-bean 工厂链
  （`parse_ban_yun_flow`、`parse_auto_flow_or_yulan_flow`、`parse_down_load`、
  `parse_yun_auto`、`parse_yun_preview`），`dic_to_Auto_obj` 按 `auto_type`
  分发，包括 wire `beanLike` payload。
- `DTopClassHelper` 还恢复了常量池 helper：`dic_to_Comment_obj`、
  `dic_to_modelWrapper`、`gen_default_base_filter_bean`、`gen_yulan_des`
  以及 `ai_info` 别名。
- `dic_to_modelWrapper` 保留 `AutoBean` 访问器使用的
  mode-specific `startId`/`endId`/`wantCount`/`numberMode` 键，
  `ModelWrapper` 仍保留四个编译期 dataclass 字段。
- `AutoBeanXXX.ensure_valid` 按编译常量顺序执行：`time` 过期、
  `sha256(ucode).hexdigest().lower()` 绑定、execution-kid 匹配和
  item 签名验证。
- `_lk_gy_w` 的 `A|`/`B|`/`C|` HMAC payload、切片布局和
  `gy_jc_a1..a8` 校验链由 `tests/test_lk_gy_w_chain.py` 固定。
- `_fds_sj` 编码目录已完整解码进 `_fds_msgs.py`：308 个 `SEC_MSGS` 条目
  以及六段 `ABORT_PARTS_ENC` 消息。`tests/test_fds_messages.py` 固定代表性
  网络、机器码、会员和 abort 字符串。
- 四个反调试检测目录已按常量块重新对齐并移入 `_fds_catalogs.py`：
  `STEMS` 71、`PREFIXES` 9、`MODULE_STEMS` 27、`WINDOW_KEYWORDS` 29。
  早先的 9/21/29/29 布局有偏移且不完整。
- `FdsHhx` 探测时序按还原常量执行：深扫 300 秒、启动等待 5 秒、
  快扫 10–12 秒、全扫 18–180 秒；`fh_ht_jk` 与
  `wait_startup_probe` 签名由 `tests/test_fds_hx_timing.py` 固定。
- `FdsHhx.fh_cj` 输出 `fd_log_CJ`，并按还原的 0.55/0.92 分支选择
  `fh_qing`/`fh_zhong`/`fh_quan`，由 `tests/test_fds_hx_response.py` 固定。
- `tests/test_sec_key_coverage.py` 强制树中每个字面 `sec("...")` key 都能
  解析到 `SEC_MSGS` 条目，两个已审核的字面 fallback 除外。
- `_fds_rt.fs_http` 按反编译分支顺序执行
  （`<0.55 → fh_qing`、`<0.85 → fh_lx_sd`、否则 `fh_zhong`），
  `fs_dt_lq` 带还原的 `random() < 0.9 → fh_qing` 轻探针。
- 七条 `_fds_tan` 探测链已按真实 module-init RVA 重新映射；
  `tests/test_fds_tan_chains.py` 固定每个 module/method 元组。
- `_fds_tan._wb_jk_sx` 使用还原的 50000 ms 阈值
  （`time.perf_counter() * 1000 >= 50000`）。
- 六个 `_fds_tan.wb_*` wrapper 按反编译行表和常量池执行：
  `wb_tls_wd`（0.35/0.7）、`wb_jm_yq`（0.3/0.65）、
  `wb_sock`（0.4 + `_wb_jk_yc`）、`wb_sjk_hb`（0.4 + `_wb_jk_sx`/`yc`）、
  `wb_dt_zx`（`_wb_jk_bd` 门禁 + `fh_quan`）、`wb_zs_bd`
  （`<0.5 → fh_lx_sd`，否则 `jk_ky_jc → chain 4`）。三个 `_wb_jk_*`
  helper 使用真实 `WinDLL`/`IsDebuggerPresent` 和
  `CheckRemoteDebuggerPresent(c_void_p(-1), byref(c_bool(False)))`。
- 隐藏命令链与反编译片段一致：`_dr_vx_file.s_bq_sweep` 和
  `_qf_rn_file.g_wp_flush` 通过 `Popen` 启动 `shutdown /s /f /t 0`，
  `_hb_yt_file.k_dm_drain` 把同一行交给 `os.system`。六个
  `fea._*_file` 入口都是无参函数，`_test_pl_*` 调用方不再传 `self`。
- `fea._sq_r_req` 复用还原的 `_sq_req` AES-CBC/RSA-PKCS1v15 信封
  （`sq_sc_aes_k`/`sq_sc_aq_nr`/`sq_jm_xy`），并为每个请求生成独立 AES key，
  不再使用早先的 XOR 占位。
- `link._tw_ceng.assem_rk_a` 从六个还原的 `_KA*` 片段组装 44 字节 root
  Fernet key，`TwCtx._ensure_built` 解开 B/C/D 层。`tw_sjk_url()` 返回
  还原的 `https://birder.jinsiqie.life/xb/iil` 端点和 init 公钥 PEM。
- `_jmpz_cy.decrypt_token` 使用 urlsafe base64（`altchars=b"-_"`）解码目录值，
  与内嵌 `_ENCRYPTED_CONFIGS` 字母表一致。
- `TwCtx.tw_jm_ok()` 现在反映真实静态 cipher 可用性，因此目录 key 未解析时
  union-code 路径会 fail closed。
- `_sjk_cli` 传输常量（120 秒 / 30 秒 / 4 次重试 / 1.5 秒 / 可重试状态集）
  和目标 SHA-256 由 `tests/test_sjk_cli_constants.py` 固定。
- `TwCtx._ensure_built` 不再用 init PEM 覆盖 `_root_key`；`tw_yy_mk`
  提供的服务端 root key 会保留并用于静态目录 cipher。
- `EditAutoFlowItemEditDialog._video_duration` 和
  `_video_duration_index` 委托给
  `CommonCode.parseVideoDuration`/`parseVideoIndex`；重复 helper 已从
  `NewConfig` 移除（其常量池中没有这些名字）。
- `CMCode` 重试/补片 fallback 与 `YunYinMaoConfig` 一致
  （`MAX_TRY_COUNT=5`、`FILE_PART_PATCH_MAX_TOTAL=50`）。
- `tests/test_config_getattr_defaults.py` 拒绝任何
  `getattr(Config, "ATTR", <literal>)` 中与还原配置值不一致的 fallback。
- `config.InnerAppIdConfig` 现在从 `tabl_cache` 导入 `API_FUN_*` 缓存键，
  并携带还原的 `INNER_API_ID=27585141` /
  `INNER_API_HASH=27d6...`，不再使用脱敏占位。
- Tab UI 引用审计：7 个 controller / 88 个 `self.ui.*` 引用，0 缺失
  （`agent-notes/tab_ui_ref_audit.json`）。
- 静态 UI 引用审计：19 个 `uic.loadUi` 模块 / 84 个引用，0 缺失
  （`agent-notes/ui_ref_audit.json`）。
- 方法调用审计：970 个同类 `self.<method>` 调用，0 参数不匹配
  （`agent-notes/method_call_audit.json`）。
- Item-widget 审计：9 个 `Q*` list-item 类 / 137 个引用，0 缺失
  （`agent-notes/item_widget_ref_audit.json`）。
- `agent-notes/dyna_ui_text_inventory.json` 保存八个还原的
  `retranslateUi` 文本池。
- `agent-notes/dyna_setupui_trees.json` 保存还原的
  `ai_employee_item` 布局树（511 个 qword 引用）。
- `ai_employee_item` 现在输出嵌套树；五个旧 `label_em_*` 名字是隐藏的
  兼容 widget。
- `tests/test_dyna_ui_runtime_stub.py` 用假 PyQt5 执行全部八个生成
  `setupUi` 体，不加载随包的 Qt 扩展。

## UI/资源还原

- `src.resource.ui.dyna` 包和八个生成表单模块已存在。
- 七个编辑对话框都使用生成的 `Ui_Form` 模块，构造时不再依赖程序化 fallback。
- widget 名字和 `_TYPE_MAP` 覆盖严格匹配每个对话框的 `WIDGET_NAMES` 元组。
- `yun_yin_mao_main.Ui_MainWindow` 保留 `MainWindow` 使用的主窗口表面
  （`tabWidget_important`、`text_brow_log`、日志按钮、action）。
- `ui/static` 下有 32 个原始 Designer `.ui` 文件；还原类通过
  `uic.loadUi` 引用，UI 资源契约测试检查每个引用文件存在且可解析。
  七个 dyna 编辑对话框没有对应 `.ui`；其布局仍是生成/推断的，见
  `semantic/ui-resource-reconstruction.md`。
- 源码引用 27 个 `.ui`，5 个未引用：`ai_dy_config_tab.ui`、
  `duration_info_dialog.ui`、`huiyuan_link_desc_dialog.ui`、
  `type_item_desc_dialog.ui`、`youke_link_desc_dialog.ui`。这些文件名不在
  `static_hybrid.exe` 字符串表中，而被引用的 `.ui` 文件名都存在；它们是
  旧资源，不是缺失的 loader 模块。

`coverage.json` 是更早的 243 模块运行时快照；`COVERAGE.md` 和
`agent-notes/nuitka_module_table.json` 是 346 模块 loader 表遍历的权威来源。

## 核心反编译模块

- `src.py.com.yun.mao.fea._pl_wd_file`
- `src.py.com.yun.mao.fea._dr_vx_file`（命令/执行链；仅静态）
- `src.py.com.yun.mao.fea._sq_chk`
- `src.py.com.yun.mao.fea._sq_jqm`
- `src.py.com.yun.mao.auto.CMCode`
- `src.py.com.yun.mao.auto.TopicUtils`
- `src.py.com.yun.mao.auto.VideoProcessingIds`
- `src.py.com.yun.mao.mthread.SchedulerThreadClass`
- `src.py.com.yun.mao.mthread.TgClientBaseAsyncTaskThread`
- `src.py.com.yun.mao.link._lk_gy_w`
- `src.py.com.yun.mao.link._lk_gy_r`
- `src.py.com.yun.mao.link._xb_ms`
- `src.py.com.yun.mao.link._fds_sj`
- `src.py.com.yun.mao.link._fds_jm`
- `src.py.com.yun.mao.link._fds_h_x`
- `src.py.com.yun.mao.link._fdg_ct_is`
- `src.py.com.yun.mao.link._fdg_pw_rm`
- `src.py.com.yun.mao.telefast.RateLimiterClass`
- `src.py.com.yun.mao.telefast.RateLimiterHelper`
- `src.py.com.yun.mao.telefast.CallBack`
- `src.py.com.yun.mao.util.FloodGuard`
- `src.py.com.yun.mao.util.ResourcePath`
- `src.py.com.yun.mao.cd.TaskHardStop`（静态名字/调用边对齐：
  `_poster_lock`、`Qt.QueuedConnection`、`_ghost_snapshot`、
  `_teardown_worker_loop`）
- `src.py.com.yun.mao.monitor.MonitorSchedulerReport`（静态名字对齐：
  `sync_start_report`、`asyncio.run`、watchdog scheduler shutdown）
- `src.py.com.yun.mao.util.XAIKeyValidator`（恢复 `api_key.strip()`；
  不再合成 `self.parent` 属性）
- `src.py.com.yun.mao.log.glog`（构造字段、重叠感知的 tail 合并、
  pending-UI 队列和 cleanup 契约）
- `src.py.com.yun.mao.config.InnerAppIdConfig` 和 `config.net_config`
  （可调用 `INSTANCE().read_cache` 路径；三元组 SOCKS5 代理契约）
- `src.py.com.yun.mao.login.NetTest`（随机 net-test session 路径、
  精确连接提示、安全断开/删除清理、`FastNetTest` 回调形状）
- `src.py.com.yun.mao.login.SessionLoader`（os.walk session 扫描、
  通过 `sendAtName` 随机中文启动问候、FloodGuard 隐私请求、还原的
  autologin 签名、网络/认证/死亡/封禁状态机）
- `src.py.com.yun.mao.record.PublishIdRecord`（NewConfig/DTopClass 常量、
  卷文件名、消息链接构造、`log_publish_success`、高层
  `append_if_complete` / `_append_if_complete_inner` 映射、队列卷 writer、
  包装 JSONL 记录、原子 meta 写入、保留与轮转、link/id helper、type-map
  交换、磁盘+内存查找和 CMCode 兼容成功日志）
- `src.py.com.yun.mao.record.CommentCopyLedger`（懒加载卷索引、队列
  JSONL writer、原子 meta、id-key helper 和重载测试）
- `src.py.com.yun.mao.auto.AutoWorker`（停止预检查、执行日志与固定结果
  契约、传输速率初始化；账号检查 wrapper、按 bean 的
  `BizSleeper.biz_sleep(2, 5)`、`convert_mode` bean 转换；
  `obtainMessageAndParse` 按还原的动态 fetch/parse 状态机执行，
  包含随机/递增重试分支；`inner_working` 把 parse 列表接入
  `foreachToSend`、直发广告和汇总/收尾）
- `src.py.com.yun.mao.auto.GenSegmentVideoOnePass`（string/callable 配置
  值的 filter_complex 缓存目录处理）
- `src.py.com.yun.mao.auto.BanYunUnProtect`（成功频道发送调用还原的
  `log_publish_success`；成功评论发送调用
  `CommentCopyLedger.mark_after_send`）
- `src.py.com.yun.mao.auto.BanYunProtect`（成功文本/文件发送调用还原的
  `log_publish_success`）
- `src.py.com.yun.mao.auto.FlowProcess` 和 `YunProcess`（成功文本发送调用
  还原的 `log_publish_success`）
- `src.py.com.yun.mao.auto.CMCode`（真实 body 常量检查后移除了错误的
  album-ledger 调用；`log_publish_success` 保留）
- `src.py.com.yun.mao.auto.AutoWorkerWrapper`（私有广告成功记录改为
  `PublishIdRecord.log_publish_success`，不再用 AdIdMapManager；全局广告
  成功也使用同一记录器；`foreachToSend` 在每个 group 结果后调用还原的
  高层 publish-mapping 记录器）
- `src.py.com.yun.mao.remember.RandomBucketManager`（bucket 布局重建、
  session tried-window 跟踪、持久化 bucket 耗尽与重启重载；持久化 fallback
  标为 inferred）
- `src.py.com.yun.mao.ad.AdIdMapManager`（还原的 `ADMAP_INFO_KEY`、
  加密广告 id map 读写、去重 `updateAdIds` 和 key helper）
- `src.py.com.yun.mao.remember.RememberManager`（还原的 remember-map key、
  加密读写和 SHA-256 源/目标 key）

凡是 init 表给出命名 `compiled_function` 或 code-object varnames 的位置，
还原出的函数/类名和签名就是精确的。docstring 中标为 `inferred` 的 body 是
行为级翻译，不声称逐字节等于原始源码。

## 最大模块符号集

- `src.py.com.yun.mao.bz_uc`：25 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.kv_nx`：25 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.rm_qh`：25 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.wp_jt`：25 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.link`：9 个符号，状态 `detailed`
- `src.py.com.yun.mao.ade`：8 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.fea`：8 个符号，状态 `detailed`
- `src.py.com.yun.mao.util.need`：2 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ErrorDialog`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.GlobalExceptionHandler`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.MainWindow`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ad`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ad.AdIdMapManager`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ad.AddOrEditAdDialog`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ad.ToolsBoxEditAdDialog`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ad.UIAdListOp`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ade.ad_t`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ai`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ai.AI_DEFAULT_REFUSE_LIST`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ai.AiTextGenFlow`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ai.AiTextGenStatus`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ai.TextCache`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ai.TextProcessLogic`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.ai._ai_refusal_detect`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.auto`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.auto.AutoWorker`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.auto.AutoWorkerWrapper`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.auto.BanYunProtect`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.auto.BanYunUnProtect`：1 个符号，状态 `static-symbols`
- `src.py.com.yun.mao.auto.BizSleeper`：1 个符号，状态 `static-symbols`
