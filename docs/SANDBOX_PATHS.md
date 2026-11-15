# 沙箱拿 `_r_u` / `_f_pk`：路径分析

日期：2026-11-15
样本：运营猫 9.6.3，SHA-256 `101DB38FAAD3BA89F99A69EE3BE2F45334332520A2A813A5E69CAAA2D3D68AE0`
约束：不在宿主机跑官方 PE；不把合成 `rk` 当成果；不跟 JA3/JA4/出口指纹线混谈。

## 结论

`_r_u` / `_f_pk` 不在静态层。layer-D 只能解开 bootstrap URL（已知 `https://birder.jinsiqie.life/xb/iil`）。业务基址和请求公钥在 Fernet catalog 里，必须：

```text
官方冻结 PE 活到引导
  -> POST /xb/iil 带回 rk
  -> TwCtx.tw_yy_mk(rk)
  -> TwCtx.tw_hq_by_k("_r_u" / "_f_pk")
  -> 才出现第二条主机
```

沙箱这条线的唯一验收是 **contacted**（DNS/SNI/HTTP 对端）。
OpenTIP 那种「进程即起即停、NetworkActivities=[]」直接作废，不要拿它的 JA3 空报告当指纹对照。

contacted 分两档：

| 档 | 看到什么 | 能证明什么 | 能不能拿到 `_r_u` |
| --- | --- | --- | --- |
| A | 只有 `birder.jinsiqie.life` | PE 活着、引导包发出去了 | 不能。catalog 仍锁着 |
| B | birder 之后出现第二主机 | 引导过闸，`rk` 已进进程 | 能。SNI/DNS 就是 `_r_u`；内存里还能扫到 `_f_pk` |

组包打生产已经固定内层 `code=-10`，这条不要再做。指纹线（JA4 / 出口 / exe_hash 白名单）是解释 -10 的，不是沙箱目标。

## 为什么公开沙箱经常白跑

目标是 **Nuitka standalone 整目录**，不是 onefile。

- `original_project/app`：顶层约 63 个文件 + `aiohttp` / `cryptography` / `PyQt5` / `certifi` / `psutil` 等包目录。
- 完整树（含分析污染）约 3280 文件 / 719 MiB；去掉 ffmpeg/magick 仍约 494 MiB。
- Qt 插件在 `PyQt5/qt-plugins/platforms/qwindows.dll`。只丢 `运营猫.exe` 会立刻退出。

启动链还要求：

1. `FdsHhx` 扫进程名 / 窗口标题 / 模块：Wireshark、Fiddler、Charles、Procmon、Frida、IDA、x64dbg 都在名单里。命中就走关机链。
2. 恢复代码里 **没有** VMware/VBox/QEMU 特征名。干净 Windows VM 比「带监控的恶意软件沙箱」更合适。
3. 这是 PyQt5 GUI。无显示、10 秒就杀进程的 detonation，大概率到不了 `sjk_lq_qd`。
4. 引导用 `aiohttp` + 自带 Python 3.11 / OpenSSL 3.0.13；缺 `_ssl.pyd` / `libssl-3.dll` / `cryptography` 同样无网。
5. 宿主机 2026-11-10 日志已经证过：分析工具在场时会先写「反调试: 禁止调试 7/8/10/13」，再 `shutdown.exe`。那不是「没启动」，是启动后被处置。

所以 OpenTIP 空网是预期，不是「样本不联网」。

## 路径排序（只保留能出 contacted 的）

### P1. 干净交互式 Windows VM（正路）

一次性 Windows 10/11，不要装分析套件。

硬条件：

- 放完整 standalone，不要 37 个零散文件。可先去掉 `ffmpeg` / `magick` / `cv2` / `numpy`（引导不需要），但必须留 Qt、aiohttp、cryptography、certifi、psutil。
- 有桌面会话，等主窗口起来，至少 2–3 分钟。
- 出网只观察，不在客户机里开 Wireshark/Fiddler/Charles/Procmon。抓包放在 **宿主机或旁路 DNS/SNI**（路由器、Hyper-V 外 vSwitch、pktmon 看 VM 网卡）。
- 用策略挡住 `shutdown.exe` / `ExitWindowsEx` / `InitiateSystemShutdownExW`，避免再把宿主或 VM 干掉。
- 样本用 9.6.3 这一份，hash 必须是上面那条。不要拿 9.5 去撞 9.6.3 白名单。

看什么：

- 第一跳 SNI：`birder.jinsiqie.life` → 档 A，只证明活了。
- 第二跳不同 SNI/DNS → 档 B，那就是 `_r_u`。随后内存字符串可补 `_f_pk`。
- 若官方 PE 也停在 -10，contacted 会永远只有 birder。那时沙箱线结束，剩下的是指纹线，不要混进这份报告。

本机现在不行：Clash Verge TUN、WinINET `127.0.0.1:7897`、分析工具名单、`workspace.json` 明确禁止动态。本机只做过 birder 的 GET 405，不能当官方 PE 沙箱。

### P2. FreeBuf 云沙箱（队列可继续，但包装要改）

「9.5 传到 25/37」有三个坑：

1. 版本：当前恢复树 `version_code = "9.6.3"`，引导体带 `pre=version` 和 `exe_hash`。9.5 即使 contacted，hash 也可能直接 -10。
2. 文件数：37 个顶层文件不够。要 zip 整棵包目录，而不是逐文件续传。
3. 产品形态：若 FreeBuf 客户机里有 Procmon/Wireshark 一类进程名，官方 PE 会先关机再联网。必须看报告里的 **Network/DNS**，不要看「已完成扫描」。

FreeBuf 回执怎么用：

- `NetworkActivities=[]` 或无 DNS：与 OpenTIP 同类，换包装或放弃该平台，不要解读指纹。
- 只有 birder：档 A，记「PE 活了」，仍没有 `_r_u`。
- 出现第二域名：档 B，停上传，把域名/IP 落到证据，再谈内存。

### P3. 其它公开沙箱（Any.Run 交互 / CAPE / Joe）

同一套门：zip 整目录、交互桌面、出网、客户机不要出现名单进程、时长够。
Any.Run 交互模式比 OpenTIP 更接近 P1。标准自动 detonation 大概率重复空网。

### P4. 内存补证据（只在档 B 之后）

`TwCtx._ENCRYPTED_CONFIGS` 的明文只在 `tw_hq_by_k` 之后出现，且 `_sq_req._config_cache` 是进程内字典，没有落盘 `rk` 的证据。

档 B 之后才值得：

- 进程字符串扫 `https://`、PEM `BEGIN PUBLIC KEY`
- 不要在档 A 或空网时做内存 dump，那只会再次看到 Fernet 密文

## 明确不做

- 再给 `/xb/iil` 加头、改信封、对照 POST。
- 把合成 `rk` 写进图谱或当已解密 catalog。
- 用沙箱报告里的 JA3/JA4 去解释 -10（那是指纹线）。
- 在本机或带 Procmon/Wireshark 的客户机跑 `运营猫.exe`。
- 把 `original_project/app` 里的 `agent-notes`、`report.md`、`$null` 一并打包上传。

## 最小 contacted 合同

一份沙箱回执必须能勾这三项，否则不算解锁：

1. 样本 hash 是 9.6.3 这条，不是「某个 9.5 exe」。
2. 进程存活超过 GUI 启动窗口（秒级退出 = 失败）。
3. 有 DNS 或 TLS SNI 记录。空网直接关闭该平台。

有第二主机再开内存；没有第二主机就停在档 A，把问题交回「官方 PE 是否也被 -10」，不要在沙箱里继续猜字段。

## NAS VMM 作为远程 VM（2026-11-15 实查）

可以远程用 DS920+ Virtual Machine Manager 当 P1 宿主，但 **不能复用现有 guest**。

实时状态：

- 在跑：`rocky94-minimal`、`kali-2026.2`（各 2 vCPU / 4 GB）。二者都是持久资产，禁止当 disposable 沙箱，也禁止在上面跑官方 PE。
- Kali 是分析机，进程名单必中，会走关机链。
- VMM 空闲大约 4 vCPU / 9 GB RAM；存储足够。宿主机是 J4125 四核，1 分钟负载已经偏高，Windows 10 GUI 能跑但会肉。
- `/web_dev/iso` 里有 Win10/Win11 ISO 实体文件，**尚未 import 进 VMM 镜像库**。当前 VMM ISO 只有 Rocky。
- 远程控制面已通：`nas_vmm.py` 可 create / power / ISO；DSM 有 VNC 共享 API，Qt GUI 必须走控制台，不能无头秒杀。
- `Default VM Network` 走 NAS 局域网，不经过分析机 Clash TUN。抓包放 NAS/旁路，guest 里不要开 Wireshark/Fiddler/Procmon。
- guest 里的 `shutdown.exe` 只关这台虚机，不会关 NAS 或分析机。这是比宿主机安全的一点。

落地前还缺：新建一次性 Windows guest（建议 Win10 LTSC，2 vCPU / 4 GB，`autorun=0`）、import ISO、装系统、再拷 9.6.3 整目录。未获用户确认前不创建、不关机现有 VM。
落地进度（已建 guest）：

- 名称：`win10-ltsc-sandbox`
- 规格：2 vCPU / 4 GB / 64 GB 盘，`autorun=2`
- 状态：已开机，安装 ISO `win10-ltsc-2019-x64` 在第一槽，`boot_from=iso`
- 控制台：DSM → Virtual Machine Manager → 该 VM → Connect
- 下一步：控制台确认网卡/`ipconfig`，映射 NAS 共享后拷 9.6.3 整目录。客户机不要装分析工具。
- 装后收尾已做：ISO 已卸，`boot_from=disk`，虚机仍 running。VMM 暂无 Guest Agent。用户回报客户机 IPv4 为 `192.168.8.11`。本机 ICMP 超时，不据此否定地址。
- 虚机映射目录：`\\nas\web_dev\operater-cat\guest-drop`（NAS `192.168.8.16`）。已放入 9.6.3 官方目录 1524 个文件（含 `运营猫.exe`），不含分析产物。建议先拷到客户机本地再运行，不要直接在 SMB 上跑。

- 2026-11-15 第一跑：官方 PE 未关机；SNI 只有 birder + Microsoft Defender；无第二主机。详见 `capture_lab/SANDBOX_FIRST_RUN.md`。
