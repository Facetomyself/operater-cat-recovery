"""Recovered entry ``nq_89_arm(_mod, _name, _m)``.

Decompiled structure: a 0.97 second ``threading.Timer`` that imports the
``(module, name)`` targets and invokes them.  The default target tuple is
present verbatim in the module constants.
Callback invocation order is inferred.
"""
from __future__ import annotations

import threading

from . import _ops

_DEFAULT_TARGETS = (
    ("src.py.com.yun.mao.wp_jt.lo_c8_qt_h9", "qt_h9_go"),
    ("src.py.com.yun.mao.rm_qh.tw_k6_mp_d5", "xa_o0_rx"),
)


def nq_89_arm() -> None:
    def _run() -> None:
        for _mod, _name in _DEFAULT_TARGETS:
            _ops.call_entry(_mod, _name)

    _t = threading.Timer(0.97, _run)
    _t.daemon = True
    _t.start()

