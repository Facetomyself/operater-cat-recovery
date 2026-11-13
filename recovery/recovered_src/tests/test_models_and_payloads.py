from __future__ import annotations

from src.py.com.yun.mao.fea._r_hb_file import RemoteHb
from src.py.com.yun.mao.fea._sq_r_bao import zq_r_item_hb
from src.py.com.yun.mao.fea._sq_jqm import SqJqm
from src.py.com.yun.mao.fea._sq_pz import _normalize_hex, jx_zw_it_hf_x


def test_sq_jqm_guest_projection():
    account = SqJqm()
    assert account.gen_grade_card_str() == "游客"
    assert account.gen_ka_info() == "个人版"
    assert not account.has_ai_ability()


def test_remote_hb_retry_terminal_models():
    assert RemoteHb.failed_retry("net").terminal is False
    assert RemoteHb.failed_terminal("bad").terminal is True
    assert RemoteHb.success({"x": 1}).data == {"x": 1}


def test_item_payload_has_stable_fields():
    body = zq_r_item_hb("u1", "aXRlbQ==", True, 1, "i1")
    assert '"uCode":"u1"' in body
    assert '"item_b64":"aXRlbQ=="' in body
    assert '"item_encoding":"base64"' in body


def test_fingerprint_normalization():
    assert _normalize_hex("aa:bb cc") == "AABBCC"
    assert jx_zw_it_hf_x(["A" * 64])
