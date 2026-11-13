# Recovered module: src.py.com.yun.mao.auto.DownLoadProcess
# The module publishes one long coroutine, only_down_load.  Message/media
# extraction, text processing, watermarking, map rebinding and the download
# call follow the module constants and decompiled call order.
from __future__ import annotations

import asyncio
import importlib
import inspect
import os
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


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

    def stop_all(self):
        self.need_break = True
        return self


def _optional_import(module_name: str, attribute: Optional[str] = None):
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


async def _call_adapted(func, positional, values):
    if not callable(func):
        return None
    try:
        signature = inspect.signature(func)
    except (TypeError, ValueError):
        return await _maybe_await(func(*positional))
    kwargs = {
        key: value
        for key, value in values.items()
        if key in signature.parameters
        and signature.parameters[key].kind
        in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
    }
    try:
        return await _maybe_await(func(*positional, **kwargs))
    except TypeError:
        return await _maybe_await(func(*positional))


def _result_class():
    return (
        _optional_import("..util.need.AllBeanDef", "ParseGroupSendResult")
        or _GroupResult
    )


def _new_result(**kwargs):
    try:
        result = _result_class()()
    except Exception:
        result = _GroupResult()
    for key, value in kwargs.items():
        try:
            setattr(result, key, value)
        except Exception:
            continue
    return result


def _stop_requested() -> bool:
    working = _optional_import("..cd", "Working")
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


def _get_messages(parse) -> List[Any]:
    getter = getattr(parse, "getMessages", None)
    if callable(getter):
        try:
            value = getter()
            if inspect.isawaitable(value):
                return []
            if value is not None:
                return list(value)
        except Exception:
            return []
    return list(getattr(parse, "messages", None) or [])


def _get_medias(parse) -> List[Any]:
    getter = getattr(parse, "getMedias", None)
    if callable(getter):
        try:
            value = getter()
            if inspect.isawaitable(value):
                return []
            if value is not None:
                return list(value)
        except Exception:
            return []
    return list(getattr(parse, "medias", None) or [])


def _message_ids(messages) -> List[int]:
    result: List[int] = []
    for item in messages or []:
        msg_id = _message_id(item)
        if msg_id:
            result.append(msg_id)
    return result


def _text_of(message) -> str:
    text = getattr(message, "text", None)
    if text is None:
        text = getattr(message, "message", None)
    return str(text or "")


def _process_text(parse, messages, bean) -> str:
    text = str(
        getattr(parse, "tart_text", None)
        or getattr(parse, "text", None)
        or ""
    )
    if not text and messages:
        text = "\n".join(filter(None, (_text_of(msg) for msg in messages)))
    keep_source = bool(
        getattr(parse, "keepSourceText", getattr(bean, "keepSourceText", False))
    )
    delete_source_text = bool(
        getattr(parse, "deleSourceText", getattr(bean, "deleSourceText", False))
    )
    delete_link = bool(getattr(parse, "deleLink", getattr(bean, "deleLink", False)))
    replaces = getattr(parse, "replaces", getattr(bean, "replaces", None))

    if not keep_source and delete_source_text:
        text = ""
    if delete_link:
        import re

        text = re.sub(r"https?://\S+", "", text)
    if replaces:
        pairs = replaces.items() if isinstance(replaces, dict) else replaces
        for pair in pairs:
            if isinstance(pair, (list, tuple)) and len(pair) >= 2:
                text = text.replace(str(pair[0]), str(pair[1]))

    logic = _optional_import("..ai", "TextProcessLogic")
    processor = getattr(logic, "process_text_to_obj", None) if logic else None
    if callable(processor):
        try:
            value = processor(text)
            if not inspect.isawaitable(value) and value is not None:
                text = str(value)
        except Exception:
            _print_trace()
    ai_processor = getattr(logic, "process_text_by_ai_if_need", None) if logic else None
    if callable(ai_processor):
        try:
            value = ai_processor(text, parse, bean)
            if inspect.isawaitable(value):
                value = None
            if value is not None:
                text = str(value)
        except Exception:
            _print_trace()
    return text


def _build_path_maps(parse, messages, medias, bean):
    path_message_map = (
        getattr(parse, "pathMessageMap", None)
        or getattr(bean, "pathMessageMap", None)
        or {}
    )
    if path_message_map:
        return dict(path_message_map)
    result: Dict[Any, Any] = {}
    for message, media in zip(messages or [], medias or []):
        path = (
            getattr(media, "path", None)
            or getattr(media, "file_path", None)
            or getattr(media, "name", None)
        )
        if path:
            result[str(path)] = message
    return result


def _source_of(parse, auto) -> Any:
    getter = getattr(parse, "getSource", None)
    if callable(getter):
        try:
            value = getter()
            if value is not None:
                return value
        except Exception:
            return getattr(auto, "source", None)
    return getattr(parse, "source", None) or getattr(auto, "source", None)


async def _group_last_id(parse, messages) -> int:
    common = _optional_import("..util.need", "CommonCode")
    getter = getattr(common, "getMessagesLastId", None) if common else None
    if callable(getter):
        try:
            return _as_int(await _maybe_await(getter(parse, messages)))
        except Exception:
            return 0
    ids = _message_ids(messages)
    return max(ids) if ids else 0


async def _call_link_helper(parse, messages, medias):
    helper = _optional_import("..link._lk_gy_w", "gy_jc_a9")
    if not callable(helper):
        return None
    try:
        return await _call_adapted(
            helper,
            (),
            {
                "parse": parse,
                "messages": messages,
                "medias": medias,
            },
        )
    except TypeError:
        try:
            return await _maybe_await(helper(parse))
        except Exception:
            return None
    except Exception:
        return None


async def _watermark_if_needed(
    auto,
    client,
    parse,
    argsWrapper,
    bean,
    log_pre_tag,
    group_files,
    path_message_map,
):
    water = getattr(bean, "water", None) or getattr(auto, "water", None)
    if not water or not group_files:
        return path_message_map
    cmcode = _optional_import(".CMCode")
    water_func = getattr(cmcode, "water_only_if_need", None) if cmcode else None
    if not callable(water_func):
        return path_message_map
    try:
        value = await _call_adapted(
            water_func,
            (),
            {
                "auto": auto,
                "client": client,
                "album": group_files,
                "argsWrapper": argsWrapper,
                "log_pre_tag": log_pre_tag,
            },
        )
    except Exception:
        _print_trace()
        return path_message_map
    rebind = getattr(cmcode, "rebind_path_message_map", None)
    if callable(rebind) and isinstance(value, dict):
        try:
            return rebind(path_message_map, value)
        except Exception:
            return path_message_map
    return path_message_map


async def _fallback_download(client, group_files, path_message_map):
    downloader = getattr(client, "download_media", None)
    folder = tempfile.mkdtemp(prefix="yunmao_download_")
    result: Dict[Any, Any] = {}
    count = 0
    for media in group_files or []:
        if _stop_requested():
            break
        source = getattr(media, "message", None) or media
        name = (
            getattr(media, "name", None)
            or getattr(media, "file_name", None)
            or f"resource_{count + 1}"
        )
        target = os.path.join(folder, os.path.basename(str(name)))
        if callable(downloader):
            try:
                value = await _maybe_await(downloader(source, file=target))
                result[target] = value
                count += 1
                continue
            except Exception:
                _print_trace()
        result[target] = None
        count += 1
    return count, result


async def _run_download(
    auto,
    client,
    parse,
    argsWrapper,
    orign_message,
    medias,
    messages,
    text,
    at_name,
    group_files,
    path_message_map,
    all_temp_files,
    origin_to_water_path_map,
    group_last_id,
    tart_keep_source,
    tart_delete_source_text,
    tart_delete_link,
    tart_replaces,
    log_pre_tag,
):
    module = _optional_import(".DownLoadBizHelper")
    func = getattr(module, "biz_download_only", None) if module else None
    if callable(func):
        return await _call_adapted(
            func,
            (),
            {
                "auto": auto,
                "client": client,
                "parse": parse,
                "argsWrapper": argsWrapper,
                "orign_message": orign_message,
                "medias": medias,
                "messages": messages,
                "text": text,
                "at_name": at_name,
                "group_files": group_files,
                "pathMessageMap": path_message_map,
                "all_temp_files": all_temp_files,
                "origin_to_water_path_map": origin_to_water_path_map,
                "group_last_id": group_last_id,
                "tartKeepSource": tart_keep_source,
                "tartDeleSourceText": tart_delete_source_text,
                "tartDeleLink": tart_delete_link,
                "tartReplaces": tart_replaces,
                "log_pre_tag": log_pre_tag,
            },
        )
    return await _fallback_download(client, group_files, path_message_map)


def _normalize_download_result(value):
    if value is None:
        return 0, None
    if isinstance(value, int):
        return max(0, value), None
    if isinstance(value, dict):
        return len(value), value
    count = getattr(value, "send_success_count", None)
    if count is None:
        count = getattr(value, "send_count", None)
    if count is None:
        count = len(getattr(value, "sended_messages", None) or [])
    return max(0, _as_int(count)), getattr(value, "sended_messages", None)


async def only_down_load(
    client,
    parse,
    log_pre_tag,
    auto,
    argsWrapper,
):
    """Download one parse group without publishing or copying comments."""

    result = _new_result(
        real_time_message_id=getattr(auto, "real_time_message_id", 0),
        need_sleep=True,
    )
    try:
        bean = getattr(argsWrapper, "beanLike", None) or auto
        messages = _get_messages(parse)
        medias = _get_medias(parse)
        group_last_id = await _group_last_id(parse, messages)
        await _call_link_helper(parse, messages, medias)
        tart_keep_source = bool(getattr(parse, "keepSourceText", False))
        tart_delete_source_text = bool(getattr(parse, "deleSourceText", False))
        tart_delete_link = bool(getattr(parse, "deleLink", False))
        tart_replaces = getattr(parse, "replaces", None)
        text = _process_text(parse, messages, bean)
        at_name = getattr(parse, "at_name", None)
        if at_name is None:
            common = _optional_import("..util.need", "CommonCode")
            parser = getattr(common, "parse_dest_one_at_name", None) if common else None
            if callable(parser):
                try:
                    at_name = parser(parse, messages)
                except Exception:
                    at_name = None
            if at_name is None:
                class_parser = getattr(auto, "parse_dest_one_at_name", None)
                if callable(class_parser):
                    try:
                        at_name = class_parser(parse)
                    except Exception:
                        at_name = None

        path_message_map = _build_path_maps(parse, messages, medias, bean)
        origin_to_water_path_map = (
            getattr(argsWrapper, "origin_to_water_path_map", None)
            or getattr(parse, "origin_to_water_path_map", None)
            or {}
        )
        group_files = list(
            getattr(parse, "group_files", None)
            or getattr(parse, "files", None)
            or medias
            or []
        )
        all_temp_files = list(getattr(parse, "all_temp_files", None) or [])
        orign_message = (
            getattr(parse, "orign_message", None)
            or (messages[0] if messages else None)
        )

        path_message_map = await _watermark_if_needed(
            auto,
            client,
            parse,
            argsWrapper,
            bean,
            log_pre_tag,
            group_files,
            path_message_map,
        )
        if _stop_requested():
            print("手动停止成功！")
            return result

        value = await _run_download(
            auto,
            client,
            parse,
            argsWrapper,
            orign_message,
            medias,
            messages,
            text,
            at_name,
            group_files,
            path_message_map,
            all_temp_files,
            origin_to_water_path_map,
            group_last_id,
            tart_keep_source,
            tart_delete_source_text,
            tart_delete_link,
            tart_replaces,
            log_pre_tag,
        )
        count, sended = _normalize_download_result(value)
        result.send_count = count
        result.send_success_count = count
        result.send_group = 1 if count else 0
        result.sended_messages = sended
        if count:
            print("成功下载", count, "个资源！")
        return result
    except asyncio.CancelledError:
        raise
    except Exception:
        _print_trace()
        return result
