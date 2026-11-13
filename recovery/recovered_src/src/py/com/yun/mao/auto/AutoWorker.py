# Recovered module: src.py.com.yun.mao.auto.AutoWorker
# Login/check/task-orchestration entrypoints reconstructed from the module
# constants and the four exact compiled-function names.
from __future__ import annotations

import asyncio
import time


async def worker_start_inner_wrapper(
    args,
    fs_by_pf=None,
    check_call_back=None,
):
    """Run one auto task and dispatch the terminal callback."""

    try:
        if callable(fs_by_pf):
            result = fs_by_pf()
            if asyncio.iscoroutine(result):
                await result
        try:
            from ..fea import _sq_ks
            from . import ProcessCache

            checker = getattr(_sq_ks, "check_account_without_loop", None)
            if callable(checker):
                checked = []
                check_result = checker(
                    lambda success: checked.append(bool(success))
                )
                if asyncio.iscoroutine(check_result):
                    check_result = await check_result
                allowed = (
                    checked[-1]
                    if checked
                    else bool(check_result)
                )
                if not allowed:
                    if callable(check_call_back):
                        check_call_back(False, args)
                    return None
                clean = getattr(ProcessCache, "clean_all_type_but_mode", None)
                if callable(clean):
                    clean()
        except asyncio.CancelledError:
            print("任务被取消")
            if callable(check_call_back):
                check_call_back(False, args)
            return None
        except Exception:
            if callable(check_call_back):
                check_call_back(False, args)
            return None
        return await worker_start_inner(args, check_call_back)
    except asyncio.CancelledError:
        print("任务被取消")
        if callable(check_call_back):
            check_call_back(False, args)
        return None
    except Exception as exc:
        print("发生了异常，请检查日志处理！", exc)
        try:
            from ..util import TracePrinterHelper

            TracePrinterHelper.print_trace()
        except Exception:
            pass
        if callable(check_call_back):
            check_call_back(False, args)
        return None


async def worker_start_inner(args, check_call_back=None):
    """Authenticate the session, validate channels and run the task loop."""

    from ..cd import Working
    from ..login.SessionLoader import autologinWithSession
    from ..util.need import CommonCode

    client = None
    try:
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            if callable(check_call_back):
                check_call_back(False, args)
            return None
        session = getattr(args, "session_abs_path", "")
        result = await autologinWithSession(session)
        client, auth_success, me = _unpack_login(result)
        if not auth_success or client is None or me is None:
            try:
                from ..util.need import utils

                _phone_suf, phone = utils.split_session(session)
            except Exception:
                phone = str(session)
            print("账号 ", phone, " 登录失败！")
            if callable(check_call_back):
                check_call_back(False, args)
            return None

        _configure_transfer_rate(args)
        check = await CommonCode.checkChannelAndGroupsWrapper(
            client,
            getattr(args, "autolist", []),
        )
        check_success, error_info = _unpack_check(check)
        if not check_success:
            print("账号存在异常信息，请检查日志，解决异常再重试！", error_info)
            if callable(check_call_back):
                check_call_back(False, args)
            return None

        await inner_working(
            client,
            args,
            me=me,
        )
        if callable(check_call_back):
            check_call_back(True, args)
        return True
    except asyncio.CancelledError:
        print("任务被取消")
        raise
    except Exception as exc:
        print("发生了异常，请检查日志处理！", exc)
        try:
            from ..util import TracePrinterHelper

            TracePrinterHelper.print_trace()
        except Exception:
            pass
        if callable(check_call_back):
            check_call_back(False, args)
        return None
    finally:
        try:
            if client is not None:
                await CommonCode.safe_disconnect(client)
        except Exception:
            pass


def _configure_transfer_rate(args):
    down_load = int(getattr(args, "down_load", 1) or 1)
    up_load = int(getattr(args, "up_load", 1) or 1)
    try:
        from ..telefast import RateTempClass

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
    return down_load, up_load


async def inner_working(
    client,
    argsWrapper=None,
    me=None,
    parseList=None,
    shared_results=None,
    autoBeans=None,
    summery_list=None,
):
    """Run the recovered per-task fetch, send, ad and summary orchestration."""

    from . import AutoWorkerWrapper, BizSleeper, ProcessCache
    from ..cd import Working

    start_time = time.time()
    summary = summery_list if isinstance(summery_list, list) else []
    task = None
    try:
        auto_wrapper = AutoWorkerWrapper
        autoxxxList = list(autoBeans or []) if autoBeans is not None else []
        if autoBeans is None:
            generator = getattr(auto_wrapper, "genLegalAutoBeanListByLimit", None)
            if callable(generator):
                autoxxxList = list(generator(argsWrapper) or [])
        mode = str(
            getattr(argsWrapper, "convert_mode", "") or ""
        ).strip().lower()
        if autoxxxList and mode:
            try:
                from ..fea import _sq_r_ca

                converter = getattr(
                    _sq_r_ca,
                    "convert_batch_with_retry",
                    None,
                )
                if callable(converter):
                    converted = converter(mode, autoxxxList)
                    if asyncio.iscoroutine(converted):
                        converted = await converted
                    if converted is not None:
                        autoxxxList = list(converted)
            except Exception:
                pass
        if not autoxxxList:
            print("合法执行的任务数量为0，请检查日志查找原因！")
            return None

        for index, autoxxx in enumerate(autoxxxList):
            if getattr(Working, "need_stop", False):
                try:
                    from ..link._fds_jm import sec

                    print(sec("rw_stop_05"))
                except Exception:
                    print("手动停止成功！")
                try:
                    from ..util import SuspendFrozenTag

                    resume = getattr(SuspendFrozenTag, "frozen_resume", None)
                    if callable(resume):
                        resume()
                except Exception:
                    pass
                return None
            try:
                setattr(ProcessCache, "current_process_index", index)
                type_text = ""
                type_getter = getattr(autoxxx, "genTypeText", None)
                if callable(type_getter):
                    type_text = str(type_getter() or "")
                type_updater = getattr(ProcessCache, "update_type_text", None)
                if callable(type_updater) and type_text:
                    type_updater(type_text)
                header = getattr(auto_wrapper, "headerLogInfo", None)
                if callable(header):
                    header_text = header(autoxxx, type_text)
                    if header_text:
                        print(header_text)
                if hasattr(ProcessCache, "update_process"):
                    ProcessCache.update_process(
                        f"（{index + 1}/{len(autoxxxList)}）"
                    )
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                print("正在快马加鞭采集消息资源中...", exc)
                continue

            success, current_parse_list = await obtainMessageAndParse(
                client,
                autoxxx,
            )
            if not success:
                print("正在快马加鞭采集消息资源中...")
                continue
            print("采集到符合条件的资源，正在执行中...")

            worker = getattr(auto_wrapper, "foreachToSend", None)
            if not callable(worker):
                continue
            task = asyncio.create_task(
                worker(
                    autoxxx,
                    client,
                    current_parse_list,
                    argsWrapper,
                    shared_results=shared_results,
                )
            )
            try:
                while not task.done():
                    await asyncio.sleep(1)
                task_result = await task
            except asyncio.CancelledError:
                task.cancel()
                print("耗时任务已被强制中断！")
                raise

            success_rt_msg_id = 0
            total_send_count = 0
            total_send_group = 0
            final_sended_messages = []
            if isinstance(task_result, dict):
                success_rt_msg_id = task_result.get("success_rt_msg_id", 0)
                total_send_count = task_result.get("total_send_count", 0)
                total_send_group = task_result.get("total_send_group", 0)
                final_sended_messages = task_result.get("final_sended_messages", [])
            elif isinstance(task_result, (tuple, list)) and len(task_result) >= 4:
                (
                    success_rt_msg_id,
                    total_send_count,
                    total_send_group,
                    final_sended_messages,
                ) = task_result[:4]

            try:
                complete = getattr(auto_wrapper, "completeItemSummery", None)
                if callable(complete):
                    summary.append(
                        complete(
                            autoxxx,
                            autoxxxList,
                            start_time,
                            success_rt_msg_id,
                            total_send_count,
                            total_send_group,
                            index,
                        )
                    )
            except Exception:
                pass

            try:
                if getattr(auto_wrapper, "is_privateAd_available", lambda _: False)(autoxxx):
                    if getattr(autoxxx, "adIsBottomUp", lambda: False)():
                        print("正在向评论区发布私有广告...")
                    await auto_wrapper.publish_private_ad(
                        argsWrapper,
                        autoxxx,
                        client,
                        getattr(autoxxx, "selfAdWrapper", None),
                    )
                if getattr(auto_wrapper, "is_globalAd_available", lambda _: False)(argsWrapper):
                    await auto_wrapper.publish_global_ad(False, autoxxx, client)
            except Exception as exc:
                print("正在快马加鞭采集消息资源中...", exc)

            sleeper = getattr(BizSleeper, "biz_sleep", None)
            if callable(sleeper):
                wait_result = sleeper(2, 5)
                if asyncio.iscoroutine(wait_result):
                    await wait_result

        try:
            print_summery = getattr(auto_wrapper, "print_summery", None)
            if callable(print_summery):
                print_summery(summary)
        except Exception:
            pass
        return None
    except asyncio.CancelledError:
        if task is not None and not task.done():
            task.cancel()
            print("耗时任务已被强制中断！")
        raise
    except Exception as exc:
        print("发生了异常，请检查日志处理！", exc)
        return None


async def obtainMessageAndParse(
    client,
    autoxxx,
    resultBean=None,
):
    """Run the recovered dynamic fetch and channel/comment parse loop."""

    from ..ai.TextCache import ALL_MESSAGE_FAILED_LIST, TextCacheBean
    from ..cd import Working
    from ..config.YunYinMaoConfig import PARSE_MESSAGE_WHILE_MAX_LOOP
    from ..fea import _dtdm_gl
    from ..fea._yjx_hb_file import yp_jx_pd_ch
    from ..link._fds_jm import sec
    from ..link._lk_gy_w import gy_jc_a1
    from ..remember import RandomBucketManager
    from ..util.need import CommonCode

    def _sec_text(value) -> str:
        if isinstance(value, (tuple, list)) and value:
            value = value[0]
        return str(value)

    async def _await(value):
        if asyncio.iscoroutine(value):
            return await value
        return value

    def _source() -> str:
        getter = getattr(autoxxx, "getSource", None)
        return str(getter() if callable(getter) else getattr(autoxxx, "source", "") or "")

    def _kid() -> str:
        return str(getattr(autoxxx, "kid", "") or "")

    def _name() -> str:
        getter = getattr(autoxxx, "getName", None)
        return str(getter() if callable(getter) else getattr(autoxxx, "name", "") or "")

    def _loop_tip(attempt: int) -> str:
        model = getattr(autoxxx, "model", "")
        text_model = getattr(autoxxx, "text_model", "")
        return (
            f"{_source()} {_name()} {text_model}/{model}，尝试了"
            f"{attempt}次解析消息都没有找到合法的消息，请检查参数，"
            "确认参数区间范围是否需要扩大！"
        )

    def _record_failure(message: str) -> None:
        try:
            ALL_MESSAGE_FAILED_LIST.append(
                TextCacheBean(
                    source=_source(),
                    genText=message,
                    log=message,
                )
            )
        except Exception:
            pass

    try:
        if not gy_jc_a1(autoxxx):
            return False, None
        fetch_message_func = _dtdm_gl.dt_hq_fn(
            _sec_text("dt_fetch_msg_04"),
            _sec_text("dt_iwt_mod_03"),
        )
        if not callable(fetch_message_func):
            print(_sec_text("dt_iwt_miss_01"))
            return False, None

        random_mode = False
        checker = getattr(autoxxx, "is_random_mode", None)
        if callable(checker):
            random_mode = bool(checker())
        source = _source()
        kid = _kid()
        if random_mode:
            clear = getattr(RandomBucketManager, "clear_session_tried_ranges", None)
            if callable(clear):
                clear(source, kid)
            else:
                fallback = getattr(RandomBucketManager, "clear_bucket_state", None)
                if callable(fallback):
                    fallback(source, kid)

        print(sec(_sec_text("rg_aw_fetch_pre_start_01")))
        message_list_object = await _await(fetch_message_func(client, autoxxx))
        print(sec(_sec_text("rg_aw_fetch_pre_end_02")))
        if getattr(Working, "need_stop", False):
            print("手动停止成功！")
            return False, None
        if message_list_object is None:
            print("1、严重错误，请检测，采集结果为NONE！")
            return False, None

        print(sec(_sec_text("rg_aw_yp_ch_pre_start_03")))
        result = await _await(
            yp_jx_pd_ch(autoxxx, message_list_object, is_monitor=False)
        )
        if result is None:
            return False, None
        if bool(getattr(result, "terminal", False)):
            if getattr(result, "msg", ""):
                print(result.msg)
            return False, None
        resultList = list(getattr(result, "beans", None) or [])
        print(
            sec(_sec_text("rg_aw_yp_ch_pre_end_tpl_04")).format(
                count=len(resultList)
            )
        )

        loop_count = 0
        max_loop = max(1, int(PARSE_MESSAGE_WHILE_MAX_LOOP))
        while not resultList:
            txt_log = _loop_tip(loop_count + 1)
            print("2、" + txt_log)
            _record_failure(txt_log)
            if getattr(Working, "need_stop", False):
                print("手动停止成功！")
                return False, None
            if loop_count > max_loop:
                print("1、" + txt_log)
                _record_failure(txt_log)
                return False, None
            loop_count += 1

            increase = getattr(autoxxx, "is_increase_mode", None)
            if callable(increase) and increase():
                start_getter = getattr(autoxxx, "increase_startId", None)
                count_getter = getattr(autoxxx, "increase_want_count", None)
                start_id = int(start_getter() if callable(start_getter) else 0)
                want_count = int(count_getter() if callable(count_getter) else 0)
                new_start_id = start_id + want_count
                try:
                    from ..dclass.AutoBeanXXX import mem_auto_for_writeback as lookup

                    if not isinstance(lookup, (dict,)) and not callable(lookup):
                        lookup = None
                    if callable(lookup):
                        mem_auto = lookup(autoxxx)
                    elif isinstance(lookup, dict):
                        mem_auto = lookup.get(kid)
                    else:
                        mem_auto = None
                except Exception:
                    mem_auto = None
                if mem_auto is not None:
                    updater = getattr(
                        CommonCode,
                        "real_time_increase_params",
                        None,
                    )
                    if callable(updater):
                        updater(mem_auto, new_start_id)
                    else:
                        params = getattr(mem_auto, "real_time_increase_params", None)
                        if isinstance(params, dict):
                            params["startId"] = new_start_id
                        else:
                            try:
                                setattr(
                                    mem_auto,
                                    "real_time_increase_params",
                                    {"startId": new_start_id},
                                )
                            except Exception:
                                pass
            elif random_mode:
                counter = getattr(
                    RandomBucketManager,
                    "session_tried_range_count",
                    None,
                )
                tried = 0
                if callable(counter):
                    try:
                        tried = int(counter(source, kid))
                    except Exception:
                        tried = 0
                print(
                    "随机模式：过滤后 0 组，继续扫描后续桶（本轮已试 "
                    f"{tried} 段 ID 窗口）"
                )

            print(sec(_sec_text("rg_aw_fetch_loop_start_05")))
            message_list_object = await _await(
                fetch_message_func(client, autoxxx)
            )
            print(sec(_sec_text("rg_aw_fetch_loop_end_06")))
            if message_list_object is None:
                print("2、严重错误，请检测，采集结果为NONE！")
                return False, None

            print(sec(_sec_text("rg_aw_yp_ch_loop_start_07")))
            result = await _await(
                yp_jx_pd_ch(autoxxx, message_list_object, is_monitor=False)
            )
            if result is None:
                return False, None
            if bool(getattr(result, "terminal", False)):
                if getattr(result, "msg", ""):
                    print(result.msg)
                return False, None
            resultList = list(getattr(result, "beans", None) or [])
            print(
                sec(_sec_text("rg_aw_yp_ch_loop_end_tpl_08")).format(
                    count=len(resultList)
                )
            )

        return True, resultList
    except asyncio.CancelledError:
        raise


def _unpack_login(result):
    if isinstance(result, tuple):
        if len(result) >= 3:
            return result[0], bool(result[1]), result[2]
        if len(result) == 2:
            return result[0], result[0] is not None, result[1]
    return result, result is not None, None


def _unpack_check(result):
    if isinstance(result, tuple):
        if len(result) >= 2:
            return bool(result[0]), result[1]
        if result:
            return bool(result[0]), None
    return bool(result), None
