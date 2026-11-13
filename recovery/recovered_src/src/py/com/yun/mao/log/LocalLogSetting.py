# Recovered module: src.py.com.yun.mao.log.LocalLogSetting
from __future__ import annotations

import datetime
import threading
from pathlib import Path

from ..util.need import utils


_TAIL_READ_CHUNK = 4096
_disk_lock = threading.Lock()
_cached_log_date = ""
_cached_last_line = ""


def _base_dir() -> Path:
    try:
        from ..config import YunYinMaoConfig

        return Path(YunYinMaoConfig.multi_abs_log_dir)
    except Exception:
        return Path.home() / "YunYinData" / "log"


def LogFile(path: str | Path | None = None) -> str:
    if path is not None:
        return str(path)
    return str(_base_dir() / (utils.get_format_date() + "_log.txt"))


def _read_last_line_fast(path: str | Path) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    try:
        with file_path.open("rb") as file:
            file.seek(0, 2)
            size = file.tell()
            if size <= 0:
                return ""
            file.seek(max(0, size - _TAIL_READ_CHUNK))
            data = file.read()
        lines = data.decode("utf-8", "ignore").splitlines()
        return lines[-1].strip() if lines else ""
    except Exception:
        return ""


def read_last_line_fast(path: str | Path | None = None) -> str:
    return _read_last_line_fast(path or LogFile())


def _read_tail_n_lines_unlocked(path: str | Path, n: int = 50) -> list[str]:
    file_path = Path(path)
    if not file_path.exists() or n <= 0:
        return []
    try:
        with file_path.open("rb") as file:
            file.seek(0, 2)
            size = file.tell()
            file.seek(max(0, size - _TAIL_READ_CHUNK * max(1, n)))
            data = file.read()
        return data.decode("utf-8", "ignore").splitlines()[-int(n) :]
    except Exception:
        return []


def read_tail_n_lines(path: str | Path | None = None, n: int = 50) -> list[str]:
    with _disk_lock:
        return _read_tail_n_lines_unlocked(path or LogFile(), n)


def _truncate_last_line(path: str | Path) -> None:
    file_path = Path(path)
    if not file_path.exists():
        return
    try:
        with file_path.open("rb+") as file:
            file.seek(0, 2)
            size = file.tell()
            if size <= 0:
                return
            file.seek(max(0, size - _TAIL_READ_CHUNK))
            data = file.read()
            pos = data.rfind(b"\n", 0, len(data) - 1)
            if pos >= 0:
                file.seek(max(0, size - _TAIL_READ_CHUNK) + pos + 1)
                file.truncate()
    except Exception:
        pass


def appendToLogInner(text: str, path: str | Path | None = None) -> None:
    path = path or LogFile()
    try:
        _base_dir().mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8", errors="ignore") as file:
            file.write(str(text or "") + "\n")
    except Exception as exc:
        print("Failed to write log: " + str(exc))


def appendToLogList(text_list: list[str]) -> None:
    for text in text_list or []:
        appendToLogInner(text)


def readLastLine() -> str:
    global _cached_log_date, _cached_last_line
    today = utils.get_format_date()
    if _cached_log_date != today:
        _cached_log_date = today
        _cached_last_line = read_last_line_fast(LogFile())
    return _cached_last_line


def deleteLastLine() -> None:
    _truncate_last_line(LogFile())


def deleteFiveDateLogFile() -> None:
    now = datetime.datetime.now()
    for i in range(0, 30):
        date = (now - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        path = _base_dir() / (date + "_log.txt")
        if i >= 5:
            utils.safe_del_file(path)


def init_folder() -> None:
    _base_dir().mkdir(parents=True, exist_ok=True)


def snapshot_recent_lines(n: int = 150) -> list[str]:
    return read_tail_n_lines(LogFile(), n)
