# Recovered module: src.py.com.yun.mao.ai._ai_refusal_detect
from __future__ import annotations

from typing import Tuple

from .AI_DEFAULT_REFUSE_LIST import get_default_token


def get_refuse_tokens() -> list[str]:
    return [token for token in get_default_token().split("|") if token]


def _message_text(msg) -> str:
    if msg is None:
        return ""
    if isinstance(msg, str):
        return msg
    if isinstance(msg, dict):
        return str(msg.get("content", msg.get("text", "")) or "")
    content = getattr(msg, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            str(part.get("text", "")) if isinstance(part, dict) else str(part)
            for part in content
        )
    return str(content or getattr(msg, "text", "") or "")


def is_soft_refusal_content(content: str) -> Tuple[bool, str]:
    text = str(content or "").strip()
    if not text:
        return False, ""
    lowered = text.lower()
    for token in get_refuse_tokens():
        if token.lower() in lowered:
            return True, token
    return False, ""


def detect_api_refusal(response) -> Tuple[bool, str]:
    try:
        choices = getattr(response, "choices", None)
        if choices is None and isinstance(response, dict):
            choices = response.get("choices")
        if not choices:
            return True, "empty choices"
        choice = choices[0]
        message = (
            choice.get("message")
            if isinstance(choice, dict)
            else getattr(choice, "message", None)
        )
        finish = (
            choice.get("finish_reason")
            if isinstance(choice, dict)
            else getattr(choice, "finish_reason", None)
        )
        refusal = (
            message.get("refusal")
            if isinstance(message, dict)
            else getattr(message, "refusal", None)
        )
        content = _message_text(message)
        if finish == "content_filter":
            return True, "content_filter"
        if refusal:
            return True, str(refusal)
        soft, token = is_soft_refusal_content(content)
        if soft:
            return True, token
        if not content.strip():
            return True, "empty content"
        return False, ""
    except Exception as exc:
        return True, str(exc)
