# Recovered module: src.py.com.yun.mao.auto.AutoWorkerWrapper
# Function names, argument names and code-object metadata are recovered from
# the module init.  The orchestration below follows the decompiled call sites;
# branches marked "inferred" are conservative fallbacks where a dependency was
# not yet recoverable.
from __future__ import annotations

import asyncio
import importlib
import inspect
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from ..record.PublishIdRecord import append_if_complete


TIME_EXE_THRESHOLD = 6000


@dataclass
class _GroupResult:
    real_time_message_id: int = 0
    need_sleep: bool = False
    send_count: int = 0
    send_group: int = 0
    sended_messages: Any = None
    need_continue: bool = False
    need_break: bool = False
    dest_id_map: Any = None
    preview_id_map: Any = None
    send_success_count: int = 0
    ai_refused: bool = False
    protect_content: bool = False
    stop_all_flag: bool = False

    def skip_group(self):
        self.need_continue = False
        self.need_break = False
        return self

    def stop_all(self):
        self.need_break = True
        self.need_continue = False
        return self

    def mark_ai_refused(self):
        self.ai_refused = True
        return self


@dataclass
class _FlowResult:
    real_time_message_id: int = 0
    send_success_count: int = 0
    orign_message: Any = None
    need_continue: bool = False
    dest_id_map: Any = None
    preview_id_map: Any = None


@dataclass
class _ProtectResult:
    real_time_message_id: int = 0
    send_success_count: int = 0
    orign_message: Any = None
    dest_id_map: Any = None
    ai_refused: bool = False
    has_exception: bool = False
    stop_all_flag: bool = False
    protect_content: bool = True

    def stop_all(self):
        self.stop_all_flag = True
        return self


@dataclass
class _ForeachTotals:
    group_result: Any = None
    sended_messages: List[Any] = field(default_factory=list)

    def apply_group_result(self, result):
        self.group_result = result
        messages = getattr(result, "sended_messages", None)
        if messages:
            self.sended_messages.extend(list(messages))
        return self

    def to_shared_results(self) -> dict:
        return {
            "group_result": self.group_result,
            "sended_messages": list(self.sended_messages),
        }

    def to_return_tuple(self):
        result = self.group_result
        if result is None:
            return 0, 0, 0, list(self.sended_messages)
        return (
            int(getattr(result, "real_time_message_id", 0) or 0),
            int(getattr(result, "send_count", 0) or 0),
            int(getattr(result, "send_group", 0) or 0),
            list(getattr(result, "sended_messages", None) or self.sended_messages),
        )


def _optional_import(module_name: str, attribute: Optional[str] = None):
    """Import a project module lazily and tolerate unfinished recovery stubs."""

    try:
        module = importlib.import_module(module_name, __package__)
    except Exception:
        return None
    if attribute is None:
        return module
    return getattr(module, attribute, None)


async def _maybe_await(value):
    if inspect.isawaitable(value):
        return await value
    return value


async def _call_maybe(func, *args, **kwargs):
    if not callable(func):
        return None
    return await _maybe_await(func(*args, **kwargs))


async def _call_adapted(func, positional: Sequence[Any], values: Dict[str, Any]):
    """Call an unfinished helper with only the keywords it actually declares."""

    if not callable(func):
        return None
    try:
        signature = inspect.signature(func)
    except (TypeError, ValueError):
        return await _call_maybe(func, *positional)
    kwargs = {
        key: value
        for key, value in values.items()
        if key in signature.parameters
        and signature.parameters[key].kind
        in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
    }
    try:
        return await _call_maybe(func, *positional, **kwargs)
    except TypeError:
        return await _call_maybe(func, *positional)


def _set_attr(obj, name: str, value):
    try:
        setattr(obj, name, value)
    except Exception:
        return obj
    return obj


def _result_class():
    return (
        _optional_import("..util.need.AllBeanDef", "ParseGroupSendResult")
        or _GroupResult
    )


def _flow_result_class():
    return _optional_import("..util.need.AllBeanDef", "FlowYunSendResult") or _FlowResult


def _protect_result_class():
    return (
        _optional_import("..util.need.AllBeanDef", "BanYunProtectSendResult")
        or _ProtectResult
    )


def _totals_class():
    return _optional_import("..util.need.AllBeanDef", "ForeachTotals") or _ForeachTotals


def _new_result(cls, **kwargs):
    try:
        result = cls()
    except Exception:
        result = _GroupResult()
    for key, value in kwargs.items():
        _set_attr(result, key, value)
    return result


def _new_group_result(**kwargs):
    return _new_result(_result_class(), **kwargs)


def _new_flow_result(**kwargs):
    return _new_result(_flow_result_class(), **kwargs)


def _new_protect_result(**kwargs):
    return _new_result(_protect_result_class(), **kwargs)


def _flag(obj, name: str, default: bool = False) -> bool:
    value = getattr(obj, name, default)
    if callable(value):
        try:
            value = value()
        except Exception:
            return default
    return bool(value)


def _working():
    return _optional_import("..cd", "Working")


def _process_cache():
    return _optional_import(".ProcessCache")


def _stop_requested() -> bool:
    working = _working()
    return bool(getattr(working, "need_stop", False)) if working else False


def _print_trace() -> None:
    helper = _optional_import("..util", "TracePrinterHelper")
    printer = getattr(helper, "print_trace", None)
    if callable(printer):
        try:
            printer()
            return
        except Exception:
            return
    import traceback

    traceback.print_exc()


def _as_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _message_id(value) -> int:
    return _as_int(getattr(value, "id", value), 0)


def _get_source(auto) -> str:
    getter = getattr(auto, "getSource", None)
    if callable(getter):
        try:
            value = getter()
            if value is not None:
                return str(value)
        except Exception:
            return str(getattr(auto, "source", "") or "")
    return str(getattr(auto, "source", "") or "")


def _get_destinations(auto) -> List[Any]:
    for name in ("getDestes", "getDest", "getAdDest"):
        getter = getattr(auto, name, None)
        if callable(getter):
            try:
                values = getter()
                if values is not None:
                    return list(values or [])
            except Exception:
                continue
    for name in ("destes", "destList", "dest_id_map"):
        values = getattr(auto, name, None)
        if values:
            return list(values.keys()) if isinstance(values, dict) else list(values)
    return []


def _parse_messages(parse) -> List[Any]:
    getter = getattr(parse, "getMessages", None)
    if callable(getter):
        try:
            values = getter()
            if inspect.isawaitable(values):
                return []
            if values is not None:
                return list(values)
        except Exception:
            return []
    return list(getattr(parse, "messages", None) or [])


def _parse_medias(parse) -> List[Any]:
    getter = getattr(parse, "getMedias", None)
    if callable(getter):
        try:
            values = getter()
            if inspect.isawaitable(values):
                return []
            if values is not None:
                return list(values)
        except Exception:
            return []
    values = getattr(parse, "medias", None)
    return list(values or [])


def _parse_ids(parse) -> List[int]:
    values = (
        getattr(parse, "original_msg_ids", None)
        or getattr(parse, "parse_ids", None)
        or getattr(parse, "message_ids", None)
    )
    if not values:
        values = _parse_messages(parse)
    result: List[int] = []
    for item in values or []:
        msg_id = _message_id(item)
        if msg_id:
            result.append(msg_id)
    return result


def _count_replies(replies) -> int:
    if replies is None:
        return 0
    if hasattr(replies, "replies"):
        replies = getattr(replies, "replies", None)
    try:
        return len(replies)
    except TypeError:
        try:
            return sum(1 for _ in replies)
        except TypeError:
            return 0


def _format_time(seconds) -> str:
    common = _optional_import("..util.need", "CommonCode")
    formatter = getattr(common, "format_time", None)
    if callable(formatter):
        try:
            return str(formatter(int(seconds or 0)))
        except Exception:
            return f"{int(seconds or 0)}s"
    total = max(0, int(seconds or 0))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def _update_forward_mode_text(value: str) -> None:
    cache = _process_cache()
    updater = getattr(cache, "update_forward_mode_text", None)
    if callable(updater):
        try:
            updater(value)
        except Exception:
            return


def _update_sub_type_text(value: str) -> None:
    cache = _process_cache()
    updater = getattr(cache, "update_sub_type_text", None)
    if callable(updater):
        try:
            updater(value)
        except Exception:
            return


def _wd_run(args_wrapper, auto):
    ticket = getattr(auto, "ticket", None)
    if ticket is None:
        ticket = getattr(args_wrapper, "ticket", None)
    mode = (
        getattr(args_wrapper, "mode", None)
        or getattr(auto, "mode", None)
        or ""
    )
    mode = str(mode).strip().lower()
    convert_mode = str(getattr(args_wrapper, "convert_mode", "") or "").strip().lower()
    return {
        "ticket": ticket,
        "mode": mode,
        "monitor": mode == "monitor",
        "convert_mode": convert_mode,
        "auto": auto,
        "args_wrapper": args_wrapper,
    }


def _parse_group_result_from_flow_yun(auto, flow, result=None):
    if result is None:
        result = _new_group_result()
    if flow is None:
        return result
    send_success_count = _as_int(
        getattr(flow, "send_success_count", getattr(flow, "send_count", 0))
    )
    _set_attr(result, "real_time_message_id", getattr(flow, "real_time_message_id", 0))
    _set_attr(result, "send_count", send_success_count)
    _set_attr(
        result,
        "send_group",
        1 if send_success_count or getattr(flow, "dest_id_map", None) else 0,
    )
    _set_attr(result, "send_success_count", send_success_count)
    _set_attr(result, "sended_messages", getattr(flow, "dest_id_map", None))
    _set_attr(result, "dest_id_map", getattr(flow, "dest_id_map", None))
    _set_attr(result, "preview_id_map", getattr(flow, "preview_id_map", None))
    _set_attr(result, "need_continue", bool(getattr(flow, "need_continue", False)))
    _set_attr(result, "need_sleep", True)
    return result


def _parse_group_result_from_protect(auto, protect, send_to_comment=False):
    result = _new_group_result(
        real_time_message_id=getattr(auto, "real_time_message_id", 0),
        protect_content=True,
    )
    if protect is None:
        return result.stop_all()
    send_success_count = _as_int(getattr(protect, "send_success_count", 0))
    _set_attr(result, "send_count", send_success_count)
    _set_attr(result, "send_success_count", send_success_count)
    _set_attr(
        result,
        "send_group",
        1 if send_success_count or getattr(protect, "dest_id_map", None) else 0,
    )
    _set_attr(result, "sended_messages", getattr(protect, "dest_id_map", None))
    _set_attr(result, "dest_id_map", getattr(protect, "dest_id_map", None))
    _set_attr(result, "send_to_comment", bool(send_to_comment))
    _set_attr(result, "ai_refused", bool(getattr(protect, "ai_refused", False)))
    if getattr(protect, "ai_refused", False):
        marker = getattr(result, "mark_ai_refused", None)
        if callable(marker):
            marker()
    if getattr(protect, "stop_all_flag", False) or getattr(protect, "has_exception", False):
        stop = getattr(result, "stop_all", None)
        if callable(stop):
            stop()
        else:
            _set_attr(result, "need_break", True)
    return result


def _print_send_success_count(send_to_comment, send_success_count):
    count = _as_int(send_success_count)
    if count <= 0:
        print("发布失败了")
        return
    print("成功发送", count, "个消息！")


async def _collect_comment_destinations(auto, client):
    common = _optional_import("..util.need", "CommonCode")
    utils = _optional_import("..util.need", "utils")
    checker = getattr(common, "check_comment_enable", None)
    comment_list: List[Any] = []
    not_comment_list: List[Any] = []
    for dest in _get_destinations(auto):
        channel_part = dest
        if utils is not None:
            try:
                channel_part, _ = utils.parse_source_parts(str(dest))
                channel_part = utils.convertPrivateIdIfNeed(channel_part)
            except Exception:
                channel_part = dest
        enabled = True
        if callable(checker):
            try:
                enabled = await _maybe_await(checker(channel_part))
            except Exception:
                enabled = True
        if enabled:
            comment_list.append(dest)
        else:
            not_comment_list.append(dest)
    return comment_list, not_comment_list


async def _generic_send(
    auto,
    client,
    parse,
    args_wrapper,
    log_pre_tag="",
    dest_to_map=None,
    protect=False,
    send_to_comment=False,
):
    """Inferred fallback when a ban-yun/flow helper is still a skeleton."""

    cmcode = _optional_import(".CMCode")
    if cmcode is not None:
        func = getattr(cmcode, "send_message_only", None)
        if callable(func):
            messages = _parse_messages(parse)
            text = str(getattr(parse, "tart_text", "") or "")
            if not text:
                text = " ".join(str(getattr(item, "message", item)) for item in messages)
            result = await _call_adapted(
                func,
                (),
                {
                    "auto": auto,
                    "client": client,
                    "destes": _get_destinations(auto),
                    "dest_to_map": dest_to_map or {},
                    "album": _parse_medias(parse),
                    "tart_text": text,
                    "for_mat": getattr(parse, "for_mat", None),
                    "is_video_or_photo": getattr(parse, "isVideoOrPhoto", None),
                    "log_pre_tag": log_pre_tag,
                    "src_topic_id": getattr(parse, "topic_id", 0),
                    "part_contexts": getattr(args_wrapper, "part_contexts", None) or [],
                },
            )
            if isinstance(result, int):
                count = result
            elif isinstance(result, (list, tuple, set, dict)):
                count = len(result)
            else:
                count = _as_int(
                    getattr(
                        result,
                        "send_success_count",
                        getattr(result, "send_count", 0),
                    )
                )
            return _new_group_result(
                real_time_message_id=getattr(auto, "real_time_message_id", 0),
                send_count=count,
                send_success_count=count,
                send_group=1 if count else 0,
                sended_messages=result if isinstance(result, (list, dict)) else None,
                need_sleep=True,
                protect_content=protect,
                send_to_comment=send_to_comment,
            )

    sender = getattr(client, "send_message", None)
    count = 0
    sent = {}
    if callable(sender):
        for dest in _get_destinations(auto):
            if _stop_requested():
                break
            text = str(getattr(parse, "tart_text", "") or "")
            try:
                message = await _maybe_await(sender(dest, text))
            except Exception:
                _print_trace()
                continue
            count += 1
            sent[dest] = [_message_id(message)]
    return _new_group_result(
        real_time_message_id=getattr(auto, "real_time_message_id", 0),
        send_count=count,
        send_success_count=count,
        send_group=1 if count else 0,
        sended_messages=sent or None,
        need_sleep=True,
        protect_content=protect,
        send_to_comment=send_to_comment,
    )


async def _process_flow_or_yun_send(
    auto,
    client,
    parse,
    args_wrapper,
    log_pre_tag="",
    *,
    is_auto_flow=False,
    is_yun=False,
):
    flow_result = None
    try:
        r_v3_edge = _wd_run(args_wrapper, auto)
        if is_yun:
            module = _optional_import(".YunProcess")
            func = getattr(module, "send_yun_process", None)
        else:
            module = _optional_import(".FlowProcess")
            func = getattr(module, "send_flow_process", None)
        if callable(func):
            flow_result = await _call_adapted(
                func,
                (),
                {
                    "auto": auto,
                    "client": client,
                    "parse": parse,
                    "args_wrapper": args_wrapper,
                    "argsWrapper": args_wrapper,
                    "log_pre_tag": log_pre_tag,
                    "r_v3_edge": r_v3_edge,
                    "is_auto_flow": is_auto_flow,
                    "is_yun": is_yun,
                },
            )
        else:
            flow_result = await _generic_send(
                auto,
                client,
                parse,
                args_wrapper,
                log_pre_tag=log_pre_tag,
            )
        return _parse_group_result_from_flow_yun(auto, flow_result)
    except Exception:
        _print_trace()
        return _new_group_result(need_sleep=True)


async def processPreviewFlowSend(auto, client, parse, argsWrapper, log_pre_tag=""):
    return await _process_flow_or_yun_send(
        auto,
        client,
        parse,
        argsWrapper,
        log_pre_tag,
        is_auto_flow=False,
        is_yun=False,
    )


async def processAutoFlowSend(auto, client, parse, argsWrapper, log_pre_tag=""):
    return await _process_flow_or_yun_send(
        auto,
        client,
        parse,
        argsWrapper,
        log_pre_tag or "自动流>>",
        is_auto_flow=True,
        is_yun=False,
    )


async def processYunAutoSend(auto, client, parse, argsWrapper, log_pre_tag=""):
    return await _process_flow_or_yun_send(
        auto,
        client,
        parse,
        argsWrapper,
        log_pre_tag or "云自动>>",
        is_auto_flow=True,
        is_yun=True,
    )


async def processYunPreViewSend(auto, client, parse, argsWrapper, log_pre_tag=""):
    return await _process_flow_or_yun_send(
        auto,
        client,
        parse,
        argsWrapper,
        log_pre_tag or "云预览>>",
        is_auto_flow=False,
        is_yun=True,
    )


async def processDownLoad(auto, client, parse, argsWrapper):
    try:
        module = _optional_import(".DownLoadProcess")
        func = getattr(module, "only_down_load", None)
        if callable(func):
            download_result = await _call_adapted(
                func,
                (),
                {
                    "client": client,
                    "parse": parse,
                    "log_pre_tag": "单纯下载>>",
                    "auto": auto,
                    "argsWrapper": argsWrapper,
                },
            )
        else:
            download_result = await _generic_send(
                auto,
                client,
                parse,
                argsWrapper,
                log_pre_tag="单纯下载>>",
            )
        count = _as_int(
            getattr(
                download_result,
                "send_success_count",
                getattr(download_result, "send_count", 0),
            )
        )
        print("成功下载", count, "个资源！")
        return _new_group_result(
            real_time_message_id=getattr(auto, "real_time_message_id", 0),
            need_sleep=True,
            send_count=count,
            send_success_count=count,
            send_group=1 if count else 0,
            sended_messages=getattr(download_result, "sended_messages", None),
        )
    except Exception:
        _print_trace()
        return _new_group_result(need_sleep=True)


async def processRepliesIfNeed(
    t_send_count,
    dest_id_map,
    auto,
    client,
    parse,
    argsWrapper,
):
    result = _new_group_result(
        real_time_message_id=getattr(auto, "real_time_message_id", 0),
        send_count=_as_int(t_send_count),
        send_success_count=_as_int(t_send_count),
        dest_id_map=dest_id_map,
    )
    try:
        comment_rule = getattr(auto, "commentRule", None) or getattr(auto, "replies", None)
        if not getattr(comment_rule, "enable", True):
            return result
        comment_list, not_comment_list = await _collect_comment_destinations(auto, client)
        if not comment_list:
            print("目标频道都没有开启评论区，不会复刻评论区！")
            return result
        if not_comment_list:
            print(">>>以下目标频道没有开启评论区")
        if comment_list:
            print("部分目标频道开启了评论区")

        common = _optional_import("..util.need", "CommonCode")
        source = _get_source(auto)
        source_ids = _parse_ids(parse)
        want_count = min(_as_int(getattr(comment_rule, "wantCount", 10), 10), 10)
        collected: Dict[int, List[Any]] = {}
        print("正在采集评论区消息...")
        for source_id in source_ids:
            if _stop_requested():
                print("手动停止成功！")
                break
            getter = getattr(common, "get_channel_messages_replies", None)
            replies = None
            if callable(getter):
                try:
                    replies = await _maybe_await(
                        getter(
                            client,
                            source,
                            reply_to=source_id,
                            limit=want_count,
                            prefix="rg_awr_cm_raw_tpl_01",
                        )
                    )
                except Exception:
                    replies = None
            if replies:
                collected[source_id] = list(replies)
        count = sum(_count_replies(value) for value in collected.values())
        print("正在开始发布到评论区资源...")
        _update_sub_type_text(">>复刻评论区")
        if not collected:
            print("评论区本组目标均已搬运，跳过发送（不生成文案、不等待）。")
            return result

        ledger = _optional_import("..record", "CommentCopyLedger")
        skipper = getattr(ledger, "should_skip_comment_group", None)
        if callable(skipper):
            try:
                if await _maybe_await(skipper(auto, collected)):
                    print("评论区本组目标均已搬运，跳过发送（不生成文案、不等待）。")
                    return result
            except Exception:
                _print_trace()

        send_result = await processBanYunSend(
            auto,
            client,
            parse,
            argsWrapper,
            dest_id_map or {},
        )
        _set_attr(result, "send_count", _as_int(t_send_count) + _as_int(count))
        _set_attr(
            result,
            "send_success_count",
            _as_int(getattr(send_result, "send_success_count", t_send_count)),
        )
        _set_attr(result, "dest_id_map", getattr(send_result, "dest_id_map", dest_id_map))
        _set_attr(result, "sended_messages", getattr(send_result, "sended_messages", None))
        _set_attr(result, "_main_send_done", True)
        if is_comment_privateAd_available(comment_rule):
            print("正在向评论区发布私有广告...")
            print(">>发布评论区广告")
            await publish_private_ad(
                argsWrapper,
                auto,
                client,
                getattr(auto, "selfAdWrapper", None),
            )
        print("发布到评论区完成！")
        return result
    except Exception:
        _print_trace()
        return result


async def processBanYunSendWrapper(auto, client, parse, argsWrapper):
    try:
        replies_result = await processRepliesIfNeed(
            0,
            {},
            auto,
            client,
            parse,
            argsWrapper,
        )
        if getattr(replies_result, "need_break", False):
            return replies_result
        if getattr(replies_result, "_main_send_done", False):
            return replies_result
        return await processBanYunSend(
            auto,
            client,
            parse,
            argsWrapper,
            getattr(replies_result, "dest_id_map", {}) or {},
        )
    except Exception:
        _print_trace()
        return _new_group_result(need_sleep=True)


async def processBanYunSend(auto, client, parse, argsWrapper, dest_to_map=None):
    try:
        if getattr(auto, "isProtectContent", False):
            _update_forward_mode_text("保护内容>>")
            module = _optional_import(".BanYunProtect")
            func = getattr(module, "send_message_protect", None)
            protect_result = None
            if callable(func):
                protect_result = await _call_adapted(
                    func,
                    (),
                    {
                        "auto": auto,
                        "client": client,
                        "parse": parse,
                        "argsWrapper": argsWrapper,
                        "dest_to_map": dest_to_map or {},
                    },
                )
            else:
                protect_result = await _generic_send(
                    auto,
                    client,
                    parse,
                    argsWrapper,
                    protect=True,
                )
            result = _parse_group_result_from_protect(auto, protect_result)
            _print_send_success_count(
                getattr(result, "send_to_comment", False),
                getattr(result, "send_success_count", 0),
            )
            return result

        helper = _optional_import("..dclass.DTopClassHelper", "DTopClassHelper")
        action_download = getattr(helper, "ACTION_DOWNLOAD", None)
        action = getattr(getattr(auto, "forWardAction", None), "action", None)
        if action_download is not None and action == action_download:
            _update_forward_mode_text("强制下载>>")
        else:
            _update_forward_mode_text(">>")

        r_v3_edge = _wd_run(argsWrapper, auto)
        module = _optional_import(".BanYunUnProtect")
        func = getattr(module, "send_message_un_protect", None)
        unprotect = None
        if callable(func):
            unprotect = await _call_adapted(
                func,
                (),
                {
                    "auto": auto,
                    "client": client,
                    "parse": parse,
                    "argsWrapper": argsWrapper,
                    "dest_to_map": dest_to_map or {},
                    "r_v3_edge": r_v3_edge,
                },
            )
        else:
            unprotect = await _generic_send(
                auto,
                client,
                parse,
                argsWrapper,
                dest_to_map=dest_to_map or {},
            )
        if unprotect is None:
            print("发送出现异常，请解决异常再重试！")
            return _new_group_result(need_sleep=True).stop_all()

        result_class = _result_class()
        factory = getattr(result_class, "from_unprotect_send", None)
        result = None
        if callable(factory):
            try:
                result = factory(unprotect)
            except Exception:
                result = None
        if result is None:
            count = _as_int(getattr(unprotect, "send_success_count", 0))
            result = _new_group_result(
                real_time_message_id=getattr(auto, "real_time_message_id", 0),
                send_count=count,
                send_success_count=count,
                send_group=1 if count else 0,
                sended_messages=getattr(unprotect, "dest_id_map", None),
                dest_id_map=getattr(unprotect, "dest_id_map", None),
                need_sleep=True,
            )
        _print_send_success_count(
            getattr(result, "send_to_comment", False),
            getattr(result, "send_success_count", 0),
        )
        remember_random_send_id(auto, getattr(unprotect, "orign_message", None))
        return result
    except Exception:
        _print_trace()
        return _new_group_result(need_sleep=True).stop_all()


def remember_random_send_id(auto, orign_message):
    ids = getattr(auto, "random_send_ids", None)
    if ids is None:
        ids = []
        _set_attr(auto, "random_send_ids", ids)
    msg_id = _message_id(orign_message)
    if msg_id and msg_id not in ids:
        ids.append(msg_id)
    manager = _optional_import("..remember", "RememberManager")
    updater = getattr(manager, "updateRememberIds", None) if manager else None
    if callable(updater):
        try:
            updater(auto, ids)
        except Exception:
            _print_trace()


def is_privateAd_available(auto):
    getter = getattr(auto, "getSelfAdes", None)
    if callable(getter):
        try:
            return bool(getter())
        except Exception:
            return False
    wrapper = getattr(auto, "selfAdWrapper", None)
    return bool(wrapper and getattr(wrapper, "ades", None))


def is_comment_privateAd_available(comment):
    if not comment:
        return False
    if getattr(comment, "adEnable", False):
        return True
    getter = getattr(comment, "getAdDest", None)
    if callable(getter):
        try:
            return bool(getter())
        except Exception:
            return False
    return bool(getattr(comment, "ades", None))


def is_globalAd_available(argsWrapper):
    wrapper = getattr(argsWrapper, "globalAdWrapper", None)
    if wrapper is None:
        top_args = getattr(argsWrapper, "topArgs", None)
        wrapper = getattr(top_args, "globalAdWrapper", None)
    if wrapper is None:
        return False
    return bool(getattr(wrapper, "ades", None) and getattr(wrapper, "adEnable", True))


async def _send_ad(
    client,
    dest,
    ad,
    files,
    parse_mode="html",
    prefix="",
    comment_to=None,
):
    flood = _optional_import("..util.FloodGuard")
    retry = getattr(flood, "with_flood_retry", None) if flood else None
    entity = await _maybe_await(client.get_entity(dest))
    text = str(getattr(ad, "text", "") or "")
    kwargs: Dict[str, Any] = {"parse_mode": parse_mode}
    if comment_to is not None:
        kwargs["comment_to"] = comment_to
    if files:
        sender = getattr(client, "send_file", None)
        call = lambda: sender(entity, files, caption=text, **kwargs)
    else:
        sender = getattr(client, "send_message", None)
        call = lambda: sender(entity, text, **kwargs)
    if not callable(sender):
        return None
    if callable(retry):
        try:
            return await _maybe_await(retry(call, prefix=prefix))
        except TypeError:
            return await _maybe_await(retry(call))
    return await _maybe_await(call())


async def saveAdId(ad, auto, t_dest_id_map, pre):
    for dest, ids in (t_dest_id_map or {}).items():
        print("保存广告ID>>>>", pre, " 的目标频道/群组 ", dest, "，", ids)
        target = getattr(ad, "idMapsByDest", None)
        if isinstance(target, dict):
            target[dest] = ids
        manager = getattr(ad, "updateAdIds", None)
        if callable(manager):
            try:
                await _maybe_await(manager(dest, ids))
            except Exception:
                _print_trace()


async def deleteLastAd(ad, auto, client):
    getter = getattr(ad, "idMapsByDest", None)
    dest_map = getter if isinstance(getter, dict) else {}
    deleter = getattr(client, "delete_messages", None)
    if not callable(deleter):
        return
    for dest, ids in list(dest_map.items()):
        if _stop_requested():
            print("手动停止成功！")
            return
        values = ids if isinstance(ids, (list, tuple, set)) else [ids]
        for msg_id in values:
            try:
                await _maybe_await(deleter(dest, [_as_int(msg_id)]))
            except Exception:
                _print_trace()


async def publish_private_ad(argsWrapper, auto, client, ad):
    if _stop_requested():
        print("手动停止成功！")
        return _new_group_result()
    if not is_privateAd_available(auto):
        return _new_group_result()
    if getattr(ad, "adIsDelete", False):
        await deleteLastAd(ad, auto, client)

    legal_files = getattr(ad, "obtain_legal_files", None)
    files = list(legal_files() or []) if callable(legal_files) else []
    dest_to_map = getattr(auto, "getAdDest", None)
    destinations = list(dest_to_map() or []) if callable(dest_to_map) else []
    if getattr(auto, "dest_to_map", None):
        destinations = destinations or list(getattr(auto, "dest_to_map"))

    _origin_to_upload: Dict[str, Any] = {}
    _part_contexts: list = []
    cmcode = _optional_import(".CMCode")
    upload_only = getattr(cmcode, "upload_only", None) if cmcode else None
    if files and callable(upload_only):
        try:
            uploaded = await _call_adapted(
                upload_only,
                (),
                {
                    "client": client,
                    "pathMessageMap": {path: None for path in files},
                    "origin_to_water_path_map": {},
                    "is_file_upload": True,
                    "spoiler": getattr(ad, "spoiler", False),
                    "log_pre_tag": "私有广告",
                },
            )
            if isinstance(uploaded, tuple) and len(uploaded) >= 2:
                _origin_to_upload = uploaded[0] or {}
                _part_contexts = list(uploaded[1] or [])
        except Exception:
            _print_trace()

    record_module = _optional_import("..record.PublishIdRecord")
    t_dest_id_map: Dict[Any, List[int]] = {}
    print("正在发布私有广告...")
    print("正在发布私有广告>>")
    for dest in destinations:
        if _stop_requested():
            print("手动停止成功！")
            break
        try:
            message = await _send_ad(
                client,
                dest,
                ad,
                files or None,
                parse_mode="html",
                prefix="private_ad/send_message/channel",
            )
            if message is not None:
                t_dest_id_map.setdefault(dest, []).append(_message_id(message))
                recorder = getattr(record_module, "log_publish_success", None)
                if callable(recorder):
                    await _maybe_await(recorder(dest, message))
        except Exception:
            _print_trace()
    if t_dest_id_map:
        await saveAdId(ad, auto, t_dest_id_map, "private_ad")
        print("私有广告发布完成！")
    return _new_group_result(send_success_count=len(t_dest_id_map))


async def publish_global_ad(send_to_comment, auto, client):
    if _stop_requested():
        print("手动停止成功！")
        return _new_group_result()
    args_wrapper = getattr(auto, "topArgs", None) or getattr(auto, "argsWrapper", None)
    wrapper = getattr(args_wrapper, "globalAdWrapper", None)
    if wrapper is None:
        wrapper = getattr(auto, "globalAdWrapper", None)
    if wrapper is None:
        return _new_group_result()
    if not is_globalAd_available(args_wrapper or auto):
        return _new_group_result()
    ad = getattr(wrapper, "ad", None) or wrapper
    if getattr(ad, "adIsDelete", False):
        await deleteLastAd(ad, auto, client)
    files = []
    getter = getattr(ad, "obtain_legal_files", None)
    if callable(getter):
        try:
            files = list(getter() or [])
        except Exception:
            files = []
    destinations = getattr(wrapper, "getAdDest", None)
    destinations = list(destinations() or []) if callable(destinations) else []
    record_module = _optional_import("..record.PublishIdRecord")
    t_dest_id_map: Dict[Any, List[int]] = {}
    print("正在发布全局广告...")
    print("正在发布全局广告>>")
    for dest in destinations:
        if _stop_requested():
            print("手动停止成功！")
            break
        try:
            message = await _send_ad(
                client,
                dest,
                ad,
                files or None,
                parse_mode="html",
                prefix="global_ad/send_message/channel",
                comment_to=getattr(ad, "comment_to_id", None) if send_to_comment else None,
            )
            if message is not None:
                t_dest_id_map.setdefault(dest, []).append(_message_id(message))
                recorder = getattr(record_module, "log_publish_success", None)
                if callable(recorder):
                    await _maybe_await(recorder(dest, message))
        except Exception:
            _print_trace()
    if t_dest_id_map:
        await saveAdId(ad, auto, t_dest_id_map, "global_ad")
        print("全局广告发布完成！")
    return _new_group_result(send_success_count=len(t_dest_id_map))


async def process_ad_second_to_last(index, auto, client, parseList, argsWrapper):
    try:
        if getattr(auto, "adIsBottomUp", False):
            print("正在向评论区发布私有广告...")
        if is_privateAd_available(auto):
            await publish_private_ad(
                argsWrapper,
                auto,
                client,
                getattr(auto, "selfAdWrapper", None),
            )
        if is_globalAd_available(argsWrapper):
            await publish_global_ad(False, auto, client)
    except Exception:
        _print_trace()


def updateByIncreaseWithRTID(auto, rt_msg_id):
    mem_auto = getattr(auto, "mem_auto", None)
    module = _optional_import("..dclass.AutoBeanXXX")
    registry = getattr(module, "mem_auto_for_writeback", None) if module else None
    if mem_auto is None and isinstance(registry, dict):
        mem_auto = registry.get(getattr(auto, "kid", None))
    if mem_auto is None:
        print("顺序 startId 写回失败：内存中找不到 kid=", getattr(auto, "kid", ""))
        return
    new_start_id = _as_int(rt_msg_id)
    params = getattr(mem_auto, "real_time_increase_params", None)
    if isinstance(params, dict):
        params["startId"] = new_start_id
        return
    _set_attr(mem_auto, "real_time_increase_params", {"startId": new_start_id})


def headerLogInfo(auto, process_str):
    lines = ["======================================"]
    common = _optional_import("..util.need", "CommonCode")
    version_code = getattr(common, "version_code", None)
    version = version_code() if callable(version_code) else getattr(auto, "version", "")
    lines.append(f"=======软件版本：{version or ''}")
    lines.append("=======执行开始")
    lines.append(f"=======名称>>  {getattr(auto, 'name', '') or ''}")
    lines.append(f"=======来源>>  {_get_source(auto)}")
    destinations = _get_destinations(auto)
    lines.append(f"=======目标>>  {destinations or getattr(auto, 'destes', '') or ''}")
    mode = getattr(auto, "auto_desc", None) or getattr(auto, "mode", None)
    lines.append(f"=======模式>>  {mode or process_str or ''}")
    action_text = getattr(auto, "get_action_text", None)
    action_text = action_text() if callable(action_text) else getattr(auto, "action", "")
    lines.append(f"=======搬运方式>>  {action_text or ''}")
    replies = getattr(auto, "commentRule", None) or getattr(auto, "replies", None)
    lines.append(f"=======评论区>>  {bool(getattr(replies, 'enable', False))}")
    if replies is not None:
        lines.append(
            f"=======评论区详情>>  {getattr(replies, 'replies_info_detail', '') or ''}"
        )
    resource_text = getattr(auto, "get_resource_text", None)
    resource_text = resource_text() if callable(resource_text) else getattr(auto, "dtype", "")
    lines.append(f"=======类型>>  {resource_text or ''}")
    water = getattr(auto, "water", "") or ""
    lines.append(f"=======水印>>  {water}")
    lines.append("======================================")
    return "\n".join(lines)


def completeItemSummery(
    auto,
    autoBeans,
    start_time,
    success_rt_msg_id,
    total_send_count,
    total_send_group,
    index,
):
    execution_time = max(0.0, time.time() - float(start_time or time.time()))
    if _flag(auto, "isBanYunType"):
        tag, unit, verb = "搬运流", "消息", "搬运了"
    elif _flag(auto, "isAutoFlowType"):
        tag, unit, verb = "自动流", "消息", "搬运了"
    elif _flag(auto, "isYuLanFlowType"):
        tag, unit, verb = "预览流", "消息", "搬运了"
    elif _flag(auto, "isDownLoadFlowType"):
        tag, unit, verb = "下载流", "资源", "下载了"
    else:
        tag, unit, verb = "搬运流", "消息", "搬运了"
    bean_count = len(list(autoBeans or []))
    text = (
        f"=======执行完成（{tag}）：{getattr(auto, 'name', '') or ''}"
        " >> 执行完成，耗时："
        f"{_format_time(execution_time)}  {verb} {_as_int(total_send_count)} {unit} "
        f"（{_as_int(total_send_group)} 组，{bean_count} 个任务，"
        f"最后实时ID：{_as_int(success_rt_msg_id)}）"
    )
    print(text)
    return text


def print_summery(summery_list):
    text_cache = _optional_import("..ai.TextCache")
    cache_list = getattr(text_cache, "AI_TXT_GEN_CACHE_LIST", None) if text_cache else None
    refused = getattr(text_cache, "ALL_MESSAGE_REFUSED_LIST", None) if text_cache else None
    failed = getattr(text_cache, "ALL_MESSAGE_FAILED_LIST", None) if text_cache else None
    print("==================================================")
    print("====================执行报告开始====================")
    for item in summery_list or []:
        print(str(item))
    for source, title in (
        (cache_list, "AI报告"),
        (failed, "错误信息报告"),
        (refused, "AI 拒绝生成报告"),
    ):
        if not source:
            continue
        print(f"{title}开始")
        for item in list(source):
            text = getattr(item, "genText", None) or getattr(item, "tip", None) or str(item)
            print(text)
        print(f"{title}结束")
    print("====================执行报告结束====================")


async def foreachToSend(
    auto,
    client,
    parseList,
    argsWrapper,
    shared_results=None,
    call_back=None,
):
    totals = _totals_class()()
    start_time = time.time()
    total_count = max(1, len(list(parseList or [])))
    current_count = 0
    index = 0
    try:
        print("开始执行任务： ++++++++++++++++++++++++++++++++++++++++++++")
        if not parseList:
            parseList = list(getattr(auto, "parseList", None) or [])
        for index, parse in enumerate(parseList or []):
            if _stop_requested():
                print("手动停止成功！")
                break
            current_count += 1
            cache = _process_cache()
            updater = getattr(cache, "update_present", None)
            if callable(updater):
                try:
                    updater(f"{current_count / total_count: .2%}")
                except Exception:
                    _print_trace()
            source = _get_source(auto)
            parse_ids = _parse_ids(parse)
            try:
                from ..util import SuspendFrozenTag

                kid = str(getattr(auto, "kid", "") or "")
                if kid and parse_ids:
                    SuspendFrozenTag.note_increase_group_progress(kid, parse_ids)
            except Exception:
                pass
            print(
                "开始执行任务： 第: ",
                current_count,
                " 组， ",
                len(_parse_messages(parse)),
                " 个资源， ",
                " ID 列表： ",
                parse_ids,
            )
            try:
                common = _optional_import("..util.need", "CommonCode")
                fetch = getattr(common, "fetch_new_quote_messages", None)
                if callable(fetch):
                    fetched = await _maybe_await(
                        fetch(client, source, parse_ids, prefix="foreachToSend")
                    )
                    if fetched:
                        _set_attr(parse, "messages", list(fetched))
            except Exception:
                print("foreachToSend fetch_new_quote_messages！")
                _print_trace()

            group_result = None
            if _flag(auto, "isBanYunType"):
                group_result = await processBanYunSendWrapper(
                    auto, client, parse, argsWrapper
                )
            elif _flag(auto, "isAutoFlowType"):
                group_result = await processAutoFlowSend(
                    auto, client, parse, argsWrapper, "自动流>>"
                )
            elif _flag(auto, "isYuLanFlowType"):
                group_result = await processPreviewFlowSend(
                    auto, client, parse, argsWrapper, "预览流>>"
                )
            elif _flag(auto, "isDownLoadFlowType"):
                group_result = await processDownLoad(auto, client, parse, argsWrapper)
            elif _flag(auto, "isYunAutoType"):
                if not _bot_ability_available(auto):
                    print("当前你没有开通BOT云猫机器人服务，跳过云自动任务执行！")
                    continue
                group_result = await processYunAutoSend(
                    auto, client, parse, argsWrapper, "云自动>>"
                )
            elif _flag(auto, "isYunPreViewType"):
                if not _bot_ability_available(auto):
                    print("当前你没有开通BOT云猫机器人服务，跳过云预览任务执行！")
                    continue
                group_result = await processYunPreViewSend(
                    auto, client, parse, argsWrapper, "云预览>>"
                )
            else:
                group_result = await processBanYunSendWrapper(
                    auto, client, parse, argsWrapper
                )

            if group_result is not None:
                totals.apply_group_result(group_result)
                try:
                    append_if_complete(
                        auto,
                        parse,
                        group_result,
                        getattr(argsWrapper, "convert_mode", None),
                    )
                except Exception:
                    print("记录发布 ID 映射失败：")
                    _print_trace()
                    continue
                success_rt = _as_int(getattr(group_result, "real_time_message_id", 0))
                if success_rt and _flag(auto, "is_increase_mode"):
                    updateByIncreaseWithRTID(auto, success_rt)
                if shared_results is not None:
                    try:
                        shared_results.update(totals.to_shared_results())
                    except Exception:
                        shared_results["shared_results"] = totals.to_shared_results()
                if getattr(group_result, "need_break", False):
                    break
                if getattr(group_result, "need_sleep", False):
                    sleeper = _optional_import(".BizSleeper")
                    sleep_func = getattr(sleeper, "biz_sleep", None)
                    if callable(sleep_func):
                        try:
                            await _maybe_await(sleep_func(1, 2))
                        except Exception:
                            _print_trace()
                    else:
                        await asyncio.sleep(1)

        return_tuple = totals.to_return_tuple()
        if callable(call_back):
            try:
                callback_result = call_back(*return_tuple)
                if inspect.isawaitable(callback_result):
                    await callback_result
            except TypeError:
                try:
                    callback_result = call_back(return_tuple)
                    if inspect.isawaitable(callback_result):
                        await callback_result
                except Exception:
                    _print_trace()
            except Exception:
                _print_trace()
        elapsed = time.time() - start_time
        print("全部条目执行完成！")
        print(f"耗时：{_format_time(elapsed)}")
        return return_tuple
    except asyncio.CancelledError:
        raise
    except Exception:
        _print_trace()
        return totals.to_return_tuple()


def _bot_ability_available(auto) -> bool:
    info = getattr(auto, "current_account_info", None)
    if info is not None:
        value = getattr(info, "has_bot_ability", None)
        if callable(value):
            try:
                return bool(value())
            except Exception:
                return False
        if value is not None:
            return bool(value)
    module = _optional_import("..fea._sq_jqm")
    account = getattr(module, "current_account_info", None) if module else None
    checker = getattr(account, "has_bot_ability", None)
    if callable(checker):
        try:
            return bool(checker())
        except Exception:
            return False
    return True
