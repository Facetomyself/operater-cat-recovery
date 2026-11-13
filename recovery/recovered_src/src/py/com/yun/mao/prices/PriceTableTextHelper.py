# Recovered module: src.py.com.yun.mao.prices.PriceTableTextHelper
from __future__ import annotations


def get_subscription_html_dark(prices: dict) -> str:
    prices = prices or {}
    permission = prices.get("permission", {})
    day1 = prices.get("day1", {})
    day15 = prices.get("day15", {})
    day30 = prices.get("day30", {})
    ai = prices.get("ai", {})
    return (
        '<div class="container">'
        "<h3>会员套餐对比</h3>"
        "<table class=\"price-grid\"><tr><th>权益</th><th>初级卡</th><th>高级卡</th><th>极客卡</th></tr>"
        f"<tr><td>最多可添加条目数量</td><td>{permission.get('basic','')}个</td><td>{permission.get('advanced','')}个</td><td>不限制数量</td></tr>"
        "<tr><td>多开分身</td><td>不可以</td><td>不可以</td><td>可以</td></tr>"
        f"<tr><td>1天</td><td>{day1.get('basic','')}U</td><td>{day1.get('advanced','')}U</td><td>{day1.get('geek','')}U</td></tr>"
        f"<tr><td>15天</td><td>{day15.get('basic','')}U</td><td>{day15.get('advanced','')}U</td><td>{day15.get('geek','')}U</td></tr>"
        f"<tr><td>30天</td><td>{day30.get('basic','')}U</td><td>{day30.get('advanced','')}U</td><td>{day30.get('geek','')}U</td></tr>"
        f"<tr><td>AI包月30天</td><td>{ai.get('basic','')}U</td><td>{ai.get('advanced','')}U</td><td>{ai.get('geek','')}U</td></tr>"
        "</table><div class=\"desc1\">默认计价单位是U，请按页面提示完成支付。</div></div>"
    )
