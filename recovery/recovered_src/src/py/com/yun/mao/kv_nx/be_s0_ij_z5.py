# Recovered module: src.py.com.yun.mao.kv_nx.be_s0_ij_z5
# Entry confirmed by module init at 0x572e520 and the terminal constants row.
from __future__ import annotations

from ..link import _fds_sj
from ..link._fds_jm import decode_str_tuple


def jm_a6_sk() -> None:
    """Show the encoded abort text, then run the two follow-up entries.

    Inferred: the exact call order follows the import/attribute order in the
    Nuitka body; the dialog timeout is the literal 1000 ms.
    """
    from src.py.com.yun.mao import ErrorDialog, GlobalExceptionHandler
    from src.py.com.yun.mao.bz_uc.gi_x9_hk_y8 import ux_l9_rx
    from src.py.com.yun.mao.rm_qh.gs_w3_df_u0 import nq_e6_go

    _show = ErrorDialog.show_error_tip
    _geh = GlobalExceptionHandler
    _w = _geh.global_window
    if _w is not None and _w.isVisible():
        _sj = decode_str_tuple(_fds_sj.ABORT_PARTS_ENC, _fds_sj.KEY)
        _dst = "\n\n".join(_sj)
        _msg = _dst
        _show(error_msg=_msg, timeout=1000)
    _ed = nq_e6_go()
    _g = ux_l9_rx()
    _r = (_ed, _g)
