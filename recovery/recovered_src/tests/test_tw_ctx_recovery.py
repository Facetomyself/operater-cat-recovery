from __future__ import annotations


def test_layer_root_key_is_assembled_from_fragments():
    from src.py.com.yun.mao.link._tw_ceng import assem_rk_a

    root = assem_rk_a()
    assert len(root) == 44
    assert root.endswith(b"=")


def test_tw_ctx_unwraps_layer_and_decodes_endpoint():
    from src.py.com.yun.mao.link._tw_ctx import TwCtx

    TwCtx._ensure_built()
    assert len(TwCtx._layer_d or b"") == 44
    assert TwCtx.tw_sjk_url() == "https://birder.jinsiqie.life/xb/iil"
    pem = TwCtx.tw_sjk_pk_pem()
    assert pem.startswith("-----BEGIN PUBLIC KEY-----")
    assert pem.rstrip().endswith("-----END PUBLIC KEY-----")


def test_tw_ctx_static_catalog_fails_closed_when_key_is_missing():
    from src.py.com.yun.mao.link._tw_ctx import TwCtx

    TwCtx._ensure_built()
    if TwCtx._static_cipher is not None:
        return
    try:
        TwCtx.tw_hq_by_k("_r_u")
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError when static cipher is missing")


def test_tw_jm_ok_reflects_static_cipher_availability():
    from src.py.com.yun.mao.link._tw_ctx import TwCtx

    TwCtx._ensure_built()
    assert TwCtx.tw_jm_ok() is (TwCtx._static_cipher is not None)


def test_tw_yy_mk_preserves_server_root_key():
    from src.py.com.yun.mao.link._tw_ctx import TwCtx

    TwCtx.tw_yy_mk("server-root-key")
    TwCtx._ensure_built()
    assert TwCtx.tw_hq_rk() == "server-root-key"


def test_decrypt_token_accepts_urlsafe_catalog_values():
    import base64

    from cryptography.fernet import Fernet

    from src.py.com.yun.mao.link import _jmpz_cy

    key = Fernet.generate_key()
    token = Fernet(key).encrypt(b"catalog-value")
    encoded = base64.urlsafe_b64encode(token).decode("ascii")

    assert _jmpz_cy.decrypt_token(encoded, key) == "catalog-value"
