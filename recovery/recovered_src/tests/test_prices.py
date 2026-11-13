from __future__ import annotations

from src.py.com.yun.mao.prices.PaymentPriceCalculator import gen_payment_price
from src.py.com.yun.mao.prices.PremiumTipHtmlFormatter import (
    build_account_type_banner_html,
    build_combined_payment_tip_html,
    build_pre_cost_html,
    format_price_tip_multiline_html,
)
from src.py.com.yun.mao.prices.PriceHtmlUtils import insert_zwsp
from src.py.com.yun.mao.prices.PriceHtmlUtils import (
    gen_recharge_failed_tip,
    get_address_info_html,
    get_full_payment_info_html,
)
from src.py.com.yun.mao.prices.AiModelInfoGenHelper import create_model_price_table
from src.py.com.yun.mao.prices.PriceTableBiggerTextHelper import (
    get_subscription_bigger_html_dark,
)
from src.py.com.yun.mao.prices.PriceTableTextHelper import get_subscription_html_dark
from src.py.com.yun.mao.util.EnumClass import CARD_BEGINNER


def test_price_calculator_recharge_rule():
    premium = type("P", (), {"remaining": 86400})()
    result = gen_payment_price(
        None,
        premium,
        "充值模式",
        {"day30": {"basic": "49"}, "ai": {"basic": "29"}},
        "30",
        CARD_BEGINNER,
        True,
    )
    assert result["price"] == 78.0
    assert "AI费用" in result["tip"]


def test_html_helpers_escape_and_space():
    assert "<br>" in format_price_tip_multiline_html("a\nb")
    assert "\u200b" in insert_zwsp("abcdefgh")


def test_payment_html_helpers():
    address_html = get_address_info_html("order-1", 12.5, "TRONADDRESS")
    assert "order-1" in address_html
    assert "12.5 USDT" in address_html
    assert "\u200b" in address_html
    full_html = get_full_payment_info_html(9.0, "@kefu")
    assert "9 USDT" in full_html
    assert "@kefu" in full_html
    assert gen_recharge_failed_tip("custom") == "custom"
    assert "暂未查询到" in gen_recharge_failed_tip("")


def test_model_price_table():
    html = create_model_price_table('[{"name":"m1","price":"1"}]')
    assert "m1" in html
    assert "模型价格表" in html
    empty = create_model_price_table("not-json")
    assert "模型价格表" in empty


def test_premium_tip_html_builders():
    cost = build_pre_cost_html("第一行\n第二行", "9.9", True)
    assert "第一行<br>第二行" in cost
    assert "9.9" in cost
    assert "#2ecc71" in cost
    invalid = build_pre_cost_html("提示", "x", False)
    assert "费用不合法" in invalid
    assert "#ff6b6b" in invalid
    banner = build_account_type_banner_html("高级卡", True)
    assert "高级卡" in banner
    assert "有AI" in banner
    combined = build_combined_payment_tip_html("操作", "状态", banner)
    assert "操作" in combined
    assert "状态" in combined
    assert "高级卡" in combined


def test_subscription_price_tables():
    prices = {
        "permission": {"basic": "3", "advanced": "10"},
        "day1": {"basic": "9", "advanced": "19", "geek": "29"},
        "day15": {"basic": "29", "advanced": "49", "geek": "79"},
        "day30": {"basic": "49", "advanced": "79", "geek": "129"},
        "ai": {"basic": "29", "advanced": "39", "geek": "49"},
    }
    html = get_subscription_html_dark(prices)
    assert "会员套餐对比" in html
    assert "3个" in html
    assert "9U" in html
    assert "129U" in html
    bigger = get_subscription_bigger_html_dark(prices)
    assert "会员套餐对比" in bigger
    assert bigger == html
