# Recovered module: src.py.com.yun.mao.fea._xx_zy_file
# Message digest and parse-request payload builders reconstructed from the
# constant names and function signatures.
from __future__ import annotations

import hashlib
import time as time_mod
import uuid


DIGEST_TEXT_MAX_LEN = 4096
PARSE_API_VERSION = 702


def _normalize_digest_text(o) -> str:
    if o is None:
        return ""
    text = str(o).strip()
    return text[:DIGEST_TEXT_MAX_LEN]


def _message_digest(msg) -> dict:
    text = _normalize_digest_text(getattr(msg, "text", ""))
    return {
        "id": getattr(msg, "id", 0),
        "groupedId": getattr(msg, "grouped_id", None),
        "msgType": getattr(msg, "message_type", None),
        "durationSec": 0,
        "sizeMb": 0,
        "text": text,
        "hasButton": bool(getattr(msg, "message_has_button", False)),
        "legal": bool(getattr(msg, "is_legal_resource", True)),
    }


def messages_to_digests(messages) -> list[dict]:
    return [_message_digest(message) for message in (messages or [])]


def build_parse_trace_id(ucode: str, nonce: str, ts, raw="") -> str:
    payload = "|".join((str(ucode), str(nonce), str(ts), str(raw)))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def serialize_auto_for_parse(auto, bean_like=False):
    if isinstance(auto, dict):
        data = dict(auto)
    else:
        data = dict(getattr(auto, "__dict__", {}))
    return {
        "autoType": data.get("auto_type", data.get("autoType", "")),
        "kid": data.get("kid", ""),
    }


def serialize_comment_rule(comment_rule):
    if isinstance(comment_rule, dict):
        return dict(comment_rule)
    return dict(getattr(comment_rule, "__dict__", {}))


def build_channel_parse_payload(
    auto,
    message_digests,
    is_monitor: bool,
    request_id: str,
    gy_jc_a3,
    time=None,
) -> dict:
    return {
        "apiVersion": PARSE_API_VERSION,
        "requestId": request_id or str(uuid.uuid4()),
        "clientTs": int(time if time is not None else time_mod.time()),
        "isMonitor": bool(is_monitor),
        "auto": serialize_auto_for_parse(auto),
        "messages": list(message_digests or []),
        "gy_jc_a3": gy_jc_a3,
    }


def build_comment_parse_payload(
    comment_rule,
    message_digests,
    request_id: str,
    time=None,
) -> dict:
    return {
        "apiVersion": PARSE_API_VERSION,
        "requestId": request_id or str(uuid.uuid4()),
        "clientTs": int(time if time is not None else time_mod.time()),
        "commentRule": serialize_comment_rule(comment_rule),
        "messages": list(message_digests or []),
    }


def parse_uni_id(uni_id_str: str):
    value = str(uni_id_str or "")
    parts = value.replace("|", "-").split("-")
    return parts
