from __future__ import annotations

import asyncio

import pytest

from src.py.com.yun.mao.cd.AsyncDequeQueueClass import AsyncDequeQueue


def test_fifo_and_capacity():
    queue = AsyncDequeQueue(maxsize=2)
    queue.put_nowait("a")
    queue.put_nowait("b")
    assert queue.qsize() == 2
    assert queue.full()
    with pytest.raises(asyncio.QueueFull):
        queue.put_nowait("c")
    assert queue.get_nowait() == "a"
    assert queue.get_nowait() == "b"
    assert queue.empty()


def test_task_done_and_join():
    async def scenario():
        queue = AsyncDequeQueue()
        await queue.put("x")
        assert await queue.get() == "x"
        queue.task_done()
        await queue.join()

    asyncio.run(scenario())


def test_task_done_underflow():
    queue = AsyncDequeQueue()
    with pytest.raises(ValueError):
        queue.task_done()


def test_closed_queue_rejects_operations():
    queue = AsyncDequeQueue()
    queue.close()
    with pytest.raises(RuntimeError):
        queue.put_nowait("x")
    with pytest.raises(RuntimeError):
        queue.get_nowait()


def test_get_timeout():
    async def scenario():
        queue = AsyncDequeQueue()
        with pytest.raises(asyncio.TimeoutError):
            await queue.get(timeout=0.01)

    asyncio.run(scenario())
