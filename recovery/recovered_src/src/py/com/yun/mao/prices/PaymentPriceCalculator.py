# Recovered module: src.py.com.yun.mao.prices.PaymentPriceCalculator
from __future__ import annotations

import math

from ..util import EnumClass


def _map_grade_to_str(grade) -> str:
    return {
        EnumClass.CARD_BEGINNER: "basic",
        EnumClass.CARD_ADVANCED: "advanced",
        EnumClass.CARD_GEEK: "geek",
    }.get(grade, str(grade or "basic"))


def _calc_price_gap(current_30_price, tar_30_price, remaining):
    try:
        day_price_gap = (float(tar_30_price) - float(current_30_price)) / 30.0
        gap_day = int(math.ceil(float(remaining) / 86400.0))
        return max(0.0, day_price_gap * gap_day)
    except Exception:
        return 0.0


def _calc_base_cost_rule(price_config: dict, day: str, tart_grade: str):
    day_key = "day" + str(day or "1")
    grade = _map_grade_to_str(tart_grade)
    config = price_config.get(day_key, {}) if isinstance(price_config, dict) else {}
    try:
        price = float(config.get(grade, 0))
    except Exception:
        price = 0.0
    rule = f"基础费用：{day}天 {price}U"
    return price, rule


def _calc_ai_cost_rule(price_config: dict, day: str, tart_grade: str):
    grade = _map_grade_to_str(tart_grade)
    config = price_config.get("ai", {}) if isinstance(price_config, dict) else {}
    try:
        price = float(config.get(grade, 0))
    except Exception:
        price = 0.0
    return price, f"AI费用{day}天 {price}U"


def _calc_upgrade_card_type(account_info, premium_enum, price_config):
    current = getattr(account_info, "grade", EnumClass.YOU_KE)
    tar = getattr(premium_enum, "tart_grade", EnumClass.CARD_ADVANCED)
    current_30 = float((price_config.get("day30", {}) or {}).get(_map_grade_to_str(current), 0) or 0)
    tar_30 = float((price_config.get("day30", {}) or {}).get(_map_grade_to_str(tar), 0) or 0)
    remaining = getattr(premium_enum, "remaining", 0)
    price = _calc_price_gap(current_30, tar_30, remaining)
    return price, f"卡类型升级计算：({tar_30} - {current_30})/30 * {max(1, int(remaining / 86400))}"


def _calc_upgrade_ai_type(account_info, premium_enum, price_config):
    tar = getattr(premium_enum, "tart_grade", EnumClass.CARD_ADVANCED)
    ai_price = float((price_config.get("ai", {}) or {}).get(_map_grade_to_str(tar), 0) or 0)
    remaining = getattr(premium_enum, "remaining", 0)
    gap = _calc_price_gap(0, ai_price, remaining)
    return gap, f"AI能力升级计算：{gap}"


def _calc_upgrade_card_and_ai_type(account_info, premium_enum, price_config):
    card_price, card_rule = _calc_upgrade_card_type(account_info, premium_enum, price_config)
    ai_price, ai_rule = _calc_upgrade_ai_type(account_info, premium_enum, price_config)
    return card_price + ai_price, card_rule + "\n" + ai_rule


def gen_payment_price(
    account_info,
    premium_enum,
    text: str = "",
    price_config: dict | None = None,
    tart_days: str = "30",
    tart_grade=None,
    tart_ai: bool = False,
) -> dict:
    price_config = price_config or {}
    mode = str(text or "充值模式")
    if mode == "升级模式":
        if getattr(account_info, "has_ai_ability", lambda: False)():
            tar_price, tar_tip = _calc_upgrade_card_and_ai_type(
                account_info, premium_enum, price_config
            )
        else:
            tar_price, tar_tip = _calc_upgrade_card_type(
                account_info, premium_enum, price_config
            )
    else:
        base_cost, base_rule = _calc_base_cost_rule(
            price_config, tart_days, tart_grade
        )
        ai_cost, ai_rule = _calc_ai_cost_rule(
            price_config, tart_days, tart_grade
        ) if tart_ai else (0, "")
        tar_price = base_cost + ai_cost
        tar_tip = base_rule + ("；" + ai_rule if ai_rule else "")
    return {
        "price": round(float(tar_price), 3),
        "tip": tar_tip,
        "mode": mode,
        "tart_days": tart_days,
        "tart_grade": tart_grade,
    }
