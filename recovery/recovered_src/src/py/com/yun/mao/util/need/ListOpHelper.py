# Recovered module: src.py.com.yun.mao.util.need.ListOpHelper
# QListWidget population helpers.  UI classes are imported lazily so the
# module stays importable in the offline test environment.
from __future__ import annotations

try:
    from PyQt5.QtCore import QSize
    from PyQt5.QtGui import QColor
    from PyQt5.QtWidgets import QListWidgetItem
except Exception:
    class QSize:
        def __init__(self, *args):
            self.args = args

    class QColor:
        @staticmethod
        def fromRgb(*args):
            return args

    class QListWidgetItem:
        def __init__(self, text="", parent=None):
            self._text = text
            self._data = {}
            self._size = None

        def setForeground(self, color):
            self._color = color

        def setSizeHint(self, size):
            self._size = size

        def setData(self, role, value):
            self._data[role] = value

        def text(self):
            return self._text


def filter_session_item_to_ui_account_data(source_list, f=None):
    result = []
    for item in source_list or []:
        try:
            if f is None or f(item):
                result.append(item)
        except Exception:
            continue
    return result


def convert_employee_to_show_item_data(employee):
    from .AllBeanDef import AiEmployeeShowItemData

    return AiEmployeeShowItemData(
        uid=int(getattr(employee, "uid", 0) or 0),
        aiBean=employee,
    )


def addHeader(qlist_widget, tranTime, tranType, text, list_item=None):
    item = list_item or QListWidgetItem(str(text))
    try:
        item.setForeground(QColor.fromRgb(247, 176, 7))
        item.setSizeHint(QSize(200, 50))
    except Exception:
        pass
    try:
        qlist_widget.addItem(item)
    except Exception:
        pass
    return item


def fillAccountListView(qlist_widget, ui_data_list):
    try:
        qlist_widget.clear()
    except Exception:
        pass
    for data in ui_data_list or []:
        account = getattr(data, "account", None)
        text = (
            getattr(account, "phone", None)
            or getattr(account, "unin_id", None)
            or str(data)
        )
        item = QListWidgetItem(str(text))
        try:
            item.setData(0, data)
        except Exception:
            pass
        addHeader(qlist_widget, None, None, text, item)
    return None


def fillEmployeeListView(qlist_widget, ui_data_list, onItemClicked=None):
    try:
        qlist_widget.clear()
    except Exception:
        pass
    for index, data in enumerate(ui_data_list or []):
        bean = getattr(data, "aiBean", None)
        text = getattr(bean, "name", None) or getattr(bean, "uid", None) or ""
        item = QListWidgetItem(str(text))
        try:
            item.setData(0, data)
        except Exception:
            pass
        addHeader(qlist_widget, None, None, text, item)
        if callable(onItemClicked):
            try:
                onItemClicked(index, data)
            except TypeError:
                try:
                    onItemClicked(item)
                except Exception:
                    pass
    return None


def fillYunYinMaoItemListView(
    qlist_widget,
    bean_list,
    onItemClicked=None,
):
    try:
        qlist_widget.clear()
    except Exception:
        pass
    for index, bean in enumerate(bean_list or []):
        text = str(
            getattr(bean, "name", None)
            or getattr(bean, "kid", None)
            or getattr(bean, "id", None)
            or ""
        )
        item = QListWidgetItem(text)
        try:
            item.setData(0, bean)
        except Exception:
            pass
        addHeader(qlist_widget, None, None, text, item)
        if callable(onItemClicked):
            try:
                onItemClicked(index, bean)
            except TypeError:
                try:
                    onItemClicked(item)
                except Exception:
                    pass
    return None


def setALLSelect(checkBox, select_all: bool):
    if checkBox is None:
        return None
    try:
        checkBox.blockSignals(True)
        checkBox.setChecked(bool(select_all))
        checkBox.blockSignals(False)
    except Exception:
        pass
    return None
