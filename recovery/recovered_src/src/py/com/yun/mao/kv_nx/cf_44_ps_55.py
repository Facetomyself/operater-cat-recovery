# Recovered module: src.py.com.yun.mao.kv_nx.cf_44_ps_55
# Entry confirmed by module init at 0x5731ce0 and the terminal constants row.
from __future__ import annotations


def pr_40_fan() -> None:
    """Emit the socket-environment rejection and invoke the registered hooks.

    The signal fires before the two encoded (module, name) pairs.
    """
    from src.py.com.yun.mao.util.need.signals import global_ui_signal

    _sig = global_ui_signal.cmd_socket_env_reject
    _sig.emit()
    for _mod, _name in (
        ("src.py.com.yun.mao.wp_jt.ru_i0_gj_x5", "ac_r3_go"),
        ("src.py.com.yun.mao.rm_qh.jm_a2_sv_j7", "hj_y4_rx"),
    ):
        _m = __import__(_mod, fromlist=(_name,))
        getattr(_m, _name)()
