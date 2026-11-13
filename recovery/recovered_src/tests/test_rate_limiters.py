from __future__ import annotations

from src.py.com.yun.mao.telefast.RateLimiterClass import (
    DownRateLimiter,
    RateLimiter,
    UpRateLimiter,
)
from src.py.com.yun.mao.telefast.RateTempClass import RateTempClass
from src.py.com.yun.mao.telefast.CallBack import convert_bytes
from src.py.com.yun.mao.telefast import RateLimiterHelper


def setup_function():
    RateLimiter._instance = None
    UpRateLimiter._instance = None
    DownRateLimiter._instance = None


def test_rate_limiter_is_singleton_and_configures_interval():
    first = RateLimiter(10)
    second = RateLimiter(20)

    assert first is second
    assert first.rate_limit == 10
    assert first.interval == 0.1


def test_subclasses_have_independent_singletons():
    assert UpRateLimiter(4) is UpRateLimiter(8)
    assert DownRateLimiter(4) is DownRateLimiter(8)
    assert UpRateLimiter(4) is not DownRateLimiter(4)


def test_rate_temp_class_init_rate():
    RateTempClass.init_rate(7, 3)
    assert RateTempClass.down_load_rate == 7
    assert RateTempClass.up_load_rate == 3


def test_convert_bytes_units():
    assert convert_bytes(0) == "0.0 B"
    assert convert_bytes(1536) == "1.5 KB"
    assert convert_bytes(1024 * 1024) == "1.0 MB"


def test_flood_descend_rate_floor():
    RateTempClass.init_rate(20, 3)
    assert RateLimiterHelper.flood_descend_rate() == (5, 3)
    RateTempClass.init_rate(4, 15)
    assert RateLimiterHelper.flood_descend_rate() == (4, 5)


def test_auto_current_rate_tiers(monkeypatch):
    monkeypatch.setattr(RateLimiterHelper, "read_last_flood_time", lambda: 0)
    assert RateLimiterHelper.get_auto_current_rate() == (1, 1)

    now = 1_700_000_000
    monkeypatch.setattr(RateLimiterHelper.time, "time", lambda: now)
    monkeypatch.setattr(
        RateLimiterHelper,
        "read_last_flood_time",
        lambda: now - 10 * 3600,
    )
    assert RateLimiterHelper.get_auto_current_rate() == (3, 2)
    monkeypatch.setattr(
        RateLimiterHelper,
        "read_last_flood_time",
        lambda: now - 100 * 3600,
    )
    assert RateLimiterHelper.get_auto_current_rate() == (20, 20)


def test_is_auto_rate_reads_cache(monkeypatch):
    class _Cache:
        def read_cache(self, *args):
            return "True"

    monkeypatch.setattr(RateLimiterHelper, "_cache", lambda: _Cache())
    assert RateLimiterHelper.is_auto_rate() is True
