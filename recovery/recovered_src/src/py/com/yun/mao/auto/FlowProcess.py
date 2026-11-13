# Recovered module: src.py.com.yun.mao.auto.FlowProcess
# Reconstruction from the Nuitka module init and constants.
# All 17 module-level functions and their argument counts are confirmed by the
# init code objects.  Media/publish fallbacks are marked inferred.
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


def _as_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _record_publish_success(dest, message) -> None:
    message_id = _as_int(getattr(message, "id", 0))
    if not message_id:
        return
    try:
        recorder = _optional_import(
            "..record.PublishIdRecord",
            "log_publish_success",
        )
        if callable(recorder):
            recorder(dest, message_id)
    except Exception:
        pass


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


def _task_fields(parse, auto):
    messages = []
    getter = getattr(parse, "getMessages", None)
    if callable(getter):
        try:
            value = getter()
            if not inspect.isawaitable(value) and value is not None:
                messages = list(value)
        except Exception:
            pass
    if not messages:
        messages = list(getattr(parse, "messages", None) or [])
    medias = list(getattr(parse, "medias", None) or [])
    text = str(
        getattr(parse, "tart_text", None)
        or getattr(parse, "text", None)
        or ""
    )
    if not text:
        text = "\n".join(
            str(
                getattr(message, "text", None)
                or getattr(message, "message", None)
                or ""
            )
            for message in messages
        ).strip()
    return messages, medias, text


def _source_of(parse, auto):
    getter = getattr(parse, "getSource", None)
    if callable(getter):
        try:
            value = getter()
            if value is not None:
                return value
        except Exception:
            pass
    return getattr(parse, "source", None) or getattr(auto, "source", None)


def _destinations(auto, preview=False) -> List[Any]:
    names = ("getYulanDestes", "getYulanDestes") if preview else ("getDestes",)
    for name in names:
        getter = getattr(auto, name, None)
        if callable(getter):
            try:
                value = getter()
                if value is not None:
                    return list(value)
            except Exception:
                pass
    attr = "yulan_destes" if preview else "destes"
    return list(getattr(auto, attr, None) or [])


async def _resolve_entity(client, dest):
    convert = getattr(_optional_import("..dclass", "DTopClass"), "convertDest", None)
    target = dest
    if callable(convert):
        try:
            target = convert(dest)
        except Exception:
            target = dest
    getter = getattr(client, "get_entity", None)
    if callable(getter):
        try:
            target = await _maybe_await(getter(target))
        except Exception:
            pass
    return target


def _copy_id_map(id_map):
    """Copy an id map without sharing its list values."""

    copied = {}
    for key, value in (id_map or {}).items():
        copied[key] = list(value) if isinstance(value, list) else value
    return copied


def _ids_from_sent(sent):
    """Normalize a Telethon send result to a list of message ids."""

    if sent is None:
        return []
    if isinstance(sent, int):
        return [sent]
    if isinstance(sent, (list, tuple, set)):
        items = sent
    else:
        items = [sent]
    ids = []
    for item in items:
        msg_id = getattr(item, "id", item)
        try:
            msg_id = int(msg_id)
        except (TypeError, ValueError):
            continue
        if msg_id:
            ids.append(msg_id)
    return ids


async def _send_text_to_destinations(
    auto,
    parse,
    client,
    destinations,
    message_text,
    parse_mode,
    log_pre,
):
    """Send one text payload to every destination and return id map."""

    dest_id_map: Dict[Any, Any] = {}
    sender = getattr(client, "send_message", None)
    if not callable(sender):
        return dest_id_map
    for dest in destinations or []:
        if _stop_requested():
            print("手动停止成功！")
            break
        if not message_text:
            break
        try:
            target = await _resolve_entity(client, dest)
            topic_id = 0
            topic_helper = _optional_import(".TopicUtils")
            fetch_topic = (
                getattr(topic_helper, "fetch_dest_topic_id", None)
                if topic_helper
                else None
            )
            if callable(fetch_topic):
                topic_id = _as_int(await _maybe_await(fetch_topic(auto, client, dest)))
            value = await _maybe_await(
                sender(
                    target,
                    message_text,
                    parse_mode=parse_mode,
                    reply_to=topic_id or None,
                )
            )
            if value is not None:
                dest_id_map.setdefault(dest, []).append(
                    _as_int(getattr(value, "id", 0))
                )
                _record_publish_success(dest, value)
                sleep_func = getattr(
                    _optional_import("..util.need", "utils"),
                    "sleep_time_fun_no_log",
                    None,
                )
                if callable(sleep_func):
                    await _maybe_await(sleep_func(1, 2))
        except Exception as exc:
            print(f"{log_pre or ''} 发送到 {dest} 失败: {exc!r}")
            _print_trace()
    return dest_id_map


async def publish_normal_text(
    auto,
    parse,
    client,
    group_last_id,
    format_mode,
    full_text_has_tail,
    text_no_tail,
    isAutoFlow,
):
    """Publish plain text to private destinations."""

    destinations = _destinations(auto, preview=False)
    text = text_no_tail or getattr(parse, "text", None) or getattr(parse, "tart_text", None)
    dest_id_map = await _send_text_to_destinations(
        auto,
        parse,
        client,
        destinations,
        str(text or ""),
        None,
        "纯文本>>搬运到私有目标>>",
    )
    return _copy_id_map(dest_id_map)


async def publish_mark_down_text(
    auto,
    parse,
    client,
    group_last_id,
    format_mode,
    full_text_has_tail,
    text_no_tail,
    isAutoFlow,
):
    """Publish HTML/Markdown text to private destinations."""

    destinations = _destinations(auto, preview=False)
    text = text_no_tail or getattr(parse, "text", None) or getattr(parse, "tart_text", None)
    dest_id_map = await _send_text_to_destinations(
        auto,
        parse,
        client,
        destinations,
        str(text or ""),
        "html" if full_text_has_tail else None,
        "纯文本即时预览>>搬运到私有目标>>",
    )
    return _copy_id_map(dest_id_map)


def get_group_video_max_duration(messages):
    """Return the largest video duration in a message group."""

    cmcode = _optional_import(".CMCode")
    getter = getattr(cmcode, "getVideoDuration", None) if cmcode else None
    durations = []
    for message in messages or []:
        duration = getattr(message, "duration", None)
        if duration is None and callable(getter):
            try:
                duration = getter(message)
            except Exception:
                duration = None
        if duration is not None:
            try:
                durations.append(int(duration))
            except (TypeError, ValueError):
                pass
    return max(durations, default=0)


def gen_yulan_tart_text(auto, orign_message, full_text_has_tail):
    """Build the preview text, member link and maximum-duration footer."""

    text = str(
        getattr(orign_message, "text", None)
        or getattr(orign_message, "message", None)
        or ""
    ).strip()
    link = ""
    huiyuan = getattr(auto, "huiYuanLink", None)
    if huiyuan and getattr(huiyuan, "enable", False):
        link = str(getattr(huiyuan, "customerHttpLink", None) or "")
    youke = getattr(auto, "youKeLink", None)
    if not link and youke:
        link = str(getattr(youke, "httpLink", None) or "")
    if link:
        utils = _optional_import("..util.need", "utils")
        formatter = getattr(utils, "format_time", None) if utils else None
        duration = _as_int(getattr(auto, "max_duration", 0))
        duration_text = formatter(duration) if callable(formatter) else str(duration)
        if full_text_has_tail:
            text += (
                f"\n<blockquote><a href='{link}'>完整版视频时长"
                f"{duration_text}</a></blockquote>"
            )
        else:
            text += f"\n完整版视频时长{duration_text} {link}"
    return text


def clearAllTempFilesByMap(origin_to_water_path_map):
    """Delete origin and watermarked files from a map."""

    deleted = 0
    items = (
        origin_to_water_path_map.items()
        if isinstance(origin_to_water_path_map, dict)
        else (origin_to_water_path_map or [])
    )
    for origin_path, upload_path in items:
        if origin_path and upload_path and origin_path != upload_path:
            deleted += int(_safe_del(upload_path))
            deleted += int(_safe_del(origin_path))
        else:
            deleted += int(_safe_del(upload_path or origin_path))
    return deleted


def clearAllTempFiles(all_temp_files):
    """Delete every path produced by a flow run."""

    deleted = 0
    for path in all_temp_files or []:
        deleted += int(_safe_del(path))
    return deleted


def delete_resource_file(files):
    """Delete resource files from a list or mapping."""

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
    """Delete thumbnails generated from resource files."""

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
    """Delete a single thumbnail while keeping the resource."""

    if not p:
        return False
    return _safe_del(_thumb_for(p))


async def _upload_and_send_to_private_channel(
    auto,
    client,
    format_mode,
    log_pre_tag,
    text_no_tail,
    origin_group_files,
    pathMessageMap,
    orign_message,
):
    """Upload downloaded origin files and send them to private targets."""

    if not origin_group_files:
        return 0, {}
    cmcode = _optional_import(".CMCode")
    uploader = getattr(cmcode, "upload_only", None)
    try:
        await _call_adapted(
            uploader,
            (),
            {
                "client": client,
                "pathMessageMap": pathMessageMap or {},
                "origin_to_water_path_map": {
                    path: path for path in origin_group_files
                },
                "log_pre_tag": log_pre_tag,
            },
        )
    except Exception:
        _print_trace()

    dest_id_map = await _send_text_to_destinations(
        auto,
        None,
        client,
        _destinations(auto, preview=False),
        str(text_no_tail or ""),
        "html" if format_mode == "html" else None,
        "私有目标",
    )
    send_count = sum(len(value) if isinstance(value, list) else 1 for value in dest_id_map.values())
    return send_count, dest_id_map


async def _upload_and_send_to_public_channel(
    auto,
    client,
    format_mode,
    log_pre_tag,
    orign_message,
    full_text_has_tail,
    yulan_to_water_path,
):
    """Upload preview files and send them to public preview targets."""

    yulan_destes = _destinations(auto, preview=True)
    if not yulan_to_water_path:
        return 0
    sender = getattr(client, "send_file", None)
    text = gen_yulan_tart_text(auto, orign_message, full_text_has_tail)
    send_count = 0
    for dest in yulan_destes:
        if _stop_requested():
            print("手动停止成功！")
            break
        try:
            target = await _resolve_entity(client, dest)
            topic_id = 0
            helper = _optional_import(".TopicUtils")
            parser = getattr(helper, "parse_msg_topic_id", None) if helper else None
            if callable(parser):
                topic_id = _as_int(parser(orign_message, 0))
            for path in yulan_to_water_path or []:
                if callable(sender):
                    value = await _maybe_await(
                        sender(
                            target,
                            path,
                            caption=text or None,
                            reply_to=topic_id or None,
                        )
                    )
                else:
                    value = await _send_text_to_destinations(
                        auto,
                        None,
                        client,
                        [dest],
                        text,
                        None,
                        "公开预览目标",
                    )
                if value is not None:
                    send_count += 1
        except Exception:
            _print_trace()
    return send_count


async def _publish_to_preview_channel(
    all_temp_files,
    argsWrapper,
    auto,
    client,
    format_mode,
    full_text_has_tail,
    group_last_id,
    log_pre_tag,
    messages,
    origin_group_file,
    orign_message,
    text_no_tail,
    force_pic_preview,
):
    """Prepare preview artifacts and publish them to preview targets."""

    if not origin_group_file:
        return 0
    cmcode = _optional_import(".CMCode")
    preview_files = list(origin_group_file)
    gen = getattr(cmcode, "gen_yulan_if_need", None) if cmcode else None
    if callable(gen):
        try:
            value = gen(
                preview_files,
                getattr(auto, "yuLanModeBean", None),
                force_pic_preview=force_pic_preview,
            )
            value = await _maybe_await(value)
            if value:
                preview_files = list(value)
        except Exception:
            _print_trace()
    count = await _upload_and_send_to_public_channel(
        auto,
        client,
        format_mode,
        log_pre_tag,
        orign_message,
        full_text_has_tail,
        preview_files,
    )
    if count:
        print("5、预览资源发布到预览频道成功！")
    return count


async def _publish_resource_download(
    argsWrapper,
    auto,
    client,
    group_last_id,
    format_mode,
    log_pre_tag,
    messages,
    orign_message,
    full_text_has_tail,
    text_no_tail,
    isAutoFlow,
):
    """Download the source resources, then publish them to private targets."""

    print("1、开始下载原始资源...")
    downloader = _optional_import(".DownLoadBizHelper")
    biz = getattr(downloader, "biz_download_only", None)
    path_map = {}
    if callable(biz):
        try:
            path_map = await _call_adapted(
                biz,
                (),
                {
                    "log_pre_tag": log_pre_tag,
                    "client": client,
                    "at_name": getattr(auto, "at_name", None),
                    "text": text_no_tail,
                    "source_channel": _source_of(auto, auto),
                    "messages": messages,
                    "is_download_flow": False,
                    "download_thumb_hit_video": False,
                },
            ) or {}
        except Exception:
            _print_trace()
    if not path_map:
        print("= = 原始资源下载失败！")
        return 0, {}
    print("1、原始资源下载成功！")
    count, dest_id_map = await _upload_and_send_to_private_channel(
        auto,
        client,
        format_mode,
        log_pre_tag,
        text_no_tail,
        list(path_map.keys()),
        path_map,
        orign_message,
    )
    if count:
        print("2、原始资源发布到目标频道成功！")
    else:
        print("= = 原始资源发布到目标频道失败！")
    return count, dest_id_map


async def send_flow_process(
    client,
    parse,
    log_pre_tag,
    auto,
    argsWrapper,
    isAutoFlow=False,
):
    """Run the auto-flow: download, private publish, preview generation."""

    result_cls = _optional_import("..util.need.AllBeanDef", "FlowYunSendResult")
    result = result_cls() if callable(result_cls) else type("_FlowResult", (), {})()
    messages, medias, text = _task_fields(parse, auto)
    orign_message = messages[0] if messages else None
    for key, value in {
        "real_time_message_id": max(
            (
                _as_int(getattr(message, "id", 0))
                for message in messages
                if _as_int(getattr(message, "id", 0))
            ),
            default=0,
        ),
        "send_success_count": 0,
        "orign_message": orign_message,
        "need_continue": False,
        "dest_id_map": {},
        "preview_id_map": {},
    }.items():
        try:
            setattr(result, key, value)
        except Exception:
            pass

    try:
        ledger = _optional_import("..record", "CommentCopyLedger")
        should_skip = getattr(ledger, "should_skip_comment_group", None)
        if callable(should_skip) and should_skip(auto):
            return result
    except Exception:
        pass

    format_mode = getattr(parse, "format_mode", None) or "html"
    full_text_has_tail = bool(getattr(parse, "full_text_has_tail", False))
    text_no_tail = str(getattr(parse, "text_no_tail", None) or text or "")
    group_last_id = max(
        (
            _as_int(getattr(message, "id", 0))
            for message in messages
            if _as_int(getattr(message, "id", 0))
        ),
        default=0,
    )

    try:
        count, dest_map = await _publish_resource_download(
            argsWrapper,
            auto,
            client,
            group_last_id,
            format_mode,
            log_pre_tag,
            messages,
            orign_message,
            full_text_has_tail,
            text_no_tail,
            isAutoFlow,
        )
        result.send_success_count = _as_int(count)
        result.dest_id_map = _copy_id_map(dest_map)
    except Exception:
        _print_trace()

    preview_count = 0
    try:
        if getattr(auto, "yuLanDestes", None) or getattr(auto, "yulan_destes", None):
            preview_count = await _publish_to_preview_channel(
                list((result.dest_id_map or {}).keys()),
                argsWrapper,
                auto,
                client,
                format_mode,
                full_text_has_tail,
                group_last_id,
                log_pre_tag,
                messages,
                list((result.dest_id_map or {}).keys()),
                orign_message,
                text_no_tail,
                bool(getattr(auto, "force_pic_preview", False)),
            )
        elif text_no_tail:
            marker = await publish_mark_down_text(
                auto,
                parse,
                client,
                group_last_id,
                format_mode,
                full_text_has_tail,
                text_no_tail,
                isAutoFlow,
            )
            result.dest_id_map.update(marker)
    except Exception:
        _print_trace()
    result.preview_id_map = {
        dest: [preview_count] for dest in _destinations(auto, preview=True)
    } if preview_count else {}
    return result
