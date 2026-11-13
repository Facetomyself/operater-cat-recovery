# Recovered module: src.py.com.yun.mao.prices.PriceHtmlUtils
from __future__ import annotations

from decimal import Decimal


def insert_zwsp(s: str, every: int = 4) -> str:
    text = str(s or "")
    every = max(1, int(every))
    return "\u200b".join(text[index : index + every] for index in range(0, len(text), every))


def get_address_info_html(onumber: str, amount: float, address: str) -> str:
    amount_str = f"{Decimal(str(amount or 0)):.3f}".rstrip("0").rstrip(".")
    addr = insert_zwsp(str(address or ""))
    return (
        "<p>订单号(重要)："
        + str(onumber or "")
        + "</p><p>到账金额："
        + amount_str
        + " USDT</p><p>收款地址："
        + addr
        + "</p>"
    )


def get_full_payment_info_html(amount: float, customer_service: str = "@xxxx") -> str:
    amount_str = f"{Decimal(str(amount or 0)):.3f}".rstrip("0").rstrip(".")
    return (
        "<div>请使用 TRON 网络转账，到账金额 "
        + amount_str
        + " USDT，少转多转都不会自动充值。唯一客服："
        + str(customer_service or "@xxxx")
        + "</div>"
    )


def gen_recharge_failed_tip(tip_str: str = "") -> str:
    if tip_str:
        return str(tip_str)
    return (
        "<div>很抱歉，暂未查询到您的订单。请确认支付是否成功、金额是否一致，"
        "或联系客服提供支付记录和订单截图。</div>"
    )
