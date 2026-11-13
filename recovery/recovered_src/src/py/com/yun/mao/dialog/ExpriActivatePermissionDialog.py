# Recovered module: src.py.com.yun.mao.dialog.ExpriActivatePermissionDialog
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

from typing import Callable

from PyQt5 import uic
from PyQt5.QtCore import QThreadPool

from ..fea import _sq_jqm
from ..fea._zz_jh_ty_file import SelfActivatePermissionTask
from ..util import ResourcePath
from ..util.need import ShotUtils, signals, utils
from ..util.need.AllBeanDef import ActivateCodeBean
from ..util.need.BaseDialog import BaseDialog


AdHtmlCallbackType = Callable[[list[str]], None]


class ExpriActivatePermissionDialog(BaseDialog):
    def __init__(
        self,
        parent=None,
        windowTitle: str | None = None,
        hours: int | None = None,
    ) -> None:
        super().__init__(parent)
        if windowTitle:
            self.setWindowTitle(windowTitle)
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("self_experience_dialog.ui"), self
        )
        self.btn_activate_permission.clicked.connect(self.activate_permission)
        self.btn_activate_cancel.clicked.connect(self.activate_cancel)
        self.hours = int(
            hours
            if hours is not None
            else _sq_jqm.current_account_info.get_experi_duration_hours()
        )
        self.label_activate_text.setText(self._get_trial_tip_html(self.hours))
        signals.global_ui_signal.cmd_activate_code_stats.connect(
            self.on_dialog_activate_code_stats
        )

    def _get_trial_tip_html(self, hours: int) -> str:
        return (
            '\n    <div style="color: #f0f0f0; font-family: \'Microsoft YaHei\', sans-serif; line-height: 1.6;">\n'
            '        <h3 style="\n'
            '            margin: 0 0 18pt 0;\n'
            '            padding-bottom: 8pt;\n'
            '            color: #40c4ff;\n'
            '            font-size: 19pt;\n'
            '            font-weight: 600;\n'
            '            text-align: center;\n'
            '            border-bottom: 1pt solid #444;\n'
            '        ">\n'
            "            🎉 恭喜获得体验会员激活权限\n"
            "        </h3>\n"
            "\n"
            '        <div style="font-size: 14.5pt; color: #bbb; margin-bottom: 16pt;">\n'
            "            请仔细阅读以下重要提示：\n"
            "        </div>\n"
            "        <br>\n"
            '        <div style="font-size: 12pt;">\n'
            '            • <span style="color: #ff5252; font-weight: bold;">重要！</span> 体验机会<span style="color: #ff5252; font-weight: bold;">仅限一次</span>，激活后不可重复领取<br><br>\n'
            "\n"
            '            • 体验时长：<span style="color: #00e0d0; font-size: 20pt; font-weight: bold;">'
            + str(hours)
            + ''
            + "小时</span><br><br>\n"
            "\n"
            '            • 现在有 【<strong>'
            + str(hours)
            + '小时</strong>】 完整时间？ → <strong style="color: #00ff9a;">建议「立即激活体验」</strong><br><br>\n'
            "\n"
            '            • 目前较忙/没准备好？ → <strong style="color: #ffca28;">请务必选择「以后再激活」</strong><br><br>\n'
            "\n"
            '            <span style="color: #ff5252; font-weight: bold;">最后一次提醒：机会只有一次！</span><br><br>\n'
            "            \n"
            '            <span style="color: #b4b4b4; font-size:10pt;">在软件顶部右侧点击【激活体验】可以唤出这个弹窗</span>\n'
            "            \n"
            "        </div>\n"
            "    </div>\n"
            "    "
        )

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        screen_width, screen_height = utils.get_screen_size()
        window_width = int(screen_width / 2)
        window_height = int(screen_height / 6)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 10)
        self.setFixedSize(window_width, window_height)
        self.move(x_position, y_position)

    def on_dialog_activate_code_stats(self, success: bool) -> None:
        if success:
            self.close()

    def activate_cancel(self) -> None:
        self.close()

    def activate_permission(self) -> None:
        """
        inferred: the three ShotUtils.shot calls are present in the constants,
        but the exact widget/enable pairing is not visible in the decompiler.
        """
        ShotUtils.shot(self.ui.btn_activate_permission)
        ShotUtils.shot(self.ui.btn_activate_cancel)
        ShotUtils.shot(self.ui)
        uCode = _sq_jqm.current_account_info.ucode
        task = SelfActivatePermissionTask(ActivateCodeBean(uCode))
        QThreadPool.globalInstance().start(task)
