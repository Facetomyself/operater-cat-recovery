# Recovered module: src.py.com.yun.mao.mthread.ReceiveCodeThread
# Static reconstruction from the Nuitka constants and Hex-Rays coroutine
# state machines.  Login/disconnect ordering is confirmed by the constants;
# the QThread status bookkeeping is a behavior-level translation.
from __future__ import annotations

import asyncio
import re
from typing import Any

from PyQt5.QtCore import QThread, pyqtSignal
from telethon import events

from ..auto import GlobalWorkingLock
from ..cd import TaskHardStop
from ..login import ClientCacheHelper
from ..login.SessionLoader import autologinWithSession
from ..util import TracePrinterHelper
from ..util.need import CommonCode, signals


TELEGRAM_OFFICIAL_ID = 777000
_CODE_PATTERNS = (
    re.compile(
        r"(?:Login code|login code|登录代码|验证码)\D{0,16}(\d{5,8})",
        re.I,
    ),
    re.compile(r"\b(\d{5,6})\b"),
)
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


def _untrack_worker() -> None:
    try:
        handler = getattr(TaskHardStop, "untrack_worker", None)
        if callable(handler):
            handler()
    except Exception:
        return


def _unpack_login_result(result: Any) -> tuple[Any, bool, Any]:
    if isinstance(result, tuple):
        if len(result) >= 3:
            return result[0], bool(result[1]), result[2]
        if len(result) == 2:
            return result[0], result[0] is not None, result[1]
    return result, result is not None, None


class ReceiveCodeThread(QThread):
    status_signal = pyqtSignal(str)
    code_signal = pyqtSignal(str)

    def __init__(self, session_abs_path: str):
        super().__init__()
        self.session_abs_path = session_abs_path
        self.loop = None
        self.client = None
        self._stopping = False

    @staticmethod
    def parse_login_code(text: str) -> str | None:
        for pattern in _CODE_PATTERNS:
            matched = pattern.search(str(text or ""))
            if matched:
                return matched.group(1)
        return None

    async def _listen(self) -> None:
        """Log in and wait for messages from Telegram's official account."""
        if self._stopping:
            return

        result = await autologinWithSession(self.session_abs_path)
        client, auth_success, me = _unpack_login_result(result)
        if not auth_success or me is None or client is None:
            print("接码登录失败，请查看日志后重试！")
            self.status_signal.emit("login_failed")
            return

        self.client = client
        print("接码登录成功，等待验证码... ")
        self.status_signal.emit("login_ok")

        async def on_official_message(event: Any) -> None:
            code = self.parse_login_code(getattr(event, "raw_text", ""))
            if code:
                self.code_signal.emit(code)

        self.client.add_event_handler(
            on_official_message,
            events.NewMessage(
                incoming=True,
                from_users=TELEGRAM_OFFICIAL_ID,
            ),
        )
        await self.client.run_until_disconnected()

    def run(self) -> None:
        """Create the receive loop and keep the QThread alive until stopped."""
        if not self._stopping:
            _set_scheduler_status(_RUNNING)
            _emit_icon_state()

        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self._listen())
        except asyncio.CancelledError:
            print("接码监听已取消")
        except Exception as exc:
            if exc.__class__.__name__ == "TaskHardStop":
                print("接码监听被手动停止")
            else:
                TracePrinterHelper.print_trace()
                print("接码监听异常: ", exc)
        finally:
            ClientCacheHelper.safe_disconnect_client()
            if self.loop is not None and not self.loop.is_closed():
                self.loop.close()
            _untrack_worker()
            _set_scheduler_status(_AIDL)
            _emit_icon_state()

    def request_stop(self) -> None:
        if self._stopping:
            return
        self._stopping = True
        try:
            if (
                self.loop is not None
                and not self.loop.is_closed()
                and self.loop.is_running()
            ):
                self.loop.call_soon_threadsafe(
                    lambda: asyncio.ensure_future(self._async_stop())
                )
        except Exception as exc:
            print("停止接码监听失败: ", exc)

    async def _async_stop(self) -> None:
        self._stopping = True
        try:
            if self.client is not None:
                await CommonCode.safe_disconnect(self.client)
        finally:
            ClientCacheHelper.safe_disconnect_client()
