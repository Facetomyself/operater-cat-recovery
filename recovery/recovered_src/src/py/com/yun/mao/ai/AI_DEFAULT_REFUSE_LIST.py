# Recovered module: src.py.com.yun.mao.ai.AI_DEFAULT_REFUSE_LIST
from __future__ import annotations


_RAW_TOKENS = """
不生成|拒绝|拒绝请求|无法生成|抱歉|请提供源文案|拒绝协助|拒绝生成|拒绝|拒绝|无法帮你改写|无法改写|拒绝改写|不能协助|无法协助|我无法协助|我不生成|我拒绝|我表示很抱歉
|我无法帮你|我无法改写|我不能协助|没有提供源文案原文
|No, I cant|I must decline|I cant assist with|No, I wont|No, I cannot|
No, I cannot|I cannot assist with|No, I cant assist
"""

DEFAULT_REFUSE_LIST = [
    token.strip()
    for token in _RAW_TOKENS.replace("\n", "").split("|")
    if token.strip()
]


def get_default_token() -> str:
    return "|".join(DEFAULT_REFUSE_LIST)
