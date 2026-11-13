# Recovered module: src.py.com.yun.mao.ErrorDialog
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

from . import GlobalExceptionHandler


def show_error_tip(error_msg: str, timeout: int = 5000) -> None:
    msg_box = QMessageBox(GlobalExceptionHandler.global_window)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("错误")
    msg_box.setText(str(error_msg))
    ok_button = msg_box.addButton(QMessageBox.Ok)
    _ = ok_button
    timer = QTimer(msg_box)
    timer.setSingleShot(True)
    timer.timeout.connect(msg_box.close)
    timer.start(int(timeout))
    msg_box.exec_()
    timer.stop()
    msg_box.deleteLater()
