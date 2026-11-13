# Recovered module: src.py.com.yun.mao.telefast.CallBack
# Progress/formatting helpers from the module constants and Hex-Rays control
# flow.  The exact bar text is confirmed by the embedded literals.
from __future__ import annotations

import time

from ..util.need import CommonCode


INTERVAL_LOG_TIME = 0.8
_UNITS = ("B", "KB", "MB", "GB", "TB")

upload_start_time = 0.0
upload_last_time = 0.0
up_start_time = 0.0
up_last_time = 0.0
water_start_time = 0.0
water_last_time = 0.0
preview_start_time = 0.0
preview_last_time = 0.0
down_start_time = 0.0
down_last_time = 0.0


def convert_bytes(size, x=0):
    """Convert a byte count to a human-readable unit string."""

    value = float(size or 0)
    index = max(0, min(int(x or 0), len(_UNITS) - 1))
    while value >= 1024 and index < len(_UNITS) - 1:
        value /= 1024.0
        index += 1
    return f"{value:.1f} {_UNITS[index]}"


def _bar(percent: float, width: int = 20) -> str:
    percent = max(0.0, min(100.0, float(percent or 0)))
    filled = int(round(width * percent / 100.0))
    return "#" * filled + "=" * (width - filled)


def _speed(current, total, new_time, execution_time) -> tuple[float, str]:
    current = max(0, int(current or 0))
    total = max(0, int(total or 0))
    percent = (current * 100.0 / total) if total else 0.0
    elapsed = float(execution_time or 0)
    speed = current / elapsed if elapsed > 0 else 0.0
    return percent, f"{convert_bytes(speed)}/s"


def upload_progress_bar(
    current,
    total,
    new_time=None,
    execution_time=0.0,
) -> None:
    global upload_last_time
    now = time.time() if new_time is None else float(new_time)
    percent, speed = _speed(current, total, now, execution_time)
    if now - upload_last_time < INTERVAL_LOG_TIME and percent < 100:
        return
    upload_last_time = now
    print(
        f"{percent:5.1f}% [{_bar(percent)}] "
        f"{convert_bytes(current)} / {convert_bytes(total)} "
        f"{speed} 正在上传 "
    )


def reset_water_progress() -> None:
    global water_start_time, water_last_time
    water_start_time = time.time()
    water_last_time = water_start_time


def water_progress_bar(
    current_sec,
    total_sec,
    new_time=None,
    execution_time=0.0,
    pct_raw=None,
    **kwargs,
) -> None:
    global water_last_time
    now = time.time() if new_time is None else float(new_time)
    water_last_time = now
    total = max(0.0, float(total_sec or 0))
    current = max(0.0, float(current_sec or 0))
    percent = float(pct_raw) if pct_raw is not None else (current * 100.0 / total if total else 0.0)
    print(
        f"{percent:5.1f}% [{_bar(percent)}]"
        "   正在绘制水印 "
        f"{CommonCode.format_time(int(current))} / "
        f"{CommonCode.format_time(int(total))}"
        f" 耗时： {CommonCode.format_time(int(execution_time))}"
    )


def water_progress_bar_done(total_sec=0, execution_time=0.0, msg_str="") -> None:
    global water_last_time
    water_last_time = time.time()
    print(
        "100% [********************]"
        "   正在绘制水印 "
        f"{CommonCode.format_time(int(total_sec))}"
        f" 耗时： {CommonCode.format_time(int(execution_time))}"
        f"{msg_str or ''}"
    )


def reset_preview_progress() -> None:
    global preview_start_time, preview_last_time
    preview_start_time = time.time()
    preview_last_time = preview_start_time


def preview_progress_bar(
    current_sec,
    total_sec,
    new_time=None,
    execution_time=0.0,
    pct_raw=None,
    **kwargs,
) -> None:
    global preview_last_time
    now = time.time() if new_time is None else float(new_time)
    preview_last_time = now
    total = max(0.0, float(total_sec or 0))
    current = max(0.0, float(current_sec or 0))
    percent = float(pct_raw) if pct_raw is not None else (current * 100.0 / total if total else 0.0)
    print(
        f"{percent:5.1f}% [{_bar(percent)}]"
        "   正在生成预览视频 "
        f"{CommonCode.format_time(int(current))} / "
        f"{CommonCode.format_time(int(total))}"
        f" 耗时： {CommonCode.format_time(int(execution_time))}"
    )


def preview_progress_bar_done(total_sec=0, execution_time=0.0, msg_str="") -> None:
    global preview_last_time
    preview_last_time = time.time()
    print(
        "100% [********************]"
        "   正在生成预览视频 "
        f"{CommonCode.format_time(int(total_sec))}"
        f" 耗时： {CommonCode.format_time(int(execution_time))}"
        f"{msg_str or ''}"
    )


def down_progress_bar(
    current,
    total,
    new_time=None,
    execution_time=0.0,
) -> None:
    global down_last_time
    now = time.time() if new_time is None else float(new_time)
    percent, speed = _speed(current, total, now, execution_time)
    if now - down_last_time < INTERVAL_LOG_TIME and percent < 100:
        return
    down_last_time = now
    print(
        f"{percent:5.1f}% [{_bar(percent)}] "
        f"{speed} 下载了 {convert_bytes(current)} / {convert_bytes(total)}"
    )
