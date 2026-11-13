from __future__ import annotations

import types

import pytest

from src.py.com.yun.mao.auto import FlowProcess, YunProcess


@pytest.mark.parametrize("module", [FlowProcess, YunProcess])
def test_flow_process_publish_success_recorder(monkeypatch, module):
    recorded = []
    monkeypatch.setattr(
        module,
        "_optional_import",
        lambda name, attr=None: (
            lambda dest, message_id: recorded.append((dest, message_id))
        ),
    )
    module._record_publish_success("dest", types.SimpleNamespace(id=7))
    assert recorded == [("dest", 7)]
