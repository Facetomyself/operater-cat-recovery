# Recovered module: src.py.com.yun.mao.jm._my_gk
from __future__ import annotations

from cryptography.hazmat.primitives import serialization

from ..link._tw_ctx import TwCtx


def jm_jz_gy_pk(public_key_pem: str | bytes | None = None):
    """Load the configured RSA public key for request/response envelopes."""
    if public_key_pem is None:
        public_key_pem = TwCtx.tw_hq_by_k("_f_pk")
    if isinstance(public_key_pem, str):
        public_key_pem = public_key_pem.encode("utf-8")
    return serialization.load_pem_public_key(public_key_pem)
