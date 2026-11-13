# Recovered module: src.py.com.yun.mao.fea._sq_chk
# Licence-response parser reconstructed from the pre-shutdown runtime trace
# and the Hex-Rays output for parse_report / hy_jx_bc.
from __future__ import annotations

import time

from . import _sq_jqm
from ._sq_jqm import SqJqm


FREEZE = 2
HUI_YUAN = 1
EXP_EIGHT = 3
CARD_GEEK = 2


def is_success(response: dict, oj: dict) -> bool:
    """Validate the envelope before reading the account state."""
    if not oj.get("isSuccess"):
        raise RuntimeError(oj.get("msg", "request failed"))
    return True


def parse_report(oj: dict) -> SqJqm | None:
    """Dispatch the report response.

    Runtime observation: status 0 and 1 both returned None from this
    dispatcher; account parsing is performed by hy_jx_bc.
    """
    data = oj.get("data", {})
    status = int(data.get("status", 0))
    if status in (0, 1):
        return None
    return hy_jx_bc(oj)


def hy_jx_bc(oj: dict) -> SqJqm:
    """Build the account object from the server report."""
    data = oj["data"]
    info = SqJqm(
        ucode=data["ucode"],
        status=data["status"],
        grade=data["grade"],
        limit=data["limit"],
        descs=data["descs"],
        hours=data["hours"],
        startTime=data["startTime"],
        endTime=data["endTime"],
        expire=data["expire"],
        hasExperi=data["hasExperi"],
        sendAtName=data["sendAtName"],
        keFu=data["keFu"],
        cloudBot=data["cloudBot"],
        botAbility=data["botAbility"],
        aiAbility=data["aiAbility"],
        experiDuration=data["experiDuration"],
        openPremium=data["openPremium"],
        priceConfig=data["priceConfig"],
        maoContacts=data["maoContacts"],
        remainingSec=data["remainingSec"],
        apiKey=data["apiKey"],
        modelList=data["modelList"],
        mul=data["mul"],
    )
    _sq_jqm.current_account_info = info
    _sq_jqm.current_account_time = time.time()
    return info


def ihy_nome() -> bool:
    return bool(_sq_jqm.current_account_info.grade)


def hy_ne() -> bool:
    return bool(_sq_jqm.current_account_info.expire)


def hy_dj() -> bool:
    return bool(_sq_jqm.current_account_info.hasExperi)


def hy_ty8() -> bool:
    return bool(_sq_jqm.current_account_info.has_exp_permission())


def zw_except_re_try() -> None:
    from ..util.need import signals

    signals.global_ui_signal.zw_except_re_try.emit()
