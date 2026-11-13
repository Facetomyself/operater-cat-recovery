from __future__ import annotations

from src.py.com.yun.mao.remember import RememberManager


def test_remember_manager_uses_recovered_key_and_round_trips(monkeypatch, tmp_path):
    assert RememberManager.REMEMBER_MAP_INFO_KEY
    monkeypatch.setattr(
        RememberManager,
        "_remember_file",
        lambda: tmp_path / "rememberMap.json",
        raising=False,
    )
    monkeypatch.setattr(
        RememberManager.utils,
        "encrypt",
        lambda key, payload: (
            key + b"|" + (payload.encode("utf-8") if isinstance(payload, str) else payload)
        ),
        raising=False,
    )
    monkeypatch.setattr(
        RememberManager.utils,
        "decrypt",
        lambda key, payload: payload.split(b"|", 1)[1].decode("utf-8"),
        raising=False,
    )
    monkeypatch.setattr(
        RememberManager.utils,
        "init_folder",
        lambda path: None,
        raising=False,
    )
    RememberManager.rememberMap.clear()
    RememberManager.updateRememberIds("@source", ["@dest"], [10, 11])
    RememberManager.rememberMap.clear()
    assert RememberManager.loadRememberMap() == {
        RememberManager._genRememberKey("@source", ["@dest"]): [10, 11]
    }
    assert RememberManager.getIds("@source", ["@dest"]) == [10, 11]
