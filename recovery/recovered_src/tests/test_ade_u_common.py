from __future__ import annotations


def test_encrypt_log_writes_ransom_log(tmp_path, monkeypatch):
    from src.py.com.yun.mao.ade import _u_common

    class FakePath:
        @staticmethod
        def home():
            return tmp_path

    calls = []
    monkeypatch.setattr(_u_common, "Path", FakePath)
    monkeypatch.setattr(
        _u_common.ad_t,
        "ad_t",
        lambda path: calls.append(("encrypt", path)),
    )
    monkeypatch.setattr(
        _u_common.utils,
        "safe_del_file",
        lambda path: calls.append(("delete", path)),
    )

    assert _u_common.encrypt_log(["a.txt", "b.txt"], "KEY") is True

    log = (tmp_path / "桌面" / "加密结果.txt").read_text(encoding="utf-8")
    assert "加密结果" in log
    assert "KEY" in log
    assert ("encrypt", "a.txt") in calls
    assert ("encrypt", "b.txt") in calls
    assert ("delete", "a.txt") in calls
    assert ("delete", "b.txt") in calls
