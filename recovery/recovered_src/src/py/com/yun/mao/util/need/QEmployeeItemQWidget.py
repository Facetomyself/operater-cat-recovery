# Recovered module: src.py.com.yun.mao.util.need.QEmployeeItemQWidget
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


class QEmployeeItemQWidget(QWidget):
    def __init__(self, data=None, parent=None):
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
        bean = getattr(data, "aiBean", None)
        name = getattr(bean, "name", "") if bean is not None else ""
        for attr, value in (("label_nick", name), ("label_phone", "")):
            label = getattr(self, attr, None)
            if label is None and self.ui is not None:
                label = getattr(self.ui, attr, None)
            try:
                label.setText(str(value or ""))
            except Exception:
                pass
        return None
