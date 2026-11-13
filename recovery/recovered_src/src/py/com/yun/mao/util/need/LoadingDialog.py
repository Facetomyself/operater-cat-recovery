# Recovered module: src.py.com.yun.mao.util.need.LoadingDialog
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QFont, QIcon, QShowEvent
from PyQt5.QtWidgets import QLabel, QVBoxLayout

from .. import ResourcePath
from . import utils
from .BaseDialog import BaseDialog


class LoadingDialog(BaseDialog):
    WIDTH = 360
    HEIGHT = 140

    def __init__(
        self,
        parent=None,
        tip: str = "请稍候...",
    ) -> None:
        super().__init__(parent)
        self._can_close = False
        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(
            Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint
        )
        self.setWindowIcon(
            QIcon(ResourcePath.get_ico_path("normal_256.ico"))
        )
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self.label = QLabel(tip, self)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.label)
        layout.addStretch(1)
        self.setLayout(layout)
        self._center()

    def showEvent(self, a0: QShowEvent) -> None:
        self._center()
        super().showEvent(a0)

    def _center(
        self,
        w: int | None = None,
        h: int | None = None,
        parent=None,
    ) -> None:
        width = self.WIDTH if w is None else int(w)
        height = self.HEIGHT if h is None else int(h)
        self.setWindowTitle(self.windowTitle())
        if parent is None:
            parent = self.parentWidget()
        if parent is not None and parent.isVisible():
            pg = parent.frameGeometry()
            x = pg.x() + (pg.width() - width) // 2
            y = pg.y() + (pg.height() - height) // 2
        else:
            screen_width, screen_height = utils.get_screen_size()
            x = (int(screen_width) - width) // 2
            y = (int(screen_height) - height) // 2
        self.move(x, y)

    def allow_close(self) -> None:
        self._can_close = True

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._can_close:
            event.accept()
            return
        event.ignore()

    def reject(self) -> None:
        if self._can_close:
            super().reject()

