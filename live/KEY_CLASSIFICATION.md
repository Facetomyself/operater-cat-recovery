# 现场公钥分类

来源：官方 PE 成功引导后的客户机 RAM。PEM 正文只在 `capture_lab/pems/`，不进对话、不进 public 仓。

## 结论

两把互异的 RSA-2048：

- `bootstrap_init`：与 `_re/runtime_secrets.txt` 的 `tw_sjk_pk_pem` 相同，用于 `/xb/iil` 引导信封。
- `catalog_candidate`：另一把，候选 `_f_pk` 或 `_r_pk`。内存里没有第二业务主机，`_r_u` 按 birder 使用。

分类脚本：`offline_protocol_lab/classify_live_pems.py`（离线、不联网）。

## 下一步

用 `catalog_candidate` 在离线 lab 验签合成/已抓到的 `sign` 字段。没有内层明文 `sign` 之前，不能声称已打通业务验签。不打生产，不点体验。
