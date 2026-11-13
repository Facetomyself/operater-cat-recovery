# Recovered module: src.py.com.yun.mao.fea._zz_jh_ty_file
# Self-service activation-code task.
from __future__ import annotations

import asyncio

from PyQt5.QtCore import QRunnable

from . import _sq_jqm, _sq_req
from ..link._fds_jm import sec
from ..util import TracePrinterHelper
from ..util.need import signals


class SelfActivatePermissionTask(QRunnable):
    def __init__(self, args=None):
        super().__init__()
        self.args = args or ()

    def run(self) -> None:
        self_activate_permission(*self.args)


def fetch_call_back(success: bool, hours: int = 0, tip_str: str = "") -> None:
    try:
        if success:
            print(sec("ty_ok_short_02"))
            signals.global_ui_signal.cmd_activate_code_stats.emit(True)
            if hours:
                tip = (
                    '<div style="color: #e0e0e0; font-family: Microsoft YaHei, '
                    'sans-serif; line-height: 1.5; font-size: 12pt;">'
                    + sec("ty_ok_tip_03")
                    + sec("ty_hours_tpl_04").format(hours=hours)
                    + "</div>"
                )
                try:
                    signals.global_ui_signal.tip_dialog_cmd.emit(tip)
                except Exception:
                    _ = tip
            elif tip_str:
                try:
                    signals.global_ui_signal.tip_dialog_cmd.emit(tip_str)
                except Exception:
                    pass
        else:
            signals.global_ui_signal.cmd_activate_code_stats.emit(False)
            print(sec("ty_fail_retry_05"))
    except Exception:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass


def self_activate_permission(*args):
    print(sec("lk_ex_pre_01"))
    try:
        return asyncio.run(self_activate_permission_inner(*args))
    except Exception as exc:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass
        fetch_call_back(False, 0, str(exc))
        return None


async def self_activate_permission_inner(u_code: str = "", *args):
    try:
        result = _sq_req.sq_ty_jh(u_code, *args)
        if asyncio.iscoroutine(result):
            result = await result
        if isinstance(result, tuple):
            success = bool(result[0]) if result else False
            content_oj = result[1] if len(result) > 1 else None
        else:
            success = bool(result)
            content_oj = result
        hours = 0
        tip_str = ""
        if isinstance(content_oj, dict):
            data = content_oj.get("data", content_oj)
            if isinstance(data, dict):
                hours = int(data.get("hours", 0) or 0)
                tip_str = str(data.get("tip", ""))
            if success:
                try:
                    hours = int(
                        _sq_jqm.current_account_info.get_experi_duration_hours()
                    )
                except Exception:
                    pass
        fetch_call_back(success, hours, tip_str)
        return success
    except Exception as exc:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass
        fetch_call_back(False, 0, str(exc))
        return False
