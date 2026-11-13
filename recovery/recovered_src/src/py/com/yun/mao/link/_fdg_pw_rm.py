# Recovered module: src.py.com.yun.mao.link._fdg_pw_rm
# Command execution wrapper reconstructed from the module string table.
from __future__ import annotations

import subprocess



def pw_rm_fire(exe: str, args: list[str] | None = None, cf: int = 0):
    """Start a hidden child process.

    The binary uses CREATE_NO_WINDOW, DEVNULL pipes and a shell-capable
    Popen call. This wrapper keeps the same observable contract.
    """
    command = [exe, *(args or [])]
    return subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=isinstance(exe, str),
        creationflags=cf | subprocess.CREATE_NO_WINDOW,
    )
