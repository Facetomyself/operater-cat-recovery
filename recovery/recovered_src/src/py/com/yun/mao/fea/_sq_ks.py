# Recovered module: src.py.com.yun.mao.fea._sq_ks
# Startup/account-check flow reconstructed from the module constants and
# runtime signatures.
from __future__ import annotations


from PyQt5.QtCore import QRunnable, QThreadPool

from . import _sq_chk, _sq_jqm, _sq_req
from ..link._fds_jm import sec
from ..link._fds_rt import fs_by_pf
from ..util import TracePrinterHelper
from ..util.need import signals


class KjJyTask(QRunnable):
    def __init__(self, ui_call_back=None):
        super().__init__()
        self.ui_call_back = ui_call_back

    def run(self):
        self.start_checker()

    def start_checker(self):
        print(sec("lk_ex_pre_01"))
        return self.start_checker_inner()

    def start_checker_inner(self):
        if _sq_chk.ihy_nome():
            return True
        if _sq_chk.hy_dj():
            signals.global_ui_signal.report_status_waring.emit(
                sec("jqm_zh_jy_fail_06")
            )
        return False

    def kj_yh_cb(self, success):
        if self.ui_call_back:
            self.ui_call_back(bool(success))


class KjSbTask(QRunnable):
    def __init__(self):
        super().__init__()

    def run(self):
        return start_report_inner()


def check_account_without_loop(check_call_back):
    """Run the local account check and invoke the callback."""
    try:
        fs_by_pf()
        _ucode = _sq_jqm.current_account_info.ucode

        def inner_call_back(success):
            return check_call_back(bool(success))

        success = _sq_chk.hy_ne()
        inner_call_back(success)
        return success
    except Exception:
        try:
            TracePrinterHelper.print_trace(sec("jqm_no_local_14"))
        except Exception:
            pass
        check_call_back(False)
        return False


def kj_by_jy(check_call_back):
    return check_account_without_loop(check_call_back)


def kj_ks_sb():
    task = KjSbTask()
    QThreadPool.globalInstance().start(task)
    return task


def kj_qd_sb():
    task = KjJyTask()
    QThreadPool.globalInstance().start(task)
    return task


def start_report_inner():
    """Report the local account state; network details live in _sq_req."""
    try:
        if not _sq_chk.ihy_nome():
            return False
        result = _sq_req.sq_jy_ma(
            _sq_jqm.current_account_info.ucode,
            callback_need_await=True,
        )
        return bool(result)
    except Exception:
        return False
