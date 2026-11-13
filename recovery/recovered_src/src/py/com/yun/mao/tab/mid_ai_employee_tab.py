# Recovered module: src.py.com.yun.mao.tab.mid_ai_employee_tab
# AI employee list controller.  Widget names, callbacks and cache keys are
# exact module constants; small adapter choices are marked inferred.
from __future__ import annotations

from typing import Any

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QAction, QMenu

from ..ai.AI_DEFAULT_REFUSE_LIST import get_default_token
from ..config import tabl_cache
from ..dclass.LoadDataClass import getAutoMap
from ..dclass.LoadEmployeeClass import (
    deleteAiEmployeeBean,
    getEmployeeMap,
)
from ..dialog import ImageDialogHelper
from ..fea import _sq_jqm
from ..util.XAIKeyValidator import XAIKeyValidator
from ..util.need import ListOpHelper, signals, utils
from ..util.need.AllBeanDef import AiEmployeeBean, AiEmployeeShowItemData
from ..util.need.EditEmployeeItemEditDialog import EditEmployeeItemEditDialog
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


def _cache() -> Any:
    return tabl_cache.INSTANCE()


def _bean_from_item(item: Any) -> Any:
    if item is None:
        return None
    data = item.data(Qt.UserRole)
    return getattr(data, "aiBean", None)


def _employee_in_use(uid: Any) -> list[str]:
    names: list[str] = []
    target = str(uid)
    for auto in list(getAutoMap().values()):
        comment_rule = getattr(auto, "commentRule", None)
        employee = getattr(comment_rule, "aiEmployee", None)
        if employee is None and isinstance(comment_rule, dict):
            employee = comment_rule.get("aiEmployee")
        employee_uid = getattr(employee, "uid", None)
        if employee_uid is None and isinstance(employee, dict):
            employee_uid = employee.get("uid")
        if str(employee_uid) == target:
            name = str(getattr(auto, "name", "") or "")
            names.append(name or str(getattr(auto, "source", "") or ""))
    return names


class AiEmployeeTab(MidBaseTab):
    def __init__(self, mainWindow: Any, ui: Any) -> None:
        super().__init__()
        self.mainWindow = mainWindow
        self.cooldown_manager = getattr(mainWindow, "cooldown_manager", None)
        self._finish_bridge = None
        self.validator_thread = None
        self.ui = ui
        self.ui_data_item_list: list[AiEmployeeShowItemData] = []
        self.init()

    def init(self) -> None:
        _connect(
            getattr(self.ui, "btn_goto_api_key", None),
            "clicked",
            self.on_goto_api_key,
        )
        _connect(
            getattr(self.ui, "btn_ai_course", None),
            "clicked",
            self.on_show_ai_course,
        )
        _connect(
            getattr(self.ui, "btn_em_save_lock", None),
            "clicked",
            self.on_save_api_and_lock,
        )
        _connect(
            getattr(self.ui, "btn_em_un_lock", None),
            "clicked",
            self.on_un_lock,
        )
        _connect(
            getattr(self.ui, "btn_add_ai_employee", None),
            "clicked",
            self.on_add_ai_employee,
        )
        _connect(
            getattr(self.ui, "btn_ai_add_refuse", None),
            "clicked",
            self.on_ai_add_refuse,
        )
        _connect(
            getattr(self.ui, "btn_ai_refuse_jiao_chen", None),
            "clicked",
            self.on_ai_refuse_jiao_chen,
        )
        _connect(
            getattr(self.ui, "textEdit_ai_refuse_list", None),
            "textChanged",
            self.ai_refuse_list_text_change,
        )
        employee_changed = getattr(
            signals.global_ui_signal, "signal_employee_data_changed", None
        )
        if employee_changed is not None:
            try:
                employee_changed.connect(self.employeeDataChanged)
            except Exception as exc:
                print("连接AI员工数据信号失败：", exc)
        self.init_list_menu()
        self.init_fill_api_if_need()
        self.init_fill_refuse_token()
        self.initListDataSource()
        self.init_employee_list()

    def init_list_menu(self) -> None:
        widget = getattr(self.ui, "listWidget_em_list", None)
        if widget is None:
            return
        widget.setContextMenuPolicy(Qt.CustomContextMenu)
        _connect(widget, "customContextMenuRequested", self.showEmployeeMenu)

    def on_show_ai_course(self) -> None:
        try:
            ImageDialogHelper.unifyShowInputApiKeyCourse(self)
        except Exception as exc:
            print("打开 AI KEY 教程失败：", exc)

    def on_goto_api_key(self) -> None:
        try:
            QDesktopServices.openUrl(QUrl("https://console.x.ai"))
        except Exception as exc:
            print("你还没有配置专属的AI API KEY", exc)

    def on_add_ai_employee(self) -> None:
        try:
            has_ability = bool(_sq_jqm.has_ai_ability_but_no_key())
        except Exception:
            has_ability = False
        if has_ability:
            _tip("你还没有配置专属的AI API KEY")
            return
        try:
            dialog = EditEmployeeItemEditDialog(
                self.mainWindow,
                "添加AI员工",
                None,
                False,
                False,
            )
            dialog.exec_()
        except Exception as exc:
            print("打开添加AI员工窗口失败：", exc)

    def employeeDataChanged(self) -> None:
        self.initListDataSource()
        self.init_employee_list()

    def on_save_api_and_lock(self) -> None:
        widget = getattr(self.ui, "lineEdit_input_api_key", None)
        if widget is None:
            return
        if not widget.isEnabled():
            _tip("请先解锁！")
            return
        api_key = str(widget.text() or "").strip()
        if not api_key:
            _tip("请输入API KEY")
            return
        if api_key == "***********" or not api_key.startswith("xai-"):
            _tip("输入的API KEY 不合法！")
            return
        utils.validate_xai_api_key(api_key)
        print("正在校验API KEY 是否可用...")
        try:
            if self.validator_thread is not None:
                try:
                    self.validator_thread.finished.disconnect(
                        self.on_validation_finished
                    )
                except Exception as exc:
                    print("断开旧 API 校验线程信号失败：", exc)
            self.validator_thread = XAIKeyValidator(api_key)
            self.validator_thread.finished.connect(self.on_validation_finished)
            self.validator_thread.start()
        except Exception as exc:
            self.on_validation_finished(False, str(exc))

    def on_validation_finished(self, is_valid: bool, message: str = "") -> None:
        api_key = ""
        widget = getattr(self.ui, "lineEdit_input_api_key", None)
        if widget is not None:
            api_key = str(widget.text() or "").strip()
            if api_key and api_key != "***********" and not api_key.startswith("xai-"):
                api_key = ""
        if is_valid and api_key:
            _cache().update_cache(
                tabl_cache.AI_EMPLOYEE_GROUP,
                tabl_cache.AI_EMPLOYEE_API_KEY,
                api_key,
            )
            if widget is not None:
                widget.setText(utils.mask_key(api_key))
            self.lock_ai_ui(True)
            _tip("API_KEY 有效，存储成功！")
        else:
            message_text = "API_KEY 校验失败，请重试，或者检查填写是否正确！"
            if message:
                message_text += " 错误信息：" + str(message)
            _tip(message_text)
        self.validator_thread = None

    def ai_refuse_list_text_change(self) -> None:
        widget = getattr(self.ui, "textEdit_ai_refuse_list", None)
        if widget is None:
            return
        old_text = str(widget.toPlainText() or "")
        token = "|".join(
            item.strip() for item in old_text.replace("\n", "|").split("|") if item.strip()
        )
        _cache().update_cache(
            tabl_cache.AI_EMPLOYEE_GROUP,
            tabl_cache.AI_REFUSE_TOKEN_LIST,
            token,
        )

    def on_ai_refuse_jiao_chen(self) -> None:
        try:
            ImageDialogHelper.unifyShowAIRefuseCourse(self)
        except Exception as exc:
            print("打开 AI 拒绝词教程失败：", exc)

    def on_ai_add_refuse(self) -> None:
        widget = getattr(self.ui, "textEdit_ai_refuse_list", None)
        if widget is None:
            return
        old_text = str(widget.toPlainText() or "").strip()
        token_list = [item.strip() for item in old_text.split("|") if item.strip()]
        defaults = [item.strip() for item in get_default_token().split("|") if item.strip()]
        new_token = "|".join(dict.fromkeys(token_list + defaults))
        widget.setText(new_token.replace("|", "|\n"))
        _cache().update_cache(
            tabl_cache.AI_EMPLOYEE_GROUP,
            tabl_cache.AI_REFUSE_TOKEN_LIST,
            new_token,
        )

    def init_fill_refuse_token(self) -> None:
        widget = getattr(self.ui, "textEdit_ai_refuse_list", None)
        if widget is None:
            return
        try:
            token_list = _cache().read_cache(
                tabl_cache.AI_EMPLOYEE_GROUP,
                tabl_cache.AI_REFUSE_TOKEN_LIST,
                "",
            )
        except Exception:
            token_list = ""
        token_list = str(token_list or "").strip() or get_default_token()
        tokens = [item.strip() for item in token_list.split("|") if item.strip()]
        widget.setText("|\n".join(tokens))

    def init_fill_api_if_need(self) -> None:
        try:
            api_key = _cache().read_cache(
                tabl_cache.AI_EMPLOYEE_GROUP,
                tabl_cache.AI_EMPLOYEE_API_KEY,
                "",
            )
        except Exception:
            api_key = ""
        widget = getattr(self.ui, "lineEdit_input_api_key", None)
        if api_key and widget is not None:
            widget.setText(utils.mask_key(str(api_key)))
            self.lock_ai_ui(True)
        else:
            self.lock_ai_ui(False)

    def lock_ai_ui(self, locked: bool = True) -> None:
        enabled = not bool(locked)
        for name in ("lineEdit_input_api_key", "btn_em_save_lock"):
            widget = getattr(self.ui, name, None)
            if widget is not None:
                widget.setEnabled(enabled)
        unlock = getattr(self.ui, "btn_em_un_lock", None)
        if unlock is not None:
            unlock.setEnabled(True)
        add_button = getattr(self.ui, "btn_add_ai_employee", None)
        if add_button is not None:
            add_button.setEnabled(enabled)

    def on_un_lock(self) -> None:
        widget = getattr(self.ui, "lineEdit_input_api_key", None)
        if widget is not None:
            widget.setEnabled(True)
            widget.clear()
        self.lock_ai_ui(False)

    def initListDataSource(self) -> None:
        self.ui_data_item_list.clear()
        employees = list(getEmployeeMap().items())
        employees.sort(key=lambda item: int(getattr(item[1], "uid", 0) or 0))
        for uid, ai_bean in employees:
            if ai_bean is None:
                continue
            self.ui_data_item_list.append(
                AiEmployeeShowItemData(
                    uid=int(getattr(ai_bean, "uid", uid) or 0),
                    aiBean=ai_bean,
                )
            )

    def init_employee_list(self) -> None:
        widget = getattr(self.ui, "listWidget_em_list", None)
        if widget is None:
            return
        try:
            ListOpHelper.fillEmployeeListView(widget, self.ui_data_item_list)
        except Exception:
            widget.clear()
            for data in self.ui_data_item_list:
                bean = data.aiBean
                if bean is not None:
                    widget.addItem(str(getattr(bean, "name", "") or "AI员工"))

    def showEmployeeMenu(self, pos: Any) -> None:
        widget = getattr(self.ui, "listWidget_em_list", None)
        if widget is None:
            return
        item = widget.itemAt(pos)
        bean = _bean_from_item(item)
        if bean is None:
            return
        menu = QMenu(widget)
        name = str(getattr(bean, "name", "") or "")
        if name == "官方色情大师":
            view = QAction("查看官方色情大师", menu)
            view.triggered.connect(lambda _=False, d=item.data(Qt.UserRole): self.readOnlyItem(d))
            menu.addAction(view)
            copy = QAction("复制官方色情大师", menu)
            copy.triggered.connect(lambda _=False, d=item.data(Qt.UserRole): self.copyItem(d))
            menu.addAction(copy)
        elif name == "官方中文记者":
            view = QAction("查看官方中文记者", menu)
            view.triggered.connect(lambda _=False, d=item.data(Qt.UserRole): self.readOnlyItem(d))
            menu.addAction(view)
            copy = QAction("复制AI员工", menu)
            copy.triggered.connect(lambda _=False, d=item.data(Qt.UserRole): self.copyItem(d))
            menu.addAction(copy)
        else:
            edit = QAction("编辑AI员工", menu)
            edit.triggered.connect(lambda _=False, d=item.data(Qt.UserRole): self.editItem(d))
            menu.addAction(edit)
            copy = QAction("复制AI员工", menu)
            copy.triggered.connect(lambda _=False, d=item.data(Qt.UserRole): self.copyItem(d))
            menu.addAction(copy)
            dele = QAction("删除AI员工", menu)
            dele.triggered.connect(lambda _=False, d=item.data(Qt.UserRole): self.deleteItem(d))
            menu.addAction(dele)
        menu.exec_(widget.mapToGlobal(pos))

    def editItem(self, data: Any) -> None:
        bean = getattr(data, "aiBean", data)
        try:
            dialog = EditEmployeeItemEditDialog(
                self.mainWindow,
                "编辑AI员工",
                bean,
                False,
                False,
            )
            dialog.exec_()
        except Exception as exc:
            print("打开编辑AI员工窗口失败：", exc)

    def copyItem(self, data: Any) -> None:
        bean = getattr(data, "aiBean", data)
        if bean is None:
            return
        try:
            copied = AiEmployeeBean(**dict(getattr(bean, "__dict__", {})))
        except Exception:
            copied = AiEmployeeBean()
            for name in (
                "name",
                "role",
                "pre_text",
                "sensitive",
                "word_min",
                "word_max",
                "model",
                "retry_count",
            ):
                setattr(copied, name, getattr(bean, name, ""))
        generated_uid = str(utils.gen_id_by_ns()) if hasattr(utils, "gen_id_by_ns") else "0"
        try:
            copied.uid = int(generated_uid[-12:])
        except (TypeError, ValueError):
            copied.uid = 0
        copied.name = (str(getattr(copied, "name", "") or "") + " 副本").strip()
        try:
            dialog = EditEmployeeItemEditDialog(
                self.mainWindow,
                "复制AI员工",
                copied,
                True,
                False,
            )
            dialog.exec_()
        except Exception as exc:
            print("打开复制AI员工窗口失败：", exc)

    def readOnlyItem(self, data: Any) -> None:
        bean = getattr(data, "aiBean", data)
        try:
            dialog = EditEmployeeItemEditDialog(
                self.mainWindow,
                "查看官方AI员工",
                bean,
                False,
                True,
            )
            dialog.exec_()
        except Exception as exc:
            print("打开查看AI员工窗口失败：", exc)

    def deleteItem(self, data: Any) -> None:
        bean = getattr(data, "aiBean", data)
        if bean is None:
            return
        uid = getattr(bean, "uid", 0)
        usage = _employee_in_use(uid)
        if usage:
            tip_str = (
                "当前AI员工正在被：【"
                + "，".join(usage)
                + "】 使用，不可以删除它"
            )
            _tip(tip_str)
            return
        deleteAiEmployeeBean(uid)
        try:
            signals.global_ui_signal.signal_employee_data_changed.emit()
        except Exception:
            self.employeeDataChanged()


__all__ = ["AiEmployeeTab"]
