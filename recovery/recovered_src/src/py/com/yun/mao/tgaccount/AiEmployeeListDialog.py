# Recovered module: src.py.com.yun.mao.tgaccount.AiEmployeeListDialog
# Behaviour-level reconstruction from Nuitka constants and the UI XML.
from __future__ import annotations

from PyQt5 import QtGui, uic

from ..dclass import LoadEmployeeClass
from ..util import ResourcePath
from ..util.need import ListOpHelper
from ..util.need.AllBeanDef import AiEmployeeBean, AiEmployeeShowItemData

try:
    from ..util.need.BaseDialog import BaseDialog
except (ImportError, AttributeError):
    from PyQt5.QtWidgets import QDialog as BaseDialog


class AiEmployeeListDialog(BaseDialog):
    def __init__(self, parent=None, select_employee_callback=None) -> None:
        super().__init__(parent)
        self.select_employee_callback = select_employee_callback
        self.setWindowTitle("选择AI员工")
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("ai_employee_list_dialog.ui"),
            self,
        )
        self.ui.qlist_view.itemClicked.connect(self.onItemClicked)
        self.init_ai_employee_list()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.setWindowTitle(self.windowTitle())
        self.setFixedSize(300, 700)
        super().showEvent(a0)

    def init_ai_employee_list(self) -> None:
        self.ui_data_item_list: list[AiEmployeeShowItemData] = []
        values = LoadEmployeeClass.getEmployeeMap().items()
        for _, auto in values:
            self.ui_data_item_list.append(
                ListOpHelper.convert_employee_to_show_item_data(auto)
            )
        self.fillListView()

    def fillListView(self) -> None:
        ListOpHelper.fillEmployeeListView(
            self.ui.qlist_view,
            self.ui_data_item_list,
        )

    def onItemClicked(self, item) -> None:
        data = item.data(32)
        custom_item: AiEmployeeBean = getattr(data, "aiBean", data)
        print("选择 ", getattr(custom_item, "name", ""), "")
        callback = self.select_employee_callback
        if callable(callback):
            callback(custom_item)
        self.close()
