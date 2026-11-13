"""Reconstructed license/account flow.

Evidence:
- Hex-Rays pseudocode: _sq_chk.parse_report, _sq_chk.hy_jx_bc
- runtime trace of hy_jx_bc reading data keys in this order:
  ucode, states, grade, limit, descs, hours, startRechargeTime,
  endRechargeTime, hasExperi, expire, botAbility, aiAbility, sendAtName,
  keFu, cloudBot, experiDuration, openPremium, priceConfig, maoContacts,
  apiKey, modelList, remainingSec, mul
- runtime observation: parse_report reads oj['data']['status']

This is a behavior reconstruction. The exact status dispatch and assignment
code are not byte-for-byte original.
"""

from __future__ import annotations

from .SqJqm_recovered import SqJqm


def is_success(response: dict, oj: dict) -> bool:
    """High confidence: reads oj['isSuccess'] and oj['msg']."""
    if not oj.get("isSuccess"):
        raise RuntimeError(oj.get("msg", "request failed"))
    return True


def parse_report(oj: dict) -> None:
    """Inferred dispatcher.

    Observed: reads oj['data']['status']; status 0 and 1 returned None in the
    live guest account. The other status values are not fully recovered.
    """
    data = oj["data"]
    status = int(data["status"])
    if status in (0, 1):
        return None
    return hy_jx_bc(oj)


def hy_jx_bc(oj: dict) -> SqJqm:
    """High confidence: field names and read order match SqJqm attributes."""
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
    # The original writes this into _sq_jqm.current_account_info and persists
    # the machine code via the encrypted .code cache.
    return info
