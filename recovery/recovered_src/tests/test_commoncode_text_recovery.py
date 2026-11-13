from __future__ import annotations

from src.py.com.yun.mao.util.need.CommonCode import process_text_to_obj


def test_process_text_to_obj_deleting_source_wins_over_markdown():
    result = process_text_to_obj(True, "source", True, True, ["a->b"])
    assert result.for_mat == "html"
    assert result.text == ""
    assert result.ai_refused is False


def test_process_text_to_obj_markdown_returns_text_unchanged():
    result = process_text_to_obj(
        True,
        "https://example.test/a -> b",
        False,
        True,
        ["->", "unused->value"],
    )
    assert result.for_mat == "markdown"
    assert result.text == "https://example.test/a -> b"


def test_process_text_to_obj_removes_links_and_applies_replacements():
    result = process_text_to_obj(
        False,
        "see https://example.test/a old value",
        False,
        True,
        ["old->new"],
    )
    assert result.for_mat == "html"
    assert result.text == "see  new value"


def test_process_text_to_obj_skips_items_without_separator():
    result = process_text_to_obj(
        False,
        "old value",
        False,
        False,
        ["not a replacement", "old->new"],
    )
    assert result.text == "new value"


def test_process_text_to_obj_malformed_replacement_stops_loop():
    result = process_text_to_obj(
        False,
        "a->b->c",
        False,
        False,
        ["a->x", "a->b->c", "b->z"],
    )
    assert result.text == "x->b->c"
