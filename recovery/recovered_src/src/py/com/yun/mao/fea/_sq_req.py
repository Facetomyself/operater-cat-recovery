# Recovered module: src.py.com.yun.mao.fea._sq_req
# Legacy licence/order HTTP client.  Request bodies are AES-CBC encrypted and
# the per-request AES key is RSA-PKCS1v15 encrypted; responses are verified
# with the configured RSA public key before JSON decoding.
from __future__ import annotations

import asyncio
import json

import aiohttp

from ..jm import _my_dt, _my_gk, _my_util
from ..link._fds_jm import sec
from ..link._tw_ctx import TwCtx
from ..util import TracePrinterHelper
from . import _sq_bao, _sq_zw


HTTP_TIME_OUT = 45
OPERATION_EX_CODE_ALLOW_AUTO_RETRY = -11
PARSE_REQUEST_MAX_RETRY = 3
PARSE_REQUEST_RETRY_DELAY_SEC = 1.5

_config_cache: dict[str, str] = {}
_sessions: dict[object, aiohttp.ClientSession] = {}


def _get_config(name: str) -> str:
    if name not in _config_cache:
        _config_cache[name] = TwCtx.tw_hq_by_k(name)
    return _config_cache[name]


def get_dev_local_host() -> str:
    return _get_config("_p_dh")


def get_pro_duct_host() -> str:
    return _get_config("_r_u")


def is_product_env() -> bool:
    try:
        from src.py.version_code import is_prod_version

        return bool(is_prod_version())
    except Exception:
        return True


def get_host() -> str:
    try:
        from ._sq_hj import hj_dev_ok

        return get_dev_local_host() if hj_dev_ok() else get_pro_duct_host()
    except Exception:
        return get_pro_duct_host() if is_product_env() else get_dev_local_host()


def URL_PRE_COM() -> str:
    return str(get_host()).rstrip("/")


def _is_async_shutdown_error(exc: BaseException) -> bool:
    return isinstance(exc, (asyncio.CancelledError, RuntimeError)) and (
        "Event loop is closed" in str(exc)
        or "event loop is closed" in str(exc).lower()
    )


def failed_or_error(exc: BaseException) -> bool:
    return not _is_async_shutdown_error(exc)


async def aio_session() -> aiohttp.ClientSession:
    connector = aiohttp.TCPConnector(ssl=False)
    return aiohttp.ClientSession(
        connector=connector,
        timeout=aiohttp.ClientTimeout(total=HTTP_TIME_OUT),
    )


async def _get_shared_session(loop=None) -> aiohttp.ClientSession:
    loop = loop or asyncio.get_running_loop()
    session = _sessions.get(loop)
    if session is None or session.closed:
        session = await aio_session()
        _sessions[loop] = session
    return session


def sq_sc_aes_k(dy_aes_key: bytes) -> bytes:
    """Wrap the per-request AES key with the configured public RSA key."""
    public_key = _my_gk.jm_jz_gy_pk()
    return _my_util.rsa_encrypt_key(public_key, dy_aes_key)


def sq_sc_aq_nr(json_content: str, dy_aes_key: bytes) -> bytes:
    """Encrypt JSON content; the returned bytes start with the random IV."""
    return _my_util.aes_encrypt(json_content, dy_aes_key)


def sq_jm_xy(source: str, dy_aes_key: bytes):
    """Verify and decode one signed encrypted response envelope.

    Returns ``(success, content_oj, proof)``.  ``proof`` is the signature
    bytes when verification succeeds and ``b""`` on a malformed response.
    """
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


def _pack_final_send_once(dy_aes_key: bytes):
    """Build the RSA-wrapped key portion of the request envelope."""
    try:
        encrypted_aes_key = sq_sc_aes_k(dy_aes_key)
        return True, {"v2k": encrypted_aes_key.hex()}, False, dy_aes_key
    except Exception:
        return False, None, True, b""


def _json_payload(json_content: str, dy_aes_key: bytes) -> dict:
    encrypted_data = sq_sc_aq_nr(json_content, dy_aes_key)
    encrypted_aes_key = sq_sc_aes_k(dy_aes_key)
    return {
        "v1c": encrypted_data.hex(),
        "v2k": encrypted_aes_key.hex(),
    }


async def _http_post_once(
    url: str,
    json_content: str,
    scene: str = "",
    request_id: str = "",
    dy_aes_key: bytes | None = None,
    headers: dict | None = None,
    check_finger: bool = True,
):
    """POST one request and decode either plain or encrypted JSON."""
    try:
        if check_finger and not is_product_env():
            _sq_zw.zw_bd_zw()
    except Exception:
        pass
    session = None
    try:
        session = await _get_shared_session()
        payload = (
            _json_payload(json_content, dy_aes_key)
            if dy_aes_key is not None
            else json_content
        )
        async with session.post(
            url,
            json=payload if isinstance(payload, dict) else None,
            data=None if isinstance(payload, dict) else payload,
            headers=headers or {"Content-Type": "application/json"},
        ) as response:
            text = await response.text()
        if dy_aes_key is not None:
            return sq_jm_xy(text, dy_aes_key)
        return True, json.loads(text), b""
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        return False, None, str(exc).encode("utf-8")
    except Exception as exc:
        return False, None, str(exc).encode("utf-8")
    finally:
        _ = session


async def sq_fs_send_with_retry(
    url: str,
    json_content: str,
    scene: str = "",
    request_id: str = "",
    dy_aes_key: bytes | None = None,
    check_finger: bool = True,
):
    """Send a request with bounded retry and response envelope decoding."""
    last_error = None
    for attempt in range(PARSE_REQUEST_MAX_RETRY + 1):
        try:
            success, content_oj, proof = await _http_post_once(
                url,
                json_content,
                scene,
                request_id,
                dy_aes_key,
                check_finger=check_finger,
            )
            if success:
                return True, content_oj
            last_error = proof
        except Exception as exc:
            last_error = exc
        if attempt < PARSE_REQUEST_MAX_RETRY:
            try:
                await asyncio.sleep(
                    PARSE_REQUEST_RETRY_DELAY_SEC * (attempt + 1)
                )
            except Exception:
                pass
    _ = last_error
    return False, None


def _safe_parse_request_with_retry(
    u_code: str,
    parse_payload: dict,
    request_id: str = "",
):
    try:
        if isinstance(parse_payload, dict) and "data" in parse_payload:
            return True, parse_payload["data"]
        return bool(parse_payload), parse_payload
    except (KeyError, TypeError):
        return False, None


def _run_sync(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    return loop.create_task(coro)


def _emit_callback(callback, success: bool, content_oj=None) -> None:
    if callback is None:
        return
    try:
        callback(bool(success), content_oj)
    except TypeError:
        callback(bool(success))
    except Exception:
        try:
            TracePrinterHelper.print_trace(sec("wl_feifa_03"))
        except Exception:
            pass


def _request(
    url: str,
    json_content: str,
    *,
    scene: str = "",
    request_id: str = "",
    check_finger: bool = True,
    callback=None,
):
    dy_aes_key = _my_dt.jm_sc_aes_k()
    result = _run_sync(
        sq_fs_send_with_retry(
            url,
            json_content,
            scene,
            request_id,
            dy_aes_key=dy_aes_key,
            check_finger=check_finger,
        )
    )
    if asyncio.isfuture(result) or asyncio.iscoroutine(result):
        result = result
    else:
        success, content_oj = result
        _emit_callback(callback, success, content_oj)
    return result


def sq_uri_jym() -> str:
    return URL_PRE_COM() + "/jym"


def sq_uri_pz() -> str:
    return URL_PRE_COM() + "/pz"


def sq_uri_qy() -> str:
    return URL_PRE_COM() + "/qy"


def sq_uri_zc() -> str:
    return URL_PRE_COM() + "/zc"


def sq_uri_cz() -> str:
    return URL_PRE_COM() + "/cz"


def sq_uri_sb() -> str:
    return URL_PRE_COM() + "/sb"


def sq_uri_yp_ch() -> str:
    return URL_PRE_COM() + "/yp/ch"


def sq_uri_yp_cm() -> str:
    return URL_PRE_COM() + "/yp/cm"


def get_activate_code_uri(name: str = "") -> str:
    return URL_PRE_COM() + "/activate" + (f"/{name}" if name else "")


def get_create_order(*args, call_back=None, callback_need_await=False):
    json_content = _sq_bao.gen_create_order_content(*args)
    return _request(
        URL_PRE_COM() + "/cz",
        json_content,
        scene="create_order",
        callback=call_back,
    )


def createOrder(*args, call_back=None, callback_need_await=False):
    return get_create_order(
        *args,
        call_back=call_back,
        callback_need_await=callback_need_await,
    )


def get_check_order_recharge(*args, call_back=None, callback_need_await=False):
    json_content = _sq_bao.gen_check_order_content(*args)
    return _request(
        sq_uri_cz(),
        json_content,
        scene="check_order",
        callback=call_back,
    )


def CheckOrderAndRecharge(*args, call_back=None, callback_need_await=False):
    return get_check_order_recharge(
        *args,
        call_back=call_back,
        callback_need_await=callback_need_await,
    )


def sq_jy_ma(uCode: str, call_back=None, callback_need_await=False):
    body = _sq_bao.zq_jy_hb(uCode, "{}")
    result = _request(
        sq_uri_jym(),
        body,
        scene="login",
        callback=call_back,
    )
    return result


def sq_lq_pz(json_content: str = "{}", call_back=None):
    return _request(
        sq_uri_pz(),
        _sq_bao.zq_pz_hb(json_content),
        scene="pz",
        callback=call_back,
    )


def sq_ty_jh(u_code: str, call_back=None, callback_need_await=False):
    body = json.dumps({"uCode": u_code}, ensure_ascii=False, separators=(",", ":"))
    return _request(
        get_activate_code_uri(),
        body,
        scene="activate",
        callback=call_back,
    )


def sq_qy_dm(
    call_back,
    code_from: str,
    code_to: str,
    cover_expri: bool,
    force_cover_yun: bool,
):
    body = _sq_bao.gen_migrate_code_content(
        code_from,
        code_to,
        cover_expri,
        force_cover_yun,
        "{}",
    )
    return _request(
        sq_uri_qy(),
        body,
        scene="migrate",
        callback=call_back,
    )


def sq_zc(
    pre: str,
    fake: str,
    call_back=None,
    callback_need_await=False,
):
    body = _sq_bao.zq_zc_hb(pre, fake)
    return _request(
        sq_uri_zc(),
        body,
        scene="register",
        callback=call_back,
    )


def sq_cz_jqm(
    reset_code: str,
    reset_call_back=None,
    check_finger: bool = True,
    dy_aes_key: bytes | None = None,
):
    body = _sq_bao.zq_cz_hb(reset_code, "{}")
    if dy_aes_key is None:
        dy_aes_key = _my_dt.jm_sc_aes_k()
    result = _run_sync(
        sq_fs_send_with_retry(
            sq_uri_cz(),
            body,
            "reset",
            dy_aes_key=dy_aes_key,
            check_finger=check_finger,
        )
    )
    if not asyncio.isfuture(result):
        _emit_callback(reset_call_back, *result)
    return result


def sq_sb(
    uCode: str,
    report_call_back=None,
    callback_need_await=False,
):
    body = json.dumps({"uCode": uCode}, ensure_ascii=False, separators=(",", ":"))
    result = _request(sq_uri_sb(), body, scene="report", callback=report_call_back)
    return result


def sq_yp_pd_ch(
    u_code: str,
    parse_payload: dict,
    request_id: str = "",
    call_back=None,
):
    body = _sq_bao.zq_yp_ch_hb(u_code, parse_payload)
    result = _run_sync(
        sq_fs_send_with_retry(
            sq_uri_yp_ch(),
            body,
            "channel",
            request_id,
            dy_aes_key=_my_dt.jm_sc_aes_k(),
        )
    )
    success = False
    content = None
    if not asyncio.isfuture(result):
        success, content = result
    _emit_callback(call_back, success, content)
    return success, content


def sq_yp_pd_cm(
    u_code: str,
    parse_payload: dict,
    request_id: str = "",
    call_back=None,
):
    body = _sq_bao.zq_yp_cm_hb(
        json.dumps(parse_payload, ensure_ascii=False, separators=(",", ":"))
    )
    result = _run_sync(
        sq_fs_send_with_retry(
            sq_uri_yp_cm(),
            body,
            "comment",
            request_id,
            dy_aes_key=_my_dt.jm_sc_aes_k(),
        )
    )
    success = False
    content = None
    if not asyncio.isfuture(result):
        success, content = result
    _emit_callback(call_back, success, content)
    return success, content
