# Recovered module: src.py.com.yun.mao.monitor.TelegramMonitorWorker
# Behaviour-level reconstruction from the module constants, code-object
# signatures, and offline Hex-Rays output.
from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List, Optional, Set

from PyQt5.QtCore import QThread, pyqtSignal
from telethon import events

from ..auto import AutoWorkerWrapper, GlobalWorkingLock, ProcessCache, TopicUtils
from ..cd import TaskHardStop, Working
from ..cd.AsyncDequeQueueClass import AsyncDequeQueue
from ..config import NewConfig
from ..fea import _sq_ks
from ..link._fds_jm import sec
from ..login.SessionLoader import autologinWithSessionByHide
from ..telefast.RateTempClass import RateTempClass
from ..util import SuspendFrozenTag
from ..util.need import CommonCode, signals, utils
from ..util.need.AllBeanDef import (
    MonitorSignalBean,
    MonitorSignalBeanWrapper,
    MonitorTgMessageBean,
    ParseBean,
)
from .MonitorFollowUp import MonitorFollowUp, resolve_event_queue_keys
from .MonitorHistoryManagerFile import MonitorHistoryManager


class TelegramMonitorWorker(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int, int, int)
    auth_signal = pyqtSignal(bool)

    def __init__(self, args: Any) -> None:
        super().__init__()
        self.argsWrapper = args
        self.client: Any = None
        self.running = False
        self.message_queues: Dict[str, AsyncDequeQueue] = {}
        self.total_messages = 0
        self.forwarded_count = 0
        self.entity_cache: Dict[Any, Any] = {}
        self.semaphore: Optional[asyncio.Semaphore] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.me: Any = None
        self.auth_success = False
        self.all_source: List[Any] = []
        self.all_log_show_source: List[str] = []
        self.all_legal_auto_beans: List[Any] = []
        self.delay = 3.0
        self.signWrapper = MonitorSignalBeanWrapper()
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self._current_send_task: Optional[asyncio.Task] = None
        self._finish_notified = False
        self.can_send_all_history = False
        self.obtain_message_timeout = 10
        self._followup: Optional[MonitorFollowUp] = None
        self.progress_signal.emit(-1, -1, -1, -1)

    def _invoke_finish_once(self, success: bool) -> None:
        if self._finish_notified:
            return
        self._finish_notified = True
        callback = getattr(self.argsWrapper, "finish_call", None)
        if callable(callback):
            try:
                callback(bool(success))
            except TypeError:
                callback()

    def run(self) -> None:
        GlobalWorkingLock.SCHEDULER_STATUS = GlobalWorkingLock.STATUES_TIMING
        signals.global_ui_signal.update_icon_states.emit("")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.semaphore = asyncio.Semaphore(3)
        beans = getattr(self.argsWrapper, "autolist", None) or []
        limit = int(getattr(self.argsWrapper, "limit", 0) or 0)
        try:
            self.all_legal_auto_beans = list(
                CommonCode.genLegalAutoBeanListByLimit(beans, limit) or []
            )
        except Exception:
            self.all_legal_auto_beans = list(beans)
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            self._invoke_finish_once(False)
            return
        if not self.all_legal_auto_beans:
            print("合法执行的任务数量为0，请检查日志查找原因！")
            self._invoke_finish_once(False)
            return

        async def main() -> None:
            for beanLike in self.all_legal_auto_beans:
                getter = getattr(beanLike, "getSource", None)
                source = getter() if callable(getter) else getattr(beanLike, "source", "")
                source = str(source or "")
                if not source:
                    continue
                channel_part, _ = utils.parse_source_parts(source)
                if not channel_part:
                    continue
                safeSource = source
                self.message_queues[safeSource] = AsyncDequeQueue(maxsize=1000)
                self.all_source.append(utils.convertSourceToIdOrAt(channel_part))
                self.all_log_show_source.append(utils.convertPrivateIdIfNeed(channel_part))
                monitorBean = MonitorSignalBean(
                    updateTime=utils.get_format_time(),
                    safeSource=safeSource,
                    queueSize=0,
                    sended=0,
                    total=0,
                    sendedTotal=0,
                )
                self.signWrapper.beanList.append(monitorBean)
                self.publish_event(safeSource, [], monitorBean)
            self.running = True
            processor_task = asyncio.create_task(self.process_queues())
            try:
                await self.inner_monitor()
            finally:
                processor_task.cancel()
                try:
                    await processor_task
                except asyncio.CancelledError:
                    pass
                except Exception:
                    pass
                await CommonCode.safe_disconnect(self.client)

        try:
            self.loop.run_until_complete(main())
            self.running = False
            self._invoke_finish_once(True)
        except asyncio.CancelledError:
            print("【Monitor】手动停止")
            self.running = False
            self._invoke_finish_once(True)
        except Exception as exc:
            print("【Monitor】异常: ", exc)
            self.running = False
            self._invoke_finish_once(False)
        finally:
            self.running = False
            try:
                if self.loop is not None and not self.loop.is_closed():
                    pending = asyncio.all_tasks(self.loop)
                    if pending:
                        self.loop.run_until_complete(
                            asyncio.wait_for(
                                asyncio.gather(*pending, return_exceptions=True),
                                timeout=2.0,
                            )
                        )
                    self.loop.close()
            except Exception:
                pass

    async def inner_monitor(self) -> None:
        def check_call_back(success: bool) -> None:
            self.auth_success = bool(success)
            self.auth_signal.emit(self.auth_success)

        try:
            authenticated = await self.monitor_start_inner_wrapper(check_call_back)
            if not authenticated or self.client is None:
                return
            self._followup = MonitorFollowUp(self)
            await self._followup.setup()
            await self.restore_history_message()
            await self.setup_event_handlers()
            print("启动监听成功！分别监听：", self.all_log_show_source)
            SuspendFrozenTag.print_last_log_if_need()
            signals.global_ui_signal.cmd_update_monitor_status.emit(
                NewConfig.MONITOR_TIP_RUNNING
            )
            await self.client.run_until_disconnected()
        except asyncio.CancelledError:
            print("inner_monitor 被取消")
            raise
        except Exception as exc:
            print("Error: ", exc)

    async def restore_history_message(self) -> None:
        manager = MonitorHistoryManager()
        try:
            history_map = manager.get_history_map()
        except Exception:
            history_map = {}
        for safeSource, beans in (history_map or {}).items():
            queue = self.message_queues.get(str(safeSource))
            if queue is None:
                continue
            values = list(beans or [])
            print("正在恢复 ", safeSource, " 的历史监听记录 ", len(values), " 个")
            for bean in values:
                await queue.put(bean)

    async def setup_event_handlers(self) -> None:
        client = self.client
        if client is None:
            return

        async def handler(event: Any) -> None:
            msg = getattr(event, "message", None)
            if msg is None:
                return
            queue_keys = set(self.message_queues)
            candidates = resolve_event_queue_keys(event, queue_keys)
            if not candidates:
                return
            for safeSource in candidates:
                queue = self.message_queues.get(safeSource)
                if queue is None:
                    continue
                grouped_id = getattr(msg, "grouped_id", None)
                group_id = int(grouped_id or getattr(msg, "id", 0) or 0)
                group_key = str(grouped_id or group_id)
                bean = MonitorTgMessageBean(
                    message_id=int(getattr(msg, "id", 0) or 0),
                    safeSource=safeSource,
                    chat_id=int(getattr(msg, "chat_id", 0) or 0),
                    group_id=group_id,
                    group_key=group_key,
                    is_text_msg=bool(getattr(msg, "is_text_message", False)),
                )
                print("接收到消息：", str(bean))
                await queue.put(bean)
                self.total_messages += 1
                self.publish_event(safeSource, [bean], None)

        try:
            client.on(events.NewMessage(chats=self.all_source), handler)
        except Exception:
            try:
                client.add_event_handler(handler, events.NewMessage(chats=self.all_source))
            except Exception as exc:
                print("注册监控消息处理器失败：", exc)
                return
        if self._followup is not None:
            await self._followup.setup()

    def publish_event(
        self,
        safeSource: str,
        messages: Optional[List[Any]] = None,
        monitorBean: Optional[MonitorSignalBean] = None,
    ) -> None:
        if monitorBean is not None and monitorBean not in self.signWrapper.beanList:
            self.signWrapper.beanList.append(monitorBean)
        queue = self.message_queues.get(str(safeSource))
        queueSize = queue.qsize() if queue is not None else 0
        total = 0
        sended = 0
        sendedTotal = 0
        for item in self.signWrapper.beanList:
            total += int(getattr(item, "total", 0) or 0)
            sended += int(getattr(item, "sended", 0) or 0)
            sendedTotal += int(getattr(item, "sendedTotal", 0) or 0)
        try:
            signals.global_ui_signal.cmd_monitor_update.emit(self.signWrapper)
        except Exception:
            pass
        self.progress_signal.emit(total, sended, queueSize, sendedTotal)

    async def process_queues(self) -> None:
        autoBeans = list(self.all_legal_auto_beans)
        try:
            for auto in autoBeans:
                getter = getattr(auto, "getSource", None)
                source = getter() if callable(getter) else getattr(auto, "source", "")
                source = str(source or "")
                queue = self.message_queues.get(source)
                if queue is None:
                    continue
                task = asyncio.create_task(self.process_single_queue(source, queue, None))
                self.active_tasks[source] = task
                task.add_done_callback(
                    lambda done, safeSource=source: self.on_task_done(done, safeSource)
                )
            while self.running and not getattr(Working, "need_stop", False):
                await asyncio.sleep(1)
        except Exception as exc:
            print("监控队列处理异常：", exc)
        finally:
            await CommonCode.safe_disconnect(self.client)

    def on_task_done(self, task: asyncio.Task, safeSource: str) -> None:
        try:
            result = task.result()
            if result is not None:
                print(str(safeSource) + " 任务完成", result)
        except asyncio.CancelledError:
            print(str(safeSource) + " 任务被取消")
        except Exception as exc:
            print(str(safeSource) + " 任务异常: ", exc)
        finally:
            self.active_tasks.pop(safeSource, None)

    async def process_single_queue(
        self,
        safeSource: str,
        queue: AsyncDequeQueue,
        task: Any = None,
    ) -> Any:
        _ = task
        async with self.semaphore:
            while self.running and not getattr(Working, "need_stop", False):
                group_messages = await self.fetch_monitor_msg_from_queue(
                    batch_size=20,
                    queue=queue,
                    safeSource=safeSource,
                )
                if not group_messages:
                    await asyncio.sleep(1)
                    continue
                await self.process_send_monitor_msg(
                    group_messages,
                    safeSource,
                    None,
                    [],
                )
        return None

    async def process_send_monitor_msg(
        self,
        group_messages: Dict[str, List[MonitorTgMessageBean]],
        safeSource: str,
        message_list_object: Any = None,
        parse_eligible_list: Optional[List[ParseBean]] = None,
        had_send_message_ids: Optional[Set[int]] = None,
    ) -> Dict[str, Any]:
        result_state: Dict[str, Any] = {
            "success_rt_msg_id": 0,
            "total_send_count": 0,
            "total_send_group": 0,
            "final_sended_messages": [],
        }
        messages = [
            bean
            for values in (group_messages or {}).values()
            for bean in (values or [])
        ]
        if not messages:
            print("group_messages 为空： ", safeSource)
            return result_state
        message_ids = [int(getattr(bean, "message_id", 0) or 0) for bean in messages]
        print(
            "正在消费队列来自 ",
            safeSource,
            "，",
            len(group_messages),
            "组消息，合计包含 ",
            len(messages),
            " 个资源！",
        )
        autos = self._autos_for_safe_source(safeSource)
        if not autos:
            print("未找到监控任务：", safeSource)
            return result_state
        quoted = []
        try:
            quoted = await CommonCode.fetch_new_quote_messages(
                self.client,
                safeSource,
                ids=message_ids,
                prefix="monitor/process_send",
            )
        except Exception as exc:
            print(sec("rw_pc_skip_tpl_06").format(safeSource), exc)
        if parse_eligible_list is None:
            parse_eligible_list = []
        if not parse_eligible_list:
            tart_text, tart_message = CommonCode.getGroupTextAndMessage(
                quoted or []
            )
            parse_eligible_list = [
                ParseBean(
                    uniId=safeSource,
                    messages=list(quoted or []),
                    tart_text=tart_text,
                    tart_message=tart_message,
                    original_msg_ids=message_ids,
                    success=True,
                )
            ]
        had_send_message_ids = set(had_send_message_ids or ())
        final_total_send_count = 0
        for auto in autos:
            if getattr(Working, "need_stop", False):
                print("手动停止成功！")
                break
            t_parse_eligible_list = self.match_topic_message_list(
                auto,
                parse_eligible_list,
            )
            if not t_parse_eligible_list:
                continue
            start_time = time.time()
            task = asyncio.create_task(
                AutoWorkerWrapper.foreachToSend(
                    auto,
                    self.client,
                    t_parse_eligible_list,
                    self.argsWrapper,
                    shared_results=result_state,
                    call_back=None,
                )
            )
            self._current_send_task = task
            try:
                completed = await task
                if completed:
                    success_rt_msg_id, total_send_count, total_send_group, sended = completed
                    result_state["success_rt_msg_id"] = int(success_rt_msg_id or 0)
                    result_state["total_send_count"] = int(total_send_count or 0)
                    result_state["total_send_group"] = int(total_send_group or 0)
                    result_state["final_sended_messages"] = list(sended or [])
                    final_total_send_count += int(total_send_count or 0)
                    for item in sended or []:
                        if isinstance(item, int):
                            had_send_message_ids.add(item)
            except asyncio.CancelledError:
                print("耗时任务已被强制中断！")
            except Exception as exc:
                print("消费队列异常，来自 ", safeSource, ": ", exc)
            finally:
                self._current_send_task = None
            try:
                await AutoWorkerWrapper.completeItemSummery(
                    auto,
                    self.all_legal_auto_beans,
                    start_time,
                    result_state["success_rt_msg_id"],
                    result_state["total_send_count"],
                    result_state["total_send_group"],
                    0,
                )
            except Exception:
                pass
            try:
                if AutoWorkerWrapper.is_privateAd_available(auto):
                    await AutoWorkerWrapper.publish_private_ad(
                        self.argsWrapper,
                        auto,
                        self.client,
                        getattr(auto, "selfAdWrapper", None),
                    )
                if AutoWorkerWrapper.is_globalAd_available(self.argsWrapper):
                    await AutoWorkerWrapper.publish_global_ad(
                        False,
                        auto,
                        self.client,
                    )
            except Exception:
                AutoWorkerWrapper._print_trace() if hasattr(AutoWorkerWrapper, "_print_trace") else None
            self._delete_record_by(
                group_messages,
                had_send_message_ids,
                message_list_object,
                t_parse_eligible_list,
            )
        print("发送了 ", final_total_send_count, " 条消息！")
        try:
            AutoWorkerWrapper.print_summery([result_state])
        except Exception:
            pass
        return result_state

    def match_topic_condition(
        self,
        auto: Any,
        t_parse_eligible_list: List[ParseBean],
    ) -> List[ParseBean]:
        getter = getattr(auto, "getSource", None)
        source = getter() if callable(getter) else getattr(auto, "source", "")
        channel_part, source_topic = utils.parse_source_parts(str(source or ""))
        source_topic_id = int(
            getattr(auto, "user_topic_id", 0) or source_topic or 0
        )
        if not source_topic_id:
            return list(t_parse_eligible_list or [])
        matched: List[ParseBean] = []
        for parse in t_parse_eligible_list or []:
            messages = list(getattr(parse, "messages", None) or [])
            m_topic_id = (
                TopicUtils.parse_msg_topic_id(messages[0], source_topic_id)
                if messages
                else 0
            )
            if int(m_topic_id or 0) == source_topic_id:
                matched.append(parse)
        print(
            "尝试匹配群组：",
            channel_part,
            " 话题ID：",
            source_topic_id,
            " 之后有效资源 ",
            len(matched),
            " 组！",
        )
        return matched

    def match_topic_message_list(
        self,
        auto: Any,
        t_parse_eligible_list: List[ParseBean],
    ) -> List[ParseBean]:
        return self.match_topic_condition(auto, t_parse_eligible_list)

    def _delete_record_by(
        self,
        group_messages: Dict[str, List[MonitorTgMessageBean]],
        had_send_message_ids: Set[int],
        message_list_object: Any,
        parse_eligible_list: List[ParseBean],
    ) -> None:
        _ = message_list_object
        manager = MonitorHistoryManager()
        eligible_ids = {
            int(getattr(message, "id", 0) or 0)
            for parse in parse_eligible_list or []
            for message in (getattr(parse, "messages", None) or [])
        }
        for safeSource, values in (group_messages or {}).items():
            beans = list(values or [])
            invalid_beans = [
                bean for bean in beans if not int(getattr(bean, "message_id", 0) or 0)
            ]
            sent_beans = [
                bean
                for bean in beans
                if int(getattr(bean, "message_id", 0) or 0) in had_send_message_ids
            ]
            ineligible_beans = [
                bean
                for bean in beans
                if eligible_ids
                and int(getattr(bean, "message_id", 0) or 0) not in eligible_ids
            ]
            to_delete = invalid_beans + sent_beans + ineligible_beans
            if not to_delete:
                continue
            try:
                manager.delete_monitor_message_list(safeSource, to_delete)
            except Exception:
                pass
            if invalid_beans:
                print("已删除无效的 ", len(invalid_beans), " 条记录")
            if sent_beans:
                print("已删除发送成功的 ", len(sent_beans), " 条记录")
            if ineligible_beans:
                print("已删除不符合解析条件的 ", len(ineligible_beans), " 条记录")

    async def fetch_monitor_msg_from_queue(
        self,
        batch_size: int,
        queue: AsyncDequeQueue,
        safeSource: str,
    ) -> Dict[str, List[MonitorTgMessageBean]]:
        group_messages: Dict[str, List[MonitorTgMessageBean]] = {}
        last_group_id: Optional[str] = None
        start_time = time.monotonic()
        total_collected = 0

        async def put_front(bean: MonitorTgMessageBean) -> None:
            try:
                await queue.put(bean, front=True)
            except TypeError:
                await queue.put(bean)

        while True:
            if getattr(Working, "need_stop", False):
                break
            remaining_timeout = self.obtain_message_timeout - (
                time.monotonic() - start_time
            )
            if self.can_send_all_history:
                print(safeSource, " 进入历史消息模式，一次性清空队列")
                try:
                    while True:
                        msg_data = queue.get_nowait()
                        if isinstance(msg_data, MonitorTgMessageBean):
                            group_key = str(msg_data.group_key or msg_data.group_id)
                            group_messages.setdefault(group_key, []).append(msg_data)
                            total_collected += 1
                        queue.task_done()
                except asyncio.QueueEmpty:
                    pass
                break
            if remaining_timeout <= 0:
                print(safeSource, " 剩余超时为0，强制退出")
                break
            print(
                safeSource,
                " 尝试获取消息，剩余超时 ",
                f"{remaining_timeout:.2f}",
                "s, 当前 qsize=",
                queue.qsize(),
            )
            try:
                msg_data = await asyncio.wait_for(
                    queue.get(),
                    timeout=max(0.0, remaining_timeout),
                )
            except (asyncio.TimeoutError, TimeoutError):
                print(safeSource, " 获取消息超时（", self.obtain_message_timeout, "s），停止收集")
                break
            except asyncio.QueueEmpty:
                print(safeSource, " 队列空异常（忽略）")
                break
            except Exception as exc:
                print("错误2 ", safeSource, ": ", exc, "（fetch_monitor_msg_from_queue 整体异常）")
                break
            try:
                if isinstance(msg_data, MonitorTgMessageBean):
                    monitorBean = msg_data
                elif isinstance(msg_data, dict):
                    monitorBean = MonitorTgMessageBean(**msg_data)
                else:
                    print(safeSource, " 忽略非法格式历史消息: ", msg_data)
                    queue.task_done()
                    continue
                if getattr(monitorBean, "is_text_msg", False):
                    print(
                        safeSource,
                        " 遇到纯文本消息（ID:",
                        getattr(monitorBean, "message_id", 0),
                        "），结束当前组",
                    )
                    queue.task_done()
                    break
                group_key = str(
                    getattr(monitorBean, "group_key", "")
                    or getattr(monitorBean, "group_id", 0)
                )
                if last_group_id is not None and group_key != last_group_id:
                    print(
                        safeSource,
                        " group_id 变化（",
                        group_key,
                        " != ",
                        last_group_id,
                        "），放回消息 ID:",
                        getattr(monitorBean, "message_id", 0),
                    )
                    await put_front(monitorBean)
                    queue.task_done()
                    break
                group_messages.setdefault(group_key, []).append(monitorBean)
                last_group_id = group_key
                total_collected += 1
                queue.task_done()
                print(
                    safeSource,
                    " 添加消息 ID:",
                    getattr(monitorBean, "message_id", 0),
                    " 到组 ",
                    group_key,
                    "，当前组大小:",
                    len(group_messages[group_key]),
                )
                if total_collected >= int(batch_size or 20):
                    print(
                        safeSource,
                        " 当前组达到批量上限（",
                        batch_size,
                        "），结束组 ID:",
                        group_key,
                    )
                    break
            except Exception as exc:
                print("错误1 ", safeSource, ": ", exc)
                try:
                    queue.task_done()
                except Exception:
                    pass
        print(
            safeSource,
            " 收集完成：",
            len(group_messages),
            " 组，合计 ",
            total_collected,
            " 条消息，耗时 ",
            f"{time.monotonic() - start_time:.2f}",
            "s",
        )
        return group_messages

    def stop_qthread(self, blocking: bool = True) -> None:
        if not self.running and self._finish_notified:
            return
        self.running = False
        try:
            TaskHardStop.request_hard_stop("停止监控")
        except Exception:
            pass
        if self._current_send_task is not None:
            try:
                self._current_send_task.cancel()
            except Exception:
                pass
        if self.loop is not None and not self.loop.is_closed():
            try:
                self.loop.call_soon_threadsafe(self.loop.quit)
            except Exception:
                pass
        if blocking:
            try:
                TaskHardStop.wait_worker_stopped(self)
            except Exception:
                pass
        self._finalize_stop()

    def _finalize_stop(self) -> None:
        self._invoke_finish_once(True)
        try:
            ProcessCache.update_scheduler("")
        except Exception:
            pass
        print("监控任务被手动停止！")
        try:
            Working.Session_Working = False
        except Exception:
            pass
        GlobalWorkingLock.SCHEDULER_STATUS = GlobalWorkingLock.STATUES_AIDL
        signals.global_ui_signal.update_icon_states.emit("")

    async def monitor_start_inner_wrapper(self, check_call_back: Any) -> bool:
        phone_suf = str(getattr(self.argsWrapper, "phone_suf", "") or "")
        account_ok = False
        try:
            account_ok = bool(_sq_ks.check_account_without_loop(lambda ok: None))
        except Exception:
            account_ok = False
        try:
            check_call_back(account_ok)
        except Exception:
            pass
        if not account_ok:
            print(phone_suf + " 存在异常信息，请检查日志，解决异常再重试！")
            return False
        session_abs_path = str(
            getattr(self.argsWrapper, "session_abs_path", "")
            or getattr(self.argsWrapper, "session", "")
        )
        if not session_abs_path:
            print(phone_suf + " 登录失败！")
            return False
        try:
            tclient = await autologinWithSessionByHide(session_abs_path)
        except Exception as exc:
            print(phone_suf + " 登录失败！", exc)
            return False
        self.auth_success = bool(tclient)
        self.auth_signal.emit(self.auth_success)
        if not tclient:
            return False
        return await self.monitor_start_inner(tclient, True)

    async def monitor_start_inner(self, tclient: Any, tauth_success: bool) -> bool:
        if not tauth_success or tclient is None:
            return False
        self.client = tclient
        try:
            self.me = await tclient.get_me()
        except Exception as exc:
            print("账号登录后获取自身信息失败：", exc)
            return False
        for auto in self.all_legal_auto_beans:
            try:
                ok = await CommonCode.checkChannelAndGroupsWrapper(
                    tclient,
                    auto,
                    True,
                )
            except Exception as exc:
                print("检查频道/群组失败：", exc)
                ok = False
            if not ok:
                print("监控被终止！")
                return False
        down_load = int(getattr(self.argsWrapper, "down_load", 1) or 1)
        up_load = int(getattr(self.argsWrapper, "up_load", 1) or 1)
        try:
            RateTempClass.init_rate(down_load, up_load)
        except Exception:
            pass
        print(
            "超级速度配置-> 最大下载速率：",
            down_load,
            " 次/秒, 最大上传速率：",
            up_load,
            " 次/秒",
        )
        try:
            ProcessCache.clean_all_type_but_mode()
        except Exception:
            pass
        self.running = True
        return True

    def _autos_for_safe_source(self, safeSource: str) -> List[Any]:
        finder = getattr(CommonCode, "findAutoBeanBySource", None)
        if callable(finder):
            try:
                found = finder(safeSource, self.all_legal_auto_beans)
            except TypeError:
                try:
                    found = finder(self.all_legal_auto_beans, safeSource)
                except Exception:
                    found = None
            except Exception:
                found = None
            if found:
                return list(found)
        result = []
        for auto in self.all_legal_auto_beans:
            getter = getattr(auto, "getSource", None)
            source = getter() if callable(getter) else getattr(auto, "source", "")
            source = str(source or "")
            channel_part, _ = utils.parse_source_parts(source)
            if safeSource in (source, str(channel_part or "")):
                result.append(auto)
        return result
