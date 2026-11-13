# Recovered module: src.py.com.yun.mao.dialog.ReceiveCodeDialog
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

import os

from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication

from ..cd import TaskHardStop, Working
from ..config import YunYinMaoConfig
from ..mthread.ReceiveCodeThread import ReceiveCodeThread
from ..util import ResourcePath
from ..util.need import signals
from ..util.need.BaseDialog import BaseDialog


def phone_digits_for_copy(phone: str) -> str:
    return "".join(ch for ch in str(phone or "") if ch.isdigit())


class ReceiveCodeDialog(BaseDialog):
    _CODE_PREFIX = "接收到的验证码："
    _EMPTY_DISPLAY = "（未设置）"
    _DIALOG_WIDTH = 540
    _DIALOG_HEIGHT = 300

    def __init__(self, main_window=None, account=None) -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.account = account
        self.setWindowTitle("接码")
        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("receive_code_dialog.ui"), self
        )
        self._worker = None
        self._closed = False
        self._holding_session = False
        self._bind_account_identity()
        self.btn_start_receive.clicked.connect(self._on_start)
        self.btn_stop_receive.clicked.connect(self._on_stop)
        self.btn_copy_phone.clicked.connect(self._on_copy_phone)
        self._set_idle_buttons()

    @staticmethod
    def _make_copy_icon() -> QIcon:
        size = 20
        pix = QPixmap(size, size)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#e6e6e6"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(7, 2, 11, 12, 2, 2)
        painter.setBrush(QColor("#4a4e52"))
        painter.drawRoundedRect(2, 6, 11, 12, 2, 2)
        painter.end()
        return QIcon(pix)

    def _bind_account_identity(self) -> None:
        nick = str(getattr(self.account, "nick", "") or "").strip()
        phone = phone_digits_for_copy(getattr(self.account, "phone", ""))
        self.ui.lb_account_name.setText(nick or self._EMPTY_DISPLAY)
        self.ui.lb_phone.setText(phone or self._EMPTY_DISPLAY)
        self.ui.btn_copy_phone.setIcon(self._make_copy_icon())
        self.ui.btn_copy_phone.setIconSize(QSize(18, 18))
        self.ui.btn_copy_phone.setToolTip("复制手机号")

    def showEvent(self, a0) -> None:
        self.setWindowTitle(self.windowTitle())
        self.setFixedSize(self._DIALOG_WIDTH, self._DIALOG_HEIGHT)
        super().showEvent(a0)

    def _set_idle_buttons(self) -> None:
        self.ui.btn_start_receive.setEnabled(True)
        self.ui.btn_stop_receive.setEnabled(False)

    def _set_busy_buttons(self) -> None:
        self.ui.btn_start_receive.setEnabled(False)
        self.ui.btn_stop_receive.setEnabled(True)

    def _session_abs_path(self) -> str:
        abs_session_file = (
            str(YunYinMaoConfig.abs_tg_account_dir())
            + "\\"
            + str(getattr(self.account, "session_file", "") or "")
        )
        if not os.path.isfile(abs_session_file):
            print("session 文件不存在：", abs_session_file)
        return abs_session_file

    def _on_copy_phone(self) -> None:
        phone = phone_digits_for_copy(getattr(self.account, "phone", ""))
        if not phone:
            print("复制失败：当前账号没有有效手机号")
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(phone)
        if clipboard.text() != phone:
            print("复制失败：无法写入剪贴板")
            return
        print("成功复制手机号：", phone)

    def _on_start(self) -> None:
        worker = self._worker
        if worker is not None and worker.isRunning():
            return
        if Working.Session_Working:
            signals.global_ui_signal.tip_dialog_cmd.emit(
                "任务正在进行中，暂不能操作！"
            )
            return
        abs_session_file = self._session_abs_path()
        if not os.path.isfile(abs_session_file):
            signals.global_ui_signal.tip_dialog_cmd.emit(
                "当前账号 session 文件不存在！"
            )
            return
        Working.Session_Working = True
        self._holding_session = True
        self.ui.lb_receive_code.setText(self._CODE_PREFIX)
        self._set_busy_buttons()
        worker = ReceiveCodeThread(abs_session_file)
        worker.code_signal.connect(self._on_code)
        worker.status_signal.connect(self._on_status)
        worker.finished.connect(self._on_worker_finished)
        self._worker = worker
        worker.start()
        sync_stop_state = getattr(
            TaskHardStop, "sync_worker_stop_state", None
        )
        if callable(sync_stop_state):
            sync_stop_state()

    def _on_stop(self) -> None:
        self._stop_worker()

    def _on_code(self, code: str) -> None:
        if self._closed:
            return
        text = (self._CODE_PREFIX + str(code or "")).strip()
        print(text)
        self.ui.lb_receive_code.setText(text)

    def _on_status(self, status: str) -> None:
        if self._closed:
            return
        if status == "login_failed":
            signals.global_ui_signal.tip_dialog_cmd.emit(
                "接码登录失败，请查看日志后重试！"
            )

    def _on_worker_finished(self) -> None:
        untrack_worker = getattr(TaskHardStop, "untrack_worker", None)
        if callable(untrack_worker):
            untrack_worker()
        self._worker = None
        self._release_working()
        if not self._closed:
            self._set_idle_buttons()

    def _stop_worker(self) -> None:
        worker = self._worker
        self._release_working()
        self._set_idle_buttons()
        if worker is not None:
            worker.request_stop()
            worker.wait(2000)
        sync_stop_state = getattr(
            TaskHardStop, "sync_worker_stop_state", None
        )
        if callable(sync_stop_state):
            sync_stop_state()

    def _release_working(self) -> None:
        if self._holding_session:
            Working.Session_Working = False
            self._holding_session = False

    def closeEvent(self, event) -> None:
        self._closed = True
        worker = self._worker
        if worker is not None and worker.isRunning():
            self._release_working()
            worker.request_stop()
            worker.wait(2000)
            sync_stop_state = getattr(
                TaskHardStop, "sync_worker_stop_state", None
            )
            if callable(sync_stop_state):
                sync_stop_state()
        event.accept()

    def reject(self) -> None:
        self.close()
