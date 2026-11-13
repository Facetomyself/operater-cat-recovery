# Recovered module: src.py.com.yun.mao.link._fds_jm
# XOR/base64 decoder used by the anti-debug and license message tables.
from __future__ import annotations

import base64
import binascii
import re
import threading

from . import _fds_sj

_SEC_MSGS_CACHE: dict[str, str] = {}
_SEC_MSGS_LOCK = threading.Lock()


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR every byte with the repeating key."""
    if not key:
        return bytes(data)
    return bytes(value ^ key[index % len(key)] for index, value in enumerate(data))


def _b64decode(value: str | bytes) -> bytes:
    raw = value.encode("ascii") if isinstance(value, str) else value
    padded = raw + b"=" * (-len(raw) % 4)
    try:
        return base64.b64decode(padded, altchars=b"-_")
    except Exception:
        return base64.urlsafe_b64decode(padded)


def decode_str(value: str | bytes, key: bytes | None = None) -> str:
    """Decode one catalog value; plaintext is accepted for reconstruction."""
    original = value
    if isinstance(value, str) and not re.fullmatch(r"[A-Za-z0-9+/=_-]+", value):
        return value
    try:
        raw = _b64decode(value)
        decoded = xor_bytes(raw, key or _fds_sj.KEY).decode("utf-8")
        if decoded and all(ch.isprintable() or ch in "\r\n\t" for ch in decoded):
            return decoded
    except (ValueError, UnicodeDecodeError, binascii.Error):
        pass
    if isinstance(original, str):
        return original
    return original.decode("utf-8", "replace")


def decode_str_tuple(values: tuple[str | bytes, ...], key: bytes | None = None) -> tuple[str, ...]:
    """Decode a tuple of catalog values in order."""
    return tuple(decode_str(value, key) for value in values)


def _decode_one_sec_msg(name: str) -> str:
    with _SEC_MSGS_LOCK:
        cached = _SEC_MSGS_CACHE.get(name)
    if cached is not None:
        return cached
    decoded = getattr(_fds_sj, "SEC_MSGS", {}).get(name)
    if decoded is None:
        encoded = _fds_sj.SEC_MSGS_ENC.get(name, name)
        decoded = decode_str(encoded)
    with _SEC_MSGS_LOCK:
        _SEC_MSGS_CACHE[name] = decoded
    return decoded


def sec(name: str) -> str:
    """Return the decoded message associated with a catalog key."""
    return _decode_one_sec_msg(name)
