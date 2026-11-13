# Recovered module: src.py.com.yun.mao.monitor.MonitorSchedulerReport
from __future__ import annotations

import asyncio
import threading
import time

try:
    from PyQt5.QtCore import QThread
except Exception:
    class QThread:
        def __init__(self, *args, **kwargs):
            self._thread = None

        def start(self):
            self._thread = threading.Thread(target=self.run)
            self._thread.start()

        def wait(self, ms=0):
            if self._thread:
                self._thread.join(ms / 1000.0 if ms else None)

        def quit(self):
            pass


class MonitorSchedulerReportThread(QThread):
    def __init__(self):
        super().__init__()
        self._running = True
        self.blocking = None

    def run(self):
        print("看门狗运行中...")
        try:
            from apscheduler.schedulers.blocking import BlockingScheduler

            self.blocking = BlockingScheduler()
            self.blocking.add_job(
                self.sync_start_report,
                "cron",
                hour="*",
                minute=0,
            )
            self.blocking.start()
        except Exception:
            while self._running:
                try:
                    self.sync_start_report()
                except Exception:
                    pass
                time.sleep(60)

    def sync_start_report(self):
        try:
            from ..fea import _sq_ks

            asyncio.run(_sq_ks.start_report_inner())
        except Exception:
            pass

    def stop_qthread(self):
        self._running = False
        print("看门狗已停止！")
        try:
            if self.blocking is not None:
                self.blocking.shutdown(wait=False)
        except Exception:
            pass
        try:
            self.quit()
        except Exception:
            pass
