"""Recovered zero-argument entry ``ac_r3_sk``.

Decompiled structure: shared abort-message decode/show path followed by
``bz_uc.dv_r4_uw_l7.sv_j1_go`` and the hidden
``kv_nx.xz_o4_eu_s1`` callback.
"""
from __future__ import annotations

from . import _ops


def ac_r3_sk() -> None:
    _show = _ops.load_attr("src.py.com.yun.mao", "GlobalExceptionHandler")
    _geh = _show
    _w = getattr(_geh, "global_window", None) if _geh is not None else None
    _dst = _ops.decode_abort_parts()
    _sj = _ops.load_attr("src.py.com.yun.mao.link", "_fds_sj")
    _msg = "\n\n".join(_dst)
    _ed = _ops.load_attr("src.py.com.yun.mao.ErrorDialog", "show_error_tip")
    if (
        _w is not None
        and getattr(_w, "isVisible", lambda: False)()
        and _ed is not None
    ):
        try:
            _ed(error_msg=_msg, timeout=1000)
        except TypeError:
            _ed(_msg, 1000)

    _g = _ops.load_attr(
        "src.py.com.yun.mao.bz_uc.dv_r4_uw_l7",
        "sv_j1_go",
    )
    _r = _ops.load_attr(
        "src.py.com.yun.mao.kv_nx.xz_o4_eu_s1",
        "zc_q2_rx",
    )
    if _g is not None:
        _g()
    if _r is not None:
        _r()
