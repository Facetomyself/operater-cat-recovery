"""Recovered entry ``dg_09_fan(global_ui_signal, _sig, _mod, _name, _m)``.

Decompiled structure: emit ``cmd_probe_light_fault`` then import each
``(module, name)`` target and invoke it.  The target tuple is embedded in
the module constants.
Import order and invocation order are inferred.
"""
from __future__ import annotations

from . import _ops

_DEFAULT_TARGETS = (
    ("src.py.com.yun.mao.wp_jt.fi_w8_wy_n9", "wy_n9_go"),
    ("src.py.com.yun.mao.rm_qh.zb_q6_gj_x5", "df_u0_rx"),
)


def dg_09_fan() -> None:
    _gs = _ops.load_attr(
        "src.py.com.yun.mao.util.need.signals", "global_ui_signal"
    )
    _ops.emit(_gs, "cmd_probe_light_fault")
    for _mod, _name in _DEFAULT_TARGETS:
        _ops.call_entry(_mod, _name)

