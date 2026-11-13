# Recovered module: src.py.com.yun.mao.bz_uc.aq_22_rt_78
# The entry emits the crypto-context fault signal and fans out to the two
# catalog handlers in source order.
from __future__ import annotations

import importlib


def yb_25_fan() -> None:
    from ..util.need.signals import global_ui_signal

    global_ui_signal.notify_crypto_ctx_broken.emit()
    for _name, _m in (
        ("src.py.com.yun.mao.bz_uc.xa_o6_yb_p3", "qt_h5_go"),
        ("src.py.com.yun.mao.kv_nx.be_s0_yb_p3", "xa_o6_rx"),
    ):
        _mod = importlib.import_module(_name)
        getattr(_mod, _m)()
