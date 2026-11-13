from __future__ import annotations

import asyncio
import types

from src.py.com.yun.mao.auto import BanYunUnProtect


def test_unprotect_logs_publish_success(monkeypatch):
    recorded = []
    marked = []
    result_cls = type("BanYunUnProtectSendResult", (), {})

    async def send_message_only(
        auto=None,
        client=None,
        dest=None,
        text=None,
        parse_mode=None,
        reply_to=None,
        prefix=None,
    ):
        if reply_to == 123:
            return types.SimpleNamespace(id=9)
        return types.SimpleNamespace(id=7)

    cmcode = types.SimpleNamespace(
        send_message_only=send_message_only,
        obtain_comment_to_id=lambda auto, parse, dest: 123,
    )
    flood = types.SimpleNamespace(with_flood_retry=None)
    working = types.SimpleNamespace(need_stop=False)
    dtop = types.SimpleNamespace(convertDest=lambda dest: dest)
    ledger = types.SimpleNamespace(
        should_skip_comment_group=lambda auto: False,
        mark_after_send=lambda *args: marked.append(args),
    )

    def fake_import(name, attr=None):
        values = {
            ("..util.need.AllBeanDef", "BanYunUnProtectSendResult"): result_cls,
            ("..cd", "Working"): working,
            ("..record", "CommentCopyLedger"): ledger,
            (".CMCode", None): cmcode,
            ("..util", "FloodGuard"): flood,
            (".TopicUtils", None): None,
            ("..dclass", "DTopClass"): dtop,
            ("..record.PublishIdRecord", "log_publish_success"): (
                lambda channel, msg_id: recorded.append((channel, msg_id))
            ),
        }
        return values.get((name, attr))

    monkeypatch.setattr(BanYunUnProtect, "_optional_import", fake_import)

    class Client:
        async def get_entity(self, dest):
            return dest

        async def send_message(self, dest, text, **kwargs):
            return types.SimpleNamespace(id=7)

    parse = types.SimpleNamespace(
        messages=[types.SimpleNamespace(id=1, text="hello")],
        medias=[],
        text="hello",
        tart_text="hello",
        source="src",
        source_main_msg_id=10,
        beanLike=None,
        ai_refused=False,
        is_keep_origin_source=False,
        full_text_has_tail=False,
        for_mat=None,
    )
    auto = types.SimpleNamespace(getDestes=lambda: ["dest"])
    result = asyncio.run(
        BanYunUnProtect.send_message_un_protect(
            Client(),
            parse,
            auto,
            {},
        )
    )
    assert result.send_success_count == 1
    assert recorded == [("dest", 7)]
    assert marked == [("src", 10, 1, "dest", 123, 9)]
