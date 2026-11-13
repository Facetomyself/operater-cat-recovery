# Recovered module: src.py.com.yun.mao.fea._jc_dd_cz_file
# Check-order-and-recharge task.
from __future__ import annotations

import asyncio

from PyQt5.QtCore import QRunnable

from . import _sq_req
from ..link._fds_jm import sec
from ..util import TracePrinterHelper
from ..util.need import signals


class CheckOrderRechargeTask(QRunnable):
    def __init__(self, args=None):
        super().__init__()
        self.args = args or ()

    def run(self) -> None:
        start_check_order(*self.args)


def start_check_order_call_back(success: bool, content_oj=None) -> None:
    try:
        payload = None
        if isinstance(content_oj, dict):
            payload = content_oj.get("data", content_oj)
        signals.global_ui_signal.cmd_check_order_stats.emit(bool(success), payload)
    except Exception:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass


def start_check_order(*args):
    print(sec("lk_ex_pre_01"))
    try:
        return asyncio.run(start_check_order_inner(*args))
    except Exception as exc:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass
        _ = exc
        start_check_order_call_back(False, None)
        return None


async def start_check_order_inner(*args):
    try:
        result = _sq_req.CheckOrderAndRecharge(*args)
        if asyncio.iscoroutine(result):
            result = await result
        if isinstance(result, tuple):
            success = bool(result[0]) if result else False
            content_oj = result[1] if len(result) > 1 else None
        else:
            success = bool(result)
            content_oj = result
        start_check_order_call_back(success, content_oj)
        return success
    except Exception as exc:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass
        _ = exc
        start_check_order_call_back(False, None)
        return False
