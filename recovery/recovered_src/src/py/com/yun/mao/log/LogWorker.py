# Recovered module: src.py.com.yun.mao.log.LogWorker
from __future__ import annotations

import threading

try:
    from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
except Exception:
    class QThread:
        def __init__(self, *args, **kwargs):
            self._thread = None

        @staticmethod
        def msleep(ms):
            import time
            time.sleep(ms / 1000.0)

        def start(self):
            self._thread = threading.Thread(target=self.run)
            self._thread.start()

        def wait(self, ms=0):
            if self._thread:
                self._thread.join(ms / 1000.0 if ms else None)

    class _Signal:
        def __init__(self):
            self._handlers = []

        def connect(self, handler):
            self._handlers.append(handler)

        def emit(self):
            for handler in list(self._handlers):
                handler()

    def pyqtSignal(*args, **kwargs):
        return _Signal()

    def pyqtSlot(*args, **kwargs):
        return lambda func: func


from . import LocalLogSetting


BATCH_SIZE = 20


class LogWorker(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True
        self.queue = []
        self.lock = threading.Lock()

    @pyqtSlot(str)
    def add_log(self, text: str):
        with self.lock:
            self.queue.append(str(text))

    def snapshot_recent_lines(self, n: int = 50) -> list[str]:
        with self.lock:
            return list(self.queue[-int(n) :])

    @pyqtSlot()
    def process(self):
        while self.running:
            texts = None
            with self.lock:
                if self.queue:
                    batch = (
                        BATCH_SIZE * 2
                        if len(self.queue) > BATCH_SIZE * 4
                        else BATCH_SIZE
                    )
                    texts = self.queue[:batch]
                    self.queue = self.queue[batch:]
            if texts:
                try:
                    LocalLogSetting.appendToLogList(texts)
                except Exception as exc:
                    print("Log write error: " + str(exc))
            with self.lock:
                queue_len = len(self.queue)
            QThread.msleep(
                20
                if queue_len > BATCH_SIZE * 4
                else 50
                if queue_len > BATCH_SIZE
                else 200
            )
        with self.lock:
            remaining_logs = self.queue.copy()
            self.queue.clear()
        if remaining_logs:
            try:
                LocalLogSetting.appendToLogList(remaining_logs)
            except Exception:
                pass
        try:
            self.finished.emit()
        except Exception:
            pass

    @pyqtSlot()
    def stop(self):
        self.running = False
