# Recovered module: src.py.com.yun.mao.util.need.BaseDialog
# Behaviour-level reconstruction from Nuitka constants and offline Hex-Rays.
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from .. import ResourcePath
from . import utils


class BaseDialog(QDialog):
    MINI_TIP_WIDTH = 650
    MINI_TIP_HEIGHT = 300

    def __init__(
        self,
        parent=None,
        windowTitle: str = "",
    ) -> None:
        super().__init__(parent)
        self.setWindowModality(Qt.NonModal)
        if windowTitle:
            self.setWindowTitle(windowTitle)
        self.setWindowIcon(
            QIcon(ResourcePath.get_ico_path("normal_256.ico"))
        )
        self.resize(1400, 1000)

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        icon1 = QIcon(ResourcePath.get_ico_path("normal_256.ico"))
        self.setWindowIcon(icon1)

    def setup_mini_tip_window(
        self,
        w: int = MINI_TIP_WIDTH,
        h: int = MINI_TIP_HEIGHT,
        parent=None,
    ) -> None:
        self.setFixedSize(w, h)
        if parent is None:
            parent = self.parentWidget()
        if parent is not None and parent.isVisible():
            pg = parent.frameGeometry()
            x = pg.x() + (pg.width() - w) // 2
            y = pg.y() + (pg.height() - h) // 2
        else:
            screen_width, screen_height = utils.get_screen_size()
            x = (int(screen_width) - w) // 2
            y = (int(screen_height) - h) // 2
        self.move(x, y)
