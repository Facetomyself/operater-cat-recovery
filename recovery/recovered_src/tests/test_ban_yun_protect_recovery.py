from __future__ import annotations

import types

from src.py.com.yun.mao.auto import BanYunProtect


def test_protected_publish_success_recorder(monkeypatch):
    recorded = []
    monkeypatch.setattr(
        BanYunProtect,
        "_optional_import",
        lambda name, attr=None: (
            lambda channel, message_id: recorded.append((channel, message_id))
        ),
    )
    BanYunProtect._record_publish_success(
        "dest",
        types.SimpleNamespace(id=7),
    )
    assert recorded == [("dest", 7)]
