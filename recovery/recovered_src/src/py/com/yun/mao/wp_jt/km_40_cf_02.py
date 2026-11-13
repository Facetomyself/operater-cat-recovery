"""Recovered zero-argument entry ``rt_40_fan``.

Decompiled structure: emit ``cmd_probe_full_fault`` then dispatch the two
``(module, name)`` targets embedded in the module constants.
"""
from __future__ import annotations

from . import _ops


def rt_40_fan() -> None:
    _ops.emit_signal(
        "src.py.com.yun.mao.util.need.signals",
        "global_ui_signal",
        "cmd_probe_full_fault",
    )
    _m = (
        ("src.py.com.yun.mao.bz_uc.lo_c4_or_f7", "mp_d1_go"),
        ("src.py.com.yun.mao.kv_nx.ru_i4_mp_d1", "tw_k2_rx"),
    )
    for _mod, _name in _m:
        _ops.call_entry(_mod, _name)

