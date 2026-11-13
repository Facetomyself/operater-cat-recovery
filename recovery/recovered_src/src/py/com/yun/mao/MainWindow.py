# Recovered module: src.py.com.yun.mao.MainWindow
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
"""Main window reconstruction.

inferred: UI fallback construction, tab controller wiring, tray text layout,
and a few Qt event orderings that are not recoverable from constants alone.
"""
from __future__ import annotations

import asyncio
import os
from types import SimpleNamespace

from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication, QProcess, QThread, QTimer, Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtWidgets import (
    QAction,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSystemTrayIcon,
    QTabWidget,
    QWidget,
)

from . import ErrorDialog
from .ad import AdIdMapManager
from .auto import CMCode, GlobalWorkingLock, ProcessCache
from .cd import Working
from .cd.ConditionalTabWidget import ConditionalTabWidget
from .config import YunYinMaoConfig, tabl_cache
from .config.tabl_cache import (
    LAST_TAB_INDEX,
    PROXY_SETTING_GROUP,
    PROXY_SETTING_enable,
    TEXT_BIAO_SHI,
    TEXT_BIAO_SHI_text,
    TOP_CACHE_GROUP,
)
from .dclass import ItemMemStore
from .dclass.LoadEmployeeClass import loadEmployee
from .dialog import ImageDialogHelper
from .dialog.ExpriActivatePermissionDialog import ExpriActivatePermissionDialog
from .fea import _sq_hj, _sq_jqm
from .link._fds_jm import sec
from .link._xb_ms import kai_shit_f_m_5s
from .log import LocalLogSetting
from .log.glog import GlobalLog
from .login import ClientCacheHelper
from .monitor.MonitorHistoryManagerFile import MonitorHistoryManager
from .proxy.ProxySettingDialog import ProxySettingDialog
from .remember import RandomBucketManager
from .remember import RememberManager
from .tab.mid_ai_employee_tab import AiEmployeeTab
from .tab.mid_ai_test_tab import AiTestTab
from .tab.mid_api_config_tab import ApiConfigTab
from .tab.mid_auto_yun_yin_tab import AutoYunYinTab
from .tab.mid_premium_tab import PremiumTab
from .tab.mid_session_fun_tab import SessionFunTab
from .tab.mid_toolbox_tab import ToolBoxTab
from .tgaccount import TGAuthAccountSetting
from .util import IncludeMagickConfig, ResourcePath, SuspendFrozenTag, TracePrinterHelper
from .util.CacheRemoveTask import CacheRemoveTask
from .util.need import CommonCode, ShotUtils, signals, utils
from .util.need.LoadingDialog import LoadingDialog
from .util.need.MiniTipDialog import MiniTipDialog
from .util.need.ResetBirdDialog import ResetBirdDialog
from .util.need.TipDialog import TipDialog

try:
    from src.resource.ui.dyna.yun_yin_mao_main import Ui_MainWindow
except Exception:
    Ui_MainWindow = None


def bring_window_to_front(window) -> None:
    """Bring a Qt top-level window to the foreground.

    Evidence: ``_re/runtime_state.txt`` exposes this module-level
    ``compiled_function`` and the module constants carry
    ``isVisible``/``isMinimized``/``showNormal``/``raise_``/
    ``activateWindow``/``windowTitle`` plus the native foreground fallback.
    """

    if not window.isVisible():
        window.show()
    if window.isMinimized():
        window.showNormal()
    window.raise_()
    window.activateWindow()
    try:
        import win32con
        import win32gui

        handle = win32gui.FindWindow(None, window.windowTitle())
        if handle:
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(handle)
    except Exception:
        return None


class YunYinMaoMainWindow(QMainWindow):
    globalInstance = None

    def __init__(self) -> None:
        super().__init__()
        self.ui = SimpleNamespace()
        self.tab_controllers = {}
        self.last_message_ended_with_newline = True
        self.session_fun_tab = None
        self.auto_yun_yin_tab = None
        self.app_toolbox_tab = None
        self.app_premium_tab = None
        self.app_ai_test_tab = None
        self.app_ai_employee_tab = None
        self.app_config_tab = None
        self.tabWidget_important = None
        self.show_main_window = None
        self.quit_action = None
        self.glog = GlobalLog()
        self.condition_tab_widget = None
        self.menu = None
        self.tray_icon = None
        self.server = None
        self.re_try_fetch_zw_t = QTimer(self)
        self.allow_close = True
        self._final_quitting = False
        YunYinMaoMainWindow.globalInstance = self
        try:
            from . import GlobalExceptionHandler

            GlobalExceptionHandler.global_window = self
        except Exception:
            self.glog.write("全局异常窗口绑定失败\n")
        self.soft_name = CommonCode.read_soft_name()
        self.setWindowTitle(self.soft_name)
        self.server_name = f"{self.soft_name}_{CMCode.r_instance_id()}"
        self.setup_single_instance()
        self.init_biz_data()
        self.init_parent_widget()
        self.init_child_widget()
        self.init_tray()
        self.update_ico_fun()
        self.init_view()
        self.display_ai_tab()
        self.display_premium_tab()
        self.display_experience_dialog_by_delay()
        self.display_input_apikey_dialog_by_delay()
        self.delete_temp_mp3()

    def setup_single_instance(self) -> bool:
        socket = QLocalSocket()
        socket.connectToServer(self.server_name)
        if socket.waitForConnected(500):
            if not YunYinMaoConfig.is_support_multi():
                error_msg = "您目前是个人版没有多开权限，请联系客服升级企业版解锁多开权限！"
            else:
                error_msg = "错误多开方式错误，请你严格按照教程方式进行多开！"
            try:
                error_msg = sec("hj_fail_tpl_05").format(error_msg=error_msg)
            except Exception:
                _ = error_msg
            ErrorDialog.show_error_tip(error_msg)
            socket.write(b"show")
            socket.waitForBytesWritten(1000)
            socket.disconnectFromServer()
            socket.waitForDisconnected(1000)
            socket.close()
            self.cleanup()
            QCoreApplication.quit()
            return False
        self.server = QLocalServer(self)
        self.server.newConnection.connect(self.handle_new_connection)
        self.server.removeServer(self.server_name)
        if not self.server.listen(self.server_name):
            print("服务器启动失败: ", self.server.errorString())
            return False
        print("单实例服务器启动成功")
        return True

    def init_biz_data(self) -> None:
        ItemMemStore.ensure_main_window_item_memory()
        loadEmployee()
        AdIdMapManager.loadAdIdMap()
        MonitorHistoryManager.load_history_map()
        RememberManager.loadRememberMap()
        load_random_bucket_map = getattr(
            RandomBucketManager, "load_random_bucket_map", None
        )
        if callable(load_random_bucket_map):
            load_random_bucket_map()
        LocalLogSetting.deleteFiveDateLogFile()
        load_dis_auth = getattr(
            TGAuthAccountSetting, "loadFromDisAuthAccountList", None
        )
        if callable(load_dis_auth):
            load_dis_auth()
        IncludeMagickConfig.setup_magick_config()
        cache_task = CacheRemoveTask()
        run_cache_task = getattr(cache_task, "run", None)
        if callable(run_cache_task):
            run_cache_task()

    def init_parent_widget(self) -> None:
        if Ui_MainWindow is not None:
            try:
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)
                self.tabWidget_important = getattr(
                    self.ui, "tabWidget_important", None
                )
            except Exception:
                print("创建服务器或初始化时出错: ")
                TracePrinterHelper.print_trace()
                self.ui = SimpleNamespace()
        if self.tabWidget_important is None:
            self.tabWidget_important = QTabWidget(self)
            self.setCentralWidget(self.tabWidget_important)
            self.ui.tabWidget_important = self.tabWidget_important
        try:
            self.condition_tab_widget = ConditionalTabWidget(
                self.tabWidget_important
            )
        except Exception:
            self.condition_tab_widget = None
        self.tabWidget_important.setObjectName("tabWidget_important")
        self.tabWidget_important.currentChanged.connect(self.on_tab_changed)
        text_browser = getattr(self.ui, "text_brow_log", None)
        if text_browser is not None:
            self.glog.attach_ui(text_browser)
        try:
            self.glog.frozeDetected.connect(self._froze_connected)
        except Exception:
            pass
        try:
            self.frozen_timeout_seconds = int(
                getattr(self, "frozen_timeout_seconds", 60)
            )
            if SuspendFrozenTag.check_frozen_timeout(
                self.frozen_timeout_seconds
            ):
                self._froze_connected()
        except Exception:
            self.glog.write("冻结检测初始化失败\n")

    def init_child_widget(self) -> None:
        bindings = (
            ("btn_expand_log", "clicked", self.expand_log),
            ("btn_open_log_folder", "clicked", self.open_log_folder),
            ("btn_open_down_load_folder", "clicked", self.open_down_load_folder),
            ("main_expri_permission", "clicked", self.on_show_expri_permission),
            ("btn_copy_log", "clicked", self.copy_log),
            ("btn_kefu_link", "clicked", self.kefu_link),
            ("btn_clear_log", "clicked", self.clear_log),
            ("action_reset", "triggered", self.click_action_reset),
            ("action_copy_code", "triggered", self.copy_code),
            ("btn_proxy_setting", "clicked", self.showProxySettingDialog),
            ("cb_enable_proxy", "stateChanged", self.onProxyStatsChanged),
            ("lineEdit_text_biao_shi", "textChanged", self.biao_shi_text_change),
        )
        for widget_name, signal_name, handler in bindings:
            widget = getattr(self.ui, widget_name, None)
            if widget is None:
                continue
            signal = getattr(widget, signal_name, None)
            if signal is not None:
                signal.connect(handler)
        signals.global_ui_signal.tip_dialog_cmd.connect(self.showTipDialog)
        signals.global_ui_signal.tip_dialog_size_cmd.connect(
            self.showTipDialogBySize
        )
        signals.global_ui_signal.tip_dialog_restart_cmd.connect(
            self.showTipDialogByRestart
        )
        signals.global_ui_signal.update_icon_states.connect(self.update_icon_states)
        signals.global_ui_signal.cmd_update_process.connect(self.update_tray_text)
        signals.global_ui_signal.cmd_activate_code_stats.connect(
            self.on_activate_code_stats
        )
        cache = tabl_cache.INSTANCE()
        biao_shi = cache.read_cache(TEXT_BIAO_SHI, TEXT_BIAO_SHI_text, "")
        line_edit = getattr(self.ui, "lineEdit_text_biao_shi", None)
        if line_edit is not None and biao_shi:
            line_edit.blockSignals(True)
            line_edit.setText(str(biao_shi))
            line_edit.blockSignals(False)
        proxy_enabled = utils.strTobool(
            cache.read_cache(PROXY_SETTING_GROUP, PROXY_SETTING_enable, "False")
        )
        check_box = getattr(self.ui, "cb_enable_proxy", None)
        if check_box is not None:
            check_box.blockSignals(True)
            check_box.setChecked(proxy_enabled)
            check_box.blockSignals(False)

    def init_tray(self) -> None:
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            QIcon(ResourcePath.get_ico_path("normal_256.ico"))
        )
        self.menu = QMenu(self)
        self.show_main_window = QAction("显示主界面", self)
        self.quit_action = QAction("退出", self)
        self.menu.addAction(self.show_main_window)
        self.menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.show_main_window.triggered.connect(self.on_restore_action)
        self.quit_action.triggered.connect(self.on_quit_action)
        self.tray_icon.show()

    def update_ico_fun(self) -> None:
        status = getattr(GlobalWorkingLock, "SCHEDULER_STATUS", None)
        icon_name = "normal_256.ico"
        if status == getattr(GlobalWorkingLock, "STATUES_TIMING", object()):
            icon_name = "timing_256.ico"
        elif status == getattr(GlobalWorkingLock, "STATUES_AIDL", object()):
            icon_name = "disable_256.ico"
        if ResourcePath.ico_is_exists(icon_name) and self.tray_icon is not None:
            self.tray_icon.setIcon(QIcon(ResourcePath.get_ico_path(icon_name)))
        self.update_tray_text()

    def display_account(self) -> None:
        label = getattr(self.ui, "lb_display_txt", None)
        if label is not None:
            label.setText(_sq_jqm.current_account_info.geneDisplay())
        self.display_grade()
        self.display_self_experience_button_if_need()

    def display_ai_tab(self) -> None:
        if not _sq_jqm.current_account_info.has_ai_ability():
            return
        try:
            self.app_ai_employee_tab = self._add_controller_tab(
                "ai_employee_tab.ui",
                "AI员工管理",
                AiEmployeeTab,
            )
        except Exception:
            self.glog.write("AI员工管理 页面加载失败\n")
        try:
            self.app_ai_test_tab = self._add_controller_tab(
                "ai_pre_test_tab.ui",
                "AI测试平台",
                AiTestTab,
            )
        except Exception:
            self.glog.write("AI测试平台 页面加载失败\n")

    def _add_controller_tab(self, ui_name: str, title: str, controller_type):
        page = QWidget(self.tabWidget_important)
        page.setObjectName(os.path.splitext(ui_name)[0])
        uic.loadUi(ResourcePath.get_ui_path(ui_name), page)
        controller = controller_type(self, page)
        self.tabWidget_important.addTab(page, title)
        self.tab_controllers[title] = controller
        return controller

    def display_premium_tab(self) -> None:
        if _sq_jqm.current_account_info.open_premium():
            try:
                self.app_premium_tab = self._add_controller_tab(
                    "premium_tab.ui",
                    "开通会员",
                    PremiumTab,
                )
            except Exception:
                self.glog.write("开通会员 页面加载失败\n")
        label = getattr(self.ui, "label_version_grade", None)
        if label is not None:
            label.setText(_sq_jqm.current_account_info.gen_ka_info())

    def display_experience_dialog_by_delay(self) -> None:
        if _sq_jqm.current_account_info.has_exp_permission():
            QTimer.singleShot(500, self.on_show_expri_permission)

    def display_input_apikey_dialog_by_delay(self) -> None:
        if _sq_jqm.current_account_info.has_ai_ability_but_no_key():
            QTimer.singleShot(500, self.on_show_input_apikey_dialog)

    def delete_temp_mp3(self) -> None:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        for root, _dirs, files in os.walk(root_dir):
            for name in files:
                if name.endswith(".mp3"):
                    utils.safe_del_file(os.path.join(root, name))

    def on_program_frozen(self) -> None:
        action = getattr(self.ui, "action_reset", None)
        if action is not None:
            action.setText("重置")
        tab_widget = self.findChild(QTabWidget)
        if tab_widget is None:
            return
        self.condition_tab_widget = ConditionalTabWidget(tab_widget)
        self.condition_tab_widget.setObjectName("tabWidget_important")
        current = tab_widget.currentWidget()
        if current is not None and hasattr(current, "on_tab_show"):
            current.on_tab_show()
        self.on_program_suspected_frozen()

    def on_tab_changed(self, index: int) -> None:
        if Working.Session_Working:
            signals.global_ui_signal.tip_dialog_cmd.emit(
                "任务正在进行中，不能切换！"
            )
            return
        condition = self.condition_tab_widget
        can_changed = getattr(condition, "can_changed_tab", None)
        if callable(can_changed) and not can_changed():
            signals.global_ui_signal.tip_dialog_cmd.emit(
                "任务正在进行中，不能切换！"
            )
            return
        widget = self.tabWidget_important.widget(index)
        tab_text = self.tabWidget_important.tabText(index)
        controller = self.tab_controllers.get(tab_text)
        if controller is None:
            controller = widget
        on_tab_show = getattr(controller, "on_tab_show", None)
        if callable(on_tab_show):
            on_tab_show()

    def can_changed_tab(self) -> bool:
        checker = getattr(self.condition_tab_widget, "can_changed_tab", None)
        return bool(checker()) if callable(checker) else True

    def setLastTab(self, index=None) -> None:
        if index is None:
            try:
                index = int(
                    tabl_cache.INSTANCE().read_cache(
                        TOP_CACHE_GROUP,
                        LAST_TAB_INDEX,
                        "0",
                    )
                )
            except Exception:
                index = 0
        if self.tabWidget_important is None:
            return
        if 0 <= int(index) < self.tabWidget_important.count():
            self.tabWidget_important.setCurrentIndex(int(index))

    def init_view(self) -> None:
        self.session_fun_tab = SessionFunTab(self, self.ui.gen_session)
        self.auto_yun_yin_tab = AutoYunYinTab(self, self.ui.tab)
        self.app_toolbox_tab = ToolBoxTab(self, self.ui.tools)
        self.app_config_tab = ApiConfigTab(self, self.ui.api_fun)
        self.tab_controllers["账号功能"] = self.session_fun_tab
        self.tab_controllers["自动运营"] = self.auto_yun_yin_tab
        self.tab_controllers["工具箱"] = self.app_toolbox_tab
        self.tab_controllers["API功能"] = self.app_config_tab
        self.display_account()
        self.displayProxy()
        self.show_env()
        self.setLastTab()

    def handle_new_connection(self) -> None:
        if self.server is None:
            return
        client = self.server.nextPendingConnection()
        if client is None:
            return
        client.readyRead.connect(lambda: self.process_client(client))

    def process_client(self, client: QLocalSocket) -> None:
        data = bytes(client.readAll()).decode("utf-8", errors="ignore")
        if "show" in data:
            self.activate_window()

    def activate_window(self) -> None:
        self.show()
        self._bring_main_window_to_front()
        self.glog.resume_ui_log()

    def _bring_main_window_to_front(self) -> None:
        try:
            app_thread = QCoreApplication.instance().thread()
            if QThread.currentThread() is not app_thread:
                return
        except Exception:
            pass
        try:
            bring_window_to_front(self)
        except Exception:
            self.glog.write("窗口置前失败\n")

    def cleanup(self) -> None:
        if self.server is not None:
            self.server.close()
            self.server = None

    def expand_log(self) -> None:
        text_browser = getattr(self.ui, "text_brow_log", None)
        button = getattr(self.ui, "btn_expand_log", None)
        if text_browser is None:
            return
        visible = text_browser.isVisible()
        text_browser.setVisible(not visible)
        if button is not None:
            button.setText("关闭全屏日志" if not visible else "打开全屏日志")

    def open_log_folder(self) -> None:
        utils.init_folder(YunYinMaoConfig.multi_abs_log_dir)
        QDesktopServices.openUrl(
            QUrl.fromLocalFile(str(YunYinMaoConfig.multi_abs_log_dir))
        )

    def open_down_load_folder(self) -> None:
        folder = YunYinMaoConfig.yun_yin_ban_yun_folder_only_down_load()
        QProcess.startDetached("explorer.exe", [str(folder)])

    def on_show_expri_permission(self) -> None:
        try:
            ShotUtils.shot(self)
        except Exception:
            self.glog.write("界面截图失败\n")
        dialog = ExpriActivatePermissionDialog(
            self,
            "自助激活会员体验",
            _sq_jqm.current_account_info.get_experi_duration_hours(),
        )
        dialog.exec_()

    def copy_log(self) -> None:
        text_browser = getattr(self.ui, "text_brow_log", None)
        if text_browser is None:
            return
        text_to_copy = text_browser.toPlainText()
        if utils.copy_text_to_clipboard(text_to_copy):
            print("日志复制成功！")
        else:
            print("复制失败，可能是", "机器码账号异常了！")

    def kefu_link(self) -> None:
        link = ""
        try:
            link = str(CommonCode.read_contact_link())
        except Exception:
            link = "https://t.me/" + str(
                _sq_jqm.current_account_info.maoContacts or ""
            ).lstrip("@")
        QDesktopServices.openUrl(QUrl(link))

    def clear_log(self) -> None:
        text_browser = getattr(self.ui, "text_brow_log", None)
        if text_browser is not None:
            text_browser.clear()

    def click_action_reset(self) -> None:
        dialog = ResetBirdDialog(self)
        dialog.exec()

    def fetch_zw(self):
        try:
            self.locked_ui(False)
            result = _sq_jqm.current_account_info.zh_ye_xx()
            self.display_account()
            return result
        except Exception:
            self.locked_ui(True)
            self.re_try_fetch_zw_t.start(500)
            try:
                signals.global_ui_signal.zw_except_re_try.emit()
            except Exception:
                pass
            return None

    def locked_ui(self, locked: bool = True) -> None:
        self.ui_locked = bool(locked)
        enabled = not self.ui_locked
        if self.tabWidget_important is not None:
            self.tabWidget_important.setEnabled(enabled)
        if self.menu is not None:
            self.menu.setEnabled(enabled)

    def copy_code(self) -> None:
        ucode = str(_sq_jqm.current_account_info.ucode or "")
        if utils.copy_text_to_clipboard(ucode):
            print("机器码已经复制成功，现在你可以去其他地方粘贴了")
        else:
            print("复制失败，可能是", "机器码账号异常了！")

    def showProxySettingDialog(self) -> None:
        dialog = ProxySettingDialog(self)
        dialog.exec_()
        check_box = getattr(self.ui, "cb_enable_proxy", None)
        if check_box is not None:
            check_box.setChecked(
                utils.strTobool(
                    tabl_cache.INSTANCE().read_cache(
                        PROXY_SETTING_GROUP, PROXY_SETTING_enable, "False"
                    )
                )
            )

    def onProxyStatsChanged(self, state: int) -> None:
        enabled = state == Qt.Checked
        print("debug debug 手动改变->代理是否开启：", enabled)
        check_box = getattr(self.ui, "cb_enable_proxy", None)
        if check_box is not None:
            check_box.blockSignals(True)
            check_box.setChecked(enabled)
            check_box.blockSignals(False)
        tabl_cache.INSTANCE().write_cache(
            PROXY_SETTING_GROUP,
            PROXY_SETTING_enable,
            "True" if enabled else "False",
        )

    def showTipDialog(self, message: str) -> None:
        try:
            dialog = TipDialog(self, str(message))
            dialog.exec_()
        except Exception:
            QMessageBox.information(self, "提示", str(message))

    def showTipDialogBySize(self, size: int) -> None:
        try:
            dialog = TipDialog(self, "", int(size))
            dialog.exec_()
        except Exception:
            QMessageBox.information(self, "提示", "出现意外，请重试！")

    def showTipDialogByRestart(self, size: int) -> None:
        try:
            dialog = TipDialog(self, "程序退出", int(size), restart=True)
            dialog.exec_()
        except Exception:
            QMessageBox.information(self, "提示", "程序退出")

    def update_icon_states(self) -> None:
        self.update_ico_fun()

    def update_tray_text(self, *_args) -> None:
        if self.tray_icon is None:
            return
        tooltip = " -".join(
            part
            for part in (
                str(getattr(ProcessCache, "CACHE_PROCESS_STR", "")),
                str(getattr(ProcessCache, "CACHE_PRESENT", "")),
                str(getattr(ProcessCache, "SCHEDULER_STR", "")),
            )
            if part
        )
        self.tray_icon.setToolTip(tooltip)

    def on_activate_code_stats(self, success: bool) -> None:
        if success:
            self.display_account()
            self.update_icon_states()
            return
        signals.global_ui_signal.tip_dialog_cmd.emit("出现意外，请重试！")

    def biao_shi_text_change(self, text: str) -> None:
        tabl_cache.INSTANCE().write_cache(
            TEXT_BIAO_SHI, TEXT_BIAO_SHI_text, str(text)
        )

    def display_grade(self) -> None:
        label = getattr(self.ui, "label_version_grade", None)
        if label is not None:
            label.setText(_sq_jqm.current_account_info.gen_ka_info())
        env_label = getattr(self.ui, "label_env_show", None)
        if env_label is not None:
            is_dev = False
            try:
                is_dev = bool(_sq_hj.hj_dev_ok())
            except Exception:
                is_dev = False
            env_label.setText("开发环境" if is_dev else "")

    def displayProxy(self) -> None:
        check_box = getattr(self.ui, "cb_enable_proxy", None)
        if check_box is None:
            return
        enabled = utils.strTobool(
            tabl_cache.INSTANCE().read_cache(
                PROXY_SETTING_GROUP,
                PROXY_SETTING_enable,
                "False",
            )
        )
        check_box.blockSignals(True)
        check_box.setChecked(enabled)
        check_box.blockSignals(False)

    def show_env(self) -> None:
        label = getattr(self.ui, "label_env_show", None)
        if label is None:
            return
        try:
            is_dev = bool(_sq_hj.hj_dev_ok())
        except Exception:
            is_dev = False
        label.setText("开发环境" if is_dev else "")

    def display_self_experience_button_if_need(self) -> None:
        button = getattr(self.ui, "main_expri_permission", None)
        if button is None:
            return
        button.setVisible(
            bool(_sq_jqm.current_account_info.has_exp_permission())
        )

    def on_show_input_apikey_dialog(self) -> None:
        ImageDialogHelper.unifyShowInputApiKeyCourse(self)

    def on_tray_icon_activated(self, reason) -> None:
        if reason == QSystemTrayIcon.DoubleClick:
            self.activate_window()

    def on_restore_action(self) -> None:
        self.activate_window()

    def on_quit_action(self) -> None:
        self.final_quit()

    def final_quit(self) -> None:
        if self._final_quitting:
            return
        self._final_quitting = True
        self.glog.pause_ui_log()
        self.allow_close = True
        if self.tray_icon is not None:
            self.tray_icon.hide()
        try:
            if self.auto_yun_yin_tab is not None:
                self.auto_yun_yin_tab.final_stop_quit()
        except Exception:
            self.glog.write("异常引发强制停止任务\n")
        try:
            if self.session_fun_tab is not None:
                self.session_fun_tab.gen_session_queue.send_stop_send()
        except Exception:
            self.glog.write("停止登录队列失败\n")

        async def await_exit() -> None:
            try:
                ClientCacheHelper.safe_disconnect_client()
            finally:
                await asyncio.sleep(0)

        try:
            asyncio.run(await_exit())
        except RuntimeError:
            ClientCacheHelper.safe_disconnect_client()
        self.cleanup()
        self.close_event()
        app = QCoreApplication.instance()
        if app is not None:
            app.quit()

    def show_message_box(self, message: str = "出现意外，请重试！") -> None:
        def min_fun() -> None:
            self.showMinimized()

        def tray_fun() -> None:
            self.glog.pause_ui_log()
            self.hide()

        def exit_fun() -> None:
            self.final_quit()

        try:
            dialog = MiniTipDialog(self, min_fun, tray_fun, exit_fun)
            label = getattr(getattr(dialog, "ui", None), "label", None)
            if label is not None and message:
                label.setText(str(message))
            dialog.show()
        except Exception:
            QMessageBox.warning(self, "提示", str(message))

    def show_dirty_item_saving_dialog(self) -> None:
        if not ItemMemStore.is_item_dirty():
            self.allow_close = True
            self.close()
            return
        loading = LoadingDialog(self, "进行合法性校验，请稍候...")
        loading.show()

        def after(ok: bool) -> None:
            try:
                loading.allow_close()
                loading.close()
            except Exception:
                pass
            if ok:
                self.allow_close = True
                self.close()
            else:
                self.show_message_box("出现意外，请重试！")

        from .fea import _sq_r_ks

        save_fun = getattr(_sq_r_ks, "save_item_r_ui", None)
        if callable(save_fun):
            try:
                save_fun(after)
            except Exception:
                after(False)
        else:
            after(False)

    def _froze_connected(self, *_args) -> None:
        self.on_program_frozen()

    def on_program_suspected_frozen(self) -> None:
        self.re_try_fetch_zw_t.start(500)
        try:
            kai_shit_f_m_5s()
        except Exception as e:
            print(e)
        repaint = getattr(self, "repaint", None)
        if callable(repaint):
            repaint()

    def close_event(self) -> bool:
        if not self.allow_close:
            self.show_dirty_item_saving_dialog()
            return False
        self.cleanup()
        return True

    def closeEvent(self, event) -> None:
        if self.close_event():
            event.accept()
        else:
            event.ignore()

