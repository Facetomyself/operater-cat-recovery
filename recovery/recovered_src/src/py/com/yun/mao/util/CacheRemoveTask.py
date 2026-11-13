# Recovered module: src.py.com.yun.mao.util.CacheRemoveTask
# Local cache migration and employee-data refresh task.  No filesystem action
# occurs at import time; run() is the only side-effecting entrypoint.
from __future__ import annotations

from pathlib import Path

try:
    from PyQt5.QtCore import QRunnable
except Exception:
    class QRunnable:
        pass


class CacheRemoveTask(QRunnable):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _migrate_item_data(local_dict=None) -> None:
        """Copy legacy local cache files into the multi-account cache."""

        try:
            from src.py.com.yun.mao.config import YunYinMaoConfig
            from src.py.com.yun.mao.dclass import (
                ItemMemStore,
                LoadDataClass,
            )
            from src.py.com.yun.mao.util import DirManager
            from src.py.com.yun.mao.util.need import utils

            source_root = Path(DirManager.get_local_data_dir())
            target_root = Path(YunYinMaoConfig.multi_abs_cache_dir)
            pairs = (
                (
                    source_root / "YunYinData" / "cache" / "yun_yin_item_data",
                    target_root / "yun_yin_item_data",
                ),
                (
                    source_root / "YunYinData" / "cache" / "adIdMap",
                    target_root / "adIdMap",
                ),
                (
                    source_root / "YunYinData" / "cache" / "ai_employee_data",
                    target_root / "ai_employee_data",
                ),
            )
            for src_path, tar_path in pairs:
                if src_path.exists() and not tar_path.exists():
                    utils.safe_copy_file(src_path, tar_path)

            try:
                if ItemMemStore.is_bootstrapped():
                    return None
                local = (
                    local_dict
                    if isinstance(local_dict, dict)
                    else LoadDataClass._snapshot_dict()
                )
                if local:
                    LoadDataClass.loadDTopClass(local)
                    ItemMemStore.apply_snapshot(local)
            except Exception:
                return None
        except Exception:
            return None
        return None

    @staticmethod
    def _reload_employee() -> None:
        try:
            from src.py.com.yun.mao.dclass import LoadEmployeeClass
            from src.py.com.yun.mao.util.need import signals

            LoadEmployeeClass.loadEmployee()
            signals.global_ui_signal.signal_employee_data_changed.emit()
        except Exception as exc:
            print("发生异常:", exc)

    def run(self) -> None:
        try:
            self._migrate_item_data()
            try:
                from src.py.com.yun.mao.util.need import signals

                signals.global_ui_signal.invoke_on_main_thread.emit(
                    self._reload_employee
                )
            except Exception:
                self._reload_employee()
        except Exception as exc:
            print("发生异常:", exc)
