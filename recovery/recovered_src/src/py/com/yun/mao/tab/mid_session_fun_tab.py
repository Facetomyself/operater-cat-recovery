# Recovered module: src.py.com.yun.mao.tab.mid_session_fun_tab
# Telegram account/session management tab.  Menu, dialog and queue calls are
# reconstructed from the module constants; retry sleeps remain inferred.
from __future__ import annotations

from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QMenu

from ..cd import Working
from ..dialog.ReceiveCodeDialog import ReceiveCodeDialog
from ..login import NetTest
from ..tgaccount.TGAuthAccount import TGAuthAccount
from ..tgaccount import TGAuthAccountSetting
from ..util.need import ListOpHelper, ShotUtils, signals
from ..util.need.AllBeanDef import FilterSessionItem
from .gen_session_queue import GenSessionQueue
from .mid_base_tab import MidBaseTab


def _tip(text: str) -> None:
    try:
        signals.global_ui_signal.tip_dialog_cmd.emit(str(text or ""))
    except Exception:
        print(text)


def _connect(widget: Any, signal_name: str, slot: Any) -> None:
    try:
        signal = getattr(widget, signal_name, None)
        if signal is not None:
            signal.connect(slot)
    except Exception:
        return None


def _changed_widget(widget: Any, enable: bool) -> None:
    if widget is None:
        return
    try:
        widget.setEnabled(bool(enable))
    except Exception:
        return None
    changed = getattr(ShotUtils, "changed_widget", None)
    if callable(changed):
        try:
            changed(widget, enable=enable)
        except Exception:
            return None


def _main_ui(tab: Any) -> Any:
    return getattr(getattr(tab, "mainWindow", None), "ui", None)


def _open_proxy_setting(tab: Any) -> None:
    try:
        from ..proxy.ProxySettingDialog import ProxySettingDialog

        ProxySettingDialog(tab.mainWindow).exec_()
    except Exception as exc:
        print("打开代理设置失败：", exc)
    reset = getattr(_main_ui(tab), "action_reset", None)
    if reset is not None:
        try:
            reset.trigger()
        except Exception as exc:
            print("重置代理界面失败：", exc)


def _account_from_data(data: Any) -> Any:
    account = getattr(data, "account", None)
    if isinstance(data, list):
        for value in data:
            if isinstance(value, TGAuthAccount):
                return value
    if isinstance(data, dict):
        account = data.get("account", data)
    if account is None and isinstance(data, FilterSessionItem):
        account = data
    return account if account is not None else data


class SessionFunTab(MidBaseTab):
    UPDATE_REN_SLEEP_MIN = 2
    UPDATE_REN_SLEEP_MAX = 5

    def __init__(self, mainWindow: Any, ui: Any) -> None:
        super().__init__()
        self.mainWindow = mainWindow
        self.ui = ui
        self.item_data_list: list[Any] = []
        self.gen_session_queue = GenSessionQueue()
        self._receive_code_dialog = None
        self.init()

    def init(self) -> None:
        _connect(
            getattr(self.ui, "btn_send_yan_zhen_ma", None),
            "clicked",
            self.request_code,
        )
        _connect(
            getattr(self.ui, "btn_login_gen_session", None),
            "clicked",
            self.phone_login,
        )
        _connect(
            getattr(self.ui, "btn_refresh_account", None),
            "clicked",
            self.refresh_account,
        )
        _connect(
            getattr(self.ui, "btn_net_test", None),
            "clicked",
            self.net_test,
        )
        update_signal = getattr(
            signals.global_ui_signal, "update_account_list", None
        )
        if update_signal is not None:
            try:
                update_signal.connect(self.refresh_account)
            except Exception as exc:
                print("连接账号刷新信号失败：", exc)

        list_widget = getattr(self.ui, "listWidget_account_list", None)
        if list_widget is not None:
            list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            _connect(
                list_widget,
                "customContextMenuRequested",
                self.shoeAccountMenu,
            )

        _connect(
            getattr(_main_ui(self), "btn_proxy_setting", None),
            "clicked",
            lambda: _open_proxy_setting(self),
        )
        _changed_widget(getattr(_main_ui(self), "cb_enable_proxy", None), True)
        self.init_session_list()

    def changedAutoTaskWidgetStatus(self, enable: bool) -> None:
        _changed_widget(
            getattr(_main_ui(self), "tabWidget_important", None),
            enable,
        )

    def net_test(self) -> None:
        Working.Session_Working = True
        self.changedAutoTaskWidgetStatus(False)

        def finish_call(success: bool, *_args: Any) -> None:
            Working.Session_Working = False
            self.changedAutoTaskWidgetStatus(True)
            if success:
                _tip("连接测试成功！")
            else:
                _tip("连接测试失败，请检查代理网络！")

        fast_test = getattr(NetTest, "FastNetTest", None)
        test = getattr(NetTest, "NetTest", None)
        try:
            if callable(fast_test):
                fast_test(finish_call)
            elif callable(test):
                test(finish_call)
            else:
                finish_call(False)
        except Exception as exc:
            print("网络测试失败：", exc)
            finish_call(False)

    def shoeAccountMenu(self, pos: Any) -> None:
        widget = getattr(self.ui, "listWidget_account_list", None)
        if widget is None:
            return
        item = widget.itemAt(pos)
        if item is None:
            return
        data = item.data(Qt.UserRole)
        if data is None:
            return
        menu = QMenu(widget)
        receive = QAction("接码", menu)
        receive.triggered.connect(
            lambda _=False, d=item.data(Qt.UserRole): self.showReceiveCode(d)
        )
        menu.addAction(receive)
        delete = QAction("删除", menu)
        delete.triggered.connect(
            lambda _=False, d=item.data(Qt.UserRole): self.deleteItem(d)
        )
        menu.addAction(delete)
        menu.exec_(widget.mapToGlobal(pos))

    def showReceiveCode(self, data: Any) -> None:
        dialog = self._receive_code_dialog
        if dialog is not None:
            try:
                if dialog.isVisible():
                    _tip("已有接码窗口，不能同时接码多个账号！")
                    dialog.raise_()
                    dialog.activateWindow()
                    return
            except Exception:
                self._receive_code_dialog = None
        worker = getattr(dialog, "_worker", None)
        if worker is not None and getattr(worker, "isRunning", lambda: False)():
            _tip("正在停止接码，请稍候再试！")
            return
        account = _account_from_data(data)
        try:
            self._receive_code_dialog = ReceiveCodeDialog(self.mainWindow, account)
            self._receive_code_dialog.finished.connect(
                self._on_receive_code_dialog_finished
            )
            self._receive_code_dialog.show()
        except Exception as exc:
            print("打开接码窗口失败：", exc)

    def _on_receive_code_dialog_finished(self, *_args: Any) -> None:
        self._clear_receive_code_dialog()

    def _clear_receive_code_dialog(self) -> None:
        self._receive_code_dialog = None

    def deleteItem(self, data: Any) -> None:
        account = _account_from_data(data)
        nick = str(getattr(account, "nick", "") or "")
        session_file = getattr(account, "session", "")
        try:
            TGAuthAccountSetting.deleteSession(session_file)
        except Exception as exc:
            print("删除账号失败：", exc)
            return
        print("删除搬运流成功 ", nick)
        self.refresh_account()

    def refresh_account(self, *_args: Any) -> None:
        try:
            account_list = TGAuthAccountSetting.getTgAccountList()
        except Exception:
            account_list = []
        list_widget = getattr(self.ui, "listWidget_account_list", None)
        if list_widget is not None:
            list_widget.clear()
        self.item_data_list = list(account_list or [])
        self.fillListView()
        _tip("刷新完成！")

    def init_session_list(self) -> None:
        self.refresh_account()

    def fillListView(self) -> None:
        widget = getattr(self.ui, "listWidget_account_list", None)
        if widget is None:
            return
        try:
            ListOpHelper.fillAccountListView(widget, self.item_data_list)
        except Exception:
            widget.clear()
            for data in self.item_data_list:
                account = _account_from_data(data)
                widget.addItem(
                    str(
                        getattr(account, "nick", "")
                        or getattr(account, "username", "")
                        or "账号"
                    )
                )

    def get_phone(self) -> str:
        widget = getattr(self.ui, "lineEdit_input_phone", None)
        if widget is None:
            return ""
        return str(widget.text() or "").strip().replace(" ", "")

    def request_code(self) -> None:
        if bool(getattr(Working, "Session_Working", False)):
            _tip("任务正在进行中，暂不能操作！")
            return
        shot = getattr(ShotUtils, "shot", None)
        if callable(shot):
            try:
                shot()
            except Exception:
                return None
        phone = self.get_phone()
        if not phone:
            _tip("请输入手机号")
            return
        self.gen_session_queue.requestCode(phone)

    def phone_login(self) -> None:
        phone = self.get_phone()
        if not phone:
            _tip("请输入手机号")
            return
        code_widget = getattr(self.ui, "lineEdit_yan_zhen_ma", None)
        two_pass_widget = getattr(self.ui, "lineEdit_two_pass_word", None)
        code = str(code_widget.text() if code_widget is not None else "").strip()
        if not code:
            _tip("请输入验证码")
            return
        two_pass = str(
            two_pass_widget.text() if two_pass_widget is not None else ""
        ).strip()

        def phone_login_callback(text: str) -> None:
            _tip(str(text or ""))

        def finish_call(success: bool, name: str = "") -> None:
            if success:
                code_widget.setText("") if code_widget is not None else None
                _tip("添加账号成功！")
                self.refresh_account()
            else:
                _tip("正在登录中...")
            _ = name

        self.gen_session_queue.phoneLogin(
            phone,
            code,
            two_pass,
            phone_login_callback,
            finish_call,
        )


__all__ = ["SessionFunTab"]
