# Recovered module: src.py.com.yun.mao.prices.PriceTableBiggerTextHelper
from __future__ import annotations

from .PriceTableTextHelper import get_subscription_html_dark


def get_subscription_bigger_html_dark(prices: dict) -> str:
    html = get_subscription_html_dark(prices)
    return html.replace('style="font-size:', 'style="font-size:larger;')
