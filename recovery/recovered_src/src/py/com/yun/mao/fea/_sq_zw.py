# Recovered module: src.py.com.yun.mao.fea._sq_zw
# Certificate-pinning / production-host selection path.
from __future__ import annotations

import hashlib
import socket
import ssl
import time
from urllib.parse import urlparse

import certifi

from ..link._fds_jm import sec
from ..link._fds_tan import wb_sock, wb_tls_wd
from ..link._tw_ctx import TwCtx
from ..util import TracePrinterHelper
from . import _sq_pz


_CACHE_TTL_SUCCESS = 300
_CACHE_TTL_FAILURE = 30
_cache_ttl = _CACHE_TTL_SUCCESS
_cached_at = 0.0
_cached_result: str | None = None
_cached_prod_host = "birder.jinsiqie.life"


def zw_hq_zs(hostname: str, port: int = 443) -> str | None:
    """Return the uppercase SHA-256 fingerprint of a server certificate."""
    context = None
    sock = None
    ssock = None
    der_cert = None
    try:
        try:
            wb_sock()
        except Exception:
            pass
        context = ssl.create_default_context(cafile=certifi.where())
        sock = socket.create_connection((hostname, port), timeout=10)
        try:
            wb_tls_wd()
        except Exception:
            pass
        ssock = context.wrap_socket(sock, server_hostname=hostname)
        der_cert = ssock.getpeercert(binary_form=True)
    except Exception as exc:
        try:
            TracePrinterHelper.print_trace(sec("wl_jy_zw_05"))
        except Exception:
            pass
        _ = exc
        return None
    finally:
        try:
            if ssock is not None:
                ssock.close()
            elif sock is not None:
                sock.close()
        except Exception:
            pass
    if not der_cert:
        return None
    return hashlib.sha256(der_cert).hexdigest().upper()


def _normalize_fingerprint(value: object) -> str:
    return str(value or "").replace(":", "").replace(" ", "").upper()


def _fingerprint_entries() -> list[tuple[str, str]]:
    """Normalize the recovered fingerprint catalog into ``(host, fp)`` pairs."""
    entries: list[tuple[str, str]] = []
    raw_items = getattr(_sq_pz, "YC_ZW_HC_LB", []) or []
    for item in raw_items:
        if isinstance(item, str):
            entries.append((item, ""))
        elif isinstance(item, (tuple, list)):
            if len(item) >= 2:
                entries.append((str(item[0]), _normalize_fingerprint(item[1])))
            elif item:
                entries.append((str(item[0]), ""))
        elif isinstance(item, dict):
            host = item.get("host") or item.get("hostname") or ""
            fp = item.get("fp") or item.get("fingerprint") or ""
            entries.append((str(host), _normalize_fingerprint(fp)))
    return entries


def zw_bd_zs(
    hostname: str,
    fingerprint_list: object = None,
    port: int = 443,
) -> bool:
    """Connect to ``hostname`` and verify its certificate fingerprint."""
    actual_fingerprint = None
    try:
        actual_fingerprint = zw_hq_zs(hostname, port)
        if not actual_fingerprint:
            return False
        if fingerprint_list is None:
            fingerprint_list = [
                fp for host, fp in _fingerprint_entries() if host == hostname and fp
            ]
        if isinstance(fingerprint_list, str):
            fingerprint_list = [fingerprint_list]
        expected = {_normalize_fingerprint(value) for value in fingerprint_list or []}
        return actual_fingerprint in expected
    except Exception as exc:
        try:
            print(sec("wl_jy_zw_05").format(exc))
        except Exception:
            pass
        _ = actual_fingerprint
        return False


def zw_bd_zw(origin: str | None = None) -> bool:
    """Validate the configured production origin against the pin catalog."""
    try:
        if origin is None:
            origin = TwCtx.tw_hq_by_k("_p_dh")
        hostname = urlparse(str(origin or "")).hostname
        if not hostname:
            return False
        return zw_bd_zs(hostname)
    except Exception as exc:
        try:
            print(sec("pz_not_ready_01"), exc)
        except Exception:
            pass
        return False


def _zw_hq_prod_host() -> str:
    """Return the cached production host, refreshing its certificate pin."""
    global _cache_ttl, _cached_at, _cached_result
    now = time.monotonic()
    if _cached_result and now - _cached_at < _cache_ttl:
        return _cached_result

    result: str | None = None
    for hostname, fingerprint in _fingerprint_entries():
        if not hostname:
            continue
        if zw_bd_zs(hostname, [fingerprint] if fingerprint else None):
            result = hostname
            break
    if result is None:
        try:
            origin = TwCtx.tw_hq_by_k("_p_dh")
            hostname = urlparse(str(origin or "")).hostname
            if hostname and zw_bd_zw(origin):
                result = hostname
        except Exception:
            result = None
    if result is None:
        result = _cached_prod_host
        _cache_ttl = _CACHE_TTL_FAILURE
    else:
        _cache_ttl = _CACHE_TTL_SUCCESS
    _cached_result = result
    _cached_at = now
    return result
