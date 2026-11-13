# Recovered module: src.py.com.yun.mao.jm._my_r_gk
# Static reconstruction from the Nuitka constants chunk and module init.
from __future__ import annotations

from cryptography.hazmat.primitives import serialization

from ..link._tw_ctx import TwCtx


def jm_jz_r_pk():
    """Load the configured RSA public key.

    Constants and the function body show:
    ``public_key_pem = TwCtx.tw_hq_by_k('_r_pk')`` followed by
    ``serialization.load_pem_public_key(public_key_pem.encode())``.
    """

    public_key_pem = TwCtx.tw_hq_by_k("_r_pk")
    return serialization.load_pem_public_key(
        public_key_pem.encode("utf-8")
    )
