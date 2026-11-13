# Recovered module: src.py.com.yun.mao.ai.AiTextGenFlow
from __future__ import annotations

import json
import re
import unicodedata
from typing import Tuple

from . import TextCache
from .AiTextGenStatus import AiTextGenStatus
from ._ai_refusal_detect import detect_api_refusal
from .TextCache import TextCacheBean
from ..util.need import utils


class AiTextGenFlow:
    _last_api_key = ""
    _g_client = None

    @classmethod
    def _is_content_policy_error(cls, exc: BaseException) -> bool:
        text = str(exc or "").lower()
        return any(
            token in text
            for token in (
                "content_policy",
                "content policy",
                "content_filter",
                "content filter",
                "safety",
                "moderation",
                "refused",
            )
        )

    @classmethod
    def _detect_api_refusal(cls, response) -> Tuple[bool, str]:
        refused, detail = detect_api_refusal(response)
        if refused and not detail:
            detail = "API 拒绝生成"
        return bool(refused), str(detail or "")

    @classmethod
    def obtain_open_ai_client(cls, api_key: str):
        if not api_key:
            return None
        if cls._g_client is not None and cls._last_api_key == api_key:
            return cls._g_client
        try:
            from openai import OpenAI

            cls._g_client = OpenAI(
                api_key=api_key,
                base_url="https://api.x.ai/v1",
            )
            cls._last_api_key = api_key
            return cls._g_client
        except Exception:
            return None

    @classmethod
    def replace_sensitive(cls, source: str, sensitive: str, ai_list=None) -> str:
        text = str(source or "")
        if not sensitive:
            return text
        parts = [
            part.strip()
            for part in str(sensitive).split("|")
            if part.strip()
        ]
        if parts:
            pattern = re.compile(
                "|".join(re.escape(part) for part in parts),
                re.IGNORECASE,
            )
            text = pattern.sub("", text)
        for block in ai_list or []:
            if block:
                text = text.replace(str(block), "")
        return text

    @classmethod
    def check_sensitive(
        cls,
        source: str,
        sensitive: str,
        ai_list=None,
    ) -> Tuple[bool, str]:
        text = str(source or "")
        parts = [
            part.strip()
            for part in str(sensitive or "").split("|")
            if part.strip()
        ]
        if parts:
            pattern = re.compile(
                "|".join(re.escape(part) for part in parts),
                re.IGNORECASE,
            )
            match = pattern.search(text)
            if match:
                return True, match.group(0)
        for block in ai_list or []:
            if block and str(block) in text:
                return True, str(block)
        return False, ""

    @classmethod
    def no_semantic(cls, text: str) -> bool:
        source = str(text or "")
        return not any(
            unicodedata.category(ch).startswith(("L", "N"))
            for ch in source
        )

    @classmethod
    def _open_client_and_prompt(cls, api_key: str, employee=None, tar_length: int = 0):
        client = cls.obtain_open_ai_client(api_key)
        model = getattr(employee, "model", "") if employee is not None else ""
        role = getattr(employee, "role", "") if employee is not None else ""
        pre_text = getattr(employee, "pre_text", "") if employee is not None else ""
        pre_message = pre_text.replace("{length}", str(tar_length))
        return client, model, pre_message, role

    @classmethod
    def _invoke(
        cls,
        client,
        model: str,
        pre_message: str,
        role: str,
        source_without_sensitive: str,
    ):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": pre_message or role or "system"},
                {"role": "user", "content": source_without_sensitive},
            ],
            temperature=0.6,
            max_tokens=min(1000, max(1, len(source_without_sensitive))),
        )
        refused, detail = cls._detect_api_refusal(response)
        if refused:
            raise RuntimeError("AI 拒绝生成文案（" + detail + "）")
        choice = response.choices[0]
        content = getattr(choice.message, "content", "") or ""
        return content

    @classmethod
    def final_gen_ai_text(
        cls,
        client,
        model: str,
        tar_length: int = 0,
        pre_message: str = "",
        role: str = "",
        source_without_sensitive: str = "",
        origin_source: str = "",
        write_cache: bool = True,
        echo_generated_before_usage_log: bool = True,
        result_print: bool = False,
    ):
        try:
            text = cls._invoke(
                client,
                model,
                pre_message,
                role,
                source_without_sensitive,
            )
            if write_cache:
                TextCache.AI_TXT_GEN_CACHE_LIST.append(
                    TextCacheBean(
                        source=origin_source,
                        genText=text,
                        log=json.dumps(
                            {"model": model, "length": tar_length},
                            ensure_ascii=False,
                        ),
                    )
                )
            if result_print:
                print("AI输出文案： " + text)
            return AiTextGenStatus.SUCCESS, text
        except Exception:
            return AiTextGenStatus.FAILED, origin_source

    @classmethod
    def generate_text(
        cls,
        source: str,
        employee=None,
        api_key: str = "",
        production: bool = True,
        need_try: bool = False,
        result_print: bool = False,
        retry_count: int = 0,
    ):
        origin_source = str(source or "")
        sensitive = getattr(employee, "sensitive", "") if employee is not None else ""
        source_without_sensitive = cls.replace_sensitive(origin_source, sensitive)
        if cls.no_semantic(source_without_sensitive):
            print("去敏感词后文本无实质语义内容，跳过 AI 生成")
            return AiTextGenStatus.FAILED, origin_source
        try:
            tar_length = utils.calculate_target_length(
                source_without_sensitive,
                getattr(employee, "word_min", 20) if employee is not None else 20,
                getattr(employee, "word_max", 100) if employee is not None else 100,
            )
            client, model, pre_message, role = cls._open_client_and_prompt(
                api_key,
                employee,
                tar_length,
            )
            if client is None:
                print(" AI Client is None！")
                return AiTextGenStatus.FAILED, origin_source
            return cls.final_gen_ai_text(
                client,
                model,
                tar_length,
                pre_message,
                role,
                source_without_sensitive,
                origin_source,
                result_print=result_print,
            )
        except Exception as exc:
            if cls._is_content_policy_error(exc):
                return AiTextGenStatus.REFUSED, origin_source
            return AiTextGenStatus.FAILED, origin_source
