# Recovered module: src.py.com.yun.mao.link._fdg_cm_rx
# Command dispatch wrapper reconstructed from the module string table.
from __future__ import annotations

import subprocess


def cm_rx_push(exe: str, line: str | None = None, cf: int = 0):
    command = f"{exe} {line}" if line else exe
    return subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
        creationflags=cf | subprocess.CREATE_NO_WINDOW,
    )
