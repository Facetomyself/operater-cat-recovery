# Recovered module: src.py.com.yun.mao.jm._my_util
# RSA/AES primitives used by the boot and licence request envelope.
from __future__ import annotations

import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def _as_bytes(value) -> bytes:
    return value.encode("utf-8") if isinstance(value, str) else bytes(value)


def _load_public_key(public_key):
    if hasattr(public_key, "encrypt"):
        return public_key
    return serialization.load_pem_public_key(_as_bytes(public_key))


def _load_private_key(private_key):
    if hasattr(private_key, "decrypt"):
        return private_key
    return serialization.load_pem_private_key(
        _as_bytes(private_key),
        password=None,
    )


def generate_rsa_keys() -> tuple[bytes, bytes]:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def aes_encrypt(data, key: bytes) -> bytes:
    """AES-CBC/PKCS7 encrypt and prefix the random IV to the ciphertext."""
    iv = os.urandom(16)
    cipher = Cipher(
        algorithms.AES(_as_bytes(key)),
        modes.CBC(iv),
        backend=default_backend(),
    )
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(_as_bytes(data)) + padder.finalize()
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext


def aes_decrypt(ciphertext: bytes, key: bytes) -> str:
    ciphertext = _as_bytes(ciphertext)
    iv, encrypted = ciphertext[:16], ciphertext[16:]
    cipher = Cipher(
        algorithms.AES(_as_bytes(key)),
        modes.CBC(iv),
        backend=default_backend(),
    )
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plain = unpadder.update(decrypted_data) + unpadder.finalize()
    return plain.decode("utf-8")


def rsa_encrypt_key(public_key, aes_key: bytes) -> bytes:
    return _load_public_key(public_key).encrypt(
        _as_bytes(aes_key),
        asymmetric_padding.PKCS1v15(),
    )


def rsa_decrypt_key(private_key, encrypted_aes_key: bytes) -> bytes:
    return _load_private_key(private_key).decrypt(
        _as_bytes(encrypted_aes_key),
        asymmetric_padding.PKCS1v15(),
    )


def jm_yq_qm(public_key, message_byte: bytes, signature_byte: bytes) -> bool:
    """Verify a SHA-256/PKCS1v15 signature; anti-debug guard stays optional."""
    try:
        try:
            from ..link._fds_tan import wb_jm_yq

            wb_jm_yq()
        except Exception:
            pass
        _load_public_key(public_key).verify(
            _as_bytes(signature_byte),
            _as_bytes(message_byte),
            asymmetric_padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False
