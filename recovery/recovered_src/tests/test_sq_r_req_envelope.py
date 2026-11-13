from __future__ import annotations

import asyncio


def test_r_req_delegates_to_recovered_envelope(monkeypatch):
    from src.py.com.yun.mao.fea import _sq_r_req, _sq_req

    calls = []
    monkeypatch.setattr(
        _sq_req,
        "sq_sc_aes_k",
        lambda key: calls.append(("aes_k", key)) or b"wrapped",
    )
    monkeypatch.setattr(
        _sq_req,
        "sq_sc_aq_nr",
        lambda content, key: calls.append(("aq", content, key)) or b"cipher",
    )
    monkeypatch.setattr(
        _sq_req,
        "sq_jm_xy",
        lambda source, key: calls.append(("jm", source, key))
        or (True, {"ok": 1}, b"proof"),
    )

    assert _sq_r_req._r_sc_aes_k(b"key") == b"wrapped"
    assert _sq_r_req._r_sc_aq_nr("body", b"key") == b"cipher"
    assert _sq_r_req._r_jm_xy("{}", b"key") == (True, {"ok": 1}, b"proof")
    assert calls == [
        ("aes_k", b"key"),
        ("aq", "body", b"key"),
        ("jm", "{}", b"key"),
    ]


def test_r_post_with_retry_uses_generated_key(monkeypatch):
    from src.py.com.yun.mao.fea import _sq_r_req

    captured = {}
    monkeypatch.setattr(
        _sq_r_req._my_dt, "jm_sc_aes_k", lambda: b"generated-key"
    )

    async def fake_post(session, headers, url, json_content, dy_aes_key):
        captured["key"] = dy_aes_key
        captured["content"] = json_content
        return True, {"data": 1}, b"proof"

    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

    monkeypatch.setattr(_sq_r_req, "_r_http_post_once", fake_post)
    monkeypatch.setattr(
        _sq_r_req.aiohttp, "ClientSession", lambda: FakeSession()
    )

    result = asyncio.run(
        _sq_r_req._r_post_with_retry("https://example.test/r", "{}")
    )
    assert result == (True, {"data": 1}, b"proof")
    assert captured["key"] == b"generated-key"
    assert captured["content"] == "{}"
