from __future__ import annotations

from types import SimpleNamespace


def _ticket(**overrides):
    from src.py.com.yun.mao.dclass.AutoBeanXXX import ExecutionTicket

    data = {
        "ver": 1,
        "batch_id": "b1",
        "etid": "e1",
        "sn": "s1",
        "af": "af1",
        "uc_hash": "u1",
        "mode": "timing",
        "iat": 10,
        "exp": 20,
        "sign_item": "00ff",
    }
    data.update(overrides)
    return ExecutionTicket(**data)


def test_build_item_sign_payload_uses_recovered_field_order():
    from src.py.com.yun.mao.dclass.AutoBeanXXX import _build_item_sign_payload

    assert (
        _build_item_sign_payload(_ticket(), "kid-1", 2)
        == "1|b1|e1|s1|af1|u1|timing|10|20|kid-1|2"
    )


def test_verify_sign_item_forwards_payload_and_hex_signature(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX as module

    captured = {}

    monkeypatch.setattr(module, "jm_jz_r_pk", lambda: "PUBLIC-KEY")

    def fake_verify(public_key, message, signature):
        captured.update(
            public_key=public_key,
            message=message,
            signature=signature,
        )
        return True

    monkeypatch.setattr(module, "jm_yq_qm", fake_verify)

    ticket = _ticket(sign_item=" 00ff ")
    assert module._verify_sign_item("kid-1", 2, ticket) is True
    assert captured["public_key"] == "PUBLIC-KEY"
    assert captured["message"] == b"1|b1|e1|s1|af1|u1|timing|10|20|kid-1|2"
    assert captured["signature"] == bytes.fromhex("00ff")


def test_verify_sign_batch_joins_kids_with_commas(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX as module

    captured = {}

    monkeypatch.setattr(module, "jm_jz_r_pk", lambda: "PUBLIC-KEY")
    monkeypatch.setattr(
        module,
        "jm_yq_qm",
        lambda key, message, signature: captured.update(
            key=key, message=message, signature=signature
        )
        or True,
    )

    assert module._verify_sign_batch("b1", 20, "nonce", ["k1", "k2"], "00ff") is True
    assert captured["message"] == b"b1|20|nonce|k1,k2"
    assert captured["signature"] == bytes.fromhex("00ff")


def test_verify_sign_batch_empty_signature_short_circuits(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX as module

    called = []
    monkeypatch.setattr(
        module, "jm_yq_qm", lambda *args: called.append(args) or True
    )

    assert module._verify_sign_batch("b1", 20, "nonce", ["k1"], "") is False
    assert called == []


def test_gy_rs_calls_verifier_with_kid_auto_type_ticket(monkeypatch):
    from src.py.com.yun.mao.dclass import AutoBeanXXX as module
    from src.py.com.yun.mao.link import _lk_gy_w

    captured = {}

    def fake_verify(kid, auto_type, ticket):
        captured.update(kid=kid, auto_type=auto_type, ticket=ticket)
        return True

    monkeypatch.setattr(module, "_verify_sign_item", fake_verify)
    obj = SimpleNamespace(ticket="TICKET", kid=None, auto_type="3")

    assert _lk_gy_w._gy_rs(obj) is True
    assert captured == {"kid": "", "auto_type": 3, "ticket": "TICKET"}


def test_ticket_from_wire_reads_ticket_fields_with_defaults():
    from src.py.com.yun.mao.dclass.AutoBeanXXX import _ticket_from_wire

    ticket = _ticket_from_wire(
        {"ver": "2", "batch_id": "b2", "exp": "30", "sign_item": "aabb"},
        auto_type=4,
        kid="kid-4",
    )

    assert ticket.ver == 2
    assert ticket.batch_id == "b2"
    assert ticket.exp == 30
    assert ticket.sign_item == "aabb"
    assert ticket.mode == ""


def test_exec_from_wire_builds_inactive_autobean():
    from src.py.com.yun.mao.dclass.AutoBeanXXX import _exec_from_wire

    auto = _exec_from_wire({"source": "demo"}, auto_type=2, kid="kid-2")

    assert auto is not None
    assert auto.kid == "kid-2"
    assert auto.auto_type == 2
    assert auto.active is False
    assert auto.priority == 100


def test_ensure_valid_checks_expiry_hash_and_exec_kid(monkeypatch):
    import hashlib
    import time

    from src.py.com.yun.mao.dclass import AutoBeanXXX as module

    ucode = "ucode-1"
    uc_hash = hashlib.sha256(ucode.encode("utf-8")).hexdigest().lower()
    ticket = module.ExecutionTicket(
        af="af1",
        exp=int(time.time()) + 60,
        uc_hash=uc_hash,
    )
    exec_obj = type("Exec", (), {"kid": "kid-1"})()
    xxx = module.AutoBeanXXX(
        kid="kid-1",
        auto_type=2,
        ticket=ticket,
        exec_obj=exec_obj,
    )
    monkeypatch.setattr(module, "_verify_sign_item", lambda *args: True)

    assert xxx.ensure_valid(ucode) is True
    assert xxx.ensure_valid("other-ucode") is False

    xxx.ticket = module.ExecutionTicket(
        af="af1",
        exp=int(time.time()) - 1,
        uc_hash=uc_hash,
    )
    assert xxx.ensure_valid(ucode) is False

    xxx.ticket = ticket
    xxx.exec_obj = type("Exec", (), {"kid": "other-kid"})()
    assert xxx.ensure_valid(ucode) is False
