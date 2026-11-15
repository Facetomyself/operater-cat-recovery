# 本机连接验证与抓包结果

## 结论

本机可以做连接验证，也可以做 TLS 握手抓包；但当前默认路由被 Clash Verge 的
`Meta` TUN 接管，不能代表干净直连出口。之前所有合成请求看到的服务端判定，
都可能同时受代理出口 IP、TLS 指纹和代理链路影响。

这次没有启动原始 PE，也没有重放 `v1c/v2k`，只做了 DNS、TCP、TLS 和 GET 探测。

## 网络路径

```text
DNS: birder.jinsiqie.life
  A    198.18.4.64
  AAAA 2001:2::419

默认路由:
  0.0.0.0/0 -> 198.18.0.2 (Meta, metric 0)

本机网卡:
  以太网 192.168.8.19/24
  Meta Tunnel (Clash Verge)

代理进程:
  clash-verge.exe
  clash-verge-service.exe
  verge-mihomo.exe

WinINET:
  ProxyEnable=1, ProxyServer=127.0.0.1:7897
```

实际出口 IP：

```text
56.10.113.225
```

使用 `curl --interface 192.168.8.19` 绕过 TUN 的尝试超时，说明当前主机没有
可直接验证的干净直连路径。

## 目标端点

```text
https://birder.jinsiqie.life:443
TCP 443: open
TLS: Cloudflare
HTTP: 1.1
GET /xb/iil -> 405 Method Not Allowed
Allow: POST
CF-RAY: ...-SIN
alt-svc: h3=":443"
```

这说明本机到 bootstrap 域名的链路可达，且该路径只接受 POST；不能用 GET 的
405 判断业务鉴权结果。

## TLS 指纹

### curl / Schannel

```text
TLS 1.2
JA3: c24b650e67952c6b705a154cedf959e8
ALPN: http/1.1
```

### Python 3.13 / OpenSSL 3.0.18

```text
TLS 1.3
JA3: b1032c06831464f33ce78e33c8adc8ae
ALPN: none
```

目标自带的是 Python 3.11 + OpenSSL 3.0.13；本机 Python 3.13/3.0.18 只能做近似
对照，不能替代官方进程的真实 ClientHello。

## 抓包能力

`pktmon` 可用，已落盘：

- `capture_lab/birder_tls.etl`：curl 握手原始 ETL。
- `capture_lab/birder_tls.txt`：带十六进制载荷的文本。
- `capture_lab/python_tls.etl`：Python/OpenSSL 握手 ETL。
- `capture_lab/python_tls.txt`：带十六进制载荷的文本。
- `capture_lab/tls_probe.py`：只做 TLS 连接和 GET 的探测脚本。

抓包显示 Python ClientHello 的关键扩展序列为：

```text
SNI / ec_point_formats / supported_groups / session_ticket /
encrypt_then_mac / extended_master_secret / signature_algorithms /
supported_versions / psk_key_exchange_modes / key_share / padding
```

## 现在还缺什么

1. 需要一个干净直连出口或独立 VM，排除 Clash TUN 和当前出口 IP 的影响。
2. 需要在授权环境中让官方客户端真实完成 bootstrap，才能拿到服务端下发的
   `rk`；合成 `rk` 只能跑本地状态机。
3. 如果官方客户端仍失败，再对照真实进程的 ClientHello、证书链、HTTP/2/1.1
   协商和请求时序；不要继续对 `/xb/iil` 做加头/改信封的盲试。

## 安全边界

- 不启动原始 `运营猫.exe`。
- 不重放生产业务请求，不伪造真实授权。
- 不把合成 fixture 当成真实 `rk` 或业务数据。
