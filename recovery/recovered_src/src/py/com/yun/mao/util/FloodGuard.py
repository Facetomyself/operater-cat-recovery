# Recovered module: src.py.com.yun.mao.util.FloodGuard
# Telegram flood-wait handling reconstructed from the constants, the embedded
# user-facing text, and the module init function names.
from __future__ import annotations

import asyncio
import functools
import time
from datetime import datetime, timedelta

from . import SuspendFrozenTag

try:
    from telethon.errors import FloodWaitError, SlowModeWaitError
except Exception:
    class FloodWaitError(Exception):
        seconds = 0

    class SlowModeWaitError(FloodWaitError):
        pass


def _rate_helper():
    from ..telefast import RateLimiterHelper

    return RateLimiterHelper


def _duration_text(seconds: int) -> str:
    seconds = max(0, int(seconds or 0))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    parts = []
    if hours:
        parts.append(f"{hours}小时")
    if minutes:
        parts.append(f"{minutes}分钟")
    parts.append(f"{secs}秒")
    return "".join(parts)


def flood_log_text(e, prefix: str = "") -> str:
    """Build the user-facing flood-wait message."""

    seconds = max(0, int(getattr(e, "seconds", 0) or 0))
    now = datetime.now()
    release_time = now + timedelta(seconds=seconds)
    error_type = "慢速模式限制" if isinstance(e, SlowModeWaitError) else "洪水泛滥限制"
    tag = f"[{prefix}] " if prefix else ""
    text = (
        f"{tag}很抱歉，你触发了 Telegram 的{error_type}，程序自动等待 "
        f"{seconds} 秒（大概在 {release_time.strftime('%Y-%m-%d %H:%M:%S')}）"
        "自动恢复。"
    )
    SuspendFrozenTag.flood_log_text = text
    return text


async def handle_flood_wait(e, prefix: str = "") -> int:
    seconds = max(0, int(getattr(e, "seconds", 0) or 0))
    print(flood_log_text(e, prefix))
    try:
        RateLimiterHelper = _rate_helper()
        RateLimiterHelper.mark_flood_time()
        if RateLimiterHelper.is_auto_rate():
            down_rate, up_rate = RateLimiterHelper.flood_descend_rate()
            RateLimiterHelper.changed_rate(down_rate, up_rate)
            RateLimiterHelper.flood_descend_rate_event(
                seconds / 3600.0,
                {"down_rate": down_rate, "up_rate": up_rate},
            )
            RateLimiterHelper.auto_masu_rate_event((down_rate, up_rate))
    except Exception:
        pass
    try:
        SuspendFrozenTag.print_last_log_if_need()
    except Exception:
        pass
    await asyncio.sleep(seconds)
    return seconds


def clean_flood_log() -> None:
    """Clear the pending flood log after a successful retry."""

    SuspendFrozenTag.flood_log_text = ""
    _ = time.time()


async def handle_other_ex(e, prefix: str = "") -> None:
    tag = f"[{prefix}] " if prefix else ""
    print(f"{tag}异常: {e!r}")


async def with_flood_retry(
    coro_func,
    max_retries: int = 3,
    prefix: str = "",
):
    """Execute ``coro_func`` and retry only Telegram flood errors."""

    max_retries = max(1, int(max_retries or 1))
    for attempt in range(max_retries):
        try:
            result = coro_func()
            if asyncio.iscoroutine(result):
                result = await result
            return result
        except (FloodWaitError, SlowModeWaitError) as exc:
            if attempt + 1 >= max_retries:
                await handle_other_ex(exc, prefix)
                raise
            await handle_flood_wait(exc, prefix)
        except Exception as exc:
            await handle_other_ex(exc, prefix)
            raise
    return None


def flood_guard(max_retries: int = 3, prefix: str = ""):
    """Decorator form of :func:`with_flood_retry`."""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async def invoke():
                return await func(*args, **kwargs)

            return await with_flood_retry(
                invoke,
                max_retries=max_retries,
                prefix=prefix,
            )

        return wrapper

    return decorator
