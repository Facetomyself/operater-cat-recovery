# Recovered module: src.py.com.yun.mao.cd.TaskHardStop
# Worker/process teardown and ghost-worker cleanup.  The original module
# depends on Qt; the fallback keeps offline imports and tests usable.
from __future__ import annotations

import asyncio
import inspect
import threading
import time
from typing import Callable

try:
    from PyQt5.QtCore import QCoreApplication, QObject, Qt, QThread, QTimer, pyqtSignal
except Exception:
    class QObject:
        def __init__(self, *args, **kwargs):
            pass

    class QCoreApplication:
        @classmethod
        def instance(cls):
            return None

    class QThread:
        @classmethod
        def currentThread(cls):
            return None

    class QTimer:
        @staticmethod
        def singleShot(*args, **kwargs):
            return None

    class Qt:
        QueuedConnection = 0

    def pyqtSignal(*args, **kwargs):
        return None


WORKER_STOP_WAIT_MS = 8000
GHOST_REAP_WAIT_MS = 3000
_TEARDOWN_LOOP_STOP_FAILSAFE_S = 2.0
_TEARDOWN_DISCONNECT_TIMEOUT_S = 3.0
_TEARDOWN_CANCEL_TIMEOUT_S = 4.0
_FALLBACK_DISCONNECT_WAIT_S = 8.0

_lock = threading.Lock()
_poster_lock = threading.Lock()
_ghost_lock = threading.Lock()
_ghost_workers: list = []
_procs: set = set()
_poster = None


class _MainThreadPoster(QObject):
    _posted = pyqtSignal(object) if pyqtSignal is not None else None

    def __init__(self):
        super().__init__()
        self._active = True
        if self._posted is not None:
            try:
                self._posted.connect(self._dispatch, Qt.QueuedConnection)
            except Exception:
                pass

    def _dispatch(self, fn):
        if callable(fn):
            try:
                fn()
            except Exception:
                pass

    def post(self, fn):
        if not self._active:
            return False
        try:
            self._posted.emit(fn)
            return True
        except Exception:
            return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._active = False
        return False


def _ensure_main_thread_poster():
    global _poster
    with _poster_lock:
        if _poster is not None:
            return _poster
        app = None
        try:
            app = QCoreApplication.instance()
        except Exception:
            app = None
        if app is None:
            return None
        try:
            _poster = _MainThreadPoster()
            _poster.moveToThread(app.thread())
        except Exception:
            _poster = None
        return _poster


def _post_to_main_thread(callback: Callable) -> bool:
    poster = _ensure_main_thread_poster()
    if poster is not None and poster.post(callback):
        return True
    try:
        QTimer.singleShot(0, callback)
        return True
    except Exception:
        return False


def track_worker(worker) -> None:
    with _ghost_lock:
        if worker not in _ghost_workers:
            _ghost_workers.append(worker)


def untrack_worker(worker=None) -> None:
    with _ghost_lock:
        if worker is None:
            _ghost_workers.clear()
        else:
            try:
                _ghost_workers.remove(worker)
            except ValueError:
                pass


def prune_ghost_workers() -> None:
    with _ghost_lock:
        alive = []
        for worker in _ghost_workers:
            try:
                if worker.isRunning():
                    alive.append(worker)
            except Exception:
                pass
        _ghost_workers[:] = alive


def _ghost_snapshot() -> list:
    with _ghost_lock:
        return list(_ghost_workers)


def any_tracked_worker_running() -> bool:
    prune_ghost_workers()
    with _ghost_lock:
        return any(
            bool(getattr(w, "isRunning", lambda: False)())
            for w in _ghost_workers
        )


def sync_worker_stop_state() -> bool:
    from . import Working

    Working.need_stop = any_tracked_worker_running()
    return bool(Working.need_stop)


def register(proc) -> None:
    with _lock:
        _procs.add(proc)


def unregister(proc) -> None:
    with _lock:
        _procs.discard(proc)


def kill_all(reason: str = "", clear_session: bool = False) -> int:
    killed = 0
    with _lock:
        procs = list(_procs)
        _procs.clear()
    for proc in procs:
        try:
            if getattr(proc, "poll", lambda: None)() is None:
                proc.kill()
                killed += 1
        except Exception:
            continue
    if reason:
        print("[HardStop] ", reason, "，已终止 ", killed, " 个 ffmpeg 子进程")
    if clear_session:
        try:
            from src.py.com.yun.mao.login import ClientCacheHelper

            ClientCacheHelper.safe_disconnect_client()
        except Exception:
            pass
    return killed


def nudge_ghost_workers() -> list:
    prune_ghost_workers()
    return _ghost_snapshot()


def force_teardown_ghost_workers(wait_ms: int = 2500) -> int:
    ghosts = nudge_ghost_workers()
    for worker in ghosts:
        try:
            worker.quit()
        except Exception:
            pass
    deadline = time.time() + max(0, wait_ms) / 1000.0
    while time.time() < deadline:
        if not any_tracked_worker_running():
            break
        time.sleep(0.05)
    still_alive = nudge_ghost_workers()
    for worker in still_alive:
        try:
            worker.terminate()
            worker.wait(500)
        except Exception as exc:
            print("[HardStop] terminate 失败：", exc)
    return len(still_alive)


def escalate_kill_ghost_workers_async(
    done_callback=None,
    wait_ms: int = GHOST_REAP_WAIT_MS,
) -> threading.Thread:
    def _bg():
        try:
            force_teardown_ghost_workers(wait_ms)
        finally:
            if callable(done_callback):
                _post_to_main_thread(lambda: done_callback(False))

    thread = threading.Thread(
        target=_bg,
        daemon=True,
        name="ghost-escalate-kill",
    )
    thread.start()
    return thread


def reap_ghost_workers(wait_ms: int = GHOST_REAP_WAIT_MS) -> int:
    return force_teardown_ghost_workers(wait_ms)


async def _teardown_worker_loop(loop, done_callback=None) -> None:
    try:
        try:
            from src.py.com.yun.mao.login import ClientCacheHelper

            value = ClientCacheHelper.safe_disconnect_client()
            if inspect.isawaitable(value):
                await asyncio.wait_for(
                    value,
                    timeout=_TEARDOWN_DISCONNECT_TIMEOUT_S,
                )
        except Exception:
            pass
        try:
            current = asyncio.current_task(loop=loop)
            tasks = [
                task
                for task in asyncio.all_tasks(loop)
                if task is not current and not task.done()
            ]
            for task in tasks:
                task.cancel()
            if tasks:
                await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=_TEARDOWN_CANCEL_TIMEOUT_S,
                )
        except Exception:
            pass
    finally:
        if callable(done_callback):
            _post_to_main_thread(lambda: done_callback())


def schedule_worker_teardown(worker, done_callback=None) -> None:
    if worker is None:
        return
    loop = getattr(worker, "loop", None)
    if loop is None or getattr(loop, "is_closed", lambda: True)():
        force_teardown_ghost_workers(500)
        if callable(done_callback):
            done_callback()
        return

    failsafe = None
    finished = False

    def _done(future=None):
        nonlocal failsafe, finished
        if finished:
            return
        finished = True
        handle = failsafe
        failsafe = None
        if handle is not None:
            try:
                handle.cancel()
            except Exception:
                pass
        if callable(done_callback):
            _post_to_main_thread(lambda: done_callback())

    async def _teardown():
        await _teardown_worker_loop(loop, None)

    def _start() -> None:
        nonlocal failsafe
        try:
            future = asyncio.ensure_future(_teardown(), loop=loop)
            future.add_done_callback(_done)
            failsafe = loop.call_later(
                _TEARDOWN_LOOP_STOP_FAILSAFE_S,
                lambda: loop.stop() if not loop.is_closed() else None,
            )
        except Exception:
            force_teardown_ghost_workers(500)
            _done()

    try:
        loop.call_soon_threadsafe(_start)
    except Exception:
        force_teardown_ghost_workers(500)
        _done()


def safe_disconnect_fallback() -> None:
    try:
        from src.py.com.yun.mao.login import ClientCacheHelper
    except Exception:
        return None

    def _run():
        loop = None
        try:
            value = ClientCacheHelper.safe_disconnect_client()
            if inspect.isawaitable(value):
                loop = asyncio.new_event_loop()
                loop.run_until_complete(value)
        except Exception:
            pass
        finally:
            if loop is not None:
                try:
                    loop.close()
                except Exception:
                    pass

    thread = threading.Thread(
        target=_run,
        daemon=True,
        name="hardstop-disconnect-fallback",
    )
    thread.start()
    thread.join(timeout=_FALLBACK_DISCONNECT_WAIT_S)
    if thread.is_alive():
        print("[HardStop] fallback disconnect 超时，放弃等待")
    return None


def request_hard_stop(reason: str = "", clear_session: bool = True) -> None:
    from . import Working

    Working.need_stop = True
    kill_all(reason, clear_session=clear_session)
    force_teardown_ghost_workers(500)
    if clear_session:
        safe_disconnect_fallback()
    return None


def wait_worker_stopped(worker, wait_ms: int = WORKER_STOP_WAIT_MS) -> bool:
    if worker is None:
        return True
    try:
        return bool(worker.wait(max(0, int(wait_ms))))
    except Exception:
        return True


def finalize_worker_async(worker, finalize_callback=None) -> threading.Thread:
    def _bg_wait():
        try:
            wait_worker_stopped(worker)
        finally:
            if callable(finalize_callback):
                _post_to_main_thread(lambda: finalize_callback(worker))

    thread = threading.Thread(
        target=_bg_wait,
        daemon=True,
        name="worker-stop-finalize",
    )
    thread.start()
    return thread
