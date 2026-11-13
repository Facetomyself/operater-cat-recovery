# 卡密与授权链路分析

## 范围与安全声明

本文归档 `operater-cat` 的本地卡密、授权文件、授权请求信封和执行票据校验链路，目的只有两个：

- 为静态逆向、源码还原和回归测试保留可审计证据。
- 为离线恢复树提供可解释的卡密门禁实现，便于后续无害化处理。

本文不提供绕过远端授权、伪造服务器响应或生成有效卡密的步骤。不要运行原始
`运营猫.exe`、`static_hybrid*.exe` 或任何恢复出来的入口点。所有结论来自现有源码、
反编译 C 伪代码、常量表和离线测试，不包含动态注入或联网验证。

文档中的 `{{SECRET_*}}` 是脱敏占位符，必须原样保留。

## 模块地图

| 层次 | 模块 | 作用 |
| --- | --- | --- |
| 本地授权文件 | `fea._sq_jqm` | 读写 `.code` / `.code.old`，维护 `SqJqm` 账户对象 |
| 授权响应解析 | `fea._sq_chk` | 解析远端报告，构造 `SqJqm` |
| 授权请求传输 | `fea._sq_req`、`link._sjk_cli` | AES-CBC + RSA 信封、签名验证、重试 |
| 配置与密钥上下文 | `link._tw_ctx` | Fernet 静态密钥、RSA 公钥、加密配置目录 |
| 执行票据绑定 | `link._lk_gy_w` | HMAC A/B/C 三段载荷和 `_g0` / `_g1` 分片 |
| 只读校验入口 | `link._lk_gy_r` | `gy_jc_b1` 轻量校验 |
| 票据对象 | `dclass.AutoBeanXXX` | wire 反序列化、`ensure_valid`、执行对象绑定 |
| 主机与证书固定 | `fea._sq_zw` | 生产主机选择、证书指纹校验、失败缓存 |

## 端到端流程

1. 启动阶段，`link._sjk_cli.SjkCli.sjk_lq_qd()` 从 `TwCtx` 取出授权服务 URL
   和 RSA 公钥，并计算当前程序版本和可执行文件 SHA-256。
2. `SjkCli._sjk_db_qq()` 生成一次性 16 字节 AES key，使用
   AES-CBC-PKCS7 加密 `sjk_zz_hb(version, exe_hash)`，再用 RSA PKCS1v15
   包装 AES key，形成 `{"v1c": ..., "v2k": ...}`。
3. 服务器返回 `isSuccess`、`data.response` 和 `data.sign`。客户端用 RSA 公钥
   验证签名，拆分 `IV || ciphertext`，再用本次 AES key 解出授权 JSON。
4. 授权引导成功后，`TwCtx.tw_yy_mk(root_key)` 保存服务器下发的 root key；
   `TwCtx.tw_hq_by_k(name)` 才能解开配置目录中的主机、公钥和接口常量。
5. 本地 `.code` 文件由 `fea._sq_jqm._zh_rd_code()` 用 Fernet 解密，读取
   `ucode` 和可选的 `muli`；没有 `.code` 时尝试把旧 `.code.old` 迁移过来。
6. 远端报告由 `fea._sq_chk.parse_report()` 分发，状态不是 `0` / `1` 时调用
   `hy_jx_bc()` 构造新的 `SqJqm`，并写入模块级 `current_account_info`。
7. 执行票据批次由 `AutoBeanXXX.parse_wire()` 重建。每个条目依次校验
   batch 签名、`compute_af(exec_obj)` 与 ticket `af`、
   `_verify_sign_item(kid, auto_type, ticket)` 和 `ensure_valid(ucode)`。
8. `link._lk_gy_w.gy_wc_hx()` 把 A/B/C 三段 HMAC 切成 `_g0` / `_g1` 分片并
   写入 `_gx` 过期时间；后续 `gy_jc_a1..a9`、`gy_jc_b1` 和
   `AutoBeanXXX.ensure_valid()` 组成实际门禁。

## 本地授权文件

固定路径：

```text
%APPDATA%/Microsofteis/lang/union_code_release/union_code/.code
%APPDATA%/Microsofteis/lang/union_code_release/union_code/.code.old
```

当前 `.code` 的明文结构只有两个字段：

```json
{"ucode": "<machine-code>", "muli": 0}
```

`muli` 是布尔语义，写入时使用 `CARD_GEEK` 常量；`zh_jz_xx()` 负责把读到
`ucode` / `mul` 同步到 `current_account_info`。`_zh_rd_code()` 本身只返回
`(ucode, bool(muli))`，不直接修改账户对象。

### 归档代码：读取与写入本地授权

```python
def _zh_rd_code(path: Path | None = None):
    code_path = Path(path) if path is not None else zh_code_pth()
    if not code_path.exists():
        return "", False
    try:
        raw = code_path.read_bytes()
        dic = json.loads(_static_cipher().decrypt(raw).decode("utf-8"))
        ucode = str(dic.get("ucode", "") or "")
        mul = bool(dic.get("muli", False)) if "muli" in dic else False
        return ucode, mul
    except Exception as exc:
        print(_sec("jqm_sh_01"), exc)
        return "", False


def _zh_bc_uc(ucode: str, mul: bool = False) -> None:
    try:
        muli = CARD_GEEK if mul else 0
        payload = json.dumps(
            {"ucode": str(ucode or ""), "muli": muli},
            ensure_ascii=False,
        ).encode("utf-8")
        encrypted = _static_cipher().encrypt(payload)
        code_path = zh_code_pth()
        code_path.parent.mkdir(parents=True, exist_ok=True)
        code_path.write_bytes(encrypted)
    except Exception as exc:
        print(_sec("jqm_sh_01"), exc)


def _read_ucode_from_legacy_bean() -> str:
    path = zh_old_pth()
    if not path.exists():
        return ""
    try:
        raw = path.read_bytes()
        plain = _static_cipher().decrypt(raw).decode("utf-8")
        obj = json.loads(plain)
        ucode = str(obj.get("ucode", "") or "")
        mul = bool(obj.get("muli", False))
        current_account_info.ucode = ucode
        current_account_info.mul = mul
        return ucode
    except Exception as exc:
        print(_sec("jqm_sh_02"), exc)
        return ""


def _migrate_legacy_bean_if_needed() -> None:
    try:
        ucode = _read_ucode_from_legacy_bean()
        code_exists = zh_code_pth().exists()
        legacy_exists = zh_old_pth().exists()
        if ucode and not code_exists and legacy_exists:
            _zh_bc_uc(ucode, current_account_info.mul)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(_sec("jqm_load_tpl_15").format(now=now))
    except Exception as exc:
        try:
            from ..util import TracePrinterHelper

            TracePrinterHelper.print_trace(_sec("jqm_sh_03"), exc)
        except Exception:
            print(_sec("jqm_sh_03"), exc)


def zh_jz_xx() -> None:
    _migrate_legacy_bean_if_needed()
    ucode, mul = _zh_rd_code()
    if ucode:
        current_account_info.ucode = ucode
        current_account_info.mul = mul
    return None


def zh_sc_wj() -> None:
    _zh_bc_uc(current_account_info.ucode, current_account_info.mul)
```

## 授权请求信封

`fea._sq_req` 保留旧版传输路径，`link._sjk_cli` 保留授权引导路径。两者使用同一组
密码学原语：

- `v1c`：`IV || AES-CBC-PKCS7(JSON)` 的十六进制。
- `v2k`：一次性 AES key 的 RSA PKCS1v15 密文十六进制。
- `response` / `sign`：服务器响应的密文和 RSA 签名。

请求侧关键代码：

```python
def _json_payload(json_content: str, dy_aes_key: bytes) -> dict:
    encrypted_data = sq_sc_aq_nr(json_content, dy_aes_key)
    encrypted_aes_key = sq_sc_aes_k(dy_aes_key)
    return {
        "v1c": encrypted_data.hex(),
        "v2k": encrypted_aes_key.hex(),
    }


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
            try:
                from ..link._fds_tan import wb_jm_yq

                wb_jm_yq()
            except Exception:
                pass
            return False, None, b""
        iv_received = response_bytes[:16]
        ciphertext_received = response_bytes[16:]
        content_json = _my_util.aes_decrypt(
            iv_received + ciphertext_received,
            dy_aes_key,
        )
        content_oj = json.loads(content_json)
        return True, content_oj, sign_bytes
    except Exception as exc:
        print(sec("wl_feifa_03"), exc)
        return False, None, b""
```

授权引导客户端还带有固定重试参数：

```text
_HTTP_TIMEOUT_SEC = 120
_BOOTSTRAP_CONNECT_TIMEOUT_SEC = 30
_BOOTSTRAP_MAX_RETRY = 4
_BOOTSTRAP_RETRY_BASE_DELAY_SEC = 1.5
_RETRYABLE_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}
```

## HMAC 票据绑定

`_lk_gy_w` 用 `TwCtx.tw_hq_by_k("_r_pk")` 作为配置密钥，先做
`SHA-256("pb_v3|" + key)` 得到本地 HMAC key。三段载荷分别覆盖批次、账号和
执行对象：

```text
A | batch_id | kid | auto_type | exp
B | sign_item[:32] | ticket.uc_hash | sha256(ucode) | kid | ticket.mode
C | etid | sn | af | kid | auto_type
```

### 归档代码：HMAC key 与三段载荷

```python
def _gy_k0() -> bytes:
    global _gy_kc
    if _gy_kc is None:
        from ._tw_ctx import TwCtx

        key = TwCtx.tw_hq_by_k("_r_pk")
        _gy_kc = hashlib.sha256(b"pb_v3|" + str(key).encode("utf-8")).digest()
    return _gy_kc


def _gy_ma(ticket: Any, kid: str, auto_type: int) -> bytes:
    text = f"A|{ticket.batch_id}|{kid}|{int(auto_type)}|{ticket.exp}"
    return text.encode("utf-8")


def _gy_mb(ticket: Any, kid: str, ucode: str) -> bytes:
    uc_hash = hashlib.sha256(str(ucode or "").encode("utf-8")).hexdigest()
    sign_item = str(getattr(ticket, "sign_item", "") or "")
    text = f"B|{sign_item[:32]}|{ticket.uc_hash}|{uc_hash}|{kid}|{ticket.mode}"
    return text.encode("utf-8")


def _gy_mc(ticket: Any, kid: str, auto_type: int) -> bytes:
    text = f"C|{ticket.etid}|{ticket.sn}|{ticket.af}|{kid}|{int(auto_type)}"
    return text.encode("utf-8")


def _gy_da(ticket: Any, kid: str, auto_type: int) -> bytes:
    return hmac.new(
        _gy_k0(), _gy_ma(ticket, kid, auto_type), hashlib.sha256
    ).digest()


def _gy_db(ticket: Any, kid: str, ucode: str) -> bytes:
    return hmac.new(
        _gy_k0(), _gy_mb(ticket, kid, ucode), hashlib.sha256
    ).digest()


def _gy_dc(ticket: Any, kid: str, auto_type: int) -> bytes:
    return hmac.new(
        _gy_k0(), _gy_mc(ticket, kid, auto_type), hashlib.sha256
    ).digest()
```

### 归档代码：分片绑定

```python
def gy_wc_hx(xxx: Any, ucode: str) -> None:
    if not ucode:
        return None
    uid = str(ucode).strip()
    ticket = xxx.ticket
    kid = str(getattr(xxx, "kid", "") or "").strip()
    auto_type = int(getattr(xxx, "auto_type", 0) or 0)
    ha = _gy_da(ticket, kid, auto_type)
    hb = _gy_db(ticket, kid, uid)
    hc = _gy_dc(ticket, kid, auto_type)
    xxx._g0 = ha[:12] + hb[:12]
    xxx._g1 = hb[12:24] + hc[:12]
    xxx._gx = int(getattr(ticket, "exp", 0) or 0)
    return None
```

分片布局：

```text
_g0 = HMAC_A[0:12] + HMAC_B[0:12]
_g1 = HMAC_B[12:24] + HMAC_C[0:12]
_gx = ticket.exp
```

### 归档代码：账号与票据一致性校验

```python
def _gy_sb(obj: Any, ucode: str) -> bool:
    if not ucode:
        return False
    try:
        ticket = obj.ticket
        kid = str(getattr(obj, "kid", "") or "").strip()
        expected = _gy_db(ticket, kid, str(ucode).strip())
        if obj._g0[12:24] != expected[:12]:
            return False
        if obj._g1[:12] != expected[12:24]:
            return False
        actual_uc_hash = hashlib.sha256(
            str(ucode).encode("utf-8")
        ).hexdigest()
        stored = getattr(ticket, "uc_hash", "")
        if not stored:
            return False
        return actual_uc_hash.lower() == str(stored).lower()
    except Exception:
        return False
```

## 校验门禁

`gy_jc_a1..a9` 不是九个独立算法，而是同一组原语的组合顺序。还原出的公共条件：

- `_gy_h0`：对象名为 `AutoBeanXXX`，`_g0` / `_g1` 均为 24 字节，且存在
  `ticket` 和 `exec`。
- `_gy_ex`：`_gx` 非零且 `time.time() < _gx`。
- `_gy_sa`：`_g0[0:12]` 与 A 段 HMAC 前 12 字节一致。
- `_gy_sb`：B 段 HMAC 的 24 字节分别落在 `_g0[12:24]` 和 `_g1[0:12]`，
  同时 `ticket.uc_hash` 必须等于当前 `ucode` 的 SHA-256。
- `_gy_sc`：`_g1[12:24]` 与 C 段 HMAC 前 12 字节一致。
- `_gy_af`：`compute_af(exec)` 与 `ticket.af` 一致。
- `_gy_rs`：调用 `AutoBeanXXX._verify_sign_item(kid, auto_type, ticket)`。

### 归档代码：最严格的组合门禁

```python
def gy_jc_a5(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj):
        return False
    ucode = _gy_uc()
    if not ucode:
        return False
    if not _gy_sb(obj, ucode):
        return False
    if not _gy_sa(obj):
        return False
    if not _gy_sc(obj):
        return False
    if not _gy_rs(obj):
        return False
    if not _gy_af(obj):
        return False
    return bool(obj.ensure_valid(ucode))
```

### 归档代码：只读校验入口

```python
def gy_jc_b1(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj):
        return False
    ucode = _gy_uc()
    if not ucode:
        return False
    if not _gy_sb(obj, ucode):
        return False
    hc = _gy_sc(obj)
    if not hc:
        return hc
    return _gy_af(obj)
```

## `AutoBeanXXX` 的 wire 校验

`parse_wire()` 从批次中取 `batch_id`、`exp`、`server_nonce`、`sign_batch` 和
`entries`，先验证整个 batch，再逐条构造 `ExecutionTicket` 和 `exec_obj`。
`ensure_valid()` 是最后一道对象级门禁：

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

`ensure_valid()` 只校验票据和当前账号的绑定关系。它不自行发起网络请求，也不
生成 `uc_hash`；`uc_hash` 必须来自服务器下发的 ticket。

## 授权响应解析

### 归档代码：报告分发与账户对象

```python
def parse_report(oj: dict) -> SqJqm | None:
    data = oj.get("data", {})
    status = int(data.get("status", 0))
    if status in (0, 1):
        return None
    return hy_jx_bc(oj)


def hy_jx_bc(oj: dict) -> SqJqm:
    data = oj["data"]
    info = SqJqm(
        ucode=data["ucode"],
        status=data["status"],
        grade=data["grade"],
        limit=data["limit"],
        descs=data["descs"],
        hours=data["hours"],
        startTime=data["startTime"],
        endTime=data["endTime"],
        expire=data["expire"],
        hasExperi=data["hasExperi"],
        sendAtName=data["sendAtName"],
        keFu=data["keFu"],
        cloudBot=data["cloudBot"],
        botAbility=data["botAbility"],
        aiAbility=data["aiAbility"],
        experiDuration=data["experiDuration"],
        openPremium=data["openPremium"],
        priceConfig=data["priceConfig"],
        maoContacts=data["maoContacts"],
        remainingSec=data["remainingSec"],
        apiKey=data["apiKey"],
        modelList=data["modelList"],
        mul=data["mul"],
    )
    _sq_jqm.current_account_info = info
    _sq_jqm.current_account_time = time.time()
    return info
```

`parse_report()` 的 `status in (0, 1)` 分支直接返回 `None`，这是运行时观察和
反编译结果一致的行为。需要账户对象时由调用方显式走 `hy_jx_bc()`。

## 主机与证书固定

`fea._sq_zw` 维护生产主机候选和证书指纹缓存：

- `zw_hq_zs(hostname)` 取 TLS 证书 DER，返回大写 SHA-256 指纹。
- `zw_bd_zs(hostname, fingerprint_list)` 规范化指纹后做集合匹配。
- `zw_bd_zw(origin)` 从 `TwCtx.tw_hq_by_k("_p_dh")` 取主机并校验。
- `_zw_hq_prod_host()` 成功缓存 300 秒，失败回退到
  `birder.jinsiqie.life` 并缓存 30 秒。
- `_xb_ms._sx_zw_hc` 会重置 `_sq_zw` 的证书 pin 缓存，避免旧主机结果长期滞留。

证书固定不是卡密算法本身的一部分，但它决定授权请求最终发往哪个主机，因此
静态分析时必须和 `TwCtx` 配置目录一起看。

## 实现分析

- `_sq_jqm` 和 `_sq_chk` 的账户字段是远端报告的直接映像，没有本地签名生成
  逻辑；本地只保存 `ucode` / `muli`。
- `TwCtx._ENCRYPTED_STATIC_KEY` 不是静态常量。它依赖服务器下发的 root key，
  离线环境没有 root key 时 `tw_jm_ok()` 返回 `False`，属于 fail-closed。
- `_lk_gy_w` 的三段 HMAC 把批次、账号、执行对象拆开校验，任何一段缺失都
  不能通过完整链；`gy_jc_a1..a9` 只是把同一组条件按不同强度组合。
- `AutoBeanXXX.parse_wire()` 同时校验 batch 签名、单条 item 签名、
  `compute_af` 指纹、`kid` 关联和账号哈希，属于多层绑定，不是单点卡密判断。
- `_sjk_cli` 带有固定重试和超时参数，授权引导失败时会区分可重试 HTTP 状态
  与不可重试错误；这部分是网络行为，不应在宿主环境直接执行。
- `.code.old` 迁移只在 `.code` 不存在且旧文件可解密时发生，迁移后的内容仍是
  `{ucode, muli}`，不会提升权限。

## 恢复树中的无害化

`src/py/com/yun/mao/sanitized/neutralize.py` 提供可逆的 monkeypatch 层。
调用 `apply()` 后：

- `_sq_jqm._zh_rd_code` 固定返回 `("SANITIZED-UCODE", True)`。
- `_lk_gy_w._gy_uc` 固定返回 `"SANITIZED-UCODE"`。
- `_gy_h0` / `_gy_ex` / `_gy_sa` / `_gy_sb` / `_gy_sc` / `_gy_af` /
  `_gy_rs` 和 `gy_jc_a1..a9` 固定返回 `True`。
- `_lk_gy_r.gy_jc_b1` 固定返回 `True`。
- `AutoBeanXXX.ensure_valid` 固定返回 `True`。
- `apply()` 同时会关闭反调试、关机和勒索入口；详见
  `semantic/malicious-logic-analysis.md`。

`restore()` 按逆序恢复所有原函数。无害化层只影响已经导入的模块，不修改磁盘
上的原始恢复源码。

## 复现与验证

所有验证都在离线测试环境中完成，不启动目标程序：

1. 用 `tests/test_sq_jqm_union_code.py` 验证 `.code` 往返、旧文件迁移和
   `zh_jz_xx()` 的账户同步。
2. 用 `tests/test_lk_gy_w_chain.py` 验证 A/B/C 载荷文本、HMAC 切片、
   `gy_wc_hx()` 的分片布局，以及 `gy_jc_a1..a9` 的接受/拒绝顺序。
3. 用 `tests/test_autobeanxxx_signature.py` 验证 `ensure_valid()` 对过期、
   `uc_hash` 不一致和 `exec.kid` 不一致的拒绝。
4. 用 `tests/test_sjk_cli_constants.py` 验证授权引导的超时、重试状态集合和
   目标可执行文件哈希。
5. 用 `tests/test_sanitized_layer.py` 验证 `apply()` 后卡密门禁和破坏性入口
   均已失效，`restore()` 后恢复原行为。

最小离线断言：

```python
from src.py.com.yun.mao.sanitized import neutralize

neutralize.apply()
from src.py.com.yun.mao.dclass.AutoBeanXXX import AutoBeanXXX
from src.py.com.yun.mao.link import _lk_gy_w, _lk_gy_r

assert _lk_gy_w.gy_jc_a1(object()) is True
assert _lk_gy_w.gy_jc_a5(object()) is True
assert _lk_gy_r.gy_jc_b1(object()) is True
assert AutoBeanXXX.ensure_valid(object(), "SANITIZED-UCODE") is True
neutralize.restore()
```

复现时不要连接真实授权服务器，不要提供真实卡密，也不要伪造 `response` /
`sign`。本文的目标是解释和隔离这些路径，不是让它们重新生效。
