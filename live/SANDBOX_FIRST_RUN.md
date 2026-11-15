# 官方 PE 沙箱第一跑（2026-11-15）

约束：未在客户机安装分析工具；抓包在 NAS tap，不在 guest。

## 现象

- 客户机直接运行 `运营猫.exe`，提示环境初始化/检测失败。
- **没有关机。** 与宿主机「反调试后 shutdown.exe」不是同一条路。

## 抓包

文件：`capture_lab/win10-vm.pcap`（NAS 同源 `web_dev/operater-cat/capture/win10.pcap0`）
规模：209 包 / 68 KiB。

SNI：

- `birder.jinsiqie.life`（Cloudflare，完整 TCP：SYN/SYNACK/PSH/FIN，无 RST）
- `wdcp.microsoft.com` / `wdcpalt.microsoft.com`（Windows Defender 云，与业务无关）

其他：

- 客户机 `192.168.8.11` → NAS `192.168.8.16:445`（映射共享）
- 未见 DNS UDP；名称走 SNI / 缓存 / LLMNR
- **没有第二业务主机。** `_r_u` / `_f_pk` 仍未出现。

对 `birder` 的 Cloudflare 地址有多次 POST 级 PSH，次数与引导 `_BOOTSTRAP_MAX_RETRY = 4` 相符。TLS 应用数据未解密，故不能从本 pcap 读出内层 `code=-10` 原文；行为与「引导发出去了、rk 没落地、UI 报环境失败」一致。

## 和恢复树的对应

文案接近：

- `hj_fail_04` 环境检测失败
- `hj_init_fail_08` 初始化失败，请重启软件！
- `hj_load_02` 正在检测网络环境，请稍后...

启动链：`sjk_lq_qd` → 失败则进不了 `tw_hq_by_k("_r_u")`。

## 结论

这是沙箱 contacted **档 A**：官方 PE 在干净 Windows + 家庭网活着并打到了 birder，catalog 仍锁。

含义：过闸不再能用「本机 Clash / 分析机 JA3 / 不是官方 exe」单独解释。官方冻结 PE 在隔离 LTSC 上同样停在引导后。

下一步：把客户机 `YunYinData\log` 拷回 `guest-drop`，核对弹窗原文和是否有「非法客户端」。不要再给 `/xb/iil` 改信封。

## 客户机日志（YunYinData/log/2026-11-15_log.txt）

四次引导全部是本地校验证书失败，不是服务端 `-10`：

```
Cannot connect to host birder.jinsiqie.life:443 ssl:True
[SSLCertVerificationError] certificate verify failed: unable to get local issuer certificate (_ssl.c:1006)
环境检测失败: 初始化失败，请重启软件！
```

时间戳 17:23:31 / 33 / 39 / 44，对上 `_BOOTSTRAP_MAX_RETRY = 4`。
弹窗是 `hj_fail_tpl_05` 套了 `hj_init_fail_08`。

pcap 里的 TLS PSH 是握手/证书链，校验失败后 FIN；**没有成功的引导 POST**。
此前「行为像 -10」应更正：这一跑还没把信封打进服务端。

原因：`SjkCli` 用 `TCPConnector(ssl=True)`，不走 `_sq_zw` 的 `certifi.where()`。
Nuitka 自带 OpenSSL 3 在干净 LTSC 上拿不到 issuer。`guest-drop/certifi/cacert.pem` 其实在，只是引导路径没用它。

客户机下一步（二选一即可，不要关校验）：

1. 启动前设置 `SSL_CERT_FILE` 指向目录里的 `certifi\cacert.pem`
2. 给这台 LTSC 打根证书/Windows Update

然后再抓一次包。

## 成功启动（2026-11-15 18:29）

客户机日志（已脱敏）：

- `True`
- 注册本机码（前缀 `yunyinmao`）
- `校验指纹...`
- `环境检测成功`
- `单实例服务器启动成功`
- `是否使用了代理：`（空）

引导已过。NAS 抓包是成功之后才开的，这一段 pcap 里几乎只有 SMB 和 Microsoft 遥测，**没有抓到引导 POST / 第二业务主机**。程序若还开着，心跳仍可能打出 `_r_u`。

## 内存结论（不关客户机）

- 客户 RAM 里业务 HTTPS 仍只有 `birder.jinsiqie.life`。
- `_r_u` / `_f_pk` 以键名出现，旁边没有第二主机。
- 扫到 2 把互异的 RSA-2048 公钥：一把与引导层一致，一把是新的（候选 `_f_pk`/`_r_pk`）。PEM 只落在本地 `capture_lab/pems/`，不进对话。
