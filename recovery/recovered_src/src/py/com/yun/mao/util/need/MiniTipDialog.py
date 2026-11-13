# Recovered module: src.py.com.yun.mao.util.need.MiniTipDialog
# Behaviour-level reconstruction from Nuitka constants and .ui XML.
from __future__ import annotations

from PyQt5 import QtGui, uic

from .. import ResourcePath
from .BaseDialog import BaseDialog


class MiniTipDialog(BaseDialog):
    def __init__(
        self,
        parent=None,
        mini_fun=None,
        tray_fun=None,
        ext_fun=None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("退出提示")
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("mini_tip_dialog.ui"), self
        )

        def m_mini_fun() -> None:
            if callable(mini_fun):
                mini_fun()
            self.hide()

        def m_tray_fun() -> None:
            if callable(tray_fun):
                tray_fun()
            self.hide()

        def m_ext_fun() -> None:
            if callable(ext_fun):
                ext_fun()
            self.hide()

        self.ui.btn_mini.clicked.connect(m_mini_fun)
        self.ui.btn_tray.clicked.connect(m_tray_fun)
        self.ui.btn_ext.clicked.connect(m_ext_fun)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.setup_mini_tip_window()
        super().showEvent(a0)
