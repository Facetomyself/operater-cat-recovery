from __future__ import annotations

import asyncio
import types

import pytest

from src.py.com.yun.mao.ai import TextCache, TextProcessLogic
from src.py.com.yun.mao.ai.AiTextGenFlow import AiTextGenFlow
from src.py.com.yun.mao.ai.AiTextGenStatus import AiTextGenStatus
from src.py.com.yun.mao.config import YunYinMaoConfig
from src.py.com.yun.mao.util.need.CommonCode import MessageMyObj
from src.py.com.yun.mao.util.need import CommonCode


@pytest.fixture
def allow_ai(monkeypatch):
    monkeypatch.setattr(
        TextProcessLogic._sq_jqm,
        "current_account_info",
        types.SimpleNamespace(has_ai_ability=lambda: True),
    )
    monkeypatch.setattr(TextProcessLogic, "sec", lambda value: value)
    monkeypatch.setattr(
        TextProcessLogic,
        "_repeat_print",
        lambda *args, **kwargs: None,
    )


def test_process_text_returns_generated_string(monkeypatch, allow_ai):
    calls = []

    def generate(source, **kwargs):
        calls.append((source, kwargs))
        return AiTextGenStatus.SUCCESS, "generated"

    monkeypatch.setattr(AiTextGenFlow, "generate_text", generate)
    employee = types.SimpleNamespace(enable=True)
    auto = types.SimpleNamespace(aiEmployee=employee, api_key="xai-test")
    bean = types.SimpleNamespace(text="old")

    result = TextProcessLogic.process_text_by_ai_if_need(
        "old",
        auto,
        bean,
    )

    assert result == "generated"
    assert bean.text == "generated"
    assert calls[0][0] == "old"


def test_process_text_returns_source_without_employee(monkeypatch, allow_ai):
    calls = []

    def generate(source, **kwargs):
        calls.append(source)
        return AiTextGenStatus.SUCCESS, "generated"

    monkeypatch.setattr(AiTextGenFlow, "generate_text", generate)
    auto = types.SimpleNamespace(aiEmployee=None, aiBean=None)

    assert (
        TextProcessLogic.process_text_by_ai_if_need(
            "source",
            auto,
            None,
        )
        == "source"
    )
    assert calls == []


def test_process_text_refused_records_bean(monkeypatch, allow_ai):
    def generate(source, **kwargs):
        return AiTextGenStatus.REFUSED, source

    monkeypatch.setattr(AiTextGenFlow, "generate_text", generate)
    TextCache.ALL_MESSAGE_REFUSED_LIST.clear()
    employee = types.SimpleNamespace(enable=True)
    auto = types.SimpleNamespace(aiEmployee=employee, api_key="xai-test")
    bean = types.SimpleNamespace(text="source", for_mat="html")

    assert (
        TextProcessLogic.process_text_by_ai_if_need(
            "source",
            auto,
            bean,
        )
        == "source"
    )
    assert len(TextCache.ALL_MESSAGE_REFUSED_LIST) == 1
    record = TextCache.ALL_MESSAGE_REFUSED_LIST[0]
    assert isinstance(record, MessageMyObj)
    assert record.for_mat == "html"
    assert record.text == "source"
    assert record.ai_refused is True
    assert bean.ai_refused is True


def test_process_text_stops_without_ai_ability(monkeypatch):
    calls = []

    def generate(source, **kwargs):
        calls.append(source)
        return AiTextGenStatus.SUCCESS, "generated"

    monkeypatch.setattr(AiTextGenFlow, "generate_text", generate)
    monkeypatch.setattr(
        TextProcessLogic._sq_jqm,
        "current_account_info",
        types.SimpleNamespace(has_ai_ability=lambda: False),
    )
    monkeypatch.setattr(TextProcessLogic, "sec", lambda value: value)
    monkeypatch.setattr(
        TextProcessLogic,
        "_repeat_print",
        lambda *args, **kwargs: None,
    )
    auto = types.SimpleNamespace(aiEmployee=types.SimpleNamespace(enable=True))

    assert TextProcessLogic.process_text_by_ai_if_need("source", auto) == "source"
    assert calls == []


def test_process_text_retries_failed_attempt(monkeypatch, allow_ai):
    calls = []

    def generate(source, **kwargs):
        calls.append(source)
        if len(calls) == 1:
            return AiTextGenStatus.FAILED, source
        return AiTextGenStatus.SUCCESS, "generated"

    monkeypatch.setattr(AiTextGenFlow, "generate_text", generate)
    monkeypatch.setattr(YunYinMaoConfig, "AI_GEN_MAX_TRY_COUNT", 2)
    auto = types.SimpleNamespace(
        aiEmployee=types.SimpleNamespace(enable=True),
        api_key="xai-test",
    )

    assert (
        TextProcessLogic.process_text_by_ai_if_need("source", auto)
        == "generated"
    )
    assert calls == ["source", "source"]


def test_process_text_rejects_invalid_api_key(monkeypatch, allow_ai):
    calls = []

    def generate(source, **kwargs):
        calls.append(source)
        return AiTextGenStatus.SUCCESS, "generated"

    monkeypatch.setattr(AiTextGenFlow, "generate_text", generate)
    auto = types.SimpleNamespace(
        aiEmployee=types.SimpleNamespace(enable=True),
        api_key="invalid-key",
    )

    assert TextProcessLogic.process_text_by_ai_if_need("source", auto) == "source"
    assert calls == []


def test_process_text_records_final_failure(monkeypatch, allow_ai):
    def generate(source, **kwargs):
        return AiTextGenStatus.FAILED, source

    monkeypatch.setattr(AiTextGenFlow, "generate_text", generate)
    TextCache.ALL_MESSAGE_FAILED_LIST.clear()
    bean = types.SimpleNamespace(text="source")
    auto = types.SimpleNamespace(
        aiEmployee=types.SimpleNamespace(enable=True),
        api_key="xai-test",
    )

    assert (
        TextProcessLogic.process_text_by_ai_if_need(
            "source",
            auto,
            bean,
        )
        == "source"
    )
    assert TextCache.ALL_MESSAGE_FAILED_LIST == [bean]


def test_common_code_small_utilities(monkeypatch):
    assert CommonCode.boolToStr(True) == "是"
    assert CommonCode.boolToStr(False) == "否"
    assert CommonCode.container_at_links("hello @user") is True
    assert CommonCode.container_at_links("https://example.test") is True
    assert CommonCode.container_at_links("plain text") is False
    assert CommonCode.message_has_button(
        types.SimpleNamespace(reply_markup={"buttons": []})
    ) is True
    assert CommonCode.message_has_button(
        types.SimpleNamespace(reply_markup=None)
    ) is False
    assert CommonCode.messages_has_button(
        [
            types.SimpleNamespace(reply_markup=None),
            types.SimpleNamespace(reply_markup={"buttons": []}),
        ]
    ) is True
    assert CommonCode.messages_has_video(
        [
            types.SimpleNamespace(video=None),
            types.SimpleNamespace(video=object()),
        ]
    ) is True
    assert CommonCode.isProtectContent(
        types.SimpleNamespace(
            sender=types.SimpleNamespace(noforwards=True),
            chat=types.SimpleNamespace(noforwards=False),
        )
    ) is True
    assert CommonCode.isProtectContent(
        types.SimpleNamespace(
            sender=None,
            chat=types.SimpleNamespace(noforwards=True),
        )
    ) is True
    class _Client:
        async def get_entity(self, entity):
            return types.SimpleNamespace(megagroup=True)

    assert asyncio.run(CommonCode.is_super_group(_Client(), object())) is True
    assert CommonCode.is_broadcast_comment_channel(
        types.SimpleNamespace(broadcast=True)
    ) is True
    assert CommonCode.is_broadcast_comment_channel(
        types.SimpleNamespace(broadcast=False)
    ) is False
    assert CommonCode.is_key_word_in_text("任务正在上传") is True
    assert CommonCode.is_key_word_in_text("普通日志") is False
    assert CommonCode.parse_text(
        types.SimpleNamespace(message=" hello ")
    ) == " hello "
    assert CommonCode.parse_text(types.SimpleNamespace()) == ""
    assert CommonCode.contain_word(
        types.SimpleNamespace(message="hello world"),
        ["world", "missing"],
    ) is True
    assert CommonCode.contain_word(
        types.SimpleNamespace(message="hello world"),
        ["missing"],
    ) is False
    assert CommonCode.messages_has_exclude_words(
        [
            types.SimpleNamespace(message="hello"),
            types.SimpleNamespace(message="blocked word"),
        ],
        ["blocked"],
    ) is True
    assert CommonCode.messages_has_contain_words(
        [types.SimpleNamespace(message="hello world")],
        ["world"],
    ) is True
    assert CommonCode.auto_correct_step_length(0, 8) == 8
    assert CommonCode.auto_correct_step_length(5, 8) == 5
    assert CommonCode.auto_correct_step_length(20, 0) == 1
    videos = [
        types.SimpleNamespace(video=object(), duration=5, size=100),
        types.SimpleNamespace(video=object(), duration=9, size=40),
    ]
    assert CommonCode.get_max_duration_message(videos) is videos[1]
    assert CommonCode.get_max_size_message(videos) is videos[0]
    assert CommonCode.get_max_duration_message([]) is None

    monkeypatch.setattr(CommonCode.random, "randrange", lambda a, b: 42)
    assert CommonCode.geneRamdomId({1, 2}) == 42

    calls = []
    monkeypatch.setattr(CommonCode.random, "randint", lambda a, b: 3)
    monkeypatch.setattr(CommonCode.time, "sleep", calls.append)
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)
    assert CommonCode.sleepTime() is None
    assert calls == [3]
    assert CommonCode._random_ranges_overlap(1, 5, 5, 8) is True
    assert CommonCode._random_ranges_overlap(1, 4, 5, 8) is False
    assert CommonCode._random_range_conflicts(
        10,
        20,
        [(1, 5), (19, 25)],
    ) is True
