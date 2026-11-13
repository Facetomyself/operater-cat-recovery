# 反调试/响应映射（静态重建）

## 检测列表（从 XOR 加密元组解码）

- 进程/工具 stem：`cheatengine`、`ida`、`frida`、`dnspy`、`scylla`、
  `x64dbg`、`x32dbg`、`hyperdbg`、`pe-sieve`。
- 前缀：`x64bridge`、`x64dbg`、`x32dbg`、`x96dbg`、`ollydbg`、
  `vehdebug`、`ida64`、`idat64`、`idaplg64`、`cheatengine-x86_64`、
  `cheatengine-i386`、`frida-agent`、`frida-gadget`、`frida`、
  `scyllahide`、`titanhide`、`sharpod`、`strongod`、`dnlib`、`dnspy`、
  `apimonitor`。
- 模块/窗口关键词：`x64dbg`、`x32dbg`、`x96dbg`、`ollydbg`、
  `windbg`、`immunity debugger`、`hyperdbg`、`cheat engine`、
  `cheatengine`、`process hacker`、`procmon`、`ida`、`ida pro`、
  `hex-rays`、`dnspy`、`megadumper`、`hollows hunter`、`pe-sieve`、
  `frida`、`api monitor`、`rohitab api monitor`、`winapioverride`、
  `scylla`、`scyllahide`、`fiddler`、`wireshark`、`http debugger`、
  `charles`、`reclass`。

## 响应层级

- `fh_qing` / `fh_zhong` / `fh_quan`：轻 / 中 / 全响应。
- `entry_blocked`：启动探测阻断入口。
- `try_begin_abort` / `seal_abort`：中止/封口路径。
- `fd_log_GD_QING` / `fd_log_GD_ZHONG` / `fd_log_GD_QUAN` /
  `fd_log_GD_CJ`：关机层级日志键（`GD` 很可能表示关机）。

## 命令执行原语

- `_fdg_pw_rm`：使用 `CREATE_NO_WINDOW`、`DEVNULL`、
  `shell`、`stdin/stdout/stderr`、`creationflags` 的 `subprocess.Popen`。
- `_fdg_ct_is`：`OpenProcessToken` / `LookupPrivilegeValueW` /
  `AdjustTokenPrivileges`。
- `_fdg_os_kx`：`os.system`。

## 直接证据

- 应用日志：`2026-11-10 12:57:43` 和 `13:07:13` 包含
  `反调试: 禁止调试7/8/10/13` 与 `7/8/12`。
- Windows 系统事件 1074：`2026-11-10 13:08:01`，
  `C:\WINDOWS\SYSTEM32\shutdown.exe` 发起关机。

## 已恢复入口映射

Nuitka `MetaPathBasedLoaderEntry` 表已在 `.data` RVA
`0x854E100` 解析，以下 initializer-to-body 映射已验证：

- `_fds_rt`：`fs_jc_qd`、`fs_ui_ok`、`fs_sjk_ws`、`fs_sjk_qd`、`fs_http`、
  `fs_hy_men`、`fs_zh_tb`、`fs_dt_mk`、`fs_dt_lq`、`fs_by_pf`、`fs_pz_jm`、
  `fs_yp_js`。
- `_fds_jm`：`xor_bytes`、`decode_str`、`decode_str_tuple`、`sec`、
  `_decode_one_sec_msg`。
- `_fdg_cm_rx`：`cm_rx_push`。
- `_fdg_ct_ew`：`ct_ew_drop`。
- `_fdg_ct_is`：`ct_is_snap`。
- `_fdg_os_kx`：`os_kx_blow`。
- `_fdg_pw_rm`：`pw_rm_fire`。

重建后的源码函数体位于
`recovered_src/src/py/com/yun/mao/link/`；机器可读映射为
`agent-notes/anti_debug_function_map.json`。
