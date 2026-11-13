from __future__ import annotations

import pytest

from src.py.com.yun.mao.link import _fds_rt


class _FakeProbe:
    def __init__(self, calls: list[tuple[str, tuple, dict]]):
        self.calls = calls

    def __getattr__(self, name: str):
        def record(*args, **kwargs):
            self.calls.append((name, args, kwargs))
            return "unused"

        return record


@pytest.fixture
def probe_calls(monkeypatch):
    calls: list[tuple[str, tuple, dict]] = []
    monkeypatch.setattr(_fds_rt, "FdsHhx", lambda: _FakeProbe(calls))
    return calls


def _set_roll(monkeypatch, value: float) -> None:
    monkeypatch.setattr(_fds_rt.random, "random", lambda: value)


def test_direct_probe_wrappers(probe_calls):
    assert _fds_rt.fs_jc_qd() is None
    assert _fds_rt.fs_ui_ok() is None
    assert _fds_rt.fs_sjk_ws() is None
    assert _fds_rt.fs_sjk_qd() is None
    assert _fds_rt.fs_zh_tb() is None

    assert probe_calls == [
        ("fh_ht_jk", (4.0, 8.0), {}),
        ("fh_ui_qd", (), {}),
        ("fh_zhong", (), {}),
        ("fh_zhong", (), {}),
        ("fh_zhong", (), {}),
    ]


@pytest.mark.parametrize(
    ("roll", "method"),
    [
        (0.10, "fh_qing"),
        (0.60, "fh_lx_sd"),
        (0.90, "fh_zhong"),
    ],
)
def test_fs_http_three_way_branch(monkeypatch, probe_calls, roll, method):
    _set_roll(monkeypatch, roll)
    assert _fds_rt.fs_http() is None
    assert probe_calls == [(method, (), {})]


@pytest.mark.parametrize(
    ("roll", "method"),
    [
        (0.10, "fh_zhong"),
        (0.50, "fh_qing"),
    ],
)
def test_fs_hy_men_branch(monkeypatch, probe_calls, roll, method):
    _set_roll(monkeypatch, roll)
    assert _fds_rt.fs_hy_men() is None
    assert probe_calls == [(method, (), {})]


@pytest.mark.parametrize(
    ("roll", "method"),
    [
        (0.10, "fh_quan"),
        (0.50, "fh_zhong"),
    ],
)
def test_fs_dt_mk_branch(monkeypatch, probe_calls, roll, method):
    _set_roll(monkeypatch, roll)
    assert _fds_rt.fs_dt_mk() is None
    assert probe_calls == [(method, (), {})]


@pytest.mark.parametrize(
    ("roll", "method"),
    [
        (0.05, "fh_quan"),
        (0.50, "fh_zhong"),
    ],
)
def test_fs_pz_jm_branch(monkeypatch, probe_calls, roll, method):
    _set_roll(monkeypatch, roll)
    assert _fds_rt.fs_pz_jm() is None
    assert probe_calls == [(method, (), {})]


@pytest.mark.parametrize(
    ("roll", "method"),
    [
        (0.10, "fh_qing"),
        (0.90, "fh_lx_sd"),
    ],
)
def test_fs_yp_js_branch(monkeypatch, probe_calls, roll, method):
    _set_roll(monkeypatch, roll)
    assert _fds_rt.fs_yp_js() is None
    assert probe_calls == [(method, (), {})]


def test_fs_dt_lq_probabilistic_light_probe(monkeypatch, probe_calls):
    monkeypatch.setattr(_fds_rt, "_dt_lq_last_mid_mono", 0.0)
    _set_roll(monkeypatch, 0.5)

    assert _fds_rt.fs_dt_lq() is None
    assert probe_calls == [
        ("fh_qing", (), {}),
        ("fh_zhong_fast", (), {}),
    ]
