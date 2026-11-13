# Recovered module: src.py.com.yun.mao.bz_uc.uw_l7_ln_c2
# Abort-message assembly and hidden error tip path.
from __future__ import annotations


def sv_j1_sk() -> None:
    from .. import GlobalExceptionHandler
    from ..ErrorDialog import show_error_tip
    from ..link import _fds_sj
    from ..link._fds_jm import decode_str_tuple
    from ..rm_qh.ps_g2_km_b7 import np_e4_rx
    from ..wp_jt.jl_a0_mp_d5 import gs_w3_go

    _geh = GlobalExceptionHandler
    _w = _geh.global_window
    _dst = decode_str_tuple(_fds_sj.ABORT_PARTS_ENC, _fds_sj.KEY)
    _msg = "\n\n".join(_dst)
    _ed = show_error_tip
    if _w is not None and _w.isVisible():
        _ed(error_msg=_msg, timeout=1000)

    _g = gs_w3_go
    _r = np_e4_rx
    _g()
    _r()
