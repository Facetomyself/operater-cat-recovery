"""Recovered zero-argument entry ``su_j5_sk``.

Decompiled structure: ``FdsHhx.seal_abort()``, the shared abort-message
decode/show path, then ``bz_uc.bd_s8_mo_d9.ad_r9_go`` and
``kv_nx.pr_g6_ce_t5.hk_y0_rx``.
"""
from __future__ import annotations

from . import _ops


def su_j5_sk() -> None:
    _hx = _ops.load_attr("src.py.com.yun.mao.link._fds_h_x", "FdsHhx")
    if isinstance(_hx, type):
        try:
            _hx = _hx()
        except (TypeError, ValueError, RuntimeError, OSError):
            _hx = None
    _ops.call_method(_hx, "seal_abort")

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
        "src.py.com.yun.mao.bz_uc.bd_s8_mo_d9",
        "ad_r9_go",
    )
    _r = _ops.load_attr(
        "src.py.com.yun.mao.kv_nx.pr_g6_ce_t5",
        "hk_y0_rx",
    )
    if _g is not None:
        _g()
    if _r is not None:
        _r()
