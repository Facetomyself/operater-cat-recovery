# Recovered module: src.py.com.yun.mao.dclass.ExecCandidateHelper
from __future__ import annotations

import hashlib
import json
import unicodedata
from typing import Any, Dict, List, Tuple

from .DTopClass import AutoBean


_WIRE_ASCII = True
_WIRE_SEP = (",", ":")
_CFG_VER = 701


def _normalize_unicode(obj):
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, dict):
        return {_normalize_unicode(k): _normalize_unicode(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_normalize_unicode(item) for item in obj]
    return obj


def _normalize_numbers(obj):
    if isinstance(obj, dict):
        return {key: _normalize_numbers(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [_normalize_numbers(value) for value in obj]
    if isinstance(obj, float) and obj.is_integer():
        return int(obj)
    return obj


def _serialize_bean_like(value) -> dict:
    if isinstance(value, AutoBean):
        data = dict(value.__dict__)
        data.pop("dtype_value", None)
        return _normalize_numbers(_normalize_unicode(data))
    if hasattr(value, "__dict__"):
        return _normalize_numbers(_normalize_unicode(dict(value.__dict__)))
    if isinstance(value, dict):
        return _normalize_numbers(_normalize_unicode(value))
    raise TypeError("exec_candidate 必须为 object")


def canonical_json_bytes(obj) -> bytes:
    return json.dumps(
        _normalize_numbers(_normalize_unicode(obj)),
        sort_keys=True,
        separators=_WIRE_SEP,
        ensure_ascii=_WIRE_ASCII,
        default=str,
    ).encode("utf-8")


def freeze_exec_candidate(exec_candidate: dict) -> str:
    return hashlib.sha256(canonical_json_bytes(exec_candidate)).hexdigest()


def compute_af(raw) -> Tuple[dict, str]:
    data = _serialize_bean_like(raw)
    frozen = freeze_exec_candidate(data)
    data.setdefault("af", frozen)
    return data, frozen


def _finalize_convert_item(item: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(item)
    result.setdefault("cfg_ver", _CFG_VER)
    return result


def build_convert_item(auto: AutoBean) -> dict:
    if not auto.beanLike if hasattr(auto, "beanLike") else False:
        pass
    exec_candidate, af = compute_af(auto)
    return _finalize_convert_item(
        {
            "kid": str(getattr(auto, "kid", "")),
            "auto_type": getattr(auto, "auto_type", 0),
            "exec_candidate": exec_candidate,
            "af": af,
        }
    )


def build_convert_items(beans: List[AutoBean]) -> List[Dict[str, Any]]:
    return [build_convert_item(auto) for auto in beans or []]
