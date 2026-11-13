# Recovered module: src.py.com.yun.mao.mthread.GenHtmlThread
# Static reconstruction from the Nuitka module constants and the
# corresponding Hex-Rays bodies.  The class glue around the async task is
# inferred where the compiled dispatcher has no direct Python equivalent.
from __future__ import annotations

from typing import Any

from telethon import TelegramClient

from .TgClientBaseAsyncTaskThread import TgClientBaseAsyncTaskThread
from ..util.need import CommonCode, FindMessageUtils
from ..util.need.AllBeanDef import GenHtmlParamsBean

try:
    from ..util.CustomerHtmlFormat import entities_to_html
except Exception:
    def entities_to_html(text: str, entities: Any = None) -> str:
        """Fallback used when the optional HTML formatter is unavailable."""
        _ = entities
        return str(text or "")


def _emit_stats(bean: Any, success: bool, message: str) -> None:
    signal = getattr(bean, "stats_signal", None)
    if signal is not None:
        signal.emit(success, message)


class GenHtmlThread(TgClientBaseAsyncTaskThread):
    def __init__(self, bean: GenHtmlParamsBean):
        super().__init__(bean)
        self.bean = bean

    async def async_biz_task_run(
        self,
        client: TelegramClient,
        me: Any,
    ) -> None:
        """Fetch the configured post and emit its Telegram-HTML rendering.

        The source body reports failures through ``bean.stats_signal`` and
        disconnects the short-lived client before returning.  The exact tail
        handling is delegated to ``CustomerHtmlFormat.entities_to_html``.
        """
        _ = me
        message = await FindMessageUtils.get_message_from_link(
            client,
            getattr(self.bean, "post_link", ""),
        )
        if message is None:
            _emit_stats(self.bean, False, "当前账号采集消息失败，请检查原因！")
            await CommonCode.safe_disconnect(client)
            return

        text = getattr(message, "text", None)
        if not text or not str(text).strip():
            _emit_stats(self.bean, False, "当前帖子没有文本内容！")
            await CommonCode.safe_disconnect(client)
            return

        original_entities = getattr(message, "entities", None) or []
        html_text_has_tail = entities_to_html(str(text), original_entities)
        html_text_has_tail = str(html_text_has_tail or "").strip()
        _emit_stats(self.bean, True, html_text_has_tail)
        await CommonCode.safe_disconnect(client)

    def sync_biz_task_run(self, client: TelegramClient, me: Any) -> None:
        return super().sync_biz_task_run(client, me)
