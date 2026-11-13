# Recovered module: src.py.com.yun.mao.mthread.SchedulerThreadClass
# Static reconstruction from the Nuitka constants and Hex-Rays bodies.
# The APScheduler job closure, hourly retry loop, and teardown path are
# translated from the compiled control flow and module constant slots.
from __future__ import annotations

import asyncio
import contextlib
import inspect
import time
from typing import Any

from PyQt5.QtCore import QThread
from apscheduler.schedulers.blocking import BlockingScheduler

from ..auto import AutoWorker, GlobalWorkingLock, ProcessCache
from ..cd import TaskHardStop, Working
from ..config import NewConfig
from ..login import ClientCacheHelper
from ..login.SessionLoader import autologinWithSessionByHide
from ..util import SuspendFrozenTag
from ..util.need import CommonCode, signals, utils
from ..util.need.AllBeanDef import DTopClassWrapper


_RUNNING = getattr(GlobalWorkingLock, "STATUES_RUNNING", "running")
_TIMING = getattr(GlobalWorkingLock, "STATUES_TIMING", "timing")
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


def _unpack_login_result(result: Any) -> tuple[Any, bool, Any]:
    if isinstance(result, tuple):
        if len(result) >= 3:
            return result[0], bool(result[1]), result[2]
        if len(result) == 2:
            return result[0], result[0] is not None, result[1]
    return result, result is not None, None


def _unpack_check_result(result: Any) -> tuple[bool, Any]:
    if isinstance(result, tuple):
        if len(result) >= 2:
            return bool(result[0]), result[1]
        if result:
            return bool(result[0]), None
    return bool(result), None


@contextlib.contextmanager
def _working_lock():
    lock = getattr(GlobalWorkingLock, "lock", None)
    if lock is None:
        yield
        return
    with lock:
        yield


class SchedulerThread(QThread):
    def __init__(self, args: DTopClassWrapper | Any):
        super().__init__()
        self.args = args
        self.bean = args
        self.scheduler = None
        self.loop = None
        self.is_running = True
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
        """Keep the scheduler alive and restart it after recoverable errors."""
        print("定时调度器启动中...")
        while self.is_running:
            try:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                init_success = self.loop.run_until_complete(
                    self._init_and_start_scheduler()
                )
                if not init_success:
                    print("定时调度器初始化失败...")
                    self._invoke_finish_once(False)
                    self._shutdown_scheduler()
                else:
                    print("调度器启动成功")
                    _call_optional(
                        SuspendFrozenTag,
                        "print_last_log_if_need",
                    )
                    if self.scheduler is not None:
                        self.scheduler.start()
            except asyncio.CancelledError:
                print("调度器线程已取消")
            except Exception as exc:
                print("调度器线程异常: ", exc)
                _call_optional(SuspendFrozenTag, "print_last_log_if_need")
                if getattr(Working, "need_stop", False):
                    break
                self._shutdown_scheduler()
                print("定时调度器异常重启中，5秒后...")
                time.sleep(5)
            finally:
                if not self.is_running:
                    self._shutdown_scheduler()
                    if self.loop is not None and not self.loop.is_closed():
                        self.loop.close()
        print("【SchedulerThread】定时调度器线程已停止")

    async def _init_and_start_scheduler(self) -> bool:
        """Authenticate the configured session and validate its channels."""
        try:
            session_path = getattr(self.args, "session_abs_path", "")
            result = await autologinWithSessionByHide(session_path)
            client, auth_success, me = _unpack_login_result(result)
            if not auth_success or me is None or client is None:
                session_parts = utils.split_session(session_path)
                phone_suf, phone = (
                    session_parts
                    if isinstance(session_parts, tuple) and len(session_parts) >= 2
                    else ("", session_path)
                )
                print("账号 ", phone_suf, phone, " 登录失败！")
                self._invoke_finish_once(False)
                return False

            self.client = client
            check_result = await _maybe_await(
                CommonCode.checkChannelAndGroupsWrapper(
                    client,
                    getattr(self.args, "autolist", []),
                )
            )
            check_success, error_info = _unpack_check_result(check_result)
            if not check_success:
                print("检查异常: ", error_info)
                self._invoke_finish_once(False)
                await CommonCode.safe_disconnect(client)
                return False

            self._start_scheduler_final(client, me)
            return True
        except Exception as exc:
            print("检查异常: ", exc)
            if "error_info" in locals():
                print(" 存在异常信息: ", error_info)
            self._invoke_finish_once(False)
            return False

    def _start_scheduler_final(self, client: Any, me: Any) -> None:
        """Install the hourly job and store the blocking scheduler handle."""
        _ = (client, me)

        def my_job(*args: Any) -> None:
            if not self.is_running:
                print("self.is_running 为 False，线程要停止，跳过任务！")
                return
            with _working_lock():
                if getattr(GlobalWorkingLock, "work_doing", False):
                    print("上次任务还在进行中，本次触发将丢弃！")
                    return
                print("自动触发任务执行开始 ...")
                try:
                    from ..link._fds_rt import fs_by_pf

                    fs_by_pf()
                except Exception as e:
                    error_msg = str(e)
                    print(error_msg)

                top_args = getattr(self.args, "topArgs", "")
                task_args = tuple()
                if top_args:
                    task_args = tuple(str(top_args).split(" ", 2))
                    print("定时任务使用的参数: ", task_args)

                _call_optional(ProcessCache, "update_scheduler", "定时任务运行中 ")
                _set_scheduler_status(_RUNNING)
                _emit_icon_state()
                try:
                    if self.loop is not None and not self.loop.is_closed():
                        self.loop.run_until_complete(
                            self._worker_start_inner_wrapper(*task_args)
                        )
                    if getattr(Working, "need_stop", False):
                        print("定时任务已手动停止。")
                    else:
                        print("自动触发任务完成一次，等待下一个整点触发中...")
                except asyncio.CancelledError:
                    print("my_job 被取消")
                except Exception as exc:
                    print("my_job 异常: ", exc)
                finally:
                    ClientCacheHelper.safe_disconnect_client()

        self.scheduler = BlockingScheduler()
        self.scheduler.add_job(
            my_job,
            "cron",
            hour=getattr(self.args, "hour", "*"),
            coalesce=True,
            misfire_grace_time=getattr(self.args, "misfire_grace_time", 3600),
        )
        print("定时任务运行中...")
        _call_optional(ProcessCache, "update_scheduler", "定时任务运行中 ")
        _set_scheduler_status(_TIMING)
        _emit_icon_state()

    async def _worker_start_inner_wrapper(self, *args: Any) -> None:
        try:
            _call_optional(
                ProcessCache,
                "update_Mode_text",
                getattr(NewConfig, "TOP_MODE_TIMING", "【定时模式】"),
            )
            result = _call_optional(
                AutoWorker,
                "worker_start_inner_wrapper",
                self,
                *args,
            )
            await _maybe_await(result)
        except asyncio.CancelledError:
            print("任务被取消")
        except Exception as exc:
            print("长时任务异常: ", exc)

    def stop_qthread(self) -> None:
        if not self.is_running and self._finish_notified:
            return
        self.is_running = False
        _call_optional(TaskHardStop, "request_hard_stop", "停止定时任务")
        self._shutdown_scheduler()
        _call_optional(AutoWorker, "schedule_worker_teardown", self)
        self.quit()
        _call_optional(AutoWorker, "wait_worker_stopped", self)
        self._finalize_stop()

    def _finalize_stop(self) -> None:
        self._invoke_finish_once(True)
        _call_optional(ProcessCache, "update_scheduler", "")
        print("定时任务被手动停止！")
        _set_scheduler_status(_AIDL)
        _emit_icon_state()

    def _shutdown_scheduler(self) -> None:
        scheduler = self.scheduler
        if scheduler is None:
            return
        try:
            scheduler.shutdown(wait=False)
        except Exception:
            self.scheduler = None
        finally:
            self.scheduler = None
