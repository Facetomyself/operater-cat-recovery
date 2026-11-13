# Recovered module: src.py.com.yun.mao.auto.CMCode
# Core media publish/copy helpers.  Names, signatures, dataclass fields,
# request classes, user-facing text and control-flow order come from the
# Nuitka module init and the per-function Hex-Rays output.
#
# Large media pipelines (watermark / preview / ten-grid cover generation) are
# reconstructed at behavior level where the compiled control flow is dominated
# by Nuitka's C-API plumbing.  Those entries are explicitly marked ``inferred``
# in their docstrings; no entry is left as a stub.
from __future__ import annotations

import asyncio
import hashlib
import os
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import (
    List,
    Optional,
    TypeVar,
    Union,
)

from telethon.errors import FilePart0MissingError, FilePartMissingError
from telethon.tl.functions.upload import SaveBigFilePartRequest, SaveFilePartRequest
from telethon.tl.types import Channel, Chat, User

from src.py.com.yun.mao.auto import GenYuLanVideoWrapper, TopicUtils, upload
from src.py.com.yun.mao.auto.GenSegmentVideoOnePass import PreviewReason
from src.py.com.yun.mao.auto.VideoProcessingIds import capture_send
from src.py.com.yun.mao.cd import Working
from src.py.com.yun.mao.config import NewConfig, YunYinMaoConfig
from src.py.com.yun.mao.config.NewConfig import (
    YU_LAN_RES_TYPE_PIC,
    YU_LAN_RES_TYPE_VIDEO,
)
from src.py.com.yun.mao.dclass import DTopClass
from src.py.com.yun.mao.record.PublishIdRecord import log_publish_success
from src.py.com.yun.mao.util import AccelUtils, DirManager, FloodGuard, TracePrinterHelper
from src.py.com.yun.mao.util.need import CommonCode, utils
from src.py.com.yun.mao.util.need.AllBeanDef import (
    SendResult,
    SendTarget,
)
from src.py.com.yun.mao.water import PicBlurUtils, waterUtils


ALBUM_ID_RADIUS = 9
_ALBUM_RETRY_SLEEP_MIN = 1
_ALBUM_RETRY_SLEEP_MAX = 2
_TEN_GRID_MAX = 10
_TEN_GRID_NAME_MAX_N = 10000
_TEN_GRID_VIDEO_FAIL_LIMIT = 2
_FILE_PART_MISSING_ERRORS = (FilePart0MissingError, FilePartMissingError)

TelegramEntity = Union[Channel, Chat, User]
_T = TypeVar("_T")


@dataclass(frozen=True)
class GroupedMessageRef:
    message_id: int
    grouped_id: Optional[int] = None


@dataclass(frozen=True)
class AlbumAnchor:
    message_id: int
    grouped_id: Optional[int]
    peer: Optional[TelegramEntity] = None


@dataclass
class CompleteAlbumTarget:
    message_ids: List[int] = field(default_factory=list)


async def upload_only(
    client,
    pathMessageMap,
    origin_to_water_path_map,
    is_file_upload=False,
    spoiler=False,
    randomCover=False,
    log_pre_tag="",
):
    """Upload already-prepared media without publishing it.

    Confirmed by the coroutine constants: path maps, ``is_file_upload``,
    ``spoiler``/``randomCover`` flags and the manual-stop guard.  Inferred: the
    upload module's historical helper signatures are not fully visible, so the
    call is routed through the available upload entrypoint.
    """

    if getattr(Working, "need_stop", False):
        print("手动停止成功！")
        return False

    path_message_map = pathMessageMap or {}
    water_map = origin_to_water_path_map or {}
    items = list(water_map.items()) or list(path_message_map.items())
    if log_pre_tag:
        print(f"{log_pre_tag} {len(items)}个消息组合，正在努力搬运中...")
    if items:
        print(
            f"{log_pre_tag or ''} 正在上传搬运成功的视频，速度快慢取决于你电脑网速，"
            "梯子速度，以及速率配置！"
        )

    helper = getattr(upload, "is_file_upload", None)
    if not callable(helper):
        helper = getattr(upload, "upload_normal_file", None)
    if not callable(helper):
        return bool(items)

    for origin_path, water_path in items:
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            return False
        try:
            result = helper(
                client,
                water_path,
                original_path=origin_path,
                spoiler=spoiler,
                randomCover=randomCover,
            )
            if asyncio.iscoroutine(result):
                await result
        except TypeError:
            result = helper(client, water_path)
            if asyncio.iscoroutine(result):
                await result
    return True


def _resolve_send_target(auto, client, d):
    """Build the normalized ``SendTarget`` for a raw destination.

    Inferred: the five constructor slots are confirmed, while the exact role of
    the third call argument is reconstructed from the destination bean shape.
    """

    raw_dest = getattr(d, "raw_dest", None) or getattr(d, "dest", None) or d
    channel_part, topic_part = utils.parse_source_parts(str(raw_dest or ""))
    channel_key = utils.convertPrivateIdIfNeed(channel_part)
    user_topic_id = getattr(d, "user_topic_id", None) or topic_part
    comment_to_msg_id = getattr(d, "comment_to_msg_id", None)
    obtain_comment = getattr(CommonCode, "obtain_comment_to_id", None)
    if callable(obtain_comment):
        try:
            comment_to_msg_id = obtain_comment(d) or comment_to_msg_id
        except Exception:
            comment_to_msg_id = getattr(d, "comment_to_msg_id", comment_to_msg_id)

    target = SendTarget(
        raw_dest=str(raw_dest or ""),
        channel_key=str(channel_key or ""),
        channel_entity=getattr(d, "channel_entity", None),
        user_topic_id=user_topic_id,
    )
    try:
        target.comment_to_msg_id = comment_to_msg_id
    except Exception:
        return target
    return target


async def _check_comment_target(client, target):
    """Validate and resolve the comment target for a normalized destination.

    The validation calls are confirmed; the returned numeric comment id is an
    inferred caller-friendly policy.
    """

    checker = getattr(CommonCode, "check_comment_enable", None)
    if callable(checker):
        try:
            enabled = checker(getattr(target, "channel_key", None))
            if asyncio.iscoroutine(enabled):
                enabled = await enabled
            if not enabled:
                return None
        except Exception:
            enabled = True

    channel_key = getattr(target, "channel_key", None)
    try:
        entity = await client.get_entity(channel_key)
    except Exception:
        entity = channel_key
    convert_dest = getattr(DTopClass, "convertDest", None)
    if callable(convert_dest):
        try:
            converted = convert_dest(entity)
            if asyncio.iscoroutine(converted):
                converted = await converted
            entity = converted or entity
        except Exception:
            entity = entity

    comment_to_msg_id = getattr(target, "comment_to_msg_id", None)
    if comment_to_msg_id is None:
        return None
    try:
        link = utils.convertMessageLinkIfNeed(channel_key, int(comment_to_msg_id))
    except Exception:
        link = str(comment_to_msg_id)
    print(f"正在向 {link} 发布评论区...")
    return int(comment_to_msg_id)


async def _resolve_dest_topic_id(
    auto,
    client,
    target,
    dest_log_type,
    src_topic_id,
):
    """Return the explicit destination topic id or ask TopicUtils for one."""

    user_topic_id = getattr(target, "user_topic_id", None)
    if user_topic_id:
        print(f"检测到用户指定了目标群组的话题ID: {user_topic_id}")
        print(
            f"{dest_log_type or ''} 当前资源会搬运到：群组 "
            f"{getattr(target, 'channel_key', '')} 的话题ID {user_topic_id} 中"
        )
        return int(user_topic_id)

    fetcher = getattr(TopicUtils, "fetch_dest_topic_id", None)
    if not callable(fetcher):
        return 0
    dest_topic_id = await fetcher(
        auto,
        client,
        getattr(target, "raw_dest", None),
    )
    if dest_topic_id:
        print(
            f"{dest_log_type or ''} 当前资源会搬运到："
            f"{getattr(target, 'channel_key', '')} 的话题ID {dest_topic_id} 中"
        )
    return int(dest_topic_id or 0)


async def _do_send_file(
    client,
    target,
    dest_topic_id,
    tart_text,
    for_mat,
    is_video_or_photo,
    album,
):
    """Send one file/album using the confirmed Telethon ``send_file`` shape."""

    caption = tart_text
    kwargs = {
        "caption": caption,
        "parse_mode": for_mat,
    }
    comment_to = getattr(target, "comment_to_msg_id", None)
    if comment_to is not None:
        kwargs["comment_to"] = comment_to
    if dest_topic_id:
        kwargs["reply_to"] = int(dest_topic_id)

    file_arg = album if album else getattr(target, "file", None)
    channel_entity = getattr(target, "channel_entity", None) or getattr(
        target,
        "channel_key",
        None,
    )
    if is_video_or_photo:
        kwargs.update(
            {
                "file": file_arg,
                "album": album or None,
                "video_note": False,
                "supports_streaming": True,
            }
        )
        prefix = "send_file/video_or_photo"
    else:
        kwargs.update(
            {
                "file": file_arg,
                "force_document": not bool(is_video_or_photo),
            }
        )
        prefix = "send_file/document"

    async def send_call():
        return await client.send_file(channel_entity, **kwargs)

    return await FloodGuard.with_flood_retry(
        send_call,
        prefix=prefix,
    )


def file_part_missing_n(exc):
    """Extract the missing part index from a Telethon file-part exception."""

    if isinstance(exc, FilePart0MissingError):
        return 0
    raw = getattr(exc, "which", None)
    if raw is None:
        args = getattr(exc, "args", ()) or ()
        raw = args[0] if args else None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def select_part_contexts_for_n(part_contexts, n):
    """Return upload contexts that contain the missing part index ``n``."""

    result = []
    try:
        target_n = int(n)
    except (TypeError, ValueError):
        return result
    for ctx in part_contexts or ():
        parts = getattr(ctx, "parts", None) or ()
        for part in parts:
            if isinstance(part, int):
                index = part
            else:
                index = getattr(part, "index", None)
                if index is None and isinstance(part, dict):
                    index = part.get("index", part.get("n"))
            try:
                if int(index) == target_n:
                    result.append(ctx)
                    break
            except (TypeError, ValueError):
                continue
    return result


async def resave_file_part(client, n, ctx):
    """Re-upload one missing file part described by ``ctx``.

    Request selection and file-size checks are confirmed.  Inferred: rate
    limiting is delegated to FloodGuard instead of replaying the old
    ``UpRateLimiter`` wiring byte-for-byte.
    """

    path = getattr(ctx, "path", None)
    parts = getattr(ctx, "parts", None) or ()
    print(f"补存分片 {n} / {len(parts)} role={getattr(ctx, 'role', '')}")
    if not path or not os.path.isfile(path):
        print(
            f"补存分片 {n} file_id={getattr(ctx, 'file_id', None)} "
            f"path={path} fail reason=本地文件不存在"
        )
        return False

    actual_size = os.path.getsize(path)
    recorded_size = int(getattr(ctx, "file_size", 0) or 0)
    if recorded_size and recorded_size != actual_size:
        print(
            f"补存分片 {n} file_size不一致 recorded={recorded_size} "
            f"actual={actual_size}"
        )

    part_size = int(getattr(ctx, "part_size", 0) or 0)
    if part_size <= 0:
        part_size = max(1, actual_size)
    offset = int(n) * part_size
    if offset < 0 or offset >= actual_size:
        print(f"补存分片 {n} offset非法 offset={offset} file_size={actual_size}")
        return False

    with open(path, "rb") as file_obj:
        file_obj.seek(offset)
        data = file_obj.read(min(part_size, actual_size - offset))
    if not data:
        print(f"补存分片 {n} 读盘不足 expect={part_size} actual=0")
        return False

    is_large = bool(getattr(ctx, "is_large", actual_size > 10 * 1024 * 1024))
    file_id = getattr(ctx, "file_id", None)
    total_parts = max(1, (actual_size + part_size - 1) // part_size)

    async def save_call():
        if is_large:
            return await client(
                SaveBigFilePartRequest(
                    file_id=file_id,
                    file_part=int(n),
                    file_total_parts=total_parts,
                    bytes=data,
                )
            )
        return await client(
            SaveFilePartRequest(
                file_id=file_id,
                file_part=int(n),
                bytes=data,
            )
        )

    try:
        await FloodGuard.with_flood_retry(
            save_call,
            prefix="resave_file_part",
        )
    except Exception as exc:
        print(f"补存分片 {n} fail reason={exc!r}")
        return False
    print(f"补存分片 {n} ok")
    return True


async def _send_to_dest_with_retry(
    auto,
    client,
    target,
    dest_log_type,
    album,
    tart_text,
    for_mat,
    is_video_or_photo,
    log_pre_tag,
    src_topic_id,
    part_contexts,
):
    """Publish to a destination, repairing missing file parts when possible.

    Inferred: retry counters and the per-n/total patch ceilings are derived
    from the recovered logs and configuration field names.
    """

    if getattr(Working, "need_stop", False):
        print("手动停止成功！")
        return SendResult()

    dest_topic_id = await _resolve_dest_topic_id(
        auto,
        client,
        target,
        dest_log_type,
        src_topic_id,
    )
    comment_to_id = getattr(target, "comment_to_msg_id", None)
    if callable(getattr(target, "is_comment_mode", None)) and target.is_comment_mode():
        comment_to_id = await _check_comment_target(client, target)

    max_try = int(getattr(YunYinMaoConfig, "MAX_TRY_COUNT", 5) or 5)
    patch_per_n = int(getattr(YunYinMaoConfig, "FILE_PART_PATCH_MAX_PER_N", 3) or 3)
    patch_total_max = int(
        getattr(YunYinMaoConfig, "FILE_PART_PATCH_MAX_TOTAL", 50) or 50
    )
    patch_n_map = defaultdict(int)
    patch_total = 0
    attempt = 0
    normal_failures = []

    while attempt < max_try:
        attempt += 1
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            break
        try:
            send_coro = _do_send_file(
                client,
                target,
                dest_topic_id,
                tart_text,
                for_mat,
                is_video_or_photo,
                album,
            )
            sent = await capture_send(client, send_coro, None, None)
            message_ids = []
            if isinstance(sent, (list, tuple)):
                for message in sent:
                    mid = getattr(message, "id", None)
                    if mid is not None:
                        message_ids.append(int(mid))
            elif sent is not None and getattr(sent, "id", None) is not None:
                message_ids.append(int(sent.id))
            album_size = len(album or ())
            result = SendResult(message_ids=message_ids, album_size=album_size)
            try:
                result.success = bool(message_ids or album_size)
            except Exception:
                result.success = bool(message_ids or album_size)

            try:
                log_publish_success(
                    getattr(target, "channel_key", ""),
                    comment_to_id,
                    sent,
                    album_size,
                )
            except Exception:
                log_publish_success(
                    target=target,
                    comment_to_id=comment_to_id,
                    sent=sent,
                    album_size=album_size,
                )
            return result
        except _FILE_PART_MISSING_ERRORS as exc:
            n = file_part_missing_n(exc)
            if n is None:
                print("补片停止：无法解析缺片下标 n")
                break
            if patch_total >= patch_total_max:
                print(f"补片停止：总次数已{patch_total}")
                break
            if patch_n_map[n] >= patch_per_n:
                print(f"补片停止：该n已{patch_n_map[n]}次")
                break
            contexts = select_part_contexts_for_n(part_contexts, n)
            if not contexts:
                print(f"补片停止：无法找到 n={n} 的分片上下文")
                break
            print(
                f"缺片 n={n}，准备补存（该n {patch_n_map[n]}/{patch_per_n}，"
                f"总补片 {patch_total}/{patch_total_max}，候选 {len(contexts)} 个）"
            )
            patched = False
            for ctx in contexts:
                if await resave_file_part(client, n, ctx):
                    patched = True
            if not patched:
                break
            patch_n_map[n] += 1
            patch_total += 1
            print(f"缺片已补存，重新发布（n={n}，该n {patch_n_map[n]}）")
            attempt -= 1
        except Exception as exc:
            text = str(exc)
            if "Failed to parse message" in text:
                print("消息解析失败（Telethon 认为该组消息无效），跳过本组计数...")
                result = SendResult(album_size=len(album or ()))
                try:
                    result.fake_success = True
                except Exception:
                    result.fake_success = True
                return result
            normal_failures.append(exc)
            print(f"{log_pre_tag or ''} 第{attempt}次，发布资源失败: {exc!r}")
            helper = getattr(TracePrinterHelper, "print_trace", None)
            if callable(helper):
                helper()
            sleep_fun = getattr(utils, "sleep_time_fun_no_log", None)
            if callable(sleep_fun) and attempt < max_try:
                await sleep_fun(1, 2)

    if normal_failures:
        raise normal_failures[-1]
    return SendResult()


async def send_message_only(
    auto,
    client,
    destes,
    dest_to_map,
    album,
    tart_text,
    for_mat,
    is_video_or_photo,
    log_pre_tag,
    src_topic_id,
    part_contexts,
    dest_log_type="",
    comment_to_id=None,
    send_success_count=0,
):
    """Send prepared content to each destination without copying comments.

    Inferred: the fourteen argument slots are confirmed by the wrapper, while
    the trailing map/counter names are reconstructed from call-site constants.
    """

    targets = []
    for dest in destes or ():
        target = dest if isinstance(dest, SendTarget) else _resolve_send_target(auto, client, dest)
        if dest_to_map and target in dest_to_map:
            target = dest_to_map[target]
        targets.append(target)

    for target in targets:
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            break
        result = await _send_to_dest_with_retry(
            auto,
            client,
            target,
            dest_log_type,
            album,
            tart_text,
            for_mat,
            is_video_or_photo,
            log_pre_tag,
            src_topic_id,
            part_contexts,
        )
        if getattr(result, "should_count", lambda: False)():
            send_success_count += max(1, len(getattr(result, "message_ids", []) or []))
        sleep_fun = getattr(utils, "sleep_time_fun_no_log", None)
        if callable(sleep_fun):
            await sleep_fun(1, 2)
    return send_success_count


def parseMessageIds(message_ids):
    """Normalize a string/iterable of messages or ids into positive integers."""

    if message_ids is None:
        return []
    if isinstance(message_ids, str):
        values = [item for item in message_ids.replace(";", ",").split(",")]
    else:
        try:
            values = list(message_ids)
        except TypeError:
            values = [message_ids]
    result = []
    for item in values:
        value = getattr(item, "id", item)
        try:
            number = int(value)
        except (TypeError, ValueError):
            continue
        if number > 0:
            result.append(number)
    return result


def grouped_message_ref_from(msg):
    """Return a stable ``GroupedMessageRef`` or ``None`` for invalid ids."""

    try:
        message_id = int(getattr(msg, "id", msg))
    except (TypeError, ValueError):
        return None
    grouped_id = getattr(msg, "grouped_id", None)
    try:
        grouped_id = int(grouped_id) if grouped_id is not None else None
    except (TypeError, ValueError):
        grouped_id = None
    return GroupedMessageRef(message_id=message_id, grouped_id=grouped_id)


def album_anchor_from_messages(messages):
    """Choose the album anchor (highest id) from a message sequence."""

    refs = [grouped_message_ref_from(msg) for msg in _as_message_list(messages)]
    refs = [ref for ref in refs if ref is not None]
    if not refs:
        return None
    anchor = max(refs, key=lambda ref: ref.message_id)
    peer = getattr(messages[0], "peer_id", None) if isinstance(messages, (list, tuple)) and messages else None
    if peer is None:
        peer = getattr(messages, "peer_id", None)
    return AlbumAnchor(
        message_id=anchor.message_id,
        grouped_id=anchor.grouped_id,
        peer=peer,
    )


def album_id_window(anchor_id, radius=ALBUM_ID_RADIUS):
    """Return a bounded numeric window around an album anchor id."""

    center = int(anchor_id)
    span = max(1, int(radius))
    return range(max(1, center - span), center + span + 1)


def message_ids_of_same_group(messages):
    """Return sorted ids that share the first message's grouped id."""

    message_list = _as_message_list(messages)
    if not message_list:
        return []
    grouped_id = getattr(message_list[0], "grouped_id", None)
    if grouped_id is None:
        return sorted(
            int(getattr(msg, "id"))
            for msg in message_list
            if getattr(msg, "id", None) is not None
        )
    return sorted(
        int(getattr(msg, "id"))
        for msg in message_list
        if getattr(msg, "grouped_id", None) == grouped_id and getattr(msg, "id", None) is not None
    )


def _as_message_list(messages):
    """Normalize a single message or a message sequence to a list."""

    if messages is None:
        return []
    if isinstance(messages, (list, tuple)):
        return [message for message in messages if message is not None]
    return [messages]


async def _retry_until_present(load, label):
    """Retry an async/sync loader until it returns a truthy value."""

    while True:
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            return None
        try:
            result = load()
            if asyncio.iscoroutine(result):
                result = await result
            if result:
                return result
            print(f"{label} 未拿到有效结果，准备重试...")
        except Exception as exc:
            print(f"{label} 失败: {exc!r}，准备重试...")
            helper = getattr(TracePrinterHelper, "print_trace", None)
            if callable(helper):
                helper()
        sleep_fun = getattr(utils, "sleep_time_fun_no_log", None)
        if callable(sleep_fun):
            await sleep_fun(_ALBUM_RETRY_SLEEP_MIN, _ALBUM_RETRY_SLEEP_MAX)


async def _load_complete_group_ids(client, anchor):
    """Load all message ids belonging to an album/group anchor."""

    if anchor is None or getattr(anchor, "grouped_id", None) is None:
        return []
    ids = list(album_id_window(anchor.message_id))

    async def _load():
        fetched = await client.get_messages(anchor.peer, ids=ids)
        group = [
            int(getattr(message, "id"))
            for message in (fetched or ())
            if getattr(message, "grouped_id", None) == anchor.grouped_id
            and getattr(message, "id", None) is not None
        ]
        return sorted(group)

    label = f"按 groupId={anchor.grouped_id} 拉取完整媒体组"
    return await _retry_until_present(_load, label) or []


def _positive_msg_ids(msg_ids):
    """Normalize ids to sorted unique positive integers."""

    result = set()
    for item in msg_ids or ():
        value = getattr(item, "id", item)
        try:
            number = int(value)
        except (TypeError, ValueError):
            continue
        if number > 0:
            result.add(number)
    return sorted(result)


async def _album_anchor_from_msg_ids(client, db_channel, anchor_id):
    """Load messages around ``anchor_id`` and build an ``AlbumAnchor``."""

    try:
        anchor_id = int(anchor_id)
    except (TypeError, ValueError):
        return None
    channel_peer = db_channel
    convert_dest = getattr(DTopClass, "convertDest", None)
    if callable(convert_dest):
        try:
            converted = convert_dest(db_channel)
            if asyncio.iscoroutine(converted):
                converted = await converted
            channel_peer = converted or db_channel
        except Exception:
            channel_peer = db_channel

    last_error = None
    for _ in range(3):
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            return None
        try:
            ids = list(album_id_window(anchor_id))
            fetched = await FloodGuard.with_flood_retry(
                lambda: client.get_messages(channel_peer, ids=ids),
                prefix="cm_code/complete_album/anchor_message",
            )
            messages = _as_message_list(fetched)
            if messages:
                return album_anchor_from_messages(messages)
            print(f"按消息 {anchor_id} 读取媒体组失败: 结果为空，准备重试...")
        except Exception as exc:
            last_error = exc
            print(f"按消息 {anchor_id} 读取媒体组失败: {exc!r}，准备重试...")
            helper = getattr(TracePrinterHelper, "print_trace", None)
            if callable(helper):
                helper()
        sleep_fun = getattr(utils, "sleep_time_fun_no_log", None)
        if callable(sleep_fun):
            await sleep_fun(_ALBUM_RETRY_SLEEP_MIN, _ALBUM_RETRY_SLEEP_MAX)
    if last_error is not None:
        return None
    return None


async def resolve_complete_album_target(client, db_channel, messages):
    """Resolve the full album id set for a partial message result."""

    msg_ids = _positive_msg_ids(messages)
    if not msg_ids:
        return CompleteAlbumTarget([])
    anchor = await _album_anchor_from_msg_ids(client, db_channel, msg_ids[0])
    if anchor is None:
        return CompleteAlbumTarget(msg_ids)
    complete_ids = await _load_complete_group_ids(client, anchor)
    return CompleteAlbumTarget(complete_ids or msg_ids)


async def gen_dest_topic_id(
    auto,
    client,
    dest_channel,
    messages,
    params_topic_id=None,
    log_pre="",
):
    """Resolve a destination topic id from parameters or source messages.

    Inferred wrapper composition; the topic-id parser and resolution calls are
    confirmed by the embedded constants.
    """

    if params_topic_id:
        print(f"{log_pre or ''} 当前资源会搬运到：{dest_channel} 的话题ID {params_topic_id} 中")
        return int(params_topic_id)

    source_part, _ = utils.parse_source_parts(
        auto.getSource() if callable(getattr(auto, "getSource", None)) else getattr(auto, "source", "")
    )
    user_topic_id = 0
    message_list = _as_message_list(messages)
    if message_list:
        user_topic_id = TopicUtils.parse_msg_topic_id(message_list[0], 0)
    target = SendTarget(
        raw_dest=str(dest_channel or ""),
        channel_key=utils.convertPrivateIdIfNeed(dest_channel),
        channel_entity=dest_channel,
        user_topic_id=user_topic_id,
    )
    try:
        target.comment_to_msg_id = getattr(target, "comment_to_msg_id", None)
    except Exception:
        target.comment_to_msg_id = None
    dest_topic_id = await _resolve_dest_topic_id(
        auto,
        client,
        target,
        log_pre,
        0,
    )
    return int(dest_topic_id or 0)


def safeFetchFirstMessage(messages):
    """Return the first message from a message/list-like object."""

    if messages is None:
        return None
    first = getattr(messages, "first", None)
    if first is not None:
        return first
    if isinstance(messages, (list, tuple)):
        return messages[0] if messages else None
    try:
        return next(iter(messages), None)
    except TypeError:
        return messages


async def water_only_if_need(
    auto,
    client,
    album,
    argsWrapper=None,
    log_pre_tag="",
):
    """Apply configured image/video watermarks to prepared media.

    Inferred orchestration: the embedded constants confirm separate private
    and global picture/video watermarks, duration checks and ``only_down_load``
    gating.  The exact legacy helper signatures are not fully recoverable.
    """

    files = []
    for item in album or ():
        path = getattr(item, "path", None)
        if path:
            files.append(path)
        elif isinstance(item, str):
            files.append(item)
    if log_pre_tag:
        print(f"{log_pre_tag} {len(files)} 个媒体文件，正在转换路径...")

    pic_water = getattr(NewConfig, "privatePicWater", None) or getattr(
        YunYinMaoConfig,
        "privatePicWater",
        None,
    )
    global_pic_water = getattr(NewConfig, "globalPicWater", None)
    private_video_water = getattr(NewConfig, "privateVideoWater", None)
    global_video_water = getattr(NewConfig, "globalVideoWater", None)

    for path in files:
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            break
        suffix = os.path.splitext(path)[1].lower()
        if suffix in (".jpg", ".jpeg", ".png"):
            water = pic_water or global_pic_water
            if not water:
                continue
            print(
                "全局水印：正在给图片添加水印..."
                if global_pic_water and not pic_water
                else "私有水印：正在给图片添加水印..."
            )
            try:
                result = waterUtils.auto_add_water(
                    path,
                    water,
                    topArgs=getattr(argsWrapper, "topArgs", None),
                )
                if asyncio.iscoroutine(result):
                    await result
            except Exception:
                result = waterUtils.auto_add_water(path, water)
                if asyncio.iscoroutine(result):
                    await result
        else:
            water = private_video_water or global_video_water
            if not water:
                continue
            duration = 0
            probe = getattr(AccelUtils, "probe_video_meta_wrapper", None)
            if callable(probe):
                try:
                    meta = probe(path)
                    if asyncio.iscoroutine(meta):
                        meta = await meta
                    duration = getattr(meta, "duration", 0) or 0
                except Exception:
                    duration = 0
            try:
                result = waterUtils.auto_add_water(
                    path,
                    water,
                    duration=duration,
                    topArgs=getattr(argsWrapper, "topArgs", None),
                )
                if asyncio.iscoroutine(result):
                    await result
            except Exception:
                result = waterUtils.auto_add_water(path, water)
                if asyncio.iscoroutine(result):
                    await result
    return album


def rebind_path_message_map(path_message_map, new_map):
    """Re-key ``path_message_map`` after files have been rewritten (inferred)."""

    old_map = path_message_map or {}
    new_paths = new_map or {}
    if len(old_map) != len(new_paths):
        print(
            f"pathMessageMap 无法按序换 key：模糊前后条数 {len(old_map)} vs {len(new_paths)}"
        )
        return old_map
    result = {}
    for (old_path, message), (_, new_path) in zip(old_map.items(), new_paths.items()):
        result[new_path] = message
    return result


def blur_files_and_rebind_messages(album, path_message_map, radius=8):
    """Blur local pictures and rebind the path/message map."""

    old_files, new_files = gen_blur_pic(album, path_message_map, radius)
    return rebind_path_message_map(
        path_message_map,
        dict(zip(old_files, new_files)),
    )


def gen_blur_pic(group_files, path_message_map, radius):
    """Generate blurred copies and return the old/new file lists."""

    old_files = []
    new_files = []
    for group_file in group_files or ():
        path = getattr(group_file, "path", None) or group_file
        if not isinstance(path, str) or not path:
            continue
        extension = os.path.splitext(path)[1].lower()
        if extension not in YunYinMaoConfig.PIC_MEDIA_FILE_LIST:
            continue
        m_dir = os.path.dirname(path)
        old_name = os.path.basename(path)
        blur_name = "_blur.".join(old_name.split("."))
        output_file = os.path.join(m_dir, blur_name)
        if os.path.exists(output_file):
            print("模糊图片是否存在：" + output_file)
        else:
            try:
                result = PicBlurUtils.apply_gaussian_blur(
                    path,
                    output_file,
                    radius,
                )
                if asyncio.iscoroutine(result):
                    result = True
                if not result:
                    continue
            except Exception:
                if not os.path.exists(output_file):
                    continue
            try:
                utils.safe_del_file(path)
            except Exception:
                pass
        old_files.append(path)
        new_files.append(output_file)
    return old_files, new_files


async def gen_yulan_if_need(
    origin_group_file,
    yuLanModeBean,
    force_pic_preview,
):
    """Build the preview upload list for the configured preview mode.

    ``yuLanModeBean.resType`` is queried with membership tests; the
    ``YU_LAN_RES_TYPE_VIDEO`` / ``YU_LAN_RES_TYPE_PIC`` checks and the
    returned path list are confirmed by the Nuitka constants and the
    decompiled control flow.
    """

    print(f"{len(origin_group_file)} 个媒体文件，正在转换路径...")
    photo_or_video_yulan_path_list_for_upload = []
    for input_file in origin_group_file:
        if Working.need_stop:
            print("手动停止成功！")
            break
        exist = os.path.exists(input_file)
        print(f"{input_file} 是否存在：{exist}")
        _, extension = os.path.splitext(input_file)
        lower_extension = extension.lower()
        if lower_extension in YunYinMaoConfig.VIDEO_MEDIA_FILE_LIST:
            if force_pic_preview:
                f = AccelUtils.extract_random_cover_image(input_file)
                if f is not None and os.path.exists(f):
                    print(
                        "(强制使用图片做预览，忽略预览资源条件) "
                        "成功根据本地视频资源，生成一个缩略图作为视频替换！"
                    )
                    photo_or_video_yulan_path_list_for_upload.append(f)
                    continue
            if YU_LAN_RES_TYPE_VIDEO in yuLanModeBean.resType:
                await gen_preview_video(
                    input_file,
                    photo_or_video_yulan_path_list_for_upload,
                    yuLanModeBean,
                )
            elif YU_LAN_RES_TYPE_PIC in yuLanModeBean.resType:
                f = AccelUtils.extract_random_cover_image(input_file)
                if f is not None and os.path.exists(f):
                    photo_or_video_yulan_path_list_for_upload.append(f)
        elif lower_extension in YunYinMaoConfig.PIC_MEDIA_FILE_LIST:
            if force_pic_preview:
                print("(强制使用图片做预览，忽略预览资源条件) 直接使用图片资源！")
                photo_or_video_yulan_path_list_for_upload.append(input_file)
            elif YU_LAN_RES_TYPE_PIC in yuLanModeBean.resType:
                photo_or_video_yulan_path_list_for_upload.append(input_file)
    return photo_or_video_yulan_path_list_for_upload


async def gen_preview_video(
    input_file,
    photo_or_video_yulan_path_list_for_upload,
    yuLanModeBean,
):
    """Generate one preview artifact and append its path to the upload list.

    The signature, ``_preview.`` infix, ``NewConfig`` mode switch and
    ``PreviewReason.STOPPED_BY_USER`` handling come from the Nuitka constants
    and the decompiled control flow.
    """

    if Working.need_stop:
        print("手动停止成功！")
        return None
    m_dir = os.path.dirname(input_file)
    old_name = os.path.basename(input_file)
    yulan_name = "_preview.".join(old_name.split("."))
    output_file = os.path.join(m_dir, yulan_name)
    mode = yuLanModeBean.mode
    if NewConfig.FLOW_YU_LAN_MODEL_PRESENT == mode:
        print("按照百分比模式生成预览视频")
        preview_result = GenYuLanVideoWrapper.generate_present_preview(
            input_file,
            output_file,
            yuLanModeBean.presentMode.present,
        )
    else:
        print("按照自定义时长方式生成预览视频")
        preview_result = GenYuLanVideoWrapper.generate_customer_preview(
            input_file,
            output_file,
            yuLanModeBean.durationMode.duration_min_second,
            yuLanModeBean.durationMode.duration_max_second,
        )
    if (
        Working.need_stop
        or preview_result.reason == PreviewReason.STOPPED_BY_USER
    ):
        print("手动停止成功！")
        utils.safe_del_file(output_file)
        return None
    exist = os.path.exists(output_file)
    print(f"预览视频是否存在：{exist}")
    if exist:
        photo_or_video_yulan_path_list_for_upload.append(output_file)
    elif preview_result.ok:
        photo_or_video_yulan_path_list_for_upload.append(input_file)
    else:
        print(
            "生成预览失败，原视频不能发布到预览频道！原因："
            f"{preview_result.reason} 详情：{preview_result.detail}"
        )
    return None


def elide_path_middle(text, max_len=30):
    """Elide the middle of a path while preserving both ends."""

    value = str(text or "")
    max_len = int(max_len)
    if max_len <= 3 or len(value) <= max_len:
        return value[:max_len] if max_len > 0 else ""
    keep = max_len - 3
    head = (keep + 1) // 2
    tail = keep - head
    return value[:head] + "..." + (value[-tail:] if tail else "")


def r_instance_id():
    """Return the stable per-instance id derived from the data/executable path."""

    is_multi = bool(getattr(YunYinMaoConfig, "is_support_multi", False))
    if is_multi:
        get_dir = getattr(DirManager, "get_local_data_dir", None)
        if callable(get_dir):
            base = get_dir()
        else:
            base = getattr(DirManager, "get_local_data_dir", "")
    else:
        base = getattr(DirManager, "executable", "") or getattr(
            YunYinMaoConfig,
            "executable",
            "",
        )
    raw = f"SingleYunYinMao_{base}"
    digest = hashlib.md5(raw.encode("utf-8")).hexdigest()
    return digest.replace("'", "").replace('"', "").replace("*", "").strip()


def processAiContent(content):
    """Strip quote/emphasis markers that AI output commonly adds."""

    return (
        str(content or "")
        .replace("'", "")
        .replace('"', "")
        .replace("*", "")
        .strip()
    )


def _ten_grid_cover_filename(stem, n):
    """Build the deterministic ten-grid cover filename."""

    return f"{stem}_complete_{int(n)}.jpg"


def _next_ten_grid_cover_path(video_path, start_n):
    """Reserve the next available ten-grid cover path.

    Returns ``(path, sequence_number)`` or ``(None, start_n)`` when numbering is
    exhausted.
    """

    video_path = os.fspath(video_path)
    directory = os.path.dirname(os.path.abspath(video_path)) or os.getcwd()
    stem = os.path.splitext(os.path.basename(video_path))[0]
    start = max(0, int(start_n or 0))
    for n in range(start, _TEN_GRID_NAME_MAX_N):
        path = os.path.join(directory, _ten_grid_cover_filename(stem, n))
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return path, n
        except FileExistsError:
            continue
        except OSError:
            continue
    print(f"宫格封面命名跳号耗尽: {stem}")
    return None, start


def _ten_grid_cover_ok(
    exclude_times,
    exclude_hashes,
    slot_index,
    slot_count,
    meta,
    allow_moviepy,
):
    """Validate a generated cover against slot/time/hash exclusions."""

    def _is_readable_image(path):
        if not path or not os.path.isfile(path):
            return False
        try:
            with open(path, "rb") as file_obj:
                header = file_obj.read(16)
        except OSError:
            return False
        return header.startswith(
            (
                b"\xff\xd8\xff",
                b"\x89PNG\r\n\x1a\n",
                b"GIF87a",
                b"GIF89a",
                b"RIFF",
            )
        )

    if slot_count and not (0 <= int(slot_index) < int(slot_count)):
        return False
    if isinstance(meta, dict):
        path = meta.get("path") or meta.get("cover") or meta.get("source")
    else:
        path = getattr(meta, "path", None) or meta
    if not path:
        return False
    path = os.fspath(path)
    if _is_readable_image(path):
        try:
            with open(path, "rb") as file_obj:
                digest = hashlib.md5(file_obj.read(65536)).hexdigest()
        except OSError:
            return False
        return digest not in (exclude_hashes or set())

    if not allow_moviepy:
        return False
    extractor = getattr(AccelUtils, "extract_random_cover_image", None)
    if not callable(extractor):
        return False
    try:
        result = extractor(path)
        if asyncio.iscoroutine(result):
            # This validation function is synchronous in the recovered module.
            return False
        return bool(result)
    except Exception:
        return False


def completeTenGrid(files, number):
    """Fill the ten-grid cover list up to ``number`` using local media.

    Inferred orchestration; cover naming, deterministic reservation and
    readability checks come from the confirmed nested helper constants.
    """

    result = [os.fspath(item) for item in (files or ())]
    target_number = min(max(0, int(number or 0)), _TEN_GRID_MAX)
    print(
        f"completeTenGrid called files size: {len(result)}，number: {target_number}"
    )
    if len(result) >= target_number:
        return result

    local_is_video = getattr(CommonCode, "localFileIsVideo", None)
    videos = []
    for path in result:
        if callable(local_is_video):
            try:
                if local_is_video(path):
                    videos.append(path)
            except Exception:
                if os.path.splitext(path)[1].lower() in (".mp4", ".mov", ".mkv", ".avi"):
                    videos.append(path)
        elif os.path.splitext(path)[1].lower() in (".mp4", ".mov", ".mkv", ".avi"):
            videos.append(path)

    print(
        f"宫格补齐：现有 {len(result)} 个，目标 {target_number}，"
        f"需补 {max(0, target_number - len(result))} 张，视频 {len(videos)} 个"
    )
    if not videos:
        return result

    used_times = set()
    used_hashes = set()
    fail_count = 0
    for slot_index in range(len(result), target_number):
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            break
        added = False
        for video in videos:
            cover, seq_n = _next_ten_grid_cover_path(video, slot_index + 1)
            if not cover:
                continue
            extractor = getattr(AccelUtils, "extract_random_cover_image", None)
            if callable(extractor):
                try:
                    extracted = extractor(video, output_file=cover)
                    if asyncio.iscoroutine(extracted):
                        # The recovered entry is sync; reject unresolved async.
                        extracted = None
                    if extracted:
                        cover = os.fspath(extracted)
                except TypeError:
                    try:
                        extracted = extractor(video)
                        if extracted and not asyncio.iscoroutine(extracted):
                            cover = os.fspath(extracted)
                    except Exception:
                        extracted = None
                except Exception:
                    extracted = None
            meta = {"path": cover, "source": video, "sequence": seq_n}
            if _ten_grid_cover_ok(
                used_times,
                used_hashes,
                slot_index,
                target_number,
                meta,
                True,
            ):
                result.append(cover)
                added = True
                used_times.add(time.time())
                try:
                    with open(cover, "rb") as file_obj:
                        used_hashes.add(hashlib.md5(file_obj.read(65536)).hexdigest())
                except OSError:
                    used_hashes.add("")
                break
        if not added:
            fail_count += 1
            if fail_count >= _TEN_GRID_VIDEO_FAIL_LIMIT:
                break

    print(f"宫格补齐完成：新增 {max(0, len(result) - len(files or ()))} 张封面")
    return result
