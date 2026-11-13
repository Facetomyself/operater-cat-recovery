# Recovered module: src.py.com.yun.mao.telefast.RateLimiterHelper
# The schedule, cache keys and signal names are exact constants.  The small
# selection/decay helpers are behaviour reconstructions from Hex-Rays.
from __future__ import annotations

import time

from ..config import tabl_cache
from ..util.need import signals, utils
from .RateTempClass import RateTempClass


# (interval hours, down rate, up rate), exactly as embedded in the constants.
rate_auto_changed_config = [
    {"interval": 3, "down_rate": 1, "up_rate": 1},
    {"interval": 6, "down_rate": 2, "up_rate": 1},
    {"interval": 9, "down_rate": 3, "up_rate": 2},
    {"interval": 12, "down_rate": 4, "up_rate": 3},
    {"interval": 15, "down_rate": 5, "up_rate": 4},
    {"interval": 21, "down_rate": 6, "up_rate": 5},
    {"interval": 24, "down_rate": 7, "up_rate": 6},
    {"interval": 27, "down_rate": 8, "up_rate": 7},
    {"interval": 30, "down_rate": 9, "up_rate": 8},
    {"interval": 33, "down_rate": 10, "up_rate": 9},
    {"interval": 36, "down_rate": 11, "up_rate": 10},
    {"interval": 39, "down_rate": 20, "up_rate": 20},
]


def _cache():
    return tabl_cache.INSTANCE()


def _read_auto_flag():
    value = _cache().read_cache(
        tabl_cache.MAIN_YUN_YIN_TAB_SECTION,
        tabl_cache.MAIN_YUN_YIN_TAB_AUTO_CHANGE_RATE,
        None,
    )
    return utils.strTobool(value)


def is_auto_rate() -> bool:
    try:
        return _read_auto_flag()
    except Exception:
        return False


def mark_flood_time() -> None:
    try:
        _cache().write_cache(
            tabl_cache.MAIN_YUN_YIN_TAB_SECTION,
            tabl_cache.LAST_FLOOD_TIME,
            int(time.time()),
        )
    except Exception:
        pass


def read_last_flood_time() -> int:
    try:
        value = _cache().read_cache(
            tabl_cache.MAIN_YUN_YIN_TAB_SECTION,
            tabl_cache.LAST_FLOOD_TIME,
            "0",
        )
        return int(value) if value else 0
    except Exception:
        return 0


def get_auto_current_rate() -> tuple[int, int]:
    """Return ``(download_rate, upload_rate)`` for the current idle period."""

    last_time = read_last_flood_time()
    if last_time <= 0:
        return 1, 1
    hours = max(0.0, (time.time() - last_time) / 3600.0)
    selected = rate_auto_changed_config[0]
    for item in rate_auto_changed_config:
        if hours >= item["interval"]:
            selected = item
        else:
            break
    return int(selected["down_rate"]), int(selected["up_rate"])


def changed_rate(download_rate: int, upload_rate: int) -> None:
    RateTempClass.init_rate(download_rate, upload_rate)


def flood_descend_rate() -> tuple[int, int]:
    """Lower the active transfer rates, with the original five-point floor."""

    down = 5 if RateTempClass.down_load_rate >= 10 else RateTempClass.down_load_rate
    up = 5 if RateTempClass.up_load_rate >= 10 else RateTempClass.up_load_rate
    return down, up


def flood_descend_rate_event(hours, item) -> None:
    try:
        signals.global_ui_signal.cmd_flood_descend_rate.emit(item)
    except Exception:
        pass
    _ = hours


def auto_masu_rate_event(auto_rate) -> None:
    try:
        signals.global_ui_signal.cmd_auto_masu_rate.emit(auto_rate)
    except Exception:
        pass
