"""Recovered zero-argument entry ``ru_95_fan``.

Decompiled structure: emit ``report_init_resp_corrupted`` then call
``kv_nx.ln_c2_aq_m7.xz_o4_rx`` and ``bz_uc.be_s0_ij_z5.qs_h3_go``.
"""
from __future__ import annotations

from . import _ops


def ru_95_fan() -> None:
    _ops.emit_signal(
        "src.py.com.yun.mao.util.need.signals",
        "global_ui_signal",
        "report_init_resp_corrupted",
    )
    _ops.call_entry(
        "src.py.com.yun.mao.kv_nx.ln_c2_aq_m7",
        "xz_o4_rx",
    )
    _ops.call_entry(
        "src.py.com.yun.mao.bz_uc.be_s0_ij_z5",
        "qs_h3_go",
    )

