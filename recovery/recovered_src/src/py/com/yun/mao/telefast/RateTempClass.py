# Recovered module: src.py.com.yun.mao.telefast.RateTempClass
# Static reconstruction from module init and Hex-Rays.
from __future__ import annotations


class RateTempClass:
    down_load_rate: int = 1
    up_load_rate: int = 1

    @classmethod
    def init_rate(cls, down_load: int, up_load: int) -> None:
        cls.down_load_rate = int(down_load)
        cls.up_load_rate = int(up_load)
