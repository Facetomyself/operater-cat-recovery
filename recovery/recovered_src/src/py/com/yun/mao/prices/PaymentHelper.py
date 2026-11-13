# Recovered module: src.py.com.yun.mao.prices.PaymentHelper
from __future__ import annotations

from ..util import EnumClass
from ..util.need import utils
from ..util.need.AllBeanDef import PremiumEnumBean


def get_price_config() -> dict:
    from ..fea import _sq_jqm

    return _sq_jqm.current_account_info.get_price_config()


def operational_tip_for_payment_mode(mode: str) -> str:
    return {
        "充值模式": "充值模式：需要选择等级和天数，AI能力可选",
        "续费模式": "续费模式：只能选择天数，不能修改等级，不能修改AI状态",
        "升级模式": "升级模式只能选择等级，不能修改天数，不能修改AI状态",
    }.get(str(mode or ""), "")


def gen_premiumEnumBean_info(account_info) -> PremiumEnumBean:
    try:
        from ..fea import _sq_jqm

        info = account_info or _sq_jqm.current_account_info
        remaining = int(getattr(info, "remainingSec", 0) or 0)
        return PremiumEnumBean(
            models=utils.get_first_n_elements([], 0),
            remaining=remaining,
            remaining_str=utils.format_remaining_time(remaining),
        )
    except Exception:
        return PremiumEnumBean()


def gen_payment_tip(account_info=None, premium_enum=None, text: str = "") -> str:
    try:
        from ..fea import _sq_jqm

        info = account_info or _sq_jqm.current_account_info
        remaining = getattr(premium_enum, "remaining", 0) if premium_enum else 0
        remaining_str = getattr(premium_enum, "remaining_str", "") if premium_enum else ""
        if getattr(info, "grade", 0) == EnumClass.YOU_KE:
            return "你是游客！你现在可以进行充值！"
        if getattr(info, "has_ai_ability", lambda: False)():
            ai_tip = "和【AI能力】"
        else:
            ai_tip = "，你可以选择付费开通AI能力"
        return (
            "你的会员未过期，剩余 "
            + (remaining_str or utils.format_remaining_time(remaining))
            + "，你可以续费！"
            + ai_tip
            + str(text or "")
        )
    except Exception:
        return str(text or "")
