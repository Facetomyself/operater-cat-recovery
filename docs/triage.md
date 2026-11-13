# 分诊

## 已回答

- 为什么动态分析会关机：应用日志记录“反调试: 禁止调试 X”，随后 System 1074 记录 `shutdown.exe` 关机；代码中存在隐藏子进程、令牌提权和 `os.system` 原语。
- 反调试检测哪些工具：已解出 Frida、x64dbg/x32dbg、IDA/Hex-Rays、Cheat Engine、Process Hacker、Procmon、Wireshark、Fiddler、Charles、HTTP Debugger、PE-sieve、Scylla、HyperDbg 等名单。
- 卡密是否只存在本地：不是。`.code` 只保存机器码和多开计数，会员等级由远程接口返回。
- 是否有持久化：本次只读检查未发现目标启动项、计划任务、服务或 WMI 命令消费者。
- 源码还原进展：346/346 个 app 模块文件已铺开，10 个模块有 verified-order 函数映射，`_sq_jqm`、`_sq_chk`、`_fds_sj`、`_fds_jm`、`_fds_h_x` 和 `_fdg_*` 已有可读重建，368 个 Python 文件通过 `compileall`。

## 部分回答

- `ABORT_PARTS_ENC` 的键表和三档关机日志键已恢复，但值表尚未完全解码。
- “反调试: 禁止调试 7/8/10/13”与具体检测项的编号映射尚未完全还原。
- Telegram 会话是否被上传到授权服务器：静态证据不足。

## 未解决

- `shutdown.exe` 的完整命令行：Security 4688 未记录到相关事件。
- 服务端是否能下发可执行命令：目前看到的是价格/模型/客服/配置字段，未发现直接命令执行证据。
- 是否存在样本外的持久化或外部 watchdog：需要隔离 VM + 网络监控继续验证。

## 下一步（仅在隔离 VM）

1. 使用一次性 VM，禁用共享目录/剪贴板/网络，阻断 `shutdown.exe`、`ExitWindowsEx`、`InitiateSystemShutdown` 等电源路径。
2. 用静态补丁或 API hook 绕过 `_fds_sj` / `_fds_tan` / `_fdg_*` 的处置逻辑，再继续分析 `parse_report` / `hy_jx_bc`。
3. 如需验证外联，使用隔离网络和 DNS/代理日志，重点观察 `birder.jinsiqie.life`、Telegram、AI 接口。
4. 若目标是“去卡密”，优先在 VM 中做假服务端/公钥替换或 `parse_report` 分支 patch；不要在宿主机直接运行未中和反调试的样本。
