# Recovered module: src.py.com.yun.mao.auto.TopicUtils
# Telegram forum-topic helpers.  Names, argument names, request classes, log
# text, and control-flow branches come from the module init and nested
# coroutine constants.  The network calls use Telethon's stable public API.
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from telethon import functions
from telethon.errors import ChannelInvalidError, ChatAdminRequiredError

from src.py.com.yun.mao.util import FloodGuard
from src.py.com.yun.mao.util.need import CommonCode, utils
from src.py.com.yun.mao.util.need.AllBeanDef import ParseBean


def parse_msg_topic_id(msg, topic_id):
    """Return the explicit topic id or the id carried by ``msg.reply_to``."""

    if topic_id:
        return int(topic_id)
    reply_to = getattr(msg, "reply_to", None)
    if reply_to is None:
        return 0
    if not getattr(reply_to, "forum_topic", False):
        return 0
    return int(
        getattr(reply_to, "reply_to_top_id", None)
        or getattr(reply_to, "reply_to_msg_id", None)
        or 0
    )


def parse_parseBean_topic_id(parse: ParseBean):
    """Resolve a topic id from a parse bean.

    ``ParseBean`` currently carries the source messages rather than a dedicated
    ``topic_id`` field, so the first message is the authoritative fallback.
    """

    explicit = getattr(parse, "topic_id", None)
    if explicit:
        return int(explicit)
    messages = getattr(parse, "messages", None) or []
    if messages:
        return parse_msg_topic_id(messages[0], 0)
    return 0


async def fetch_topic_info(client, source_channel, topic_id):
    """Fetch ``(title, icon_color)`` for a source forum topic."""

    if not topic_id:
        return None, None
    try:
        source_result = await FloodGuard.with_flood_retry(
            lambda: client(
                functions.channels.GetForumTopicsByIDRequest(
                    peer=source_channel,
                    topics=[int(topic_id)],
                )
            ),
            prefix="fetch_topic_info/GetForumTopicsByIDRequest",
        )
        topics = getattr(source_result, "topics", None) or []
        if not topics:
            print(f"无法获取源话题 {topic_id} 的信息，跳过")
            return None, None
        source_topic = topics[0]
        return (
            getattr(source_topic, "title", None),
            getattr(source_topic, "icon_color", None),
        )
    except Exception as exc:
        print(f"获取源话题信息失败: {exc!r}")
        return None, None


async def ensure_forum_enabled(client, channel):
    """Ensure that a group has Telegram forum topics enabled."""

    try:
        entity = await FloodGuard.with_flood_retry(
            lambda: client.get_entity(channel),
            prefix="topic_utils/ensure_forum_enabled/get_entity",
        )
        if not getattr(entity, "megagroup", False):
            print("警告：目标不是 群组，无法使用话题！！")
            return False
        if getattr(entity, "forum", False):
            print("目标群组已启用话题模式！")
            return True

        print("目标群组未启用话题模式，正在启用...")
        await FloodGuard.with_flood_retry(
            lambda: client(
                functions.channels.ToggleForumRequest(
                    channel=entity,
                    enabled=True,
                    tabs=False,
                )
            ),
            prefix="topic_utils/ensure_forum_enabled/ToggleForumRequest",
        )
        print("目标群组话题模式已启用")
        return True
    except Exception as exc:
        print(f"自动开启话题失败: {exc!r}")
        return False


async def create_topic_if_not_exists(
    client,
    dest_channel,
    title,
    icon_color=None,
    enable=True,
):
    """Find an exact destination topic or create it and return its id."""

    if not enable:
        return None
    try:
        search_result = await FloodGuard.with_flood_retry(
            lambda: client(
                functions.channels.GetForumTopicsRequest(
                    peer=dest_channel,
                    q=title,
                    offset_date=datetime.now(timezone.utc) - timedelta(days=365),
                    offset_id=0,
                    offset_topic=0,
                    limit=100,
                )
            ),
            prefix="create_topic/GetForumTopicsRequest",
        )
        for topic in getattr(search_result, "topics", None) or []:
            topic_title = getattr(topic, "title", None)
            if topic_title == title:
                topic_id = getattr(topic, "id", None)
                print(f"找到匹配的目标群组话题ID： {topic_id}")
                return topic_id
            if topic_title:
                print(f"搜索到的标题 '{topic_title}' 与 '{title}' 不精确匹配，将创建新话题")
                break
        else:
            print(f"未找到标题 '{title}' 的匹配话题，将创建新话题")

        try:
            me = await client.get_me()
            permissions = await client.get_permissions(dest_channel, me)
            participant = getattr(permissions, "participant", None)
            if participant is None:
                print("当前账号无权限信息或不是参与者，跳过创建")
                return None
            admin_rights = getattr(permissions, "admin_rights", None)
            if admin_rights is None or not getattr(admin_rights, "manage_topics", False):
                print("当前账号无 admin_rights 或 manage_topics 属性，跳过创建!")
                return None
            print("权限检查通过：有 manage_topics 权限")
        except Exception:
            # Permission probes vary by Telethon/account type.  The create
            # request below still enforces the server-side permission.
            permissions = None

        create_result = await FloodGuard.with_flood_retry(
            lambda: client(
                functions.channels.CreateForumTopicRequest(
                    peer=dest_channel,
                    title=title,
                    icon_color=int(icon_color or 0),
                )
            ),
            prefix="create_topic/CreateForumTopicRequest",
        )

        new_topic_id = None
        for update in getattr(create_result, "updates", None) or []:
            message = getattr(update, "message", None)
            if message is None:
                continue
            action = getattr(message, "action", None)
            if action is not None and action.__class__.__name__ == "MessageActionTopicCreate":
                new_topic_id = getattr(message, "id", None)
                break
            if new_topic_id is None:
                new_topic_id = getattr(message, "id", None)
        if new_topic_id is not None:
            print(f"已创建新话题 '{title}'，ID: {new_topic_id}")
        return new_topic_id
    except ChannelInvalidError:
        print("目标频道无效或未加入")
        return None
    except ChatAdminRequiredError:
        print("创建话题需管理员权限")
        return None
    except Exception as exc:
        print(f"创建话题失败: {exc!r}")
        return None


async def fetch_dest_topic_id(auto, client, d):
    """Resolve/create the destination topic corresponding to the source topic."""

    source_raw = ""
    try:
        source_raw = auto.getSource()
    except Exception:
        source_raw = getattr(auto, "source", "") or ""

    source_part, source_topic = utils.parse_source_parts(source_raw)
    dest_part, dest_topic = utils.parse_source_parts(d)
    dest_part = utils.convertPrivateIdIfNeed(dest_part)
    source_part = utils.convertPrivateIdIfNeed(source_part)

    topic_id = 0
    if source_topic:
        try:
            topic_id = int(source_topic)
        except (TypeError, ValueError):
            topic_id = 0
    if not topic_id:
        topic_id = int(getattr(auto, "user_topic_id", 0) or 0)

    dest_entity = await client.get_entity(dest_part)
    is_group = bool(await CommonCode.is_super_group(client, dest_entity))
    if not is_group:
        print(f"警告：目标 {dest_part} 不是群组，无法使用话题！！")
        return 0

    if not await ensure_forum_enabled(client, dest_entity):
        return 0

    if dest_topic:
        try:
            return int(dest_topic)
        except (TypeError, ValueError):
            return 0
    if not topic_id:
        return 0

    source_title, source_icon_color = await fetch_topic_info(
        client,
        source_part,
        topic_id,
    )
    if not source_title:
        return 0
    new_topic_id = await create_topic_if_not_exists(
        client,
        dest_entity,
        source_title,
        source_icon_color,
    )
    return int(new_topic_id or 0)
