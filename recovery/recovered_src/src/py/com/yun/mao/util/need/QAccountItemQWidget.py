# Recovered module: src.py.com.yun.mao.util.need.QAccountItemQWidget
from __future__ import annotations

try:
    from PyQt5 import uic
    from PyQt5.QtWidgets import QWidget
except Exception:
    uic = None

    class QWidget:
        def __init__(self, parent=None):
            self.parent = parent
            self.label_nick = None
            self.label_phone = None


from ..ResourcePath import get_ui_path
from .AllBeanDef import ListUIAccountShowItemData


class QAccountItemQWidget(QWidget):
    def __init__(self, data: ListUIAccountShowItemData | None = None, parent=None):
        super().__init__(parent)
        self.ui = None
        if uic is not None:
            try:
                self.ui = uic.loadUi(get_ui_path("user_item_widget.ui"), self)
            except Exception:
                self.ui = None
        self.setData(data)

    def setData(self, data):
        self.data = data
        account = getattr(data, "account", None)
        nick = getattr(account, "nick", "") if account is not None else ""
        phone = getattr(account, "phone", "") if account is not None else ""
        for attr, value in (("label_nick", nick), ("label_phone", phone)):
            label = getattr(self, attr, None) or getattr(self.ui, attr, None) if self.ui else getattr(self, attr, None)
            try:
                label.setText(str(value or ""))
            except Exception:
                pass
        return None
