# Recovered module: src.py.com.yun.mao.remember.RandomBucketManager
# Function names, parameters and return annotations come from the Nuitka
# constants.  Step-length rounding, edge boundaries and the unencrypted
# persistence fallback are inferred where the current recovered utils module
# has no matching encrypt/decrypt primitive.
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from typing import Any

from ..config import YunYinMaoConfig
from ..util.need import utils
from ..util.need import CommonCode


RANDOM_BUCKET_MAP_KEY = b"Kp8mR2xQvN5wL9jH3fT6yU1aZ4cE0sB7dG5iO8nM2qW="

_bucket_map: dict[str, dict[str, Any]] = {}
_session_tried_ranges: dict[str, list[tuple[int, int]]] = {}

# Compatibility aliases for the earlier simplified recovery.
_state = _bucket_map


def _gen_key(source: str, entry_kid: str = "") -> str:
    payload = f"{source}|{entry_kid}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _bucket_file(source: str, entry_kid: str = "") -> str:
    cache_dir = YunYinMaoConfig.abs_cache_dir
    if callable(cache_dir):
        cache_dir = cache_dir()
    folder = Path(f"{cache_dir}/randomBucketMap")
    utils.init_folder(folder)
    return str(folder / _gen_key(source, entry_kid))


def _ranges_overlap(
    start_a: int,
    end_a: int,
    start_b: int,
    end_b: int,
) -> bool:
    return max(int(start_a), int(start_b)) <= min(int(end_a), int(end_b))


def _range_conflicts(
    start: int,
    end: int,
    exclude_ranges: list[tuple[int, int]],
) -> bool:
    for ex_start, ex_end in exclude_ranges or []:
        if _ranges_overlap(start, end, ex_start, ex_end):
            return True
    return False


def auto_correct_step_length(top_num: int, step_length: int) -> int:
    top_num = max(0, int(top_num))
    step_length = max(1, int(step_length))
    if top_num <= 0:
        return step_length
    return max(1, min(step_length, top_num))


def _calc_random_end(random_end: int, step_length: int) -> int:
    random_end = max(0, int(random_end))
    step_length = max(1, int(step_length))
    if random_end <= 0:
        return 0
    return ((random_end + step_length - 1) // step_length) * step_length


def _num_buckets(random_end: int, step_length: int) -> int:
    step_length = max(1, int(step_length))
    random_end = max(0, int(random_end))
    return max(1, (random_end + step_length - 1) // step_length)


def _build_geographic_segments(
    num_buckets: int,
    step_length: int,
) -> list[tuple[int, int]]:
    step_length = max(1, int(step_length))
    segments: list[tuple[int, int]] = []
    for geo_index in range(max(0, int(num_buckets))):
        start = geo_index * step_length
        end = start + step_length - 1
        segments.append((start, end))
    return segments


def _generate_random_bucket_ranges(
    num_buckets: int,
    step_length: int,
) -> list[list[int]]:
    segments = _build_geographic_segments(num_buckets, step_length)
    random.shuffle(segments)
    return [[int(start), int(end)] for start, end in segments]


def _layout_is_valid(
    state: dict[str, Any] | None,
    step_length: int,
    top_num: int,
    num_buckets: int,
) -> bool:
    if not state:
        return False
    if int(state.get("step_length", -1) or -1) != int(step_length):
        return False
    if int(state.get("last_top_num", -1) or -1) != int(top_num):
        return False
    bucket_ranges = state.get("bucket_ranges") or []
    if len(bucket_ranges) != int(num_buckets):
        return False
    for pair in bucket_ranges:
        if not isinstance(pair, (list, tuple)) or len(pair) < 2:
            return False
        start, end = int(pair[0]), int(pair[1])
        if start > end or end - start + 1 != int(step_length):
            return False
    return True


def _bucket_range_from_state(
    state: dict[str, Any],
    bucket_index: int,
) -> tuple[int, int]:
    pair = (state.get("bucket_ranges") or [])[int(bucket_index)]
    return int(pair[0]), int(pair[1])


def clear_session_tried_ranges(source: str, entry_kid: str = "") -> None:
    _session_tried_ranges.pop(_gen_key(source, entry_kid), None)


def get_session_tried_ranges(
    source: str,
    entry_kid: str = "",
) -> list[tuple[int, int]]:
    return list(_session_tried_ranges.get(_gen_key(source, entry_kid), []))


def record_session_tried_range(
    source: str,
    entry_kid: str,
    start_id: int,
    end_id: int,
) -> None:
    ranges = _session_tried_ranges.setdefault(_gen_key(source, entry_kid), [])
    window = (int(start_id), int(end_id))
    if window not in ranges:
        ranges.append(window)


def session_tried_range_count(source: str, entry_kid: str = "") -> int:
    return len(_session_tried_ranges.get(_gen_key(source, entry_kid), []))


def _resolve_context(
    source: str,
    entry_kid: str = "",
) -> tuple[str, dict[str, Any]]:
    key = _gen_key(source, entry_kid)
    state = _bucket_map.setdefault(key, {})
    return key, state


def _write_to_disk(path: str | Path, json_string: str | dict[str, Any]) -> None:
    try:
        if isinstance(json_string, dict):
            json_string = json.dumps(json_string, ensure_ascii=False)
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        encrypt = getattr(utils, "encrypt", None)
        if callable(encrypt):
            payload = encrypt(RANDOM_BUCKET_MAP_KEY, json_string)
        else:
            payload = json_string.encode("utf-8")
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        with open(target, "wb") as file:
            file.write(payload)
    except Exception:
        return


def load_random_bucket_map() -> None:
    cache_dir = YunYinMaoConfig.abs_cache_dir
    if callable(cache_dir):
        cache_dir = cache_dir()
    path = Path(f"{cache_dir}/randomBucketMap")
    if not path.exists():
        return
    _bucket_map.clear()
    for file in path.iterdir():
        try:
            if not file.is_file():
                continue
            with open(file, "rb") as handle:
                line = handle.readline().strip()
            if not line:
                continue
            decrypt = getattr(utils, "decrypt", None)
            if callable(decrypt):
                txt = decrypt(RANDOM_BUCKET_MAP_KEY, line)
            else:
                txt = line.decode("utf-8")
            if isinstance(txt, bytes):
                txt = txt.decode("utf-8")
            loaded = json.loads(txt)
            if isinstance(loaded, dict):
                _bucket_map[file.name] = loaded
        except Exception:
            continue


def clean_buckets(source: str, entry_kid: str = "") -> None:
    key = _gen_key(source, entry_kid)
    _bucket_map.pop(key, None)
    _bucket_map.pop(_key(source, entry_kid), None)
    clear_session_tried_ranges(source, entry_kid)
    try:
        Path(_bucket_file(source, entry_kid)).unlink(missing_ok=True)
    except Exception:
        pass


def _apply_random_layout(
    source: str,
    entry_kid: str,
    key: str,
    state: dict[str, Any],
    step_length: int,
    top_num: int,
    num_buckets: int,
    reason: str,
) -> None:
    bucket_ranges = _generate_random_bucket_ranges(num_buckets, step_length)
    state["step_length"] = int(step_length)
    state["last_top_num"] = int(top_num)
    state["bucket_ranges"] = bucket_ranges
    state["tried_buckets"] = []
    clear_session_tried_ranges(source, entry_kid)
    _write_to_disk(
        _bucket_file(source, entry_kid),
        json.dumps(state, ensure_ascii=False),
    )
    print(
        f"随机模式：{reason}，已随机生成 {num_buckets} 个等宽桶布局"
        f"（步长 {step_length}），已清除枯竭记录"
    )


def bucket_count(
    source: str,
    entry_kid: str,
    count: int,
    top_num: int,
) -> int:
    _ = _resolve_context(source, entry_kid)
    step_length = max(100, int(top_num) // max(1, int(count)))
    step_length = auto_correct_step_length(top_num, step_length)
    random_end = _calc_random_end(top_num, step_length)
    num_buckets = _num_buckets(random_end, step_length)
    return num_buckets


def pick_next_bucket_range(
    source: str,
    entry_kid: str,
    count: int,
    top_num: int,
    session_excludes: list[tuple[int, int]] | None = None,
) -> tuple[int, int, int] | None:
    key, state = _resolve_context(source, entry_kid)
    top_num = max(0, int(top_num))
    count = max(1, int(count))
    step_length = max(100, top_num // count)
    step_length = auto_correct_step_length(top_num, step_length)
    random_end = _calc_random_end(top_num, step_length)
    num_buckets = _num_buckets(random_end, step_length)

    if not _layout_is_valid(state, step_length, top_num, num_buckets):
        if not state.get("bucket_ranges"):
            reason = "首次分配桶"
        elif int(state.get("step_length", 0) or 0) != step_length:
            reason = (
                f"期望数量变更（步长 {state.get('step_length')} -> "
                f"{step_length}）"
            )
        elif int(state.get("last_top_num", 0) or 0) != top_num:
            reason = (
                f"频道最大ID变更（{state.get('last_top_num')} -> "
                f"{top_num}）"
            )
        else:
            reason = "桶布局无效，重新分配"
        _apply_random_layout(
            source,
            entry_kid,
            key,
            state,
            step_length,
            top_num,
            num_buckets,
            reason,
        )

    excludes = list(session_excludes or [])
    excludes.extend(get_session_tried_ranges(source, entry_kid))
    tried_list = list(state.get("tried_buckets") or [])
    tried_set = {int(item) for item in tried_list}
    untried: list[tuple[int, int, int]] = []
    for bucket_index, pair in enumerate(state.get("bucket_ranges") or []):
        if int(bucket_index) in tried_set:
            continue
        start, end = int(pair[0]), int(pair[1])
        if _range_conflicts(start, end, excludes):
            continue
        untried.append((int(bucket_index), start, end))
    if not untried:
        return None

    bucket_index, start, end = random.choice(untried)
    record_session_tried_range(source, entry_kid, start, end)
    print(
        f"随机模式桶 #{bucket_index + 1}/{num_buckets}，"
        f"ID 窗口 ({start}, {end})，已枯竭 {len(tried_set)} 桶"
    )
    return start, end, bucket_index


def mark_bucket_exhausted(
    source: str,
    entry_kid: str,
    bucket_index: int,
    count: int,
    top_num: int,
) -> None:
    key, state = _resolve_context(source, entry_kid)
    bucket_ranges = state.get("bucket_ranges") or []
    bucket_index = int(bucket_index)
    if bucket_index < 0 or bucket_index >= len(bucket_ranges):
        return
    tried_set = {int(item) for item in (state.get("tried_buckets") or [])}
    tried_list = list(tried_set)
    if bucket_index not in tried_set:
        tried_list.append(bucket_index)
    tried_list = sorted(tried_list)
    state["tried_buckets"] = tried_list
    _write_to_disk(
        _bucket_file(source, entry_kid),
        json.dumps(state, ensure_ascii=False),
    )
    start, end = _bucket_range_from_state(state, bucket_index)
    print(
        f"随机模式桶 #{bucket_index + 1}/{len(bucket_ranges)} 已枯竭"
        f"（窗口 ({start}, {end}) 内无新资源），"
        f"持久化已枯竭 {len(tried_list)} 桶"
    )


def pick_persisted_range(
    source: str,
    entry_kid: str,
    count: int,
    top_num: int,
    session_excludes: list[tuple[int, int]] | None = None,
) -> tuple[int, int]:
    picked = pick_next_bucket_range(
        source,
        entry_kid,
        count,
        top_num,
        session_excludes,
    )
    if picked is None:
        key, state = _resolve_context(source, entry_kid)
        bucket_ranges = state.get("bucket_ranges") or []
        tried_count = len({int(item) for item in (state.get("tried_buckets") or [])})
        if bucket_ranges and tried_count >= len(bucket_ranges):
            print(
                f"随机模式：条目桶已全部枯竭（共 {len(bucket_ranges)} 桶），"
                f"开始新一轮轮询"
            )
            state["tried_buckets"] = []
            clear_session_tried_ranges(source, entry_kid)
            _write_to_disk(
                _bucket_file(source, entry_kid),
                json.dumps(state, ensure_ascii=False),
            )
            picked = pick_next_bucket_range(
                source,
                entry_kid,
                count,
                top_num,
                session_excludes,
            )
        elif bucket_ranges:
            clear_session_tried_ranges(source, entry_kid)
            picked = pick_next_bucket_range(
                source,
                entry_kid,
                count,
                top_num,
                session_excludes,
            )
    if picked is None:
        return 0, max(0, int(top_num))

    start, end, bucket_index = picked
    mark_bucket_exhausted(source, entry_kid, bucket_index, count, top_num)
    expand = getattr(CommonCode, "expand_random_group_fetch_id_window", None)
    if callable(expand):
        start, end = expand(start, end)
    return int(start), int(end)


# Compatibility helpers retained from the earlier simplified recovery.
def _key(source: str, entry_kid: str = "") -> str:
    return f"{source}|{entry_kid}"


def _state_file() -> Path:
    try:
        cache_dir = YunYinMaoConfig.abs_cache_dir
        if callable(cache_dir):
            cache_dir = cache_dir()
        base = Path(cache_dir)
    except Exception:
        base = Path.home() / "YunYinData"
    return base / "randomBucket" / "state.json"


def _load_state() -> dict:
    try:
        path = _state_file()
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                for key, state in data.items():
                    if isinstance(state, dict):
                        _bucket_map.setdefault(str(key), state)
    except Exception:
        pass
    return _bucket_map


def _save_state() -> None:
    try:
        path = _state_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(_bucket_map, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass


def _bucket_ranges(top_num: int, num_buckets: int, step_length: int):
    top_num = max(0, int(top_num))
    num_buckets = max(1, int(num_buckets))
    step_length = max(1, int(step_length))
    segments = []
    for index in range(num_buckets):
        start = top_num - (index + 1) * step_length
        end = start + step_length - 1
        segments.append((max(0, start), max(0, end)))
    return segments


def _random_ranges_overlap(start_a, end_a, start_b, end_b) -> bool:
    return _ranges_overlap(start_a, end_a, start_b, end_b)


def _random_range_conflicts(start, end, excludes) -> bool:
    return _range_conflicts(start, end, excludes)


def clear_bucket_state(source: str, entry_kid: str = "") -> None:
    _bucket_map.pop(_key(source, entry_kid), None)
    _save_state()


def reset_memory_for_test() -> None:
    _bucket_map.clear()
    _session_tried_ranges.clear()
