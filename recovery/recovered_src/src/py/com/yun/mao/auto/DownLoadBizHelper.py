# Recovered module: src.py.com.yun.mao.auto.DownLoadBizHelper
# Reconstruction from the Nuitka code-object table, constants and the
# download call sites used by DownLoadProcess.  Function name and argument
# counts come from the module init; a few retry/fallback details are inferred.
from __future__ import annotations

import asyncio
import hashlib
import importlib
import inspect
import os
import re
import traceback
import uuid
from typing import Any, Dict, Optional


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


def _as_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_bool(value, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


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


def _call_back_module():
    return _optional_import("..telefast", "CallBack")


def _safe_suffix(value: str) -> str:
    suffix = str(value or "").strip()
    if not suffix:
        return ""
    if not suffix.startswith("."):
        suffix = "." + suffix
    suffix = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", suffix)
    return suffix[:20]


def _document_name(document, message=None) -> str:
    name = getattr(document, "attributes", None)
    if name:
        for attribute in document.attributes or []:
            candidate = getattr(attribute, "file_name", None)
            if candidate:
                return str(candidate)
    for source in (document, message):
        candidate = getattr(source, "file_name", None) or getattr(
            source, "name", None
        )
        if candidate:
            return str(candidate)
    message_id = _as_int(getattr(message, "id", 0), 0)
    if getattr(document, "mime_type", None) == "image/jpeg":
        return f"photo_{message_id or uuid.uuid4().hex[:8]}.jpg"
    if getattr(document, "mime_type", None) == "video/mp4":
        return f"video_{message_id or uuid.uuid4().hex[:8]}.mp4"
    return f"resource_{message_id or uuid.uuid4().hex[:8]}"


async def _fetch_updated_message(client, source_channel, msg):
    """Re-fetch a message before downloading its media."""

    getter = getattr(client, "get_messages", None)
    if callable(getter):
        try:
            result = await _maybe_await(
                getter(source_channel, ids=getattr(msg, "id", None))
            )
            if isinstance(result, (list, tuple)):
                result = result[0] if result else None
            if result is not None:
                return result
        except Exception:
            print("观察中——更新引用失败！")
    return msg


def _get_root_directory(is_download_flow: bool) -> str:
    """Return the configured work directory for normal/download-only flows."""

    config = _optional_import("..config", "YunYinMaoConfig")
    if is_download_flow:
        name = "yun_yin_ban_yun_folder_only_down_load"
    else:
        name = "yun_yin_ban_yun_folder"
    value = getattr(config, name, None) if config else None
    if not value:
        value = os.path.join(os.path.expanduser("~"), "YunYinMao", "download")
    value = os.fspath(value)
    try:
        os.makedirs(value, exist_ok=True)
    except Exception:
        pass
    return value


def _build_and_reserve_file_path(
    root_dir,
    text,
    origin_file_name,
    target_suffix,
    media_index,
):
    """Build a collision-free target path and reserve it atomically.

    The original combines the sanitized source name with a short text digest
    and a zero-padded media index.  The UUID and emergency branches are
    inferred fallbacks for invalid or exhausted names.
    """

    root_dir = os.fspath(root_dir or ".")
    try:
        os.makedirs(root_dir, exist_ok=True)
    except Exception:
        pass

    common = _optional_import("..util.need", "CommonCode")
    obtain = getattr(common, "obtainFileNameAndSuffix", None) if common else None
    if callable(obtain):
        try:
            value = obtain(origin_file_name)
            if isinstance(value, (list, tuple)) and len(value) >= 2:
                origin_file_name, target_suffix = value[0], value[1]
        except Exception:
            pass

    origin_file_name = str(origin_file_name or "")
    base_name, source_suffix = os.path.splitext(os.path.basename(origin_file_name))
    suffix = _safe_suffix(target_suffix or source_suffix)
    normalized_text = re.sub(r"[^\w\s]+", " ", str(text or ""))
    normalized_text = re.sub(r"#[^\s#]+", " ", normalized_text)
    normalized_text = re.sub(r"\s+", " ", normalized_text).strip()
    digest = hashlib.md5(normalized_text.encode("utf-8")).hexdigest()[:8]
    safe_base = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", base_name)
    safe_base = safe_base.rstrip("_ .") or "resource"
    max_len = max(8, 91 - len(suffix) - 9)
    safe_base = safe_base[:max_len]
    index = max(0, _as_int(media_index, 0))

    candidates = [
        f"{safe_base}_{digest}_{index:02d}{suffix}",
        f"{safe_base}_{digest}_{index:02d}_{uuid.uuid4().hex[:6]}{suffix}",
        f"resource_{uuid.uuid4().hex}{suffix}",
    ]
    for candidate in candidates:
        path = os.path.join(root_dir, candidate)
        try:
            fd = os.open(
                path,
                os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                0o600,
            )
            os.close(fd)
            return path
        except FileExistsError:
            continue
        except Exception:
            break

    fallback_path = os.path.join(
        root_dir,
        f"emergency_{uuid.uuid4().hex}{suffix}",
    )
    try:
        fd = os.open(fallback_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
    except Exception:
        pass
    return fallback_path


def _cleanup_empty_placeholder(file_path, download_success):
    """Remove the empty file reserved before a failed download."""

    if download_success or not file_path:
        return
    try:
        if os.path.isfile(file_path) and os.path.getsize(file_path) <= 0:
            os.remove(file_path)
    except Exception:
        pass


async def _handle_picture_download(client, msg, file_path):
    """Download a photo, or extract the first frame when the thumb hits video."""

    helper = _optional_import(".VideoFirstFrameCoverHelper")
    frame_downloader = (
        getattr(helper, "download_video_cover_from_first_frame", None)
        if helper
        else None
    )
    if callable(frame_downloader) and _as_bool(
        getattr(msg, "download_thumb_hit_video", False)
    ):
        try:
            value = frame_downloader(client, msg, file_path)
            value = await _maybe_await(value)
            if value:
                return os.fspath(value)
        except Exception:
            _print_trace()

    downloader = getattr(client, "download_media", None)
    if not callable(downloader):
        return file_path
    try:
        value = await _maybe_await(downloader(msg, file=file_path))
        return os.fspath(value) if value else file_path
    except Exception:
        _print_trace()
        return file_path


async def _retry_fast_download(client, document, file_path):
    """Try the accelerator download path for a document."""

    helper = _optional_import("..telefast", "FastDownUpLoadUtils")
    fast_download = getattr(helper, "fast_down_load", None) if helper else None
    if not callable(fast_download):
        return False
    try:
        value = fast_download(
            client=client,
            document=document,
            file_path=file_path,
        )
        await _maybe_await(value)
        return os.path.isfile(file_path) and os.path.getsize(file_path) > 0
    except TypeError:
        try:
            value = fast_download(client, document, file_path)
            await _maybe_await(value)
            return os.path.isfile(file_path) and os.path.getsize(file_path) > 0
        except Exception:
            _print_trace()
    except Exception:
        _print_trace()
    return False


async def _retry_normal_download(client, media, file_path):
    """Use Telethon's normal download with flood retry and retry count."""

    downloader = getattr(client, "download_media", None)
    if not callable(downloader):
        return False
    config = _optional_import("..config", "YunYinMaoConfig")
    part_size = _as_int(
        getattr(config, "normal_down_load_part_size_kb", 512),
        512,
    )
    flood = _optional_import("..util", "FloodGuard")
    with_retry = getattr(flood, "with_flood_retry", None) if flood else None
    max_retries = max(1, _as_int(getattr(config, "MAX_TRY_COUNT", 3), 3))
    for retry_count in range(1, max_retries + 1):
        if _stop_requested():
            print("手动停止成功！")
            return False
        try:
            callback_cls = _call_back_module()
            callback = callback_cls() if callable(callback_cls) else None
            kwargs = {
                "file": file_path,
                "part_size_kb": part_size,
                "progress_callback": callback,
            }
            if callable(with_retry):
                value = with_retry(
                    lambda: downloader(media, **kwargs),
                    prefix="DownLoadBizHelper/normal_download",
                )
            else:
                value = downloader(media, **kwargs)
            value = await _maybe_await(value)
            if value and os.path.isfile(file_path):
                return os.path.getsize(file_path) > 0
        except Exception:
            print(f"第{retry_count}次，使用普通下载方式")
            _print_trace()
            waiter = _optional_import("..util.need", "utils")
            sleep_func = getattr(waiter, "sleep_time_fun_no_log", None)
            if callable(sleep_func):
                try:
                    await _maybe_await(sleep_func(1, 4))
                except Exception:
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)
    return False


async def _download_with_retry(client, message, file_path):
    """Run the fast path first, then the normal Telethon path."""

    if _stop_requested():
        print("手动停止成功！")
        return False
    media = getattr(message, "media", None) or getattr(message, "document", None)
    document = getattr(media, "document", None) or media
    config = _optional_import("..config", "YunYinMaoConfig")
    max_try = max(1, _as_int(getattr(config, "MAX_TRY_COUNT", 3), 3))
    for retry_count in range(1, max_try + 1):
        if await _retry_fast_download(client, document, file_path):
            return True
        print(f"第{retry_count}次，使用超级下载方式")
    return await _retry_normal_download(client, media, file_path)


def _modify_md5_if_media(file_path):
    """Modify a downloaded media file's MD5 when the common helper allows it."""

    if not file_path or not os.path.isfile(file_path):
        return False
    common = _optional_import("..util.need", "CommonCode")
    is_video = getattr(common, "localFileIsVideo", None) if common else None
    is_photo = getattr(common, "localFileIsPhoto", None) if common else None
    if not (
        (callable(is_video) and is_video(file_path))
        or (callable(is_photo) and is_photo(file_path))
    ):
        return False
    utils = _optional_import("..util.need", "utils")
    calculate_md5 = getattr(utils, "calculate_md5", None) if utils else None
    modify_md5 = getattr(utils, "modify_media_md5", None) if utils else None
    try:
        original_md5 = calculate_md5(file_path) if callable(calculate_md5) else None
        if callable(modify_md5):
            modify_md5(file_path)
        modified_md5 = calculate_md5(file_path) if callable(calculate_md5) else None
        if original_md5 or modified_md5:
            print(f"原始媒体 MD5: {original_md5}")
            print(f"修改后的 MD5: {modified_md5}")
        return True
    except Exception as exc:
        print(f"MD5修改异常（忽略）: {exc!r}")
        return False


async def biz_download_only(
    log_pre_tag="",
    client=None,
    at_name=None,
    text="",
    source_channel=None,
    messages=None,
    is_download_flow=False,
    download_thumb_hit_video=True,
):
    """Download every media message in a source group.

    Returns a ``{local_path: message}`` map.  The caller in DownLoadProcess
    consumes this map as the downloaded-resource set and keeps the paths in
    ``all_temp_files`` for later watermark/upload steps.
    """

    messages = list(messages or [])
    path_message_map: Dict[str, Any] = {}
    if not messages:
        return path_message_map

    root_dir = _get_root_directory(_as_bool(is_download_flow))
    total = len(messages)
    for index, raw_msg in enumerate(messages):
        if _stop_requested():
            print("手动停止成功！")
            break
        msg = await _fetch_updated_message(client, source_channel, raw_msg)
        media = getattr(msg, "media", None)
        document = getattr(media, "document", None)
        photo = getattr(media, "photo", None)
        if not media and not document and not photo:
            continue

        origin_file_name = _document_name(document, msg)
        target_suffix = os.path.splitext(origin_file_name)[1]
        file_path = _build_and_reserve_file_path(
            root_dir,
            text,
            origin_file_name,
            target_suffix,
            index,
        )
        print(
            f"{log_pre_tag or ''} 第 {index + 1}/{total}，开始下载..."
        )
        download_success = False
        try:
            if photo and not document:
                await _handle_picture_download(client, msg, file_path)
                download_success = os.path.isfile(file_path)
            elif _as_bool(download_thumb_hit_video) and _as_bool(
                getattr(msg, "download_thumb_hit_video", False)
            ):
                await _handle_picture_download(client, msg, file_path)
                download_success = os.path.isfile(file_path)
            else:
                download_success = await _download_with_retry(
                    client,
                    msg,
                    file_path,
                )
        except Exception as exc:
            print(f"{log_pre_tag or ''}，下载异常: {exc!r}")
            _print_trace()

        _cleanup_empty_placeholder(file_path, download_success)
        if download_success and os.path.isfile(file_path):
            _modify_md5_if_media(file_path)
            path_message_map[file_path] = msg
    return path_message_map
