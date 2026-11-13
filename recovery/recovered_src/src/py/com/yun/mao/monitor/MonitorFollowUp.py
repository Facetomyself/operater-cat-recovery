# Recovered module: src.py.com.yun.mao.monitor.MonitorFollowUp
# Behaviour-level reconstruction from Nuitka constants, code-object
# signatures, and offline Hex-Rays output.  Branches marked "inferred" are
# conservative where the recovered dependency is still a stub.
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Set

from telethon import events, functions
from telethon.errors import ChannelPrivateError, MessageNotModifiedError, UserNotParticipantError
from telethon.tl import types
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipant,
    ChannelParticipantAdmin,
    ChannelParticipantBanned,
    ChannelParticipantCreator,
    ChannelParticipantSelf,
    MessageService,
)
from telethon.utils import get_peer_id

from ..auto import AutoWorkerWrapper
from ..cd import Working
try:
    from ..dclass.DTopClass import convertDest
except ImportError:
    def convertDest(value: Any) -> Any:
        return value
from ..fea import _sq_r_ca
from ..record import PublishIdRecord
from ..util import FloodGuard, TracePrinterHelper
from ..util.CustomerHtmlFormat import entities_to_html
from ..util.need import CommonCode, utils
from ..util.need.AllBeanDef import ParseBean


ALBUM_LOOKBACK = 9


def _flag(obj: Any, name: str, default: bool = False) -> bool:
    value = getattr(obj, name, default)
    if callable(value):
        try:
            value = value()
        except Exception:
            return default
    return bool(value)


def first_id_from_album_messages(event_id: int, messages: Sequence[Any]) -> int:
    """Return the smallest message id in the album containing ``event_id``."""

    values = [msg for msg in (messages or []) if msg is not None]
    try:
        event_id = int(event_id or 0)
    except (TypeError, ValueError):
        event_id = 0
    if not values:
        return event_id
    grouped_id = getattr(values[0], "grouped_id", None)
    same = [
        int(getattr(msg, "id", 0) or 0)
        for msg in values
        if getattr(msg, "grouped_id", None) == grouped_id
        and getattr(msg, "id", None) is not None
    ]
    if not same:
        same = [int(getattr(msg, "id", event_id) or event_id) for msg in values]
    return min(same) if same else event_id


def is_source_channel_mirror(msg: Any, source_peer_id: Optional[int]) -> bool:
    """Detect a forwarded mirror of a source-channel post."""

    fwd = getattr(msg, "fwd_from", None)
    channel_post = getattr(fwd, "channel_post", None) if fwd is not None else None
    from_id = getattr(fwd, "from_id", None) if fwd is not None else None
    if not channel_post or from_id is None or source_peer_id is None:
        return False
    try:
        return int(get_peer_id(from_id)) == int(source_peer_id)
    except Exception:
        return False


def discussion_reply_anchor_id(msg: Any) -> Optional[int]:
    """Resolve the discusssion-group anchor carried by a reply."""

    reply = getattr(msg, "reply_to", None)
    if reply is None:
        return None
    top = getattr(reply, "reply_to_top_id", None)
    rid = getattr(reply, "reply_to_msg_id", None)
    try:
        value = top or rid
        return int(value) if value else None
    except (TypeError, ValueError):
        return None


def channel_post_id_from_anchor(anchor_msg: Any) -> Optional[int]:
    """Extract the source-channel post id embedded in a discussion anchor."""

    fwd = getattr(anchor_msg, "fwd_from", None)
    post = getattr(fwd, "channel_post", None) if fwd is not None else None
    try:
        return int(post) if post else None
    except (TypeError, ValueError):
        return None


def message_html(msg: Any) -> str:
    """Render Telethon message text and entities as Telegram HTML."""

    text = getattr(msg, "message", None)
    if text is None:
        text = getattr(msg, "text", "")
    text = str(text or "")
    entities = getattr(msg, "entities", None)
    if entities:
        try:
            return entities_to_html(text, entities)
        except Exception:
            TracePrinterHelper.print_trace()
    return text


def resolve_event_queue_keys(event: Any, queue_keys: Set[str]) -> List[str]:
    """Map an event chat/user name to the monitor queue keys it owns."""

    queue_keys = set(queue_keys or ())
    chat = getattr(event, "chat", None)
    if chat is None:
        chat = getattr(event, "message", None)
        chat = getattr(chat, "chat", None) if chat is not None else None
    candidates: List[str] = []
    username_obj = getattr(chat, "username", None) if chat is not None else None
    if username_obj:
        username = str(username_obj)
        candidates.append(username if username.startswith("@") else "@" + username)
    chat_id = getattr(chat, "id", None) if chat is not None else None
    if chat_id is not None:
        raw = str(chat_id)
        candidates.append(raw)
        if raw.lstrip("-").isdigit():
            candidates.append(raw if raw.startswith("-100") else "-100" + raw.lstrip("-"))
    usernames = getattr(chat, "usernames", None) if chat is not None else None
    if usernames:
        for item in usernames:
            name = getattr(item, "username", item)
            if name:
                name = str(name)
                candidates.append(name if name.startswith("@") else "@" + name)
    result: List[str] = []
    for candidate in candidates:
        for key in queue_keys:
            if (key == candidate or key.startswith(candidate + "|")) and key not in result:
                result.append(key)
    return result


def source_needs_comment_live(auto: Any) -> bool:
    """A source needs live comment following when BanYun does not copy it."""

    return _flag(auto, "needSendComment", False) and not _flag(auto, "isBanYunType", False)


def source_needs_caption_sync(auto: Any) -> bool:
    """A source caption is mirrored when the source text is preserved."""

    return _flag(auto, "keepSourceText", False) and not _flag(auto, "isBanYunType", False)


def _channel_part_of(auto: Any) -> str:
    """Return the channel/group part of an auto bean source."""

    getter = getattr(auto, "getSource", None)
    source = getter() if callable(getter) else getattr(auto, "source", "")
    channel_part, _ = utils.parse_source_parts(str(source or ""))
    return str(channel_part or "")


def _discussion_chat_keys(disc: Any) -> List[int]:
    """Return all numeric keys that may identify the linked discussion chat."""

    out: List[int] = []
    seen: Set[int] = set()
    raw_id = getattr(disc, "id", None)
    values = [raw_id]
    try:
        values.append(get_peer_id(disc))
    except Exception:
        pass
    for value in values:
        try:
            number = int(value)
        except (TypeError, ValueError):
            continue
        for key in (number, -100 - abs(number) if number >= 0 else number):
            if key not in seen:
                seen.add(key)
                out.append(key)
    return out


def is_broadcast_comment_channel(entity: Any) -> bool:
    """Whether the entity can own a linked discussion group."""

    return bool(
        getattr(entity, "broadcast", False)
        or getattr(entity, "megagroup", False)
        or getattr(entity, "gigagroup", False)
    )


class MonitorFollowUp:
    """Follow source edits and new comments after a monitor task starts."""

    def __init__(self, worker: Any) -> None:
        self.worker = worker
        self.discussion_chat_ids: Set[int] = set()
        self.discussion_to_sources: Dict[int, Set[str]] = {}
        self.source_peer_by_safe: Dict[str, int] = {}
        self.channel_part_by_safe: Dict[str, str] = {}
        self._handlers_registered = False

    async def setup(self) -> None:
        sources = list(getattr(self.worker, "all_source", None) or [])
        if not sources:
            for auto in list(getattr(self.worker, "all_legal_auto_beans", None) or []):
                channel_part = _channel_part_of(auto)
                if channel_part:
                    sources.append(channel_part)
        seen_source: Set[str] = set()
        for safe_source in sources:
            safe_source = str(safe_source or "")
            if not safe_source or safe_source in seen_source:
                continue
            seen_source.add(safe_source)
            await self._prepare_discussions(safe_source)
        registered_parts: Set[str] = set()
        for channel_part in list(self.channel_part_by_safe.values()):
            if channel_part and channel_part not in registered_parts:
                registered_parts.add(channel_part)
                self._register_handlers(channel_part)

    def _autos_for_safe_source(self, safe_source: str) -> List[Any]:
        beans = list(getattr(self.worker, "all_legal_auto_beans", None) or [])
        finder = getattr(CommonCode, "findAutoBeanBySource", None)
        if callable(finder):
            try:
                found = finder(safe_source, beans)
            except TypeError:
                try:
                    found = finder(beans, safe_source)
                except Exception:
                    found = None
            except Exception:
                found = None
            if found:
                return list(found)
        result: List[Any] = []
        for auto in beans:
            channel_part = _channel_part_of(auto)
            source = str(getattr(auto, "getSource", lambda: getattr(auto, "source", ""))() or "")
            if safe_source in (source, channel_part):
                result.append(auto)
                continue
            if str(getattr(auto, "safeSource", "")) == safe_source:
                result.append(auto)
        return result

    async def _prepare_discussions(self, safe_source: str) -> None:
        seen_source: Set[str] = set()
        for auto in self._autos_for_safe_source(safe_source):
            channel_part = _channel_part_of(auto)
            if not channel_part or channel_part in seen_source:
                continue
            seen_source.add(channel_part)
            self.channel_part_by_safe[safe_source] = channel_part
            disc = await self._join_source_discussion(channel_part, safe_source)
            if disc is None:
                continue
            try:
                disc_peer_id = int(get_peer_id(disc))
            except Exception:
                disc_peer_id = int(getattr(disc, "id", 0) or 0)
            if not disc_peer_id:
                continue
            mapped = self.discussion_to_sources.setdefault(disc_peer_id, set())
            mapped.add(safe_source)
            self.discussion_chat_ids.update(_discussion_chat_keys(disc))

    async def _join_source_discussion(self, channel_part: str, safe_source: str) -> Optional[Any]:
        client = getattr(self.worker, "client", None)
        if client is None:
            return None
        try:
            source_entity = await FloodGuard.with_flood_retry(
                lambda: client.get_entity(utils.convertPrivateIdIfNeed(channel_part)),
                prefix="monitor/followup/source_entity",
            )
            try:
                self.source_peer_by_safe[safe_source] = int(get_peer_id(source_entity))
            except Exception:
                self.source_peer_by_safe[safe_source] = int(getattr(source_entity, "id", 0) or 0)
            if not is_broadcast_comment_channel(source_entity):
                print("源 ", channel_part, " 不是广播频道，跳过讨论组监听")
                return None
            full_channel = await FloodGuard.with_flood_retry(
                lambda: client(GetFullChannelRequest(channel=source_entity)),
                prefix="monitor/followup/full_channel",
            )
            full_chat = getattr(full_channel, "full_chat", None)
            linked_id = getattr(full_chat, "linked_chat_id", None)
            if not linked_id:
                print("源 ", channel_part, " 未绑定讨论组，无法监听后续评论")
                return None
            disc = await FloodGuard.with_flood_retry(
                lambda: client.get_entity(types.PeerChannel(int(linked_id))),
                prefix="monitor/followup/disc_entity",
            )
            await self._ensure_joined(disc, channel_part)
            return disc
        except Exception:
            print("解析/加入源讨论组失败 ", channel_part, "：")
            TracePrinterHelper.print_trace()
            return None

    async def _ensure_joined(self, disc: Any, channel_part: str) -> None:
        client = getattr(self.worker, "client", None)
        me = getattr(self.worker, "me", None)
        if client is None:
            return
        participant = None
        try:
            participant = await FloodGuard.with_flood_retry(
                lambda: client(
                    GetParticipantRequest(
                        channel=disc,
                        participant=getattr(me, "id", me),
                    )
                ),
                prefix="monitor/followup/disc_participant",
            )
        except UserNotParticipantError:
            participant = None
        except Exception:
            print("检查讨论组成员失败 ", channel_part, "：")
            TracePrinterHelper.print_trace()
        ok_types = (
            ChannelParticipant,
            ChannelParticipantCreator,
            ChannelParticipantAdmin,
            ChannelParticipantSelf,
            ChannelParticipantBanned,
        )
        joined = participant is not None and isinstance(participant.participant, ok_types)
        if joined:
            return
        print("尝试加入源讨论组（一比一复刻）：", channel_part)
        try:
            await FloodGuard.with_flood_retry(
                lambda: client(functions.channels.JoinChannelRequest(channel=disc)),
                prefix="monitor/followup/join_disc",
            )
            print("加入源讨论组成功：", channel_part)
        except ChannelPrivateError:
            print("源讨论组为私密，无法自动加入：", channel_part)
        except Exception:
            print("加入源讨论组失败：", channel_part, "：")
            TracePrinterHelper.print_trace()

    def _register_handlers(self, channel_part: str) -> None:
        if self._handlers_registered:
            return
        client = getattr(self.worker, "client", None)
        if client is None:
            return
        self._handlers_registered = True

        async def on_source_edited(event: Any) -> None:
            if not getattr(self.worker, "running", False) or _flag(Working, "need_stop", False):
                return
            try:
                msg = getattr(event, "message", None)
                if isinstance(msg, MessageService) or msg is None:
                    return
                queue_keys = set(self.channel_part_by_safe)
                safe_sources = resolve_event_queue_keys(event, queue_keys)
                if not safe_sources:
                    safe_sources = list(queue_keys)
                if safe_sources:
                    await self._handle_caption_edit(event)
            except Exception:
                print("监控文案同步异常：")
                TracePrinterHelper.print_trace()

        async def on_discussion_new(event: Any) -> None:
            if not getattr(self.worker, "running", False) or _flag(Working, "need_stop", False):
                return
            try:
                msg = getattr(event, "message", None)
                if isinstance(msg, MessageService) or msg is None:
                    return
                await self._handle_discussion_comment(event)
            except Exception:
                print("监控评论同步异常：")
                TracePrinterHelper.print_trace()

        all_source = list(getattr(self.worker, "all_source", None) or [])
        disc_ids = list(self.discussion_chat_ids)
        try:
            client.on(events.MessageEdited(chats=all_source), on_source_edited)
        except Exception:
            TracePrinterHelper.print_trace()
        if disc_ids:
            try:
                client.on(events.NewMessage(chats=disc_ids), on_discussion_new)
            except Exception:
                TracePrinterHelper.print_trace()

    async def resolve_group_first_id(self, entity: Any, msg: Any) -> int:
        event_id = int(getattr(msg, "id", 0) or 0)
        grouped_id = getattr(msg, "grouped_id", None)
        if not grouped_id or not event_id:
            return event_id
        min_id = max(1, event_id - ALBUM_LOOKBACK)
        ids = list(range(min_id, event_id + 1))
        client = getattr(self.worker, "client", None)
        fetched: Any = []
        if client is not None:
            try:
                fetched = await FloodGuard.with_flood_retry(
                    lambda: client.get_messages(entity, ids=ids),
                    prefix="monitor/followup/album_first",
                )
            except Exception:
                TracePrinterHelper.print_trace()
        if fetched and not isinstance(fetched, (list, tuple)):
            fetched = [fetched]
        return first_id_from_album_messages(event_id, fetched or [msg])

    async def _caption_message(
        self,
        entity: Any,
        event_msg: Any,
        first_id: int,
    ) -> Any:
        client = getattr(self.worker, "client", None)
        if client is None or not first_id:
            return event_msg
        got: Any = None
        try:
            got = await FloodGuard.with_flood_retry(
                lambda: client.get_messages(entity, ids=[int(first_id)]),
                prefix="monitor/followup/caption_first",
            )
        except Exception:
            TracePrinterHelper.print_trace()
        if isinstance(got, (list, tuple)):
            got = got[0] if got else None
        return got or event_msg

    async def _handle_caption_edit(self, event: Any) -> None:
        msg = getattr(event, "message", None)
        if msg is None:
            return
        source_peer_id = None
        try:
            source_peer_id = int(get_peer_id(getattr(event, "chat_id", None)))
        except Exception:
            source_peer_id = None
        safe_source = None
        if source_peer_id is not None:
            for key, value in self.source_peer_by_safe.items():
                if int(value) == source_peer_id:
                    safe_source = key
                    break
        if safe_source is None:
            return
        autos = [
            auto
            for auto in self._autos_for_safe_source(safe_source)
            if source_needs_caption_sync(auto)
        ]
        if not autos:
            return
        first_id = await self.resolve_group_first_id(getattr(event, "chat_id", None), msg)
        caption_msg = await self._caption_message(getattr(event, "chat_id", None), msg, first_id)
        new_html = message_html(caption_msg or msg)
        wait_idle = getattr(PublishIdRecord, "wait_writer_idle", None)
        if callable(wait_idle):
            try:
                wait_idle(2.0)
            except Exception:
                TracePrinterHelper.print_trace()
        dest_map = self._dest_id_map_for(safe_source, first_id)
        client = getattr(self.worker, "client", None)
        if client is None:
            return
        for dest_channel, ids in (dest_map or {}).items():
            for dest_msg_id in ids:
                try:
                    await FloodGuard.with_flood_retry(
                        lambda dc=dest_channel, did=dest_msg_id: client.edit_message(
                            dc,
                            int(did),
                            convertDest(new_html),
                            parse_mode="html",
                        ),
                        prefix="monitor/followup/edit_caption",
                    )
                    print("已同步源帖 ", safe_source, " 文案到 ", dest_channel, "/", dest_msg_id)
                except MessageNotModifiedError:
                    continue
                except Exception:
                    print("同步目标文案失败 ", dest_channel, "/", dest_msg_id, "：")
                    TracePrinterHelper.print_trace()

    async def _handle_discussion_comment(self, event: Any) -> None:
        msg = getattr(event, "message", None)
        if msg is None or isinstance(msg, MessageService):
            return
        safe_sources: Set[str] = set()
        for key in (
            str(getattr(event, "chat_id", "") or ""),
            str(getattr(msg, "chat_id", "") or ""),
        ):
            if key in self.channel_part_by_safe:
                safe_sources.add(self.channel_part_by_safe[key])
        try:
            disc_peer_id = int(get_peer_id(getattr(event, "chat_id", None)))
        except Exception:
            disc_peer_id = 0
        safe_sources.update(self.discussion_to_sources.get(disc_peer_id, set()))
        if not safe_sources:
            return
        anchor_id = discussion_reply_anchor_id(msg)
        client = getattr(self.worker, "client", None)
        if client is None:
            return
        anchor_msg: Any = None
        if anchor_id:
            try:
                anchor_msg = await FloodGuard.with_flood_retry(
                    lambda: client.get_messages(
                        getattr(event, "chat_id", None),
                        ids=[int(anchor_id)],
                    ),
                    prefix="monitor/followup/disc_anchor",
                )
            except Exception:
                TracePrinterHelper.print_trace()
        if isinstance(anchor_msg, (list, tuple)):
            anchor_msg = anchor_msg[0] if anchor_msg else None
        channel_post_id = channel_post_id_from_anchor(anchor_msg) or anchor_id
        for safe_source in safe_sources:
            autos = [
                auto
                for auto in self._autos_for_safe_source(safe_source)
                if source_needs_comment_live(auto)
            ]
            if not autos:
                continue
            source_peer_id = self.source_peer_by_safe.get(safe_source)
            if is_source_channel_mirror(msg, source_peer_id):
                continue
            channel_part = self.channel_part_by_safe.get(safe_source) or _channel_part_of(autos[0])
            source_ref = utils.convertPrivateIdIfNeed(channel_part)
            first_id = int(channel_post_id or anchor_id or 0)
            source_msg: Any = None
            if first_id:
                try:
                    source_msg = await FloodGuard.with_flood_retry(
                        lambda: client.get_messages(source_ref, ids=[first_id]),
                        prefix="monitor/followup/source_post",
                    )
                except Exception:
                    TracePrinterHelper.print_trace()
                if isinstance(source_msg, (list, tuple)):
                    source_msg = source_msg[0] if source_msg else None
                try:
                    first_id = await self.resolve_group_first_id(source_ref, source_msg or msg)
                except Exception:
                    print("解析源组首 ID 失败，回退 channel_post=", first_id, "：")
                    TracePrinterHelper.print_trace()
            dest_map = self._dest_id_map_for(safe_source, first_id)
            for auto in autos:
                kid = str(getattr(auto, "kid", "") or "")
                try:
                    need_convert = str(
                        getattr(auto, "convert_mode", "")
                        or getattr(self.worker.argsWrapper, "convert_mode", "")
                    ).lower() == "monitor"
                    converted: Any = [source_msg or msg]
                    if need_convert and source_msg is not None:
                        converted = await _sq_r_ca.convert_batch_with_retry(
                            "monitor",
                            [source_msg],
                        )
                        if not converted:
                            print("监控评论同步换票失败，跳过本条")
                            continue
                    parse = ParseBean(
                        uniId=safe_source,
                        messages=list(converted or [source_msg or msg]),
                        tart_text=message_html(msg),
                        original_msg_ids=[int(getattr(msg, "id", 0) or 0)],
                        source_main_msg_id=first_id or None,
                        comment_to_msg_id=anchor_id,
                        success=True,
                    )
                    await AutoWorkerWrapper.processRepliesIfNeed(
                        len(parse.messages),
                        dest_map,
                        auto,
                        client,
                        parse,
                        getattr(self.worker, "argsWrapper", None),
                    )
                except Exception:
                    print("监控评论复刻异常 kid=", kid, "：")
                    TracePrinterHelper.print_trace()

    def _dest_id_map_for(self, safe_source: str, first_id: int) -> Dict[str, List[int]]:
        out: Dict[str, List[int]] = {}
        channel_part = self.channel_part_by_safe.get(safe_source)
        for auto in self._autos_for_safe_source(safe_source):
            kid = str(getattr(auto, "kid", "") or "")
            if not channel_part:
                channel_part = _channel_part_of(auto)
            links: List[str] = []
            try:
                links = list(
                    PublishIdRecord.lookup_dest_links_for_source(
                        channel_part,
                        int(first_id or 0),
                        kid=kid,
                    )
                    or []
                )
            except Exception:
                links = []
            dest_cfgs: List[str] = []
            getter = getattr(auto, "getDestes", None)
            if callable(getter):
                try:
                    dest_cfgs = [str(value) for value in (getter() or [])]
                except Exception:
                    dest_cfgs = []
            if not dest_cfgs:
                try:
                    dest_cfgs = [str(value) for value in (getattr(auto, "destes", None) or [])]
                except Exception:
                    dest_cfgs = []
            try:
                mapped = PublishIdRecord.dest_id_map_from_dest_links(links, dest_cfgs)
            except Exception:
                mapped = {}
            if not mapped and dest_cfgs:
                try:
                    mapped = PublishIdRecord.dest_id_map_from_dest_links(dest_cfgs, dest_cfgs)
                except Exception:
                    mapped = {}
            for dest_channel, ids in (mapped or {}).items():
                bucket = out.setdefault(str(dest_channel), [])
                for msg_id in ids or []:
                    value = int(msg_id)
                    if value not in bucket:
                        bucket.append(value)
        return out
