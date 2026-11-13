# Recovered module: src.py.com.yun.mao.util.need.signals
# Qt signal bus.  The fallback keeps pure-Python imports usable without PyQt5.
from __future__ import annotations

try:
    from PyQt5.QtCore import QObject, pyqtSignal
except Exception:
    class QObject:
        def __init__(self, *args, **kwargs):
            pass

    class _Signal:
        def __get__(self, instance, owner):
            return None

    def pyqtSignal(*args, **kwargs):
        return _Signal()


class UISignals(QObject):
    cmd_refresh_private_send_tab_user_list = pyqtSignal()
    cmd_refresh_private_send_tab_bot_list = pyqtSignal()
    msg_stop_listener = pyqtSignal()
    msg_init_sender_success_listener = pyqtSignal()
    auto_chat_init_session_result = pyqtSignal(bool)
    auto_chat_session_join_group_result = pyqtSignal(bool)
    auto_chat_exception_to_stop = pyqtSignal()
    verify_secret_result = pyqtSignal()
    listener_send_sd_success = pyqtSignal()
    cmd_env_checked_result = pyqtSignal(bool, str)
    reset_code_success = pyqtSignal()
    tip_dialog_cmd = pyqtSignal(str)
    tip_dialog_size_cmd = pyqtSignal(int)
    tip_dialog_restart_cmd = pyqtSignal(int)
    report_status_waring = pyqtSignal(str)
    zw_except_re_try = pyqtSignal()
    auto_read_next_msg = pyqtSignal()
    cmd_login_code = pyqtSignal()
    cmd_listener_login_code_failed = pyqtSignal()
    signal_display_hua_shu_detail = pyqtSignal(str)
    signal_yun_yin_data_changed = pyqtSignal()
    signal_employee_data_changed = pyqtSignal()
    update_increase_auto_bean = pyqtSignal(object)
    update_icon_states = pyqtSignal()
    update_account_list = pyqtSignal()
    cmd_select_tg_account = pyqtSignal(object)
    cmd_update_process = pyqtSignal(object)
    cmd_monitor_update = pyqtSignal(object)
    show_dialog_signal = pyqtSignal(object)
    notify_link_integrity_fail = pyqtSignal()
    cmd_socket_env_reject = pyqtSignal()
    report_conn_timing_fault = pyqtSignal()
    cmd_cert_anchor_mismatch = pyqtSignal()
    notify_crypto_ctx_broken = pyqtSignal()
    cmd_marshal_pipeline_halt = pyqtSignal()
    report_init_resp_corrupted = pyqtSignal()
    cmd_probe_light_fault = pyqtSignal()
    report_probe_mid_fault = pyqtSignal()
    cmd_probe_full_fault = pyqtSignal()
    notify_secondary_scan_fault = pyqtSignal()
    cmd_update_monitor_status = pyqtSignal(object)
    cmd_update_stats = pyqtSignal(object)
    cmd_migrate_code_stats = pyqtSignal(bool, str)
    cmd_activate_code_stats = pyqtSignal(bool)
    cmd_post_ad_stats = pyqtSignal(object)
    cmd_create_order_success = pyqtSignal(object)
    cmd_create_order_failed = pyqtSignal(str)
    cmd_check_order_stats = pyqtSignal(bool, object)
    cmd_flood_descend_rate = pyqtSignal(object)
    cmd_auto_masu_rate = pyqtSignal(object)
    invoke_on_main_thread = pyqtSignal(object)


global_ui_signal = UISignals()
