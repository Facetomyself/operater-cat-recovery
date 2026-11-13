# Recovered module: src.py.com.yun.mao.monitor.HistoryMessageOpDialog
# Behaviour-level reconstruction from the module constants, method signatures,
# and offline Hex-Rays output.
from __future__ import annotations

from typing import Any

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QListWidgetItem

from ..util import ResourcePath
from ..util.need import utils
from ..util.need.AllBeanDef import MonitorTgMessageBean
from ..util.need.BaseDialog import BaseDialog
from .QHistoryMsgItemQWidget import QHistoryMsgItemQWidget


class HistoryMessageOpDialog(BaseDialog):
    def __init__(
        self,
        parent=None,
        history_map: Any = None,
        confirm_callback: Any = None,
    ) -> None:
        super().__init__(parent, "历史监听未处理完成的消息")
        self.history_map = history_map or {}
        self.confirm_callback = confirm_callback
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("history_message_list_op.ui"),
            self,
        )
        view = self._widget("history_list_view")
        if view is not None:
            self.history_list_view = view
        button = self._widget("btn_confirm_monitor")
        if button is not None:
            button.clicked.connect(self.confirm_callback_wrapper)
        self.fill_history()

    def _widget(self, name: str):
        widget = getattr(self, name, None)
        if widget is None and self.ui is not None:
            widget = getattr(self.ui, name, None)
        return widget

    def confirm_callback_wrapper(self) -> None:
        callback = self.confirm_callback
        try:
            if callable(callback):
                callback(True)
        except Exception:
            if callable(callback):
                try:
                    callback(False)
                except Exception:
                    pass
        finally:
            self.close()

    def fill_history(self) -> None:
        view = self._widget("history_list_view") or self._widget("history_message_list")
        if view is None:
            return
        history = self.history_map or {}
        if isinstance(history, dict):
            grouped = {str(key): list(value or []) for key, value in history.items()}
        else:
            grouped: dict[str, list] = {}
            for item in history:
                if isinstance(item, MonitorTgMessageBean):
                    key = str(getattr(item, "safeSource", "") or "")
                elif isinstance(item, dict):
                    key = str(item.get("safeSource", "") or "")
                else:
                    key = ""
                grouped.setdefault(key, []).append(item)
        for autoBeanName, msgs in grouped.items():
            messages = list(msgs or [])
            safe_source = autoBeanName
            if messages:
                first = messages[0]
                safe_source = str(
                    getattr(first, "safeSource", "")
                    or (first.get("safeSource", "") if isinstance(first, dict) else "")
                    or autoBeanName
                )
            customQWidget = QHistoryMsgItemQWidget()
            customQWidget.bindData(str(autoBeanName), len(messages), safe_source)
            item = QListWidgetItem()
            item.setSizeHint(customQWidget.sizeHint())
            view.addItem(item)
            view.setItemWidget(item, customQWidget)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        screen_width, screen_height = utils.get_screen_size()
        # Recovered factors: width 3/5, height 7/10, center x /2, center y /6.
        window_width = int(screen_width * 3 / 5)
        window_height = int(screen_height * 7 / 10)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 6)
        self.resize(window_width, window_height)
        self.move(x_position, y_position)
