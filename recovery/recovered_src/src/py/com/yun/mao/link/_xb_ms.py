# Recovered module: src.py.com.yun.mao.link._xb_ms
# Public names/signatures and retry/timeout constants come from the Nuitka
# module table and init decompilation.  Network body details below are
# behaviour-level reconstructions and are marked inferred.
from __future__ import annotations

import asyncio
import json

from PyQt5.QtCore import QRunnable, QThreadPool

from ._fds_jm import sec
from ._sjk_bao import sjk_zz_hb
from ._sjk_cli import SjkCli
from ._tw_ctx import TwCtx
from src.py.com.yun.mao.util import TracePrinterHelper


_ALLOWED_PATH_PREFIX = "/xb/"
_CATALOG_PATH_KEY = "_v_s_f_ms"
_MAX_RETRY = 4
_RETRY_BASE_DELAY_SEC = 1.5
_HTTP_TIMEOUT_SEC = 120
_CONNECT_TIMEOUT_SEC = 30
_RETRYABLE_HTTP_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})

def join_xb_url(origin: str, path: str) -> str | None:
    if not isinstance(origin, str) or not isinstance(path, str):
        return None
    origin = origin.strip()
    path = path.strip()
    if "://" not in origin:
        return None
    if not path.startswith(_ALLOWED_PATH_PREFIX):
        return None
    if "\\" in path or ".." in path or "?#" in path:
        return None
    clean_origin = origin.rstrip("/")
    clean_path = "/".join(part for part in path.split("/") if part)
    return f"{clean_origin}/{clean_path}"


def _sx_zw_hc() -> None:
    """Reset the certificate-pin cache on ``_sq_zw``."""
    from src.py.com.yun.mao.fea import _sq_zw

    _sq_zw._cached_result = None
    _sq_zw._cached_at = 0.0
    _sq_zw._cache_ttl = 0.0
    return None


def apply_md5s_body(body: dict) -> bool:
    """Refresh the catalog and pin cache when ``body['lg']`` is present."""
    if not isinstance(body, dict):
        return False
    if not body.get("lg"):
        return False
    try:
        from src.py.com.yun.mao.fea import _sq_pz

        _sq_pz.a_r_zw_md(sec("s_k_mL_slde_"))
        _sx_zw_hc()
        return True
    except Exception:
        return False


def _resolve_url() -> str | None:
    """Resolve and validate the XB catalog URL."""
    try:
        from src.py.com.yun.mao.fea import _sq_req
        from src.py.com.yun.mao.fea._sq_hj import hj_dev_ok

        origin = getattr(_sq_req, "URL_PRE_COM", "") or TwCtx.tw_hq_by_k("SO")
        path = TwCtx.tw_hq_by_k(_CATALOG_PATH_KEY)
        validate = getattr(SjkCli, "_sjk_validate_url", None)
        if callable(validate):
            candidate = validate(origin, path)
            if candidate:
                candidate = validate(candidate, dev=hj_dev_ok())
                if candidate:
                    return str(candidate)
        return join_xb_url(str(origin or ""), str(path or ""))
    except Exception as e:
        try:
            print(e)
        except Exception:
            pass
        return None


async def _post_once(
    url: str,
    version: str,
    exe_hash: str,
    ssl_verify: bool,
) -> tuple[bool, bool]:
    """POST one signed XB request and decode the AES/RSA response envelope."""
    import aiohttp

    payload, dy_aes_key = SjkCli._sjk_db_qq(
        TwCtx.tw_sjk_pk_pem(),
        sjk_zz_hb(version, exe_hash),
    )
    if payload is None:
        return False, False
    headers = {"Content-Type": "application/json"}
    timeout = aiohttp.ClientTimeout(
        total=_HTTP_TIMEOUT_SEC, connect=_CONNECT_TIMEOUT_SEC
    )
    try:
        connector = aiohttp.TCPConnector(ssl=ssl_verify)
        async with aiohttp.ClientSession(
            connector=connector, timeout=timeout
        ) as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status in _RETRYABLE_HTTP_STATUS:
                    return False, True
                if resp.status != 200:
                    return False, False
                try:
                    outer = await resp.json()
                except (aiohttp.ClientPayloadError, json.JSONDecodeError):
                    outer = json.loads(await resp.text())
    except (aiohttp.ClientError, asyncio.TimeoutError, TimeoutError):
        return False, True
    except Exception as e:
        try:
            print(e)
        except Exception:
            pass
        return False, False

    if not isinstance(outer, dict) or not outer.get("isSuccess"):
        return False, False
    data = outer.get("data") or {}
    if not isinstance(data, dict):
        return False, False
    inner = SjkCli._sjk_jb_xy(
        data.get("response", ""),
        data.get("sign", ""),
        dy_aes_key,
    )
    if inner is None:
        inner = data.get("msg")
    if isinstance(inner, dict):
        apply_md5s_body(inner)
    return bool(inner), False


async def _fe_s_l_nt_ine() -> bool:
    """Retry the XB request four times with linear backoff."""
    url = _resolve_url()
    if not url:
        return False
    try:
        version = str(SjkCli._resolve_version() or "")
        exe_hash = str(SjkCli._sjk_exe_hx() or "")
    except Exception:
        version = ""
        exe_hash = ""
    applied = False
    for attempt in range(_MAX_RETRY):
        applied, retryable = await _post_once(
            url, version, exe_hash, True
        )
        if applied:
            return True
        if not retryable:
            return False
        if attempt + 1 < _MAX_RETRY:
            await asyncio.sleep(_RETRY_BASE_DELAY_SEC * (attempt + 1))
    return applied


class _fe_skld_inte(QRunnable):
    def run(self) -> None:
        try:
            asyncio.run(_fe_s_l_nt_ine())
        except Exception as e:
            try:
                print(e)
                TracePrinterHelper.print_trace(e)
            except Exception:
                pass


def kai_shit_f_m_5s() -> None:
    try:
        QThreadPool.globalInstance().start(_fe_skld_inte())
    except Exception as e:
        try:
            print(e)
            TracePrinterHelper.print_trace(e)
        except Exception:
            pass
    return None
