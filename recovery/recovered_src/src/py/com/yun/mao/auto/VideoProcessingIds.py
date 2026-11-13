# Recovered module: src.py.com.yun.mao.auto.VideoProcessingIds
# Telethon helper that follows "video processing" temporary message ids until
# the server publishes the real channel-post ids.
#
# Function names, signatures, annotations, update classes and log text are
# confirmed by the Nuitka init/function metadata.  The class-level patching in
# ``Watch`` is reconstructed from the coroutine branches; those mechanics are
# marked inferred where Telethon owns the exact call site.
from __future__ import annotations

import asyncio
import time
from typing import Dict, Iterable, List, Optional, Set, Tuple

from telethon import events
from telethon.tl import types

from src.py.com.yun.mao.cd import Working
from src.py.com.yun.mao.util import SuspendFrozenTag


_POST_UPDATES = (types.UpdateNewChannelMessage, types.UpdateNewMessage)
_LISTEN_UPDATES = (types.UpdateDeleteScheduledMessages,)

_POSTED_CAP = 80
_WAIT_SEC = 600.0
_POLL_SEC = 2.0


def _as_messages(update_or_updates) -> list:
    if update_or_updates is None:
        return []
    if isinstance(update_or_updates, (list, tuple)):
        candidates = update_or_updates
    else:
        messages = getattr(update_or_updates, "messages", None)
        if messages is not None:
            candidates = messages
        else:
            message = getattr(update_or_updates, "message", None)
            if message is not None:
                candidates = (message,)
            elif getattr(update_or_updates, "id", None) is not None:
                candidates = (update_or_updates,)
            else:
                candidates = ()
    return [message for message in candidates if message is not None]


def _positive_int(value) -> Optional[int]:
    try:
        result = int(value)
    except (TypeError, ValueError):
        return None
    return result if result > 0 else None


def _peer_key(obj) -> Optional[Tuple[str, int]]:
    peer = getattr(obj, "peer_id", None) or getattr(obj, "peer", None)
    if peer is None:
        message = getattr(obj, "message", None)
        if message is not None:
            peer = getattr(message, "peer_id", None) or getattr(message, "peer", None)
    if peer is None:
        return None
    for name in ("channel_id", "chat_id", "user_id"):
        value = _positive_int(getattr(peer, name, None))
        if value is not None:
            return name[:-3], value
    raw = _positive_int(peer)
    if raw is not None:
        return peer.__class__.__name__.lower(), raw
    return None


def _media_key(msg) -> Optional[Tuple[str, int]]:
    media = getattr(msg, "media", None)
    if media is None:
        return None
    for name in ("photo", "document"):
        item = getattr(media, name, None)
        value = _positive_int(getattr(item, "id", None))
        if value is not None:
            return name, value
    return None


def _walk_updates(update_or_updates):
    if update_or_updates is None:
        return
    if isinstance(update_or_updates, types.UpdateShort):
        yield update_or_updates.update
        return
    updates = getattr(update_or_updates, "updates", None)
    other_updates = getattr(update_or_updates, "other_updates", None)
    if updates is not None or other_updates is not None:
        for update in updates or []:
            yield update
        for update in other_updates or []:
            yield update
        return
    yield update_or_updates


def pending_ids(sent) -> List[int]:
    result: List[int] = []
    for msg in _as_messages(sent):
        if not getattr(msg, "video_processing_pending", False):
            continue
        mid = _positive_int(getattr(msg, "id", None))
        if mid is not None:
            result.append(mid)
    return result


def first_still_pending(sent) -> bool:
    for msg in _as_messages(sent):
        if getattr(msg, "video_processing_pending", False):
            return True
    return False


def _safe_id_map(pairs: Iterable, pending: Set[int]) -> Dict[int, int]:
    mapping: Dict[int, int] = {}
    for pair in pairs or ():
        try:
            sid_raw, rid_raw = pair
        except (TypeError, ValueError):
            continue
        sid = _positive_int(sid_raw)
        rid = _positive_int(rid_raw)
        if sid is None or rid is None:
            continue
        if pending and sid not in pending:
            continue
        mapping[sid] = rid
    return mapping


def _delete_scheduled_hint(update_or_updates) -> Optional[str]:
    hint: Optional[str] = None
    for update in _walk_updates(update_or_updates):
        if not isinstance(update, types.UpdateDeleteScheduledMessages):
            continue
        queued = getattr(update, "messages", None) or []
        sent = getattr(update, "sent_messages", None) or []
        if queued and sent and len(queued) != len(sent):
            hint = (
                "收到 UpdateDeleteScheduledMessages 但长度不一致 "
                f"queued={len(queued)} sent={len(sent)}，忽略按位映射"
            )
        elif sent:
            hint = f"收到官方 sent_messages 映射 {len(sent)} 条"
        else:
            hint = (
                "收到 UpdateDeleteScheduledMessages "
                f"queued={len(queued)} sent={len(sent)}"
            )
    return hint


def scheduled_to_real_id_map(update_or_pairs, pending: Set[int]) -> Dict[int, int]:
    mapping: Dict[int, int] = {}
    updates = getattr(update_or_pairs, "updates", None)
    is_update = updates is not None or isinstance(update_or_pairs, types.UpdateShort)
    if not is_update:
        return _safe_id_map(update_or_pairs, pending)

    for update in _walk_updates(update_or_pairs):
        if not isinstance(update, types.UpdateDeleteScheduledMessages):
            continue
        queued = getattr(update, "messages", None) or []
        sent = getattr(update, "sent_messages", None) or []
        if not sent:
            continue
        if queued and len(queued) == len(sent):
            mapping.update(_safe_id_map(zip(queued, sent), pending))
        elif not pending:
            mapping.update(_safe_id_map(zip(queued, sent), set()))
    return mapping


def collect_posted_messages(update_or_updates) -> List:
    posted: List = []
    seen: Set[Tuple[Optional[Tuple[str, int]], int]] = set()

    def add(message) -> None:
        if message is None:
            return
        mid = _positive_int(getattr(message, "id", None))
        if mid is None:
            return
        key = (_peer_key(message), mid)
        if key in seen:
            return
        seen.add(key)
        posted.append(message)

    for update in _walk_updates(update_or_updates):
        if isinstance(update, _POST_UPDATES):
            add(getattr(update, "message", None))
        if isinstance(update, types.UpdateDeleteScheduledMessages):
            for message in getattr(update, "sent_messages", None) or []:
                add(message)
        for message in _as_messages(update):
            add(message)

    while len(posted) > _POSTED_CAP:
        posted.pop(0)
    return posted


def apply_id_map(sent, id_map: Dict[int, int]) -> List[int]:
    if not id_map:
        return extract_ids(sent)
    for msg in _as_messages(sent):
        mid = _positive_int(getattr(msg, "id", None))
        if mid is None or mid not in id_map:
            continue
        real = id_map[mid]
        try:
            setattr(msg, "id", real)
        except Exception:
            continue
        try:
            setattr(msg, "video_processing_pending", False)
        except Exception:
            continue
        print(f"视频处理队列ID已替换: {mid} → {real}")
    return extract_ids(sent)


def map_first_to_posted(sent, posted) -> Dict[int, int]:
    pending = [
        msg
        for msg in _as_messages(sent)
        if getattr(msg, "video_processing_pending", False)
    ]
    posted_messages = list(posted or ())
    mapping: Dict[int, int] = {}

    for pending_msg in pending:
        pending_id = _positive_int(getattr(pending_msg, "id", None))
        if pending_id is None:
            continue
        peer_key = _peer_key(pending_msg)
        media_key = _media_key(pending_msg)
        for real_msg in posted_messages:
            real_id = _positive_int(getattr(real_msg, "id", None))
            if real_id is None or real_id in mapping.values():
                continue
            if _peer_key(real_msg) != peer_key:
                continue
            if media_key is not None and _media_key(real_msg) not in (None, media_key):
                continue
            mapping[pending_id] = real_id
            break

    if mapping:
        return mapping

    for pending_msg, real_msg in zip(pending, posted_messages):
        pending_id = _positive_int(getattr(pending_msg, "id", None))
        real_id = _positive_int(getattr(real_msg, "id", None))
        if pending_id is not None and real_id is not None:
            mapping[pending_id] = real_id
    return mapping


def extract_ids(sent) -> List[int]:
    ids: Set[int] = set()
    seen: Set[Tuple[Optional[Tuple[str, int]], int]] = set()
    for msg in _as_messages(sent):
        mid = _positive_int(getattr(msg, "id", None))
        if mid is None:
            continue
        key = (_peer_key(msg), mid)
        if key in seen:
            continue
        seen.add(key)
        ids.add(mid)
    return sorted(ids)


class Watch:
    """Collect raw updates and bridge temporary ids to published ids."""

    def __init__(self, client):
        self._client = client
        self._map: Dict[int, int] = {}
        self._posted: List = []
        self._posted_ids: Set[int] = set()
        self._orig_call = None
        self._raw_event = None
        self._got = asyncio.Event()

    def _remember_posted(self, msg, mid=None) -> None:
        message_id = _positive_int(mid if mid is not None else getattr(msg, "id", None))
        if message_id is None:
            return
        self._posted_ids.add(message_id)
        if msg not in self._posted:
            self._posted.append(msg)
        while len(self._posted) > _POSTED_CAP:
            self._posted.pop(0)
        self._got.set()

    def _ingest(self, update_or_updates) -> None:
        for msg in collect_posted_messages(update_or_updates):
            self._remember_posted(msg)
        pending = set(pending_ids(update_or_updates))
        if not pending:
            pending = set(self._map)
        mapping = scheduled_to_real_id_map(update_or_updates, pending)
        if mapping:
            self._map.update(mapping)
            self._got.set()
        hint = _delete_scheduled_hint(update_or_updates)
        if hint:
            print(hint)

    def _apply_known(self, sent) -> List[int]:
        return apply_id_map(sent, self._map)

    async def _poll_history(self) -> None:
        if self._client is None:
            return
        peers = []
        for msg in self._posted[-20:]:
            peer = getattr(msg, "peer_id", None) or getattr(msg, "peer", None)
            if peer is not None:
                peers.append(peer)
        for peer in peers:
            try:
                messages = await self._client.get_messages(peer, limit=20)
            except Exception as exc:
                print(f"拉取频道最近消息失败: {exc!r}")
                continue
            for message in messages or []:
                self._remember_posted(message)

    async def __aenter__(self):
        async def on_raw(update):
            self._ingest(update)

        self._raw_event = on_raw
        try:
            self._client.add_event_handler(self._raw_event, events.Raw)
        except Exception:
            self._raw_event = None
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._raw_event is not None:
            try:
                self._client.remove_event_handler(self._raw_event, events.Raw)
            except Exception:
                return False
        self._raw_event = None
        return False

    def ids(self) -> List[int]:
        return sorted(set(self._map.values()) | set(self._posted_ids))


async def capture_send(client, send_coro, watch, sent):
    """Await a send coroutine and wait for temporary ids to become real ids."""

    if callable(send_coro) and not asyncio.iscoroutine(send_coro):
        result = send_coro()
        if asyncio.iscoroutine(result):
            result = await result
    else:
        result = await send_coro

    target = sent if sent is not None else result
    if watch is None:
        return result

    watch._ingest(result)
    watch._apply_known(target)
    if not first_still_pending(target):
        return result

    first_ids = pending_ids(target)
    print(
        "发送结果仍在视频处理队列（组内第一条临时ID="
        f"{first_ids[0] if first_ids else None}，整组临时ID={sorted(first_ids)}），"
        f"等待真实帖子ID，最多 {_WAIT_SEC:.0f} 秒..."
    )
    deadline = time.monotonic() + _WAIT_SEC
    last_poll = 0.0
    last_hint = 0.0
    while time.monotonic() < deadline:
        if getattr(Working, "need_stop", False):
            break
        watch._apply_known(target)
        if not first_still_pending(target):
            break
        now = time.monotonic()
        if now - last_poll >= _POLL_SEC:
            last_poll = now
            await watch._poll_history()
        if now - last_hint >= 15:
            last_hint = now
            print(
                "仍在等待组内第一条官方帖子ID映射，临时ID="
                f"{pending_ids(target)}"
            )
        watch._got.clear()
        try:
            await asyncio.wait_for(
                watch._got.wait(),
                timeout=max(0.05, min(1.0, deadline - time.monotonic())),
            )
        except asyncio.TimeoutError:
            continue

    watch._apply_known(target)
    if first_still_pending(target):
        print(
            "未能解析组内第一条真实帖子ID，仍为处理队列ID "
            f"{pending_ids(target)}"
        )
    try:
        SuspendFrozenTag.print_last_log_if_need()
    except Exception:
        return result
    return result
