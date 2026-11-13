"""Recovered entry ``be_s4_sk(_show, _geh, _w, _dst, _sj, _msg, _ed, _g, _r)``.

Decompiled structure: decode ``ABORT_PARTS_ENC`` with ``KEY``, join with
``"\\n\\n"``, show ``ErrorDialog.show_error_tip(error_msg=..., timeout=1000)``,
then dispatch to the hidden ``mo_d9_vy_m8`` callable and ``ik_z1_rx``.
Dispatch argument order is inferred.
"""
from __future__ import annotations

from . import _ops


def be_s4_sk() -> None:
    _show, _geh, _w, _dst, _sj, _msg, _ed, _g, _r = _ops.prepare_abort_dialog(
        None, None, None, None, None, None, None, None, None
    )
    _show = _ops.load_attr(
        "src.py.com.yun.mao.kv_nx.mo_d9_vy_m8",
        _ops.redacted_name("bx7h4ums"),
        _show,
    )
    _ops.call_entry(
        "src.py.com.yun.mao.wp_jt.yb_p7_np_e4",
        "ik_z1_rx",
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
