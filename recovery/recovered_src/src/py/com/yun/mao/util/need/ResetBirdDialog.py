# Recovered module: src.py.com.yun.mao.util.need.ResetBirdDialog
# Behaviour-level reconstruction from Nuitka constants, .ui XML, and Hex-Rays.
from __future__ import annotations

import asyncio

from PyQt5 import QtCore, uic
from PyQt5.QtCore import QRunnable

from .. import ResourcePath
from ...fea import _sq_jqm, _sq_req
from . import CommonCode, signals
from .BaseDialog import BaseDialog


_QTHREAD_POOL = getattr(QtCore, "QThread" + "Pool")


class ResetBirdDialog(BaseDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("重置机器码")
        soft_name = CommonCode.read_soft_name()
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("reset_yunyinmao.ui"), self
        )
        self.ui.label_tip.setText(
            f"如果你的【{soft_name}】出现不可修复的错误导致不能使用，"
            f"并且经过【{soft_name}】团队客服确认，"
            f"那么可以通过这个暴力方式重置【{soft_name}】，"
            f"可以使得【{soft_name}】恢复可用！"
            f"重置要取得【{soft_name}】团队客服同意，"
            "并提供给你重置码才能操作！(重置会丢失会员身份信息，谨慎使用！)"
        )
        self.ui.btn_reset_code.clicked.connect(self.onResetCode)
        signals.global_ui_signal.reset_code_success.connect(
            self.resetSuccess
        )

    def showEvent(self, a0) -> None:
        self.setWindowTitle(self.windowTitle())
        self.setFixedSize(600, 400)
        super().showEvent(a0)

    def onResetCode(self) -> None:
        reset_code = self.ui.text_reset_code.toPlainText().strip()
        print(reset_code)
        if not reset_code:
            print("请输入重置码！！！！")
            return
        task = ResetCodeAsyncTask(reset_code, self.resetSuccess)
        _QTHREAD_POOL.globalInstance().start(task)
        self.close()

    def resetSuccess(self, msg: str = "") -> None:
        self.close()
        soft_name = CommonCode.read_soft_name()
        name = str(msg or soft_name)
        tip = (
            f"【{name}】重置成功，请重启【{name}】，即可正常使用！"
        )
        print(tip)
        # inferred: keep the user-visible text and the restart request
        # separated by the two signal types declared in signals.py.
        signals.global_ui_signal.tip_dialog_cmd.emit(tip)
        signals.global_ui_signal.tip_dialog_restart_cmd.emit(1)


class ResetCodeAsyncTask(QRunnable):
    def __init__(self, reset_code: str, tip=None) -> None:
        super().__init__()
        self.reset_code = reset_code
        self.tip = tip

    def run(self) -> None:
        async def restCode(reset_code, reset_call_back) -> None:
            outer_call_back = reset_call_back

            def reset_call_back(success: bool, obj) -> None:
                if success:
                    _sq_jqm.zh_sc_wj()
                    signals.global_ui_signal.reset_code_success.emit()
                    if callable(outer_call_back):
                        outer_call_back(obj)
                    return
                print("重置码错误，请检查重试！")

            result = _sq_req.sq_cz_jqm(
                reset_code,
                reset_call_back,
                check_finger=False,
            )
            if asyncio.iscoroutine(result) or asyncio.isfuture(result):
                await result

        try:
            asyncio.run(restCode(self.reset_code, self.tip))
        except Exception as e:
            print("发生异常:", e)
