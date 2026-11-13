# Recovered module: src.py.com.yun.mao.kv_nx.dv_r4_uw_l7
# Entry confirmed by module init at 0x5733fa0 and the terminal constants row.
from __future__ import annotations

from ..link import _fds_sj
from ..link._fds_jm import decode_str_tuple


def tw_k2_sk() -> None:
    """Show the encoded abort text, then run the two follow-up entries.

    Inferred: the exact call order follows the import/attribute order in the
    Nuitka body; the dialog timeout is the literal 1000 ms.
    """
    from src.py.com.yun.mao import ErrorDialog, GlobalExceptionHandler
    from src.py.com.yun.mao.bz_uc.qt_h5_tv_k0 import yb_p3_rx
    from src.py.com.yun.mao.rm_qh.su_j5_nq_e6 import ru_i0_go

    _show = ErrorDialog.show_error_tip
    _geh = GlobalExceptionHandler
    _w = _geh.global_window
    if _w is not None and _w.isVisible():
        _sj = decode_str_tuple(_fds_sj.ABORT_PARTS_ENC, _fds_sj.KEY)
        _dst = "\n\n".join(_sj)
        _msg = _dst
        _show(error_msg=_msg, timeout=1000)
    _ed = ru_i0_go()
    _g = yb_p3_rx()
    _r = (_ed, _g)
