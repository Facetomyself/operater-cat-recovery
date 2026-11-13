# Recovered module: src.py.com.yun.mao.telefast.RateLimiterClass
# Static reconstruction from module init, code-object varnames and Hex-Rays.
from __future__ import annotations

import threading
import time


class RateLimiter:
    """Singleton, thread-safe interval limiter."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, rate_limit_per_second: int):
        if getattr(self, "_initialized", False):
            return
        self.rate_limit = int(rate_limit_per_second)
        self.interval = 1.0 / self.rate_limit
        self._initialized = False
        self.lock = threading.Lock()
        self.last_request_time = time.time()
        self._initialized = True

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.lock.release()
        return False

    def wait(self) -> None:
        with self.lock:
            current_time = time.time()
            elapsed_time = current_time - self.last_request_time
            time_to_wait = self.interval - elapsed_time
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            self.last_request_time = time.time()


class UpRateLimiter(RateLimiter):
    pass


class DownRateLimiter(RateLimiter):
    pass
