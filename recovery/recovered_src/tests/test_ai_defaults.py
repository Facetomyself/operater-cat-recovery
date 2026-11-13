from __future__ import annotations

from src.py.com.yun.mao.util import AI_INNER_DEF, AiTestTipHtmlHelper


def test_ai_inner_defaults_are_populated():
    assert AI_INNER_DEF.SEXY_DEFAULT_ROLE
    assert AI_INNER_DEF.SEXY_DEFAULT_PRE_TEXT
    assert AI_INNER_DEF.NEWS_DEFAULT_ROLE
    assert AI_INNER_DEF.NEWS_DEFAULT_PRE_TEXT
    assert "儿童性交易" in AI_INNER_DEF.SENSITIVE_DEFAULT
    assert AI_INNER_DEF.DEFAULT_INNER_AI_MODEL == "grok-4-1-fast"


def test_ai_test_tip_html_helper_returns_html():
    html = AiTestTipHtmlHelper.create_ai_test_platform_tip()
    assert isinstance(html, str)
    assert "AI专属测试体验平台" in html
