# Recovered module: src.py.com.yun.mao.jm._my_dt
from __future__ import annotations

import os


def jm_sc_aes_k() -> bytes:
    """Generate the per-request 16-byte AES key."""
    return os.urandom(16)
