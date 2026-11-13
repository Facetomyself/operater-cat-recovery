from __future__ import annotations

from types import SimpleNamespace


def test_mem_auto_for_writeback_prefers_loaded_bean(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX, LoadDataClass

    expected = object()
    monkeypatch.setattr(
        LoadDataClass,
        "getAutoBeanById",
        lambda kid: expected if kid == "kid-1" else None,
    )
    bean = SimpleNamespace(kid="kid-1", exec_obj=object())
    assert AutoBeanXXX.mem_auto_for_writeback(bean) is expected


def test_mem_auto_for_writeback_falls_back_to_exec_obj(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX, LoadDataClass

    monkeypatch.setattr(LoadDataClass, "getAutoBeanById", lambda kid: None)
    exec_obj = object()
    bean = SimpleNamespace(kid="kid-2", exec_obj=exec_obj)
    assert AutoBeanXXX.mem_auto_for_writeback(bean) is exec_obj
