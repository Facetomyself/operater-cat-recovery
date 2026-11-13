# Recovered module: src.py.com.yun.mao.util.need.TipDialog
# Behaviour-level reconstruction from Nuitka constants, .ui XML, and Hex-Rays.
from __future__ import annotations

import os
import sys

from PyQt5 import QtGui, uic
from PyQt5.QtGui import QCloseEvent

from .. import ResourcePath
from . import utils
from .BaseDialog import BaseDialog


NORMAL_SIZE = 1
LARGE_SIZE = 2


class TipDialog(BaseDialog):
    def __init__(
        self,
        parent=None,
        tip: str = "",
        size: int = NORMAL_SIZE,
        restart: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("提示")
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("tip_dialog.ui"), self
        )
        self.tip = tip
        self.size = size
        self.restart = restart
        self.ui.lb_tip.setText(tip)
        self.ui.btn_kown.setText("重启软件" if restart else "我明白了")
        self.ui.btn_kown.clicked.connect(self.clickIKown)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.setWindowTitle(self.windowTitle())
        screen_width, screen_height = utils.get_screen_size()
        # Recovered factors: large 5.0/6 x 2.5/6, normal 1.2/4 x 1.5/6.
        if self.size == LARGE_SIZE:
            window_width = int(screen_width * 5.0 / 6.0)
            window_height = int(screen_height * 2.5 / 6.0)
        else:
            window_width = int(screen_width * 1.2 / 4.0)
            window_height = int(screen_height * 1.5 / 6.0)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.resize(window_width, window_height)
        self.move(x_position, y_position)
        super().showEvent(a0)

    def clickIKown(self) -> None:
        if self.restart:
            self.restart_app()
            return
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.restart:
            event.ignore()
            return
        event.accept()

    def reject(self) -> None:
        if self.restart:
            self.restart_app()
            return
        super().reject()

    def restart_app(self) -> None:
        os.execl(sys.executable, sys.executable, *sys.argv)
