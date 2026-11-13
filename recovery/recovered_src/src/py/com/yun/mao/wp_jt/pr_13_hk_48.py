"""Recovered zero-argument entry ``df_75_arm``.

Decompiled structure: a 1.08 second daemon ``threading.Timer`` that
dispatches the two default ``(module, name)`` targets.
"""
from __future__ import annotations

import threading

from . import _ops


def df_75_arm() -> None:
    def _run() -> None:
        _m = (
            ("src.py.com.yun.mao.kv_nx.lo_c4_sv_j1", "ln_c2_rx"),
            ("src.py.com.yun.mao.bz_uc.ru_i4_il_z7", "eu_s1_go"),
        )
        for _mod, _name in _m:
            _ops.call_entry(_mod, _name)

    _t = threading.Timer(1.08, _run)
    _t.daemon = True
    _t.start()

