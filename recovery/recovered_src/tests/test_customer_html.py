from __future__ import annotations

from src.py.com.yun.mao.util.CustomerHtmlFormat import (
    code_unit_length,
    entities_to_html,
    slice_by_cu,
)


class MessageEntityBold:
    def __init__(self, offset, length):
        self.offset = offset
        self.length = length


class MessageEntityTextUrl:
    def __init__(self, offset, length, url):
        self.offset = offset
        self.length = length
        self.url = url


def test_customer_html_wraps_bold_and_url():
    text = "hello world"
    entities = [
        MessageEntityBold(0, 5),
        MessageEntityTextUrl(6, 5, "https://example.com?a=1&b=2"),
    ]
    result = entities_to_html(text, entities)

    assert "<b>hello</b>" in result
    assert 'href="https://example.com?a=1&amp;b=2"' in result
    assert "<a " in result and "</a>" in result


def test_code_unit_helpers_handle_non_bmp():
    assert code_unit_length("a😊") == 3
    assert slice_by_cu("a😊b", 1, 2) == "😊"
