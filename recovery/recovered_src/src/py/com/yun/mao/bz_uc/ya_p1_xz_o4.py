# Recovered module: src.py.com.yun.mao.bz_uc.ya_p1_xz_o4
# Seal-abort plus the same hidden abort-message path.
from __future__ import annotations


def aq_m7_sk() -> None:
    from .. import GlobalExceptionHandler
    from ..ErrorDialog import show_error_tip
    from ..link import _fds_sj
    from ..link._fds_h_x import FdsHhx
    from ..link._fds_jm import decode_str_tuple
    from ..rm_qh.zc_q8_wy_n9 import rt_i8_rx
    from ..wp_jt.vx_m2_wz_n1 import km_b7_go

    _hx = FdsHhx()
    _hx.seal_abort()

    _geh = GlobalExceptionHandler
    _w = _geh.global_window
    _dst = decode_str_tuple(_fds_sj.ABORT_PARTS_ENC, _fds_sj.KEY)
    _msg = "\n\n".join(_dst)
    _ed = show_error_tip
    if _w is not None and _w.isVisible():
        _ed(error_msg=_msg, timeout=1000)

    _g = km_b7_go
    _r = rt_i8_rx
    _g()
    _r()
