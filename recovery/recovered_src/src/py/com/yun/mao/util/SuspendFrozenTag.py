# Recovered module: src.py.com.yun.mao.util.SuspendFrozenTag
# Small state facade for pausing/resuming sequential-ID progress.
from __future__ import annotations


__all__ = [
    "program_working_running",
    "set_program_working_running",
    "frozen_resume",
    "clear_increase_group_progress",
    "note_increase_group_progress",
    "apply_increase_skip_on_frozen",
    "check_frozen_timeout",
    "print_last_log_if_need",
]


_last_log_text = ""
flood_log_text = ""
_program_working_running = False
_frozen_resume = False
_increase_progress: dict[str, dict] = {}
current_increase_kid = ""
current_increase_next_start_id = 0


def program_working_running() -> bool:
    return _program_working_running


def set_program_working_running(value: bool) -> None:
    global _program_working_running
    _program_working_running = bool(value)


def frozen_resume() -> None:
    """Toggle the one-shot resume flag.

    inferred: both the frozen-detection path and the recovery-release path
    call this module-level function; a toggle keeps both call sites working
    without inventing a second entry point.
    """

    global _frozen_resume
    _frozen_resume = not _frozen_resume


def clear_increase_group_progress() -> None:
    global current_increase_kid, current_increase_next_start_id
    _increase_progress.clear()
    current_increase_kid = ""
    current_increase_next_start_id = 0


def note_increase_group_progress(kid: str, parse_ids: list) -> None:
    global current_increase_kid, current_increase_next_start_id
    current_increase_kid = str(kid)
    last_id = max([int(value) for value in parse_ids or []], default=0)
    current_increase_next_start_id = int(last_id or 0)
    _increase_progress[current_increase_kid] = {
        "parse_ids": list(parse_ids or []),
        "next_start_id": current_increase_next_start_id,
    }


def _apply_increase_skip(kid: str, next_id: int) -> bool:
    try:
        from ..dclass import LoadDataClass
        from ..util.need import CommonCode

        mem = LoadDataClass.getAutoBeanById(kid)
        if mem is None:
            print(f"假死跳过顺序 ID:内存中找不到条目 kid={kid}")
            return False
        cur = getattr(mem, "increase_startId", 0)
        if int(next_id) <= int(cur):
            print(
                f"假死跳过顺序 ID:next={next_id} "
                f"未大于当前 startId={cur} ,跳过写回 kid={kid}"
            )
            return False
        CommonCode.real_time_increase_params(mem, int(next_id))
        LoadDataClass.writeToDist()
        return True
    except Exception as exc:
        print(f"假死跳过顺序 ID 写回失败:{exc}")
        return False


def apply_increase_skip_on_frozen(kid: str, parse_ids: list) -> bool:
    try:
        last_id = max([int(value) for value in parse_ids or []], default=0)
        if not last_id:
            return False
        return _apply_increase_skip(kid, int(last_id) + 1)
    except Exception:
        return False


def check_frozen_timeout(timeout: int = 600) -> bool:
    global _frozen_resume
    result = bool(_frozen_resume)
    _frozen_resume = False
    return result


def print_last_log_if_need() -> str:
    return _last_log_text or flood_log_text
