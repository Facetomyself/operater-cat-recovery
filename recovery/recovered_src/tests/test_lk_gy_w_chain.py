from __future__ import annotations

import hashlib
import hmac
import time
from types import SimpleNamespace


def _module(monkeypatch, ucode="ucode-1"):
    from src.py.com.yun.mao.link import _lk_gy_w as module

    monkeypatch.setattr(module, "_gy_k0", lambda: b"k" * 32)
    monkeypatch.setattr(module, "_gy_uc", lambda: ucode)
    return module


def _ticket(ucode="ucode-1", exp=None):
    return SimpleNamespace(
        batch_id="batch",
        etid="etid",
        sn="sn",
        af="af",
        exp=int(time.time()) + 60 if exp is None else exp,
        uc_hash=hashlib.sha256(ucode.encode("utf-8")).hexdigest(),
        sign_item="s" * 64,
        mode="timing",
    )


def _obj(ticket):
    cls = type("AutoBeanXXX", (), {"ensure_valid": lambda self, ucode: True})
    obj = cls()
    obj.ticket = ticket
    obj.kid = "kid-1"
    obj.auto_type = 2
    obj.exec = object()
    return obj


def test_hmac_payloads_use_recovered_a_b_c_layout(monkeypatch):
    module = _module(monkeypatch)
    ticket = _ticket()

    assert module._gy_ma(ticket, "kid-1", 2) == (
        f"A|batch|kid-1|2|{ticket.exp}".encode("utf-8")
    )
    expected_b = (
        f"B|{'s' * 32}|{ticket.uc_hash}|"
        f"{hashlib.sha256(b'ucode-1').hexdigest()}|kid-1|timing"
    )
    assert module._gy_mb(ticket, "kid-1", "ucode-1") == expected_b.encode(
        "utf-8"
    )
    assert module._gy_mc(ticket, "kid-1", 2) == b"C|etid|sn|af|kid-1|2"

    key = b"k" * 32
    assert module._gy_da(ticket, "kid-1", 2) == hmac.new(
        key, module._gy_ma(ticket, "kid-1", 2), hashlib.sha256
    ).digest()
    assert module._gy_db(ticket, "kid-1", "ucode-1") == hmac.new(
        key, module._gy_mb(ticket, "kid-1", "ucode-1"), hashlib.sha256
    ).digest()
    assert module._gy_dc(ticket, "kid-1", 2) == hmac.new(
        key, module._gy_mc(ticket, "kid-1", 2), hashlib.sha256
    ).digest()


def test_gy_wc_hx_builds_matching_slices(monkeypatch):
    module = _module(monkeypatch)
    ticket = _ticket()
    obj = _obj(ticket)

    module.gy_wc_hx(obj, "ucode-1")

    assert obj._g0 == module._gy_da(ticket, "kid-1", 2)[:12] + module._gy_db(
        ticket, "kid-1", "ucode-1"
    )[:12]
    assert obj._g1 == module._gy_db(ticket, "kid-1", "ucode-1")[
        12:24
    ] + module._gy_dc(ticket, "kid-1", 2)[:12]
    assert obj._gx == ticket.exp
    assert module._gy_sa(obj) is True
    assert module._gy_sb(obj, "ucode-1") is True
    assert module._gy_sc(obj) is True


def test_validation_chain_accepts_valid_object_and_rejects_each_gap(
    monkeypatch,
):
    module = _module(monkeypatch)
    ticket = _ticket()
    obj = _obj(ticket)
    module.gy_wc_hx(obj, "ucode-1")

    monkeypatch.setattr(module, "_gy_af", lambda value: True)
    monkeypatch.setattr(module, "_gy_rs", lambda value: True)
    for name in (
        "gy_jc_a1",
        "gy_jc_a2",
        "gy_jc_a3",
        "gy_jc_a4",
        "gy_jc_a5",
        "gy_jc_a6",
        "gy_jc_a7",
        "gy_jc_a8",
        "gy_jc_a9",
    ):
        assert getattr(module, name)(obj) is True, name

    expired = _ticket(exp=int(time.time()) - 1)
    expired_obj = _obj(expired)
    module.gy_wc_hx(expired_obj, "ucode-1")
    assert module.gy_jc_a1(expired_obj) is False

    bad_ucode = _ticket(ucode="other")
    bad_obj = _obj(bad_ucode)
    module.gy_wc_hx(bad_obj, "ucode-1")
    assert module._gy_sb(bad_obj, "ucode-1") is False
    assert module.gy_jc_a2(bad_obj) is False
