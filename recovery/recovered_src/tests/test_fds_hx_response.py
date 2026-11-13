from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    ("roll", "expected"),
    [
        (0.10, "fh_qing"),
        (0.70, "fh_zhong"),
        (0.95, "fh_quan"),
    ],
)
def test_fh_cj_selects_probabilistic_response(monkeypatch, roll, expected):
    from src.py.com.yun.mao.link import _fds_h_x as module

    probe = module.FdsHhx()
    calls: list[str] = []
    monkeypatch.setattr(probe, "_fd_log", lambda *args, **kwargs: calls.append("log"))
    monkeypatch.setattr(probe, "fh_ui_qd", lambda: calls.append("ui"))
    monkeypatch.setattr(probe, "fh_ht_jk", lambda: calls.append("ht"))
    monkeypatch.setattr(probe, "fh_qing", lambda: calls.append("fh_qing"))
    monkeypatch.setattr(probe, "fh_zhong", lambda: calls.append("fh_zhong"))
    monkeypatch.setattr(probe, "fh_quan", lambda: calls.append("fh_quan"))
    monkeypatch.setattr(probe, "jk_qb", lambda: False)
    monkeypatch.setattr(module.random, "random", lambda: roll)

    assert probe.fh_cj() is False
    assert calls[:3] == ["log", "ui", "ht"]
    assert calls[3] == expected
