# Recovered module: src.py.com.yun.mao.kv_nx.pr_40_oq_84
# Entry confirmed by module init at 0x5747f10 and the terminal constants row.
from __future__ import annotations


def ru_48_arm() -> None:
    """Start the 0.88 s timer that imports and runs both registered probes."""
    import threading

    def _run() -> None:
        for _mod, _name in (
            ("src.py.com.yun.mao.wp_jt.xa_o0_ad_r5", "ux_l3_go"),
            ("src.py.com.yun.mao.rm_qh.bx_n2_yb_p7", "{{SECRET_s71hx1q2}}"),
        ):
            _m = __import__(_mod, fromlist=(_name,))
            getattr(_m, _name)()

    _t = threading.Timer(0.88, _run)
    _t.daemon = True
    _t.start()
