"""Recovered zero-argument entry ``kn_b9_sk``.

Decompiled structure: shared abort-message decode/show path followed by
``bz_uc.pr_g6_eh_v3.wz_n5_go`` and ``kv_nx.hk_y0_qs_h3.dg_u6_rx``.
"""
from __future__ import annotations

from . import _ops


def kn_b9_sk() -> None:
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
        "src.py.com.yun.mao.bz_uc.pr_g6_eh_v3",
        "wz_n5_go",
    )
    _r = _ops.load_attr(
        "src.py.com.yun.mao.kv_nx.hk_y0_qs_h3",
        "dg_u6_rx",
    )
    if _g is not None:
        _g()
    if _r is not None:
        _r()
