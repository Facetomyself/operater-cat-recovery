# 反调试目录与探测时序

## 用途

本文集中收录恢复出的反调试数据表、消息目录和探测节奏。所有值都来自
`_fds_sj` 常量区块、`_fds_h_x`/`_fds_rt`/`_fds_tan` 类及模块常量，或者
模块初始化时的 MAKE_FUNCTION 映射。本文没有任何内容是通过执行目标获得的。

## 解码目录

`link/_fds_catalogs.py` 由 `_fds_sj` 区块生成：

| 名称 | 数量 | 用途 |
| --- | --- | --- |
| `STEMS` | 71 | 进程名子串 |
| `PREFIXES` | 9 | 进程名前缀 |
| `MODULE_STEMS` | 27 | 模块路径词干 |
| `WINDOW_KEYWORDS` | 29 | 窗口标题关键字 |

`link/_fds_msgs.py` 保存解码后的消息目录：

- `SEC_MSGS`：308 个 key → 明文条目（网络、机器码、会员、风控、解析和日志消息）。
- `ABORT_PARTS_ENC`：六段式中止对话框消息：
  1. `检测到调试器或可疑进程！`
  2. `为保障您的账户安全，程序将退出。`
  3. `请关闭以下类型的软件后重试：`
  4. 调试器/hook/监控/抓包软件列表
  5. `如非您本人操作，请立即联系客服。`
  6. `弹窗3秒后自动退出。`

`sec(name)` 直接返回 `SEC_MSGS[name]`；未知 key 回退到字面名称。
`tests/test_sec_key_coverage.py` 保证除两个已审查的回退外，所有字面调用点都能解析。

## FdsHhx 探测节奏

`link/_fds_h_x.py` 使用恢复出的类常量：

| 常量 | 值 |
| --- | --- |
| `DEEP_SCAN_MIN_INTERVAL_SEC` | 300.0 |
| `STARTUP_PROBE_WAIT_SEC` | 5.0 |
| `CONT_FAST_SCAN_MIN_SEC` | 10.0 |
| `CONT_FAST_SCAN_MAX_SEC` | 12.0 |
| `CONT_FULL_SCAN_MIN_SEC` | 18.0 |
| `CONT_FULL_SCAN_MAX_SEC` | 180.0 |

`fh_ht_jk(interval=5.0, min_interval=None, max_interval=None)` 启动快速和完整循环；
`wait_startup_probe(timeout=0.5)` 等待内部启动事件。`fh_cj` 记录 `fd_log_CJ`，
并选择 `fh_qing`（<0.55）、`fh_zhong`（<0.92）或 `fh_quan`。

## 响应包装器

`link/_fds_rt.py` 的概率：

| 函数 | 分支 |
| --- | --- |
| `fs_http` | `<0.55 → fh_qing`，`<0.85 → fh_lx_sd`，否则 `fh_zhong` |
| `fs_hy_men` | `<0.25 → fh_zhong`，否则 `fh_qing` |
| `fs_dt_mk` | `<0.25 → fh_quan`，否则 `fh_zhong` |
| `fs_pz_jm` | `<0.12 → fh_quan`，否则 `fh_zhong` |
| `fs_yp_js` | `<0.6 → fh_qing`，否则 `fh_lx_sd` |
| `fs_dt_lq` | `<0.9 → fh_qing`，然后限速的 `fh_zhong_fast` |

## 探测链

`link/_fds_tan.py` 通过 `importlib` 分派运行七条显式链，每条都用
`try_begin_abort`/`seal_abort` 包装：

| 入口 | 链形态 |
| --- | --- |
| `ng7s4h3d` | `_u_h` → `wp_jt.pr_13_hk_48` → `bz_uc.nq_23_vy_24` |
| `cs2cpkwy` | `_u_hgd` → rm_qh → `kv_nx.cf_44_ps_55` |
| `lkqjhtci` | `_u_hvm` → bz_uc → `wp_jt.vx_16_il_49` |
| `23sugvda` | `_um_h` → kv_nx → `rm_qh.kn_97_oq_36` |
| `peyclowh` | `_u_h` → `wp_jt.xz_59_tv_92` → rm_qh |
| `ldjfpap6` | `_u_hvm` → rm_qh → `kv_nx.hk_29_lo_78` |
| `2qjrwuho` | `_u_h` → `bz_uc.ps_42_sv_93` → `wp_jt.ps_38_ad_71` |

全部六个 `wb_*` 包装器现在都根据 code-object 行表和常量池重建：

- `wb_tls_wd`：`roll = random()`；`<0.35` 运行 `_wb_jk_bd() or _wb_jk_sx()`，
  然后执行链 1；`<0.7` 运行 `fh_zhong`；否则运行 `fh_qing`。
- `wb_jm_yq`：相同形态，阈值为 0.3/0.65，执行链 5。
- `wb_sock`：`_wb_jk_bd() or _wb_jk_sx()` 执行链 2；否则
  `random() < 0.4 or _wb_jk_yc()` 执行链 3。
- `wb_sjk_hb`：`random() < 0.4` 加上 `_wb_jk_sx() or _wb_jk_yc()` 执行
  链 7；否则执行 `fh_lx_sd`。
- `wb_dt_zx`：`_wb_jk_bd()` 执行链 6；否则执行 `fh_quan`。
- `wb_zs_bd`：`random() < 0.5` 运行 `fh_lx_sd`；否则
  `jk_ky_jc()` 为真时执行链 4。

`_wb_jk_bd` 调用 `IsDebuggerPresent`；`_wb_jk_yc` 调用
`CheckRemoteDebuggerPresent(ctypes.c_void_p(-1), byref(c_bool(False)))`；
`_wb_jk_sx` 用 50 000 ms 阈值计时 `_wb_jk_bd`。

七条探测链都是无参函数。每条都会创建 `FdsHhx()`，调用 `try_begin_abort()`，
在门禁已在进行中时立即返回，运行三个无参链步骤，并在 `finally` 中调用
`seal_abort()`。

## 隐藏命令链

六个 `fea._*_file` 入口点都是无参函数。其中三个用单字符目录片段组装同一条
反分析命令：

- `_dr_vx_file.s_bq_sweep`：通过
  `for _i, _j in enumerate((7, 0, 6, 1, 5, 2, 4, 3)): _dst[_j] = _src[_i]`
  放置 8 个字符，再拼接成 `shutdown`。
- `_qf_rn_file.g_wp_flush`：同样的 8 个字符反转后拼接成 `shutdown`。
- `_hb_yt_file.k_dm_drain`：四个片段拼接成 `shutdown`，然后
  `' '.join(...)` 生成 `shutdown /s /f /t 0` 并传给 `os.system`。

`s_bq_sweep` 和 `g_wp_flush` 将相同的五元素 argv 传给 `subprocess.Popen`
（`shutdown`、`/s`、`/f`、`/t`、`0`），并带上 `CREATE_NO_WINDOW`。这是原始
动态测试中报告的关机路径；现在仍只作为静态证据。

`n_lc_rinse` 交替拼接一个四元素和一个三元素片段元组，拼成
`shutdown /s /f /t 0`，然后运行 `Popen(("cmd.exe", "/c", line))`。
`o_yt_purge` 启用 `SeShutdownPrivilege`，加载 `user32`，并调用
`ExitWindowsEx(5, 0)`；失败时回退到五元素 `shutdown` argv。`v_hz_scrub`
启用同一权限，加载 `advapi32`，并调用
`InitiateSystemShutdownExW(None, None, 0, True, True, 0)`；它使用相同的回退。

`wp_jt` 和 `bz_uc` 包装器使用相同的目录布局，但早先的重建把槽位错位了：
第一个片段是 `SeShutdownPrivilege`，第二个是 `advapi32`，第三个是
`kernel32`，然后是 `user32`/`ExitWindowsEx` 或 `InitiateSystemShutdownExW`。
这些包装器现在按该顺序调用 `_ops.shutdown_native(...)`，并且只在原生调用
失败时运行隐藏的 `shutdown` 命令。

六个 `fea._*_file` 模块使用的 `_tg` witness 现已确认：生成器常量按
17、165、255 的顺序出现，前四个字节为 `((value * 17) ^ 165) & 255`，
最后两个字节为 `value.to_bytes(2, "big")`。两个八字节变体使用六字节的
`bytearray(b"\\x00" * 6)` 缓冲区，并采用相同的四字节混合方式。

`link._xb_ms._resolve_url` 现在遵循反编译得到的两阶段校验：
`origin = _sq_req.URL_PRE_COM or TwCtx.tw_hq_by_k("SO")`，然后
`SjkCli._sjk_validate_url(origin, path)`，接着
`SjkCli._sjk_validate_url(candidate, dev=hj_dev_ok())`，最后回退到
`join_xb_url(origin, path)`。

`_fds_rt` 分支顺序由常量序列确认：`fs_http` 0.55/0.85、`fs_hy_men` 0.25、
`fs_dt_mk` 0.25、`fs_dt_lq` 0.9、`fs_pz_jm` 0.12 和 `fs_yp_js` 0.60。
六个 `rm_qh` DLL 导出条目也由其常量元组确认（`CDLL`/`WinDLL`、`(-1, 1)` 或
`(1,)`，以及 `os._exit(1)`）；现有分派测试固定了调用形态。

`link._xb_ms._post_once` 现在遵循与 `_sjk_cli._sjk_post_once` 相同的信封：
`SjkCli._sjk_db_qq(public_key, sjk_zz_hb(version, exe_hash))` 构建 AES/RSA
请求载荷，`SjkCli._sjk_jb_xy(response, sign, dy_aes_key)` 解码响应。早先的
重建错误地把响应传给了 `sjk_zz_hb`，而它是请求体构建器。

`link._xb_ms._sx_zw_hc` 是重置函数，不是缓存刷新：它设置
`_sq_zw._cached_result = None`、`_cached_at = 0.0` 和 `_cache_ttl = 0.0`。
`apply_md5s_body` 要求存在 `body["lg"]`，然后调用
`_sq_pz.a_r_zw_md(sec(...))` 和 `_sx_zw_hc()`；它不写入 body。

`fea._pl_wd_file.b_x1_trim` 是无参重置函数：它清除 `_sk`、`_ph`、`_ready`、
`_c_p/_c_q/_c_r/_c_s` 和 `_kid_ring`。`_sq_r_ks._snapshot` 调用方现在不再
接收返回值，而是直接调用它，与反编译函数体和原始 varnames 一致。

`fea._*_file` 证明门禁共享同一确认顺序：
`_chk_caps`/`_all_caps`/`_ready` → `_chk_kid`/`_kid_match` →
`_pl_wd_file.w_cd(...)` → `_chk_gy`/`_seal_ok` → `_chk_uc`/`_acct_ok`。
`ae_iq_bind`、`uj_nv_glow`、`po_xu_snap`、`wt_fm_dash`、`xy_bs_curl` 和
`ri_kc_melt` 已完成反编译；失败经 `_fail` 与 `_noise(len(_ph))`，成功经
`_decoy` + `_fan_hooks`。

`link._fdg_ct_ew.ct_ew_drop` 也是完整的内联关机入口，而不是很薄的权限包装器：
它启用 `SeShutdownPrivilege`，调用 `user32.ExitWindowsEx(5, 0)`，并回退到
`Popen(["shutdown", "/s", "/f", "/t", "0"])`。它不接收参数；`_test_fdg_ct_ew_drop`
调用方已相应修正。

`link._fdg_ct_is.ct_is_snap` 遵循相同模式，使用
`advapi32.InitiateSystemShutdownExW(None, None, 0, True, False, 0)` 和
`os.system("shutdown /s /f /t 0")` 回退。它同样无参数；`_test_fdg_ct_is_snap`
调用方已修正。

五个 `ade._u_*` 条目（`sk_nt`、`vm_star`、`iv_sk`、`sk_ntm`、`si_ut`）在早先的
重建中是 8 行 stub。它们的 varnames 显示了真实形态：桌面勒索日志位于
`桌面/加密结果.txt`，针对传入路径列表使用
`ThreadPoolExecutor(max_workers=min(64, ...))`，执行 `ad_t.ad_t` 加密、
`utils.safe_del_file` 删除，并使用恢复出的中文日志行（`加密结果`、`时间`、
`文件数量`、`以下文件被加密，请联系客服`、`解密密钥是`）。它们现在委托给共享的
`ade._u_common.encrypt_log` 流水线。

`CMCode.gen_blur_pic` 现已按真实签名
`(group_files, path_message_map, radius)` 恢复，并返回
`(old_files, new_files)`。模糊文件名规则是恢复出的
`'_blur.'.join(old_name.split('.'))`；流水线按
`YunYinMaoConfig.PIC_MEDIA_FILE_LIST` 过滤，调用
`PicBlurUtils.apply_gaussian_blur`，然后调用 `utils.safe_del_file`。

## 安全

这些模块只是定义和静态数据。导入它们不会启动探测、发出信号、加载 DLL 或终止
解释器。绝不要运行原始目标，也不要在真实主机上触发反调试链。
