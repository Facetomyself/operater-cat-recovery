# Recovered module: src.py.com.yun.mao.prices.PremiumTipHtmlFormatter
from __future__ import annotations

import html


def _escape(text: str) -> str:
    return html.escape(str(text or ""), quote=False)


def format_price_tip_multiline_html(tip: str) -> str:
    lines = [_escape(line) for line in str(tip or "").split("\n") if line.strip()]
    return "<br>".join(lines)


def build_pre_cost_html(tip: str, price_text: str = "", valid: bool = True) -> str:
    safe_tip_html = format_price_tip_multiline_html(tip)
    color = "#2ecc71" if valid else "#ff6b6b"
    warn = "" if valid else "<div style='color:#ff6b6b;'>由于费用不合法，请重新选择！</div>"
    return (
        "<div style='line-height:1.62;padding:9px 11px;border-radius:8px;'>"
        "<div style='font-size:9pt;color:#9aa4b2;'>费用预览</div>"
        f"<div style='font-size:9pt;color:#d8dee9;'>{safe_tip_html}</div>"
        f"<div style='margin-top:9px;font-weight:700;'><span>总预计费用：</span>"
        f"<span style='color:{color};'>{_escape(price_text)}</span></div>"
        + warn
        + "</div>"
    )


def build_account_type_banner_html(card_display_name: str, has_ai: bool) -> str:
    name = _escape(card_display_name or "未知")
    ai_text = "有AI" if has_ai else "无AI"
    return (
        "<div style='margin-bottom:10px;padding-bottom:10px;'>"
        "当前账户是 "
        f"<span style='color:#f3d27a;font-weight:700;'>{name}</span>"
        f" <span style='color:#c8d6c2;'>{ai_text}</span></div>"
    )


def _fragment_operational_tip_html(operational: str) -> str:
    return f"<div style='color:#d7e1ec;'>{_escape(operational)}</div>"


def _fragment_status_tip_html(status: str) -> str:
    return f"<div style='color:#a8c5ff;'>{_escape(status)}</div>"


def build_combined_payment_tip_html(
    operational: str,
    status: str,
    account_banner_html: str | None = None,
) -> str:
    parts = [
        account_banner_html or "",
        _fragment_operational_tip_html(operational),
        _fragment_status_tip_html(status),
    ]
    return "<div style='line-height:1.5;'>" + "".join(parts) + "</div>"
