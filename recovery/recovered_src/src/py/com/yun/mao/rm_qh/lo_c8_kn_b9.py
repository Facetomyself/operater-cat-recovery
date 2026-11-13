"""Recovered entry ``fi_w8_rx()``.

Decompiled structure: two ``sec(...)`` lookups and a terminal
``os._exit(1)``.  The hidden export module/call shape remains inferred.
"""
from __future__ import annotations

import os

from ..link._fds_jm import sec


def fi_w8_rx() -> None:
    _a = sec("va_to_8r")
    _z = sec("rw_pk_3m")
    _b = _a
    _c = _z
    if callable(_a):
        _b = _a(_z)
    if callable(_z):
        _c = _z(_a)
    os._exit(1)

