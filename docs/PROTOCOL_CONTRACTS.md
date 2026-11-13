# 接口与关键代码契约

## 范围和边界

本文用于离线阅读、接口建模和恢复验证，不用于对真实服务端进行未授权请求。
所有字段来自恢复源码、Nuitka 常量、Hex-Rays 输出和离线测试；`{{SECRET_*}}`
是脱敏占位符。

不要把本文的合成 fixture 当作服务端真实响应。真实响应仍需要合法授权、服务端
签名和配置密钥。完整源码副本、测试和离线 lab 都在本交付目录中。

## 1. 通用传输契约

### 1.1 主机选择

`fea._sq_req` 的主机来源：

```text
get_host()
  -> 开发路径: TwCtx.tw_hq_by_k("_p_dh")
  -> 生产路径: TwCtx.tw_hq_by_k("_r_u")
```

`URL_PRE_COM()` 返回去掉尾部 `/` 的 host。恢复出的 bootstrap 端点是：

```text
https://birder.jinsiqie.life/xb/iil
```

`fea._sq_zw` 还对生产主机做证书指纹固定；指纹目录来自 `_sq_pz.YC_ZW_HC_LB`，
失败缓存 30 秒，成功缓存 300 秒。

### 1.2 旧版请求信封

`fea._sq_req` 使用：

```text
AES-CBC/PKCS7(JSON)
  -> IV || ciphertext
  -> RSA-PKCS1v15 包装 16 字节 AES key
  -> 请求体 {"v1c": ciphertext_hex, "v2k": wrapped_key_hex}
```

关键代码：

```python
def _json_payload(json_content: str, dy_aes_key: bytes) -> dict:
    encrypted_data = sq_sc_aq_nr(json_content, dy_aes_key)
    encrypted_aes_key = sq_sc_aes_k(dy_aes_key)
    return {
        "v1c": encrypted_data.hex(),
        "v2k": encrypted_aes_key.hex(),
    }
```

响应体：

```text
{"response": "<ciphertext_hex>", "sign": "<rsa_signature_hex>"}
```

客户端先验证 RSA-SHA256 签名，再切前 16 字节作为 IV，用本次 AES key 解密 JSON。

```python
def sq_jm_xy(source: str, dy_aes_key: bytes):
    try:
        oj = json.loads(source) if isinstance(source, str) else source
        if not isinstance(oj, dict):
            return False, None, b""
        response = oj.get("response", "")
        sign = oj.get("sign", "")
        response_bytes = bytes.fromhex(str(response))
        sign_bytes = bytes.fromhex(str(sign))
        public_key = _my_gk.jm_jz_gy_pk()
        legal_message = _my_util.jm_yq_qm(
            public_key,
            response_bytes,
            sign_bytes,
        )
        if not legal_message:
            return False, None, b""
        iv_received = response_bytes[:16]
        ciphertext_received = response_bytes[16:]
        content_json = _my_util.aes_decrypt(
            iv_received + ciphertext_received,
            dy_aes_key,
        )
        return True, json.loads(content_json), sign_bytes
    except Exception as exc:
        print(sec("wl_feifa_03"), exc)
        return False, None, b""
```

### 1.3 授权引导传输

`link._sjk_cli.SjkCli` 是另一条 bootstrap 路径，但密码学原语相同：

- 请求体由 `_sjk_bao.sjk_zz_hb(version, exe_hash)` 生成。
- `_sjk_db_qq()` 生成一次性 16 字节 AES key，AES-CBC 加密 JSON，再用 RSA
  PKCS1v15 包装 key。
- 响应外层至少包含 `isSuccess`；成功数据在 `data.response` / `data.sign`。
- 内层解密后可能包含 `rk`，供 `TwCtx.tw_yy_mk(root_key)` 使用。

已知契约风险：恢复出的 `_sjk_jb_xy()` 调用
`jm_yq_qm(response_bytes, sign_bytes)` 只有两个参数，而
`_my_util.jm_yq_qm(public_key, message, signature)` 需要三个参数。该路径在
真实服务端使用前必须重新核对。

## 2. Endpoint 矩阵

### 2.1 旧版授权/订单接口

所有路径都以 `URL_PRE_COM()` 为前缀。

| 方法 | 路径 | 客户端函数 | 请求构建器 | 请求字段 | 主要消费者 |
| --- | --- | --- | --- | --- | --- |
| POST | `/jym` | `sq_jy_ma` | `zq_jy_hb` | `uCode`, `payload` | 登录结果 |
| POST | `/zc` | `sq_zc` | `zq_zc_hb` | `pre`, `fake` | 注册结果 |
| POST | `/pz` | `sq_lq_pz` | `zq_pz_hb` | 原样 JSON | 配置/授权数据 |
| POST | `/qy` | `sq_qy_dm` | `gen_migrate_code_content` | `code_from`, `code_to`, `cover_expri`, `force_cover_yun`, `payload` | 迁移结果 |
| POST | `/cz` | `get_create_order` | `gen_create_order_content` | `order`（当前恢复体使用 `repr(item)`，推断） | 创建订单 |
| POST | `/cz` | `get_check_order_recharge` | `gen_check_order_content` | 原样 JSON | 检查订单/充值 |
| POST | `/cz` | `sq_cz_jqm` | `zq_cz_hb` | `reset`, `payload` | 重置卡密 |
| POST | `/sb` | `sq_sb` | 直接 `json.dumps` | `uCode` | 上报/状态 |
| POST | `/activate` | `sq_ty_jh` | 直接 `json.dumps` | `uCode` | 激活码 |
| POST | `/yp/ch` | `sq_yp_pd_ch` | `zq_yp_ch_hb` | `uCode`, `parse_payload` | 频道/消息解析 |
| POST | `/yp/cm` | `sq_yp_pd_cm` | `zq_yp_cm_hb` | `parse_payload` JSON | 评论解析 |

`/cz` 同时承载创建订单、检查充值、重置卡密三种 scene，不能只按路径区分；
调用方必须结合 `scene` 和请求体判断。

### 2.2 远端报告/心跳接口

| 方法 | 路径 | 客户端函数 | 请求体 | 下游行为 |
| --- | --- | --- | --- | --- |
| POST | `/r` | `sq_r_raw_post` | 调用方 JSON | 通用原始请求 |
| POST | `/r_spi` | `sq_r_spi` | item 请求体 | 启动/周期心跳 |
| POST | `/r_spui` | `sq_r_spui` | item 请求体 | 周期 UI 上报，成功可清 dirty |
| POST | `/r_ui` | `sq_r_ui` | item 请求体 | 应用远端账号状态 |
| POST | `/r_roi` | `sq_r_roi` | item 请求体 | ROI 报告，可能带 `itemUpdated` |
| POST | `/r_ca` | `sq_r_ca` | 转换批次 | 返回执行票据/顺序 |

`_sq_r_req` 的超时/重试：

```text
_R_HTTP_TIMEOUT = 45
_R_MAX_RETRY = 3
_R_RETRY_DELAY_SEC = 1.5
```

业务重试预算：

```text
_SPI_BIZ_RETRY = 4
_SPUI_BIZ_RETRY = 3
_UI_BIZ_RETRY = 3
_ROI_BIZ_RETRY = 4
_CA_BIZ_RETRY = 4
```

## 3. 请求体构建器

### 3.1 旧版 `_sq_bao`

```python
def gen_migrate_code_content(
    code_from: str,
    code_to: str,
    cover_expri: bool,
    force_cover_yun: bool,
    json_content: str,
) -> str:
    return _json(
        {
            "code_from": code_from,
            "code_to": code_to,
            "cover_expri": cover_expri,
            "force_cover_yun": force_cover_yun,
            "payload": json_content,
        }
    )


def zq_cz_hb(reset: str, json_content: str) -> str:
    return _json({"reset": reset, "payload": json_content})


def zq_jy_hb(uCode: str, json_content: str) -> str:
    return _json({"uCode": uCode, "payload": json_content})


def zq_pz_hb(json_content: str) -> str:
    return json_content


def zq_yp_ch_hb(u_code: str, parse_payload: dict) -> str:
    return _json({"uCode": u_code, "parse_payload": parse_payload})


def zq_yp_cm_hb(json_content: str) -> str:
    return json_content


def zq_zc_hb(pre: str, fake: str) -> str:
    return _json({"pre": pre, "fake": fake})
```

`gen_create_order_content()` 当前恢复体是：

```python
def gen_create_order_content(*args, **kwargs) -> str:
    return _json({"order": [repr(item) for item in args]})
```

这里使用 `repr(item)`，只能作为行为级线索，不能当作真实线上字段 schema。

### 3.2 `r_spi` / `r_ca` 构建器

```python
def zq_r_item_hb(
    uCode: str,
    item_b64: str = "",
    include_item: bool = False,
    cfg_ver: int = 0,
    iid: str = "",
    b64: str | None = None,
    enc: str | None = None,
    ih: str | None = None,
) -> str:
    item_hash = ih or hash_item_b64(item_b64)
    payload = {
        "uCode": uCode,
        "instance_id": iid,
        "cfg_ver": cfg_ver,
        "item_hash": item_hash,
    }
    if include_item:
        payload["item_b64"] = b64 or item_b64
        payload["item_encoding"] = enc or "base64"
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def zq_r_convert_hb(uCode: str, mode: str, items: list) -> str:
    return json.dumps(
        {"uCode": uCode, "mode": mode, "items": items},
        ensure_ascii=False,
        separators=(",", ":"),
    )
```

空 `item_b64` 的 `item_hash` 是空字节串的 SHA-256：

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

### 3.3 bootstrap 请求体

```python
def sjk_zz_hb(version: str, exe_hash: str) -> str:
    user_id = _rand_en(5)
    email = f"john.doe{random.randint(1, 10)}@gail.com"
    details = {
        "name": _unit_name(),
        "contact": {
            "email": email,
            "phone": f"+1-202-555-{random.randint(10, 99)}",
        },
        "address": {
            "street": "742 Evergreen Terrace",
            "city": "Springfield",
            "random": random.randint(1, 100),
            "metadata": {
                "lat": 39.7817,
                "lon": -89.6501,
                "hash": "sha256:" + (exe_hash or "")[:50],
                "pre": version,
                "fake": _rand_en(5),
                "n": _rand_en(6),
                "h": _rand_en(6),
                "uc_ns": _unit_name(),
                "tags": ["residential", "verified"],
            },
        },
    }
    return json.dumps(
        {"userInfo": {"userId": user_id, "details": details}},
        ensure_ascii=False,
        separators=(",", ":"),
    )
```

### 3.4 启动心跳的调用顺序

```python
def _build_spi_body(ucode: str, item_b64: str = "", include_item: bool = False) -> str:
    try:
        return _sq_r_bao.zq_r_item_hb(
            ucode,
            item_b64=item_b64,
            include_item=include_item,
        )
    except TypeError:
        return _sq_r_bao.zq_r_item_hb(ucode, item_b64, include_item)
```

启动链的顺序是：

```text
qd_r_spi_boot
  -> _spi_fetch
     -> r_spi
     -> _coerce_remote_hb
     -> _apply_user_from_remote -> hy_jx_bc
  -> _bootstrap_item_memory
```

## 4. 响应字段

### 4.1 `SqJqm` 账号对象

```text
身份: ucode, status, grade, limit
时间: hours, startTime, endTime, remainingSec, expire
能力: hasExperi, experiDuration, botAbility, aiAbility, mul
服务: sendAtName, keFu, cloudBot, maoContacts, priceConfig, modelList, apiKey
```

`hy_jx_bc()` 要求输入是带顶层 `data` 的 envelope：

```python
def hy_jx_bc(oj: dict) -> SqJqm:
    data = oj["data"]
    info = SqJqm(
        ucode=data["ucode"],
        status=data["status"],
        grade=data["grade"],
        ...
        mul=data["mul"],
    )
    _sq_jqm.current_account_info = info
    _sq_jqm.current_account_time = time.time()
    return info
```

`parse_report()` 对 `status in (0, 1)` 返回 `None`；其他状态交给
`hy_jx_bc()`。这两个状态和业务含义仍需补证。

### 4.2 `RemoteHb`

```text
terminal: bool   # true 表示不要重试
msg: str         # 传输/业务错误
data: Any        # 解码后的业务数据
```

`success`、`failed_retry`、`failed_terminal` 是重试策略的边界。

### 4.3 item 快照

```json
{
  "scheduler": null,
  "autoMap": {},
  "globalAdWrapper": {
    "adEnable": false,
    "adIsBottomUp": false,
    "delete": false,
    "ades": []
  },
  "water": null
}
```

云端传输为 `base64(gzip(JSON))`。本地脏代际流程：

```text
generation = ItemMemStore.get_dirty_generation()
snapshot = ItemMemStore.dump_snapshot_gzip_b64()
send(snapshot)
if response_ok:
    ItemMemStore.clear_item_dirty_if_generation(generation)
```

### 4.4 转换批次

请求：

```json
{"uCode": "LAB-UCODE", "mode": "convert", "items": [{"kid": "kid-1"}]}
```

期望响应形状：

```json
{
  "data": [
    {
      "kid": "kid-1",
      "auto_type": 2,
      "af": "af-1",
      "ticket": {
        "ver": 2,
        "batch_id": "batch-1",
        "etid": "etid-1",
        "sn": "sn-1",
        "af": "af-1",
        "uc_hash": "sha256(ucode)",
        "mode": "timing",
        "iat": 1,
        "exp": 9999999999,
        "sign_item": "hex"
      }
    }
  ],
  "sign_batch": "hex"
}
```

恢复出的 `convert_batch_with_retry()` 会把返回条目中的 `kid` 转成 `bytes`，
并补上 `sign_batch`。下游若按字符串处理 `kid` 会出错。

## 5. 票据校验关键代码

### 5.1 `AutoBeanXXX.parse_wire`

```text
检查 batch_id / exp / server_nonce / sign_batch / entries
  -> _verify_sign_batch(...)
  -> 逐条 _ticket_from_wire / _exec_from_wire
  -> compute_af(exec_obj) == ticket.af
  -> _verify_sign_item(sign_kid, auto_type, ticket)
  -> ensure_valid(ucode)
  -> gy_wc_hx(xxx, ucode)
```

`ensure_valid()` 的关键判断：

```python
def ensure_valid(self, ucode: str) -> bool:
    ticket = self.ticket
    if ticket is None:
        return False
    raw_kid = str(self.kid or "")
    if not raw_kid or not ucode:
        return False
    now = int(time.time())
    uc_hash = hashlib.sha256(str(ucode).encode("utf-8")).hexdigest().lower()
    exp = int(getattr(ticket, "exp", 0) or 0)
    if exp and now > exp:
        return False
    bound_hash = str(getattr(ticket, "uc_hash", "") or "").lower()
    if bound_hash and bound_hash != uc_hash:
        return False
    exec_kid = str(getattr(self.exec_obj, "kid", "") or "")
    if exec_kid and exec_kid != raw_kid:
        return False
    if not _verify_sign_item(raw_kid, self.auto_type, ticket):
        return False
    return True
```

### 5.2 HMAC A/B/C

```python
def _gy_ma(ticket, kid, auto_type):
    return f"A|{ticket.batch_id}|{kid}|{int(auto_type)}|{ticket.exp}".encode()

def _gy_mb(ticket, kid, ucode):
    uc_hash = hashlib.sha256(str(ucode or "").encode()).hexdigest()
    sign_item = str(getattr(ticket, "sign_item", "") or "")
    return f"B|{sign_item[:32]}|{ticket.uc_hash}|{uc_hash}|{kid}|{ticket.mode}".encode()

def _gy_mc(ticket, kid, auto_type):
    return f"C|{ticket.etid}|{ticket.sn}|{ticket.af}|{kid}|{int(auto_type)}".encode()

def gy_wc_hx(xxx, ucode):
    ha = _gy_da(xxx.ticket, xxx.kid, xxx.auto_type)
    hb = _gy_db(xxx.ticket, xxx.kid, ucode)
    hc = _gy_dc(xxx.ticket, xxx.kid, xxx.auto_type)
    xxx._g0 = ha[:12] + hb[:12]
    xxx._g1 = hb[12:24] + hc[:12]
    xxx._gx = int(xxx.ticket.exp or 0)
```

## 6. 服务端必须返回的最小集合

| 链路 | 必须返回 | 用途 |
| --- | --- | --- |
| bootstrap | `isSuccess`、`data.response`、`data.sign`、内层 `rk` | 解配置目录/建立 root key |
| `r_spi` | `isSuccess/success`、`is_register`、`item`、账号 `data` | 启动账号和条目 |
| `r_spui` | 成功状态、可选 item/report | 周期同步与 dirty 清理 |
| `r_ui` | 账号 `data` | 应用远端能力变更 |
| `r_roi` | `isSuccess`、`itemUpdated`、报告 | ROI 同步 |
| `r_ca` | ordered items、`sign_batch`、ticket 字段 | 生成可执行票据 |
| `/jym`、`/zc` | 登录/注册结果、账号数据 | 启动入口 |
| `/cz`、`/activate`、`/qy` | 订单/激活/迁移状态 | 授权和付费流程 |
| `_f_pk` / `_r_pk` | PEM 公钥 | 请求/响应和票据验签 |

如果服务端不提供账号能力字段，`SqJqm` 默认为游客/无 AI/无 bot/无多开：
`grade=0`、`hasExperi=0`、`aiAbility=0`、`botAbility=0`、`mul=False`、
`apiKey=""`、`modelList="[]"`。这会让对应的 UI/worker 分支不启用。

## 7. 已知契约问题

1. `_apply_user_from_remote()` 先把外层 `data` 解包，再调用 `hy_jx_bc()`；
   但 `hy_jx_bc()` 又要求 `oj["data"]`，会触发 `KeyError: 'data'`。
   离线 lab 已记录该问题。
2. `qd_r_spi_boot()` 直接调用异步 `_spi_fetch()` 而没有 `await`，心跳结果不会
   进入正常账号解析。离线 lab 用同步 stub 绕过以验证下游。
3. `_sjk_cli._sjk_jb_xy()` 的 `jm_yq_qm` 调用参数数量与恢复出的
   `_my_util.jm_yq_qm(public_key, message, signature)` 不一致，需重点核对。
4. `TwCtx._ENCRYPTED_STATIC_KEY` 在当前恢复树中是占位符，配置目录会
   fail-closed；真实环境必须补层密钥或由合法 bootstrap 提供 root key。
5. `gen_create_order_content()` 使用 `repr(item)`，属于行为级重建，不足以
   证明真实订单字段。

## 8. 离线验证建议

1. 先阅读 `offline_protocol_lab/findings.md`。
2. 运行 `offline_protocol_lab/run_lab.py`，确认 `r_spi`/`r_ca` 的请求字段和
   下游状态变化。
3. 在 `recovered_src` 下运行 `python -m pytest -q`，保持 455 个离线用例。
4. 不要用真实账号或真实服务端做猜测性请求；先用合成 fixture 补字段 schema
   和负向用例。

## 9. 关键文件索引

| 文件 | 用途 |
| --- | --- |
| `recovered_src/src/py/com/yun/mao/fea/_sq_req.py` | 旧版信封、endpoint、重试 |
| `recovered_src/src/py/com/yun/mao/fea/_sq_r_req.py` | `r_spi`/`r_ui`/`r_roi`/`r_ca` |
| `recovered_src/src/py/com/yun/mao/fea/_sq_r_qi.py` | 心跳、账号应用、item bootstrap |
| `recovered_src/src/py/com/yun/mao/fea/_sq_r_ca.py` | 转换批次和票据返回处理 |
| `recovered_src/src/py/com/yun/mao/fea/_sq_bao.py` | 旧版请求体构建 |
| `recovered_src/src/py/com/yun/mao/fea/_sq_r_bao.py` | item/convert 请求体 |
| `recovered_src/src/py/com/yun/mao/link/_sjk_cli.py` | bootstrap 请求/响应 |
| `recovered_src/src/py/com/yun/mao/link/_sjk_bao.py` | bootstrap 请求体 |
| `recovered_src/src/py/com/yun/mao/link/_tw_ctx.py` | 配置/密钥目录 |
| `recovered_src/src/py/com/yun/mao/dclass/AutoBeanXXX.py` | ticket/wire/签名/ensure_valid |
| `recovered_src/src/py/com/yun/mao/link/_lk_gy_w.py` | HMAC A/B/C 和分片 |
| `recovered_src/src/py/com/yun/mao/fea/_sq_chk.py` | `parse_report` / `hy_jx_bc` |
