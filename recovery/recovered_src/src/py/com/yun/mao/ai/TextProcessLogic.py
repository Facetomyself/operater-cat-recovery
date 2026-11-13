# Recovered module: src.py.com.yun.mao.ai.TextProcessLogic
from __future__ import annotations

from .AiTextGenFlow import AiTextGenFlow
from .AiTextGenStatus import AiTextGenStatus
from . import TextCache
from ..config import YunYinMaoConfig, tabl_cache
from ..dclass import LoadEmployeeClass
from ..fea import _sq_jqm
from ..link._fds_jm import sec
from ..util.need.CommonCode import MessageMyObj


def _repeat_print(msg: str, times: int = 3):
    for _ in range(max(0, int(times))):
        print(msg)


def process_text_inner(obj, aiBean, api_key):
    source = str(getattr(obj, "text", obj) or "")
    max_attempts = max(
        1,
        int(getattr(YunYinMaoConfig, "AI_GEN_MAX_TRY_COUNT", 1) or 1),
    )
    retry_count = 0
    last_status = None
    generated = source
    for attempt in range(1, max_attempts + 1):
        _repeat_print(f"第{attempt}次，AI生成文本...")
        status, generated = AiTextGenFlow.generate_text(
            source,
            employee=aiBean,
            api_key=api_key,
            production=True,
            need_try=False,
        )
        last_status = status
        if status == AiTextGenStatus.SUCCESS:
            try:
                setattr(obj, "text", generated)
            except Exception:
                pass
            return str(generated or source)
        retry_count += 1
        if status == AiTextGenStatus.REFUSED:
            _repeat_print(
                f"AI 拒绝生成该文案（已尝试 {retry_count} 次）"
            )
        else:
            _repeat_print(
                f"AI生产文本遇到问题，尝试了{retry_count}次，"
                "都生成失败了，请检查原因！"
            )

    if last_status == AiTextGenStatus.REFUSED:
        for_mat = getattr(obj, "for_mat", "") if obj is not None else ""
        TextCache.ALL_MESSAGE_REFUSED_LIST.append(
            MessageMyObj(for_mat, generated, True)
        )
        try:
            setattr(obj, "ai_refused", True)
        except Exception:
            pass
    else:
        TextCache.ALL_MESSAGE_FAILED_LIST.append(obj)
    _repeat_print("将会使用源文案发布")
    return generated or source


def process_text_by_ai_if_need(text, auto, bean=None):
    source = str(text or "")
    try:
        info = getattr(_sq_jqm, "current_account_info", None)
        checker = getattr(info, "has_ai_ability", None)
        if callable(checker):
            try:
                if not checker():
                    _repeat_print(sec("ai_no_hy_nl_01"))
                    return source
            except Exception:
                pass

        employee = (
            getattr(auto, "aiEmployee", None)
            or getattr(auto, "aiBean", None)
        )
        if not employee:
            uid = getattr(bean, "uid", "") or getattr(auto, "uid", "")
            if uid:
                try:
                    employee = LoadEmployeeClass.getAiEmployee(uid)
                except Exception:
                    employee = None
        if not employee:
            _repeat_print(sec("ai_no_yg_tpl_04"))
            return source

        api_key = (
            getattr(bean, "api_key", "")
            or getattr(auto, "api_key", "")
        )
        if not api_key:
            try:
                api_key = tabl_cache.INSTANCE().read_cache(
                    tabl_cache.AI_EMPLOYEE_GROUP,
                    tabl_cache.AI_EMPLOYEE_API_KEY,
                    "",
                )
            except Exception:
                api_key = ""
        api_key = str(api_key or "")
        if api_key and not api_key.startswith("xai-"):
            _repeat_print(
                "api_key API Key 格式错误，必须以 'xai-' 开头，请你重新配置！"
            )
            return source

        if not employee or not getattr(employee, "enable", True):
            return source

        target = bean if bean is not None else source
        if bean is not None:
            try:
                setattr(bean, "text", source)
            except Exception:
                pass
        return process_text_inner(target, employee, api_key)
    except Exception:
        return source
