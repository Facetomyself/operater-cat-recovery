# Recovered module: src.py.com.yun.mao.util.AiTestTipHtmlHelper
# The module constants chunk contains one public helper and its HTML payload.
from __future__ import annotations


AI_TEST_PLATFORM_TIP_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            padding: 6px 12px;
            background-color: #3c3f42;
            font-family: "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
            color: #ffffff;
        }
        .container {
            background-color: #2d2f33;
            border-radius: 8px;
            padding: 10px 14px;
            box-sizing: border-box;
        }
        .title {
            text-align: center;
            color: #ff6b9d;
            font-size: 13pt;
            font-weight: bold;
            margin: 0 0 3px 0;
        }
        .subtitle {
            text-align: center;
            color: #a0a0a0;
            font-size: 9pt;
            margin-bottom: 8px;
        }
        .content {
            font-size: 10pt;
            line-height: 1.48;
            color: #e0e0e0;
        }
        ol {
            padding-left: 18px;
            margin: 4px 0 0 0;
        }
        li {
            margin-bottom: 6px;
        }
        .highlight {
            color: #ff8ab3;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">AI专属测试体验平台</div>
        <div class="subtitle">（限时免费体验测试）</div>

        <div class="content">
            <strong>说明：</strong>
            <ol>
                <li>仅限非AI会员免费测试使用。</li>
                <li>可以切换内置的<span class="highlight">官方色情大师</span>或<span class="highlight">官方中文记者</span>AI员工。</li>
                <li>开通AI会员后可<span class="highlight">自定义</span>色情AI员工或新闻记者员工，或者其他能力的AI员工。</li>
                <li>此测试平台仅仅是文本同义转换，应用场景为：把电报的帖子文案做同义转换，让收录平台判定为原创资源。</li>
                <li>最终解释权归运营猫官方。</li>
                <li>本平台为<span class="highlight">限时免费</span>体验。</li>
            </ol>
        </div>
    </div>
</body>
</html>"""


def create_ai_test_platform_tip() -> str:
    """Return the AI test-platform tip HTML used by the AI test tab."""
    return AI_TEST_PLATFORM_TIP_HTML
