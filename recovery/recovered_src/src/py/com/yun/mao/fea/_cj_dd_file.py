# Recovered module: src.py.com.yun.mao.fea._cj_dd_file
# Asynchronous create-order task and UI signal bridge.
from __future__ import annotations

import asyncio

from PyQt5.QtCore import QRunnable

from . import _sq_req
from ..link._fds_jm import sec
from ..util import TracePrinterHelper
from ..util.need import signals


class CreateOrderTask(QRunnable):
    def __init__(self, args=None):
        super().__init__()
        self.args = args or ()

    def run(self) -> None:
        start_create_order(*self.args)


def _result_parts(result):
    if isinstance(result, tuple):
        if len(result) >= 2 and isinstance(result[0], bool):
            return result[0], result[1]
        if result:
            return bool(result[0]), result[1] if len(result) > 1 else None
    return bool(result), result


def create_order_call_back(
    success: bool,
    content_oj=None,
    order=None,
) -> None:
    """Dispatch the create-order result to the UI."""
    try:
        if success:
            payload = order
            if payload is None and isinstance(content_oj, dict):
                payload = content_oj.get("data", content_oj)
            signals.global_ui_signal.cmd_create_order_success.emit(payload)
        else:
            msg = ""
            if isinstance(content_oj, dict):
                msg = str(content_oj.get("msg", ""))
            signals.global_ui_signal.cmd_create_order_failed.emit(msg)
    except Exception:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass


def start_create_order(*args):
    print(sec("lk_ex_pre_01"))
    try:
        return asyncio.run(start_create_order_inner(*args))
    except Exception as exc:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass
        _ = exc
        create_order_call_back(False, None)
        return None


async def start_create_order_inner(*args):
    try:
        result = _sq_req.createOrder(*args)
        if asyncio.iscoroutine(result):
            result = await result
        success, content_oj = _result_parts(result)
        order = None
        if success:
            if isinstance(content_oj, dict):
                order = content_oj.get("data", content_oj)
            else:
                order = content_oj
        create_order_call_back(success, content_oj, order)
        return order
    except Exception as exc:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass
        create_order_call_back(False, None)
        _ = exc
        return None
