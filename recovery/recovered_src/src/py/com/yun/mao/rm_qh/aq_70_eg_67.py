"""Recovered entry ``bd_29_arm()``.

Decompiled structure: a 1.12 second ``threading.Timer`` whose callback
dispatches to ``su_j5_go`` and ``zb_q6_rx``.
Callback argument forwarding is inferred.
"""
from __future__ import annotations

import threading

from . import _ops


def bd_29_arm() -> None:
    def _cb() -> None:
        _ops.call_entry("src.py.com.yun.mao.wp_jt.tw_k6_or_f3", "su_j5_go")
        _ops.call_entry("src.py.com.yun.mao.rm_qh.ru_i0_ux_l3", "zb_q6_rx")

    _th = threading.Timer(1.12, _cb)
    _th.daemon = True
    _tm = _th
    _tm.start()

