# Recovered module: src.py.com.yun.mao.dialog.CourseImageDialog
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
"""Course image viewer.

Recovered: 1080x768 minimum size, horizontal center /2, vertical center /8.
"""
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from ..util.AppStyleDef import APP_ALL_STYLE_DEF
from ..util.need import utils
from ..util.need.BaseDialog import BaseDialog


class CourseImageDialog(BaseDialog):
    def __init__(self, parent=None, images=None, title: str = "图片对话框") -> None:
        super().__init__(parent)
        self.setStyleSheet(APP_ALL_STYLE_DEF)
        self.images = list(images or [])
        self.current_index = 0
        self.setWindowTitle(title)
        self.setMinimumSize(1080, 768)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        self.label.setMinimumSize(self.width(), self.height())

        font_btn = QFont()
        font_btn.setPointSize(14)

        self.prev_btn = QPushButton("上一页", self)
        self.prev_btn.setFixedSize(100, 30)
        self.prev_btn.setFont(font_btn)
        self.prev_btn.clicked.connect(self.prev_image)

        self.next_btn = QPushButton("下一页", self)
        self.next_btn.setFixedSize(100, 30)
        self.next_btn.setFont(font_btn)
        self.next_btn.clicked.connect(self.next_image)

        self.current_label = QLabel(self)
        self.current_label.setAlignment(Qt.AlignCenter)
        self.current_label.setFixedSize(100, 30)
        font_label = QFont()
        font_label.setPointSize(14)
        self.current_label.setFont(font_label)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.current_label)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addStretch()
        layout.addLayout(nav_layout)
        self.setLayout(layout)

        self.show_image()

    def show_image(self) -> None:
        if not self.images:
            self.current_label.setText("0/0")
            return
        pixmap = QPixmap(self.images[self.current_index])
        if pixmap.isNull():
            print("图片加载失败！请检查路径。")
        self.label.setPixmap(pixmap)
        self.update_current_label()

    def update_current_label(self) -> None:
        self.current_label.setText(
            str(self.current_index + 1) + "/" + str(len(self.images))
        )

    def prev_image(self) -> None:
        if not self.images:
            return
        self.current_index = (self.current_index - 1) % len(self.images)
        self.show_image()

    def next_image(self) -> None:
        if not self.images:
            return
        self.current_index = (self.current_index + 1) % len(self.images)
        self.show_image()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        screen_width, screen_height = utils.get_screen_size()
        x_position = int((screen_width - self.width()) / 2)
        y_position = int((screen_height - self.height()) / 8)
        self.resize(self.width(), self.height())
        self.move(x_position, y_position)
