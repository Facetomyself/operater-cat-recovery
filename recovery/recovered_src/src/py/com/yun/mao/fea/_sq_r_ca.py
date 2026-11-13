# Recovered module: src.py.com.yun.mao.fea._sq_r_ca
# Batch conversion request with bounded retry.
from __future__ import annotations

import asyncio
from typing import Any, List, Optional

from . import _sq_jqm, _sq_r_bao, _sq_r_req
from ..dclass.ExecCandidateHelper import build_convert_items
from ..link._fds_jm import sec
from ._r_hb_file import RemoteHb
from ._pl_wd_file import q_m3_seal


_CA_BIZ_RETRY = 4


def _hb_parts(result) -> tuple[bool, Any, str, bool]:
    if isinstance(result, RemoteHb):
        return (
            bool(result.data is not None and not result.terminal),
            result.data,
            result.msg,
            result.terminal,
        )
    if isinstance(result, tuple) and len(result) >= 2 and isinstance(result[0], bool):
        return bool(result[0]), result[1], "", False
    if isinstance(result, dict):
        return bool(result.get("isSuccess", True)), result, str(result.get("msg", "")), False
    return bool(result), result, "", False


async def convert_batch_with_retry(
    mode: str,
    beans: List[object],
) -> Optional[List[object]]:
    if not beans:
        return []
    try:
        ucode = _sq_jqm.current_account_info.ucode
        items = build_convert_items(beans)
        body = _sq_r_bao.zq_r_convert_hb(ucode, mode, items)
    except Exception as exc:
        print(sec("rw_cs_fail_01"), exc)
        return None

    last_hb = None
    data = None
    for attempt in range(_CA_BIZ_RETRY):
        try:
            result = _sq_r_req.sq_r_ca(body)
            if asyncio.iscoroutine(result):
                result = await result
            ok, data, msg, terminal = _hb_parts(result)
            if ok:
                break
            last_hb = msg
            if terminal:
                break
        except Exception as exc:
            last_hb = exc
            print(sec("rw_net_fail_02"), exc)
        if attempt + 1 < _CA_BIZ_RETRY:
            try:
                await asyncio.sleep(_sq_r_req._R_RETRY_DELAY_SEC)
            except Exception:
                pass
    if data is None:
        print(sec("rw_hb_bad_03"), last_hb)
        return None
    ordered = data.get("data", data) if isinstance(data, dict) else data
    if not isinstance(ordered, list):
        ordered = [ordered] if ordered is not None else []
    try:
        q_m3_seal(ordered)
    except Exception:
        pass
    try:
        sign_batch = data.get("sign_batch", "") if isinstance(data, dict) else ""
        if sign_batch:
            for item in ordered:
                if isinstance(item, dict):
                    item.setdefault("sign_batch", sign_batch)
                else:
                    setattr(item, "sign_batch", sign_batch)
        for item in ordered:
            if isinstance(item, dict) and "kid" in item:
                item["kid"] = str(item["kid"]).encode("utf-8")
    except Exception:
        pass
    return ordered
