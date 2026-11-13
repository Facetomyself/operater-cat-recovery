# Recovered module: src.py.com.yun.mao.auto.ProcessCache
# Global process cache plus the UI refresh signals.  The update/clean functions
# were recovered from the module init qword slots and their decompiled bodies.
from __future__ import annotations

from src.py.com.yun.mao.util.need import signals


CACHE_PROCESS_STR = ""
CACHE_PRESENT = ""
CACHE_MODE_TEXT = ""
CACHE_TYPE_TEXT = ""
CACHE_SUB_TYPE_TEXT = ""
FORWARD_MODE = ""
SCHEDULER_STR = ""


def update_process(process):
    global CACHE_PROCESS_STR

    CACHE_PROCESS_STR = process
    signals.global_ui_signal.cmd_update_process.emit("")


def update_present(present):
    global CACHE_PRESENT

    CACHE_PRESENT = present
    signals.global_ui_signal.cmd_update_process.emit("")


def update_Mode_text(top_text):
    global CACHE_MODE_TEXT

    CACHE_MODE_TEXT = top_text
    signals.global_ui_signal.cmd_update_process.emit("")


def update_type_text(type_text):
    global CACHE_TYPE_TEXT

    CACHE_TYPE_TEXT = type_text
    signals.global_ui_signal.cmd_update_process.emit("")


def update_sub_type_text(sub_type_text):
    global CACHE_SUB_TYPE_TEXT

    CACHE_SUB_TYPE_TEXT = sub_type_text
    signals.global_ui_signal.cmd_update_process.emit("")


def update_forward_mode_text(forward_mode):
    global FORWARD_MODE

    FORWARD_MODE = forward_mode
    signals.global_ui_signal.cmd_update_process.emit("")


def update_scheduler(scheduler):
    global SCHEDULER_STR

    SCHEDULER_STR = scheduler
    signals.global_ui_signal.cmd_update_process.emit("")


def clean_all_type_but_mode():
    """Clear process/type fields while keeping the selected mode text."""

    global CACHE_PROCESS_STR
    global CACHE_PRESENT
    global CACHE_TYPE_TEXT
    global CACHE_SUB_TYPE_TEXT
    global FORWARD_MODE

    CACHE_PROCESS_STR = ""
    CACHE_PRESENT = ""
    CACHE_TYPE_TEXT = ""
    CACHE_SUB_TYPE_TEXT = ""
    FORWARD_MODE = ""
