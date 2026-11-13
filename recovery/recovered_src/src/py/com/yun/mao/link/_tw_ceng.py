# Recovered module: src.py.com.yun.mao.link._tw_ceng
# Layered Fernet helpers reconstructed from the constant/signature metadata.
from __future__ import annotations

import base64

from cryptography.fernet import Fernet


PLACEHOLDER_ENC_KEY_B = "BUILD_PLACEHOLDER_ENC_KEY_B"
PLACEHOLDER_ENC_KEY_C = "BUILD_PLACEHOLDER_ENC_KEY_C"
PLACEHOLDER_ENC_KEY_D = "BUILD_PLACEHOLDER_ENC_KEY_D"
PLACEHOLDER_ENC_INIT_URL_DEV = "BUILD_PLACEHOLDER_ENC_INIT_URL_DEV"
PLACEHOLDER_ENC_INIT_URL_PROD = "BUILD_PLACEHOLDER_ENC_INIT_URL_PROD"
PLACEHOLDER_ENC_INIT_PUBLIC_KEY = "BUILD_PLACEHOLDER_ENC_INIT_PUBLIC_KEY"

_KA0 = "HXuzM1JE"
_KA1 = "qwAZhFXv"
_KA2 = "gJdUriOk"
_KA3 = "QxS-c_mY"
_KA4 = "b2OkU94R"
_KA5 = "vR8="


def _encrypt_bytes(plaintext: bytes, wrapping_key: bytes) -> str:
    token = Fernet(wrapping_key).encrypt(plaintext)
    return base64.b64encode(token).decode("ascii")


def _decrypt_bytes(ciphertext_b64: str, wrapping_key: bytes) -> bytes:
    raw = base64.b64decode(ciphertext_b64, altchars=b"-_")
    return Fernet(wrapping_key).decrypt(raw)


def generate_layer_keys() -> tuple[bytes, bytes, bytes]:
    return (
        Fernet.generate_key(),
        Fernet.generate_key(),
        Fernet.generate_key(),
    )


def assem_rk_a(material: bytes = b"") -> bytes:
    """Assemble the root layer key from its base64 fragments."""
    text = (
        bytes(material)
        if material
        else (_KA0 + _KA1 + _KA2 + _KA3 + _KA4 + _KA5).encode("ascii")
    )
    return text


def build_nested_layer_ciphertexts(
    key_b: bytes, key_c: bytes, key_d: bytes
) -> tuple[bytes, bytes, bytes, str, str, str]:
    root_a = assem_rk_a(key_b + key_c + key_d)
    enc_b = _encrypt_bytes(key_b, root_a)
    enc_c = _encrypt_bytes(key_c, key_b)
    enc_d = _encrypt_bytes(key_d, key_c)
    return key_b, key_c, key_d, enc_b, enc_c, enc_d


def encrypt_with_layer_d(plaintext: str, key_d: bytes) -> str:
    return _encrypt_bytes(plaintext.encode("utf-8"), key_d)


def decrypt_with_layer_d(ciphertext_b64: str, key_d: bytes) -> str:
    return _decrypt_bytes(ciphertext_b64, key_d).decode("utf-8")


def unwrap_to_layer_d(
    enc_b: str,
    enc_c: str,
    enc_d: str,
    root_a: bytes | None = None,
    key_b: bytes | None = None,
    key_c: bytes | None = None,
    key_d: bytes | None = None,
) -> bytes:
    """Unwrap the layer material down to key D."""
    if key_d is not None:
        return key_d
    if key_b is not None:
        resolved_c = _decrypt_bytes(enc_c, key_b)
        return _decrypt_bytes(enc_d, resolved_c)
    if root_a is not None:
        resolved_b = _decrypt_bytes(enc_b, root_a)
        resolved_c = _decrypt_bytes(enc_c, resolved_b)
        return _decrypt_bytes(enc_d, resolved_c)
    raise ValueError("insufficient layer material")


def tw_sjk_ph(value: str) -> bool:
    """Return True when a build-time placeholder was not replaced."""
    return value.startswith(("BUILD_PLACEHOLDER_", "BUILD_TIME_PLACEHOLDER_"))
