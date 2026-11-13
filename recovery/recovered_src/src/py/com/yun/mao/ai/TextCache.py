# Recovered module: src.py.com.yun.mao.ai.TextCache
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TextCacheBean:
    source: str = ""
    genText: str = ""
    log: str = ""


AI_TXT_GEN_CACHE_LIST: list = []
ALL_MESSAGE_FAILED_LIST: list = []
ALL_MESSAGE_REFUSED_LIST: list = []
