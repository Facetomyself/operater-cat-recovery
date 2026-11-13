# Recovered module: src.py.com.yun.mao.kv_nx.hk_y8_gi_x9
# Entry confirmed by module init at 0x573e5e0 and the terminal constants row.
from __future__ import annotations

from ..link import _fds_sj
from ..link._fds_jm import decode_str_tuple


def bd_s8_sk() -> None:
    """Seal the abort state, show the encoded text, and run both follow-ups."""
    from src.py.com.yun.mao import ErrorDialog, GlobalExceptionHandler
    from src.py.com.yun.mao.link._fds_h_x import FdsHhx
    from src.py.com.yun.mao.rm_qh.eg_v7_vx_m2 import vy_m4_go
    from src.py.com.yun.mao.bz_uc import ya_p1_fh_w2 as _ya_m

    _hx = FdsHhx()
    _hx.seal_abort()
    _show = ErrorDialog.show_error_tip
    _geh = GlobalExceptionHandler
    _w = _geh.global_window
    if _w is not None and _w.isVisible():
        _sj = decode_str_tuple(_fds_sj.ABORT_PARTS_ENC, _fds_sj.KEY)
        _dst = "\n\n".join(_sj)
        _msg = _dst
        _show(error_msg=_msg, timeout=1000)
    _ed = vy_m4_go()
    _g = _ya_m.aq_m7_rx()
    _r = (_ed, _g)
