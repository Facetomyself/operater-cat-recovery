from __future__ import annotations

try:
    from PyQt5 import uic
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtWidgets import QWidget
except Exception:
    uic = None
    Qt = None
    QPixmap = None

    class QWidget:
        def __init__(self, parent=None):
            self.parent = parent


from ..ResourcePath import drawable_is_exists, get_drawable_path, get_ui_path


class FlowItemWidgetBase(QWidget):
    UI_NAME = ""
    TYPE_TEXT = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = None
        self.active = True
        self.data = None
        self.index = 0
        if uic is not None and self.UI_NAME:
            try:
                self.ui = uic.loadUi(get_ui_path(self.UI_NAME), self)
            except Exception:
                self.ui = None

    def _label(self, name):
        value = getattr(self, name, None)
        if value is None and self.ui is not None:
            value = getattr(self.ui, name, None)
        return value

    def _set_text(self, name, value):
        try:
            self._label(name).setText(str(value if value is not None else ""))
        except Exception:
            pass

    def _set_visible(self, name, visible):
        try:
            self._label(name).setVisible(bool(visible))
        except Exception:
            pass

    def setActive(self, active):
        self.active = bool(active)
        return None

    def setSelect(self, select):
        check = self._label("checkBox_select")
        try:
            check.setChecked(bool(select))
        except Exception:
            pass
        return None

    def bindData(self, data=None, index=0):
        self.data = data
        self.index = int(index or 0)
        self.updateAutoBeanUI()
        return self

    def ai_is_enable(self) -> bool:
        data = self.data
        bean = getattr(data, "beanLike", None) or data
        employee = getattr(bean, "aiEmployee", None)
        return bool(getattr(employee, "enable", employee))

    def display_ai_icon(self, data=None, icon_name="ai_text_icon_enable.png"):
        label = self._label("label_ai_icon")
        try:
            if not drawable_is_exists(icon_name):
                label.clear()
                return None
            pixmap = QPixmap(get_drawable_path(icon_name))
            try:
                pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio)
            except Exception:
                pass
            label.setPixmap(pixmap)
        except Exception:
            pass
        return None

    def displayActionLabel(self):
        data = self.data
        bean = getattr(data, "beanLike", None) or data
        action = getattr(bean, "action", "")
        self._set_text("label_action", f"动作：{action}" if action else "")
        return None

    def updateAutoBeanUI(self):
        data = self.data
        bean = getattr(data, "beanLike", None) or data
        self._set_text("label_xu_hao", f"序号：{self.index}")
        self._set_text("dl_label_xu_hao", f"序号：{self.index}")
        self._set_text("label_lei_xin", f"类型：{self.TYPE_TEXT} ")
        self._set_text("dl_label_lei_xin", f"类型：{self.TYPE_TEXT} ")
        name = getattr(bean, "name", "")
        source = getattr(bean, "source", "")
        dtype = getattr(bean, "dtype", "")
        model = getattr(bean, "auto_desc", "")
        self._set_text("label_name", f"名称：{name}")
        self._set_text("label_source", f"来源：{source}")
        self._set_text("label_dtpye", f"资源类型：{dtype}")
        self._set_text("label_model", f"模式选择：{model}")
        self._set_text("dl_label_name", f"名称：{name}")
        self._set_text("dl_label_source", f"来源：{source}")
        self._set_text("dl_label_dtpye", f"资源类型：{dtype}")
        self._set_text("dl_label_model", f"模式选择：{model}")
        self._set_text("label_priority", getattr(bean, "priority", ""))
        self._set_text("label_action", getattr(bean, "action", ""))
        self._set_text("label_dest", getattr(bean, "destes", ""))
        self._set_text("label_yulan_dest", getattr(bean, "yulan_destes", ""))
        self._set_text("label_yun_auto_dest", getattr(bean, "yulan_destes", ""))
        self._set_text("label_duration", getattr(bean, "baseFilter", ""))
        self._set_text("dl_label_filter_max", getattr(bean, "baseFilter", ""))
        return None

    def setData(self, *args):
        if len(args) >= 2:
            self.index, self.data = args[0], args[1]
        elif args:
            self.data = args[0]
        self.updateAutoBeanUI()
        return None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
