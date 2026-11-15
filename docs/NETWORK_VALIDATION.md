# 本机连接验证与抓包结论

## 结论

本机可以做 bootstrap 域名的连接验证和 TLS 握手抓包，但当前网络不是干净直连：

- 默认路由被 Clash Verge 的 `Meta` TUN 接管。
- WinINET 代理为 `127.0.0.1:7897`。
- 使用物理以太网源地址绕过 TUN 的测试超时。
- 因此当前请求看到的服务端判定，可能同时受代理出口、TLS 指纹和链路影响。

本机没有启动原始 PE，也没有重放生产 `v1c/v2k`。

## 链路结果

```text
目标: https://birder.jinsiqie.life:443
TCP 443: open
TLS: Cloudflare
HTTP: 1.1
GET /xb/iil -> 405 Method Not Allowed
Allow: POST
alt-svc: h3=":443"
```

GET 的 405 只能说明路径可达且只接受 POST，不能用来判断授权结果。

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

目标自带 Python 3.11 + OpenSSL 3.0.13；本机 Python 3.13/OpenSSL 3.0.18 只能
做近似对照，不能替代官方进程的 ClientHello。

## 抓包能力

本机 `pktmon` 可用，已成功落 ETL 并转换成带十六进制载荷的文本。抓包能覆盖
TCP SYN、TLS ClientHello/ServerHello 和 HTTP 响应头；TLS 应用数据不可直接
解密。

详细抓包文件和脚本保留在本地 `capture_lab/`，未提交 public 仓库。

## 下一步

1. 用干净直连出口或独立 VM 做对照，排除 Clash TUN 和代理出口。
2. 在授权环境中让官方客户端真实完成 bootstrap，确认 `rk` 下发。
3. 如果官方客户端仍失败，再对照真实进程的 ClientHello、证书链、HTTP 协商和
   请求时序。
4. 不要继续对 `/xb/iil` 做加头/改信封的盲试；合成 `rk` 不代表真实业务配置
   已解密。
5. 沙箱只验收 contacted，路径拆分见 `docs/SANDBOX_PATHS.md`；不要把沙箱 JA3 并进本文件的指纹线。
