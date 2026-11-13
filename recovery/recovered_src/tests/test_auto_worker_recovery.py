from __future__ import annotations

import asyncio
import inspect
import sys
import types

import src.py.com.yun.mao.fea as fea_pkg
from src.py.com.yun.mao.auto import AutoWorker as auto_worker_module
from src.py.com.yun.mao.auto import AutoWorkerWrapper, BizSleeper, ProcessCache
from src.py.com.yun.mao.auto.AutoWorker import (
    _configure_transfer_rate,
    inner_working,
    obtainMessageAndParse,
    worker_start_inner_wrapper,
)
from src.py.com.yun.mao.cd import Working


def test_inner_working_empty_bean_result_contract(monkeypatch, capsys):
    wrapper = types.ModuleType("AutoWorkerWrapper")
    wrapper.genLegalAutoBeanListByLimit = lambda args: []
    process_cache = types.ModuleType("ProcessCache")
    process_cache.update_process = lambda value: None
    working = types.ModuleType("Working")
    working.need_stop = False
    monkeypatch.setitem(
        sys.modules,
        "src.py.com.yun.mao.auto.AutoWorkerWrapper",
        wrapper,
    )
    monkeypatch.setitem(
        sys.modules,
        "src.py.com.yun.mao.auto.ProcessCache",
        process_cache,
    )
    monkeypatch.setitem(
        sys.modules,
        "src.py.com.yun.mao.cd.Working",
        working,
    )

    result = asyncio.run(inner_working(None, None, autoBeans=[]))
    assert result is None
    assert "合法执行的任务数量为0" in capsys.readouterr().out


def test_configure_transfer_rate_logs(monkeypatch, capsys):
    telefast = types.ModuleType("src.py.com.yun.mao.telefast")
    rate = types.ModuleType("RateTempClass")
    calls = []
    rate.init_rate = lambda down, up: calls.append((down, up))
    telefast.RateTempClass = rate
    monkeypatch.setitem(
        sys.modules,
        "src.py.com.yun.mao.telefast",
        telefast,
    )
    args = types.SimpleNamespace(down_load=3, up_load=4)
    assert _configure_transfer_rate(args) == (3, 4)
    assert calls == [(3, 4)]
    assert "最大下载速率： 3" in capsys.readouterr().out


def test_worker_wrapper_checks_account_before_worker(monkeypatch):
    calls = {"clean": 0, "worker": 0}
    sq_ks = types.ModuleType("_sq_ks")
    sq_ks.check_account_without_loop = lambda callback: callback(True)
    monkeypatch.setattr(fea_pkg, "_sq_ks", sq_ks, raising=False)
    monkeypatch.setattr(
        ProcessCache,
        "clean_all_type_but_mode",
        lambda: calls.__setitem__("clean", calls["clean"] + 1),
    )

    async def fake_worker(args, callback=None):
        calls["worker"] += 1
        return "ok"

    monkeypatch.setattr(auto_worker_module, "worker_start_inner", fake_worker)
    assert asyncio.run(
        worker_start_inner_wrapper(object(), None, None)
    ) == "ok"
    assert calls == {"clean": 1, "worker": 1}


def test_worker_wrapper_stops_when_account_check_fails(monkeypatch):
    calls = {"worker": 0, "callback": []}
    sq_ks = types.ModuleType("_sq_ks")
    sq_ks.check_account_without_loop = lambda callback: callback(False)
    monkeypatch.setattr(fea_pkg, "_sq_ks", sq_ks, raising=False)

    async def fake_worker(args, callback=None):
        calls["worker"] += 1

    def callback(success, args):
        calls["callback"].append((success, args))

    monkeypatch.setattr(auto_worker_module, "worker_start_inner", fake_worker)
    args = object()
    assert asyncio.run(
        worker_start_inner_wrapper(args, None, callback)
    ) is None
    assert calls["worker"] == 0
    assert calls["callback"] == [(False, args)]


def test_inner_working_calls_biz_sleep(monkeypatch):
    sleeps = []

    async def foreach_to_send(auto, client, parse_list, args_wrapper, **kwargs):
        return (4, 1, 1, [])

    monkeypatch.setattr(AutoWorkerWrapper, "foreachToSend", foreach_to_send)
    monkeypatch.setattr(ProcessCache, "update_process", lambda value: None)
    monkeypatch.setattr(ProcessCache, "update_type_text", lambda value: None)
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "completeItemSummery",
        lambda *args: "summary",
    )
    monkeypatch.setattr(AutoWorkerWrapper, "print_summery", lambda value: None)
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "is_privateAd_available",
        lambda auto: False,
    )
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "is_globalAd_available",
        lambda args: False,
    )
    async def fake_obtain(client, auto):
        return True, [{"id": 1}]

    monkeypatch.setattr(auto_worker_module, "obtainMessageAndParse", fake_obtain)

    async def biz_sleep(low, high):
        sleeps.append((low, high))

    monkeypatch.setattr(BizSleeper, "biz_sleep", biz_sleep)
    monkeypatch.setattr(Working, "need_stop", False)

    bean = object()
    asyncio.run(inner_working(None, None, autoBeans=[bean]))
    assert sleeps == [(2, 5)]


def test_foreach_to_send_does_not_publish_ads():
    source = inspect.getsource(AutoWorkerWrapper.foreachToSend)
    assert "process_ad_second_to_last" not in source
    assert "publish_private_ad" not in source
    assert "publish_global_ad" not in source


def test_inner_working_publishes_ads_once(monkeypatch):
    calls = []

    async def foreach_to_send(auto, client, parse_list, args_wrapper, **kwargs):
        return (4, 1, 1, [])

    async def publish_private(*args):
        calls.append("private")

    async def publish_global(*args):
        calls.append("global")

    monkeypatch.setattr(AutoWorkerWrapper, "foreachToSend", foreach_to_send)
    monkeypatch.setattr(ProcessCache, "update_process", lambda value: None)
    monkeypatch.setattr(ProcessCache, "update_type_text", lambda value: None)
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "completeItemSummery",
        lambda *args: "summary",
    )
    monkeypatch.setattr(AutoWorkerWrapper, "print_summery", lambda value: None)
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "is_privateAd_available",
        lambda auto: True,
    )
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "is_globalAd_available",
        lambda args: True,
    )
    monkeypatch.setattr(AutoWorkerWrapper, "publish_private_ad", publish_private)
    monkeypatch.setattr(AutoWorkerWrapper, "publish_global_ad", publish_global)
    monkeypatch.setattr(BizSleeper, "biz_sleep", lambda *args: None)
    monkeypatch.setattr(Working, "need_stop", False)

    async def fake_obtain(client, auto):
        return True, [{"id": 1}]

    monkeypatch.setattr(auto_worker_module, "obtainMessageAndParse", fake_obtain)
    bean = types.SimpleNamespace(
        adIsBottomUp=lambda: False,
        selfAdWrapper=None,
    )

    asyncio.run(inner_working(None, None, autoBeans=[bean]))
    assert calls == ["private", "global"]


def test_inner_working_converts_beans_by_mode(monkeypatch):
    source_bean = object()
    converted_bean = object()
    converted_calls = []
    foreach_beans = []
    sq_r_ca = types.ModuleType("_sq_r_ca")

    async def convert(mode, beans):
        converted_calls.append((mode, list(beans)))
        return [converted_bean]

    sq_r_ca.convert_batch_with_retry = convert
    monkeypatch.setattr(fea_pkg, "_sq_r_ca", sq_r_ca, raising=False)

    async def foreach_to_send(auto, client, parse_list, args_wrapper, **kwargs):
        foreach_beans.append(auto)
        return (4, 1, 1, [])

    monkeypatch.setattr(AutoWorkerWrapper, "foreachToSend", foreach_to_send)
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "process_ad_second_to_last",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(ProcessCache, "update_process", lambda value: None)
    monkeypatch.setattr(ProcessCache, "update_type_text", lambda value: None)
    monkeypatch.setattr(BizSleeper, "biz_sleep", lambda *args: None)
    monkeypatch.setattr(Working, "need_stop", False)
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "completeItemSummery",
        lambda *args: "summary",
    )
    monkeypatch.setattr(AutoWorkerWrapper, "print_summery", lambda value: None)
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "is_privateAd_available",
        lambda auto: False,
    )
    monkeypatch.setattr(
        AutoWorkerWrapper,
        "is_globalAd_available",
        lambda args: False,
    )
    async def fake_obtain(client, auto):
        return True, [{"id": 1}]

    monkeypatch.setattr(auto_worker_module, "obtainMessageAndParse", fake_obtain)

    args = types.SimpleNamespace(convert_mode="timing")
    asyncio.run(
        inner_working(
            None,
            args,
            autoBeans=[source_bean],
        )
    )
    assert converted_calls == [("timing", [source_bean])]
    assert foreach_beans == [converted_bean]


def test_obtain_message_fetches_and_parses(monkeypatch):
    from src.py.com.yun.mao.cd import Working
    from src.py.com.yun.mao.fea import _dtdm_gl
    from src.py.com.yun.mao.fea import _yjx_hb_file
    from src.py.com.yun.mao.link import _lk_gy_w

    calls = []

    async def fetch(client, auto):
        calls.append(("fetch", auto.kid))
        return [{"id": 1}]

    async def parse(auto, messages, is_monitor=False):
        calls.append(("parse", len(messages), is_monitor))
        return _yjx_hb_file.YjxHb.success([{"id": 3}])

    monkeypatch.setattr(_dtdm_gl, "dt_hq_fn", lambda *args: fetch)
    monkeypatch.setattr(_yjx_hb_file, "yp_jx_pd_ch", parse)
    monkeypatch.setattr(_lk_gy_w, "gy_jc_a1", lambda obj: True)
    monkeypatch.setattr(Working, "need_stop", False)

    auto = types.SimpleNamespace(
        kid="kid-1",
        model="",
        text_model="",
        getSource=lambda: "@source",
        getName=lambda: "demo",
        is_random_mode=lambda: False,
        is_increase_mode=lambda: False,
    )
    result = asyncio.run(
        obtainMessageAndParse(
            None,
            auto,
            resultBean="result-bean",
        )
    )
    assert result == (True, [{"id": 3}])
    assert calls == [("fetch", "kid-1"), ("parse", 1, False)]


def test_obtain_message_retries_random_bucket(monkeypatch):
    from src.py.com.yun.mao.ai import TextCache
    from src.py.com.yun.mao.cd import Working
    from src.py.com.yun.mao.fea import _dtdm_gl
    from src.py.com.yun.mao.fea import _yjx_hb_file
    from src.py.com.yun.mao.link import _lk_gy_w
    from src.py.com.yun.mao.remember import RandomBucketManager

    calls = []
    cleared = []
    parsed = []

    async def fetch(client, auto):
        calls.append("fetch")
        return [{"id": 1}]

    async def parse(auto, messages, is_monitor=False):
        parsed.append(len(messages))
        if len(parsed) == 1:
            return _yjx_hb_file.YjxHb.success([])
        return _yjx_hb_file.YjxHb.success([{"id": 3}])

    monkeypatch.setattr(_dtdm_gl, "dt_hq_fn", lambda *args: fetch)
    monkeypatch.setattr(_yjx_hb_file, "yp_jx_pd_ch", parse)
    monkeypatch.setattr(_lk_gy_w, "gy_jc_a1", lambda obj: True)
    monkeypatch.setattr(Working, "need_stop", False)
    monkeypatch.setattr(
        RandomBucketManager,
        "clear_session_tried_ranges",
        lambda source, kid="": cleared.append((source, kid)),
    )
    monkeypatch.setattr(
        RandomBucketManager,
        "session_tried_range_count",
        lambda source, kid="": 2,
    )
    TextCache.ALL_MESSAGE_FAILED_LIST.clear()

    auto = types.SimpleNamespace(
        kid="kid-1",
        model="model",
        text_model="text_model",
        getSource=lambda: "@source",
        getName=lambda: "demo",
        is_random_mode=lambda: True,
        is_increase_mode=lambda: False,
    )
    result = asyncio.run(obtainMessageAndParse(None, auto))

    assert result == (True, [{"id": 3}])
    assert calls == ["fetch", "fetch"]
    assert parsed == [1, 1]
    assert cleared == [("@source", "kid-1")]
    assert len(TextCache.ALL_MESSAGE_FAILED_LIST) == 1


def test_foreach_to_send_records_publish_mapping(monkeypatch):
    calls = []
    sleeps = []
    sent_result = types.SimpleNamespace(
        send_count=1,
        send_group=1,
        send_success_count=1,
        dest_id_map={"@dest": [7]},
        preview_id_map=None,
        real_time_message_id=0,
        need_break=False,
        need_sleep=False,
    )

    def record_mapping(auto, parse, group_result, convert_mode=None):
        calls.append((auto, parse, group_result, convert_mode))

    async def send_group(auto, client, parse, args_wrapper):
        return sent_result

    async def no_ad(*args, **kwargs):
        return None

    async def biz_sleep(low, high):
        sleeps.append((low, high))

    monkeypatch.setattr(AutoWorkerWrapper, "append_if_complete", record_mapping)
    monkeypatch.setattr(AutoWorkerWrapper, "processBanYunSendWrapper", send_group)
    monkeypatch.setattr(AutoWorkerWrapper, "process_ad_second_to_last", no_ad)
    monkeypatch.setattr(BizSleeper, "biz_sleep", biz_sleep)
    monkeypatch.setattr(Working, "need_stop", False)

    auto = types.SimpleNamespace(
        isBanYunType=True,
        getSource=lambda: "@source",
        name="demo",
        destes=["@dest"],
        yulan_destes=[],
    )
    parse = types.SimpleNamespace(messages=[types.SimpleNamespace(id=99)])
    args = types.SimpleNamespace(convert_mode="timing")

    asyncio.run(
        AutoWorkerWrapper.foreachToSend(
            auto,
            None,
            [parse],
            args,
        )
    )

    assert calls == [(auto, parse, sent_result, "timing")]
    assert sleeps == []
