# Recovered module: src.py.com.yun.mao.mthread.TgClientBaseAsyncTaskThread
# Static reconstruction from the Nuitka constants and Hex-Rays bodies.
# This is the common async Telegram task/thread lifecycle used by the HTML
# and advertisement workers.
from __future__ import annotations

import asyncio
from typing import Any

from PyQt5.QtCore import QThread

from ..auto import GlobalWorkingLock
from ..login import ClientCacheHelper
from ..login.SessionLoader import autologinWithSession
from ..util import TracePrinterHelper
from ..util.need import CommonCode, signals
from ..util.need.AllBeanDef import PostAdTestBean, TgClientTaskSuperBean


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


def _unpack_login_result(result: Any) -> tuple[Any, bool, Any]:
    if isinstance(result, tuple):
        if len(result) >= 3:
            return result[0], bool(result[1]), result[2]
        if len(result) == 2:
            return result[0], result[0] is not None, result[1]
    return result, result is not None, None


def _emit_error(bean: Any) -> None:
    signal = getattr(bean, "stats_signal", None)
    if signal is not None:
        signal.emit(False, "发生错误，请查阅日志解决！")


class TgClientBaseAsyncTaskThread(QThread):
    def __init__(
        self,
        args: TgClientTaskSuperBean | PostAdTestBean | None = None,
        *extra: Any,
        **kwargs: Any,
    ):
        super().__init__()
        _ = (extra, kwargs)
        self.args = args
        self.bean = args
        self.loop = None
        self._is_stopping = False
        self._task = None
        self.client = None

    def run(self) -> None:
        """Run the login + async business task inside a dedicated event loop."""
        _set_scheduler_status(_RUNNING)
        _emit_icon_state()
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self._safe_worker_start_inner_wrapper())
        except asyncio.CancelledError:
            print("被手动停止")
        except Exception:
            TracePrinterHelper.print_trace()
            _emit_error(self.bean)
        finally:
            ClientCacheHelper.safe_disconnect_client()
            if self.loop is not None and not self.loop.is_closed():
                self.loop.close()
            _set_scheduler_status(_AIDL)
            _emit_icon_state()

    async def _safe_worker_start_inner_wrapper(self) -> None:
        """Authenticate the session, then await the subclass business task."""
        if self._is_stopping:
            print("被手动停止")
            return

        client = None
        try:
            session_path = getattr(self.bean, "session_abs_path", "")
            result = await autologinWithSession(session_path)
            client, auth_success, me = _unpack_login_result(result)
            if not auth_success or me is None or client is None:
                _emit_error(self.bean)
                return

            self.client = client
            self._task = asyncio.ensure_future(
                self.async_biz_task_run(client, me)
            )
            await self._task
        except asyncio.CancelledError:
            print("被手动停止")
        except Exception:
            TracePrinterHelper.print_trace()
            _emit_error(self.bean)
        finally:
            try:
                if client is not None:
                    await CommonCode.safe_disconnect(client)
                self.client = None
            except Exception:
                ClientCacheHelper.safe_disconnect_client()

    async def async_biz_task_run(self, client: Any, me: Any) -> None:
        """Base hook implemented by concrete Telegram tasks.

        The compiled base body is an immediate ``return None``; subclasses
        replace it with their actual network workflow.
        """
        _ = (client, me)
        return None

    def sync_biz_task_run(self, client: Any, me: Any) -> None:
        """Run the async business hook from the thread's event loop."""
        if self.loop is None or self.loop.is_closed():
            asyncio.run(self.async_biz_task_run(client, me))
            return None
        self._task = asyncio.ensure_future(self.async_biz_task_run(client, me))
        self.loop.run_until_complete(self._task)
        return None

    def stop(self) -> None:
        """Cancel the active task and stop the QThread without touching the GUI."""
        if self._is_stopping:
            return
        self._is_stopping = True
        try:
            loop = self.loop
            if loop is not None and not loop.is_closed() and loop.is_running():
                loop.call_soon_threadsafe(
                    lambda: (
                        self._task.cancel()
                        if self._task is not None and not self._task.done()
                        else None
                    )
                )
        except Exception:
            TracePrinterHelper.print_trace()
        finally:
            self.quit()
            self.wait(1000)
            _set_scheduler_status(_AIDL)
            _emit_icon_state()
