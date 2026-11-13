# Recovered module: src.py.com.yun.mao.auto.VideoFirstFrameCoverHelper
# Static reconstruction from Nuitka metadata, string constants, and control flow.
from __future__ import annotations

import asyncio
import ctypes
import os
import subprocess
import tempfile

from telethon import utils as tg_utils

from src.py.com.yun.mao.cd import Working
from src.py.com.yun.mao.config import YunYinMaoConfig
from src.py.com.yun.mao.telefast import CallBack, FastDownUpLoadUtils
from src.py.com.yun.mao.util import AccelUtils
from src.py.com.yun.mao.util.FloodGuard import with_flood_retry
from src.py.com.yun.mao.util.need import utils

from .IsoBmffFirstFrameParser import (
    IsoBmffAnalysis,
    analyze_iso_bmff,
    detect_container,
    estimate_tail_metadata_bytes,
    head_has_incomplete_top_level_moov,
)


_TG_MB = 1024 * 1024
_TG_FILE_ALIGN = 4096
_WHOLE_FILE_MAX_SIZE = 10 * _TG_MB
_TG_LARGE_FILE = 17 * _TG_MB
_TG_LARGE_LIMITS = (524288, 1048576, 2097152, 4194304)
_HEAD_STAGES = (524288, 262144, 131072, 65536, 32768, 16384, 8192, 4096)
_TAIL_STAGES = (131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216)
# inferred: symbol names are confirmed; which 8 MiB literal belongs to which
# cap is reconstructed from use sites and the surrounding numeric pool.
_MAX_METADATA_TAIL_BYTES = 16777216
_MAX_METADATA_HEAD_BYTES = 8388608
_MAX_UNIQUE_DOWNLOAD_BYTES = 8388608
_AVI_TAIL_BYTES = 8388608
_MAX_DENSE_GAP_BYTES = 1048576
_FFMPEG_TIMEOUT_SECONDS = 30


def _align_down(value: int, align: int) -> int:
    align = max(1, int(align or 1))
    return (max(0, int(value or 0)) // align) * align


def _align_up(value: int, align: int) -> int:
    align = max(1, int(align or 1))
    value = max(0, int(value or 0))
    return ((value + align - 1) // align) * align


def _file_align(value: int) -> int:
    return _align_down(value, _TG_FILE_ALIGN)


def _file_size(path: str) -> int:
    try:
        return max(0, int(os.path.getsize(path)))
    except OSError:
        return 0


def _file_ready(path: str) -> bool:
    return bool(path) and _file_size(path) > 0


def _read_file_bytes(path: str) -> bytes:
    try:
        with open(path, "rb") as in_file:
            return in_file.read()
    except OSError:
        return b""


def _document_download_size(document) -> int:
    if document is None:
        return 0
    size = int(getattr(document, "size", 0) or 0)
    try:
        _, location = tg_utils.get_input_location(document)
        size = int(getattr(location, "size", 0) or size or 0)
    except Exception:
        pass
    return max(0, size)


def _head_range(file_size: int, head_bytes: int) -> tuple[int, int]:
    file_size = max(0, int(file_size or 0))
    requested = min(file_size, max(0, int(head_bytes or 0)))
    download = min(file_size, _align_up(requested, _TG_FILE_ALIGN))
    return 0, download


def _tail_range(file_size: int, tail_bytes: int) -> tuple[int, int]:
    file_size = max(0, int(file_size or 0))
    requested = min(file_size, max(0, int(tail_bytes or 0)))
    raw_start = max(0, file_size - requested)
    byte_offset = _align_down(raw_start, _TG_FILE_ALIGN)
    download = max(0, file_size - byte_offset)
    return byte_offset, download


def _pick_chunk_limit(remaining: int, file_size: int, byte_offset: int) -> int:
    remaining = max(0, int(remaining or 0))
    file_size = max(0, int(file_size or 0))
    byte_offset = max(0, int(byte_offset or 0))
    remain_in_file = max(0, file_size - byte_offset)
    if file_size <= _TG_LARGE_FILE:
        mb_cap = max(_TG_LARGE_LIMITS)
    else:
        mb_cap = min(_TG_LARGE_LIMITS)
    cap = min(remaining, remain_in_file, mb_cap, _MAX_UNIQUE_DOWNLOAD_BYTES)
    if cap <= 0:
        return 0
    return max(1, min(cap, _align_up(cap, _TG_FILE_ALIGN)))


def _range_progress(written: int, _chunk_total: int, base: tuple[int, int]) -> None:
    initial_size, range_total = base
    if range_total <= 0:
        return
    completed_before_chunk = max(0, int(initial_size or 0))
    current = min(range_total, completed_before_chunk + max(0, int(written or 0)))
    CallBack.down_progress_bar(current, range_total)


async def _download_range(
    client,
    document,
    partial_path: str,
    byte_offset: int,
    max_bytes: int,
    file_size: int,
    append: bool = False,
) -> None:
    file_size = max(0, int(file_size or 0))
    byte_offset = max(0, int(byte_offset or 0))
    remaining = min(max(0, int(max_bytes or 0)), max(0, file_size - byte_offset))
    if remaining <= 0 or document is None:
        return
    initial_size = _file_size(partial_path) if append else 0
    range_total = initial_size + remaining
    first = True
    current_offset = byte_offset
    while remaining > 0:
        if Working.need_stop:
            print("封面下载已停止")
            raise asyncio.CancelledError
        chunk_limit = _pick_chunk_limit(remaining, file_size, current_offset)
        if chunk_limit <= 0:
            break
        size_before = _file_size(partial_path)
        callback = lambda current, total, *args, base=(initial_size, range_total): _range_progress(
            current, total, base
        )
        try:
            await with_flood_retry(
                lambda: FastDownUpLoadUtils.fast_down_load_partial(
                    client,
                    document,
                    partial_path,
                    max_bytes=chunk_limit,
                    byte_offset=current_offset,
                    append=append if first else True,
                    progress_callback=callback,
                    reset_timer=first,
                ),
                max_retries=YunYinMaoConfig.MAX_TRY_COUNT,
                prefix="video_cover_partial_download",
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            print(
                "部分下载视频失败（offset=",
                current_offset,
                ", limit=",
                chunk_limit,
                "）：",
                exc,
            )
            raise
        size_after = _file_size(partial_path)
        got = max(0, size_after - size_before)
        if got <= 0:
            print(
                "部分下载无数据（offset=",
                current_offset,
                ", 期望=",
                chunk_limit,
                "，文件大小=",
                size_after,
                "）",
            )
            break
        current_offset += got
        remaining = max(0, remaining - got)
        first = False


async def _ensure_head_bytes(
    client,
    document,
    head_path: str,
    file_size: int,
    current_bytes: int,
    target_bytes: int,
) -> int:
    current = min(file_size, max(0, int(current_bytes or _file_size(head_path))))
    target = min(
        file_size,
        _MAX_METADATA_HEAD_BYTES,
        _align_up(max(0, int(target_bytes or 0)), _TG_FILE_ALIGN),
    )
    if target <= current:
        return current
    add_bytes = target - current
    print("封面下载：头部增量 offset=", current, ", target=", target)
    await _download_range(
        client,
        document,
        head_path,
        current,
        add_bytes,
        file_size,
        append=current > 0,
    )
    actual = _file_size(head_path)
    if actual < target:
        print("head 下载不完整：期望=", target, "，实际=", actual)
    return actual


async def _ensure_tail_bytes(
    client,
    document,
    tail_path: str,
    prefix_path: str,
    file_size: int,
    current_offset: int,
    target_bytes: int,
) -> tuple[int, int]:
    # inferred: prefix/old-tail overlap merge follows the recovered locals;
    # the exact retry ordering is not present in the static strings.
    file_size = max(0, int(file_size or 0))
    target_length = min(file_size, max(0, int(target_bytes or 0)))
    target_offset = _align_down(max(0, file_size - target_length), _TG_FILE_ALIGN)
    target_length = max(0, file_size - target_offset)
    existing = _file_size(tail_path)
    if (
        existing == target_length
        and current_offset == target_offset
        and target_length > 0
    ):
        return target_offset, target_length

    prefix_length = min(target_length, _TG_FILE_ALIGN)
    prefix_actual = 0
    if prefix_length > 0:
        await _download_range(
            client,
            document,
            prefix_path,
            target_offset,
            prefix_length,
            file_size,
            append=False,
        )
        prefix_actual = _file_size(prefix_path)
    if prefix_actual <= 0:
        return target_offset, 0

    old_tail = _read_file_bytes(tail_path) if existing else b""
    merged = bytearray(_read_file_bytes(prefix_path)[:prefix_actual])
    if old_tail and current_offset == target_offset + prefix_actual:
        merged.extend(old_tail)
    with open(tail_path, "wb") as tail_file:
        tail_file.write(merged[:target_length])
    if len(merged) < target_length:
        print(
            "封面下载：tail 增量 offset=",
            target_offset + len(merged),
            ", target=",
            target_length,
        )
        await _download_range(
            client,
            document,
            tail_path,
            target_offset + len(merged),
            target_length - len(merged),
            file_size,
            append=True,
        )
    actual = _file_size(tail_path)
    if actual != target_length:
        print("tail 下载不完整：期望=", target_length, "，实际=", actual)
    return target_offset, actual


def _metadata_head_target(
    analysis: IsoBmffAnalysis,
    file_size: int,
    tail_bytes: int,
) -> int:
    required = max(0, int(getattr(analysis, "required_head_end", 0) or 0))
    max_head = min(
        _MAX_METADATA_HEAD_BYTES,
        max(0, int(file_size or 0) - max(0, int(tail_bytes or 0))),
    )
    target = min(max_head, _align_up(required, _TG_FILE_ALIGN))
    return max(0, target)


def _tail_download_targets(head: bytes, file_size: int) -> tuple[int, tuple[int, ...]]:
    estimated = estimate_tail_metadata_bytes(
        head,
        file_size,
        _MAX_METADATA_TAIL_BYTES,
    )
    first_target = min(
        _MAX_METADATA_TAIL_BYTES,
        max(_TG_FILE_ALIGN, estimated or _TAIL_STAGES[0]),
    )
    targets = {first_target}
    for stage in _TAIL_STAGES:
        if stage <= _MAX_METADATA_TAIL_BYTES:
            targets.add(stage)
    return estimated, tuple(sorted(targets))


def _enable_sparse_file(file_obj) -> bool:
    if os.name != "nt":
        return False
    try:
        import msvcrt
        from ctypes import wintypes

        fsctl_set_sparse = 590020
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        device_io_control = kernel32.DeviceIoControl
        device_io_control.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        ]
        device_io_control.restype = wintypes.BOOL
        returned = wintypes.DWORD(0)
        handle = wintypes.HANDLE(msvcrt.get_osfhandle(file_obj.fileno()))
        return bool(
            device_io_control(
                handle,
                fsctl_set_sparse,
                None,
                0,
                None,
                0,
                ctypes.byref(returned),
                None,
            )
        )
    except Exception as exc:
        print("启用 NTFS sparse 失败: ", exc)
        return False


def _assemble_head_tail_mp4(
    head_path: str,
    tail_path: str,
    out_path: str,
    file_size: int,
    tail_byte_offset: int | None,
) -> bool:
    if tail_byte_offset is None:
        return False
    head = _read_file_bytes(head_path)
    tail = _read_file_bytes(tail_path)
    if not head or not tail:
        return False
    tail_byte_offset = max(0, min(int(tail_byte_offset), int(file_size or 0)))
    if tail_byte_offset < len(head):
        overlap = len(head) - tail_byte_offset
        tail = tail[overlap:]
    gap = max(0, tail_byte_offset - len(head))
    sparse_enabled = False
    try:
        with open(out_path, "w+b") as out_file:
            sparse_enabled = _enable_sparse_file(out_file)
            if gap > _MAX_DENSE_GAP_BYTES and not sparse_enabled:
                print(
                    "文件系统不支持 sparse，拒绝创建 ",
                    gap,
                    " 字节的稠密空洞",
                )
                return False
            out_file.write(head)
            out_file.seek(tail_byte_offset)
            out_file.write(tail)
            out_file.truncate(int(file_size or (tail_byte_offset + len(tail))))
            out_file.flush()
            os.fsync(out_file.fileno())
        print(
            "封面临时文件：logical=",
            file_size,
            ", sparse=",
            "yes" if sparse_enabled else "dense-small-gap",
        )
        return True
    except OSError as exc:
        print("封面临时文件组装失败: ", exc)
        return False


async def _extract_first_frame(
    video_path: str,
    cover_path: str,
    input_format: str | None,
) -> bool:
    ffmpeg = AccelUtils.resolve_ffmpeg_bin()
    if not ffmpeg:
        return False
    cmd = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-probesize",
        "32M",
        "-analyzeduration",
        "10M",
        "-an",
        "-sn",
        "-dn",
        "-fflags",
        "+genpts+discardcorrupt+igndts",
        "-err_detect",
        "ignore_err",
    ]
    if input_format in ("raw_m4v", "m4v"):
        cmd.extend(["-f", "m4v"])
    cmd.extend(
        [
            "-i",
            video_path,
            "-frames:v",
            "1",
            "-q:v",
            "2",
            cover_path,
        ]
    )
    kwargs = AccelUtils.subprocess_no_console_kwargs()
    if not isinstance(kwargs, dict):
        kwargs = {}
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **kwargs,
        )
    except Exception as exc:
        print("ffmpeg 截取视频首帧失败: ", exc)
        return False

    loop = asyncio.get_running_loop()
    communicate_task = asyncio.create_task(process.communicate())
    deadline = loop.time() + _FFMPEG_TIMEOUT_SECONDS
    try:
        while not communicate_task.done():
            if Working.need_stop:
                process.kill()
                communicate_task.cancel()
                await asyncio.gather(communicate_task, return_exceptions=True)
                print("视频首帧截取已停止")
                return False
            remaining = deadline - loop.time()
            if remaining <= 0:
                process.kill()
                communicate_task.cancel()
                await asyncio.gather(communicate_task, return_exceptions=True)
                print("ffmpeg 截帧超时（", _FFMPEG_TIMEOUT_SECONDS, "秒）")
                return False
            await asyncio.wait({communicate_task}, timeout=min(0.25, remaining))
        stdout, stderr = await communicate_task
    except asyncio.CancelledError:
        if process.returncode is None:
            process.kill()
        await asyncio.gather(communicate_task, return_exceptions=True)
        raise
    except Exception as exc:
        if process.returncode is None:
            process.kill()
            await process.wait()
        print("ffmpeg 截取视频首帧失败: ", exc)
        return False

    if process.returncode != 0:
        err = (stderr or b"").decode("utf-8", "replace").strip()
        if "moov atom not found" in err:
            print("ffmpeg 截帧失败: moov atom not found")
        else:
            print("ffmpeg 截帧失败: ", err[:200])
        return False
    return _file_ready(cover_path)


async def _try_head_only_stages(
    head_path: str,
    cover_path: str,
    file_size: int,
    current_bytes: int,
    input_format: str | None,
) -> tuple[bool, int]:
    attempted = 0
    last_attempted_size = -1
    for target in _HEAD_STAGES:
        if target > current_bytes:
            continue
        if target == last_attempted_size:
            continue
        last_attempted_size = target
        attempted = target
        if await _extract_first_frame(head_path, cover_path, input_format):
            return True, attempted
    return False, attempted or current_bytes


async def _try_assembled_frame(
    head_path: str,
    tail_path: str,
    partial_path: str,
    cover_path: str,
    file_size: int,
    tail_offset: int,
) -> bool:
    if not _assemble_head_tail_mp4(
        head_path,
        tail_path,
        partial_path,
        file_size,
        tail_offset,
    ):
        return False
    success = await _extract_first_frame(partial_path, cover_path, "mp4")
    utils.safe_del_file(partial_path)
    return success


async def _fallback_thumb_download(client, msg, pic_path: str) -> str:
    # inferred: thumb=-1 selects Telegram's largest thumbnail.
    if not pic_path:
        pic_path = os.path.join(
            tempfile.gettempdir(),
            f"video_thumb_{getattr(msg, 'id', 0) or 0}.jpg",
        )
    temp_path = pic_path + ".download"
    result = None
    try:
        result = await with_flood_retry(
            lambda: client.download_media(msg, file=temp_path, thumb=-1),
            max_retries=YunYinMaoConfig.MAX_TRY_COUNT,
            prefix="video_cover_thumb",
        )
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        print("Telegram 缩略图下载失败: ", exc)
    if result is None:
        print("Telegram 缩略图下载结果为空")
    if _file_ready(temp_path):
        try:
            os.replace(temp_path, pic_path)
        except OSError:
            return temp_path
    if _file_ready(pic_path):
        return pic_path
    utils.safe_del_file(temp_path)
    return ""


async def download_video_cover_from_first_frame(client, msg) -> str:
    document = getattr(msg, "document", None)
    if document is None:
        media = getattr(msg, "media", None)
        document = getattr(media, "document", None)
    if document is None:
        print("封面下载：无法获取文件大小，回退到 Telegram 缩略图")
        return await _fallback_thumb_download(client, msg, "")

    file_size = _document_download_size(document)
    if file_size <= 0:
        print("封面下载：无法获取文件大小，回退到 Telegram 缩略图")
        return await _fallback_thumb_download(client, msg, "")

    file_path = getattr(getattr(msg, "file", None), "name", None)
    if not file_path:
        file_path = f"video_{getattr(msg, 'id', 0) or 0}.mp4"
    dir_path = tempfile.mkdtemp(prefix="video_cover_")
    filename = os.path.basename(str(file_path))
    name_without_ext, ext = os.path.splitext(filename)
    if not ext:
        ext = ".mp4"
    cover_path = os.path.join(dir_path, name_without_ext + ".jpg")
    partial_video_path = os.path.join(
        dir_path,
        name_without_ext + "_cover_partial" + ext,
    )
    head_path = os.path.join(dir_path, name_without_ext + "_cover_head" + ext)
    tail_path = os.path.join(dir_path, name_without_ext + "_cover_tail" + ext)
    tail_prefix_path = os.path.join(
        dir_path,
        name_without_ext + "_cover_tail_prefix" + ext,
    )

    try:
        if file_size <= _WHOLE_FILE_MAX_SIZE:
            print("封面下载：文件 ", file_size, " 字节，整段下载后截帧")
            await _download_range(
                client,
                document,
                partial_video_path,
                0,
                file_size,
                file_size,
                append=False,
            )
            head_data = _read_file_bytes(partial_video_path)[:65536]
            container = detect_container(head_data, ext)
            input_format = "m4v" if container == "raw_m4v" else None
            success = await _extract_first_frame(
                partial_video_path,
                cover_path,
                input_format,
            )
            if success:
                print(
                    "成功从视频首帧生成高清封面（整段 ",
                    file_size,
                    " 字节）: ",
                    cover_path,
                )
                return cover_path
            print("完整小文件仍无法截帧，直接回退缩略图")
            return await _fallback_thumb_download(client, msg, cover_path)

        head_target = min(file_size, _HEAD_STAGES[0])
        head_downloaded = await _ensure_head_bytes(
            client,
            document,
            head_path,
            file_size,
            0,
            head_target,
        )
        head_data = _read_file_bytes(head_path)
        analysis = IsoBmffAnalysis(False, None, "moov_not_complete")
        try:
            analysis = analyze_iso_bmff(head_data, file_size)
        except Exception as exc:
            print("视频轨样本范围不可用：", exc)
        container = detect_container(head_data, ext)
        print("封面下载：识别容器=", container)
        input_format = "m4v" if container == "raw_m4v" else None

        if container == "classic_mp4" and analysis.moov_complete:
            head_target = _metadata_head_target(analysis, file_size, 0)
            head_downloaded = await _ensure_head_bytes(
                client,
                document,
                head_path,
                file_size,
                head_downloaded,
                head_target,
            )
            if head_target and head_target <= head_downloaded:
                print("视频轨首关键帧精确 head 目标=", head_target)
                success = await _extract_first_frame(
                    head_path,
                    cover_path,
                    input_format,
                )
                if success:
                    print(
                        "成功从 faststart 视频首帧生成高清封面（head=",
                        head_downloaded,
                        "）",
                    )
                    return cover_path

        success, attempted = await _try_head_only_stages(
            head_path,
            cover_path,
            file_size,
            head_downloaded,
            input_format,
        )
        if success:
            print(
                "成功从视频首帧生成高清封面（",
                container,
                " head-only）: ",
                cover_path,
            )
            return cover_path

        if container == "avi":
            tail_offset, tail_downloaded = await _ensure_tail_bytes(
                client,
                document,
                tail_path,
                tail_prefix_path,
                file_size,
                0,
                _AVI_TAIL_BYTES,
            )
            if tail_downloaded:
                success = await _try_assembled_frame(
                    head_path,
                    tail_path,
                    partial_video_path,
                    cover_path,
                    file_size,
                    tail_offset,
                )
                if success:
                    print(
                        "成功从 AVI 首帧生成高清封面（head=",
                        head_downloaded,
                        ", tail=",
                        tail_downloaded,
                        "）",
                    )
                    return cover_path
            print(" 头部策略截帧失败，回退缩略图")
            return await _fallback_thumb_download(client, msg, cover_path)

        tail_estimated, tail_targets = _tail_download_targets(head_data, file_size)
        if tail_estimated:
            print("封面下载：根据 mdat 边界估算尾部元数据=", tail_estimated, " 字节")
        tail_offset = 0
        tail_downloaded = 0
        for tail_target in tail_targets:
            if Working.need_stop:
                print("封面下载已停止")
                raise asyncio.CancelledError
            if tail_target <= tail_downloaded:
                continue
            tail_offset, tail_downloaded = await _ensure_tail_bytes(
                client,
                document,
                tail_path,
                tail_prefix_path,
                file_size,
                tail_offset,
                tail_target,
            )
            if not tail_downloaded:
                continue
            print(
                "封面下载：tail offset=",
                tail_offset,
                ", size=",
                tail_downloaded,
            )
            success = await _try_assembled_frame(
                head_path,
                tail_path,
                partial_video_path,
                cover_path,
                file_size,
                tail_offset,
            )
            if success:
                if container == "fragmented_mp4":
                    print(
                        "成功从 fMP4 首帧生成高清封面（head=",
                        head_downloaded,
                        ", tail=",
                        tail_downloaded,
                        "）",
                    )
                else:
                    print(
                        "成功从视频首帧生成高清封面（head=",
                        head_downloaded,
                        ", tail=",
                        tail_downloaded,
                        "）: ",
                        cover_path,
                    )
                return cover_path
            if not analysis.moov_complete and head_has_incomplete_top_level_moov(
                head_data
            ):
                print(" 尚无完整 moov，继续增量扩展")
            if tail_downloaded >= min(file_size, _MAX_UNIQUE_DOWNLOAD_BYTES):
                break
        print("部分下载截帧失败，回退到 Telegram 缩略图")
        return await _fallback_thumb_download(client, msg, cover_path)
    except asyncio.CancelledError:
        print("封面下载已停止")
        raise
    except Exception as exc:
        print("部分下载截帧失败，回退到 Telegram 缩略图: ", exc)
        return await _fallback_thumb_download(client, msg, cover_path)
    finally:
        for path in (head_path, tail_path, tail_prefix_path, partial_video_path):
            if path:
                utils.safe_del_file(path)
