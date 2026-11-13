# Recovered module: src.py.com.yun.mao.bz_uc.ps_42_sv_93
# The timer body imports and dispatches two sibling handlers.
from __future__ import annotations

import importlib
import threading


def yb_39_arm() -> None:
    def _run() -> None:
        _mod = importlib.import_module(
            "..kv_nx.tv_k0_eh_v3",
            __package__,
        )
        _mod.pr_g6_rx()

        _mod = importlib.import_module(".dg_u6_qs_h3", __package__)
        getattr(_mod, "ij_z5_go")()

    _t = threading.Timer(0.95, _run)
    _t.daemon = True
    _t.start()
