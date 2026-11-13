from __future__ import annotations

import asyncio
import threading
import time
import types

from src.py.com.yun.mao.cd import TaskHardStop
from src.py.com.yun.mao.login import ClientCacheHelper


def test_teardown_worker_loop_excludes_current_task(monkeypatch):
    monkeypatch.setattr(
        ClientCacheHelper,
        "safe_disconnect_client",
        lambda: None,
        raising=False,
    )
    loop = asyncio.new_event_loop()

    async def scenario():
        pending = asyncio.create_task(asyncio.sleep(60))
        await TaskHardStop._teardown_worker_loop(loop)
        assert pending.cancelled()

    try:
        loop.run_until_complete(scenario())
    finally:
        loop.close()


def test_schedule_worker_teardown_runs_done_callback(monkeypatch):
    finished = []

    async def disconnect():
        return None

    monkeypatch.setattr(
        ClientCacheHelper,
        "safe_disconnect_client",
        disconnect,
        raising=False,
    )
    monkeypatch.setattr(
        TaskHardStop,
        "_post_to_main_thread",
        lambda callback: callback() or True,
    )
    loop = asyncio.new_event_loop()
    worker = types.SimpleNamespace(loop=loop)
    thread = threading.Thread(target=loop.run_forever, daemon=True)
    thread.start()

    TaskHardStop.schedule_worker_teardown(
        worker,
        lambda: finished.append(True),
    )
    try:
        deadline = time.time() + 1.0
        while not finished and time.time() < deadline:
            time.sleep(0.01)
    finally:
        loop.call_soon_threadsafe(loop.stop)
        thread.join(timeout=1.0)
        loop.close()

    assert finished == [True]
