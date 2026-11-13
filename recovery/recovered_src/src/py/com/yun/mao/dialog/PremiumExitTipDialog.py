# Recovered module: src.py.com.yun.mao.dialog.PremiumExitTipDialog
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

from PyQt5 import uic

from ..util import ResourcePath
from ..util.need.BaseDialog import BaseDialog


class PremiumExitTipDialog(BaseDialog):
    def __init__(self, parent=None, close_fun=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("订单关闭确认通知")
        uic.loadUi(ResourcePath.get_ui_path("premium_exit_tip_dialog.ui"), self)
        self.close_fun = close_fun

        def m_wait_fun() -> None:
            self.close()

        def m_close_fun() -> None:
            if callable(self.close_fun):
                self.close_fun()
            self.accept()

        self.btn_wait.clicked.connect(m_wait_fun)
        self.btn_close.clicked.connect(m_close_fun)

    def showEvent(self, a0) -> None:
        self.setWindowTitle(self.windowTitle())
        self.setFixedSize(650, 300)
        super().showEvent(a0)
