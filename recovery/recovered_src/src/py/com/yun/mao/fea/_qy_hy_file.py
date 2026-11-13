# Recovered module: src.py.com.yun.mao.fea._qy_hy_file
# Code-migration task and UI status bridge.
from __future__ import annotations

import asyncio

from PyQt5.QtCore import QRunnable

from . import _sq_req
from ..link._fds_jm import sec
from ..util import TracePrinterHelper
from ..util.need import signals, utils


class FeaMigrateCodeTask(QRunnable):
    def __init__(self, args=None):
        super().__init__()
        self.args = args or ()

    def run(self) -> None:
        start_migrate_code(*self.args)


def fetch_call_back(
    success: bool,
    content_oj=None,
    ucode: str = "",
    startTime: str = "",
    endTime: str = "",
    error_msg: str = "",
) -> None:
    try:
        if success:
            shown_ucode = ucode
            try:
                shown_ucode = utils.un_mask_ucode(ucode)
            except Exception:
                pass
            print(
                sec("qy_ok_tpl_01").format(
                    shown_ucode,
                    startTime,
                    endTime,
                )
            )
            signals.global_ui_signal.cmd_migrate_code_stats.emit(True, "")
        else:
            if not error_msg and isinstance(content_oj, dict):
                error_msg = str(content_oj.get("msg", ""))
            print(sec("qy_fail_tpl_03").format(error_msg))
            signals.global_ui_signal.cmd_migrate_code_stats.emit(
                False,
                error_msg,
            )
    except Exception:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass


def start_migrate_code(*args):
    print(sec("lk_ex_pre_01"))
    try:
        return asyncio.run(start_migrate_code_inner(*args))
    except Exception as exc:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass
        _ = exc
        fetch_call_back(False, None, error_msg=str(exc))
        return None


async def start_migrate_code_inner(
    old_u_code: str = "",
    new_u_code: str = "",
    cover_expri: bool = False,
    force_cover_yun: bool = False,
):
    try:
        result = _sq_req.sq_qy_dm(
            old_u_code,
            new_u_code,
            cover_expri,
            force_cover_yun,
        )
        if asyncio.iscoroutine(result):
            result = await result
        if isinstance(result, tuple):
            success = bool(result[0]) if result else False
            content_oj = result[1] if len(result) > 1 else None
        else:
            success = bool(result)
            content_oj = result
        data = content_oj.get("data", {}) if isinstance(content_oj, dict) else {}
        fetch_call_back(
            success,
            content_oj,
            ucode=str(data.get("ucode", new_u_code)),
            startTime=str(data.get("startRechargeTime", "")),
            endTime=str(data.get("endRechargeTime", "")),
            error_msg=str(
                content_oj.get("msg", "")
                if isinstance(content_oj, dict)
                else ""
            ),
        )
        return success
    except Exception as exc:
        try:
            TracePrinterHelper.print_trace(sec("lk_ex_pre_01"))
        except Exception:
            pass
        fetch_call_back(False, None, error_msg=str(exc))
        return False
