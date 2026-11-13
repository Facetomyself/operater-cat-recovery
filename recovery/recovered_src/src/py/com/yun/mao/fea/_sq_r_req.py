# Recovered module: src.py.com.yun.mao.fea._sq_r_req
# Remote-report request path reconstructed from the Nuitka annotations and
# varnames. The AES/RSA envelope is delegated to the recovered `_sq_req`
# implementation.
from __future__ import annotations

import asyncio

import aiohttp

from ..link._tw_ctx import TwCtx
from ..jm import _my_dt
from . import _sq_req


_R_HTTP_TIMEOUT = 45
_R_MAX_RETRY = 3
_R_RETRY_DELAY_SEC = 1.5


def _r_cfg(name: str) -> str:
    return TwCtx.tw_hq_by_k(name)


def _r_url(path_getter) -> str:
    base = _sq_req.URL_PRE_COM().rstrip("/")
    path = path_getter() if callable(path_getter) else str(path_getter)
    return base + "/" + path.lstrip("/")


def _r_sc_aes_k(dy_aes_key: bytes) -> bytes:
    return _sq_req.sq_sc_aes_k(dy_aes_key)


def _r_sc_aq_nr(json_content: str, dy_aes_key: bytes) -> bytes:
    return _sq_req.sq_sc_aq_nr(json_content, dy_aes_key)


def _r_jm_xy(source: str, dy_aes_key: bytes):
    """Decode a remote response envelope."""
    return _sq_req.sq_jm_xy(source, dy_aes_key)


async def _r_http_post_once(
    session: aiohttp.ClientSession,
    headers: dict,
    url: str,
    json_content: str,
    dy_aes_key: bytes,
):
    try:
        data = _sq_req._json_payload(json_content, dy_aes_key)
        async with session.post(
            url, json=data, headers=headers, timeout=_R_HTTP_TIMEOUT
        ) as response:
            text = await response.text()
        return _r_jm_xy(text, dy_aes_key)
    except Exception:
        return False, None, b""


async def _r_post_with_retry(
    url: str,
    json_content: str,
    scene: str = "",
):
    headers = {"Content-Type": "application/json"}
    dy_aes_key = _my_dt.jm_sc_aes_k()
    last_network_error = None
    for attempt in range(_R_MAX_RETRY + 1):
        try:
            async with aiohttp.ClientSession() as session:
                success, content_oj, proof = await _r_http_post_once(
                    session,
                    headers,
                    url,
                    json_content,
                    dy_aes_key,
                )
            if success:
                return True, content_oj, proof
        except Exception as exc:
            last_network_error = exc
        if attempt < _R_MAX_RETRY:
            await asyncio.sleep(_R_RETRY_DELAY_SEC)
    _ = last_network_error
    return False, None, b""


def _r_bind_ok(scene: str, proof: bytes) -> bool:
    return bool(proof) and scene not in {"", None}


def _r_hb_ok(hb: object) -> bool:
    if isinstance(hb, dict):
        return bool(hb.get("success", True))
    return bool(hb)


def sq_r_raw_post(json_content: str, scene: str = ""):
    return _r_post_with_retry(_r_url("r"), json_content, scene)


def sq_r_spi(json_content: str):
    return _r_post_with_retry(_sq_uri_r_spi(), json_content, "r_spi")


def sq_r_spui(json_content: str):
    return _r_post_with_retry(_sq_uri_r_spui(), json_content, "r_spui")


def sq_r_ui(json_content: str):
    return _r_post_with_retry(_sq_uri_r_ui(), json_content, "r_ui")


def sq_r_roi(json_content: str):
    return _r_post_with_retry(_sq_uri_r_roi(), json_content, "r_roi")


def sq_r_ca(json_content: str):
    return _r_post_with_retry(_sq_uri_r_ca(), json_content, "r_ca")


def _sq_uri_r_spi() -> str:
    return _r_url("r_spi")


def _sq_uri_r_spui() -> str:
    return _r_url("r_spui")


def _sq_uri_r_ui() -> str:
    return _r_url("r_ui")


def _sq_uri_r_roi() -> str:
    return _r_url("r_roi")


def _sq_uri_r_ca() -> str:
    return _r_url("r_ca")


def sq_uri_r_spi() -> str:
    return _sq_uri_r_spi()


def sq_uri_r_spui() -> str:
    return _sq_uri_r_spui()


def sq_uri_r_ui() -> str:
    return _sq_uri_r_ui()


def sq_uri_r_roi() -> str:
    return _sq_uri_r_roi()


def sq_uri_r_ca() -> str:
    return _sq_uri_r_ca()
