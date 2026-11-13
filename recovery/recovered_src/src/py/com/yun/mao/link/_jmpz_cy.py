# Recovered module: src.py.com.yun.mao.link._jmpz_cy
# Fernet catalog helpers reconstructed from the constant/signature metadata.
from __future__ import annotations

import base64

from cryptography.fernet import Fernet


PLACEHOLDER_ENCRYPTED_STATIC_KEY = (
    "BUILD_TIME_PLACEHOLDER_FOR_ENCRYPTED_STATIC_KEY"
)


def encrypt_catalog(
    plaintext_catalog: dict[str, str], static_key: bytes
) -> dict[str, str]:
    """Encrypt each catalog value with a static Fernet key."""
    cipher = Fernet(static_key)
    result = {}
    for name, plaintext in plaintext_catalog.items():
        token = cipher.encrypt(plaintext.encode("utf-8"))
        result[name] = base64.b64encode(token).decode("ascii")
    return result


def decrypt_token(encrypted_b64: str, static_key: bytes) -> str:
    """Decrypt a base64-wrapped Fernet token."""
    raw = base64.b64decode(encrypted_b64, altchars=b"-_")
    return Fernet(static_key).decrypt(raw).decode("utf-8")


def encrypt_static_key_with_root(static_key: bytes, root_key: str) -> str:
    """Wrap the static key with the root key derived by the outer layer."""
    cipher = Fernet(root_key.encode("ascii") if isinstance(root_key, str) else root_key)
    token = cipher.encrypt(static_key)
    return base64.b64encode(token).decode("ascii")


def is_placeholder_static_key(value: str) -> bool:
    return not value or value.startswith("BUILD_TIME_PLACEHOLDER_")
