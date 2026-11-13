# 订单、激活与条目同步

## 订单任务

UI 任务模块具有相同的结构：

```text
QRunnable
  -> asyncio.run(inner)
  -> build JSON with _sq_bao
  -> _sq_req request helper
  -> callback / Qt signal
```

模块：

- `fea/_cj_dd_file.py`：创建订单任务，以及成功/失败信号。
- `fea/_jc_dd_cz_file.py`：检查订单并充值任务，
  `cmd_check_order_stats`。
- `fea/_qy_hy_file.py`：迁移任务，`cmd_migrate_code_stats`。
- `fea/_zz_jh_ty_file.py`：激活码任务，
  `cmd_activate_code_stats`。

`fea/_sq_bao.py` 是 JSON 请求体构建器的字段名权威来源。关键值包括
`uCode`、`item_b64`、`item_encoding`、`item_hash`、`cfg_ver`、
订单/充值字段以及迁移标志。

## 条目脏数据生成契约

远端条目同步不得清除较新的本地编辑。重建后的契约如下：

```text
generation = ItemMemStore.get_dirty_generation()
snapshot   = ItemMemStore.dump_snapshot_gzip_b64()
send(snapshot)
if response_ok:
    ItemMemStore.clear_item_dirty_if_generation(generation)
```

`ItemMemStore.bootstrap_item_memory(is_register, cloud_empty,
cloud_encoding, cloud_payload_b64)` 协调以下情况：

- 存在云端快照 -> 应用该快照；
- 云端为空 + 存在本地快照 -> 本地命中；
- 两者都不存在 -> 空快照（注册时标记为脏）。

云端 payload 解码器接受 base64(gzip(JSON))，本地读取器为了诊断也兼容
纯 JSON。

## 重试与终态策略

`RemoteHb.terminal` 是唯一的终态信号。非终态失败使用模块特定的重试预算
（`_SPI_BIZ_RETRY`、`_SPUI_BIZ_RETRY`、`_UI_BIZ_RETRY`、
`_ROI_BIZ_RETRY`、`_CA_BIZ_RETRY`）。`_sq_r_qi` 和
`_sq_r_ks` 使用 `_sq_r_req._R_RETRY_DELAY_SEC` 进行退避。
