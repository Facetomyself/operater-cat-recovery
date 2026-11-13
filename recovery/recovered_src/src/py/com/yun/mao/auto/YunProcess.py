# Recovered module: src.py.com.yun.mao.auto.YunProcess
# Reconstruction from the Nuitka init table and constants.
# Ten module-level functions are created directly by init; the remaining
# preview/text/cleanup steps are the eleven nested bodies observed in the
# module's code-object table.  Cloud payload details are marked inferred.
from __future__ import annotations

import importlib
import inspect
import os
import traceback
from typing import Any, Dict, List, Optional, Sequence


_GLOBAL_DEST_ID_MAP: Dict[Any, Any] = {}
_GLOBAL_PREVIEW_ID_MAP: Dict[Any, Any] = {}


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


def _destinations(auto, preview=False) -> List[Any]:
    getter = getattr(
        auto,
        "getYulanDestes" if preview else "getDestes",
        None,
    )
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
    """Copy an id map without sharing list values."""

    copied = {}
    for key, value in (id_map or {}).items():
        copied[key] = list(value) if isinstance(value, list) else value
    return copied


def _set_global_dest_map(dest_map):
    """Replace the module-level destination id map."""

    global _GLOBAL_DEST_ID_MAP
    _GLOBAL_DEST_ID_MAP = _copy_id_map(dest_map or {})
    return _copy_id_map(_GLOBAL_DEST_ID_MAP)


def _set_global_preview_map(preview_map):
    """Replace the module-level preview id map."""

    global _GLOBAL_PREVIEW_ID_MAP
    _GLOBAL_PREVIEW_ID_MAP = _copy_id_map(preview_map or {})
    return _copy_id_map(_GLOBAL_PREVIEW_ID_MAP)


def _get_dest_id_map_from_global():
    """Return a defensive copy of the current destination map."""

    return _copy_id_map(_GLOBAL_DEST_ID_MAP)


def _delete_single_thumb(path):
    """Delete a single generated thumbnail."""

    if not path:
        return False
    return _safe_del(_thumb_for(path))


def _delete_single_thumb_and_file(path):
    """Delete a resource and its generated thumbnail."""

    if not path:
        return 0
    deleted = int(_delete_single_thumb(path))
    deleted += int(_safe_del(path))
    return deleted


def _delete_resources(files):
    """Delete resource files from a path, iterable or mapping."""

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


def _delete_thumbs(files):
    """Delete thumbnails for a path, iterable or mapping."""

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
        deleted += int(_delete_single_thumb(path))
    return deleted


async def _publish_resource(
    client,
    auto,
    original_messages,
    params_dest_id_map,
    format_mode,
    full_text_has_tail,
    html_link_string,
    db_channel,
    msg_ids,
    entity,
    target,
):
    """Publish original resources to the private cloud repository.

    Parameter names come from the cloud-publish variable block.  The exact
    Telegram request wrapper is inferred from CMCode.upload_only/send_file.
    """

    dest_map: Dict[Any, Any] = {}
    if not original_messages:
        return dest_map
    sender = getattr(client, "send_file", None)
    for index, message in enumerate(original_messages):
        if _stop_requested():
            print("手动停止成功！")
            break
        path = (
            getattr(message, "path", None)
            or getattr(message, "file_path", None)
            or (message if isinstance(message, str) else None)
        )
        if not path:
            continue
        try:
            destination = entity or db_channel or target
            if callable(sender):
                value = await _maybe_await(
                    sender(
                        destination,
                        path,
                        caption=html_link_string or None,
                    )
                )
            else:
                value = await _publish_to_cloud_text(
                    client,
                    destination,
                    html_link_string or "",
                    format_mode,
                )
            if value is not None:
                dest_map.setdefault(destination, []).append(
                    _as_int(getattr(value, "id", index))
                )
        except Exception:
            _print_trace()
    _set_global_dest_map(dest_map)
    return dest_map


async def _publish_to_cloud_text(client, destination, text, format_mode):
    sender = getattr(client, "send_message", None)
    if not callable(sender) or not text:
        return None
    return await _maybe_await(
        sender(
            destination,
            text,
            parse_mode="html" if format_mode == "html" else None,
        )
    )


async def send_yun_process(
    client,
    parse,
    log_pre_tag,
    auto,
    args_wrapper,
    isAutoFlow=False,
):
    """Run the cloud-repository flow, including preview publication."""

    result_cls = _optional_import("..util.need.AllBeanDef", "FlowYunSendResult")
    result = result_cls() if callable(result_cls) else type("_YunResult", (), {})()
    messages = list(getattr(parse, "messages", None) or [])
    getter = getattr(parse, "getMessages", None)
    if callable(getter):
        try:
            value = getter()
            if not inspect.isawaitable(value) and value is not None:
                messages = list(value)
        except Exception:
            pass
    original_messages = list(messages)
    orign_message = original_messages[0] if original_messages else None
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
            for message in original_messages
        ).strip()
    format_mode = getattr(parse, "format_mode", None) or "html"
    full_text_has_tail = bool(getattr(parse, "full_text_has_tail", False))
    text_no_tail = str(getattr(parse, "text_no_tail", None) or text or "")
    real_time_message_id = max(
        (
            _as_int(getattr(message, "id", 0))
            for message in original_messages
            if _as_int(getattr(message, "id", 0))
        ),
        default=0,
    )
    for key, value in {
        "real_time_message_id": real_time_message_id,
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

    def _ids_from_sent(sent):
        if sent is None:
            return []
        if isinstance(sent, int):
            return [sent]
        values = sent if isinstance(sent, (list, tuple, set)) else [sent]
        ids = []
        for item in values:
            msg_id = getattr(item, "id", item)
            msg_id = _as_int(msg_id)
            if msg_id:
                ids.append(msg_id)
        return ids

    async def _send_text_to_destinations(
        destinations,
        message_text,
        parse_mode,
        log_pre,
    ):
        dest_id_map: Dict[Any, Any] = {}
        sender = getattr(client, "send_message", None)
        if not callable(sender):
            return dest_id_map
        for dest in destinations or []:
            if _stop_requested():
                print("手动停止成功！")
                break
            try:
                target = await _resolve_entity(client, dest)
                value = await _maybe_await(
                    sender(target, message_text, parse_mode=parse_mode)
                )
                if value is not None:
                    dest_id_map.setdefault(dest, []).extend(_ids_from_sent(value))
                    _record_publish_success(dest, value)
            except Exception as exc:
                print(f"{log_pre or ''} 发送到 {dest} 失败: {exc!r}")
                _print_trace()
        return dest_id_map

    async def _publish_normal_text(destinations):
        return await _send_text_to_destinations(
            destinations,
            text_no_tail,
            None,
            "纯文本>>搬运到私有云仓库>>" if not _destinations(auto, preview=True)
            else "纯文本>>搬运到公开预览>>",
        )

    async def _publish_markdown_text(destinations):
        return await _send_text_to_destinations(
            destinations,
            text_no_tail,
            "html" if full_text_has_tail else None,
            "纯文本即时预览>>搬运到私有云仓库>>",
        )

    def _generate_preview_text():
        preview_text = gen_yulan_tart_text(auto, orign_message, full_text_has_tail)
        version = _optional_import("src.py", "version_code")
        if version:
            preview_text = f"{preview_text}\n{version}"
        return preview_text

    async def _handle_media_upload_and_publish(origin_files, path_msg_map):
        if not origin_files:
            return 0, {}
        cmcode = _optional_import(".CMCode")
        uploader = getattr(cmcode, "upload_only", None)
        try:
            await _call_adapted(
                uploader,
                (),
                {
                    "client": client,
                    "pathMessageMap": path_msg_map or {},
                    "origin_to_water_path_map": {
                        path: path for path in origin_files
                    },
                    "log_pre_tag": log_pre_tag,
                },
            )
        except Exception:
            _print_trace()
        destinations = _destinations(auto, preview=False)
        dest_map = await _publish_markdown_text(destinations)
        count = sum(
            len(value) if isinstance(value, list) else 1
            for value in dest_map.values()
        )
        return count, dest_map

    async def _publish_to_preview_channel(origin_files):
        cmcode = _optional_import(".CMCode")
        preview_files = list(origin_files or [])
        gen = getattr(cmcode, "gen_yulan_if_need", None) if cmcode else None
        if callable(gen):
            try:
                value = await _maybe_await(
                    gen(
                        preview_files,
                        getattr(auto, "yuLanModeBean", None),
                        force_pic_preview=bool(
                            getattr(auto, "force_pic_preview", False)
                        ),
                    )
                )
                if value:
                    preview_files = list(value)
            except Exception:
                _print_trace()
        sender = getattr(client, "send_file", None)
        preview_map: Dict[Any, Any] = {}
        preview_text = _generate_preview_text()
        for dest in _destinations(auto, preview=True):
            try:
                target = await _resolve_entity(client, dest)
                for path in preview_files:
                    if callable(sender):
                        value = await _maybe_await(
                            sender(
                                target,
                                path,
                                caption=preview_text or None,
                            )
                        )
                    else:
                        value = await _publish_to_cloud_text(
                            client,
                            target,
                            preview_text,
                            format_mode,
                        )
                    if value is not None:
                        preview_map.setdefault(dest, []).extend(
                            _ids_from_sent(value)
                        )
            except Exception:
                _print_trace()
        _set_global_preview_map(preview_map)
        return preview_map

    def _clear_files_by_map(file_map):
        deleted = 0
        for origin_path, upload_path in (file_map or {}).items():
            if origin_path != upload_path:
                deleted += int(_safe_del(upload_path))
            deleted += int(_safe_del(origin_path))
        return deleted

    def _clear_files_list(files):
        deleted = 0
        for path in files or []:
            deleted += int(_safe_del(path))
        return deleted

    def _cleanup_temp_files(args_wrapper, file_groups, all_files_to_clean, group):
        path_map = {}
        if isinstance(file_groups, dict):
            path_map = file_groups
        deleted = _clear_files_by_map(path_map)
        deleted += _clear_files_list(all_files_to_clean)
        print("删除临时文件成功！")
        return deleted

    def delete_temp_files(args_wrapper, file_groups, all_files_to_clean, group):
        return _cleanup_temp_files(
            args_wrapper,
            file_groups,
            all_files_to_clean,
            group,
        )

    try:
        downloader = _optional_import(".DownLoadBizHelper")
        biz = getattr(downloader, "biz_download_only", None)
        path_msg_map = {}
        if callable(biz):
            path_msg_map = await _call_adapted(
                biz,
                (),
                {
                    "log_pre_tag": log_pre_tag,
                    "client": client,
                    "at_name": getattr(auto, "at_name", None),
                    "text": text_no_tail,
                    "source_channel": getattr(parse, "source", None)
                    or getattr(auto, "source", None),
                    "messages": original_messages,
                    "is_download_flow": False,
                    "download_thumb_hit_video": False,
                },
            ) or {}
    except Exception:
        _print_trace()
        path_msg_map = {}

    if path_msg_map:
        try:
            _clear_files_list([])
            upload_count, dest_map = await _handle_media_upload_and_publish(
                list(path_msg_map.keys()),
                path_msg_map,
            )
            result.send_success_count = _as_int(upload_count)
            result.dest_id_map = _set_global_dest_map(dest_map)
        except Exception:
            _print_trace()
        try:
            preview_map = await _publish_to_preview_channel(
                list(path_msg_map.keys())
            )
            result.preview_id_map = preview_map
        except Exception:
            _print_trace()
    elif text_no_tail:
        dest_map = await _publish_normal_text(_destinations(auto, preview=False))
        result.dest_id_map = _set_global_dest_map(dest_map)

    try:
        _cleanup_temp_files(
            args_wrapper,
            path_msg_map,
            list(path_msg_map.keys()),
            None,
        )
    except Exception:
        _print_trace()
    return result


def get_group_video_max_duration(messages):
    """Return the largest video duration in a cloud group."""

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
            durations.append(_as_int(duration))
    return max(durations, default=0)


def gen_yulan_tart_text(auto, orign_message, full_text_has_tail):
    """Build the cloud preview footer from member/guest links and media time."""

    text = str(
        getattr(orign_message, "text", None)
        or getattr(orign_message, "message", None)
        or ""
    ).strip()
    huiyuan = getattr(auto, "huiYuanLink", None)
    youke = getattr(auto, "youKeLink", None)
    link = ""
    if huiyuan and getattr(huiyuan, "enable", False):
        link = str(getattr(huiyuan, "customerHttpLink", None) or "")
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
