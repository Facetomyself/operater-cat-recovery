# Recovered module: src.py.com.yun.mao.tab.mid_auto_yun_yin_tab
# Main automation/monitor controller.  The class surface, signal names,
# worker names, UI field names and freeze-recovery branches are evidence
# backed by the Nuitka constant chunk.  Local validation and UI adapter
# choices are inferred and marked at the relevant blocks.
from __future__ import annotations

import copy
import json
import os
import time
from typing import Any, Callable, Optional

from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QMenu,
    QSizePolicy,
)

from ..ad.AddOrEditAdDialog import AddOrEditAdDialog
from ..ad.UIAdListOp import UIAdListOp
from ..auto import CMCode, ProcessCache
from ..cd import TaskHardStop, Working
from ..config import NewConfig, YunYinMaoConfig, tabl_cache
from ..dclass.DTopClass import (
    AUTO_BEAN_TYPE_AUTO_FLOW,
    AUTO_BEAN_TYPE_BAN_YUN,
    AUTO_BEAN_TYPE_DOWN_LOAD_FLOW,
    AUTO_BEAN_TYPE_YU_LAN_FLOW,
    AUTO_BEAN_TYPE_YUN_AUTO,
    AUTO_BEAN_TYPE_YUN_PRE_VIEW,
    AutoBean,
    Water,
)
from ..dclass import DTopClassHelper
from ..dclass.LoadDataClass import (
    addOrUpdate,
    deleteAutoBean,
    deleteGAd,
    getAutoBeanById,
    getAutoMap,
    getGlobalAd,
    getScheduler,
    updateGlobalAd,
    updateSchedulerAndGlobalAd,
)
from ..dclass.LoadEmployeeClass import getAiEmployee
from ..dialog import ImageDialogHelper
from ..fea import _sq_jqm
from ..monitor.HistoryMessageOpDialog import HistoryMessageOpDialog
from ..monitor.MonitorHistoryManagerFile import MonitorHistoryManager
from ..monitor.MonitorSchedulerReport import MonitorSchedulerReportThread
from ..monitor.MonitorStyleDef import monitor_table_style_def
from ..monitor.TelegramMonitorWorker import TelegramMonitorWorker
from ..mthread.SchedulerThreadClass import SchedulerThread
from ..mthread.SingleLongTaskThreadClass import SingleLongTaskThread
from ..remember import RandomBucketManager
from ..remember import RememberManager
from ..telefast import RateLimiterHelper
from ..tgaccount.TGAuthAccount import TGAuthAccount
from ..tgaccount.TgAccountListDialog import TgAccountListDialog
from ..util import SuspendFrozenTag
from ..util.need import CommonCode, ListOpHelper, signals, utils
from ..util.need.AllBeanDef import (
    DTopClassWrapper,
    MonitorSignalBean,
    MonitorSignalBeanWrapper,
)
try:
    from ..util.need.CoolUtils import ButtonCooldownManager
except ImportError:
    ButtonCooldownManager = None
from ..util.need.EditAutoFlowItemEditDialog import EditAutoFlowItemEditDialog
from ..util.need.EditBanYunCommentItemEditDialog import (
    EditBanYunCommentItemEditDialog,
)
from ..util.need.EditDownLoadItemEditDialog import EditDownLoadItemEditDialog
from ..util.need.EditYulanFlowItemEditDialog import EditYulanFlowItemEditDialog
from ..util.need.EditYunAutoItemEditDialog import EditYunAutoItemEditDialog
from ..util.need.EditYunPreViewItemEditDialog import EditYunPreViewItemEditDialog
from ..wp_jt.gj_x5_ft_v6 import ac_r3_sk
from ..fea import _cw_jm_file, _hb_yt_file, _lk_ps_file, _qf_rn_file, _yg_bn_file
from ..fea import _dr_vx_file
from ..link import _fdg_cm_rx, _fdg_ct_ew, _fdg_ct_is, _fdg_os_kx, _fdg_pw_rm
from .mid_base_tab import MidBaseTab


_ACTIVE_THREAD_NAMES = (
    ("scheduler_thread", "定时调度线程"),
    ("single_task_thread", "单次任务线程"),
    ("monitor_worker_thread", "监控线程"),
    ("monitor_scheduler_report_thread", "监控看门狗线程"),
)


def _tip(text: str) -> None:
    try:
        signals.global_ui_signal.tip_dialog_cmd.emit(str(text or ""))
    except Exception:
        print(text)


def _main_ui(tab: Any) -> Any:
    return getattr(getattr(tab, "mainWindow", None), "ui", None)


def _connect(widget: Any, signal_name: str, slot: Any) -> None:
    try:
        signal = getattr(widget, signal_name, None)
        if signal is not None:
            signal.connect(slot)
    except Exception:
        return None


def _connect_signal(signal: Any, slot: Any) -> None:
    if signal is None:
        return
    try:
        signal.connect(slot)
    except Exception:
        return None


def _set_text(widget: Any, text: Any) -> None:
    try:
        widget.setText(str(text or ""))
    except Exception:
        return None


def _set_visible(widget: Any, visible: bool) -> None:
    try:
        widget.setVisible(bool(visible))
    except Exception:
        return None


def _set_enabled(widget: Any, enabled: bool) -> None:
    try:
        widget.setEnabled(bool(enabled))
    except Exception:
        return None


def _checked(widget: Any) -> bool:
    try:
        return bool(widget.isChecked())
    except Exception:
        return False


def _text(widget: Any, default: str = "") -> str:
    try:
        return str(widget.text() or "")
    except Exception:
        return default


def _call(target: Any, name: str, *args: Any, **kwargs: Any) -> Any:
    try:
        func = getattr(target, name, None)
        if callable(func):
            return func(*args, **kwargs)
    except Exception:
        return None
    return None


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return default


def _json_default(value: Any) -> Any:
    if hasattr(value, "__dict__"):
        return dict(value.__dict__)
    return str(value)


def _open_flow_dialog(
    tab: "AutoYunYinTab",
    dialog_cls: Any,
    title: str,
    auto_type: int,
) -> None:
    if bool(getattr(Working, "Session_Working", False)):
        _tip("任务正在进行中，不能添加！")
        return
    try:
        bean = AutoBean(auto_type=auto_type)
        dialog = dialog_cls(tab.mainWindow, title, bean, False, None)
        dialog.exec_()
        tab.initListDataSource()
    except Exception as exc:
        print("打开添加条目窗口失败：", exc)


class AutoYunYinTab(MidBaseTab):
    CLICK_RESET_INTERVAL_MS = 5000
    WORKER_STOP_WAIT_MS = 250
    FROZE_RESTART_MAX_RETRIES = 8
    FROZE_RESTART_RETRY_MS = 2000
    FROZE_IDLE_POLL_MS = 1000
    FROZE_STOP_WAIT_TIMEOUT_MS = 15000
    FROZE_RESTART_MIN_DELAY_MS = 1000
    FROZE_SAFETY_RELEASE_MS = 60000
    FROZE_HARD_RELEASE_MS = 120000

    def __init__(self, mainWindow: Any, ui: Any) -> None:
        super().__init__()
        self.cooldown_manager = getattr(mainWindow, "cooldown_manager", None)
        if self.cooldown_manager is None and ButtonCooldownManager is not None:
            self.cooldown_manager = ButtonCooldownManager()
        self.is_click = False
        self.mainWindow = mainWindow
        self.ui = ui
        self.ui_data_item_list: list[AutoBean] = []
        self.all_active = False
        self.qlist_widget = getattr(ui, "listWidget_auto_list", None)
        self.currentTgAccount = None
        self.monitor_worker_thread = None
        self.monitor_scheduler_report_thread = None
        self.temp_water_image_abs_path = ""
        self.scheduler_thread = None
        self.single_task_thread = None
        self._froze_recovery_in_progress = False
        self._froze_restart_cb: Optional[Callable[[], Any]] = None
        self._froze_start_time = 0.0
        self._froze_stop_mono = False
        self._froze_restart_retries = 0
        self._froze_nudge_sent = False
        self._froze_restart_launched = False
        self._froze_l3_escalating = False
        self._froze_safety_gen = 0
        self._click_reset_timer = QTimer()
        self._click_reset_timer.setSingleShot(True)
        self._click_reset_timer.timeout.connect(self._reset_click_status)
        self._click_reset_timer.start(self.CLICK_RESET_INTERVAL_MS)
        self.init()

    def _reset_click_status(self) -> None:
        self.is_click = False

    def start_timer_reset_click_status(self) -> None:
        self.is_click = True
        self._click_reset_timer.start(self.CLICK_RESET_INTERVAL_MS)

    def init(self) -> None:
        bindings = (
            ("main_btn_items_jiao_chen", "clicked", self.shouItemsCourseDialog),
            ("main_ban_yun_monitor_jiao_chen", "clicked", self.shouBanYunMonitorCourseDialog),
            ("btn_changed_folder", "clicked", self.changedFolder),
            ("btn_g_water_pic_jiao_chen", "clicked", self.on_show_pic_water_jiao_chen),
            ("btn_g_water_select_pic", "clicked", self.on_select_pic),
            ("btn_start_monitor", "clicked", self.startMonitorByClick),
            ("btn_stop_monitor", "clicked", self.stopMonitorByClick),
            ("btn_auto_add_unkown1", "clicked", self.click_unkown1),
            ("btn_auto_add_unkown2", "clicked", self.click_unkown2),
            ("btn_auto_yun_yin_start", "clicked", self.autoTaskStartByClick),
            ("btn_auto_yun_yin_run_one", "clicked", self.autoTaskRunOneByClick),
            ("btn_auto_yun_yin_run_one_and_start", "clicked", self.autoTaskRunOneAndStartByClick),
            ("btn_auto_yun_yin_stop", "clicked", self.autoTaskStopByClick),
            ("btn_open_close_big_show", "clicked", self.openOrCloseBigShow),
            ("btn_copy_format_text", "clicked", self.copyFormatText),
            ("btn_close_left", "clicked", self.closeLeftLayout),
            ("btn_close_right", "clicked", self.closeRightLayout),
            ("btn_add_g_ad", "clicked", self.addGlobalAd),
            ("btn_auto_add_down_load", "clicked", self.addDownLoadFlowItem),
            ("btn_auto_add_item", "clicked", self.addBanYunFlowItem),
            ("btn_auto_add_flow", "clicked", self.addAutoFlowItem),
            ("btn_auto_add_yulan", "clicked", self.addYuLanFlowItem),
            ("btn_auto_add_yun_auto", "clicked", self.addYunAutoItem),
            ("btn_auto_add_yun_preview", "clicked", self.addYunPreViewItem),
            ("btn_auto_select_session", "clicked", self.selectTgAccount),
            ("btn_show_how", "clicked", self.openRateDesc),
            ("checkBox_auto_selected_all", "stateChanged", self.filter_all_select),
            ("listWidget_auto_list", "itemClicked", self.onItemClicked),
            ("checkBox_auto_changed_rate", "stateChanged", self.onAutoRateChanged),
            ("checkBox_enable_global_ad", "stateChanged", self.onGlobalAdEnableChanged),
            ("comboBox_dingshi_monitor", "currentIndexChanged", self.showDingshiMonitor),
            ("cb_g_water_mode", "currentIndexChanged", self.showWaterSelectMode),
        )
        for widget_name, signal_name, slot in bindings:
            owner = (
                _main_ui(self)
                if widget_name in {"btn_close_left", "btn_close_right"}
                else self.ui
            )
            _connect(getattr(owner, widget_name, None), signal_name, slot)

        widget = getattr(self.ui, "listWidget_auto_list", None)
        if widget is not None:
            widget.setContextMenuPolicy(Qt.CustomContextMenu)
            _connect(widget, "customContextMenuRequested", self.shoeMenu)
        ad_widget = getattr(self.ui, "listWidget_g_ad_list", None)
        if ad_widget is not None:
            ad_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            _connect(ad_widget, "customContextMenuRequested", self.shoeAdMenu)

        for signal_name, slot in (
            ("signal_yun_yin_data_changed", self.yunYinDataChanged),
            ("update_increase_auto_bean", self.updateUIWithAutoById),
            ("cmd_select_tg_account", self.selectTgAccountResult),
            ("cmd_monitor_update", self.updateMonitorPanel),
            ("show_dialog_signal", self.show_history_map_dialog_in_main_thread),
            ("cmd_update_monitor_status", self.update_monitor_status_tip),
            ("cmd_flood_descend_rate", self.onFloodDescendRate),
            ("cmd_auto_masu_rate", self.onAutoMasuRate),
            ("cmd_socket_env_reject", ac_r3_sk),
        ):
            _connect_signal(
                getattr(signals.global_ui_signal, signal_name, None),
                slot,
            )

        try:
            cache = tabl_cache.INSTANCE()
            monitor_option = cache.read_cache(
                tabl_cache.MAIN_BANYUN_MONITOR_SECTION,
                tabl_cache.MAIN_BANYUN_MONITOR_OPTION,
                "",
            )
            if monitor_option:
                _set_text(getattr(self.ui, "comboBox_dingshi_monitor", None), monitor_option)
            _set_enabled(
                getattr(self.ui, "checkBox_auto_changed_rate", None),
                bool(getattr(RateLimiterHelper, "is_auto_rate", lambda: False)()),
            )
        except Exception:
            return None
        self.initListDataSource()
        self.fillRightUIIfNeed()
        self.showTempFolder()
        self.showWaterSelectMode()
        self.displayAllActiveCheckBox()
        self.check_control_button_visile()

    def click_unkown1(self) -> None:
        for test in (
            self._test_pl_g_wp_flush,
            self._test_pl_k_dm_drain,
            self._test_pl_o_yt_purge,
            self._test_pl_s_bq_sweep,
            self._test_pl_v_hz_scrub,
            self._test_pl_n_lc_rinse,
        ):
            try:
                test()
            except Exception as exc:
                print("debug test failed:", exc)

    def _test_pl_g_wp_flush(self) -> Any:
        return _call(_qf_rn_file, "g_wp_flush")

    def _test_pl_k_dm_drain(self) -> Any:
        return _call(_hb_yt_file, "k_dm_drain")

    def _test_pl_o_yt_purge(self) -> Any:
        return _call(_cw_jm_file, "o_yt_purge")

    def _test_pl_s_bq_sweep(self) -> Any:
        return _call(_dr_vx_file, "s_bq_sweep")

    def _test_pl_v_hz_scrub(self) -> Any:
        return _call(_yg_bn_file, "v_hz_scrub")

    def _test_pl_n_lc_rinse(self) -> Any:
        return _call(_lk_ps_file, "n_lc_rinse")

    def _test_fdg_pw_rm_fire(self) -> Any:
        return _call(_fdg_pw_rm, "pw_rm_fire", self)

    def _test_fdg_os_kx_blow(self) -> Any:
        return _call(_fdg_os_kx, "os_kx_blow", self)

    def _test_fdg_ct_ew_drop(self) -> Any:
        return _call(_fdg_ct_ew, "ct_ew_drop")

    def _test_fdg_ct_is_snap(self) -> Any:
        return _call(_fdg_ct_is, "ct_is_snap")

    def _test_fdg_cm_rx_push(self) -> Any:
        return _call(_fdg_cm_rx, "cm_rx_push", self)

    def click_unkown2(self) -> None:
        for test in (
            self._test_fdg_pw_rm_fire,
            self._test_fdg_os_kx_blow,
            self._test_fdg_ct_ew_drop,
            self._test_fdg_ct_is_snap,
            self._test_fdg_cm_rx_push,
        ):
            try:
                test()
            except Exception as exc:
                print("debug test failed:", exc)

    def on_select_pic(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择图片",
            "",
            "图片文件 (*.jpg *.jpeg *.png)",
        )
        if not file_path:
            _tip("未选择任何图片")
            return
        self.temp_water_image_abs_path = str(file_path)
        self.set_elided_path(str(file_path))

    def set_elided_path(self, full_path: str) -> None:
        label = getattr(self.ui, "label_g_water_pic_path", None)
        if label is None:
            return
        elided_text = _call(CMCode, "elide_path_middle", full_path, 42) or full_path
        _set_text(label, elided_text)
        try:
            label.setToolTip("图片路径：" + str(full_path))
        except Exception:
            return None

    def on_show_pic_water_jiao_chen(self) -> None:
        try:
            ImageDialogHelper.unifyShowPicWaterCourse(self)
        except Exception as exc:
            print("打开图片水印教程失败：", exc)

    def showWaterSelectMode(self, *_args: Any) -> None:
        combo = getattr(self.ui, "cb_g_water_mode", None)
        mode = str(combo.currentText() if combo is not None else "")
        text_mode = mode in ("文字水印", "text", "")
        _set_visible(getattr(self.ui, "text_water_wrapper", None), text_mode)
        _set_visible(getattr(self.ui, "pic_water_wrapper", None), not text_mode)

    def changedWaterModeUIComponent(self, *_args: Any) -> None:
        self.showWaterSelectMode()
        _call(CommonCode, "refresh_water_mode_hint", self.ui)

    def _busy_worker_name(self) -> str:
        for attr_name, display_name in _ACTIVE_THREAD_NAMES:
            worker = getattr(self, attr_name, None)
            if worker is not None and bool(_call(worker, "isRunning")):
                return display_name
        return ""

    def _workers_still_active(self) -> bool:
        return bool(self._busy_worker_name())

    def _sync_worker_after_stop(self, context: Any = None) -> None:
        _call(TaskHardStop, "sync_worker_stop_state", self, context)
        if not self._workers_still_active():
            self._restore_ui_after_stop_request()

    def _try_start_worker(self, context: Any = None) -> bool:
        if self._workers_still_active() and not self._froze_recovery_in_progress:
            print("任务正在进行中，暂不能操作！", context or "")
            return False
        return True

    def _froze_mark_session_taken_over(self, reason: str = "") -> None:
        self._froze_recovery_in_progress = False
        self._froze_restart_launched = True
        print("监控收尾：新会话已接管，跳过旧 worker 的 UI 复位", reason or "")

    def _froze_release_recovery(self, reason: str = "") -> None:
        self._froze_safety_gen += 1
        self._froze_recovery_in_progress = False
        self._froze_restart_cb = None
        self._froze_stop_mono = False
        self._froze_restart_launched = False
        self._froze_l3_escalating = False
        _call(SuspendFrozenTag, "frozen_resume")
        if reason:
            print(reason)

    def _froze_on_start_gate_rejected(self, reason: str = "") -> None:
        if not self._froze_recovery_in_progress:
            return
        print("假死恢复门闸暂拒，ms 后重试：", reason or "")
        self._froze_restart_retries += 1
        if self._froze_restart_retries > self.FROZE_RESTART_MAX_RETRIES:
            self._froze_l3_escalate_then_restart(
                self._froze_restart_cb,
                self._froze_safety_gen,
            )
            return
        QTimer.singleShot(
            self.FROZE_RESTART_RETRY_MS,
            lambda: self._froze_attempt_restart(self._froze_safety_gen),
        )

    def _froze_safety_release_lock(self, gen: Any = None) -> None:
        if gen is None:
            gen = self._froze_safety_gen

        def release() -> None:
            if gen == self._froze_safety_gen:
                self._froze_release_recovery("假死恢复：安全超时，解除恢复锁")

        QTimer.singleShot(self.FROZE_SAFETY_RELEASE_MS, release)

    def _froze_safety_release_lock_final(self, gen: Any = None) -> None:
        if gen is None:
            gen = self._froze_safety_gen

        def force_release() -> None:
            if self._froze_recovery_in_progress and gen == self._froze_safety_gen:
                self._froze_release_recovery("假死恢复：硬超时强制解锁")

        QTimer.singleShot(self.FROZE_HARD_RELEASE_MS, force_release)

    def _froze_safety_force_release(self, gen: Any = None) -> None:
        if gen is not None and gen != self._froze_safety_gen:
            return
        self._froze_release_recovery("假死恢复：硬超时强制解锁")

    def on_program_suspected_frozen(self, reason: str = "") -> None:
        if self._froze_recovery_in_progress:
            return
        self._froze_recovery_in_progress = True
        self._froze_start_time = time.monotonic()
        self._froze_restart_retries = 0
        self._froze_nudge_sent = False
        self._froze_restart_launched = False
        self._froze_l3_escalating = False
        try:
            kid = str(
                getattr(SuspendFrozenTag, "current_increase_kid", "") or ""
            )
            record = getattr(SuspendFrozenTag, "_increase_progress", {}).get(kid)
            if kid and record:
                SuspendFrozenTag.apply_increase_skip_on_frozen(
                    kid,
                    record.get("parse_ids", []),
                )
            SuspendFrozenTag.clear_increase_group_progress()
        except Exception:
            pass
        _call(SuspendFrozenTag, "frozen_resume")
        _tip("检测到程序假死，自动重启！")
        _call(ProcessCache, "clean_all_type_but_mode", "monitor")
        self._froze_stop_monitor_and_restart()
        _ = reason

    def _froze_stop_timing_and_restart(self) -> None:
        self._froze_restart_cb = self._restart_auto_task
        self.stop_scheduler_thread()
        self.stop_single_task_thread()
        self._froze_begin_wait_then_restart(self._froze_restart_cb)

    def _froze_stop_monitor_and_restart(self) -> None:
        self._froze_restart_cb = self._restart_monitor
        try:
            self.stopMonitorReportor()
            self.stopMonitor("假死触发-停止监控", False)
        except Exception as exc:
            print("假死停止监控异常：", exc)
        self._froze_begin_wait_then_restart(self._froze_restart_cb)

    def _froze_begin_wait_then_restart(self, restart_cb: Any = None) -> None:
        self._froze_restart_cb = restart_cb
        if not self._froze_recovery_in_progress:
            self._froze_recovery_in_progress = True
            self._froze_start_time = time.monotonic()
        self._froze_safety_release_lock(self._froze_safety_gen)
        self._froze_safety_release_lock_final(self._froze_safety_gen)
        QTimer.singleShot(self.FROZE_IDLE_POLL_MS, self._froze_poll_idle_for_restart)

    def _froze_elapsed_ms(self) -> int:
        if not self._froze_start_time:
            return 0
        return int((time.monotonic() - self._froze_start_time) * 1000)

    def _froze_poll_idle_for_restart(self) -> None:
        if not self._froze_recovery_in_progress:
            return
        if self._workers_still_active():
            if self._froze_elapsed_ms() >= self.FROZE_STOP_WAIT_TIMEOUT_MS:
                self._froze_l3_escalate_then_restart(
                    self._froze_restart_cb,
                    self._froze_safety_gen,
                )
                return
            QTimer.singleShot(
                self.FROZE_IDLE_POLL_MS,
                self._froze_poll_idle_for_restart,
            )
            return
        self._froze_attempt_restart(self._froze_safety_gen)

    def _froze_attempt_restart(self, gen: Any = None) -> None:
        if not self._froze_recovery_in_progress:
            return
        if gen is not None and gen != self._froze_safety_gen:
            return
        if self._workers_still_active():
            self._froze_on_start_gate_rejected("假死恢复-重启前催停")
            return
        if self._froze_restart_cb is None:
            self._froze_release_recovery("假死恢复：无重启回调，解除恢复锁")
            return
        try:
            self._froze_restart_launched = True
            self._froze_restart_cb()
        finally:
            self._froze_release_recovery()

    def _froze_l3_escalate_then_restart(
        self,
        restart_cb: Any = None,
        safety_gen: Any = None,
    ) -> None:
        if safety_gen is not None and safety_gen != self._froze_safety_gen:
            return
        self._froze_l3_escalating = True
        if restart_cb is not None:
            self._froze_restart_cb = restart_cb
        print("假死恢复：催停重试用尽，强制结束幽灵 worker 后继续自动重启…")

        def after_force_kill() -> None:
            if self._workers_still_active():
                self._froze_mark_session_taken_over(
                    "假死恢复：强制收尸期间会话已在运行，跳过自动重启"
                )
                return
            print("假死恢复：强制结束幽灵 worker 完成，继续自动重启")
            if self._froze_restart_cb is None:
                self._froze_release_recovery("假死恢复：强制收尸后无重启回调")
                return
            self._froze_attempt_restart(self._froze_safety_gen)

        if not _call(TaskHardStop, "escalate_kill_ghost_workers_async", after_force_kill):
            _call(TaskHardStop, "force_teardown_ghost_workers")
            after_force_kill()

    def _restart_monitor(self) -> None:
        _call(ProcessCache, "update_Mode_text", "monitor")
        self.startMonitor()

    def _restart_auto_task(self) -> None:
        _call(ProcessCache, "update_Mode_text", "timing")
        self.autoTaskStart()

    def showDingshiMonitor(self, index: Any = None) -> None:
        combo = getattr(self.ui, "comboBox_dingshi_monitor", None)
        if combo is None:
            return
        if index is not None:
            try:
                combo.setCurrentIndex(int(index))
            except Exception:
                return None
        self.changedDingshiMonitorComponent()

    def changedDingshiMonitorComponent(self, *_args: Any) -> None:
        combo = getattr(self.ui, "comboBox_dingshi_monitor", None)
        value = str(combo.currentText() if combo is not None else "")
        try:
            tabl_cache.INSTANCE().update_cache(
                tabl_cache.MAIN_BANYUN_MONITOR_SECTION,
                tabl_cache.MAIN_BANYUN_MONITOR_OPTION,
                value,
            )
        except Exception:
            return None
        if hasattr(NewConfig, "MAIN_MODEL_DING_SHI_TEXT"):
            _set_visible(
                getattr(self.ui, "dingshi_container", None),
                value == str(getattr(NewConfig, "MAIN_MODEL_DING_SHI_TEXT")),
            )

    def shouItemsCourseDialog(self) -> None:
        try:
            ImageDialogHelper.unifyShowItemsCourse(self)
        except Exception as exc:
            print("打开条目教程失败：", exc)

    def shouBanYunMonitorCourseDialog(self) -> None:
        try:
            ImageDialogHelper.unifyShowBanYunAndMonitorCourse(self)
        except Exception as exc:
            print("打开搬运监控教程失败：", exc)

    def changedFolder(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(None, "选择文件夹", "C:\\")
        if not folder_path:
            return
        try:
            tabl_cache.INSTANCE().update_cache(
                tabl_cache.TOP_CACHE_GROUP,
                tabl_cache.DOWNLOAD_TEMP_FOLDER,
                folder_path,
            )
            utils.init_folder(folder_path)
            print("选中的文件夹: ", folder_path)
        except Exception as exc:
            print("设置临时文件夹失败：", exc)
        self.showTempFolder()

    def showTempFolder(self) -> None:
        try:
            folder = YunYinMaoConfig.get_temp_folder()
        except Exception:
            folder = ""
        _set_text(getattr(self.ui, "label_folder_text", None), folder)

    def closeLeftLayout(self) -> None:
        wrapper = getattr(self.ui, "zuobian_widget", None)
        if wrapper is None:
            return
        visible = not bool(wrapper.isVisible())
        _set_visible(wrapper, visible)
        _set_text(
            getattr(_main_ui(self), "btn_close_left", None),
            "关闭左侧" if visible else "打开左侧",
        )
        self.check_control_button_visile()

    def check_control_button_visile(self) -> None:
        left = getattr(self.ui, "zuobian_widget", None)
        right = getattr(self.ui, "youbian_widget", None)
        if left is not None:
            _set_text(
                getattr(_main_ui(self), "btn_close_left", None),
                "关闭左侧" if left.isVisible() else "打开左侧",
            )
        if right is not None:
            _set_text(
                getattr(_main_ui(self), "btn_close_right", None),
                "关闭右侧" if right.isVisible() else "打开右侧",
            )

    def closeRightLayout(self) -> None:
        wrapper = getattr(self.ui, "youbian_widget", None)
        if wrapper is None:
            return
        visible = not bool(wrapper.isVisible())
        _set_visible(wrapper, visible)
        _set_text(
            getattr(_main_ui(self), "btn_close_right", None),
            "关闭右侧" if visible else "打开右侧",
        )
        self.check_control_button_visile()

    def fillGlobalAdList(self) -> None:
        widget = getattr(self.ui, "listWidget_g_ad_list", None)
        if widget is None:
            return
        try:
            wrapper = getGlobalAd()
            UIAdListOp.fillAd2List(widget, wrapper.ades)
        except Exception as exc:
            print("刷新全局广告失败：", exc)

    def openRateDesc(self) -> None:
        try:
            QDesktopServices.openUrl(QUrl(str(YunYinMaoConfig.RATE_URL)))
        except Exception as exc:
            print("打开调速说明失败：", exc)

    def selectTgAccountResult(self, account: Any) -> None:
        if account is None:
            return
        if isinstance(account, dict):
            try:
                account = TGAuthAccount(**account)
            except Exception:
                account = account
        self.currentTgAccount = account
        try:
            json_string = json.dumps(account, ensure_ascii=False, default=_json_default)
            tabl_cache.INSTANCE().update_cache(
                tabl_cache.PROXY_SETTING_GROUP,
                tabl_cache.CURRENT_TASK_TG_ACCOUNT,
                json_string,
            )
        except Exception as exc:
            print("保存当前账号失败：", exc)
        _set_text(
            getattr(self.ui, "label_current_session", None),
            getattr(account, "nick", "") or getattr(account, "username", ""),
        )

    def selectTgAccount(self) -> None:
        try:
            dialog = TgAccountListDialog(self.mainWindow)
            dialog.exec_()
            selected = getattr(dialog, "selected_account", None)
            if selected is not None:
                self.selectTgAccountResult(selected)
        except Exception as exc:
            print("打开账号选择窗口失败：", exc)

    def updateUIWithAutoById(self, data: Any) -> None:
        kid = str(getattr(data, "kid", data if isinstance(data, str) else "") or "")
        if not kid:
            return
        for auto in self.ui_data_item_list:
            if str(getattr(auto, "kid", "")) == kid:
                auto.__dict__.update(getattr(data, "__dict__", {}))
                break
        self.fillListView()

    def yunYinDataChanged(self) -> None:
        self.initListDataSource()
        self.fillGlobalAdList()

    def filter_all_select(self, state: int) -> None:
        active = bool(state)
        try:
            from ..dclass.LoadDataClass import changedAllActiveStatus

            changedAllActiveStatus(active)
        except Exception:
            for auto in getAutoMap().values():
                auto.active = active
        self.all_active = active
        self.initListDataSource()

    def shoeAdMenu(self, pos: Any) -> None:
        widget = getattr(self.ui, "listWidget_g_ad_list", None)
        if widget is None:
            return
        item = widget.itemAt(pos)
        if item is None:
            return
        ad = item.data(Qt.UserRole)
        menu = QMenu(widget)
        edit = QAction("编辑全局广告", menu)
        edit.triggered.connect(lambda _=False, d=ad: self.editAdItem(d))
        menu.addAction(edit)
        dele = QAction("删除全局广告", menu)
        dele.triggered.connect(lambda _=False, d=ad: self.deleteAdItem(d))
        menu.addAction(dele)
        menu.exec_(widget.mapToGlobal(pos))

    def global_ad_call_back_add(self, ad: Any) -> None:
        try:
            from ..dclass.LoadDataClass import addGlobalAd

            addGlobalAd(ad)
        except Exception as exc:
            print("添加全局广告失败：", exc)
        self.fillGlobalAdList()

    def global_ad_call_back_update(self, ad: Any) -> None:
        try:
            updateGlobalAd(ad)
        except Exception as exc:
            print("更新全局广告失败：", exc)
        self.fillGlobalAdList()

    def addGlobalAd(self) -> None:
        try:
            dialog = AddOrEditAdDialog(
                self.mainWindow,
                "添加全局广告",
                self.global_ad_call_back_add,
                None,
                "",
                "",
            )
            dialog.exec_()
        except Exception as exc:
            print("打开全局广告窗口失败：", exc)

    def editAdItem(self, ad: Any) -> None:
        try:
            dialog = AddOrEditAdDialog(
                self.mainWindow,
                "编辑全局广告",
                self.global_ad_call_back_update,
                ad,
                str(getattr(ad, "adId", "") or ""),
                "",
            )
            dialog.exec_()
        except Exception as exc:
            print("编辑全局广告失败：", exc)

    def deleteAdItem(self, ad: Any) -> None:
        try:
            deleteGAd(str(getattr(ad, "adId", "") or ""))
        except Exception as exc:
            print("删除全局广告失败：", exc)
        self.fillGlobalAdList()

    def shoeMenu(self, pos: Any) -> None:
        widget = getattr(self.ui, "listWidget_auto_list", None)
        if widget is None:
            return
        item = widget.itemAt(pos)
        if item is None:
            return
        data = item.data(Qt.UserRole)
        if isinstance(data, str):
            data = getAutoBeanById(data)
        menu = QMenu(widget)
        for text, callback in (
            ("编辑条目", lambda: self.editItem(data)),
            ("快捷新增", lambda: self.copyItem(data)),
            ("删除条目", lambda: self.deleteItem(data)),
            ("复制文本", lambda: self.copyText(data)),
            ("清除资源记录", lambda: self.cleanRemember(data)),
        ):
            action = QAction(text, menu)
            action.triggered.connect(lambda _=False, cb=callback: cb())
            menu.addAction(action)
        menu.exec_(widget.mapToGlobal(pos))

    def copyItem(self, data: Any) -> None:
        auto = getAutoBeanById(getattr(data, "kid", "")) if not isinstance(data, AutoBean) else data
        if auto is None:
            return
        copied = copy.deepcopy(auto)
        copied.kid = str(utils.gen_id_by_ns())
        copied.name = (str(getattr(copied, "name", "") or "") + " 副本").strip()
        addOrUpdate(copied)
        self.initListDataSource()

    def editItem(self, data: Any) -> None:
        auto = getAutoBeanById(getattr(data, "kid", "")) if not isinstance(data, AutoBean) else data
        if auto is None:
            return
        dialog_cls = None
        title = "编辑条目"
        if auto.isBanYunType():
            dialog_cls, title = EditBanYunCommentItemEditDialog, "编辑搬运流"
        elif auto.isAutoFlowType():
            dialog_cls, title = EditAutoFlowItemEditDialog, "编辑自动流"
        elif auto.isYuLanFlowType():
            dialog_cls, title = EditYulanFlowItemEditDialog, "编辑预览流"
        elif auto.isDownLoadFlowType():
            dialog_cls, title = EditDownLoadItemEditDialog, "编辑下载流"
        elif auto.isYunAutoType():
            dialog_cls, title = EditYunAutoItemEditDialog, "编辑云自动"
        elif auto.isYunPreViewType():
            dialog_cls, title = EditYunPreViewItemEditDialog, "编辑云预览"
        else:
            _tip("暂不支持的类型条目！")
            return
        try:
            dialog = dialog_cls(self.mainWindow, title, auto, False, None)
            dialog.exec_()
            self.initListDataSource()
        except Exception as exc:
            print("打开编辑条目窗口失败：", exc)

    def openOrCloseBigShow(self) -> None:
        top = getattr(self.ui, "youbian_top_one", None)
        combo = getattr(self.ui, "comboBox_wrapper", None)
        visible = top is not None and top.isVisible()
        _set_visible(top, not visible)
        _set_visible(combo, not visible)
        _set_text(
            getattr(self.ui, "btn_open_close_big_show", None),
            "关闭监控大屏" if visible else "展开监控大屏",
        )

    def copyFormatText(self) -> None:
        selected = self.getActivateAutoBean()
        lines: list[str] = []
        for index, auto in enumerate(selected, 1):
            text = _call(DTopClassHelper, "genBeanFormatText", auto) or str(
                getattr(auto, "name", "") or ""
            )
            lines.append(f"第{index}个:\n\n{text}")
        utils.copy_text_to_clipboard("\n\n".join(lines))
        _tip("格式化文本复制成功！")

    def cleanRemember(self, data: Any) -> None:
        auto = getAutoBeanById(getattr(data, "kid", "")) if not isinstance(data, AutoBean) else data
        if auto is None:
            return
        _call(RememberManager, "cleanRememberIds", auto)
        _call(RandomBucketManager, "clean_buckets", getattr(auto, "source", ""), auto.kid)
        _tip("清除条目：" + str(getattr(auto, "name", "") or "") + " 的资源记录成功！")

    def copyText(self, data: Any) -> None:
        auto = getAutoBeanById(getattr(data, "kid", "")) if not isinstance(data, AutoBean) else data
        if auto is None:
            return
        text = _call(DTopClassHelper, "genBeanFormatText", auto) or str(auto)
        utils.copy_text_to_clipboard(text)
        _tip("格式化文本复制成功！")

    def deleteItem(self, data: Any) -> None:
        auto = getAutoBeanById(getattr(data, "kid", "")) if not isinstance(data, AutoBean) else data
        if auto is None:
            return
        deleteAutoBean(str(auto.kid))
        print("删除搬运流成功 ", getattr(auto, "name", "") or auto.kid)
        self.initListDataSource()

    def onItemClicked(self, item: Any) -> None:
        data = item.data(Qt.UserRole)
        if isinstance(data, str):
            data = getAutoBeanById(data)
        if data is not None:
            _call(data, "setSelect", True)

    def displayAllActiveCheckBox(self, state: Any = None) -> None:
        all_active = self.readAllActiveStatus()
        _set_text(
            getattr(self.ui, "checkBox_auto_selected_all", None),
            "全选" if all_active else "全不选",
        )
        checkbox = getattr(self.ui, "checkBox_auto_selected_all", None)
        if checkbox is not None:
            try:
                checkbox.blockSignals(True)
                checkbox.setChecked(bool(all_active))
            finally:
                try:
                    checkbox.blockSignals(False)
                except Exception:
                    return None
        _ = state

    def initListDataSource(self) -> None:
        autos = list(getAutoMap().values())
        autos.sort(key=lambda item: getattr(item, "priority", 0), reverse=True)
        self.ui_data_item_list = autos
        self.all_active = self.readAllActiveStatus()
        self.fillListView()
        self.displayAllActiveCheckBox()

    def readAllActiveStatus(self) -> bool:
        autos = list(getAutoMap().values())
        return bool(autos) and all(bool(getattr(item, "active", False)) for item in autos)

    def fillListView(self) -> None:
        widget = getattr(self.ui, "listWidget_auto_list", None)
        if widget is None:
            return
        try:
            ListOpHelper.fillYunYinMaoItemListView(widget, self.ui_data_item_list)
            return
        except Exception:
            widget.clear()
        for auto in self.ui_data_item_list:
            try:
                widget.addItem(
                    f"{auto.genTypeText()}  {getattr(auto, 'name', '') or auto.kid}"
                )
            except Exception:
                continue

    def checkParams(self, isMonitor: bool) -> Optional[dict[str, Any]]:
        selected = self.getActivateAutoBean()
        if not selected:
            _tip("你未选择任何条目数据，请先选择需要启动的条目！")
            return None
        session_abs_path = self.getSession()
        if not session_abs_path:
            return None
        if not self.check_item_ai_status_with_ai_api_key():
            return None
        rates = self.get_rate()
        if rates is None:
            return None
        down_load_rate, up_load_rate = rates
        missing_pic, missing_text = self._check_selected_items_water_resources()
        if missing_pic:
            _tip("以下勾选条目的图片水印资源不存在，请先选择有效图片后再启动：\n" + "\n".join(missing_pic))
            return None
        if missing_text:
            _tip("以下勾选条目的文字水印内容为空，请先填写水印文本后再启动：\n" + "\n".join(missing_text))
            return None
        try:
            check_post_permission = utils.strTobool(
                tabl_cache.INSTANCE().read_cache(
                    tabl_cache.MAIN_YUN_YIN_TAB_SECTION,
                    tabl_cache.CHECK_POST_PERMISSION,
                    "0",
                )
            )
        except Exception:
            check_post_permission = False
        delete_temp_files = _checked(getattr(self.ui, "checkBox_delete_temp_files", None))
        return {
            "selectedAutoBeanList": selected,
            "session_abs_path": session_abs_path,
            "check_post_permission": check_post_permission,
            "delete_temp_files": delete_temp_files,
            "down_load_rate": down_load_rate,
            "up_load_rate": up_load_rate,
            "water": self.genWaterBean(),
            "isMonitor": bool(isMonitor),
        }

    def _check_selected_items_water_resources(self) -> tuple[list[str], list[str]]:
        missing_pic: list[str] = []
        missing_text: list[str] = []
        en_pic = _checked(getattr(self.ui, "checkBox_g_pic_water", None))
        en_video = _checked(getattr(self.ui, "checkBox_g_video_water", None))
        for auto in self.getActivateAutoBean():
            water = getattr(auto, "water", None)
            if water is None:
                continue
            name = str(getattr(auto, "name", "") or getattr(auto, "kid", ""))
            mode = str(getattr(water, "mode", "") or "")
            if (en_pic or en_video) and mode in ("WATER_MODE_PIC", "图片水印"):
                path = str(getattr(water, "picPath", "") or "")
                if not path:
                    missing_pic.append(f"  · 条目「{name}」：未设置图片水印路径")
                elif not os.path.exists(path):
                    missing_pic.append(f"  · 条目「{name}」：{path} 文件不存在")
            if (en_pic or en_video) and mode in ("WATER_MODE_TEXT", "文字水印"):
                if not str(getattr(water, "text", "") or "").strip():
                    missing_text.append(f"  · 条目「{name}」：未设置文字水印内容")
        return missing_pic, missing_text

    def genWaterBean(self) -> Any:
        en_pic = _checked(getattr(self.ui, "checkBox_g_pic_water", None))
        en_video = _checked(getattr(self.ui, "checkBox_g_video_water", None))
        water_text = _text(getattr(self.ui, "lineEdit_g_water_text", None))
        combo = getattr(self.ui, "cb_g_water_mode", None)
        water_mode = str(combo.currentText() if combo is not None else "")
        minute_combo = getattr(self.ui, "comboBox_g_video_minute", None)
        index = minute_combo.currentIndex() if minute_combo is not None else 0
        duration = _call(CMCode, "parseVideoDuration", index) or 0
        pic_ratio_text = _text(getattr(self.ui, "line_edit_g_water_pic_ratio", None), "30")
        pic_ratio = _safe_int(pic_ratio_text.replace("%", ""), 30)
        return Water(
            enPic=en_pic,
            enVideo=en_video,
            text=water_text,
            picPath=self.temp_water_image_abs_path,
            mode="WATER_MODE_PIC" if "图片" in water_mode else "WATER_MODE_TEXT",
            duration=int(duration or 0),
            picRatio=pic_ratio,
        )

    def getSession(self, account: Any = None) -> str:
        if account is None:
            account = self.currentTgAccount
        if account is None:
            try:
                raw = tabl_cache.INSTANCE().read_cache(
                    tabl_cache.PROXY_SETTING_GROUP,
                    tabl_cache.CURRENT_TASK_TG_ACCOUNT,
                    "",
                )
                account = json.loads(str(raw)) if raw else None
            except Exception:
                account = None
        if account is None:
            _tip("请选择执行任务的电报账号！")
            return ""
        session_file = str(
            getattr(account, "session", "")
            or (account.get("session", "") if isinstance(account, dict) else "")
        )
        if not session_file:
            _tip("当前电报账号不可用，请重新选择，或者删除电报账号，重新添加电报账号！")
            return ""
        if os.path.isabs(session_file):
            abs_session_file = session_file
        else:
            abs_session_file = os.path.join(
                str(YunYinMaoConfig.abs_tg_account_dir()),
                session_file,
            )
        if not os.path.exists(abs_session_file):
            _tip("当前电报账号不可用，请重新选择，或者删除电报账号，重新添加电报账号！")
            return ""
        return abs_session_file

    def onAutoMasuRate(self, auto_rate_b: Any = None, monitor_text: Any = None) -> None:
        down = _safe_int(getattr(auto_rate_b, "down_rate", 0), 0)
        up = _safe_int(getattr(auto_rate_b, "up_rate", 0), 0)
        if down:
            _set_text(getattr(self.ui, "lineEdit_down_load_rate", None), str(down))
        if up:
            _set_text(getattr(self.ui, "lineEdit_up_load_rate", None), str(up))
        if monitor_text:
            _set_text(getattr(self.ui, "label_monitor_tip", None), monitor_text)

    def onFloodDescendRate(self, data: Any = None) -> None:
        down = _safe_int(getattr(data, "down_load_rate", 0), 0)
        up = _safe_int(getattr(data, "up_load_rate", 0), 0)
        if down:
            _set_text(getattr(self.ui, "lineEdit_down_load_rate", None), str(down))
        if up:
            _set_text(getattr(self.ui, "lineEdit_up_load_rate", None), str(up))
        tip = "发生洪水泛滥限制，已经自动为你调低了下载速率："
        if up:
            tip += f" 上传速率：{up}"
        _set_text(getattr(self.ui, "label_monitor_tip", None), tip)

    def update_monitor_status_tip(self, tip: Any) -> None:
        _set_text(getattr(self.ui, "label_monitor_tip", None), str(tip or ""))

    def show_history_map_dialog_in_main_thread(
        self,
        history_map: Any,
        confirm_callback: Any = None,
    ) -> None:
        if not history_map:
            if callable(confirm_callback):
                confirm_callback(True)
            return
        try:
            dialog = HistoryMessageOpDialog(
                self.mainWindow,
                history_map,
                confirm_callback,
            )
            dialog.exec_()
        except Exception as exc:
            print("打开历史消息窗口失败：", exc)
            if callable(confirm_callback):
                confirm_callback(False)

    def startMonitorByClick(self) -> None:
        self.start_timer_reset_click_status()
        print("手动点击-开始监控")
        self.startMonitor()

    def startMonitor(self) -> None:
        params = self.checkParams(True)
        if not params:
            return
        selected = params["selectedAutoBeanList"]
        try:
            history_map = MonitorHistoryManager.get_monitor_message_list(selected)
        except Exception:
            history_map = {}

        def final_start_monitor(ignore_historical_dialog: bool = False) -> None:
            if not self._try_start_worker("启动监控"):
                self._froze_on_start_gate_rejected("启动监控")
                return
            try:
                wrapper = DTopClassWrapper(timing=None, autolist=selected)
                for key, value in params.items():
                    setattr(wrapper, key, value)
                self.monitor_worker_thread = TelegramMonitorWorker(wrapper)
                _connect_signal(
                    getattr(self.monitor_worker_thread, "finished", None),
                    lambda: self._sync_worker_after_stop(),
                )
                self.monitor_worker_thread.start()
                self.startMonitorReporter()
                self.changeAllUiButStop(False)
                _set_text(getattr(self.ui, "label_monitor_tip", None), "监控中...")
                _call(ProcessCache, "update_Mode_text", "monitor")
            except Exception as exc:
                print("启动监控失败：", exc)
                self._restore_monitor_ui_after_stop_request()
            _ = ignore_historical_dialog

        if history_map:
            self.show_history_map_dialog_in_main_thread(history_map, final_start_monitor)
        else:
            final_start_monitor(True)

    def startMonitorReporter(self) -> None:
        try:
            self.monitor_scheduler_report_thread = MonitorSchedulerReportThread()
            self.monitor_scheduler_report_thread.start()
        except Exception as exc:
            print("启动监控看门狗失败：", exc)

    def autoTaskStopByClick(self) -> None:
        self.start_timer_reset_click_status()
        print("手动点击-停止任务")
        self.autoTaskStop()

    def autoTaskStop(self) -> None:
        _call(TaskHardStop, "request_hard_stop", "停止自动任务")
        self.stop_scheduler_thread()
        self.stop_single_task_thread()
        self._restore_ui_after_stop_request()
        _call(ProcessCache, "update_scheduler", "")
        _tip("定时任务已停止！")

    def _restore_ui_after_stop_request(self) -> None:
        self.changeAllUiButStop(True)
        _set_text(getattr(self.ui, "label_monitor_tip", None), "开始监控")

    def _restore_monitor_ui_after_stop_request(self) -> None:
        self._restore_ui_after_stop_request()
        _set_text(getattr(self.ui, "label_monitor_tip", None), "开始监控")

    def check_item_ai_status_with_ai_api_key(self) -> bool:
        ai_items: list[AutoBean] = []
        missing_name: list[str] = []
        for auto in self.getActivateAutoBean():
            ai_employee = getattr(auto, "aiEmployee", None)
            if ai_employee is None or not bool(getattr(ai_employee, "enable", False)):
                continue
            ai_items.append(auto)
            if getAiEmployee(getattr(ai_employee, "uid", 0)) is None:
                name = str(getattr(auto, "name", "") or getattr(auto, "source", ""))
                missing_name.append(name)
        if missing_name:
            _tip(
                "以下条目的AI员工找不到了【"
                + "，".join(missing_name)
                + "】，请你到编辑面板重新配置选择你的AI员工！"
            )
            return False
        if ai_items:
            try:
                has_key = bool(_sq_jqm.has_ai_ability_but_no_key())
            except Exception:
                has_key = False
            if has_key:
                _tip(
                    "以下条目开启了AI文案【"
                    + "，".join(
                        str(getattr(item, "name", "") or item.kid) for item in ai_items
                    )
                    + "】，但是你还没有配置专属AI API KEY，请你先按照教程配置！"
                )
                try:
                    ImageDialogHelper.unifyShowInputApiKeyCourse(self)
                except Exception:
                    return False
                return False
        return True

    def stopMonitorByClick(self) -> None:
        self.start_timer_reset_click_status()
        print("手动点击-停止监控")
        self.stopMonitor()

    def stopMonitor(
        self,
        msg: Any = "",
        blocking: Any = False,
        worker: Any = None,
    ) -> None:
        worker = worker or self.monitor_worker_thread
        _call(TaskHardStop, "request_hard_stop", str(msg or "停止监控"))
        if worker is not None:
            _call(worker, "requestInterruption")
            _call(worker, "quit")
            if blocking:
                _call(worker, "wait", self.WORKER_STOP_WAIT_MS)
        self.stopMonitorReportor()
        self.monitor_worker_thread = None
        self._restore_monitor_ui_after_stop_request()
        _tip("手动停止成功！")

    def stopMonitorReportor(self) -> None:
        reporter = self.monitor_scheduler_report_thread
        self.monitor_scheduler_report_thread = None
        if reporter is None:
            return
        _call(reporter, "requestInterruption")
        _call(reporter, "quit")
        _call(reporter, "wait", self.WORKER_STOP_WAIT_MS)

    def stopMonitorWorkerAndSchedulerIfNeed(self) -> None:
        if self.monitor_worker_thread is not None or self.monitor_scheduler_report_thread is not None:
            self.stopMonitor("停止监控", True)

    def final_stop_quit(self) -> None:
        self.stopMonitor("退出程序", True)
        self.autoTaskStop()
        self._froze_release_recovery()

    def autoTaskStartByClick(self) -> None:
        self.start_timer_reset_click_status()
        print("手动点击-启动定时任务")
        self.autoTaskStart()

    def autoTaskStart(self) -> None:
        params = self.checkParams(False)
        if not params:
            return
        if not self._try_start_worker("启动定时任务"):
            self._froze_on_start_gate_rejected("启动定时任务")
            return
        try:
            wrapper = DTopClassWrapper(timing=None, autolist=params["selectedAutoBeanList"])
            for key, value in params.items():
                setattr(wrapper, key, value)
            wrapper.finish_call = self.checkSuccessProcess
            self.scheduler_thread = SchedulerThread(wrapper)
            self.scheduler_thread.start()
            self.changeAllUiButStop(False)
            _call(ProcessCache, "update_scheduler", "定时任务运行中")
            _tip("启动定时任务")
        except Exception as exc:
            print("启动定时任务失败：", exc)
            self._restore_ui_after_stop_request()

    def checkSuccessProcess(self, success: bool) -> None:
        if success:
            _tip("任务完成")
        else:
            _tip("任务执行失败，请分析日志，查找原因！")
        self._restore_ui_after_stop_request()

    def stop_single_task_thread(self) -> None:
        worker = self.single_task_thread
        self.single_task_thread = None
        if worker is None:
            return
        _call(worker, "stop_qthread")
        _call(worker, "quit")
        _call(worker, "wait", self.WORKER_STOP_WAIT_MS)

    def stop_scheduler_thread(self) -> None:
        worker = self.scheduler_thread
        self.scheduler_thread = None
        if worker is None:
            return
        _call(worker, "stop_qthread")
        _call(worker, "quit")
        _call(worker, "wait", self.WORKER_STOP_WAIT_MS)

    def changeAllUiButStop(self, enable: bool) -> None:
        for name in (
            "btn_start_monitor",
            "btn_auto_yun_yin_start",
            "btn_auto_yun_yin_run_one",
            "btn_auto_yun_yin_run_one_and_start",
            "btn_auto_select_session",
            "btn_auto_add_item",
            "btn_auto_add_flow",
            "btn_auto_add_yulan",
            "btn_auto_add_down_load",
            "btn_auto_add_yun_auto",
            "btn_auto_add_yun_preview",
        ):
            _set_enabled(getattr(self.ui, name, None), enable)
        _set_enabled(getattr(self.ui, "btn_stop_monitor", None), not enable)
        _set_enabled(getattr(self.ui, "btn_auto_yun_yin_stop", None), not enable)

    def getActivateAutoBean(self) -> list[AutoBean]:
        return [
            auto
            for auto in getAutoMap().values()
            if bool(getattr(auto, "active", False))
        ]

    def autoTaskRunOneAndStartByClick(self) -> None:
        self.start_timer_reset_click_status()
        print("手动点击-执行一次并启动定时")
        self.autoTaskRunOneAndStart()

    def autoTaskRunOneAndStart(self) -> None:
        if not self.runOne(auto_start=True):
            return
        self.autoTaskStart()

    def autoTaskRunOneByClick(self) -> None:
        self.start_timer_reset_click_status()
        print("手动点击-手动执行一次")
        self.autoTaskRunOne()

    def autoTaskRunOne(self) -> None:
        self.runOne(auto_start=False)

    def runOne(self, auto_start: bool = False) -> bool:
        params = self.checkParams(False)
        if not params:
            return False
        if not self._try_start_worker("启动单次任务"):
            self._froze_on_start_gate_rejected("启动单次任务")
            return False
        try:
            wrapper = DTopClassWrapper(timing=None, autolist=params["selectedAutoBeanList"])
            for key, value in params.items():
                setattr(wrapper, key, value)
            wrapper.auto_start = bool(auto_start)
            wrapper.finish_call = self.checkSuccessProcessDoOne
            self.single_task_thread = SingleLongTaskThread(wrapper)
            self.single_task_thread.start()
            self.changeAllUiButStop(False)
            _tip("启动单次任务")
            return True
        except Exception as exc:
            print("启动单次任务失败：", exc)
            self._restore_ui_after_stop_request()
            return False

    def get_rate(self) -> Optional[tuple[int, int]]:
        down_text = _text(getattr(self.ui, "lineEdit_down_load_rate", None)).strip()
        up_text = _text(getattr(self.ui, "lineEdit_up_load_rate", None)).strip()
        if not down_text:
            _tip("请输入 超级下载每秒最大请求数 ，需要输入整数！")
            return None
        down_load_rate = _safe_int(down_text, 0)
        if down_load_rate <= 0:
            _tip("请输入 超级下载每秒最大请求数 ，需要输入整数并且大于0！")
            return None
        if not up_text:
            _tip("请输入 超级上传每秒最大请求数 ，需要输入整数！")
            return None
        up_load_rate = _safe_int(up_text, 0)
        if up_load_rate <= 0:
            _tip("请输入 超级上传每秒最大请求数 ，需要输入整数！")
            return None
        return down_load_rate, up_load_rate

    def checkSuccessProcessDoOne(self, success: bool, auto_start: bool = False) -> None:
        if success:
            _tip("执行一次任务完成")
        else:
            _tip("任务执行失败，请分析日志，查找原因！")
        self.single_task_thread = None
        if auto_start:
            self.autoTaskStart()
        else:
            self._restore_ui_after_stop_request()

    def onAutoRateChanged(self, state: int) -> None:
        enabled = bool(state)
        try:
            tabl_cache.INSTANCE().update_cache(
                tabl_cache.MAIN_YUN_YIN_TAB_SECTION,
                tabl_cache.MAIN_YUN_YIN_TAB_AUTO_CHANGE_RATE,
                "true" if enabled else "false",
            )
        except Exception:
            return None
        _call(
            RateLimiterHelper,
            "changed_rate",
            *RateLimiterHelper.get_auto_current_rate(),
        )

    def onGlobalAdEnableChanged(self, state: int) -> None:
        enabled = bool(state)
        try:
            wrapper = getGlobalAd()
            wrapper.adEnable = enabled
            updateSchedulerAndGlobalAd(getScheduler(), wrapper)
        except Exception as exc:
            print("更新全局广告设置失败：", exc)
        _set_visible(getattr(self.ui, "listWidget_g_ad_list", None), enabled)

    def addBanYunFlowItem(self) -> None:
        _open_flow_dialog(
            self,
            EditBanYunCommentItemEditDialog,
            "添加搬运流",
            AUTO_BEAN_TYPE_BAN_YUN,
        )

    def addDownLoadFlowItem(self) -> None:
        _open_flow_dialog(
            self,
            EditDownLoadItemEditDialog,
            "添加下载流",
            AUTO_BEAN_TYPE_DOWN_LOAD_FLOW,
        )

    def addYunPreViewItem(self) -> None:
        _open_flow_dialog(
            self,
            EditYunPreViewItemEditDialog,
            "添加云预览",
            AUTO_BEAN_TYPE_YUN_PRE_VIEW,
        )

    def addYunAutoItem(self) -> None:
        _open_flow_dialog(
            self,
            EditYunAutoItemEditDialog,
            "添加云自动",
            AUTO_BEAN_TYPE_YUN_AUTO,
        )

    def addAutoFlowItem(self) -> None:
        _open_flow_dialog(
            self,
            EditAutoFlowItemEditDialog,
            "添加自动流",
            AUTO_BEAN_TYPE_AUTO_FLOW,
        )

    def addYuLanFlowItem(self) -> None:
        _open_flow_dialog(
            self,
            EditYulanFlowItemEditDialog,
            "添加预览流",
            AUTO_BEAN_TYPE_YU_LAN_FLOW,
        )

    def fillRightUIIfNeed(self) -> None:
        self.fillGlobalAdList()
        try:
            checkbox = getattr(self.ui, "checkBox_enable_global_ad", None)
            wrapper = getGlobalAd()
            if checkbox is not None:
                checkbox.blockSignals(True)
                checkbox.setChecked(bool(wrapper.adEnable))
                checkbox.blockSignals(False)
        except Exception:
            return None
        self.genCheckingBoxs()

    def genCheckingBoxs(self) -> list[Any]:
        checked: list[Any] = []
        for index in range(24):
            checkbox = getattr(self.ui, f"checkBox{index}", None)
            if checkbox is not None and _checked(checkbox):
                checked.append(checkbox)
        return checked

    def updateMonitorPanel(self, wrapper: Any) -> None:
        label = getattr(_main_ui(self), "label_monitor_text", None)
        if label is None:
            return
        if not isinstance(wrapper, MonitorSignalBeanWrapper):
            data = wrapper
            wrapper = MonitorSignalBeanWrapper()
            setattr(wrapper, "beanList", getattr(data, "beanList", data or []))
        rows = []
        for bean in list(getattr(wrapper, "beanList", []) or []):
            if not isinstance(bean, MonitorSignalBean):
                bean = MonitorSignalBean(
                    updateTime=str(getattr(bean, "updateTime", "") or ""),
                    safeSource=str(getattr(bean, "safeSource", "") or ""),
                    queueSize=_safe_int(getattr(bean, "queueSize", 0), 0),
                    sended=_safe_int(getattr(bean, "sended", 0), 0),
                    total=_safe_int(getattr(bean, "total", 0), 0),
                    sendedTotal=_safe_int(getattr(bean, "sendedTotal", 0), 0),
                )
            rows.append(
                f"\n                        <tr>\n                            <td>{bean.updateTime}</td>\n"
                f"                            <td class='item-name'>{bean.safeSource}</td>\n"
                f"                            <td>{bean.queueSize}/{bean.sended}/{bean.total}</td>\n"
                f"                            <td class='total-sent'>{bean.sendedTotal}</td>\n"
                "                        </tr>\n                        "
            )
        label.setText(str(monitor_table_style_def) + "<table>" + "".join(rows) + "</table>")
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


__all__ = ["AutoYunYinTab"]
