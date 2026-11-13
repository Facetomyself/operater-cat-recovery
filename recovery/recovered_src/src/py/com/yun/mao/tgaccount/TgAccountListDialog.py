# Recovered module: src.py.com.yun.mao.tgaccount.TgAccountListDialog
# Behaviour-level reconstruction from Nuitka constants and the UI XML.
from __future__ import annotations

from PyQt5 import QtGui, uic

from ..util import ResourcePath
from ..util.need import ListOpHelper, signals
from ..util.need.AllBeanDef import FilterSessionItem, ListUIAccountShowItemData
from . import TGAuthAccountSetting
from .TGAuthAccount import TGAuthAccount

try:
    from ..util.need.BaseDialog import BaseDialog
except (ImportError, AttributeError):
    from PyQt5.QtWidgets import QDialog as BaseDialog


class TgAccountListDialog(BaseDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.selected_account = None
        self.setWindowTitle("选择账号")
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("account_list_dialog.ui"),
            self,
        )
        self.ui.qlist_view.itemClicked.connect(self.onItemClicked)
        self.init_session_list()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.setWindowTitle(self.windowTitle())
        self.setFixedSize(300, 700)
        super().showEvent(a0)

    def init_session_list(self) -> None:
        self.item_data_list: list[ListUIAccountShowItemData] = []
        accounts = TGAuthAccountSetting.getTgAccountList() or []
        for source in accounts:
            if isinstance(source, FilterSessionItem):
                key = source.session_abs_path
                account = getattr(source, "account", None)
                values = ""
            elif isinstance(source, dict):
                account_values = {
                    name: source.get(name)
                    for name in (
                        "session_file",
                        "session",
                        "nick",
                        "phone",
                        "userName",
                    )
                }
                if not account_values["userName"]:
                    account_values["userName"] = source.get("username")
                account = TGAuthAccount(**account_values)
                key = (
                    account.session_file
                    or account.session
                    or account.userName
                    or account.phone
                )
                values = account.phone or account.userName
            else:
                account = source
                key = (
                    getattr(account, "session_file", None)
                    or getattr(account, "session", None)
                    or getattr(account, "userName", None)
                    or getattr(account, "phone", None)
                )
                values = (
                    getattr(account, "phone", None)
                    or getattr(account, "userName", None)
                )
            if account is None:
                continue
            custom_item = ListUIAccountShowItemData(
                unin_id=str(key or values or ""),
                select=False,
                account=account,
            )
            self.item_data_list.append(custom_item)
        self.fillListView()

    def fillListView(self) -> None:
        ListOpHelper.fillAccountListView(
            self.ui.qlist_view,
            self.item_data_list,
        )

    def onItemClicked(self, item) -> None:
        data = item.data(32)
        account = getattr(data, "account", data)
        self.selected_account = account
        print(
            "选择 ",
            getattr(account, "nick", ""),
            "",
            " ",
            getattr(account, "phone", ""),
        )
        signals.global_ui_signal.cmd_select_tg_account.emit(account)
        self.close()
