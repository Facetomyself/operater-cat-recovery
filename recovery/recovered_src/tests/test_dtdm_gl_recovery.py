from __future__ import annotations

import base64

from src.py.com.yun.mao.fea import _dtdm_gl
from src.py.com.yun.mao.fea._dtdm_jz import DtdmJz
from src.py.com.yun.mao.fea import _dtdm_jz
from src.py.com.yun.mao.link import _fds_tan
from src.py.com.yun.mao.link import _fds_rt


def test_dt_hq_fn_reads_cached_namespace(monkeypatch):
    key = "worker-key"

    def worker():
        return "ok"

    monkeypatch.setitem(
        DtdmJz._code_cache,
        key,
        {"dynamic_inner_work_task": worker},
    )
    monkeypatch.setattr(_fds_rt, "fs_dt_mk", lambda: None)

    assert _dtdm_gl.dt_hq_fn("dynamic_inner_work_task", key) is worker
    assert _dtdm_gl.dt_hq_fn("missing", key) is None
    assert _dtdm_gl.dt_hq_fn("dynamic_inner_work_task", "missing") is None


def test_dt_jz_dm_binds_worker_from_cache(monkeypatch):
    key = "worker-key"

    def worker():
        return "ok"

    monkeypatch.setitem(
        DtdmJz._code_cache,
        key,
        {"dynamic_inner_work_task": worker},
    )
    monkeypatch.setattr(_fds_rt, "fs_dt_mk", lambda: None)
    monkeypatch.setattr(
        DtdmJz,
        "dt_jz_xy",
        classmethod(
            lambda cls, response_data, code_key: (
                "dtdm_demo" if code_key == key else ""
            )
        ),
    )
    monkeypatch.setattr(_dtdm_gl, "sec", lambda value: value)
    monkeypatch.setattr(_dtdm_gl, "dynamic_inner_work_task", None)

    assert _dtdm_gl.dt_jz_dm(
        {"byte_code_iwt": "payload", "worker_key": key}
    ) is True
    assert _dtdm_gl.dynamic_inner_work_task is worker


def test_dt_jz_xy_runs_probe_before_cache_hit(monkeypatch):
    key = "worker-key"
    calls = []

    monkeypatch.setattr(
        _fds_tan,
        "wb_dt_zx",
        lambda *args, **kwargs: calls.append("probe"),
    )
    monkeypatch.setattr(_dtdm_jz, "sec", lambda value: value)
    monkeypatch.setitem(DtdmJz._code_cache, key, {"worker": lambda: None})

    assert DtdmJz.dt_jz_xy({"byte_code_iwt": "payload"}, key) == key
    assert calls == ["probe"]


def test_decode_and_decompress_reports_gzip_fallback(monkeypatch, capsys):
    monkeypatch.setattr(_dtdm_jz, "sec", lambda value: value)
    payload = base64.b64encode(b"not-gzip").decode("ascii")

    assert DtdmJz._decode_and_decompress(payload) == b"not-gzip"
    assert "dt_jz_gz_fail_tpl_14" in capsys.readouterr().out
