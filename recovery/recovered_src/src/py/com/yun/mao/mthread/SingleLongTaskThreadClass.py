# Recovered module: src.py.com.yun.mao.mthread.SingleLongTaskThreadClass
# Static reconstruction from the Nuitka constants and Hex-Rays bodies.
# The class is a one-shot QThread wrapper around AutoWorker; stop/finalize
# paths are behavior-level translations of the compiled control flow.
from __future__ import annotations

import asyncio
import inspect
from typing import Any

from PyQt5.QtCore import QThread

from ..auto import AutoWorker, GlobalWorkingLock, ProcessCache
from ..cd import TaskHardStop
from ..config import NewConfig
from ..login import ClientCacheHelper
from ..util.need import signals
from ..util.need.AllBeanDef import DTopClassWrapper


_RUNNING = getattr(GlobalWorkingLock, "STATUES_RUNNING", "running")
_AIDL = getattr(GlobalWorkingLock, "STATUES_AIDL", "aidl")


def _set_scheduler_status(status: str) -> None:
    try:
        setattr(GlobalWorkingLock, "SCHEDULER_STATUS", status)
    except Exception:
        return


def _emit_icon_state() -> None:
    try:
        signals.global_ui_signal.update_icon_states.emit("")
    except Exception:
        return


def _call_optional(target: Any, name: str, *args: Any, **kwargs: Any) -> Any:
    try:
        handler = getattr(target, name, None)
        if callable(handler):
            return handler(*args, **kwargs)
    except Exception:
        return None
    return None


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


def _worker_args(args: Any) -> tuple[Any, ...]:
    top_args = getattr(args, "topArgs", "")
    if not top_args:
        return ()
    parts = str(top_args).split(" ", 2)
    return tuple(parts)


class SingleLongTaskThread(QThread):
    def __init__(self, args: DTopClassWrapper | Any):
        super().__init__()
        self.args = args
        self.bean = args
        self.loop = None
        self._is_stopping = False
        self._finish_notified = False
        self.client = None

    def _invoke_finish_once(self, success: bool) -> None:
        if self._finish_notified:
            return
        self._finish_notified = True
        finish_call = getattr(self.args, "finish_call", None)
        if callable(finish_call):
            try:
                finish_call(success)
            except Exception as exc:
                print("finish_call 执行失败: ", exc)

    def run(self) -> None:
        print("手动触发任务执行一次开始 ...")
        _set_scheduler_status(_RUNNING)
        _emit_icon_state()
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            _call_optional(
                ProcessCache,
                "update_Mode_text",
                getattr(NewConfig, "TOP_MODE_TIMING", "【定时模式】"),
            )
            self.loop.run_until_complete(
                self._safe_worker_start_inner_wrapper(*_worker_args(self.args))
            )
            self._invoke_finish_once(True)
        except asyncio.CancelledError:
            print("【SingleLongTask】手动停止")
            self._invoke_finish_once(False)
        except Exception as exc:
            print("【SingleLongTask】异常: ", exc)
            self._invoke_finish_once(False)
        finally:
            ClientCacheHelper.safe_disconnect_client()
            if self.loop is not None and not self.loop.is_closed():
                self.loop.close()
            _set_scheduler_status(_AIDL)
            _emit_icon_state()
            print("【SingleLongTask】线程已停止")

    async def _safe_worker_start_inner_wrapper(self, *args: Any) -> None:
        if self._is_stopping:
            print("【SingleLongTask】被手动停止")
            return
        try:
            result = _call_optional(
                AutoWorker,
                "worker_start_inner_wrapper",
                self,
                *args,
            )
            await _maybe_await(result)
        except asyncio.CancelledError:
            print("【SingleLongTask】被取消")
        except Exception as exc:
            print("异步【SingleLongTask】内部异常: ", exc)

    def stop_qthread(self) -> None:
        if self._is_stopping:
            return
        self._is_stopping = True
        _call_optional(TaskHardStop, "request_hard_stop", "停止单次任务")

        _call_optional(AutoWorker, "schedule_worker_teardown", self)
        self.quit()
        _call_optional(AutoWorker, "wait_worker_stopped", self)
        self._finalize_stop()

    def _finalize_stop(self) -> None:
        self._invoke_finish_once(True)
        _call_optional(ProcessCache, "update_scheduler", "")
        print("【SingleLongTask】被手动停止！")
        _set_scheduler_status(_AIDL)
        _emit_icon_state()
