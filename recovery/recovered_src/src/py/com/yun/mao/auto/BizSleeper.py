# Recovered module: src.py.com.yun.mao.auto.BizSleeper
# The async function and its local names are confirmed by the module code
# metadata; the body follows the init constant order and the nested coroutine
# control flow.
from __future__ import annotations

import asyncio
import random

from src.py.com.yun.mao.util import SuspendFrozenTag


async def biz_sleep(min_sec: int, max_sec: int):
    """Sleep for a random business delay.

    The debug line, frozen-state log flush, and random interval are all present
    in the embedded constants.  ``asyncio.sleep`` is the final await.
    """

    sleep_time = random.randint(int(min_sec), int(max_sec))
    print(f"debug 安全因素，需要等待 {sleep_time} 秒")
    SuspendFrozenTag.print_last_log_if_need()
    await asyncio.sleep(sleep_time)
