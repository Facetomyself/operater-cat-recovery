# Recovered module: src.py.com.yun.mao.bz_uc.km_74_qs_60
# Delayed two-step dispatch. The arguments are retained because the recovered
# entry signature is two-positional; the decompiled callback does not consume
# them.
from __future__ import annotations

import importlib
import threading


def km_23_arm() -> None:
    def _cb() -> None:
        _mod = importlib.import_module(
            "src.py.com.yun.mao.kv_nx.zc_q2_or_f7"
        )
        getattr(_mod, "lo_c4_rx")()

        _mod = importlib.import_module(
            "src.py.com.yun.mao.bz_uc.nq_e0_wz_n5"
        )
        _mod.eh_v3_go()

    _th = threading.Timer(1.0, _cb)
    _th.daemon = True
    _th.start()
