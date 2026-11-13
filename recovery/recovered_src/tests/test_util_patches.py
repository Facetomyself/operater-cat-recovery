from __future__ import annotations

from src.py.com.yun.mao.util.moviepy_ffmpeg_patch import (
    _decode_ffmpeg_stderr,
    _stderr_bytes_as_utf8,
)
from src.py.com.yun.mao.util.XAIKeyValidator import XAIKeyValidator


def test_ffmpeg_stderr_decoder_accepts_utf8_and_fallback_bytes():
    assert _decode_ffmpeg_stderr("中文".encode("utf-8")) == "中文"
    assert isinstance(_decode_ffmpeg_stderr(b"\xff\xfe"), str)
    assert isinstance(_stderr_bytes_as_utf8(b"\xff\xfe"), bytes)


def test_xai_validator_strips_api_key_without_synthesizing_parent():
    validator = XAIKeyValidator(" bad-key ")
    assert validator.api_key == "bad-key"
    assert not hasattr(validator, "parent")
