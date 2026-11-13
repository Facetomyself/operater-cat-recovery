"""Recovered entry ``jl_a0_sk(_hx, _show, _geh, _w, _dst, _sj, _msg, _ed, _g, _r)``.

Decompiled structure: ``FdsHhx.seal_abort()``, the shared abort dialog
prefix, then dispatch to the hidden ``ya_p1_dv_r4`` callable and
``mp_d5_rx``.
Dispatch argument order and instance creation are inferred.
"""
from __future__ import annotations

from . import _ops


def jl_a0_sk() -> None:
    _hx = _ops.load_attr(
        "src.py.com.yun.mao.link._fds_h_x", "FdsHhx"
    )
    if isinstance(_hx, type):
        try:
            _hx = _hx()
        except Exception:
            _hx = None
    _ops.call_method(_hx, "seal_abort")
    _show, _geh, _w, _dst, _sj, _msg, _ed, _g, _r = _ops.prepare_abort_dialog(
        None, None, None, None, None, None, None, None, None
    )
    _show = _ops.load_attr(
        "src.py.com.yun.mao.kv_nx.ya_p1_dv_r4",
        _ops.redacted_name("6kjn5j2v"),
        _show,
    )
    _ops.call_entry(
        "src.py.com.yun.mao.wp_jt.gs_w3_zb_q6",
        "mp_d5_rx",
        _hx,
        _show,
        _geh,
        _w,
        _dst,
        _sj,
        _msg,
        _ed,
        _g,
        _r,
    )
