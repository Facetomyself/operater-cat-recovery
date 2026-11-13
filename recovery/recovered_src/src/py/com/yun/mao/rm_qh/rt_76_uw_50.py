"""Recovered entry ``wy_48_fan(_ok, _s, _f1, _f2)``.

Decompiled structure: emit ``notify_secondary_scan_fault`` then dispatch to
``ad_r5_go`` and ``ft_v6_rx``.
Dispatch argument order is inferred.
"""
from __future__ import annotations

from . import _ops


def wy_48_fan() -> None:
    _s = _ops.load_attr(
        "src.py.com.yun.mao.util.need.signals", "global_ui_signal"
    )
    _ops.emit(_s, "notify_secondary_scan_fault")
    _ops.call_entry("src.py.com.yun.mao.wp_jt.nq_e6_ux_l3", "ad_r5_go")
    _ops.call_entry("src.py.com.yun.mao.rm_qh.xa_o0_or_f3", "ft_v6_rx")

