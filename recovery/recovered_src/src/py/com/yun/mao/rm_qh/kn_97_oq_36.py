"""Recovered entry ``ik_30_fan(_gs, _e1, _e2)``.

Decompiled structure: emit ``cmd_cert_anchor_mismatch`` then dispatch to
``jm_a2_rx`` and ``cf_t1_go``.
Dispatch argument order is inferred.
"""
from __future__ import annotations

from . import _ops


def ik_30_fan() -> None:
    _gs = _ops.load_attr(
        "src.py.com.yun.mao.util.need.signals", "global_ui_signal"
    )
    _ops.emit(_gs, "cmd_cert_anchor_mismatch")
    _ops.call_entry("src.py.com.yun.mao.rm_qh.vy_m4_wz_n1", "jm_a2_rx")
    _ops.call_entry("src.py.com.yun.mao.wp_jt.vy_m4_sv_j7", "cf_t1_go")

