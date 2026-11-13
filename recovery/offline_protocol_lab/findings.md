# 离线协议实验结果

## 运行信息

```text
脚本：offline_protocol_lab/run_lab.py
输入：offline_protocol_lab/fixtures/synthetic_responses.json
输出：offline_protocol_lab/run-output.json
网络：socket.create_connection 和 aiohttp.ClientSession 均替换为抛错 stub
目标程序：未启动
真实账号/真实卡密：未使用
```

本次运行返回 `bootstrap.result = true`，心跳合成账号写入成功，转换批次返回
一条合成票据。

## 已验证的字段流

### 1. 授权引导

`SjkCli.sjk_lq_qd()` 进入 `_sjk_post_once` 时携带：

- `url = https://lab.invalid/xb/iil`
- `public_key = LAB-PUBLIC-KEY-NOT-REAL`
- `version = 9.6.3`
- `exe_hash = 101db38faad3ba89f99a69ee3be2f45334332520a2a813a5e69caaa2d3d68ae0`
- `ssl_verify = False`

合成响应 `{"isSuccess": true, "rk": "LAB-ROOT-KEY-NOT-REAL"}` 使客户端返回
`True`。本次 stub 只验证分支；真实请求体还应由 `sjk_zz_hb()` 生成。

### 2. `r_spi` 心跳

`s_b_i_kaishi()` 的心跳请求体字段为：

```json
{
  "uCode": "LAB-UCODE",
  "instance_id": "",
  "cfg_ver": 0,
  "item_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

`item_hash` 在空条目时是空字节串的 SHA-256。合成心跳响应的顶层结构需要同时
包含 `item` / `is_register` 和 `data`：

```json
{
  "isSuccess": true,
  "is_register": false,
  "item": {"encoding": "gzip", "payloadB64": ""},
  "data": {"ucode": "LAB-UCODE", "...": "SqJqm fields"}
}
```

`hy_jx_bc()` 接受内层 `data` 后会把 `grade`、`expire`、`hasExperi`、
`aiAbility`、`botAbility`、`apiKey`、`modelList`、`cloudBot`、`priceConfig`、
`remainingSec` 和 `mul` 全部写进 `current_account_info`。

### 3. 条目 bootstrap

空 `item` 进入 `_bootstrap_item_memory()` 后记录的参数为：

```text
is_register=false
cloud_empty=true
cloud_encoding=gzip
cloud_payload_b64=""
```

本地 `LoadDataClass.getAutoMap()` 被 stub 为两个条目，日志显示
`branch=login autoCount=2`。说明云端为空时，下游仍会读取本地条目快照。

### 4. 心跳后的登录路径

`s_b_i_kaishi()` 在心跳完成后仍调用 `sq_jy_ma()`，本次记录到：

```text
login_ucodes = ["LAB-UCODE"]
startup_result = True
```

这意味着：**心跳不是启动终点**，登录/注册仍是独立的远程步骤。

### 5. `r_ca` 转换批次

请求体为：

```json
{
  "uCode": "LAB-UCODE",
  "mode": "convert",
  "items": [{"kid": "kid-lab-1", "source": "lab"}]
}
```

合成响应返回一条 `ticket` 和 `sign_batch`。`convert_batch_with_retry()` 的
返回值中 `kid` 被转成 `bytes`（输出记录为十六进制
`6b69642d6c61622d31`），同时补上 `sign_batch`。下游不能假设 `kid` 始终是
字符串。

## 已发现的恢复树契约问题

### `_apply_user_from_remote()` 与 `hy_jx_bc()` 的入参不一致

恢复体中的调用顺序是：

```text
_apply_user_from_remote(outer)
  -> outer["data"] 解包出 inner
  -> hy_jx_bc(inner)
```

但 `hy_jx_bc()` 第一行是：

```python
data = oj["data"]
```

直接把内层账户字典传进去会抛 `KeyError: 'data'`。本次实验室记录到了这个异常。
为了继续观察下游，`run_lab.py` 增加了仅限实验室的 `hy_jx_bc` shim：
入参没有 `data` 时自动包一层 `{"data": ...}`。该 shim 不修改恢复源码。

### `qd_r_spi_boot()` 调用异步函数未 `await`

`_sq_r_qi._spi_fetch()` 是 `async def`，但 `qd_r_spi_boot()` 直接执行：

```python
last_hb = _spi_fetch(ucode)
```

这样拿到的是 coroutine，不是 `RemoteHb`，后续 `last_hb.data` 不会进入账号解析。
本次实验把 `_spi_fetch()` 替换成同步 stub，绕过了这个恢复缺陷，以便验证
`hy_jx_bc` 和 bootstrap 的下游行为。

## 结论

- 合成响应足以摸清请求字段、响应分支和状态更新顺序。
- 不能据此生成真实可用响应：`r_spi` / `r_ca` 的真实数据仍需服务端签名和配置密钥。
- 去卡密后，心跳、登录、云端条目和转换票据仍是独立的远程依赖。
- 本次实验只写入 `offline_protocol_lab/`，没有修改 `recovered_src/src`、
  `recovered_src/tests` 或 `MANIFEST.json`。
