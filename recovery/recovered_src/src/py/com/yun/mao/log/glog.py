# Recovered module: src.py.com.yun.mao.log.glog
# UI log facade.  PyQt5 is optional for offline imports.
from __future__ import annotations

import sys
import time

from . import LocalLogSetting


UI_BACKFILL_LINES = 150
MAX_PENDING_UI_LINES = 500


try:
    from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal
    HAS_QT = True
except Exception:
    HAS_QT = False

    class QObject:
        def __init__(self, *args, **kwargs):
            pass

    class _Signal:
        def connect(self, handler):
            pass

        def emit(self, *args, **kwargs):
            pass

    def pyqtSignal(*args, **kwargs):
        return _Signal()

    class QTimer:
        @staticmethod
        def singleShot(ms, fn):
            fn()

    class QThread:
        @staticmethod
        def currentThread():
            return None


class LogStream:
    def __init__(self, on_new_text):
        self.on_new_text = on_new_text

    def write(self, newText):
        if newText:
            target = self.on_new_text
            if hasattr(target, "emit"):
                target.emit(str(newText))
            else:
                target(str(newText))

    def flush(self):
        pass


class GlobalLog(QObject):
    frozeDetected = pyqtSignal()

    def __init__(
        self,
        parent=None,
        ui=None,
        frozen_timeout_seconds: int = 60,
    ):
        super().__init__(parent)
        self.parent = parent
        self.ui = ui
        self.last_message_ended_with_newline = True
        self.last_log = []
        self.frozen_timeout_seconds = frozen_timeout_seconds
        self.frozen_threshold_ms = int(frozen_timeout_seconds * 1000)
        self._ui_attached = False
        self._ui_log_paused = False
        self._pending_ui_lines = []
        self._text_browser = None
        self._log_stream = LogStream(self.onDisplayUpdateText)
        self._cleaned = False
        self.last_log_time = time.time()
        self.frozen_timer = None
        self._frozen_timer = None
        self.stdout = sys.stdout
        self.log_thread = None
        self.log_worker = None
        if HAS_QT:
            try:
                from .LogWorker import LogWorker

                self.log_thread = QThread(self)
                self.log_worker = LogWorker()
                self.log_worker.moveToThread(self.log_thread)
                self.log_thread.started.connect(self.log_worker.process)
                self.log_worker.finished.connect(self.log_thread.quit)
                self.log_worker.finished.connect(self.log_worker.deleteLater)
                self.log_thread.finished.connect(self.log_thread.deleteLater)
                self.log_thread.start()
            except Exception:
                self.log_thread = None
                self.log_worker = None

    def write(self, text):
        self._log_stream.write(text)

    def _append_to_text_browser(self, text):
        self.last_log_time = time.time()
        value = str(text)
        self.last_log.append(value)
        self.last_message_ended_with_newline = value.endswith("\n")
        if self._ui_log_paused:
            self._pending_ui_lines.extend(value.splitlines())
            self._pending_ui_lines = self._pending_ui_lines[
                -MAX_PENDING_UI_LINES:
            ]
            return
        if self._text_browser is not None:
            try:
                self._text_browser.append(value)
            except Exception:
                pass
        LocalLogSetting.appendToLogInner(value)

    def attach_ui(self, widget):
        self.ui = widget
        self._text_browser = getattr(widget, "text_brow_log", widget)
        self._ui_attached = self._text_browser is not None
        return self

    def pause_ui_log(self):
        self._ui_log_paused = True

    def resume_ui_log(self):
        was_paused = self._ui_log_paused
        self._ui_log_paused = False
        pending = self._pending_ui_lines
        self._pending_ui_lines = []
        if was_paused and pending and not self._cleaned:
            QTimer.singleShot(0, lambda: self._flush_pending_ui_lines(pending))

    def _flush_pending_ui_lines(self, pending):
        for line in pending:
            self._append_to_text_browser(line)

    def _backfill_ui_log_from_disk(self, n: int = UI_BACKFILL_LINES):
        return LocalLogSetting.read_tail_n_lines(LogFile=None, n=n)

    def _merge_tail_lines(self, disk_lines, mem_lines, n=UI_BACKFILL_LINES):
        def _norm(text):
            return str(text or "").rstrip("\n").strip()

        disk = [_norm(line) for line in (disk_lines or [])]
        mem = [_norm(line) for line in (mem_lines or [])]
        overlap = 0
        max_k = min(len(disk), len(mem))
        for k in range(max_k, 0, -1):
            if disk[-k:] == mem[:k]:
                overlap = k
                break
        merged = disk + mem[overlap:]
        return merged[-int(n) :]

    def _on_frozen_timeout(self):
        if self._cleaned:
            return None
        if time.time() - self.last_log_time >= self.frozen_timeout_seconds:
            try:
                from ..util import SuspendFrozenTag

                SuspendFrozenTag.flood_log_text = "程序疑似卡死，请检查日志"
            except Exception:
                pass
            try:
                self.frozeDetected.emit()
            except Exception:
                pass
        return None

    def _restart_frozen_timer(self):
        self.last_log_time = time.time()
        if self.frozen_timer is not None:
            try:
                self.frozen_timer.stop()
            except Exception:
                pass
        try:
            self.frozen_timer = QTimer(self)
            self.frozen_timer.setSingleShot(True)
            self.frozen_timer.timeout.connect(self._on_frozen_timeout)
            self.frozen_timer.start(max(1, int(self.frozen_threshold_ms)))
        except Exception:
            self.frozen_timer = None
        self._frozen_timer = self.frozen_timer
        return None

    def onDisplayUpdateText(self, newText):
        self._append_to_text_browser(newText)
        self._restart_frozen_timer()
        return None

    def cleanup(self):
        self._cleaned = True
        try:
            if self.frozen_timer is not None:
                self.frozen_timer.stop()
        except Exception:
            pass
        try:
            if self.log_worker is not None:
                self.log_worker.stop()
        except Exception:
            pass
        try:
            if self.log_thread is not None and self.log_thread.isActive():
                self.log_thread.quit()
                self.log_thread.wait(3000)
        except Exception:
            pass
        return None

    def stop(self):
        return self.cleanup()

    def get_last_line(self, n: int = 1) -> str:
        lines = self._pending_ui_lines or []
        if not lines and self._text_browser is not None:
            try:
                lines = self._text_browser.toPlainText().splitlines()
            except Exception:
                lines = []
        return "\n".join(lines[-max(1, int(n)):])

    def remove_empty_line(self, text: str) -> str:
        return "\n".join(
            line for line in str(text or "").splitlines() if line.strip()
        )


global_log = GlobalLog()
glog = global_log
