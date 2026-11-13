# Recovered module: src.py.com.yun.mao.remember.RememberManager
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ..util.need import utils


REMEMBER_MAP_INFO_KEY = b"GveTnVHwS3w7Q6P940ObjtGXRi91yVhSDD0LV_R9haI="
rememberMap: dict[str, list[int]] = {}


def _remember_file() -> Path:
    try:
        from ..config import YunYinMaoConfig

        base = Path(YunYinMaoConfig.abs_cache_dir)
    except Exception:
        base = Path.home() / "YunYinData"
    return base / "rememberMap" / "rememberMap.json"


def _genRememberKey(source: str, destes) -> str:
    text = str(source or "") + "|".join(str(dest) for dest in (destes or []))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def loadRememberMap() -> dict:
    global rememberMap
    path = _remember_file()
    try:
        if path.exists():
            payload = path.read_bytes().strip()
            decrypt = getattr(utils, "decrypt", None)
            if callable(decrypt) and REMEMBER_MAP_INFO_KEY:
                payload = decrypt(REMEMBER_MAP_INFO_KEY, payload)
            if isinstance(payload, bytes):
                payload = payload.decode("utf-8")
            data = json.loads(payload)
            if isinstance(data, dict):
                rememberMap = data
    except Exception:
        pass
    return rememberMap


def getIds(source: str, destes) -> list[int]:
    key = _genRememberKey(source, destes)
    return list(rememberMap.get(key, []))


def updateRememberIds(source: str, destes, ids) -> None:
    key = _genRememberKey(source, destes)
    old_ids = list(rememberMap.get(key, []))
    old_ids.extend(int(value) for value in (ids or []))
    rememberMap[key] = old_ids
    writeToDist()


def cleanRememberIds() -> None:
    rememberMap.clear()
    writeToDist()


def writeToDist() -> None:
    path = _remember_file()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        init_folder = getattr(utils, "init_folder", None)
        if callable(init_folder):
            init_folder(str(path.parent))
        payload = json.dumps(
            rememberMap,
            ensure_ascii=False,
            default=str,
        )
        encrypt = getattr(utils, "encrypt", None)
        if callable(encrypt) and REMEMBER_MAP_INFO_KEY:
            payload = encrypt(REMEMBER_MAP_INFO_KEY, payload)
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        path.write_bytes(payload)
    except Exception:
        pass
