# Recovered module: src.py.com.yun.mao.mthread.PostHtmlADThread
# Static reconstruction from the Nuitka constants and Hex-Rays bodies.
# Telegram-call ordering follows the compiled coroutine state machine; the
# small compatibility wrappers are marked inferred in their docstrings.
from __future__ import annotations

import contextlib
import inspect
from typing import Any

from telethon import TelegramClient
from telethon.tl import types

from .TgClientBaseAsyncTaskThread import TgClientBaseAsyncTaskThread
from ..auto import CMCode
from ..util import FloodGuard
from ..util.need import CommonCode, utils
from ..util.need.AllBeanDef import PostAdTestBean


try:
    flood_guard = FloodGuard.flood_guard
except Exception:
    def flood_guard(max_retries: int = 3, prefix: str = ""):
        """No-op fallback for the static recovery environment."""
        _ = (max_retries, prefix)

        def decorator(func):
            return func

        return decorator


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


@contextlib.contextmanager
def _upload_only_context():
    marker = getattr(CMCode, "upload_only", None)
    try:
        candidate = marker() if callable(marker) else marker
    except Exception:
        candidate = None
    if hasattr(candidate, "__enter__") and hasattr(candidate, "__exit__"):
        with candidate:
            yield
    else:
        yield


def _emit_stats(bean: Any, success: bool, message: str) -> None:
    signal = getattr(bean, "stats_signal", None)
    if signal is not None:
        signal.emit(success, message)


class PostHtmlADThread(TgClientBaseAsyncTaskThread):
    def __init__(self, bean: PostAdTestBean):
        super().__init__(bean)
        self.bean = bean

    async def async_biz_task_run(
        self,
        client: TelegramClient,
        me: Any,
    ) -> None:
        """Resolve the configured channel and publish the test advertisement."""
        channel_part, topic_id = utils.parse_source_parts(
            getattr(self.bean, "channel_source", "")
        )
        if channel_part is not None:
            channel_part = utils.convertPrivateIdIfNeed(channel_part)

        channel_entity = await self.check_channel(channel_part, client, me)
        if channel_entity is None:
            _emit_stats(self.bean, False, "发布测试广告失败，请查找原因！")
            return

        account_name = (
            getattr(me, "first_name", "")
            or getattr(me, "username", "")
        )
        try:
            error = await _maybe_await(
                CommonCode.checkSendPermission(
                    account_name,
                    client,
                    channel_entity,
                    me,
                )
            )
        except Exception as exc:
            print("发生错误！", exc)
            error = str(exc)
        if error:
            print(error)
            _emit_stats(self.bean, False, "")
            return

        await self.publish_test_ad(client, channel_entity, topic_id)

    async def check_channel(
        self,
        channel_entity: Any,
        client: TelegramClient,
        me: Any,
    ) -> Any:
        """Resolve a channel/group entity, mirroring the source error text."""
        try:
            entity = await client.get_entity(channel_entity)
            if entity is None:
                raise ValueError("entity not found")
            return entity
        except Exception:
            full_name = getattr(me, "full_name", "")
            error_msg = (
                "发生错误！"
                + str(channel_entity)
                + "  找不到了，请检查后重试！！[如果是私密频道群组，请检查当前操作的电报账号 "
                + str(full_name)
                + " 是否能访问源频道群组！]"
            )
            print(error_msg)
            return None

    def gen_msg_link(self, entity: Any, message: Any) -> str:
        """Return a public or private Telegram message link."""
        message_link = getattr(message, "message_link", None)
        if message_link:
            return str(message_link)

        link = ""
        channel_id = ""
        if isinstance(entity, types.Channel):
            username = getattr(entity, "username", None)
            if username:
                link = "".join(
                    ("https://t.me/", str(username), "/", str(message.id))
                )
            else:
                channel_id = str(getattr(entity, "id", ""))
                if channel_id.startswith("-100"):
                    channel_id = channel_id[4:]
                link = "".join(
                    ("https://t.me/c/", channel_id, "/", str(message.id))
                )
        return link

    @flood_guard(max_retries=3, prefix="publish_test_ad")
    async def publish_test_ad(
        self,
        client: TelegramClient,
        channel_entity: Any,
        topic_id: Any,
    ) -> None:
        """Send the configured text/files and report the resulting message link.

        The compiled body uses Telethon's ``send_message``/``send_file`` pair
        with HTML parse mode and the topic reply target.  Optional CMCode
        helpers are invoked defensively because they are absent from the
        reduced recovery source tree.
        """
        text = str(getattr(self.bean, "ad_html_text", "") or "")
        files = list(getattr(self.bean, "ad_files", None) or [])
        if not text and not files:
            _emit_stats(self.bean, False, "发布测试广告失败，请查找原因！")
            return

        message = None
        try:
            with _upload_only_context():
                if text:
                    message = await client.send_message(
                        channel_entity,
                        text,
                        parse_mode="HTML",
                        reply_to=topic_id,
                    )
                for file_path in files:
                    message = await client.send_file(
                        channel_entity,
                        file_path,
                        caption=text or "正在发布测试广告>>",
                        parse_mode="HTML",
                        reply_to=topic_id,
                        video_note=False,
                        supports_streaming=True,
                    )

            if message is None:
                fetcher = getattr(CMCode, "safeFetchFirstMessage", None)
                if callable(fetcher):
                    message = await _maybe_await(
                        fetcher(client, channel_entity)
                    )
                if message is None:
                    messages = await client.get_messages(channel_entity, limit=1)
                    message = messages[0] if messages else None

            link = self.gen_msg_link(channel_entity, message) if message else ""
            _emit_stats(self.bean, True, "发布测试广告成功！ → " + link)
        except Exception as exc:
            print("发生错误！", exc)
            _emit_stats(self.bean, False, "发布测试广告失败，请查找原因！")

    def sync_biz_task_run(self, client: TelegramClient, me: Any) -> None:
        return super().sync_biz_task_run(client, me)
