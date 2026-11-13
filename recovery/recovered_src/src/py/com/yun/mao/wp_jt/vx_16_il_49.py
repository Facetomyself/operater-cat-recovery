"""Recovered zero-argument entry ``bd_29_fan``.

Decompiled structure: emit ``report_conn_timing_fault`` then call
``bz_uc.tw_k2_mp_d1.or_f7_go`` and ``kv_nx.ps_g8_ux_l9.vy_m8_rx``.
"""
from __future__ import annotations

from . import _ops


def bd_29_fan() -> None:
    _ops.emit_signal(
        "src.py.com.yun.mao.util.need.signals",
        "global_ui_signal",
        "report_conn_timing_fault",
    )
    _ops.call_entry(
        "src.py.com.yun.mao.bz_uc.tw_k2_mp_d1",
        "or_f7_go",
    )
    _ops.call_entry(
        "src.py.com.yun.mao.kv_nx.ps_g8_ux_l9",
        "vy_m8_rx",
    )

