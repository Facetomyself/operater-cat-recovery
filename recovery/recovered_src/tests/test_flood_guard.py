from __future__ import annotations

import asyncio

import pytest

from src.py.com.yun.mao.util import FloodGuard, SuspendFrozenTag


def test_duration_text():
    assert FloodGuard._duration_text(0) == "0秒"
    assert FloodGuard._duration_text(3661) == "1小时1分钟1秒"
    assert FloodGuard._duration_text(-5) == "0秒"


def test_flood_log_text_sets_pending_message():
    error = FloodGuard.FloodWaitError()
    error.seconds = 5
    text = FloodGuard.flood_log_text(error, "prefix")
    assert "洪水泛滥限制" in text
    assert "[prefix]" in text
    assert "5 秒" in text
    assert SuspendFrozenTag.flood_log_text == text


def test_with_flood_retry_retries_once(monkeypatch):
    calls = []

    async def fake_handle(error, prefix=""):
        calls.append((error, prefix))

    monkeypatch.setattr(FloodGuard, "handle_flood_wait", fake_handle)
    attempts = {"count": 0}

    async def operation():
        attempts["count"] += 1
        if attempts["count"] == 1:
            error = FloodGuard.FloodWaitError()
            error.seconds = 0
            raise error
        return "ok"

    result = asyncio.run(FloodGuard.with_flood_retry(operation, max_retries=2))
    assert result == "ok"
    assert len(calls) == 1
    assert attempts["count"] == 2


def test_with_flood_retry_reraises_non_flood(monkeypatch):
    async def fake_other(error, prefix=""):
        return None

    monkeypatch.setattr(FloodGuard, "handle_other_ex", fake_other)

    async def operation():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        asyncio.run(FloodGuard.with_flood_retry(operation))


def test_flood_guard_decorator(monkeypatch):
    async def fake_handle(error, prefix=""):
        return None

    monkeypatch.setattr(FloodGuard, "handle_flood_wait", fake_handle)
    attempts = {"count": 0}

    @FloodGuard.flood_guard(max_retries=2)
    async def operation():
        attempts["count"] += 1
        if attempts["count"] == 1:
            error = FloodGuard.FloodWaitError()
            error.seconds = 0
            raise error
        return 7

    assert asyncio.run(operation()) == 7
    assert attempts["count"] == 2
