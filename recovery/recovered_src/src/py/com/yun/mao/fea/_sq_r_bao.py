# Recovered module: src.py.com.yun.mao.fea._sq_r_bao
# Request-payload helpers reconstructed from the function signatures and
# constant names. The JSON field names are exact; formatting details remain
# behavioural reconstruction.
from __future__ import annotations

import base64
import hashlib
import json


def _escape_json_str(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _convert_payload_json(mode: str, items: list) -> str:
    return json.dumps(
        {"mode": mode, "items": items},
        ensure_ascii=False,
        separators=(",", ":"),
    )


def hash_item_b64(item_b64: str) -> str:
    """Hash an item after base64 decoding it when possible."""
    try:
        raw = base64.b64decode(item_b64)
    except Exception:
        raw = item_b64.encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _remote_payload_json(
    instance_id: str,
    item_b64: str,
    item_encoding: str,
    item_hash: str,
    cfg_ver: int,
) -> str:
    return json.dumps(
        {
            "instance_id": instance_id,
            "item_b64": item_b64,
            "item_encoding": item_encoding,
            "item_hash": item_hash,
            "cfg_ver": cfg_ver,
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )


def zq_r_convert_hb(uCode: str, mode: str, items: list) -> str:
    return json.dumps(
        {"uCode": uCode, "mode": mode, "items": items},
        ensure_ascii=False,
        separators=(",", ":"),
    )


def zq_r_item_hb(
    uCode: str,
    item_b64: str = "",
    include_item: bool = False,
    cfg_ver: int = 0,
    iid: str = "",
    b64: str | None = None,
    enc: str | None = None,
    ih: str | None = None,
) -> str:
    item_hash = ih or hash_item_b64(item_b64)
    payload = {
        "uCode": uCode,
        "instance_id": iid,
        "cfg_ver": cfg_ver,
        "item_hash": item_hash,
    }
    if include_item:
        payload["item_b64"] = b64 or item_b64
        payload["item_encoding"] = enc or "base64"
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
