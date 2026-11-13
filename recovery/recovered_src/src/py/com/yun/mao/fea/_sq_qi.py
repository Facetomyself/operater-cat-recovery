# Recovered module: src.py.com.yun.mao.fea._sq_qi
# Startup/register flow reconstructed from the module constants and varnames.
from __future__ import annotations


from PyQt5.QtCore import QRunnable

from . import _sq_jqm, _sq_req, _sq_r_qi
from ..link._fds_jm import sec
from ..link._fds_h_x import FdsHhx
from ..util import TracePrinterHelper
from ..util.need import CommonCode, FakeUniqueMachineCode, signals


class SqQiTask(QRunnable):
    def __init__(self):
        super().__init__()

    def run(self):
        return qd_qi_dong()


def qd_cl_jg(can_enter_main_window: bool, probe=None) -> bool:
    """Entry gate before the main window is allowed to open."""
    if can_enter_main_window:
        return True
    try:
        return not (probe or FdsHhx()).entry_blocked()
    except Exception:
        return True


def qd_qi_dong():
    """Start the startup probe and registration flow."""
    try:
        probe = FdsHhx()
        if not qd_cl_jg(not probe.entry_blocked(), probe):
            signals.global_ui_signal.cmd_env_checked_result.emit(
                False, sec("hj_restart_07")
            )
            return False
        probe.fh_ui_qd()
        result = s_b_i_kaishi()
        signals.global_ui_signal.cmd_env_checked_result.emit(True, "")
        return result
    except Exception:
        try:
            TracePrinterHelper.print_trace(sec("hj_restart_07"))
        except Exception:
            pass
        signals.global_ui_signal.cmd_env_checked_result.emit(False, "")
        return False


def s_b_i_kaishi():
    """Boot the account or auto-register path."""
    try:
        boot = _sq_r_qi.qd_r_spi_boot()
        if boot is not None:
            return boot
        ucode = _sq_jqm.current_account_info.ucode
        if not ucode:
            pre = CommonCode.read_ucode_pre()
            ucode = FakeUniqueMachineCode.gen_fake_unique_machine_code()
            _ = pre, ucode
            return _sq_req.sq_zc(
                pre=pre,
                fake=ucode,
            )
        return _sq_req.sq_jy_ma(ucode, callback_need_await=True)
    except Exception:
        return False


def zc_hz_dl_rol():
    """Post-registration hook used when the local account is empty."""
    try:
        return _sq_r_qi.qd_r_zc_after_register(success=True)
    except Exception:
        return None
