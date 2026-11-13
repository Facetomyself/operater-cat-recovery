"""Recovered entry ``xa_98_arm(_x1, _x2)``.

Decompiled structure: a 1.15 second ``threading.Timer`` whose callback
dispatches to ``wz_n1_go`` and ``bx_n2_rx``.
Callback argument forwarding is inferred.
"""
from __future__ import annotations

import threading

from . import _ops


def xa_98_arm() -> None:
    def _kick() -> None:
        _ops.call_entry("src.py.com.yun.mao.wp_jt.be_s4_km_b7", "wz_n1_go")
        _ops.call_entry("src.py.com.yun.mao.rm_qh.np_e4_cf_t1", "bx_n2_rx")

    _T = threading.Timer(1.15, _kick)
    _T.daemon = True
    _u = _T
    _u.start()

