# 运营猫 9.6.3 静态分析报告

## 0. 结论摘要

- 目标是未签名的 Nuitka/Python 3.11 Windows 桌面程序，带 PyQt5、Telethon、aiohttp、cryptography、OpenCV、FFmpeg、ImageMagick 等依赖。
- **严重**：内置多层反调试/反分析逻辑。检测到调试器、Frida、x64dbg、IDA、Cheat Engine、Process Hacker、Procmon、Wireshark、Fiddler、Charles、HTTP Debugger、PE-sieve、Scylla 等工具后，会写入“反调试: 禁止调试 X”日志，并存在调用 `shutdown.exe` 执行系统关机的行为。
- 直接证据：应用日志在 `2026-11-10 12:57:43` 和 `13:07:13` 记录“反调试: 禁止调试 7/8/10/13”和“7/8/12”；Windows 系统事件 `1074` 在 `2026-11-10 13:08:01` 记录 `C:\WINDOWS\SYSTEM32\shutdown.exe` 发起关机。
- **高**：远程卡密/授权校验、Fernet/RSA 加密配置、机器码绑定、文件系统扫描（含 `ghidra-master`）、隐藏数据目录、Telegram 会话处理。
- **代码还原**：已解析 Nuitka 模块加载表，346 个 app 模块文件全部铺开；核心授权/反调试模块已有可读源码，368 个 Python 文件通过 `compileall`。
- **建议**：立即停止在宿主机运行和动态分析；仅在一次性隔离 VM 中继续；轮换 Telegram 会话与相关凭据；检查持久化和网络外联。

## 1. 样本与打包信息

- 入口：`D:\reverse_ENV\workspace\operater-cat\运营猫.exe`
- 大小：`161,002,496` 字节
- SHA-256：`101DB38FAAD3BA89F99A69EE3BE2F45334332520A2A813A5E69CAAA2D3D68AE0`
- 数字签名：未签名（`NotSigned`）
- 版本信息：FileDescription / ProductName / CompanyName / FileVersion 均为空
- 运行时：Nuitka standalone，Python 3.11.9，PyQt5、Telethon、aiohttp、requests、cryptography、OpenCV、FFmpeg、ImageMagick、numpy、PIL、pywin32
- Python DLL：改名后的 5.8 MB DLL，SHA-256 `0817A2A657A24C0D5FBB60DF56960F42FC66B3039D522EC952DAB83E2D869364`

打包细节：PE 表里的 `.text` 原始偏移与运行时代码不一致；真实 Nuitka 代码在文件偏移上整体后移 `0x5000000`。按常规 RVA 反汇编会读到错位数据，需使用 `file_offset = 0x400 + (rva - 0x1000) + 0x5000000` 才能对应内存中的真实函数。

## 2. 反调试与关机链（严重）

### 2.1 模块分工

- `src.py.com.yun.mao.link._fds_sj`：`FdsHhx` 反调试主逻辑，检测调试器、进程名、窗口标题、模块/内存映射。
- `src.py.com.yun.mao.link._fds_tan`：调试状态探测与辅助检查。
- `src.py.com.yun.mao.link._fds_h_x`：反分析共享状态、`entry_blocked` / `try_begin_abort` / `seal_abort`。
- `src.py.com.yun.mao.link._fds_jm`：XOR 字符串解码、`sec`、`decode_str_tuple`。
- `src.py.com.yun.mao.link._fdg_pw_rm`：隐藏窗口子进程执行器，使用 `subprocess.Popen`、`CREATE_NO_WINDOW`、`DEVNULL`。
- `src.py.com.yun.mao.link._fdg_ct_is`：进程令牌提权，使用 `OpenProcessToken`、`LookupPrivilegeValueW`、`AdjustTokenPrivileges`。
- `src.py.com.yun.mao.link._fdg_os_kx`：`os.system` 命令执行。
- `src.py.com.yun.mao.ade._ade_sing`：文件系统扫描，查找 `ghidra-master`、隐藏/系统/重解析点文件。

### 2.2 检测项

- `IsDebuggerPresent`、`CheckRemoteDebuggerPresent`。
- 进程名扫描：`psutil.process_iter`、进程名缓存、快/慢/深度扫描。
- 窗口标题扫描：`EnumWindows`、`IsWindowVisible`、`GetWindowTextLengthW`、`GetWindowTextW`。
- 模块/内存映射扫描：`memory_maps`、模块路径、`ZombieProcess` 处理。
- 启动阻断：`entry_blocked`、`STARTUP_PROBE_WAIT_SEC`。
- 处置分级：`fh_qing`（轻）、`fh_zhong`（中）、`fh_quan`（全）、`fh_cj`（触发）。
- 日志键：`fd_log_RA`、`RB`、`RC`、`RW`、`RPE`、`RPP`、`RM`、`JC`、`CJ`、`QB`、`GD_QING`、`GD_ZHONG`、`GD_QUAN`、`GD_CJ`。其中 `GD` 高度疑似“关机”，`QING/ZHONG/QUAN` 对应轻/中/全三档。

### 2.3 已解出的检测名单

字符串使用 16 字节 XOR key 加密，key 与密文均可在静态文件中恢复。以下为已确认解出的名单（完整输出见 `agent-notes/enc_blocks_decoded.txt`）：

- 进程/工具 stem：`cheatengine`、`ida`、`frida`、`dnspy`、`scylla`、`x64dbg`、`x32dbg`、`hyperdbg`、`pe-sieve`。
- 前缀：`x64bridge`、`x64dbg`、`x32dbg`、`x96dbg`、`ollydbg`、`vehdebug`、`ida64`、`idat64`、`idaplg64`、`cheatengine-x86_64`、`cheatengine-i386`、`frida-agent`、`frida-gadget`、`frida`、`scyllahide`、`titanhide`、`sharpod`、`strongod`、`dnlib`、`dnspy`、`apimonitor`。
- 模块/窗口关键词：`x64dbg`、`x32dbg`、`x96dbg`、`ollydbg`、`windbg`、`immunity debugger`、`hyperdbg`、`cheat engine`、`cheatengine`、`process hacker`、`procmon`、`ida`、`ida pro`、`hex-rays`、`dnspy`、`megadumper`、`hollows hunter`、`pe-sieve`、`frida`、`api monitor`、`rohitab api monitor`、`winapioverride`、`scylla`、`scyllahide`、`fiddler`、`wireshark`、`http debugger`、`charles`、`reclass`。
- 弹窗文案：`检测到调试器或可疑进程！`、`为保障您的账户安全，程序将退出。`、`请关闭以下类型的软件后重试：`、`弹窗3秒后自动退出。`

### 2.4 关机触发链

应用日志 `D:\reverse_ENV\workspace\YunYinData\log\2026-11-10_log.txt`：

```text
2026-11-10 12:57:43 反调试: 禁止调试7
2026-11-10 12:57:43 反调试: 禁止调试8
2026-11-10 12:57:43 反调试: 禁止调试10
2026-11-10 12:57:43 反调试: 禁止调试13
...
2026-11-10 13:07:13 反调试: 禁止调试7
2026-11-10 13:07:13 反调试: 禁止调试8
2026-11-10 13:07:13 反调试: 禁止调试12
```

Windows 系统事件 `1074`：

```text
TimeCreated: 2026-11-10 13:08:01
Process:     C:\WINDOWS\SYSTEM32\shutdown.exe (MENGMA)
Shutdown Type: 关机
Reason Code:   0x800000ff
User:          MENGMA\mengma
```

代码层证据：

- `_fdg_pw_rm` 使用 `subprocess.Popen`，带 `CREATE_NO_WINDOW`、`DEVNULL`、`shell`、`stdin/stdout/stderr`、`creationflags`，并包含三个在工具输出中被脱敏的常量；其形态与 `shutdown.exe` 命令及参数一致。
- `_fdg_ct_is` 使用 `GetCurrentProcess`、`OpenProcessToken`、`LookupPrivilegeValueW`、`AdjustTokenPrivileges`、`CloseHandle`，具备启用关机/调试相关令牌权限的能力。
- `_fdg_os_kx` 使用 `os.system`，提供另一条命令执行路径。
- `ABORT_PARTS_ENC` 字典包含 `fd_log_GD_QING`、`fd_log_GD_ZHONG`、`fd_log_GD_QUAN`、`fd_log_GD_CJ` 等键，和“轻/中/全/触发”处置分级对应。
- `shutdown.exe`、`ExitWindowsEx`、`InitiateSystemShutdown` 等敏感命令/API 名在静态文件中没有明文，说明关机命令经过 XOR/字符串混淆；这本身也是规避静态检测的行为。

结论：这不是普通崩溃或用户误操作，而是**检测到分析工具后主动执行系统关机**的破坏性响应。日志时间、事件日志时间和代码原语三者一致。

### 2.5 反取证与文件系统扫描

- `ade._ade_sing` 会扫描磁盘、`Program Files (x86)`、`Program Files`、`AppData`、`ProgramData`、`System Volume Information`、`$Recycle.Bin`、`Windows.old`、`$WinREAgent`、`Documents and Settings`、`node_modules`、`Recovery`、`README.md`、`LICENSE.txt` 等位置，并专门查找 `ghidra-master`。
- 检查 `FILE_ATTRIBUTE_HIDDEN`、`FILE_ATTRIBUTE_SYSTEM`、`FILE_ATTRIBUTE_REPARSE_POINT`，用于发现隐藏/系统/重解析点文件。
- `set_hidden_recursive` 使用 `win32api.GetFileAttributes` / `SetFileAttributes` 和 `FILE_ATTRIBUTE_HIDDEN` 递归隐藏 `YunYinData` 目录，属于反取证行为。

## 3. 卡密/授权架构（原始任务背景）

### 3.1 远程校验

- 授权接口：`https://birder.jinsiqie.life/xb/iil`。
- 客户端使用 `TwCtx` 解密内置配置：Fernet 加密的 URL、RSA 公钥、静态 Fernet key。
- `_fds_rt.fs_http` 负责 POST，请求包含版本、EXE 哈希、机器码、加密 payload、签名。
- `_sq_chk.parse_report` / `hy_jx_bc` 解析服务端返回的 `data`，更新 `_sq_jqm.current_account_info`。
- `_sq_jqm` 维护 `ucode`、`status`、`grade`、`limit`、`expire`、`aiAbility`、`botAbility`、`mul` 等字段。

### 3.2 本地缓存

- 缓存文件：`%APPDATA%\Microsofteis\lang\union_code_release\union_code\.code`。
- 内容为 Fernet token，解密后仅包含 `ucode`（机器码）和 `muli`（多开计数），**不包含会员等级**。
- 会员等级来自服务端每次校验，简单改 `.code` 不能解锁。

### 3.3 对“去卡密”的含义

- 仅改本地缓存无效；需要让 `parse_report` / `hy_jx_bc` 走会员数据分支，或替换服务端响应/公钥并伪造签名。
- 该程序会在检测到调试/注入时执行关机等破坏性动作，**不适合在宿主机上做动态 patch**。
- 如继续逆向，应先在一次性 VM 中阻断 `shutdown.exe`/电源 API、断网、禁用共享目录，再做离线补丁或假服务端实验。

## 4. 数据与隐私风险

- Telegram 会话处理：`telethon`、`SessionLoader`、`TGAuthAccount`、`FastTelethon`、`session_abs_path`、`autologinWithSession` 等；会话目录为 `YunYinData\tgaccount`。本次运行该目录为空，但程序具备读取/自动登录 Telegram 会话的能力。
- 机器码绑定：`CMCode`、`FakeUniqueMachineCode`、`ucode`，机器码会发送到授权服务器。
- 服务端可控字段：`priceConfig`、`modelList`、`maoContacts`、`keFu`、`cloudBot`，用于价格、模型、客服链接等 UI/业务逻辑。
- AI 相关：`api.x.ai`、OpenAI API、`apiKey` 字段；可能保存或使用第三方 API key。
- 日志：`YunYinData\log\*.txt` 记录机器码、环境检测、风控提示、反调试触发等信息。

## 5. 持久化与系统面检查

- 未发现指向 `operater-cat` / `运营猫` / `YunYinData` 的启动项、Run/RunOnce、计划任务、服务或 WMI 命令消费者。
- `hosts` 与防火墙未发现 `birder.jinsiqie.life` 或该程序的条目。
- 唯一确认的系统级破坏行为是运行期的 `shutdown.exe` 关机。
- EXE 未签名、无版本信息，降低了溯源和完整性判断能力。

## 6. 证据索引

- 静态关键词扫描：`agent-notes/static_scan.txt`
- 关键 API/命令上下文：`agent-notes/keyword_context.txt`
- 反调试模块字符串：`agent-notes/fds_sj_strings.txt`
- 解密后的检测名单：`agent-notes/enc_blocks_decoded.txt`
- 文件哈希清单：`agent-notes/file_hashes.json`
- 运行时模块/授权对象 dump（关机前采集）：`_re/runtime_dump.txt`、`_re/runtime_secrets.txt`
- 应用日志：`D:\reverse_ENV\workspace\YunYinData\log\2026-11-10_log.txt`
- 关机事件：Windows 系统事件 1074，`2026-11-10 13:08:01`

## 7. 处置建议

1. 停止在宿主机运行该程序；不要再做 Frida/调试器/注入类动态分析。
2. 在一次性隔离 VM 中继续分析，禁用共享目录/剪贴板/网络，阻断 `shutdown.exe` 和电源相关 API。
3. 轮换 Telegram 账号会话与相关凭据；删除 `YunYinData\tgaccount` 中可能存在的 `.session` 文件。
4. 检查网络侧是否有向 `birder.jinsiqie.life`、Telegram、AI 接口的可疑外联；保留日志。
5. 若该程序曾以管理员权限运行，建议做一次主机完整性检查和凭据轮换。
6. 如果仍要推进“去卡密”，先在 VM 中中和 `_fds_sj` / `_fds_tan` / `_fdg_*` 的关机路径，再处理 `parse_report` / `hy_jx_bc` 或假服务端；不要在宿主上直接试补丁。

## 8. 未完成项

- `shutdown.exe` 的完整命令行未捕获：Security 4688 未记录到相关事件。
- `ABORT_PARTS_ENC` 的值表尚未完全解码，但键表和三档关机日志键已经确认。
- 是否曾把 Telegram 会话/API key 外传到授权服务器：静态证据不足，需要隔离 VM 的网络抓包。
- 服务端是否能下发可执行命令：目前看到的字段以价格/模型/客服/配置为主，未发现直接命令执行证据。
- Nuitka 全量反编译不可行；当前结论基于静态字符串、模块结构、机器码和系统日志证据。

## 9. 代码还原进展

- `recovered_src/` 已补齐到 346 个 app 模块文件；当前源码树为 368 个 Python 文件、3127 个函数、262 个类，`compileall` 全部通过。
- 解析到 Nuitka `MetaPathBasedLoaderEntry` 表：`.data` RVA `0x854E100`，2777 个嵌入模块记录；346 个 app 模块，记录格式为 `name / python_init_func / bytecode_index / bytecode_size / flags`。
- 从模块初始化函数提取 2443 个 `.pdata` 函数入口引用；其中 286 个引用已落到具体名字，10 个模块已 verified-order。
- 真实模块树已写回核心源码：
  - `recovered_src/src/py/com/yun/mao/fea/_sq_jqm.py`：`SqJqm` 账号模型、字段和方法。
  - `recovered_src/src/py/com/yun/mao/fea/_sq_chk.py`：`is_success`、`parse_report`、`hy_jx_bc`。
  - `recovered_src/src/py/com/yun/mao/link/_fds_sj.py`：解码后的反调试名单和 200 个日志键。
  - `recovered_src/src/py/com/yun/mao/link/_fds_jm.py`：XOR/base64/UTF-8 解码、`sec` 缓存。
  - `recovered_src/src/py/com/yun/mao/link/_fds_h_x.py`：`FdsHhx` 启动探针、进程/窗口/模块扫描、分级响应。
  - `recovered_src/src/py/com/yun/mao/link/_fdg_*.py`：隐藏子进程、令牌权限、`os.system` 和命令包装。
- 反调试函数映射表：`agent-notes/anti_debug_function_map.json`；全量函数引用：`agent-notes/function_map_full.json`。
- 已补齐 `_tw_ctx/_tw_ceng/_jmpz_cy` 授权配置层、`_sq_r_bao` payload、`ade` 文件扫描/AES-GCM 链（默认 dry-run）以及机器码/API 配置模块。
- 离线验证：`SqJqm` 游客/会员/多开/企业版判定通过；`_fds_jm` 名单解码通过；`TwCtx` 配置目录为 21 项；扫描器 dry-run 通过；`compileall` 368 个源码文件通过；pytest 455 个用例通过。
- 当前限制：`_sq_req` 已从占位壳改为 AES-CBC/RSA-PKCS1v15 请求信封重建；剩余不确定项集中在界面/业务模块和未能静态观察到的协议细节，不能宣称逐字节还原原始源码。
- 运行时映射已确认：`_re/static_hybrid.exe` 同时映射内层 app 代码和外层运行时；`compiled_function` 对象大小 `0xE0`，`+0x78` 是 C 函数指针，`+0xB8` 是名字，`+0xC8` 是哈希；`tp_call`、`tp_dealloc`、`tp_repr`、`tp_hash` 已定位并反编译。
