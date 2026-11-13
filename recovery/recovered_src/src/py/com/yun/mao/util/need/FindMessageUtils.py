# Recovered module: src.py.com.yun.mao.util.need.FindMessageUtils
from __future__ import annotations


from . import utils


async def get_message_from_link(client, link: str):
    """Read a Telegram post link through a client when Telethon is available."""
    try:
        text = str(link or "").strip().rstrip("/")
        if "t.me/" not in text:
            print("不是电报帖子链接")
            return None
        parts = text.split("t.me/", 1)[1].split("/")
        if len(parts) < 2:
            print("不存在消息ID，不能正确采集消息")
            return None
        username = parts[0]
        message_id = utils.safe_parse_to_int(parts[-1], 0)
        if message_id <= 0:
            print("不存在消息ID，不能正确采集消息")
            return None
        if username == "c":
            entity = utils.convertPrivateIdIfNeed(parts[1])
            message_id = utils.safe_parse_to_int(parts[-1], 0)
        else:
            entity = await client.get_entity(username)
        messages = await client.get_messages(entity, ids=[message_id])
        return messages[0] if messages else None
    except Exception:
        return None
