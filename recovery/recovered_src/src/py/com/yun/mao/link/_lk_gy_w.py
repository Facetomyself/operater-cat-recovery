# Recovered module: src.py.com.yun.mao.link._lk_gy_w
# Names, signatures and the HMAC chain are reconstructed from the Nuitka
# constants/function table and the module init decompilation.
from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any


_gy_kc: bytes | None = None


def _gy_k0() -> bytes:
    global _gy_kc
    if _gy_kc is None:
        from ._tw_ctx import TwCtx

        key = TwCtx.tw_hq_by_k("_r_pk")
        _gy_kc = hashlib.sha256(b"pb_v3|" + str(key).encode("utf-8")).digest()
    return _gy_kc


def _gy_uc() -> str:
    from src.py.com.yun.mao.fea import _sq_jqm

    account = getattr(_sq_jqm, "zh_ye_xx", None)
    if not account:
        return ""
    info = account.current_account_info()
    if not info:
        return ""
    ucode = getattr(info, "ucode", "")
    return str(ucode).strip() if ucode else ""


def _gy_af(obj: Any) -> bool:
    try:
        from ..dclass.ExecCandidateHelper import compute_af

        ticket = getattr(obj, "ticket", None)
        exec_obj = getattr(obj, "exec", None)
        if not ticket or not exec_obj:
            return False
        expected = getattr(ticket, "af", "")
        if not expected:
            return False
        exec_dict = json.loads(json.dumps(exec_obj, default=lambda o: o.__dict__))
        actual = compute_af(exec_dict)
        return str(actual).lower() == str(expected).lower()
    except Exception:
        return False


def _gy_ma(ticket: Any, kid: str, auto_type: int) -> bytes:
    text = f"A|{ticket.batch_id}|{kid}|{int(auto_type)}|{ticket.exp}"
    return text.encode("utf-8")


def _gy_mb(ticket: Any, kid: str, ucode: str) -> bytes:
    uc_hash = hashlib.sha256(str(ucode or "").encode("utf-8")).hexdigest()
    sign_item = str(getattr(ticket, "sign_item", "") or "")
    text = f"B|{sign_item[:32]}|{ticket.uc_hash}|{uc_hash}|{kid}|{ticket.mode}"
    return text.encode("utf-8")


def _gy_mc(ticket: Any, kid: str, auto_type: int) -> bytes:
    text = f"C|{ticket.etid}|{ticket.sn}|{ticket.af}|{kid}|{int(auto_type)}"
    return text.encode("utf-8")


def _gy_da(ticket: Any, kid: str, auto_type: int) -> bytes:
    return hmac.new(
        _gy_k0(), _gy_ma(ticket, kid, auto_type), hashlib.sha256
    ).digest()


def _gy_db(ticket: Any, kid: str, ucode: str) -> bytes:
    return hmac.new(
        _gy_k0(), _gy_mb(ticket, kid, ucode), hashlib.sha256
    ).digest()


def _gy_dc(ticket: Any, kid: str, auto_type: int) -> bytes:
    return hmac.new(
        _gy_k0(), _gy_mc(ticket, kid, auto_type), hashlib.sha256
    ).digest()


def gy_wc_hx(xxx: Any, ucode: str) -> None:
    if not ucode:
        return None
    uid = str(ucode).strip()
    ticket = xxx.ticket
    kid = str(getattr(xxx, "kid", "") or "").strip()
    auto_type = int(getattr(xxx, "auto_type", 0) or 0)
    ha = _gy_da(ticket, kid, auto_type)
    hb = _gy_db(ticket, kid, uid)
    hc = _gy_dc(ticket, kid, auto_type)
    xxx._g0 = ha[:12] + hb[:12]
    xxx._g1 = hb[12:24] + hc[:12]
    xxx._gx = int(getattr(ticket, "exp", 0) or 0)
    return None


def _gy_h0(obj: Any) -> bool:
    try:
        if obj is None or obj.__class__.__name__ != "AutoBeanXXX":
            return False
        g0 = getattr(obj, "_g0", None)
        g1 = getattr(obj, "_g1", None)
        if not isinstance(g0, (bytes, bytearray)):
            return False
        if not isinstance(g1, (bytes, bytearray)):
            return False
        if len(g0) != 24 or len(g1) != 24:
            return False
        if not getattr(obj, "ticket", None):
            return False
        return getattr(obj, "exec", None) is not None
    except Exception:
        return False


def _gy_ex(obj: Any) -> bool:
    try:
        gx = int(getattr(obj, "_gx", 0) or 0)
        if not gx:
            return False
        return time.time() < gx
    except Exception:
        return False


def _gy_sa(obj: Any) -> bool:
    try:
        ticket = obj.ticket
        kid = str(getattr(obj, "kid", "") or "").strip()
        auto_type = int(getattr(obj, "auto_type", 0) or 0)
        expected = _gy_da(ticket, kid, auto_type)
        return obj._g0[:12] == expected[:12]
    except Exception:
        return False


def _gy_sb(obj: Any, ucode: str) -> bool:
    if not ucode:
        return False
    try:
        ticket = obj.ticket
        kid = str(getattr(obj, "kid", "") or "").strip()
        expected = _gy_db(ticket, kid, str(ucode).strip())
        if obj._g0[12:24] != expected[:12]:
            return False
        if obj._g1[:12] != expected[12:24]:
            return False
        actual_uc_hash = hashlib.sha256(
            str(ucode).encode("utf-8")
        ).hexdigest()
        stored = getattr(ticket, "uc_hash", "")
        if not stored:
            return False
        return actual_uc_hash.lower() == str(stored).lower()
    except Exception:
        return False


def _gy_sc(obj: Any) -> bool:
    try:
        ticket = obj.ticket
        kid = str(getattr(obj, "kid", "") or "").strip()
        auto_type = int(getattr(obj, "auto_type", 0) or 0)
        expected = _gy_dc(ticket, kid, auto_type)
        return obj._g1[12:24] == expected[:12]
    except Exception:
        return False


def _gy_rs(obj: Any) -> bool:
    """Delegate to AutoBeanXXX's wire-signature verifier.

    The decompiled body imports ``_verify_sign_item`` lazily and calls it as
    ``(kid, auto_type, ticket)``.  A ``None`` kid is normalised to the empty
    string before the call, matching the original ``PyObject_Str`` branch.
    """

    from ..dclass.AutoBeanXXX import _verify_sign_item

    ticket = obj.ticket
    kid = getattr(obj, "kid", "")
    kid = "" if kid is None else str(kid)
    auto_type = int(getattr(obj, "auto_type", 0) or 0)
    return bool(_verify_sign_item(kid, auto_type, ticket))


def gy_jc_a1(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj):
        return False
    return _gy_sa(obj)


def gy_jc_a2(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj) or not _gy_sa(obj):
        return False
    ucode = _gy_uc()
    return bool(ucode and _gy_sb(obj, ucode))


def gy_jc_a3(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj):
        return False
    ucode = _gy_uc()
    return bool(ucode and _gy_sb(obj, ucode))


def gy_jc_a4(obj: Any) -> bool:
    if not gy_jc_a3(obj) or not _gy_af(obj):
        return False
    return _gy_rs(obj)


def gy_jc_a5(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj):
        return False
    ucode = _gy_uc()
    if not ucode:
        return False
    if not _gy_sb(obj, ucode):
        return False
    if not _gy_sa(obj):
        return False
    if not _gy_sc(obj):
        return False
    if not _gy_rs(obj):
        return False
    if not _gy_af(obj):
        return False
    return bool(obj.ensure_valid(ucode))


def gy_jc_a6(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj):
        return False
    if not _gy_sc(obj) or not _gy_af(obj):
        return False
    ticket = getattr(obj, "ticket", None)
    mode = str(getattr(ticket, "mode", "") or "").strip().lower()
    if mode and mode not in ("timing", "once", "monitor"):
        return False
    ucode = _gy_uc()
    return bool(ucode and _gy_sb(obj, ucode))


def gy_jc_a7(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj):
        return False
    ucode = _gy_uc()
    if not ucode:
        return False
    if not _gy_sa(obj) or not _gy_af(obj):
        return False
    if not _gy_sb(obj, ucode):
        return False
    return _gy_rs(obj)


def gy_jc_a8(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj):
        return False
    if not _gy_sc(obj) or not _gy_af(obj):
        return False
    return _gy_rs(obj)


def gy_jc_a9(obj: Any) -> bool:
    if not _gy_h0(obj) or not _gy_ex(obj):
        return False
    ucode = _gy_uc()
    if not ucode:
        return False
    if not _gy_af(obj) or not _gy_sa(obj):
        return False
    return _gy_sb(obj, ucode)


class GyJcXc:
    """Namespace exposing the recovered validation helpers."""

    gy_wc_hx = staticmethod(gy_wc_hx)
    _gy_h0 = staticmethod(_gy_h0)
    _gy_ex = staticmethod(_gy_ex)
    _gy_sa = staticmethod(_gy_sa)
    _gy_sb = staticmethod(_gy_sb)
    _gy_uc = staticmethod(_gy_uc)
    gy_jc_a3 = staticmethod(gy_jc_a3)
    _gy_af = staticmethod(_gy_af)
    _gy_rs = staticmethod(_gy_rs)
    _gy_sc = staticmethod(_gy_sc)
    gy_jc_a1 = staticmethod(gy_jc_a1)
    gy_jc_a2 = staticmethod(gy_jc_a2)
    gy_jc_a4 = staticmethod(gy_jc_a4)
    gy_jc_a5 = staticmethod(gy_jc_a5)
    gy_jc_a6 = staticmethod(gy_jc_a6)
    gy_jc_a7 = staticmethod(gy_jc_a7)
    gy_jc_a8 = staticmethod(gy_jc_a8)
    gy_jc_a9 = staticmethod(gy_jc_a9)
