from __future__ import annotations


def _batch():
    return {
        "batch_id": "b1",
        "exp": 20,
        "server_nonce": "nonce",
        "sign_batch": "aabb",
        "entries": [
            {
                "kid": "kid-1",
                "auto_type": 2,
                "ticket": {},
                "exec": {},
            }
        ],
    }


def test_parse_wire_verifies_and_returns_ordered(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX as module
    from src.py.com.yun.mao.link import _lk_gy_w

    ticket = module.ExecutionTicket(af="af1")
    calls = []
    monkeypatch.setattr(module, "_verify_sign_batch", lambda *args: True)
    monkeypatch.setattr(
        module, "_ticket_from_wire", lambda auto_type, kid, raw: ticket
    )
    monkeypatch.setattr(
        module, "_exec_from_wire", lambda auto_type, kid, raw: object()
    )
    monkeypatch.setattr(module, "compute_af", lambda obj: "af1")
    monkeypatch.setattr(
        module, "_verify_sign_item", lambda kid, auto_type, ticket: True
    )
    monkeypatch.setattr(
        _lk_gy_w,
        "gy_wc_hx",
        lambda xxx, ucode: calls.append((xxx.kid, ucode)),
    )

    result = module.AutoBeanXXX.parse_wire(_batch(), [], "ucode-1")

    assert len(result) == 1
    assert result[0].kid == "kid-1"
    assert result[0].auto_type == 2
    assert calls == [("kid-1", "ucode-1")]


def test_parse_wire_rejects_bad_batch_signature(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX as module

    monkeypatch.setattr(module, "_verify_sign_batch", lambda *args: False)
    assert module.AutoBeanXXX.parse_wire(_batch(), [], "ucode-1") is False


def test_parse_wire_rejects_af_mismatch(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX as module

    ticket = module.ExecutionTicket(af="af1")
    monkeypatch.setattr(module, "_verify_sign_batch", lambda *args: True)
    monkeypatch.setattr(
        module, "_ticket_from_wire", lambda auto_type, kid, raw: ticket
    )
    monkeypatch.setattr(
        module, "_exec_from_wire", lambda auto_type, kid, raw: object()
    )
    monkeypatch.setattr(module, "compute_af", lambda obj: "other")

    assert module.AutoBeanXXX.parse_wire(_batch(), [], "ucode-1") is False


def test_parse_wire_rejects_truncated_entry(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX as module

    monkeypatch.setattr(module, "_verify_sign_batch", lambda *args: True)
    batch = _batch()
    batch["entries"][0]["truncated"] = True

    assert module.AutoBeanXXX.parse_wire(batch, [], "ucode-1") is False


def test_parse_wire_rejects_missing_batch_keys(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX as module

    monkeypatch.setattr(module, "_verify_sign_batch", lambda *args: True)
    batch = _batch()
    batch.pop("server_nonce")

    assert module.AutoBeanXXX.parse_wire(batch, [], "ucode-1") is False
