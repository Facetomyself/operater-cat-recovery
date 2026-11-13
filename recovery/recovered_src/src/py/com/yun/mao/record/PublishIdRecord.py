# Recovered module: src.py.com.yun.mao.record.PublishIdRecord
# Publish-id mapper records, stored as JSONL volumes plus meta.json.
from __future__ import annotations

import copy
import json
import os
import queue
import re
import threading
import time
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
)

from ..config.NewConfig import (
    MAIN_MODEL_DING_SHI_TEXT,
    MAIN_MODEL_MONITOR_TEXT,
)
from ..dclass.DTopClass import (
    AUTO_BEAN_TYPE_AUTO_FLOW,
    AUTO_BEAN_TYPE_BAN_YUN,
    AUTO_BEAN_TYPE_DOWN_LOAD_FLOW,
    AUTO_BEAN_TYPE_YUN_AUTO,
    AUTO_BEAN_TYPE_YUN_PRE_VIEW,
    AUTO_BEAN_TYPE_YU_LAN_FLOW,
)
from ..util.need import utils


MODE_MONITOR = "monitor"
MODE_TIMING = "timing"
PUBLISH_SUCCESS_LOG_PREFIX = "发布成功，资源链接： "
VOLUME_NAME_RE = re.compile(r"^data-(\d+)\.jsonl$")
_TAIL_SCAN_BYTES = 65536
META_WRITE_ATTEMPTS = 3
TYPE_BY_AUTO = {
    AUTO_BEAN_TYPE_BAN_YUN: "搬运流",
    AUTO_BEAN_TYPE_AUTO_FLOW: "自动流",
    AUTO_BEAN_TYPE_YU_LAN_FLOW: "预览流",
    AUTO_BEAN_TYPE_DOWN_LOAD_FLOW: "下载流",
    AUTO_BEAN_TYPE_YUN_AUTO: "云自动",
    AUTO_BEAN_TYPE_YUN_PRE_VIEW: "云预览",
}
_PREVIEW_FIELD_TYPES = frozenset({"云预览", "预览流"})
_DEST_FROM_PREVIEW_MAP_TYPES = frozenset({"云预览", "预览流"})
RECORD_DIR_NAME = "main_record"
META_FILE_NAME = "meta.json"
VOLUME_MAX_BYTES = 32 * 1024 * 1024
RECORD_RETENTION_MAX_BYTES = 3 * 1024 * 1024 * 1024

_record_dir_override: Optional[str] = None
_entries: Dict[str, dict] = {}
_meta_cache: dict = {"active": 1, "items": []}
_write_backend = None
_cache_lock = threading.Lock()
_write_queue: "queue.Queue[Optional[dict]]" = queue.Queue()
_writer_started = False
_writer_thread: Optional[threading.Thread] = None
WriteJob = Dict[str, Any]
WriteBackend = Callable[[WriteJob], None]


def _base_dir() -> Path:
    if _record_dir_override:
        return Path(_record_dir_override)
    try:
        from ..config import YunYinMaoConfig

        return Path(YunYinMaoConfig.abs_cache_only_multi_dir) / RECORD_DIR_NAME
    except Exception:
        return Path.home() / "YunYinData" / RECORD_DIR_NAME


def record_dir(folder: Optional[str] = None) -> str:
    if folder:
        return str(folder)
    return str(_base_dir())


def meta_json_path() -> str:
    return str(_base_dir() / META_FILE_NAME)


def volume_path(index: int) -> str:
    return str(_base_dir() / volume_file_name(index))


def volume_file_name(index: int) -> str:
    return f"data-{int(index):04d}.jsonl"


def _list_volume_files(folder: str) -> List[Tuple[int, str, int]]:
    root = Path(folder)
    out: List[Tuple[int, str, int]] = []
    try:
        for path in root.iterdir():
            match = VOLUME_NAME_RE.match(path.name)
            if not match or not path.is_file():
                continue
            out.append((int(match.group(1)), str(path), path.stat().st_size))
    except OSError:
        return []
    out.sort(key=lambda item: item[0])
    return out


def _max_volume_index(folder: str) -> int:
    files = _list_volume_files(folder)
    return max((item[0] for item in files), default=0)


def _read_meta_file(folder: str) -> dict:
    path = Path(folder) / META_FILE_NAME
    try:
        if not path.exists():
            return {"active": 1, "items": []}
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"active": 1, "items": []}
        data.setdefault("active", 1)
        data.setdefault("items", [])
        return data
    except Exception:
        return {"active": 1, "items": []}


def _write_meta_file_once(folder: str, meta: dict) -> None:
    root = Path(folder)
    root.mkdir(parents=True, exist_ok=True)
    path = root / META_FILE_NAME
    tmp = root / (META_FILE_NAME + f".{os.getpid()}.{threading.get_ident()}.tmp")
    text = json.dumps(meta, ensure_ascii=False, indent=2)
    with tmp.open("w", encoding="utf-8", newline="\n") as file:
        file.write(text)
        file.flush()
        os.fsync(file.fileno())
    os.replace(tmp, path)


def _write_meta_file(folder: str, meta: dict) -> None:
    last_error = None
    for _ in range(META_WRITE_ATTEMPTS):
        try:
            _write_meta_file_once(folder, meta)
            return
        except Exception as exc:
            last_error = exc
            time.sleep(0.02)
    if last_error is not None:
        raise last_error


def _upsert_meta_item(meta: dict, kid: str, name: str, type_text: str) -> None:
    items = meta.setdefault("items", [])
    for item in items:
        if str(item.get("kid", "")) == str(kid):
            item.update(
                {
                    "kid": str(kid),
                    "name": str(name),
                    "type": str(type_text),
                }
            )
            return
    items.append({"kid": str(kid), "name": str(name), "type": str(type_text)})


def _reconcile_active(folder: str, meta: dict) -> None:
    max_idx = _max_volume_index(folder)
    try:
        active = int(meta.get("active", 1) or 1)
    except (TypeError, ValueError):
        active = 1
    meta["active"] = max(active, max_idx + (0 if max_idx else 1))


def _ensure_disk_meta(folder: str) -> dict:
    meta = _read_meta_file(folder)
    _reconcile_active(folder, meta)
    return meta


def _volume_has_incomplete_tail(path: str) -> bool:
    file_path = Path(path)
    if not file_path.exists() or file_path.stat().st_size <= 0:
        return False
    try:
        with file_path.open("rb") as file:
            file.seek(max(0, file_path.stat().st_size - _TAIL_SCAN_BYTES))
            chunk = file.read()
    except OSError:
        return False
    if not chunk or chunk.endswith(b"\n"):
        return False
    stripped = chunk.rstrip()
    if not stripped:
        return False
    last = stripped.rsplit(b"\n", 1)[-1]
    try:
        json.loads(last.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return True
    return False


def _append_bytes(path: str, payload: bytes) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = b"" if not _volume_has_incomplete_tail(path) else b"\n"
    with file_path.open("ab") as file:
        file.write(prefix + payload)
        file.flush()
        os.fsync(file.fileno())


def _apply_retention(folder: str, meta: dict) -> None:
    files = _list_volume_files(folder)
    total = sum(item[2] for item in files)
    try:
        active = int(meta.get("active", 1) or 1)
    except (TypeError, ValueError):
        active = 1
    for index, path, size in files:
        if total <= RECORD_RETENTION_MAX_BYTES:
            break
        if index == active:
            continue
        try:
            Path(path).unlink()
            total -= size
        except OSError:
            continue


def type_text_of(auto_type: int) -> Optional[str]:
    return TYPE_BY_AUTO.get(int(auto_type or 0))


def mode_text_of(convert_mode: Optional[str]) -> str:
    text = str(convert_mode or "").strip().lower()
    if text == MODE_MONITOR:
        return MAIN_MODEL_MONITOR_TEXT
    return MAIN_MODEL_DING_SHI_TEXT


def build_message_link(config: str, msg_id: int) -> Optional[str]:
    return build_sent_message_link(config, msg_id)


def _positive_int(value: Any) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return 0
    return number if number > 0 else 0


def _public_username(channel: str) -> str:
    text = str(channel or "").strip()
    if text.startswith("@"):
        return text[1:]
    prefix = "https://t.me/"
    if text.startswith(prefix):
        return text[len(prefix) :].split("/", 1)[0]
    return text


def _private_channel_id(channel: str) -> str:
    text = str(channel or "").strip()
    prefix = "https://t.me/c/"
    if text.startswith(prefix):
        text = text[len(prefix) :].split("/", 1)[0]
    text = text.lstrip("+-")
    if text.startswith("100"):
        text = text[3:]
    return text


def _channel_key(channel: str) -> str:
    text = str(channel or "").strip()
    if not text:
        return ""
    if text.startswith("https://t.me/c/") or text.lstrip("+-").isdigit():
        return _private_channel_id(text)
    return _public_username(text).lstrip("@").lower()


def _as_str_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)]


def _as_id_list(value: Any) -> List[int]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [number for item in value if (number := _positive_int(item))]
    number = _positive_int(value)
    return [number] if number else []


def lookup_ids(cfg: str, id_map: Optional[Dict[str, Any]]) -> List[int]:
    if not cfg or not id_map:
        return []
    key = _channel_key(cfg)
    value = None
    if cfg in id_map:
        value = id_map.get(cfg)
    elif key:
        for raw_key, raw_value in id_map.items():
            if _channel_key(str(raw_key)) == key:
                value = raw_value
                break
    return _as_id_list(value)


def first_sent_msg_id(sent_or_ids: Any) -> Optional[int]:
    ids = _as_id_list(sent_or_ids)
    return ids[0] if ids else None


def _build_link_list(
    cfgs: Sequence[str],
    id_map: Optional[Dict[str, Any]],
) -> Optional[List[str]]:
    links: List[str] = []
    for cfg in cfgs or []:
        ids = lookup_ids(cfg, id_map)
        if not ids:
            return None
        channel, _topic = _cfg_channel(cfg)
        for msg_id in ids:
            link = build_sent_message_link(channel, msg_id)
            if not link:
                return None
            links.append(link)
    return links


def maps_for_type(
    type_text: str,
    dest_id_map: Optional[Dict[str, Any]],
    preview_id_map: Optional[Dict[str, Any]],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    dest = dict(dest_id_map or {})
    preview = dict(preview_id_map or {})
    if type_text in {"云预览", "预览流"}:
        return preview, dest
    return dest, preview


def _sent_message_ids(sent: Any) -> List[int]:
    if sent is None:
        return []
    items = sent if isinstance(sent, (list, tuple, set)) else [sent]
    ids: List[int] = []
    for item in items:
        msg_id = getattr(item, "id", item)
        number = _positive_int(msg_id)
        if number:
            ids.append(number)
    return ids


def log_publish_success(*args, **kwargs) -> Optional[str]:
    if len(args) >= 4:
        target, comment_to_id, sent, album_size = args[:4]
        msg_id = None
    else:
        target = kwargs.get("target", args[0] if args else None)
        msg_id = kwargs.get(
            "msg_id",
            args[1] if len(args) > 1 else None,
        )
        comment_to_id = kwargs.get("comment_to_id")
        sent = kwargs.get("sent")
        album_size = kwargs.get("album_size", 0)
    _ = album_size
    channel = (
        getattr(target, "channel_key", None)
        or getattr(target, "username", None)
        or target
    )
    ids = ([_positive_int(msg_id)] if msg_id is not None else [])
    ids = [value for value in ids if value]
    if not ids:
        ids = _sent_message_ids(sent)
    last_link = None
    for message_id in ids:
        link = (
            build_comment_message_link(
                str(channel or ""),
                message_id,
                None,
                _positive_int(comment_to_id) or None,
            )
            if comment_to_id
            else build_message_link(str(channel or ""), message_id)
        )
        if link:
            print(PUBLISH_SUCCESS_LOG_PREFIX + link)
            last_link = link
    return last_link


def build_comment_message_link(
    channel: str,
    msg_id: int,
    topic_id: Optional[int] = None,
    comment_to_id: Optional[int] = None,
) -> Optional[str]:
    base = _compose_tme_link(channel, msg_id, topic_id, None)
    if not base:
        return None
    if comment_to_id:
        return base + "?single&comment=" + str(comment_to_id)
    return base


def build_sent_message_link(
    channel: str,
    msg_id: int,
    topic_id: Optional[int] = None,
    comment_to_id: Optional[int] = None,
) -> Optional[str]:
    return _compose_tme_link(channel, msg_id, topic_id, comment_to_id)


def _compose_tme_link(
    channel: str,
    msg_id: int,
    topic_id: Optional[int] = None,
    comment_to_id: Optional[int] = None,
) -> Optional[str]:
    text = str(channel or "").strip()
    mid = int(msg_id or 0)
    if not text or mid <= 0:
        return None
    if text.startswith("https://t.me/c/") or text.lstrip("+-").isdigit():
        base = "https://t.me/c/" + _private_channel_id(text)
    elif text.lstrip("-").isdigit():
        value = text.lstrip("-")
        if value.startswith("100"):
            value = value[3:]
        base = "https://t.me/c/" + value
    else:
        base = "https://t.me/" + _public_username(text)
    if topic_id:
        base += "/" + str(topic_id)
    base += "/" + str(mid)
    if comment_to_id:
        base += "?comment=" + str(comment_to_id)
    return base


def parse_tme_message_link(link: str) -> Tuple[Optional[str], Optional[int]]:
    text = str(link or "").strip()
    private_match = re.match(r"^https://t\.me/c/(\d+)/(\d+)", text)
    if private_match:
        return "-100" + private_match.group(1), int(private_match.group(2))
    public_match = re.match(r"^https://t\.me/([A-Za-z0-9_]+)/(\d+)", text)
    if public_match:
        return public_match.group(1), int(public_match.group(2))
    return None, None


def _cfg_channel(cfg: str) -> Tuple[str, Optional[int]]:
    source, topic = utils.parse_source_parts(str(cfg or ""))
    try:
        return source or "", int(topic) if topic else None
    except Exception:
        return source or "", None


def _source_first_id(parse) -> int:
    messages = getattr(parse, "messages", None) or []
    if messages:
        first_id = _positive_int(getattr(messages[0], "id", 0))
        if first_id:
            return first_id
    original_ids = getattr(parse, "original_msg_ids", None) or []
    for value in original_ids:
        first_id = _positive_int(value)
        if first_id:
            return first_id
    return 0


def resolve_record_lists(
    auto,
    parse=None,
) -> Tuple[str, List[str], List[str]]:
    try:
        auto_type = int(getattr(auto, "auto_type", 0) or 0)
        type_text = type_text_of(auto_type) or ""
        dest_cfgs = list(
            auto.getDestes()
            if hasattr(auto, "getDestes")
            else getattr(auto, "destes", [])
            or []
        )
        preview_cfgs = list(
            auto.getYulanDestes()
            if hasattr(auto, "getYulanDestes")
            else getattr(auto, "yulan_destes", [])
            or []
        )
        return type_text, dest_cfgs, preview_cfgs
    except Exception:
        return "", [], []


def _append_if_complete_inner(auto, parse, group_result, convert_mode=None) -> None:
    try:
        type_text, dest_cfgs, preview_cfgs = resolve_record_lists(auto, parse)
        dest_id_map = getattr(group_result, "dest_id_map", None) or {}
        preview_id_map = getattr(group_result, "preview_id_map", None) or {}
        dest_lookup, preview_lookup = maps_for_type(
            type_text,
            dest_id_map,
            preview_id_map,
        )
        if not dest_cfgs and not preview_cfgs:
            return
        if dest_cfgs and not is_cfg_list_complete(dest_cfgs, dest_lookup):
            return
        if (
            type_text in _PREVIEW_FIELD_TYPES
            and preview_cfgs
            and not is_cfg_list_complete(preview_cfgs, preview_lookup)
        ):
            return

        source_cfg = ""
        source_getter = getattr(auto, "getSource", None)
        if callable(source_getter):
            source_cfg = str(source_getter() or "")
        source_first_id = _source_first_id(parse)
        source_link = (
            build_message_link(source_cfg, source_first_id)
            if source_cfg and source_first_id
            else None
        )
        dest_links = _build_link_list(dest_cfgs, dest_lookup) or []
        preview_links = _build_link_list(preview_cfgs, preview_lookup) or []
        mapper_item = {
            "time": utils.get_format_time(),
            "mode": mode_text_of(convert_mode),
            "source": source_link or "",
            "dest": dest_links,
        }
        if type_text in _PREVIEW_FIELD_TYPES:
            mapper_item["preview"] = preview_links

        kid = str(getattr(auto, "kid", "") or "").strip()
        get_name = getattr(auto, "getName", None)
        name_value = get_name() if callable(get_name) else getattr(auto, "name", "")
        name = str(name_value or "").strip()
        _commit_mapper_item(kid, name, type_text, mapper_item)
    except Exception:
        print("记录发布 ID 映射失败：")
        _safe_print_trace()


def append_if_complete(auto, parse, group_result, convert_mode=None) -> None:
    _append_if_complete_inner(auto, parse, group_result, convert_mode)


def is_cfg_list_complete(cfgs: Sequence[str], id_map: Optional[Dict[str, Any]]) -> bool:
    if not cfgs:
        return False
    return all(bool(lookup_ids(cfg, id_map)) for cfg in cfgs)


def _commit_mapper_item(
    kid: str,
    name: str,
    type_text: str,
    mapper_item: dict,
) -> None:
    mapper_copy = copy.deepcopy(mapper_item)
    entry = {
        "kid": str(kid),
        "name": str(name),
        "type": str(type_text),
        "mapper_item": mapper_copy,
    }
    with _cache_lock:
        _entries[str(kid)] = entry
        _upsert_meta_item(_meta_cache, kid, name, type_text)
        meta = copy.deepcopy(_meta_cache)
    _schedule_write(
        {
            "folder": record_dir(),
            "meta": meta,
            "kid": str(kid),
            "name": str(name),
            "type_text": str(type_text),
            "mapper_item": mapper_copy,
            "entry": copy.deepcopy(entry),
        }
    )


def _persist_entries() -> None:
    try:
        with _cache_lock:
            meta = copy.deepcopy(_meta_cache)
        _write_meta_file(record_dir(), meta)
    except Exception:
        _safe_print_trace("写入发布 ID meta 失败：")


def _safe_print_trace(prefix: str) -> None:
    try:
        from ..util import TracePrinterHelper

        TracePrinterHelper.print_trace()
    except Exception:
        print(prefix)


def iter_mapper_lines(folder: Optional[str] = None) -> Iterator[dict]:
    root = Path(record_dir(folder))
    if not root.exists():
        return iter(())
    def _iter():
        for path in sorted(root.glob("data-*.jsonl")):
            try:
                for line in path.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        yield json.loads(line)
            except Exception:
                continue
    return _iter()


def load_meta(folder: Optional[str] = None) -> dict:
    return _read_meta_file(record_dir(folder))


def aggregated_entries_for_test() -> List[dict]:
    return list(_entries.values())


def lookup_dest_links_for_source(
    source_channel: str,
    first_msg_id: int,
    kid: Optional[str] = None,
) -> List[str]:
    want_source = build_message_link(source_channel, first_msg_id)
    result: List[str] = []
    seen = set()

    def _consume(item: dict) -> None:
        if not isinstance(item, dict):
            return
        if kid is not None and str(item.get("kid", "")) != str(kid):
            return
        mapper = item.get("mapper_item", item)
        if not isinstance(mapper, dict):
            return
        if want_source and mapper.get("source") != want_source:
            return
        if not mapper.get("source") or not mapper.get("dest"):
            return
        for value in _as_str_list(mapper["dest"]):
            if value not in seen:
                seen.add(value)
                result.append(value)

    for item in _entries.values():
        _consume(item)
    for item in iter_mapper_lines():
        _consume(item)
    return result


def dest_id_map_from_dest_links(
    dest_links: Sequence[str],
    dest_cfgs: Optional[Sequence[str]] = None,
) -> Dict[str, List[int]]:
    by_key: Dict[str, List[int]] = {}
    for link in dest_links or []:
        channel, msg_id = parse_tme_message_link(link)
        if channel and msg_id:
            by_key.setdefault(_channel_key(channel), []).append(msg_id)
    if dest_cfgs is None:
        return {
            key: list(ids)
            for key, ids in by_key.items()
        }
    result: Dict[str, List[int]] = {}
    for cfg in dest_cfgs or []:
        channel, _topic = _cfg_channel(cfg)
        ids = by_key.get(_channel_key(channel))
        if ids:
            result[cfg] = list(ids)
    return result


def _commit_mapper_job(job: WriteJob) -> None:
    folder = str(job.get("folder") or record_dir())
    meta = job.get("meta")
    if not isinstance(meta, dict):
        meta = _ensure_disk_meta(folder)
    mapper_item = job.get("mapper_item") or {}
    line_obj = job.get("entry")
    if not isinstance(line_obj, dict):
        line_obj = {
            "kid": str(job.get("kid", "")),
            "name": str(job.get("name", "")),
            "type": str(job.get("type_text", "")),
            "mapper_item": mapper_item,
        }
    payload = (
        json.dumps(line_obj, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    active = int(meta.get("active", 1) or 1)
    path = Path(folder) / volume_file_name(active)
    if (
        path.exists()
        and (
            path.stat().st_size >= VOLUME_MAX_BYTES
            or _volume_has_incomplete_tail(str(path))
        )
    ):
        active += 1
        meta["active"] = active
        path = Path(folder) / volume_file_name(active)
    _append_bytes(str(path), payload)
    _write_meta_file(folder, meta)
    _apply_retention(folder, meta)


def _do_write(job: WriteJob) -> None:
    backend = _write_backend
    try:
        if backend is not None:
            backend(job)
        else:
            _commit_mapper_job(job)
    except Exception:
        _safe_print_trace("写入发布 ID 记录失败：")


def _writer_loop() -> None:
    while True:
        job = _write_queue.get()
        try:
            if job is None:
                return
            _do_write(job)
        finally:
            _write_queue.task_done()


def _ensure_writer() -> None:
    global _writer_started, _writer_thread
    if _writer_started and _writer_thread is not None and _writer_thread.is_alive():
        return
    _writer_thread = threading.Thread(
        target=_writer_loop,
        name="publish-id-record-writer",
        daemon=True,
    )
    _writer_thread.start()
    _writer_started = True


def _schedule_write(job: WriteJob) -> None:
    _ensure_writer()
    _write_queue.put(job)


def wait_writer_idle(timeout: float = 2.0) -> bool:
    if not _writer_started:
        return True
    deadline = time.time() + max(0.0, float(timeout))
    while _write_queue.unfinished_tasks:
        if time.time() >= deadline:
            print("等待发布 ID 记录写盘超时")
            return False
        time.sleep(0.02)
    return True


def flush_writes_for_test(timeout: float = 5.0) -> None:
    wait_writer_idle(timeout)


def set_record_dir_for_test(folder: Optional[str]) -> None:
    global _record_dir_override
    _record_dir_override = folder


def set_write_backend_for_test(backend) -> None:
    global _write_backend
    _write_backend = backend


def reset_memory_for_test() -> None:
    _entries.clear()
    _meta_cache.clear()
    _meta_cache.update({"active": 1, "items": []})
