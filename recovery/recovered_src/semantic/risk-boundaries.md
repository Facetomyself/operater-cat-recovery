# 风险边界

样本包含主动反分析行为。不要在宿主机上运行原始可执行文件。

## 已确认的静态链

- `link/_fds_sj.py`：针对 debugger、进程名、窗口标题、Frida、IDA、
  x64dbg、Cheat Engine、Procmon、Wireshark 及相关工具的已解码检测 catalog。
- `link/_fds_msgs.py`：308 条已解码的 `SEC_MSGS` 条目，以及中止对话框
  使用的六段式 `ABORT_PARTS_ENC` 消息。这些值是从常量块中恢复出来的
  明文，不是运行时解码结果。
- `link/_fds_catalogs.py`：四个已解码的检测 catalog
  （`STEMS` 71、`PREFIXES` 9、`MODULE_STEMS` 27、`WINDOW_KEYWORDS` 29）。
- `FdsHhx` 探测节奏：深度扫描 300 s，启动等待 5 s，快速扫描
  10–12 s，完整扫描 18–180 s。
- `FdsHhx.fh_cj` 响应阈值：0.55（`fh_qing`）、0.92（`fh_zhong`），
  否则为 `fh_quan`。
- `link/_fds_h_x.py`：启动探测、入口门禁和中止状态。
- `link/_fds_tan.py` / `_fds_rt.py`：探测和响应包装器。
- `link/_fdg_pw_rm.py`：隐藏的 `subprocess.Popen` 命令执行。
- `link/_fdg_ct_is.py`：token 权限调整。
- `link/_fdg_os_kx.py`：`os.system` 命令路径。
- `ade/_ade_sing.py`：文件系统扫描、隐藏/系统/reparse-point 检查。

应用日志和 Windows 事件 1074 此前显示过 `shutdown.exe` 响应。
本树不会执行或测试该路径。

## 动态代码

`fea/_dtdm_jz.py` 包含已恢复的 `marshal.loads` + `exec` worker 命名空间
加载器。它仅作为源码证据保留；离线测试从不调用它。`link/_sjk_cli.py` 和
`fea/_sq_req.py` 描述网络/加密流程，但不会由测试调用。

## 不透明的 `_fds_tan` 辅助函数

七个探测链辅助函数已完成反编译和映射。每个函数都使用显式的
`importlib` 模块/方法分派，由 `try_begin_abort()` 控制，并在 `finally`
块中通过 `seal_abort()` 关闭。路由已由 qword 链确认：

| 辅助函数体 RVA | 角色证据 |
| --- | --- |
| `0x57F83D0` | `_wb_jk_sx` 计时探测；`_wb_jk_bd()` + 50 000 ms 阈值 |
| `0x5843FE0` | `_nx_r4_qm`；`_u_h.sk_nt` → `wp_jt.pr_13_hk_48` → `bz_uc.nq_23_vy_24` |
| `0x5845990` | `_jv_c8_wt`；`_u_hgd.vm_star` → `rm_qh.aq_70_eg_67` → `kv_nx.cf_44_ps_55` |
| `0x5847340` | `_pl_a1_hz`；`_u_hvm.iv_sk` → `bz_uc.pr_43_qs_39` → `wp_jt.vx_16_il_49` |
| `0x5848CF0` | `_yk_m6_bd`；`_um_h.sk_ntm` → `kv_nx.pr_40_oq_84` → `rm_qh.kn_97_oq_36` |
| `0x584A6A0` | `_sg_e3_uf`；`_u_h.sk_nt` → `wp_jt.xz_59_tv_92` → `bz_uc.aq_22_rt_78` |
| `0x584C050` | `_to_x9_kr`；`_u_hvm.iv_sk` → `rm_qh.wz_79_su_79` → `kv_nx.hk_29_lo_78` |
| `0x584DA00` | `_wq_b2_ln`；`_u_h.sk_nt` → `bz_uc.ps_42_sv_93` → `wp_jt.ps_38_ad_71` |

constants/varnames 显示 `FdsHhx`、`_u_h`、`_u_hgd`、`_u_hvm`、`_um_h`，
概率位于 `0.3`-`0.7` 范围，以及 `fh_zhong`、`fh_qing`、`fh_lx_sd`、
`fh_quan`、`jk_ky_jc`、`seal_abort`、`vm_star`、`sk_nt`、`iv_sk` 等
方法。测试会 monkeypatch `importlib.import_module` 和 `FdsHhx`；
它们从不执行真正的反调试链。

## 安全规则

- 仅将 `_re/static_hybrid.exe` 作为分析镜像使用。
- 不要执行原始目标 `运营猫.exe`。
- 不要附加 Frida、debugger 或 injector。
- 任何未来的动态验证都必须使用一次性 VM，并隔离网络/电源/共享文件夹。
