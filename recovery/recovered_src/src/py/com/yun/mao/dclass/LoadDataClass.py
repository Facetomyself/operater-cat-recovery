# Recovered module: src.py.com.yun.mao.dclass.LoadDataClass
# Persistent item/flow model loader and mutation facade.
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from . import ItemMemStore
from .DTopClass import (
    AdWrapper,
    AutoBean,
    DTopClass,
    Water,
)


try:
    from ..config import YunYinMaoConfig

    _base_dir = Path(YunYinMaoConfig.abs_cache_dir)
except Exception:
    _base_dir = Path.home() / "YunYinData"

DataClassFile = _base_dir / "yun_yin_item_data"
dTopClass: Optional[DTopClass] = None


def _json_default(value):
    if hasattr(value, "__dict__"):
        return dict(value.__dict__)
    return str(value)


def _dict_to_auto(value):
    if isinstance(value, AutoBean):
        return value
    if not isinstance(value, dict):
        return AutoBean()
    from .DTopClassHelper import dic_to_Auto_obj

    fields = dict(value)
    fields.pop("__class__", None)
    return dic_to_Auto_obj(fields)


def loadDTopClass(dict_of_dicts: Optional[dict] = None) -> DTopClass:
    global dTopClass
    if dict_of_dicts is None:
        dict_of_dicts = {
            "scheduler": None,
            "autoMap": {},
            "globalAdWrapper": {},
            "water": None,
        }
    auto_map = {
        str(kid): _dict_to_auto(value)
        for kid, value in (dict_of_dicts.get("autoMap") or {}).items()
    }
    global_ad = dict_of_dicts.get("globalAdWrapper") or {}
    try:
        global_ad_wrapper = (
            global_ad
            if isinstance(global_ad, AdWrapper)
            else AdWrapper(**global_ad)
        )
    except Exception:
        global_ad_wrapper = AdWrapper()
    water = dict_of_dicts.get("water")
    try:
        water_obj = water if isinstance(water, Water) or water is None else Water(**water)
    except Exception:
        water_obj = None
    dTopClass = DTopClass(
        scheduler=dict_of_dicts.get("scheduler"),
        autoMap=auto_map,
        globalAdWrapper=global_ad_wrapper,
        water=water_obj,
    )
    return dTopClass


def _ensure_loaded() -> DTopClass:
    if dTopClass is None:
        return loadDTopClass()
    return dTopClass


def _snapshot_dict() -> dict:
    obj = _ensure_loaded()
    return {
        "scheduler": obj.scheduler,
        "autoMap": obj.autoMap,
        "globalAdWrapper": obj.globalAdWrapper,
        "water": obj.water,
    }


def _write_snapshot(obj: dict) -> None:
    DataClassFile.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, default=_json_default)
    DataClassFile.write_text(text, encoding="utf-8")
    ItemMemStore.mark_item_dirty()


def writeToDist_legacy_disk() -> None:
    _write_snapshot(_snapshot_dict())


def writeToDist() -> None:
    _write_snapshot(_snapshot_dict())


def getAutoMap() -> dict:
    return _ensure_loaded().autoMap


def getScheduler():
    return _ensure_loaded().scheduler


def getGlobalAd():
    return _ensure_loaded().globalAdWrapper


def updateSchedulerAndGlobalAd(scheduler=None, global_ad=None) -> None:
    obj = _ensure_loaded()
    if scheduler is not None:
        obj.scheduler = scheduler
    if global_ad is not None:
        obj.globalAdWrapper = global_ad
    writeToDist()


def addOrUpdate(bean: AutoBean) -> None:
    obj = _ensure_loaded()
    obj.autoMap[str(bean.kid)] = bean
    writeToDist()


def deleteAutoBean(kid: str) -> None:
    obj = _ensure_loaded()
    obj.autoMap.pop(str(kid), None)
    writeToDist()


def changedAllActiveStatus(active: bool) -> None:
    obj = _ensure_loaded()
    for bean in obj.autoMap.values():
        bean.active = bool(active)
    writeToDist()


def deleteGAd(adId: str) -> None:
    obj = _ensure_loaded()
    obj.globalAdWrapper.ades = [
        ad for ad in obj.globalAdWrapper.ades
        if str(getattr(ad, "adId", getattr(ad, "ad_id", ""))) != str(adId)
    ]
    writeToDist()


def updateGlobalAd(ad) -> None:
    obj = _ensure_loaded()
    ad_id = str(getattr(ad, "adId", getattr(ad, "ad_id", "")))
    obj.globalAdWrapper.ades = [
        ad if str(getattr(item, "adId", "")) == ad_id else item
        for item in obj.globalAdWrapper.ades
    ]
    writeToDist()


def addGlobalAd(ad) -> None:
    obj = _ensure_loaded()
    obj.globalAdWrapper.ades.append(ad)
    writeToDist()


def updateWater(water) -> None:
    obj = _ensure_loaded()
    obj.water = water
    writeToDist()


def getAutoBeanById(kid: str):
    return _ensure_loaded().autoMap.get(str(kid))
