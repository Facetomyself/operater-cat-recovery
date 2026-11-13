from __future__ import annotations

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from src.py.com.yun.mao.jm._my_dt import jm_sc_aes_k
from src.py.com.yun.mao.jm._my_util import (
    aes_decrypt,
    aes_encrypt,
    generate_rsa_keys,
    jm_yq_qm,
    rsa_decrypt_key,
    rsa_encrypt_key,
)


def test_aes_cbc_pkcs7_roundtrip():
    key = jm_sc_aes_k()
    assert len(key) == 16
    encrypted = aes_encrypt("运营猫-offline", key)
    assert aes_decrypt(encrypted, key) == "运营猫-offline"


def test_rsa_key_wrap_and_signature_roundtrip():
    private_pem, public_pem = generate_rsa_keys()
    key = jm_sc_aes_k()
    wrapped = rsa_encrypt_key(public_pem, key)
    assert rsa_decrypt_key(private_pem, wrapped) == key

    message = b"offline-message"
    private_key = __import__(
        "cryptography.hazmat.primitives.serialization",
        fromlist=["load_pem_private_key"],
    ).load_pem_private_key(private_pem, password=None)
    public_key = __import__(
        "cryptography.hazmat.primitives.serialization",
        fromlist=["load_pem_public_key"],
    ).load_pem_public_key(public_pem)
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    assert jm_yq_qm(public_key, message, signature)
