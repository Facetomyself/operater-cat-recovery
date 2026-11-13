# Recovered module: src.py.com.yun.mao.record.CommentCopyLedger
# Ledger mapping source comments to destination comments.
from __future__ import annotations

import copy
import json
import os
import queue
import re
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from ..config import YunYinMaoConfig
from ..util.need import utils


LEDGER_DIR_NAME = "comment_record"
META_FILE_NAME = "meta.json"
VOLUME_NAME_RE = re.compile(r"^data-(\d+)\.jsonl$")
VOLUME_MAX_BYTES = 32 * 1024 * 1024

_copied_index: Set[Tuple[str, str, int]] = set()
_ledger_entries: List[dict] = []
_dir_override: Optional[str] = None
_index_lock = threading.Lock()
_index_loaded = False
_write_queue: "queue.Queue[Optional[dict]]" = queue.Queue()
_writer_started = False
_writer_thread: Optional[threading.Thread] = None
_disk_meta: dict = {"active": 1}


def comment_key(channel: str, main_id: int, comment_id: int) -> str:
    return f"{channel}_{main_id}_{comment_id}"


def encode_id_key(channel: str, main_id: int, comment_id: int) -> str:
    return comment_key(channel, main_id, comment_id)


def decode_id_key(value: str):
    try:
        channel, main, comment = str(value).rsplit("_", 2)
        return channel, int(main), int(comment)
    except Exception:
        return None


def _decode_id_key(value: str):
    return decode_id_key(value)


def _source_comment_ids(parse) -> List[int]:
    ids = getattr(parse, "original_msg_ids", None) or getattr(parse, "msg_ids", None) or []
    if not ids:
        messages = getattr(parse, "messages", None) or []
        ids = [getattr(msg, "id", 0) for msg in messages if getattr(msg, "id", 0)]
    return [int(value) for value in ids]


def source_channel_of(parse) -> str:
    return str(getattr(parse, "source_channel", "") or getattr(parse, "uniId", "") or "")


def source_main_id_of(parse) -> int:
    return int(getattr(parse, "source_main_msg_id", 0) or 0)


def parse_comment_ids(parse) -> List[int]:
    return _source_comment_ids(parse)


def already_copied(
    source_channel: str,
    source_main_id: int,
    comment_id: int,
    dest_channel: str,
    dest_main_id: int,
) -> bool:
    _ensure_index_loaded()
    return (source_channel, dest_channel, int(comment_id)) in _copied_index


def mark_after_send(
    source_channel: str,
    source_main_id: int,
    comment_id: int,
    dest_channel: str,
    dest_main_id: int,
    dest_comment_id: int,
) -> None:
    _ensure_index_loaded()
    _copied_index.add((source_channel, dest_channel, int(comment_id)))
    entry = {
        "source": comment_key(source_channel, source_main_id, comment_id),
        "dest": comment_key(dest_channel, dest_main_id, dest_comment_id),
        "time": utils.get_format_time(),
    }
    _ledger_entries.append(entry)
    _schedule_write(
        {
            "folder": _ledger_dir_str(),
            "source": entry["source"],
            "dest": entry["dest"],
            "time": entry["time"],
            "entry": copy.deepcopy(entry),
        }
    )


def mark_copied(
    source_channel: str,
    source_main_id: int,
    comment_id: int,
    dest_channel: str,
    dest_main_id: int,
    dest_comment_id: int,
) -> None:
    mark_after_send(
        source_channel,
        source_main_id,
        comment_id,
        dest_channel,
        dest_main_id,
        dest_comment_id,
    )


def _persist() -> None:
    try:
        _write_meta(_ledger_dir_str(), _read_meta(_ledger_dir_str()))
    except Exception:
        print("写入评论账本失败：")


def _ledger_dir() -> Path:
    if _dir_override:
        return Path(_dir_override)
    try:
        return Path(YunYinMaoConfig.abs_cache_only_multi_dir) / LEDGER_DIR_NAME
    except Exception:
        return Path.home() / "YunYinData" / LEDGER_DIR_NAME


def _ledger_dir_str() -> str:
    return str(_ledger_dir())


def volume_file_name(index: int) -> str:
    return f"data-{int(index):04d}.jsonl"


def volume_path(index: int) -> str:
    return str(_ledger_dir() / volume_file_name(index))


def _list_volume_indexes(folder: str) -> List[int]:
    root = Path(folder)
    indexes: List[int] = []
    try:
        for path in root.iterdir():
            match = VOLUME_NAME_RE.match(path.name)
            if match and path.is_file():
                indexes.append(int(match.group(1)))
    except OSError:
        return []
    indexes.sort()
    return indexes


def _read_meta(folder: str) -> dict:
    path = Path(folder) / META_FILE_NAME
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"active": 1}
    except Exception:
        return {"active": 1}


def _write_meta(folder: str, meta: dict) -> None:
    root = Path(folder)
    root.mkdir(parents=True, exist_ok=True)
    path = root / META_FILE_NAME
    tmp = root / (META_FILE_NAME + f".{os.getpid()}.{threading.get_ident()}.tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(meta, file, ensure_ascii=False, separators=(",", ":"))
        file.write("\n")
        file.flush()
        os.fsync(file.fileno())
    os.replace(tmp, path)


def _read_volume_hits(path: str) -> Set[Tuple[str, str, int]]:
    hits: Set[Tuple[str, str, int]] = set()
    file_path = Path(path)
    if not file_path.exists():
        return hits
    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                source_key = row.get("source")
                dest_key = row.get("dest")
                source = decode_id_key(source_key) if source_key else None
                dest = decode_id_key(dest_key) if dest_key else None
                if source and dest:
                    hits.add((source[0], dest[0], int(source[2])))
    except OSError:
        print("读取评论账本失败：", path)
    return hits


def _ensure_index_loaded() -> None:
    global _index_loaded
    if _index_loaded:
        return
    with _index_lock:
        if _index_loaded:
            return
        folder = _ledger_dir_str()
        for index in _list_volume_indexes(folder):
            _copied_index.update(
                _read_volume_hits(str(Path(folder) / volume_file_name(index)))
            )
        _index_loaded = True


def _persist_job(job: dict) -> None:
    folder = str(job.get("folder") or _ledger_dir_str())
    meta = _read_meta(folder)
    active = int(meta.get("active", 1) or 1)
    path = Path(folder) / volume_file_name(active)
    if path.exists() and path.stat().st_size >= VOLUME_MAX_BYTES:
        active += 1
        meta["active"] = active
        path = Path(folder) / volume_file_name(active)
    entry = job.get("entry") or {
        "source": job.get("source"),
        "dest": job.get("dest"),
        "time": job.get("time") or utils.get_format_time(),
    }
    root = Path(folder)
    root.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")
        file.flush()
        os.fsync(file.fileno())
    _write_meta(folder, meta)


def _writer_loop() -> None:
    while True:
        job = _write_queue.get()
        try:
            if job is None:
                return
            try:
                _persist_job(job)
            except Exception:
                print("写入评论账本失败：")
        finally:
            _write_queue.task_done()


def _ensure_writer() -> None:
    global _writer_started, _writer_thread
    if _writer_started and _writer_thread is not None and _writer_thread.is_alive():
        return
    _writer_thread = threading.Thread(
        target=_writer_loop,
        name="comment-copy-ledger-writer",
        daemon=True,
    )
    _writer_thread.start()
    _writer_started = True


def _schedule_write(job: dict) -> None:
    _ensure_writer()
    _write_queue.put(job)


def destination_main_id_of(parse) -> int:
    return int(
        getattr(parse, "dest_main_msg_id", 0)
        or getattr(parse, "dest_main_id", 0)
        or 0
    )


def dest_ids_aligned_to_sources(
    parse,
    dest_channel: str,
    dest_main_id: int,
    source_comment_ids: Sequence[int],
) -> List[int]:
    return [
        cid
        for cid in source_comment_ids or []
        if already_copied(
            source_channel_of(parse),
            source_main_id_of(parse),
            int(cid),
            dest_channel,
            dest_main_id,
        )
    ]


def extract_sent_ids(sent) -> List[int]:
    ids = []
    for item in sent or []:
        mid = getattr(item, "id", None)
        if mid is None and isinstance(item, dict):
            mid = item.get("id")
        if mid is not None:
            ids.append(int(mid))
    return ids


def should_skip_comment_group(parse, dest_to_map: Optional[Dict] = None) -> bool:
    ids = _source_comment_ids(parse)
    if not ids:
        return False
    return not union_missing_ids(parse, dest_to_map)


def missing_for_dest(
    source_comment_ids: Sequence[int],
    dest_ids: Sequence[int],
) -> List[int]:
    return list(source_comment_ids or [])[len(dest_ids or []) :]


def missing_comment_ids(
    source_channel: str,
    source_main_id: int,
    comment_ids: Sequence[int],
    dest_channel: str,
    dest_main_id: int,
) -> List[int]:
    return [
        int(cid)
        for cid in comment_ids or []
        if not already_copied(
            source_channel,
            source_main_id,
            int(cid),
            dest_channel,
            dest_main_id,
        )
    ]


def union_missing_for_map(
    source_comment_ids: Sequence[int],
    dest_ids: Sequence[int],
) -> List[int]:
    return missing_for_dest(source_comment_ids, dest_ids)


def union_missing_ids(parse, dest_to_map: Optional[Dict] = None) -> List[int]:
    ids = _source_comment_ids(parse)
    if dest_to_map is None:
        return ids
    source_channel = source_channel_of(parse)
    source_main_id = source_main_id_of(parse)
    missing: List[int] = []
    seen: Set[int] = set()
    for dest_channel, value in (dest_to_map or {}).items():
        if isinstance(value, dict):
            dest_main_id = int(
                value.get("main_id")
                or value.get("dest_main_id")
                or 0
            )
        elif isinstance(value, (list, tuple)):
            dest_main_id = int(value[0]) if value else 0
        else:
            try:
                dest_main_id = int(value or 0)
            except (TypeError, ValueError):
                dest_main_id = 0
        for cid in ids:
            comment_id = int(cid)
            if comment_id in seen:
                continue
            if not already_copied(
                source_channel,
                source_main_id,
                comment_id,
                str(dest_channel),
                dest_main_id,
            ):
                seen.add(comment_id)
                missing.append(comment_id)
    return missing


def comment_send_success_tuple(
    send_to_comment: bool,
    any_comment_sent: bool,
    count_if_sent: int,
    group_last_id: int,
) -> Tuple[int, int]:
    if send_to_comment and any_comment_sent:
        return int(count_if_sent), int(group_last_id)
    return 0, int(group_last_id)


def message_ids_of(messages: Sequence[Any]) -> List[int]:
    return [int(getattr(msg, "id", 0) or 0) for msg in (messages or []) if getattr(msg, "id", 0)]


def messages_by_ids(messages: Sequence[Any], want_ids: Sequence[int]) -> List[Any]:
    wanted = {int(value) for value in want_ids or []}
    return [msg for msg in (messages or []) if int(getattr(msg, "id", 0) or 0) in wanted]


def slice_album_for_missing(
    album: Sequence[Any],
    album_source_messages: Sequence[Any],
    missing_ids: Sequence[int],
) -> Optional[List[Any]]:
    if not album or not missing_ids:
        return []
    by_id = {int(getattr(msg, "id", 0) or 0): msg for msg in album_source_messages or []}
    return [by_id[int(mid)] for mid in missing_ids if int(mid) in by_id]


def message_ids_of_parse(parse) -> List[int]:
    return message_ids_of(getattr(parse, "messages", None) or [])


def flush_writes_for_test(timeout: float = 3.0) -> None:
    wait_writer_idle(timeout)


def wait_writer_idle(timeout: float = 3.0) -> bool:
    if not _writer_started:
        return True
    deadline = time.time() + max(0.0, float(timeout))
    while _write_queue.unfinished_tasks:
        if time.time() >= deadline:
            print("等待评论账本写盘超时")
            return False
        time.sleep(0.02)
    return True


def set_dir_override_for_test(path: Optional[str]) -> None:
    global _dir_override, _index_loaded
    _dir_override = path
    _index_loaded = False


def reset_for_test() -> None:
    global _index_loaded
    _copied_index.clear()
    _ledger_entries.clear()
    _index_loaded = False
