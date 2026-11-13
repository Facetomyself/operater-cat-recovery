# Recovered module: src.py.com.yun.mao.dclass.ItemMemStore
# In-memory item/flow snapshot used by the remote sync protocol.
from __future__ import annotations

import base64
import gzip
import json
from pathlib import Path
from typing import Optional


_item_dirty = False
_dirty_generation = 0
_bootstrapped = False
_last_synced_snapshot: Optional[dict] = None
_snapshot: Optional[dict] = None


def _empty_snapshot_dict() -> dict:
    return {
        "scheduler": None,
        "autoMap": {},
        "globalAdWrapper": {
            "adEnable": False,
            "adIsBottomUp": False,
            "delete": False,
            "ades": [],
        },
        "water": None,
    }


def _default_path() -> Path:
    try:
        from ..config import YunYinMaoConfig

        base = Path(YunYinMaoConfig.abs_cache_dir)
    except Exception:
        base = Path.home() / "YunYinData"
    return base / "yun_yin_item_data"


def local_item_path() -> Path:
    try:
        from . import LoadDataClass

        return Path(LoadDataClass.DataClassFile)
    except Exception:
        return _default_path()


def local_item_file_exists() -> bool:
    try:
        return local_item_path().is_file()
    except Exception:
        return False


def delete_local_item_file() -> None:
    try:
        path = local_item_path()
        if path.exists():
            path.unlink()
    except Exception:
        pass


def dump_snapshot() -> dict:
    if _snapshot is None:
        return _empty_snapshot_dict()
    return json.loads(json.dumps(_snapshot, ensure_ascii=False, default=str))


def dump_snapshot_json() -> str:
    return json.dumps(dump_snapshot(), ensure_ascii=False, default=str)


def dump_snapshot_gzip_b64() -> str:
    raw = dump_snapshot_json().encode("utf-8")
    packed = gzip.compress(raw, compresslevel=6)
    return base64.b64encode(packed).decode("ascii")


def apply_snapshot(dict_of_dicts: dict, dirty: bool = False) -> None:
    global _snapshot, _item_dirty
    _snapshot = dict_of_dicts or _empty_snapshot_dict()
    _item_dirty = bool(dirty)


def _remember_sync_baseline() -> None:
    global _last_synced_snapshot
    _last_synced_snapshot = dump_snapshot()


def _dict_to_dtop(dict_of_dicts: dict):
    try:
        from .LoadDataClass import loadDTopClass

        return loadDTopClass(dict_of_dicts)
    except Exception:
        from .DTopClass import DTopClass

        return DTopClass(
            scheduler=dict_of_dicts.get("scheduler"),
            autoMap=dict_of_dicts.get("autoMap", {}),
            water=dict_of_dicts.get("water"),
        )


def decode_cloud_item_payload(
    empty: bool,
    encoding: str,
    payload_b64: str,
) -> Optional[dict]:
    if empty or not payload_b64:
        return None
    try:
        raw = base64.b64decode(payload_b64)
        if encoding == "gzip":
            raw = gzip.decompress(raw)
        text = raw.decode("utf-8")
        data = json.loads(text)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def read_local_snapshot_dict() -> Optional[dict]:
    try:
        dpath = local_item_path()
        if not dpath.is_file():
            return None
        with dpath.open("rb") as file:
            line = file.readline().strip()
        if not line:
            return None
        # The persisted format is base64(gzip(JSON)); tolerate plain JSON.
        try:
            raw = gzip.decompress(base64.b64decode(line))
        except Exception:
            raw = line
        data = json.loads(raw.decode("utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def is_item_dirty() -> bool:
    return bool(_item_dirty)


def mark_item_dirty() -> None:
    global _item_dirty, _dirty_generation
    _item_dirty = True
    _dirty_generation += 1


def get_dirty_generation() -> int:
    return int(_dirty_generation)


def clear_item_dirty_if_generation(generation: int) -> bool:
    global _item_dirty
    if int(generation) != int(_dirty_generation):
        return False
    _item_dirty = False
    _remember_sync_baseline()
    return True


def clear_item_dirty() -> None:
    clear_item_dirty_if_generation(_dirty_generation)


def discard_unsynced_changes() -> None:
    global _snapshot
    _snapshot = (
        json.loads(json.dumps(_last_synced_snapshot, ensure_ascii=False))
        if _last_synced_snapshot is not None
        else _empty_snapshot_dict()
    )
    clear_item_dirty()


def is_bootstrapped() -> bool:
    return bool(_bootstrapped)


def reset_bootstrap_flag_for_tests() -> None:
    global _bootstrapped
    _bootstrapped = False


def set_migration_discard_baseline_empty() -> None:
    global _last_synced_snapshot
    _last_synced_snapshot = _empty_snapshot_dict()


def bootstrap_item_memory(
    is_register: bool,
    cloud_empty: bool,
    cloud_encoding: str,
    cloud_payload_b64: str,
) -> str:
    """Reconcile cloud and local snapshots during boot/register."""
    global _bootstrapped, _snapshot, _item_dirty
    cloud_dict = decode_cloud_item_payload(
        cloud_empty,
        cloud_encoding,
        cloud_payload_b64,
    )
    local_dict = read_local_snapshot_dict()
    branch = ""
    if cloud_dict is not None:
        apply_snapshot(cloud_dict, dirty=False)
        branch = "cloud_hit"
    elif local_dict is not None:
        apply_snapshot(local_dict, dirty=False)
        branch = "cloud_empty_local_hit"
    else:
        apply_snapshot(_empty_snapshot_dict(), dirty=bool(is_register))
        branch = "cloud_empty_no_local"
    if is_register:
        delete_local_item_file()
    _bootstrapped = True
    _ = _snapshot
    return branch


def ensure_main_window_item_memory() -> bool:
    if _bootstrapped:
        return True
    branch = bootstrap_item_memory(
        False,
        True,
        "gzip",
        "",
    )
    return branch in (
        "cloud_hit",
        "cloud_empty_local_hit",
        "cloud_empty_no_local",
    )
