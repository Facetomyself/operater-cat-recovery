"""Recovered entry ``rt_i8_sk(_show, _geh, _w, _dst, _sj, _msg, _ed, _g, _r)``.

Decompiled structure: decode ``ABORT_PARTS_ENC`` with ``KEY``, join with
``"\\n\\n"``, show ``ErrorDialog.show_error_tip(error_msg=..., timeout=1000)``,
then dispatch to the hidden ``aq_m7_ln_c2`` callable and ``eg_v7_rx``.
Dispatch argument order is inferred.
"""
from __future__ import annotations

from . import _ops


def rt_i8_sk() -> None:
    _show, _geh, _w, _dst, _sj, _msg, _ed, _g, _r = _ops.prepare_abort_dialog(
        None, None, None, None, None, None, None, None, None
    )
    _show = _ops.load_attr(
        "src.py.com.yun.mao.kv_nx.aq_m7_ln_c2",
        _ops.redacted_name("mfktlpdl"),
        _show,
    )
    _ops.call_entry(
        "src.py.com.yun.mao.wp_jt.oq_f1_bx_n2",
        "eg_v7_rx",
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
