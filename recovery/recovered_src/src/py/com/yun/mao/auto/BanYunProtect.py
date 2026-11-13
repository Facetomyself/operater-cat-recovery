# Recovered module: src.py.com.yun.mao.auto.BanYunProtect
# Reconstruction from the Nuitka init code objects and constants.
# The six module-level functions and their argument lists are confirmed by the
# init table.  Individual media fallbacks are marked inferred.
from __future__ import annotations

import importlib
import inspect
import os
import traceback
from typing import Any, Dict, List, Optional, Sequence


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


async def _call_adapted(func, positional: Sequence[Any], values: Dict[str, Any]):
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
    return await _maybe_await(func(*positional, **kwargs))


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
            pass
    traceback.print_exc()


def _as_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _record_publish_success(channel, message) -> None:
    message_id = _as_int(getattr(message, "id", 0))
    if not message_id:
        return
    try:
        recorder = _optional_import(
            "..record.PublishIdRecord",
            "log_publish_success",
        )
        if callable(recorder):
            recorder(channel, message_id)
    except Exception:
        pass


def _get_messages(parse) -> List[Any]:
    getter = getattr(parse, "getMessages", None)
    if callable(getter):
        try:
            value = getter()
            if not inspect.isawaitable(value) and value is not None:
                return list(value)
        except Exception:
            pass
    return list(getattr(parse, "messages", None) or [])


def _get_medias(parse) -> List[Any]:
    getter = getattr(parse, "getMedias", None)
    if callable(getter):
        try:
            value = getter()
            if not inspect.isawaitable(value) and value is not None:
                return list(value)
        except Exception:
            pass
    return list(getattr(parse, "medias", None) or [])


def _source_of(parse, auto) -> Any:
    getter = getattr(parse, "getSource", None)
    if callable(getter):
        try:
            value = getter()
            if value is not None:
                return value
        except Exception:
            pass
    return getattr(parse, "source", None) or getattr(auto, "source", None)


def _text_of(message) -> str:
    text = getattr(message, "text", None)
    if text is None:
        text = getattr(message, "message", None)
    return str(text or "")


def _targets(auto, dest_to_map) -> List[Any]:
    if isinstance(dest_to_map, dict) and dest_to_map:
        return list(dest_to_map.keys())
    for name in ("getDestes", "get_destes"):
        getter = getattr(auto, name, None)
        if callable(getter):
            try:
                value = getter()
                if value is not None:
                    return list(value)
            except Exception:
                pass
    return list(
        getattr(auto, "destes", None)
        or getattr(auto, "destinations", None)
        or []
    )


def _result_class():
    return _optional_import(
        "..util.need.AllBeanDef", "BanYunProtectSendResult"
    )


def _new_result(**kwargs):
    cls = _result_class()
    result = cls() if callable(cls) else type("_ProtectResult", (), {})()
    defaults = {
        "real_time_message_id": 0,
        "send_success_count": 0,
        "orign_message": None,
        "dest_id_map": {},
        "send_to_comment": False,
        "ai_refused": False,
    }
    for key, value in defaults.items():
        try:
            setattr(result, key, value)
        except Exception:
            pass
    for key, value in kwargs.items():
        try:
            setattr(result, key, value)
        except Exception:
            pass
    return result


def _safe_del(path) -> bool:
    if not path:
        return False
    utils = _optional_import("..util.need", "utils")
    safe_del_file = getattr(utils, "safe_del_file", None) if utils else None
    if callable(safe_del_file):
        try:
            return bool(safe_del_file(path))
        except Exception:
            return False
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
    except Exception:
        pass
    return False


def _thumb_for(path):
    accel = _optional_import("..util", "AccelUtils")
    generator = getattr(accel, "gene_thumb_path", None) if accel else None
    if callable(generator):
        try:
            return generator(path)
        except Exception:
            pass
    stem, suffix = os.path.splitext(str(path or ""))
    return f"{stem}_thumb{suffix or '.jpg'}"


def clearAllTempFilesByMap(origin_to_water_path_map):
    """Delete both the origin and uploaded/watermarked copies."""

    deleted = 0
    if not origin_to_water_path_map:
        return deleted
    items = (
        origin_to_water_path_map.items()
        if isinstance(origin_to_water_path_map, dict)
        else origin_to_water_path_map
    )
    for origin_path, upload_path in items:
        if origin_path and upload_path and origin_path != upload_path:
            deleted += int(_safe_del(upload_path))
            deleted += int(_safe_del(origin_path))
        else:
            deleted += int(_safe_del(upload_path or origin_path))
    return deleted


def clearAllTempFiles(all_temp_files):
    """Delete every path collected during one protect run."""

    deleted = 0
    for path in all_temp_files or []:
        deleted += int(_safe_del(path))
    return deleted


def delete_resource_file(files):
    """Delete resource paths; accepts a path, iterable or mapping."""

    if not files:
        return 0
    if isinstance(files, dict):
        paths = list(files.keys()) + list(files.values())
    elif isinstance(files, (str, bytes, os.PathLike)):
        paths = [files]
    else:
        paths = list(files)
    deleted = 0
    for path in paths:
        deleted += int(_safe_del(path))
    return deleted


def delete_thumb_file(files):
    """Delete generated thumbnails for resource paths."""

    if not files:
        return 0
    if isinstance(files, (str, bytes, os.PathLike)):
        paths = [files]
    elif isinstance(files, dict):
        paths = list(files.keys()) + list(files.values())
    else:
        paths = list(files)
    deleted = 0
    for path in paths:
        if path:
            deleted += int(_safe_del(_thumb_for(path)))
    return deleted


def delete_single_thumb_file(p):
    """Delete one generated thumbnail, keeping the resource itself."""

    if not p:
        return False
    return _safe_del(_thumb_for(p))


async def send_message_protect(
    client=None,
    parse=None,
    log_pre_tag="",
    auto=None,
    argsWrapper=None,
    dest_to_map=None,
):
    """Publish a parsed group with Telegram protected-content mode enabled."""

    result = _new_result()
    messages = _get_messages(parse)
    medias = _get_medias(parse)
    orign_message = messages[0] if messages else None
    result.orign_message = orign_message
    source_channel = _source_of(parse, auto)
    bean = getattr(parse, "beanLike", None) or getattr(parse, "bean", None)

    try:
        ledger = _optional_import("..record", "CommentCopyLedger")
        should_skip = getattr(ledger, "should_skip_comment_group", None)
        if callable(should_skip) and should_skip(auto):
            return result
    except Exception:
        pass

    text = str(
        getattr(parse, "tart_text", None)
        or getattr(parse, "text", None)
        or ""
    )
    if not text and messages:
        text = "\n".join(filter(None, (_text_of(msg) for msg in messages)))

    logic = _optional_import("..ai", "TextProcessLogic")
    try:
        processor = getattr(logic, "process_text_to_obj", None) if logic else None
        if callable(processor):
            value = processor(text)
            if value is not None and not inspect.isawaitable(value):
                text = str(value)
        ai_processor = (
            getattr(logic, "process_text_by_ai_if_need", None) if logic else None
        )
        if callable(ai_processor):
            value = ai_processor(text, auto, bean)
            if inspect.isawaitable(value):
                value = await value
            if value is not None:
                text = str(value)
    except Exception:
        _print_trace()

    if bool(getattr(parse, "ai_refused", False)) or bool(
        getattr(bean, "ai_refused", False)
    ):
        result.ai_refused = True
        if not bool(getattr(parse, "is_keep_origin_source", False)):
            print("AI 拒绝生成文案，跳过本组消息，继续下一组...")
            return result
        print("AI 拒绝生成文案，将会使用源文案发布...")

    for_mat = getattr(parse, "for_mat", None) or getattr(bean, "for_mat", None)
    parse_mode = "html" if getattr(for_mat, "name", for_mat) == "HTML" else None
    cmcode = _optional_import(".CMCode")
    topic_utils = _optional_import(".TopicUtils")
    parse_topic = (
        getattr(topic_utils, "parse_parseBean_topic_id", None)
        if topic_utils
        else None
    )
    send_message = getattr(client, "send_message", None)
    send_file = getattr(client, "send_file", None)
    flood = _optional_import("..util", "FloodGuard")
    with_retry = getattr(flood, "with_flood_retry", None) if flood else None
    dest_id_map: Dict[Any, Any] = {}
    all_temp_files: List[str] = []
    path_message_map: Dict[str, Any] = {}
    origin_to_water_path_map: Dict[str, str] = {}
    any_comment_sent = False
    topic_id = 0
    if callable(parse_topic):
        try:
            topic_id = _as_int(parse_topic(parse))
        except Exception:
            topic_id = 0

    async def try_run(upload_path):
        """Send one downloaded/uploaded resource to all destinations."""

        nonlocal any_comment_sent
        sent_count = 0
        for dest in _targets(auto, dest_to_map):
            if _stop_requested():
                print("手动停止成功！")
                break
            target = dest
            convert = (
                getattr(_optional_import("..dclass", "DTopClass"), "convertDest", None)
            )
            if callable(convert):
                try:
                    target = convert(dest)
                except Exception:
                    target = dest
            dest_topic = topic_id
            if isinstance(dest_to_map, dict):
                dest_topic = _as_int(dest_to_map.get(dest), topic_id)
            try:
                entity = getattr(client, "get_entity", None)
                if callable(entity):
                    target = await _maybe_await(entity(target))
            except Exception:
                pass
            try:
                if text:
                    sender = getattr(cmcode, "send_message_only", None)
                    value = await _call_adapted(
                        sender,
                        (),
                        {
                            "auto": auto,
                            "client": client,
                            "destes": [target],
                            "dest_to_map": dest_to_map or {},
                            "album": None,
                            "tart_text": text,
                            "for_mat": for_mat,
                            "is_video_or_photo": False,
                            "log_pre_tag": log_pre_tag,
                            "src_topic_id": dest_topic,
                            "part_contexts": [],
                            "dest_log_type": "protect/send_message/channel/plaintext",
                        },
                    )
                    if value is None and callable(send_message):
                        value = await _maybe_await(
                            send_message(
                                target,
                                text,
                                parse_mode=parse_mode,
                                reply_to=dest_topic or None,
                            )
                        )
                    if value is not None:
                        sent_count += max(1, _as_int(value, 1))
                        dest_id_map.setdefault(dest, []).append(
                            _as_int(getattr(value, "id", 0))
                        )
                        _record_publish_success(dest, value)
                if upload_path and callable(send_file):
                    kwargs = {
                        "caption": text or None,
                        "parse_mode": parse_mode,
                        "reply_to": dest_topic or None,
                    }
                    kwargs = {
                        key: value
                        for key, value in kwargs.items()
                        if value is not None
                    }
                    if callable(with_retry):
                        value = await _maybe_await(
                            with_retry(
                                lambda: send_file(
                                    target,
                                    upload_path,
                                    **kwargs,
                                ),
                                prefix="protect/send_file/channel/media",
                            )
                        )
                    else:
                        value = await _maybe_await(
                            send_file(target, upload_path, **kwargs)
                        )
                    if value is not None:
                        sent_count += 1
                        dest_id_map.setdefault(dest, []).append(
                            _as_int(getattr(value, "id", 0))
                        )
                        _record_publish_success(dest, value)
            except Exception:
                _print_trace()
        return sent_count

    download_helper = _optional_import(".DownLoadBizHelper")
    downloader = getattr(download_helper, "biz_download_only", None)
    try:
        if callable(downloader):
            path_message_map = await _call_adapted(
                downloader,
                (),
                {
                    "log_pre_tag": log_pre_tag,
                    "client": client,
                    "at_name": getattr(parse, "at_name", None),
                    "text": text,
                    "source_channel": source_channel,
                    "messages": messages,
                    "is_download_flow": False,
                    "download_thumb_hit_video": False,
                },
            ) or {}
            all_temp_files.extend(path_message_map.keys())
    except Exception:
        _print_trace()

    if path_message_map:
        try:
            watermark = getattr(cmcode, "water_only_if_need", None)
            value = await _call_adapted(
                watermark,
                (),
                {
                    "auto": auto,
                    "client": client,
                    "album": list(path_message_map.keys()),
                    "pathMessageMap": path_message_map,
                    "argsWrapper": argsWrapper,
                    "log_pre_tag": log_pre_tag,
                    "spoiler": bool(getattr(bean, "spoiler", False)),
                    "randomCover": bool(getattr(bean, "randomCover", False)),
                },
            )
            if isinstance(value, dict) and value:
                origin_to_water_path_map = dict(value)
        except Exception:
            _print_trace()
        if not origin_to_water_path_map:
            origin_to_water_path_map = {
                path: path for path in path_message_map.keys()
            }
        try:
            uploader = getattr(cmcode, "upload_only", None)
            await _call_adapted(
                uploader,
                (),
                {
                    "client": client,
                    "pathMessageMap": path_message_map,
                    "origin_to_water_path_map": origin_to_water_path_map,
                    "is_file_upload": False,
                    "spoiler": bool(getattr(bean, "spoiler", False)),
                    "randomCover": bool(getattr(bean, "randomCover", False)),
                    "log_pre_tag": log_pre_tag,
                },
            )
        except Exception:
            _print_trace()
        for upload_path in (
            origin_to_water_path_map.values()
            or path_message_map.keys()
        ):
            if _stop_requested():
                print("手动停止成功！")
                break
            try:
                result.send_success_count += await try_run(upload_path)
            except Exception:
                _print_trace()
    elif medias:
        for media in medias:
            path = (
                getattr(media, "path", None)
                or getattr(media, "file_path", None)
                or (media if isinstance(media, str) else None)
            )
            if path:
                all_temp_files.append(path)
                result.send_success_count += await try_run(path)
    elif text:
        result.send_success_count += await try_run(None)

    try:
        comment_to_id = None
        comment_helper = getattr(cmcode, "obtain_comment_to_id", None)
        if callable(comment_helper):
            comment_to_id = comment_helper(auto, parse, source_channel)
            if inspect.isawaitable(comment_to_id):
                comment_to_id = await comment_to_id
        if comment_to_id:
            for dest in _targets(auto, dest_to_map):
                target = dest
                convert = (
                    getattr(_optional_import("..dclass", "DTopClass"), "convertDest", None)
                )
                if callable(convert):
                    try:
                        target = convert(dest)
                    except Exception:
                        target = dest
                sender = getattr(cmcode, "send_message_only", None)
                value = await _call_adapted(
                    sender,
                    (),
                    {
                        "auto": auto,
                        "client": client,
                        "destes": [target],
                        "dest_to_map": dest_to_map or {},
                        "album": None,
                        "tart_text": text,
                        "for_mat": for_mat,
                        "is_video_or_photo": False,
                        "log_pre_tag": log_pre_tag,
                        "src_topic_id": topic_id,
                        "part_contexts": [],
                        "comment_to_id": comment_to_id,
                        "dest_log_type": "protect/send_message/comment/markdown",
                    },
                )
                if value is None and text and callable(send_message):
                    value = await _maybe_await(
                        send_message(
                            target,
                            text,
                            parse_mode=parse_mode,
                            reply_to=comment_to_id,
                        )
                    )
                if value is not None:
                    any_comment_sent = True
                    result.send_success_count += max(1, _as_int(value, 1))
    except Exception:
        _print_trace()

    result.dest_id_map = dest_id_map
    result.send_to_comment = any_comment_sent
    result.real_time_message_id = max(
        (
            _as_int(getattr(message, "id", 0))
            for message in messages
            if _as_int(getattr(message, "id", 0))
        ),
        default=0,
    )
    for path in all_temp_files:
        _safe_del(path)
    for origin_path, upload_path in origin_to_water_path_map.items():
        if origin_path != upload_path:
            _safe_del(upload_path)
    return result
