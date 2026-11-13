from __future__ import annotations

from src.py.com.yun.mao.fea._xx_zy_file import (
    build_channel_parse_payload,
    build_parse_trace_id,
    messages_to_digests,
    parse_uni_id,
)


class Message:
    id = 7
    grouped_id = 9
    message_type = "text"
    text = "hello"
    message_has_button = False
    is_legal_resource = True


def test_message_digest_and_payload_shape():
    digest = messages_to_digests([Message()])[0]
    assert digest["id"] == 7
    assert digest["text"] == "hello"
    payload = build_channel_parse_payload(
        type("Auto", (), {"kid": "k1"})(),
        [digest],
        False,
        "rid",
        None,
        time=0,
    )
    assert payload["requestId"] == "rid"
    assert payload["apiVersion"] == 702
    assert payload["isMonitor"] is False


def test_trace_and_uni_id_helpers():
    assert len(build_parse_trace_id("u", "n", "0")) == 16
    assert parse_uni_id("a-b") == ["a", "b"]
