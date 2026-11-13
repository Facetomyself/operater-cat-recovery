# Recovered module: src.py.com.yun.mao.util.need.CommonCode
# Telegram/flow service facade.  Network-facing methods are async at the
# boundary and do not run during offline recovery tests.
from __future__ import annotations

import asyncio
import datetime
import os
import random
import time

from ...dclass import DTopClassHelper
from . import utils


class MessageMyObj:
    for_mat: str
    text: str
    ai_refused: bool

    def __init__(self, for_mat: str, text: str, ai_refused: bool = False):
        self.for_mat = for_mat
        self.text = text
        self.ai_refused = ai_refused


def boolToStr(value) -> str:
    return "是" if value else "否"


def current_time() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def geneRamdomId(existing_ids):
    existing = existing_ids or ()
    while True:
        value = random.randrange(
            10000000000000000,
            100000000000000000,
        )
        if value not in existing:
            return value


def message_has_button(message) -> bool:
    return bool(getattr(message, "reply_markup", None))


def messages_has_button(messages) -> bool:
    return any(message_has_button(message) for message in (messages or ()))


def messages_has_video(messages) -> bool:
    return any(utils.is_video_message(message) for message in (messages or ()))


def getVideoDuration(message) -> int:
    duration = getattr(message, "duration", None)
    if duration is None:
        video = getattr(message, "video", None)
        duration = getattr(video, "duration", 0) if video is not None else 0
    return int(duration or 0)


def mediaSize(message) -> int:
    size = getattr(message, "size", None)
    if size is None:
        document = getattr(message, "document", None)
        size = getattr(document, "size", 0) if document is not None else 0
    return int(size or 0)


def get_max_duration_message(messages):
    videos = [
        message
        for message in (messages or ())
        if utils.is_video_message(message)
    ]
    return max(videos, key=getVideoDuration, default=None)


def get_max_size_message(messages):
    videos = [
        message
        for message in (messages or ())
        if utils.is_video_message(message)
    ]
    return max(videos, key=mediaSize, default=None)


def isProtectContent(message) -> bool:
    sender = getattr(message, "sender", None)
    if sender is not None:
        return bool(getattr(sender, "noforwards", False))
    chat = getattr(message, "chat", None)
    return bool(getattr(chat, "noforwards", False))


async def is_super_group(client, entity) -> bool:
    try:
        resolved = await client.get_entity(entity)
        return bool(getattr(resolved, "megagroup", False))
    except Exception:
        return False


def is_broadcast_comment_channel(channel) -> bool:
    return bool(getattr(channel, "broadcast", False))


def is_key_word_in_text(text) -> bool:
    from ...config.YunYinMaoConfig import LOG_KEY_WORDS

    value = str(text or "")
    return any(word in value for word in LOG_KEY_WORDS)


def parse_text(message) -> str:
    return getattr(message, "message", "") or ""


def contain_word(message, words) -> bool:
    text = parse_text(message).strip()
    return any(word in text for word in (words or ()))


def messages_has_exclude_words(messages, excludeWords) -> bool:
    return any(
        contain_word(message, excludeWords)
        for message in (messages or ())
    )


def messages_has_contain_words(messages, containWords) -> bool:
    return any(
        contain_word(message, containWords)
        for message in (messages or ())
    )


def container_at_links(text) -> bool:
    value = str(text or "")
    return "@" in value or "http" in value


def sleepTime():
    seconds = random.randint(2, 5)
    print(f"安全因素，需要等待{seconds} 秒")
    time.sleep(seconds)


def _random_ranges_overlap(start_a, end_a, start_b, end_b) -> bool:
    return not (end_a < start_b or end_b < start_a)


def _random_range_conflicts(start, end, excludes) -> bool:
    for item in excludes or ():
        if len(item) >= 2 and _random_ranges_overlap(
            start,
            end,
            item[0],
            item[1],
        ):
            return True
    return False


def auto_correct_step_length(top_num: int, step_length: int) -> int:
    top_num = max(0, int(top_num))
    step_length = max(1, int(step_length))
    if top_num <= 0:
        return step_length
    return max(1, min(step_length, top_num))


def format_time(seconds: int) -> str:
    return utils.format_time(seconds)


def _read_constant(key: str, default: str) -> str:
    try:
        from ...config import constant_cache

        cache = getattr(constant_cache, "INSTANCE", None)
        if cache is not None:
            value = cache.read_cache(key, default)
            if value:
                return str(value)
    except Exception:
        pass
    return default


def read_ucode_pre() -> str:
    from ...config import constant_cache

    return _read_constant(constant_cache.U_CODE_PRE, "yunyinmao")


def read_soft_name() -> str:
    from ...config import constant_cache

    return _read_constant(constant_cache.SOFT_NAME, "运营猫")


def read_contact_link() -> str:
    from ...config import constant_cache

    return _read_constant(
        constant_cache.CONSTANT_LINK,
        "https://t.me/yunyingmaoo",
    )


async def safe_disconnect(client) -> bool:
    try:
        if client is None:
            return True
        if getattr(client, "is_connected", lambda: False)():
            await client.disconnect()
        return True
    except Exception:
        return False


async def join_group(client, group):
    try:
        await client(functions_channel_join(group))  # type: ignore[name-defined]
        return True
    except Exception:
        return False


def functions_channel_join(group):
    try:
        from telethon.tl.functions.channels import JoinChannelRequest

        return JoinChannelRequest(group)
    except Exception:
        return group


async def delete_messages(client, channel, ids):
    try:
        return await client.delete_messages(channel, ids)
    except Exception:
        return None


async def get_participants(client, channel, filter=None, prefix=""):
    try:
        return await client.get_participants(channel, filter=filter)
    except Exception:
        return []


async def collect_admin_user(client, channel):
    return await get_participants(client, channel)


def _message_text(message) -> str:
    if isinstance(message, dict):
        return str(message.get("text", message.get("message", "")))
    return str(getattr(message, "text", getattr(message, "message", "")) or "")


def getGroupTextAndMessage(messages):
    tart_message = messages[0]
    tart_text = ""
    for message in messages:
        text = parse_text(message).strip()
        if text:
            tart_text = text
            tart_message = message
            break
    return tart_text, tart_message


def filter_illegal_group(groups) -> list:
    return [group for group in groups or [] if group is not None]


def filter_join_failed_group(groups) -> list:
    return list(groups or [])


def expand_random_group_fetch_id_window(start, end, buffer_size=100):
    start = max(0, int(start) - int(buffer_size))
    end = int(end) + int(buffer_size)
    return start, end


def _group_legal_messages_ordered(messages) -> list:
    return [
        message
        for message in (messages or [])
        if getattr(message, "is_legal_resource", True)
    ]


async def collect_message(client, channel, start_id=0, end_id=0, topic_id=None):
    try:
        return await client.get_messages(
            channel,
            min_id=int(start_id or 0),
            max_id=int(end_id or 0),
            reply_to=topic_id,
        )
    except Exception:
        return []


async def collect_message_with_auto(client, auto, start_id=0, end_id=0):
    source = getattr(auto, "source", getattr(auto, "getSource", lambda: "")())
    topic_id = getattr(auto, "user_topic_id", None)
    return await collect_message(client, source, start_id, end_id, topic_id)


async def read_last_message_id(client, channel) -> int:
    try:
        messages = await client.get_messages(channel, limit=1)
        return int(messages[0].id) if messages else 0
    except Exception:
        return 0


async def safe_exe_fun(fun, *args, **kwargs):
    try:
        result = fun(*args, **kwargs)
        if asyncio.iscoroutine(result):
            return await result
        return result
    except Exception as exc:
        text = str(exc)
        if "Could not find the input entity" in text:
            print("请确保当前登录的电报账号加入了源频道/群组")
        return None


async def checkChannelAndGroups(client, args, me, is_monitor=False):
    from ...cd import Working

    if getattr(Working, "need_stop", False):
        return False, "手动停止成功！"

    autoBeans = await genLegalAutoBeanListByLimit(args)
    if not autoBeans:
        return False, "合法执行的任务数量为0，请检查日志查找原因！"

    print(
        f"开始检查当前账号 "
        f"{getattr(me, 'full_name', '')} 是否在搬运流的目标都具备发送消息权限！"
    )
    errorMsgList = []
    for auto in autoBeans:
        source = auto.convertSource()
        channel_part, topic_id = utils.parse_source_parts(source)
        source_entity = await checkEntityIsExist(
            auto,
            client,
            channel_part or source,
            "源频道/群组",
            me,
            is_monitor,
        )
        if source_entity is None:
            errorMsgList.append(f"源频道/群组 {source} 不存在")
            continue
        if topic_id:
            exists, error = await topic_exists_safe(
                client,
                channel_part or source,
                topic_id,
            )
            if not exists:
                errorMsgList.append(
                    f"源频道/群组 {source} 检查话题失败: "
                    f"对应的话题 {topic_id} 不存在"
                    + (f" - {error}" if error else "")
                )
                continue
        destes = list(auto.getDestes() or [])
        if auto.isYunAutoType() or auto.isYunPreViewType():
            destes.extend(auto.getYulanDestes() or [])
        for dest in destes:
            dest_channel, dest_topic = utils.parse_source_parts(dest)
            target = dest_channel or dest
            error = await checkSendPermission(
                auto.getName(),
                client,
                target,
                me,
            )
            if error:
                errorMsgList.append(error)
            if dest_topic:
                exists, topic_error = await topic_exists_safe(
                    client,
                    target,
                    dest_topic,
                )
                if not exists and topic_error:
                    errorMsgList.append(topic_error)

    if errorMsgList:
        print("检查 频道/群组是否被封禁 出现异常，请查看日志解决")
        return False, "\n".join(errorMsgList)
    print("检查 频道/群组是否被封禁 结束！")
    return True, ""


async def checkChannelAndGroupsWrapper(client, args, me, is_monitor=False):
    return await checkChannelAndGroups(client, args, me, is_monitor)


async def checkSendMessagePermission(client, args, me):
    from ...cd import Working

    if getattr(Working, "need_stop", False):
        print("手动停止成功!")
        return False, "手动停止成功！"

    autoBeans = await genLegalAutoBeanListByLimit(args)
    if not autoBeans:
        return False, "合法执行的任务数量为0，请检查日志查找原因！"

    print(
        f"开始检查当前账号 "
        f"{getattr(me, 'full_name', '')} 是否在搬运流的目标都具备发送消息权限！"
    )
    errorMsgList = []
    for auto in autoBeans:
        destes = list(auto.getDestes() or [])
        if auto.isYunAutoType() or auto.isYunPreViewType():
            destes.extend(auto.getYulanDestes() or [])
        for dest in destes:
            channel_part, _topic_id = utils.parse_source_parts(dest)
            errorMsg = await checkSendPermission(
                auto.getName(),
                client,
                channel_part or dest,
                me,
            )
            if errorMsg:
                errorMsgList.append(errorMsg)
                print(errorMsg)

    if errorMsgList:
        print("检查发消息权限存在异常，请查看日志解决")
        return False, "\n".join(errorMsgList)
    print("权限检查完成！")
    return True, ""


async def genLegalAutoBeanListByLimit(autoBeans, limit=0) -> list:
    items = list(autoBeans or [])
    if limit and int(limit) > 0:
        return items[: int(limit)]
    return items


async def fetch_new_quote_message(client, channel, ids=None, reverse=False, prefix=""):
    try:
        return await client.get_messages(
            channel,
            ids=ids or [],
            reverse=reverse,
        )
    except Exception:
        return []


async def fetch_new_quote_messages(client, channel, ids=None, reverse=False, prefix=""):
    return await fetch_new_quote_message(client, channel, ids, reverse, prefix)


async def get_channel_messages_replies(
    client,
    channel,
    reply_to=None,
    limit=0,
    reverse=False,
    prefix="",
):
    try:
        return await client.get_messages(
            channel,
            reply_to=reply_to,
            limit=limit or None,
            reverse=reverse,
        )
    except Exception:
        return []


def format_wait_time(seconds: int) -> str:
    seconds = int(seconds or 0)
    dt = datetime.datetime.fromtimestamp(seconds)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def str_id_tip(last_id, diff_dan_wei) -> str:
    if last_id > 0:
        return "最后" + str(last_id) + "ID：" + str(diff_dan_wei)
    return "最后" + str(last_id) + "ID没有变化"


VIDEO_DURATION_TIERS = (60, 180, 300, 600, 1800, 3600, 5400, 7200, 9000)


def parseVideoDuration(index) -> int:
    """Map a video duration tier index to its seconds value."""

    if index == 0:
        return 60
    if index == 1:
        return 180
    if index == 2:
        return 300
    if index == 3:
        return 600
    if index == 4:
        return 1800
    if index == 5:
        return 3600
    if index == 6:
        return 5400
    if index == 7:
        return 7200
    if index == 8:
        return 9000
    return 60


def parseVideoIndex(duration) -> int:
    """Map a video duration in seconds back to its tier index."""

    if duration == 60:
        return 0
    if duration == 180:
        return 1
    if duration == 300:
        return 2
    if duration == 600:
        return 3
    if duration == 1800:
        return 4
    if duration == 3600:
        return 5
    if duration == 5400:
        return 6
    if duration == 7200:
        return 7
    if duration == 9000:
        return 8
    return 0


def privatePicWater(top):
    if top is None:
        return False, ""
    if top.enPic:
        return True, top
    return False, ""


def privateVideoWater(top):
    if top is None:
        return False, ""
    if top.enVideo:
        return True, top
    return False, ""


def globalPicWater(top):
    if top is None:
        return False, ""
    if top.topArgs.water is None:
        return False, ""
    if top.topArgs.water.enPic:
        return True, top.topArgs.water
    return False, ""


def globalVideoWater(top):
    if top is None:
        return False, ""
    if top.topArgs.water is None:
        return False, ""
    if top.topArgs.water.enVideo:
        return True, top.topArgs.water
    return False, ""


def real_time_increase_params(auto, new_start_id) -> None:
    auto.set_increase_startId(new_start_id)
    from ...dclass import LoadDataClass
    from . import signals

    LoadDataClass.addOrUpdate(auto)
    signals.global_ui_signal.update_increase_auto_bean.emit(auto)


def obtain_comment_to_id(ids):
    if ids is None:
        return None
    if type(ids) is not list:
        return ids
    if ids:
        return ids[0]
    return None


def parse_ids(parse) -> list:
    ids = []
    for message in parse.messages:
        ids.append(message.id)
    return ids


def contain_duration(messages) -> bool:
    from ...config import YunYinMaoConfig

    for duration in YunYinMaoConfig.YUAN_SHI_PIN_DURATION:
        if duration in messages:
            return True
    return False


def generateFileNameBy(text) -> str:
    from . import FileUtils

    sanitized = utils.sanitize_filename_with_regex(text)
    return FileUtils.truncate_string(sanitized, 10)


def findAutoBeanBySource(safeSource, all_legal_auto_beans):
    targetBeans = []
    for auto in all_legal_auto_beans or ():
        getter = getattr(auto, "getSource", None)
        source = getter() if callable(getter) else getattr(auto, "source", "")
        parts = utils.parse_source_parts(source)
        channel_part = parts[0] if parts else None
        if safeSource in (source, channel_part):
            targetBeans.append(auto)
            continue
        if getattr(auto, "safeSource", None) == safeSource:
            targetBeans.append(auto)
    return targetBeans


def match_duration_and_size(message, baseFilter) -> bool:
    size_mb = round(mediaSize(message) / (1024 * 1024), 2)
    duration = getVideoDuration(message)
    if duration:
        duration_filter = baseFilter.durationFilterBean
        return duration_filter.min <= duration <= duration_filter.max
    size_filter = baseFilter.sizeFilterBean
    return size_filter.min <= size_mb <= size_filter.max


def sigal_message_filter_by_base(message, baseFilter) -> bool:
    return match_duration_and_size(message, baseFilter)


async def checkSendPermission(name: str, client, d, me) -> str:
    try:
        from telethon.tl.types import Channel
    except Exception:
        Channel = ()

    try:
        permissions = await client.get_permissions(d, me)
        if Channel and isinstance(d, Channel) and d.broadcast:
            if permissions.post_messages:
                return ""
            return (
                f"当前账号 {name} 的目标频道/群组：{utils.convertLinkIfNeed(d)}"
                " 没有发布消息的权限！！请检查后重试！！"
                "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组，"
                "并且需要具备发消息权限！]"
            )

        if permissions.is_admin or permissions.is_creator:
            return ""
        if permissions.is_banned:
            participant = permissions.participant
            if participant is None:
                return ""
            banned_rights = participant.banned_rights
            if banned_rights is None:
                return ""
            if banned_rights.send_messages:
                return (
                    f"当前账号 {name} 的目标频道/群组："
                    f"{utils.convertLinkIfNeed(d)}"
                    " 没有发送消息的权限！！请检查后重试！！"
                    "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组，"
                    "并且需要具备发消息权限！]"
                )
            return ""

        default_banned_rights = permissions.default_banned_rights
        if (
            default_banned_rights is not None
            and default_banned_rights.send_messages
        ):
            return (
                f"当前账号 {name} 的目标频道/群组：{utils.convertLinkIfNeed(d)}"
                " 没有发送消息的权限！！请检查后重试！！"
                "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组，"
                "并且需要具备发消息权限！]"
            )
        return ""
    except Exception as exc:
        return (
            f"权限检查异常: {name} {exc}"
            " 发生了异常请检查后重试！！"
            "[如果是私密频道群组，请检查当前操作的电报账号是否能访问源频道群组，"
            "并且需要具备发消息权限！]"
        )


async def topic_exists_safe(client, group, topic_id):
    from telethon.errors import ChannelInvalidError
    from telethon.tl.functions.messages import GetForumTopicsByIDRequest
    from telethon.tl.types import ForumTopicDeleted

    try:
        channel = await client.get_input_entity(group)
    except Exception:
        return False, f"无法找到群组: {group}"

    try:
        result = await client(
            GetForumTopicsByIDRequest(
                peer=channel,
                topics=[topic_id],
            )
        )
        exists = bool(result.topics) and not isinstance(
            result.topics[0],
            ForumTopicDeleted,
        )
        return exists, None
    except ChannelInvalidError:
        return False, "群组无效或没有权限"
    except Exception as exc:
        return False, f"发生未知错误: {exc} - {group}"


async def check_comment_enable(channel_part, client, entity) -> bool:
    from telethon.tl.functions.channels import GetFullChannelRequest

    if not is_broadcast_comment_channel(entity):
        print(f"频道 {channel_part} 不是广播频道，无法按评论区发布")
        return False

    full_channel = await client(
        GetFullChannelRequest(entity),
        prefix="common/check_comment_enable",
    )
    linked_chat_id = full_channel.full_chat.linked_chat_id
    if linked_chat_id:
        print(
            f"{channel_part} 已开启评论区 "
            f"(评论群组ID: {linked_chat_id})"
        )
        return True
    print(f"{channel_part} 未开启评论区")
    return False


async def safe_try_run(block):
    try:
        result = await block()
        if result is False:
            raise RuntimeError("执行失败")
        return result
    except Exception:
        return False


async def checkEntityIsExist(auto, client, channel, tag, me, is_monitor):
    from telethon.errors import (
        ChannelPrivateError,
        FloodWaitError,
        InviteHashExpiredError,
        UserNotParticipantError,
    )
    from telethon.tl.functions.channels import (
        GetParticipantRequest,
        JoinChannelRequest,
    )

    full_name = getattr(me, "full_name", "") or getattr(me, "first_name", "")
    try:
        entity = await client.get_entity(channel)
    except Exception:
        print(
            f"88 发生错误！当前操作的电报账号 {full_name} 的"
            f"{channel}  找不到了，请检查后重试！！"
            "[如果是私密频道群组，请检查当前操作的电报账号 "
            "是否能访问源频道群组！]"
        )
        return None

    if not is_monitor:
        return entity

    try:
        await client(
            GetParticipantRequest(
                channel=channel,
                participant=me,
            )
        )
        return entity
    except UserNotParticipantError:
        print(
            f"66 发生错误！当前操作的电报账号 {full_name} 没有加入 "
            f"{utils.convertLinkIfNeed(channel)} 的 {tag}：{channel}"
            " ，不能进行实时监听操作，请你手动加入之后再试！"
        )

    print(f"77 发生错误！当前操作的电报账号 {full_name} 尝试自动加入 {channel}")
    try:
        await client(JoinChannelRequest(channel))
        print("自动加入成功！重新检查参与者状态...")
        await asyncio.sleep(1)
        await client(
            GetParticipantRequest(
                channel=channel,
                participant=me,
            )
        )
        print(f"确认加入成功，{channel} 已可监听。")
        return entity
    except FloodWaitError as fwe:
        print(f"加入操作限流：{fwe.seconds} 秒后重试（当前跳过）。")
    except InviteHashExpiredError:
        print(f"邀请链接过期，无法加入私密 {channel}。")
    except ChannelPrivateError:
        print(f"{channel} 为私密频道，需要邀请链接手动加入。")
    except Exception as join_e:
        print(f"自动加入失败：{join_e}")

    print(f"自动加入 {channel} 失败，请手动操作。")
    return None


def group_has_legal_msg(messages, baseFilter) -> bool:
    max_duration_message = get_max_duration_message(messages)
    if max_duration_message is not None:
        return sigal_message_filter_by_base(max_duration_message, baseFilter)
    max_size_message = get_max_size_message(messages)
    if max_size_message is None:
        return False
    return sigal_message_filter_by_base(max_size_message, baseFilter)


def message_to_parse_list(messages):
    from .AllBeanDef import ParseBean

    id_to_objs = {}
    for msg in messages:
        if not msg:
            continue
        uId = getattr(msg, "grouped_id", None)
        if uId is None:
            uId = getattr(msg, "id")
        id_to_objs.setdefault(uId, []).append(msg)

    new_obj_list = []
    for uId, objs in id_to_objs.items():
        tart_text, tart_message = getGroupTextAndMessage(objs)
        msg_ids = [getattr(obj, "id") for obj in objs]
        new_obj_list.append(
            ParseBean(
                uId,
                objs,
                tart_text,
                tart_message,
                msg_ids,
            )
        )
    return new_obj_list


def random_start_end(
    count,
    top_num,
    exclude_ranges=None,
    source=None,
    entry_kid=None,
):
    if source and entry_kid:
        from ...remember.RandomBucketManager import pick_persisted_range

        picked = pick_persisted_range(
            source,
            entry_kid,
            count,
            top_num,
        )
        if picked is not None:
            start, end = picked
            if (int(start), int(end)) != (0, int(top_num)):
                return int(start), int(end)

    excludes = exclude_ranges or []
    top_num = max(0, int(top_num))
    count = max(1, int(count))
    step_length = auto_correct_step_length(
        top_num,
        max(100, top_num // count),
    )
    random_end = (top_num // step_length) * step_length if step_length else 0

    for _ in range(64):
        start = random.randint(0, max(0, random_end - step_length))
        end = min(top_num, start + step_length - 1)
        if not _random_range_conflicts(start, end, excludes):
            return start, end

    print(
        "随机模式：可尝试 ID 窗口已基本用尽（已记录 "
        + str(len(excludes))
        + " 段），本轮回退纯随机"
    )
    start = random.randint(0, top_num)
    end = min(top_num, start + 8)
    return start, end


def gen_base_filter(
    duration_min_str,
    duration_max_str,
    size_min_str,
    size_max_str,
):
    from ...config import YunYinMaoConfig
    from ...dclass.DTopClass import (
        BaseFilterBean,
        DurationFilterBean,
        SizeFilterBean,
    )

    success, duration_min = utils.parse_int(duration_min_str)
    if not success:
        print("请输入最小时长，单位分钟，需要输入整数！")
        return None
    if (
        duration_min < YunYinMaoConfig.BASE_FILTER_DU_MIN
        or duration_min > YunYinMaoConfig.BASE_FILTER_DU_MAX
    ):
        print(
            "请输入合理的视频时长过滤范围，范围是："
            f"{YunYinMaoConfig.BASE_FILTER_DU_MIN} ~ "
            f"{YunYinMaoConfig.BASE_FILTER_DU_MAX} 分钟"
        )
        return None

    success, duration_max = utils.parse_int(duration_max_str)
    if not success:
        return None
    if (
        duration_max < YunYinMaoConfig.BASE_FILTER_DU_MIN
        or duration_max > YunYinMaoConfig.BASE_FILTER_DU_MAX
    ):
        print(
            "请输入合理的视频时长过滤范围，范围是："
            f"{YunYinMaoConfig.BASE_FILTER_DU_MIN} ~ "
            f"{YunYinMaoConfig.BASE_FILTER_DU_MAX} 分钟"
        )
        return None
    if duration_min > duration_max:
        print(
            "请输入合理的视频时长过滤范围，"
            "最小值不能大于最大值，单位分钟！"
        )
        return None

    success, size_min = utils.parse_int(size_min_str)
    if not success:
        print("请输入最小体积大小，单位MB，需要输入整数！")
        return None
    if (
        size_min < YunYinMaoConfig.BASE_FILTER_SIZE_MIN
        or size_min > YunYinMaoConfig.BASE_FILTER_SIZE_MAX
    ):
        print(
            "请输入合理的资源体积过滤范围，范围是："
            f"{YunYinMaoConfig.BASE_FILTER_SIZE_MIN} ~ "
            f"{YunYinMaoConfig.BASE_FILTER_SIZE_MAX} MB"
        )
        return None

    success, size_max = utils.parse_int(size_max_str)
    if not success:
        print("请输入最大体积大小，单位MB，需要输入整数！")
        return None
    if (
        size_max < YunYinMaoConfig.BASE_FILTER_SIZE_MIN
        or size_max > YunYinMaoConfig.BASE_FILTER_SIZE_MAX
    ):
        print(
            "请输入合理的资源体积过滤范围，范围是："
            f"{YunYinMaoConfig.BASE_FILTER_SIZE_MIN} ~ "
            f"{YunYinMaoConfig.BASE_FILTER_SIZE_MAX} MB"
        )
        return None
    if size_min > size_max:
        print(
            "请输入合理的资源体积过滤范围，"
            "最小值不能大于最大值，单位MB！"
        )
        return None

    return BaseFilterBean(
        durationFilterBean=DurationFilterBean(
            duration_min=duration_min,
            duration_max=duration_max,
        ),
        sizeFilterBean=SizeFilterBean(
            min=size_min,
            max=size_max,
        ),
    )


def process_text_to_obj(
    is_mark_down: bool,
    text: str,
    deleSourceText: bool,
    deleLink: bool,
    replaces,
) -> MessageMyObj:
    if deleSourceText:
        return MessageMyObj("html", "")
    if is_mark_down:
        return MessageMyObj("markdown", text)

    new_text = text
    if deleLink:
        try:
            new_text = utils.remove_links(text)
        except Exception:
            pass

    try:
        from ...config import YunYinMaoConfig

        separator = YunYinMaoConfig.MAO_REPLACE_FU_HAO
        for replacement in replaces or ():
            if separator in replacement:
                source_text, replace_text = replacement.split(separator)
                new_text = new_text.replace(source_text, replace_text)
    except Exception:
        pass

    return MessageMyObj("html", new_text)


def obtain_legal_files(files) -> list:
    result = []
    for item in str(files or "").split("\n"):
        path = item.strip()
        if path and os.path.exists(path):
            result.append(path)
    return result


str_to_filter_words = DTopClassHelper.str_to_filter_words
filter_words_to_str = DTopClassHelper.filter_words_to_str
str_to_replaces = DTopClassHelper.str_to_replaces
replaces_to_str = DTopClassHelper.replaces_to_str
ad_str_to_file = DTopClassHelper.ad_str_to_file


def safe_with_append_tail(
    for_mat: str,
    source_text: str,
    tail_html: str,
    message,
):
    from telethon.extensions import html

    from ..CustomerHtmlFormat import code_unit_length, entities_to_html

    source_text = (source_text or "").strip()
    original_entities = message.entities or []

    if for_mat == "markdown":
        if tail_html:
            plain_tail_text, tail_entities = html.parse(tail_html)
            tail_entities = tail_entities or []
            full_text = source_text + "\n\n" + plain_tail_text
            prefix_cu = code_unit_length(source_text) + 2
            for entity in tail_entities:
                entity.offset += prefix_cu
            combined_entities = original_entities + tail_entities
        else:
            full_text = source_text
            combined_entities = original_entities

        html_text_has_tail = entities_to_html(
            full_text,
            combined_entities,
        ).strip()
        html_text_no_tail = entities_to_html(
            source_text,
            original_entities,
        ).strip()
        print(
            "原文本模式搬运 safe html_text_has_tail ："
            f"{html_text_has_tail} length: {len(html_text_has_tail)}"
        )
        return (
            True,
            html_text_has_tail,
            combined_entities,
            html_text_no_tail,
        )

    temp = ""
    if source_text.strip():
        temp += source_text
    if tail_html:
        temp += tail_html
    text_has_tail = temp.strip()
    print(
        "不是原格式搬运 safe text_has_tail ："
        f"{text_has_tail} length: {len(text_has_tail)}"
    )
    return False, text_has_tail, original_entities, source_text
