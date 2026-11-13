from __future__ import annotations

from src.py.com.yun.mao.ad import AdIdMapManager


def test_ad_id_map_uses_recovered_key_and_round_trips(monkeypatch, tmp_path):
    assert AdIdMapManager.ADMAP_INFO_KEY
    monkeypatch.setattr(
        AdIdMapManager.YunYinMaoConfig,
        "abs_cache_dir",
        lambda: str(tmp_path),
    )
    monkeypatch.setattr(
        AdIdMapManager.utils,
        "encrypt",
        lambda key, payload: (
            key + b"|" + (payload.encode("utf-8") if isinstance(payload, str) else payload)
        ),
        raising=False,
    )
    monkeypatch.setattr(
        AdIdMapManager.utils,
        "decrypt",
        lambda key, payload: payload.split(b"|", 1)[1].decode("utf-8"),
        raising=False,
    )
    monkeypatch.setattr(
        AdIdMapManager.utils,
        "init_folder",
        lambda path: None,
        raising=False,
    )
    AdIdMapManager.adIdMap.clear()
    assert AdIdMapManager.updateAdIds("k-1", [1, 2]) == [1, 2]
    AdIdMapManager.adIdMap.clear()
    assert AdIdMapManager.loadAdIdMap() == {"k-1": [1, 2]}
    assert AdIdMapManager.getIds("k-1") == [1, 2]
