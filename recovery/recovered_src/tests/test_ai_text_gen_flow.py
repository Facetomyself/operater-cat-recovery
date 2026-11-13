from __future__ import annotations

import types

from src.py.com.yun.mao.ai.AiTextGenFlow import AiTextGenFlow


def test_check_sensitive_and_replace_sensitive():
    assert AiTextGenFlow.check_sensitive(
        "hello BAD world",
        "x| bad ",
    ) == (True, "BAD")
    assert AiTextGenFlow.check_sensitive("hello", "x|bad") == (False, "")
    assert AiTextGenFlow.check_sensitive(
        "hello world",
        "",
        ("world",),
    ) == (True, "world")

    replaced = AiTextGenFlow.replace_sensitive(
        "a BAD b bad c",
        " bad |",
    )
    assert "bad" not in replaced.lower()


def test_no_semantic():
    assert AiTextGenFlow.no_semantic("!!! --- ...") is True
    assert AiTextGenFlow.no_semantic("abc 123") is False


def test_detect_api_refusal_content_filter():
    response = types.SimpleNamespace(
        choices=[
            types.SimpleNamespace(
                message=types.SimpleNamespace(content="x", refusal=None),
                finish_reason="content_filter",
            )
        ]
    )
    assert AiTextGenFlow._detect_api_refusal(response) == (
        True,
        "content_filter",
    )
