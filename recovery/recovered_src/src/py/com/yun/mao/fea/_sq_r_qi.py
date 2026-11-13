# Recovered module: src.py.com.yun.mao.fea._sq_r_qi
# Startup heartbeat / remote-user / item-memory bootstrap path.
from __future__ import annotations

import asyncio
import base64
import gzip
from typing import Any

from . import _sq_chk, _sq_jqm, _sq_r_bao, _sq_r_req
from ..dclass import ItemMemStore, LoadDataClass
from ..link._fds_jm import sec
from ..util.need import signals, utils
from ._r_hb_file import RemoteHb


_SPI_BIZ_RETRY = 4


def _decode_cloud_item(encoding: str, payload_b64: str) -> Any:
    """Decode the optional item snapshot carried by a heartbeat response."""
    if not payload_b64:
        return None
    raw = base64.b64decode(payload_b64)
    if encoding == "gzip":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8")


def _item_wire_tuple(item: Any) -> tuple[bool, str, str]:
    """Normalize an item snapshot to ``(empty, encoding, payload_b64)``.

    The server accepts both ``payloadB64`` (legacy) and ``payload_b64``.  An
    empty item is represented by the default ``(True, "gzip", "")`` tuple.
    """
    if not item:
        return True, "gzip", ""
    if isinstance(item, (tuple, list)):
        if len(item) >= 3:
            return bool(item[0]), str(item[1] or "gzip"), str(item[2] or "")
        if len(item) == 2:
            return False, str(item[1] or "gzip"), str(item[0] or "")
        return False, "gzip", str(item[0] or "")
    if not isinstance(item, dict):
        return False, "gzip", str(item)

    payload_b64 = item.get("payloadB64")
    if payload_b64 is None:
        payload_b64 = item.get("payload_b64", "")
    payload_b64 = str(payload_b64 or "").strip()
    if not payload_b64:
        return True, "gzip", ""

    encoding = item.get("encoding") or item.get("item_encoding") or "gzip"
    return False, str(encoding), payload_b64


def _coerce_remote_hb(result: Any) -> RemoteHb:
    """Accept the historical tuple result or a ``RemoteHb`` object."""
    if isinstance(result, RemoteHb):
        return result
    if isinstance(result, tuple):
        if len(result) >= 2 and isinstance(result[0], bool):
            ok = result[0]
            payload = result[1]
            if ok:
                return RemoteHb.success(payload)
            return RemoteHb.failed_retry(str(payload or ""))
        if len(result) >= 3 and isinstance(result[0], bool):
            ok = result[0]
            return RemoteHb.success(result[1]) if ok else RemoteHb.failed_retry(
                str(result[2] or "")
            )
    if isinstance(result, dict):
        if result.get("isSuccess", True):
            return RemoteHb.success(result)
        return RemoteHb.failed_retry(str(result.get("msg", "")))
    if result is None:
        return RemoteHb.failed_retry("")
    return RemoteHb.success(result)


def _apply_user_from_remote(
    data: Any,
    user: Any = None,
) -> tuple[bool, bool]:
    """Apply a remote account/report object to the current account state.

    Returns ``(applied, mul_changed)``.  ``hy_jx_bc`` is the authoritative
    parser for the server's ``data`` object and also updates
    ``_sq_jqm.current_account_info``.
    """
    try:
        if isinstance(data, RemoteHb):
            data = data.data
        if isinstance(data, dict) and "data" in data:
            if not data.get("isSuccess", True):
                print(str(data.get("msg", "")))
                return False, False
            data = data.get("data") or {}
        if not isinstance(data, dict):
            return False, False

        old_mul = bool(getattr(user, "mul", False))
        info = _sq_chk.hy_jx_bc(data)
        if user is not None and user is not info:
            for name, value in vars(info).items():
                try:
                    setattr(user, name, value)
                except Exception:
                    pass
        mul_changed = old_mul != bool(getattr(info, "mul", False))
        if mul_changed:
            try:
                signals.global_ui_signal.report_status_waring.emit("")
            except Exception:
                pass
        return True, mul_changed
    except Exception as exc:
        try:
            print(sec("jqm_yz_tpl_12").format(exc))
        except Exception:
            print(str(exc))
        return False, False


def _build_spi_body(ucode: str, item_b64: str = "", include_item: bool = False) -> str:
    """Build the heartbeat body while tolerating the two recovered signatures."""
    try:
        return _sq_r_bao.zq_r_item_hb(
            ucode,
            item_b64=item_b64,
            include_item=include_item,
        )
    except TypeError:
        return _sq_r_bao.zq_r_item_hb(
            ucode,
            item_b64,
            include_item,
        )


async def _spi_fetch(ucode: str) -> RemoteHb | None:
    """Fetch one SPI heartbeat with bounded retries."""
    if not ucode:
        return None
    last_hb: RemoteHb | None = None
    for attempt in range(_SPI_BIZ_RETRY):
        try:
            body = _build_spi_body(ucode, include_item=False)
            result = await _sq_r_req.sq_r_spi(body)
            last_hb = _coerce_remote_hb(result)
            if _sq_r_req._r_hb_ok(last_hb):
                return last_hb
            if getattr(last_hb, "terminal", False):
                break
        except Exception as exc:
            last_hb = RemoteHb.failed_retry(str(exc))
        if attempt + 1 < _SPI_BIZ_RETRY:
            try:
                await asyncio.sleep(_sq_r_req._R_RETRY_DELAY_SEC)
            except Exception:
                pass
    return last_hb


def _bootstrap_item_memory(data: dict) -> tuple[str, int]:
    """Apply the server snapshot and return ``(branch, auto_count)``."""
    is_register = bool(data.get("is_register"))
    item = data.get("item")
    empty, encoding, payload_b64 = _item_wire_tuple(item)
    branch = "register" if is_register else "login"
    try:
        decoded = _decode_cloud_item(encoding, payload_b64) if not empty else None
    except Exception:
        decoded = None
        print(sec("cloud item decode fail"))
    try:
        ItemMemStore.bootstrap_item_memory(
            is_register,
            empty,
            encoding,
            payload_b64,
        )
    except Exception as exc:
        print(f"{sec('cloud item decode fail')}: {exc}")
    auto_count = 0
    try:
        auto_map = LoadDataClass.getAutoMap()
        auto_count = len(auto_map) if hasattr(auto_map, "__len__") else 0
    except Exception:
        pass
    try:
        print(f"[item-bootstrap] branch={branch} autoCount={auto_count}")
    except Exception:
        pass
    _ = decoded
    return branch, auto_count


def qd_r_spi_boot() -> None:
    """Boot the heartbeat and seed the local account/item state."""
    user = _sq_jqm.current_account_info
    ucode = getattr(user, "ucode", "") or ""
    try:
        ucode = utils.un_mask_ucode(ucode)
    except Exception:
        pass
    if not ucode:
        return None
    last_hb = _spi_fetch(ucode)
    if last_hb is None:
        return None
    data = last_hb.data if isinstance(last_hb, RemoteHb) else last_hb
    if isinstance(data, dict):
        ok, mul_changed = _apply_user_from_remote(data, user)
        if ok:
            _bootstrap_item_memory(data)
        _ = mul_changed
    return None


def qd_r_zc_after_register(success: bool) -> None:
    """Refresh account and item state after a registration attempt."""
    if not success:
        return None
    user = _sq_jqm.current_account_info
    ucode = getattr(user, "ucode", "") or ""
    try:
        ucode = utils.un_mask_ucode(ucode)
    except Exception:
        pass
    if not ucode:
        return None
    last_hb = _spi_fetch(ucode)
    if last_hb is None:
        return None
    data = last_hb.data if isinstance(last_hb, RemoteHb) else last_hb
    if isinstance(data, dict):
        ok, _ = _apply_user_from_remote(data, user)
        if ok:
            _bootstrap_item_memory(data)
    return None
