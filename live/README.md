# live/ 现场明文交接

其他机器直接用这个目录。按用户要求提交**全部明文**（含 `rk` / static key / PEM / catalog）。

## 先看

- `CATALOG_PLAIN.md`：origin、path、三把公钥角色
- `catalog_named_plain.json`：21 条 catalog 明文（含 PEM 正文）
- `catalog_urls.json`：拼好的 URL
- `SANDBOX_FIRST_RUN.md`：沙箱跑通过程
- `keys/rk.txt`：现场服务端下发的 Fernet `rk`（44 字符）
- `keys/static_key.txt`：`rk` 解开的 catalog static key
- `pems/_f_pk.pem`、`pems/_r_pk.pem`：业务请求/票据公钥
- `pems/pk_2.pem`：引导 `tw_sjk_pk_pem`（与 runtime 引导公钥相同）

## 用法

```text
origin = https://birder.jinsiqie.life
rk 先解 static key，再解 catalog 令牌（PE 里是套了一层 urlsafe-b64 的 Fernet）
请求信封：AES-CBC + RSA-PKCS1v15(_f_pk) -> {v1c,v2k}
响应验签：RSA-SHA256(_f_pk, response_bytes, sign)
```

离线脚本在 `recovery/offline_protocol_lab/`：`catalog_urls.py`、`envelope_offline.py`、`classify_live_pems.py`。不自动打生产。

## 不要做

不要在客户机点仅一次的体验。不要把分析工具装进沙箱 VM。
