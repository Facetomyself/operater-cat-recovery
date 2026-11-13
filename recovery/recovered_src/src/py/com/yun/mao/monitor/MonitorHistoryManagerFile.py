# Recovered module: src.py.com.yun.mao.monitor.MonitorHistoryManagerFile
from __future__ import annotations

import json
import threading
from pathlib import Path

from ..util.need import utils
from ..util.need.AllBeanDef import MonitorTgMessageBean


class MonitorHistoryManager:
    _instances = {}
    _lock = threading.Lock()
    _initialized = False
    _history_map: dict[str, list] = {}
    _file_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.load_history_map()

    @classmethod
    def get_instance(cls):
        return cls()

    def _get_history_file_path(self) -> str:
        try:
            from ..config import YunYinMaoConfig

            base = Path(YunYinMaoConfig.abs_cache_dir)
        except Exception:
            base = Path.home() / "YunYinData"
        path = base / "monitor_history.json"
        utils.init_folder(path.parent)
        return str(path)

    def load_history_map(self) -> None:
        global _history_map
        path = Path(self._get_history_file_path())
        try:
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                self._history_map = {
                    str(key): [MonitorTgMessageBean(**item) for item in values]
                    for key, values in (data or {}).items()
                }
        except Exception as exc:
            print("加载历史记录失败: " + str(exc))
            self._history_map = {}

    def get_history_map(self) -> dict:
        return self._history_map

    def _write_to_file(self) -> None:
        path = Path(self._get_history_file_path())
        try:
            data = {
                key: [dict(bean.__dict__) for bean in values]
                for key, values in self._history_map.items()
            }
            path.write_text(
                json.dumps(data, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            print("写入历史记录失败: " + str(exc))

    def update_monitor_message_list(self, safe_source: str, new_beans: list) -> None:
        if not isinstance(safe_source, str):
            raise TypeError("safe_source 必须是字符串")
        existing = list(self._history_map.get(safe_source, []))
        existing_ids = {getattr(bean, "message_id", None) for bean in existing}
        for bean in new_beans or []:
            if not isinstance(bean, MonitorTgMessageBean):
                raise TypeError("new_beans 必须是 MonitorTgMessageBean 列表")
            if getattr(bean, "message_id", None) not in existing_ids:
                existing.append(bean)
                existing_ids.add(getattr(bean, "message_id", None))
        self._history_map[safe_source] = existing
        with self._file_lock:
            self._write_to_file()

    def get_monitor_message_list(self, safe_source: str) -> list:
        return list(self._history_map.get(safe_source, []))

    def clean_monitor_message_list(self, safe_source: str) -> None:
        if not isinstance(safe_source, str):
            raise TypeError("safe_source 必须是字符串")
        self._history_map.pop(safe_source, None)
        with self._file_lock:
            self._write_to_file()

    def delete_monitor_message_list(self, safe_source: str, delete_beans: list) -> None:
        if not isinstance(safe_source, str):
            raise TypeError("safe_source 必须是字符串")
        delete_ids = {
            getattr(bean, "message_id", None)
            for bean in (delete_beans or [])
            if isinstance(bean, MonitorTgMessageBean)
        }
        self._history_map[safe_source] = [
            bean
            for bean in self._history_map.get(safe_source, [])
            if getattr(bean, "message_id", None) not in delete_ids
        ]
        with self._file_lock:
            self._write_to_file()


def monitor_history_manager() -> MonitorHistoryManager:
    return MonitorHistoryManager.get_instance()
