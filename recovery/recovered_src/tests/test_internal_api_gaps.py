from __future__ import annotations

from types import SimpleNamespace


def test_tabl_cache_recovered_keys():
    from src.py.com.yun.mao.config import tabl_cache

    assert tabl_cache.API_FUN_TAB == "api_fun_group"
    assert tabl_cache.API_FUN_api_id == "api_id"
    assert tabl_cache.API_FUN_api_hash == "api_hash"
    assert tabl_cache.AI_REFUSE_TOKEN_LIST == "new_ai_refuse_token_list"


def test_sq_jqm_module_level_ai_key_probe(monkeypatch):
    from src.py.com.yun.mao.fea import _sq_jqm

    monkeypatch.setattr(
        _sq_jqm,
        "current_account_info",
        SimpleNamespace(has_ai_ability_but_no_key=lambda: True),
    )
    assert _sq_jqm.has_ai_ability_but_no_key() is True


def test_payment_helper_price_config(monkeypatch):
    from src.py.com.yun.mao.fea import _sq_jqm
    from src.py.com.yun.mao.prices import PaymentHelper

    monkeypatch.setattr(
        _sq_jqm,
        "current_account_info",
        SimpleNamespace(get_price_config=lambda: {"a": 1}),
    )
    assert PaymentHelper.get_price_config() == {"a": 1}


def test_suspend_frozen_tag_flood_text():
    from src.py.com.yun.mao.util import SuspendFrozenTag

    SuspendFrozenTag.flood_log_text = "flood"
    assert SuspendFrozenTag.print_last_log_if_need() == "flood"
    SuspendFrozenTag.flood_log_text = ""
