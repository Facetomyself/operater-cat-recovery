# Recovered module: src.py.com.yun.mao.monitor.QHistoryMsgItemQWidget
# Behaviour-level reconstruction from the module constants, method signatures,
# and offline Hex-Rays output.
from __future__ import annotations

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from ..util import ResourcePath
from .MonitorHistoryManagerFile import MonitorHistoryManager


class QHistoryMsgItemQWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.autoBeanName = ""
        self.safeSource = ""
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("q_history_item_widget.ui"),
            self,
        )
        self._set_text("label_name", "")
        self._set_text("label_size", "0")
        button = self._widget("btn_clean_history")
        if button is not None:
            button.clicked.connect(self.clean_history)

    def _widget(self, name: str):
        widget = getattr(self, name, None)
        if widget is None and self.ui is not None:
            widget = getattr(self.ui, name, None)
        return widget

    def _set_text(self, name: str, value: str) -> None:
        label = self._widget(name)
        setter = getattr(label, "setText", None)
        if callable(setter):
            setter(str(value))

    def bindData(self, autoBeanName: str, size: int, safeSource: str) -> None:
        self.autoBeanName = str(autoBeanName or "")
        self.safeSource = str(safeSource or "")
        self._set_text("label_name", self.autoBeanName)
        self._set_text("label_size", str(int(size or 0)))

    def clean_history(self) -> None:
        MonitorHistoryManager().clean_monitor_message_list(self.safeSource)
        self._set_text("label_size", "0")
        print(self.autoBeanName + " 历史监听数据清除成功！")
