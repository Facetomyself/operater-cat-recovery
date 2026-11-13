# Recovered module: src.py.com.yun.mao.cd.ConditionalTabWidget
from __future__ import annotations

try:
    from PyQt5.QtCore import QEvent
    from PyQt5.QtWidgets import QTabWidget
except Exception:
    class QTabWidget:
        def __init__(self, parent=None):
            self.parent = parent

        def tabBar(self):
            return None

        def installEventFilter(self, obj):
            return None

        def eventFilter(self, obj, event):
            return False

    class QEvent:
        MouseButtonPress = 2


class ConditionalTabWidget(QTabWidget):
    def __init__(self, parent=None, can_changed_tab=None):
        super().__init__(parent)
        self.tab_condition_met = can_changed_tab
        self.tab_widget = self
        self.can_changed_tab = can_changed_tab
        try:
            self.tabBar().installEventFilter(self)
        except Exception:
            pass

    def eventFilter(self, obj, event):
        try:
            if (
                obj is self.tabBar()
                and event.type() == QEvent.MouseButtonPress
                and callable(self.tab_condition_met)
                and not self.tab_condition_met()
            ):
                return True
        except Exception:
            pass
        return super().eventFilter(obj, event)
