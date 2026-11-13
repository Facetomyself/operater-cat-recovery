"""Recovered zero-argument entry ``eg_v7_rx``.

Decompiled structure: ``ctypes.CDLL``, hidden export lookup, call with
``(1,)`` and ``os._exit(1)``.  Optional CDLL keyword defaults are not
observable as non-default values.
"""
from __future__ import annotations

import ctypes
import os

from ..link._fds_jm import sec


def eg_v7_rx() -> None:
    _sy = sec("hi_xp_7m")
    _z = sec("sx_ql_7n")
    _ct = ctypes.CDLL(_sy)
    _lib = _ct
    _ep = getattr(_ct, _z)
    _o = _ep(1)
    _p = _o
    os._exit(1)

