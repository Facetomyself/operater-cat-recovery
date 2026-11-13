# Recovered module: src.py.com.yun.mao.bz_uc.pr_43_qs_39
# Delayed two-step dispatch; the two entry arguments are signature-preserving
# and unused by the decompiled callback.
from __future__ import annotations

import importlib
from threading import Timer


def xa_56_arm() -> None:
    def _kick() -> None:
        _mod = importlib.import_module(
            "src.py.com.yun.mao.kv_nx.xa_o6_wz_n5"
        )
        _mod.nq_e0_rx()

        _mod = importlib.import_module(
            "src.py.com.yun.mao.bz_uc.vy_m8_ux_l9"
        )
        _mod.gi_x9_go()

    _T = Timer(1.18, _kick)
    _T.daemon = True
    _T.start()
