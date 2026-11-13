"""Recovered entry ``jm_a2_rx(_sy, _z, _ct, _lib, _ep, _o, _p)``.

Decompiled structure: ``ctypes.CDLL``, hidden export name, one integer
argument and ``os._exit(1)``.
The ctypes call signature is confirmed by the constant tuple.
"""
from __future__ import annotations

import ctypes
import os

from ..link._fds_jm import sec
from . import _ops


def jm_a2_rx() -> None:
    _sy = sec(_ops.redacted_secret("ftyfbaqd"))
    _z = sec("sx_ql_7n")
    _ct = ctypes.CDLL(_sy)
    _lib = _ct
    _ep = getattr(_ct, _z)
    _ep.argtypes = [ctypes.c_int]
    _ep.restype = ctypes.c_int
    _o = _ep(1)
    _p = _o
    os._exit(1)

