# Recovered module: src.py.com.yun.mao.auto.upload
# The seven function names, argument names and chunk constants come from the
# module init and code-object metadata.  Telethon objects and local helpers are
# imported lazily so importing this module performs no I/O or upload.
from __future__ import annotations

import asyncio
import importlib
import inspect
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, List, Optional


_TG_LARGE_FILE_BYTES = 10 * 1024 * 1024
_FAST_UPLOAD_PART_SIZE = 512 * 1024


@dataclass
class _PartContext:
    path: str = ""
    file_id: Any = None
    parts: list = None
    file_size: int = 0
    part_size: int = 0
    is_large: bool = False
    role: Any = None

    def __post_init__(self):
        if self.parts is None:
            self.parts = []


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


def _flag(obj, name: str, default: bool = False) -> bool:
    value = getattr(obj, name, default)
    if callable(value):
        try:
            value = value()
        except Exception:
            return default
    return bool(value)


def _path_flag(obj, name: str, path) -> bool:
    func = getattr(obj, name, None) if obj is not None else None
    if not callable(func):
        return False
    try:
        return bool(func(path))
    except Exception:
        return False


def _working():
    return _optional_import("..cd", "Working")


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


def _max_try_count() -> int:
    config = _optional_import("..config", "YunYinMaoConfig")
    return max(1, int(getattr(config, "MAX_TRY_COUNT", 5) or 5))


def _up_load_part_size_kb() -> int:
    config = _optional_import(".down_load_config")
    return max(1, int(getattr(config, "up_load_part_size_kb", 512) or 512))


def _telethon_default_part_size(file_size: int) -> int:
    """Return Telethon's preferred upload part size for ``file_size``."""

    size = max(0, int(file_size or 0))
    getter = _optional_import("telethon.utils", "get_appropriated_part_size")
    if callable(getter):
        try:
            return max(1024, int(getter(size)))
        except Exception:
            return 1024
    return 1024


def _part_context_class():
    return (
        _optional_import("..util.need.AllBeanDef", "UploadPartContext")
        or _PartContext
    )


def _make_part_context(
    path,
    input_file=None,
    part_size=None,
    role=None,
):
    abs_path = os.path.abspath(os.fspath(path))
    try:
        file_size = int(os.path.getsize(abs_path))
    except OSError:
        file_size = 0
    if part_size is None:
        part_size = _telethon_default_part_size(file_size)
    context = _part_context_class()()
    context.path = abs_path
    context.file_id = getattr(input_file, "id", None)
    context.parts = list(getattr(input_file, "parts", None) or [])
    context.file_size = file_size
    context.part_size = max(1024, int(part_size))
    context.is_large = file_size >= _TG_LARGE_FILE_BYTES
    context.role = role
    return context


def gen_media_file_name(path):
    """Return the display filename used for uploaded media."""

    return format(path, "")


def _mime_type(path) -> str:
    common = _optional_import("..util.need", "CommonCode")
    getter = getattr(common, "getMimeType", None) if common else None
    if callable(getter):
        try:
            value = getter(path)
            if value:
                return str(value)
        except Exception:
            value = None
    guessed, _ = mimetypes.guess_type(str(path))
    return guessed or "application/octet-stream"


def _call_back_module():
    return _optional_import("..telefast", "CallBack")


def _fast_upload(client, path, progress_callback=None):
    module = _optional_import("..telefast", "FastDownUpLoadUtils")
    func = getattr(module, "fast_up_load", None) if module else None
    if not callable(func):
        return None
    try:
        return func(client, path, progress_callback=progress_callback)
    except TypeError:
        return func(client, path)


async def _normal_upload_file(client, path, progress_callback=None):
    uploader = getattr(client, "upload_file", None)
    if not callable(uploader):
        return None
    kwargs = {
        "part_size_kb": _up_load_part_size_kb(),
        "progress_callback": progress_callback,
        "max_retries": _max_try_count(),
    }
    flood = _optional_import("..util.FloodGuard")
    retry = getattr(flood, "with_flood_retry", None) if flood else None
    call = lambda: uploader(path, **kwargs)
    if callable(retry):
        try:
            return await _maybe_await(retry(call, prefix="upload/upload_file"))
        except TypeError:
            return await _maybe_await(retry(call))
    try:
        return await _maybe_await(call())
    except TypeError:
        return await _maybe_await(uploader(path, progress_callback=progress_callback))


async def _upload_with_fast_fallback(client, path, progress_callback=None):
    callback = getattr(_call_back_module(), "upload_progress_bar", None)
    if progress_callback is None:
        progress_callback = callback
    uploaded = None
    if callable(_fast_upload):
        try:
            uploaded = await _maybe_await(
                _fast_upload(client, path, progress_callback=progress_callback)
            )
        except Exception:
            _print_trace()
    if uploaded is None:
        uploaded = await _normal_upload_file(
            client,
            path,
            progress_callback=progress_callback,
        )
    return uploaded


def _unpack_upload(value):
    if isinstance(value, tuple):
        media = value[0] if value else None
        context = value[1] if len(value) > 1 else None
        return media, context
    return value, None


def _probe_video(path):
    accel = _optional_import("..util", "AccelUtils")
    probe = getattr(accel, "probe_video_meta_with_audio", None) if accel else None
    if not callable(probe):
        return None
    try:
        return probe(path)
    except Exception:
        return None


def _extract_cover(path, random_cover=False):
    accel = _optional_import("..util", "AccelUtils")
    if not accel:
        return None
    name = "extract_random_cover_image" if random_cover else "extract_first_cover_image"
    extractor = getattr(accel, name, None)
    if not callable(extractor):
        return None
    try:
        return extractor(path)
    except Exception:
        return None


async def _upload_thumb(client, thumb_path):
    if not thumb_path:
        return None
    uploader = getattr(client, "upload_file", None)
    if not callable(uploader):
        return None
    try:
        return await _maybe_await(uploader(thumb_path))
    except Exception:
        _print_trace()
        return None


async def upload(
    log_pre_tag,
    client,
    origin_to_water_path_map=None,
    pathMessageMap=None,
    is_file_upload=False,
    spoiler=False,
    randomCover=False,
    orignMessage=None,
    newAlbum=None,
    part_contexts=None,
    isVideoOrPhoto=None,
):
    """Upload every prepared path and return ``(last_media, part_contexts)``."""

    if _stop_requested():
        print("手动停止成功！")
        return None, []
    path_map = pathMessageMap or {}
    water_map = origin_to_water_path_map or {}
    items = list(water_map.items()) or list(path_map.items())
    if not items and path_map:
        items = [(value, value) for value in path_map]
    contexts: List[Any] = list(part_contexts or [])
    last_media = None
    total = max(1, len(items))
    common = _optional_import("..util.need", "CommonCode")

    for index, (origin_path, upload_path) in enumerate(items, 1):
        if _stop_requested():
            print("手动停止成功！")
            return last_media, contexts
        upload_path = upload_path or origin_path
        origin_path = origin_path or upload_path
        print(
            f"{log_pre_tag or ''} 第 {index}/{total},开始上传... 正在上传：{upload_path}"
        )
        try:
            mime_type = _mime_type(upload_path)
            file_name = gen_media_file_name(upload_path)
            message_spoiler = spoiler or bool(getattr(orignMessage, "spoiler", False))
            result = None
            if is_file_upload:
                result = await upload_normal_file(client, upload_path, mime_type)
            elif isVideoOrPhoto or _path_flag(common, "localFileIsVideo", upload_path):
                result = await upload_video(
                    client,
                    upload_path,
                    file_name=file_name,
                    spoiler=message_spoiler,
                    randomCover=randomCover,
                )
            elif _path_flag(common, "localFileIsPhoto", upload_path):
                result = await upload_photo(
                    client,
                    upload_path,
                    spoiler=message_spoiler,
                )
            else:
                result = await upload_normal_file(client, upload_path, mime_type)
            media, context = _unpack_upload(result)
            if media is not None:
                last_media = media
                if newAlbum is not None and hasattr(newAlbum, "append"):
                    newAlbum.append(media)
            if context is not None:
                contexts.append(context)
        except Exception:
            _print_trace()
            try:
                fallback = await upload_normal_file(client, upload_path)
                media, context = _unpack_upload(fallback)
                if media is not None:
                    last_media = media
                if context is not None:
                    contexts.append(context)
            except Exception:
                _print_trace()
    return last_media, contexts


async def upload_video(
    client,
    path,
    file_name=None,
    spoiler=False,
    randomCover=False,
):
    """Upload a video, probe metadata, attach a cover and build input media."""

    if _stop_requested():
        print("手动停止成功！")
        return None, None
    file_name = file_name or gen_media_file_name(path)
    uploaded = None
    for attempt in range(1, _max_try_count() + 1):
        if _stop_requested():
            print("手动停止成功！")
            return None, None
        try:
            uploaded = await _upload_with_fast_fallback(client, path)
            if uploaded is not None:
                break
        except Exception:
            print("第", attempt, "次，视频资源，使用超级上传方式")
            _print_trace()
            sleep_func = _optional_import("..util.need", "utils")
            waiter = getattr(sleep_func, "sleep_time_fun_no_log", None)
            if callable(waiter):
                try:
                    await _maybe_await(waiter(1, 4))
                except Exception:
                    await asyncio.sleep(1)
    if uploaded is None:
        print("视频资源，发生异常，普通上传")
        return None, None

    meta = _probe_video(path)
    duration = int(getattr(meta, "duration", 0) or 0)
    width = int(getattr(meta, "width", 0) or getattr(meta, "w", 0) or 0)
    height = int(getattr(meta, "height", 0) or getattr(meta, "h", 0) or 0)
    has_audio = bool(getattr(meta, "has_audio", True))
    print("视频音轨: ", "有" if has_audio else "无")
    thumb_path = _extract_cover(path, random_cover=randomCover)
    thumb = await _upload_thumb(client, thumb_path)

    try:
        from telethon.tl import types
    except Exception:
        return None, None
    attributes = [types.DocumentAttributeFilename(file_name)]
    if width and height:
        attributes.append(types.DocumentAttributeImageSize(width, height))
    try:
        video_attr = types.DocumentAttributeVideo(
            duration=duration,
            w=width,
            h=height,
            round_message=False,
            supports_streaming=True,
            nosound=not has_audio,
        )
    except TypeError:
        video_attr = types.DocumentAttributeVideo(
            duration=duration,
            w=width,
            h=height,
            round_message=False,
            supports_streaming=True,
        )
    attributes.append(video_attr)
    try:
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type="video/mp4",
            attributes=attributes,
            thumb=thumb,
            spoiler=spoiler,
            nosound_video=not has_audio,
        )
    except TypeError:
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type="video/mp4",
            attributes=attributes,
            thumb=thumb,
            spoiler=spoiler,
        )
    context = _make_part_context(path, uploaded, _FAST_UPLOAD_PART_SIZE, role="video")
    return media, context


async def upload_normal_file(
    client,
    path,
    mime_type=None,
    force_file=False,
):
    """Upload a generic file with the fast path and Telethon fallback."""

    if _stop_requested():
        print("手动停止成功！")
        return None, None
    uploaded = None
    for attempt in range(1, _max_try_count() + 1):
        if _stop_requested():
            print("手动停止成功！")
            return None, None
        try:
            uploaded = await _upload_with_fast_fallback(client, path)
            if uploaded is not None:
                break
        except Exception:
            print("第", attempt, "次，通用文件资源，使用超级上传方式")
            _print_trace()
            waiter = _optional_import("..util.need", "utils")
            sleep_func = getattr(waiter, "sleep_time_fun_no_log", None)
            if callable(sleep_func):
                try:
                    await _maybe_await(sleep_func(1, 4))
                except Exception:
                    await asyncio.sleep(1)
    if uploaded is None:
        print("通用文件资源，发生异常，普通上传")
        return None, None
    try:
        from telethon.tl import types
    except Exception:
        return None, None
    file_name = gen_media_file_name(path)
    media = None
    try:
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            attributes=[types.DocumentAttributeFilename(file_name)],
            mime_type=mime_type or _mime_type(path),
            force_file=force_file,
        )
    except TypeError:
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            attributes=[types.DocumentAttributeFilename(file_name)],
            mime_type=mime_type or _mime_type(path),
        )
    context = _make_part_context(path, uploaded, _FAST_UPLOAD_PART_SIZE, role="file")
    return media, context


async def upload_photo(client, path, spoiler=False):
    """Upload an image and return ``InputMediaUploadedPhoto`` with context."""

    if _stop_requested():
        print("手动停止成功！")
        return None, None
    uploader = getattr(client, "upload_file", None)
    if not callable(uploader):
        print("图片资源，普通上传")
        return None, None
    callback = getattr(_call_back_module(), "upload_progress_bar", None)
    try:
        uploaded = await _maybe_await(
            uploader(
                path,
                progress_callback=callback,
                max_retries=_max_try_count(),
            )
        )
    except TypeError:
        uploaded = await _maybe_await(uploader(path))
    except Exception:
        _print_trace()
        uploaded = await _maybe_await(uploader(path))
    if uploaded is None:
        return None, None
    try:
        from telethon.tl import types
    except Exception:
        return None, None
    try:
        media = types.InputMediaUploadedPhoto(file=uploaded, spoiler=spoiler)
    except TypeError:
        media = types.InputMediaUploadedPhoto(file=uploaded)
    context = _make_part_context(
        path,
        uploaded,
        _telethon_default_part_size(os.path.getsize(path)),
        role="photo",
    )
    return media, context
