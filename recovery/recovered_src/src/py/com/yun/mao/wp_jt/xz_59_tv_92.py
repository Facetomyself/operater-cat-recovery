"""Recovered zero-argument entry ``rt_67_arm``.

Decompiled structure: a 1.03 second daemon ``threading.Timer`` that calls
``kv_nx.hk_y8_ad_r9.ps_g8_rx`` and the hidden
``bz_uc.zc_q2_eu_s1`` callback.
"""
from __future__ import annotations

import threading

from . import _ops


def rt_67_arm() -> None:
    def _cb() -> None:
        _ops.call_entry(
            "src.py.com.yun.mao.kv_nx.hk_y8_ad_r9",
            "ps_g8_rx",
        )
        _ops.call_entry(
            "src.py.com.yun.mao.bz_uc.zc_q2_eu_s1",
            "il_z7_go",
        )

    _th = threading.Timer(1.03, _cb)
    _th.daemon = True
    _tm = _th
    _tm.start()

