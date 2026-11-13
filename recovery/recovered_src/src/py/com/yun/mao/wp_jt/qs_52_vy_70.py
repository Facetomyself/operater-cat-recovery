"""Recovered zero-argument entry ``ln_06_arm``.

Decompiled structure: a 0.92 second daemon ``threading.Timer`` that calls
``kv_nx.nq_e0_kn_b3.jm_a6_rx`` and ``bz_uc.jm_a6_kn_b3.ce_t5_go``.
"""
from __future__ import annotations

import threading

from . import _ops


def ln_06_arm() -> None:
    def _kick() -> None:
        _ops.call_entry(
            "src.py.com.yun.mao.kv_nx.nq_e0_kn_b3",
            "jm_a6_rx",
        )
        _ops.call_entry(
            "src.py.com.yun.mao.bz_uc.jm_a6_kn_b3",
            "ce_t5_go",
        )

    _T = threading.Timer(0.92, _kick)
    _T.daemon = True
    _u = _T
    _u.start()

