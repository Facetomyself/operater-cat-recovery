# Recovered module: src.py.com.yun.mao.cd.AsyncDequeQueueClass
from __future__ import annotations

import asyncio
import time
from collections import deque
from typing import Any, Optional


class AsyncDequeQueue:
    def __init__(self, maxsize: int = 0):
        self.maxsize = int(maxsize or 0)
        self._queue = deque()
        self._unfinished_tasks = 0
        self._finished = asyncio.Event()
        self._finished.set()
        self._mutex = asyncio.Lock()
        self._not_empty = asyncio.Condition(self._mutex)
        self._not_full = asyncio.Condition(self._mutex)
        self._closed = False

    def _check_closed(self):
        if self._closed:
            raise RuntimeError("operation on closed queue")

    def _wake_up_waiters(self):
        self._not_empty.notify_all()
        self._not_full.notify_all()

    def qsize(self) -> int:
        return len(self._queue)

    def empty(self) -> bool:
        return not self._queue

    def full(self) -> bool:
        return bool(self.maxsize and len(self._queue) >= self.maxsize)

    async def put(self, item: Any, block: bool = True, timeout: Optional[float] = None):
        self._check_closed()
        async with self._not_full:
            if not block and self.full():
                raise asyncio.QueueFull
            if block and self.full():
                end_time = time.monotonic() + timeout if timeout else None
                while self.full():
                    remaining = None if end_time is None else end_time - time.monotonic()
                    if remaining is not None and remaining <= 0:
                        raise asyncio.TimeoutError
                    try:
                        await asyncio.wait_for(self._not_full.wait(), remaining)
                    except asyncio.TimeoutError:
                        raise asyncio.TimeoutError
            self._queue.append(item)
            self._unfinished_tasks += 1
            self._finished.clear()
            self._not_empty.notify()

    def put_nowait(self, item: Any):
        self._check_closed()
        if self.full():
            raise asyncio.QueueFull
        self._queue.append(item)
        self._unfinished_tasks += 1
        self._finished.clear()

    async def get(self, block: bool = True, timeout: Optional[float] = None):
        self._check_closed()
        async with self._not_empty:
            if not block and self.empty():
                raise asyncio.QueueEmpty
            if block and self.empty():
                end_time = time.monotonic() + timeout if timeout else None
                while self.empty():
                    remaining = None if end_time is None else end_time - time.monotonic()
                    if remaining is not None and remaining <= 0:
                        raise asyncio.TimeoutError
                    try:
                        await asyncio.wait_for(self._not_empty.wait(), remaining)
                    except asyncio.TimeoutError:
                        raise asyncio.TimeoutError
            item = self._queue.popleft()
            self._not_full.notify()
            return item

    def get_nowait(self):
        self._check_closed()
        if self.empty():
            raise asyncio.QueueEmpty
        return self._queue.popleft()

    def task_done(self):
        if self._unfinished_tasks <= 0:
            raise ValueError("task_done() called too many times")
        self._unfinished_tasks -= 1
        if self._unfinished_tasks == 0:
            self._finished.set()

    async def join(self):
        await self._finished.wait()

    def close(self):
        self._closed = True
