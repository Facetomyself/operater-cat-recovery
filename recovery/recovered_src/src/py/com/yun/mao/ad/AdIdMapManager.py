# Recovered module: src.py.com.yun.mao.ad.AdIdMapManager
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

import json
from pathlib import Path

from ..config import YunYinMaoConfig
from ..util import TracePrinterHelper
from ..util.need import utils


# Recovered from the module's bytes constant.
ADMAP_INFO_KEY = b"GveTnVHwS3w7Q6P940ObjtGXRi91yVhSDD0LV_R9haI="
AdIdMapFile = "adIdMap"

adIdMap: dict[str, list] = {}


def _ad_id_map_path() -> Path:
    path = Path(YunYinMaoConfig.abs_cache_dir()) / AdIdMapFile
    if path.is_dir():
        path = path / "adIdMap.json"
    return path


def _decrypt_payload(payload):
    decrypt = getattr(utils, "decrypt", None)
    if callable(decrypt) and ADMAP_INFO_KEY:
        return decrypt(ADMAP_INFO_KEY, payload)
    return payload


def _encrypt_payload(payload: str) -> bytes:
    encrypt = getattr(utils, "encrypt", None)
    if callable(encrypt) and ADMAP_INFO_KEY:
        payload = encrypt(ADMAP_INFO_KEY, payload)
    if isinstance(payload, bytes):
        return payload
    return str(payload).encode("utf-8")


def loadAdIdMap() -> dict[str, list]:
    global adIdMap
    file_path = _ad_id_map_path()
    if not file_path.exists():
        return adIdMap
    try:
        with open(file_path, "rb") as file:
            line = file.readline()
            if not line:
                return adIdMap
            txt = line.strip()
            payload = _decrypt_payload(txt)
            if isinstance(payload, bytes):
                payload = payload.decode("utf-8")
            decoded = json.loads(payload)
            if isinstance(decoded, dict):
                adIdMap = decoded
    except Exception:
        TracePrinterHelper.print_trace()
    return adIdMap


def genAdKey(kid, adId, dest) -> str:
    return str(kid) + str(adId) + str(dest)


def getIds(adkey) -> list:
    return list(adIdMap.get(adkey, []))


def updateAdIds(adkey, ids) -> list:
    existing_ids = set(adIdMap.get(adkey, []))
    combined_ids = list(adIdMap.get(adkey, []))
    for value in ids or []:
        if value not in existing_ids:
            existing_ids.add(value)
            combined_ids.append(value)
    adIdMap[adkey] = combined_ids
    writeToDist()
    return combined_ids


def writeToDist() -> None:
    try:
        file_path = _ad_id_map_path()
        utils.init_folder(str(file_path.parent))
        json_string = json.dumps(
            adIdMap,
            ensure_ascii=False,
            default=lambda o: o.__dict__,
        )
        with open(file_path, "wb") as file:
            file.write(_encrypt_payload(json_string))
    except Exception:
        TracePrinterHelper.print_trace()
