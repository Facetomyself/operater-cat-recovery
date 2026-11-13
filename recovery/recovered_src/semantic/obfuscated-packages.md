# 混淆包语义

## 包

加载器表暴露四个混淆包：

- `bz_uc`（22 个入口模块）
- `kv_nx`（23 个入口模块）
- `rm_qh`（23 个入口模块）
- `wp_jt`（23 个入口模块）

每个包都有一个 `_ops.py`（`kv_nx` 使用包 `__init__.py`）承载共享控制流原语。
入口模块是薄分派包装器。

## 共享模式

恢复出的辅助函数暴露：

- `import_module` / `load_attr` / `call_entry` / `call_method`；
- `emit` / `emit_signal` 用于 Qt 信号总线；
- `decode_abort_parts` / `abort_message` 用于编码中止目录；
- `show_error_tip` / `prepare_abort_dialog` 用于恢复 UI；
- `global_window` / `global_exception_handler` 和定时器；
- `hidden_popen` / `enable_privileges` / `system_command` 用于隐藏 Windows
  命令路径。

`bz_uc` 和 `wp_jt` 还包含 `AdjustTokenPrivileges` 使用的 `_LUID`、`_LAA` 和
`_TP` ctypes 结构。

## 已验证分派链

以下 `bz_uc` 条目由 `tests/test_bz_uc_dispatch.py` 按反编译常量顺序固定。
全部 22 个 `bz_uc` 入口模块均已覆盖：

- `aq_22_rt_78.yb_25_fan`：发出
  `global_ui_signal.notify_crypto_ctx_broken`，然后调用
  `bz_uc.xa_o6_yb_p3.qt_h5_go` 和 `kv_nx.be_s0_yb_p3.xa_o6_rx`。
- `ya_p1_xz_o4.aq_m7_sk`：`FdsHhx.seal_abort`、解码
  `_fds_sj.ABORT_PARTS_ENC`，在全局窗口可见时显示拼接后的中止消息，然后调用
  `wp_jt.vx_m2_wz_n1.km_b7_go` 和 `rm_qh.zc_q8_wy_n9.rt_i8_rx`。
- `bd_s8_mo_d9.ad_r9_go`：启用四个恢复出的权限目录槽位，然后启动五段隐藏
  命令元组。
- `km_74_qs_60.km_23_arm`：`threading.Timer(1.0)` 回调导入
  `kv_nx.zc_q2_or_f7` / `bz_uc.nq_e0_wz_n5` 并调用 `lo_c4_rx` /
  `eh_v3_go`。
- `pr_43_qs_39.xa_56_arm`：`threading.Timer(1.18)` 回调导入
  `kv_nx.xa_o6_wz_n5` / `bz_uc.vy_m8_ux_l9` 并调用 `nq_e0_rx` /
  `gi_x9_go`。
- `fi_49_qs_87.aq_87_fan`：发出 `report_probe_mid_fault`，然后调用
  `bz_uc.hk_y0_ce_t5.kn_b3_go` 和 `kv_nx.fh_w2_il_z7.ru_i4_rx`。恢复出的
  导入路径是 `kv_nx.fh_w2_il_z7`，不是早先重复的 `kv_nx.kv_nx` 路径。
- `nq_23_vy_24.cf_79_fan`：发出 `notify_link_integrity_fail`，然后调用
  `kv_nx.dg_u6_qt_h5.tv_k0_rx` 和 `bz_uc.ps_g8_ad_r9.mo_d9_go`。
- `ux_l9_rx` 和 `aq_m7_rx`：终止型 `gc.collect(2)` / `os._exit(1)` 条目。
  `_g/_o/_fn/_p` 是本地别名，不是参数。
- `uw_l7_ln_c2.sv_j1_sk`：中止消息组装、可选错误提示，然后调用
  `wp_jt.jl_a0_mp_d5.gs_w3_go` 和 `rm_qh.ps_g2_km_b7.np_e4_rx`。
- `hk_y0_ce_t5.kn_b3_go` 和 `jm_a6_kn_b3.ce_t5_go`：通过 `_ops.hidden_popen`
  进行五段隐藏命令分派。

`kv_nx` 已验证条目：

- `be_s0_ij_z5.jm_a6_sk`：仅在全局窗口可见时显示解码后的中止消息，用
  `\n\n` 拼接，然后调用 `rm_qh.gs_w3_df_u0.nq_e6_go` 和
  `bz_uc.gi_x9_hk_y8.ux_l9_rx`。
- `cf_44_ps_55.pr_40_fan`：发出 `cmd_socket_env_reject`，然后调用
  `wp_jt.ru_i0_gj_x5.ac_r3_go` 和
  `rm_qh.jm_a2_sv_j7.hj_y4_rx`。
- `dv_r4_uw_l7.tw_k2_sk`：与 `be_s0_ij_z5` 相同的 abort-tip 契约，然后调用
  `rm_qh.su_j5_nq_e6.ru_i0_go` 和 `bz_uc.qt_h5_tv_k0.yb_p3_rx`。
- `aq_m7_ln_c2.xz_o4_go`：内联 token 权限设置，在 `OpenProcessToken` 失败时
  使用五段 `subprocess.Popen` 回退。
- `hk_y8_gi_x9`：封存中止，仅在全局窗口可见时显示解码消息，然后调用
  `rm_qh.eg_v7_vx_m2.vy_m4_go` 和 `bz_uc.ya_p1_fh_w2.aq_m7_rx`。
- `pr_40_oq_84.ru_48_arm`：0.88 秒定时器分派到
  `wp_jt.xa_o0_ad_r5.ux_l3_go` 和 `rm_qh.bx_n2_yb_p7`（脱敏导出）。

`wp_jt` 已验证条目：

- `gj_x5_ft_v6.ac_r3_sk`：解码/显示中止消息，然后调用
  `bz_uc.dv_r4_uw_l7.sv_j1_go` 和 `kv_nx.xz_o4_eu_s1.zc_q2_rx`。
- `kn_b9_rt_i8`：解码/显示中止消息，然后调用两个恢复出的同级目标。
- `or_f3_df_u0`：`FdsHhx.seal_abort`、解码/显示中止消息，然后调用
  `bz_uc.bd_s8_mo_d9.ad_r9_go` 和 `kv_nx.pr_g6_ce_t5`。

`rm_qh.zc_q8_wy_n9.rt_i8_rx` 是零参数条目。其 `_g/_o/_fn/_p` code-object
varnames 是 `gc`/`gc.collect` 和 `os`/`os._exit` 的本地别名，不是参数。

## 分派表

以下名称只出现在分派字符串中。它们不是加载器表条目，也没有源文件；应视为
仅字符串分派目标，而不是缺失模块：

- `bz_uc`：`dg_u6_qs_h3`、`lo_c4_or_f7`、`ru_i4_il_z7`、`xa_o6_yb_p3`
- `kv_nx`：`be_s0_yb_p3`、`lo_c4_sv_j1`、`ru_i4_mp_d1`、`tv_k0_eh_v3`
- `rm_qh`：`bx_n2_yb_p7`、`jm_a2_sv_j7`、`tw_k6_mp_d5`、`zb_q6_gj_x5`
- `wp_jt`：`fi_w8_wy_n9`、`lo_c8_qt_h9`、`ru_i0_gj_x5`、`xa_o0_ad_r5`

## 置信度与安全

- 入口名、函数名和模块边界为加载器表精确。
- 全部 90 个单入口混淆模块都有匹配的恢复函数签名。
  `_re/audit_obfuscated_signatures.py` 比较恢复源码参数数量与 Hex-Rays 函数
  签名，并将仅含 tstate 的 C 函数体视为零 Python 参数函数。当前审计报告
  0 个发现和 0 个缺失证据。
- 隐藏命令操作数顺序、权限目录槽位以及一些脱敏/编码值属于推断。
- `hidden_popen` 和 `enable_privileges` 仅为定义。导入该包不会启动进程、
  加载 DLL、发出信号或终止解释器。
- 绝不要针对目标执行这些路径。反调试链具有破坏性。

## 证据

- `agent-notes/nuitka_module_table.json`
- `agent-notes/function_map_full.json`
- `agent-notes/source_recovery_audit.json`
- `agent-notes/decompiled/targets/`（入口级 Hex-Rays 证据）
- `recovered_src/tests/test_bz_uc_dispatch.py`
- `src/py/com/yun/mao/{bz_uc,kv_nx,rm_qh,wp_jt}/`
