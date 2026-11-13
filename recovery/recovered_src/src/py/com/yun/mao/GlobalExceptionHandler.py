# Recovered module: src.py.com.yun.mao.GlobalExceptionHandler
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

import asyncio
import os
import sys
import traceback

from PyQt5.QtWidgets import QApplication

from src.py import version_code

from . import ErrorDialog
from .config import YunYinMaoConfig
from .util.need import utils


global_window = None


def custom_excepthook(exc_type, exc_value, exc_traceback) -> None:
    if issubclass(exc_type, asyncio.CancelledError):
        return

    error_msg = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )

    def log_error(error_msg: str) -> None:
        log_dir = str(YunYinMaoConfig.multi_abs_log_dir)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(
            log_dir,
            str(utils.get_format_date()) + "_error.log",
        )
        now_time = utils.get_format_time()
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("--------------------------------------------------\n")
            f.write("软件版本: " + str(getattr(version_code, "version", "")) + "\n")
            f.write("时间: " + str(now_time) + "\n")
            f.write("异常类型: " + str(exc_type.__name__) + "\n")
            f.write("异常信息: " + str(exc_value) + "\n")
            f.write("堆栈跟踪: \n" + str(error_msg) + "\n")
            f.write("--------------------------------------------------\n")
        print("异常已记录到 " + log_file + "，程序即将退出。")

    log_error(error_msg)

    app = QApplication.instance()
    if app is not None:
        ErrorDialog.show_error_tip(
            "程序发生异常，请你把日志目录的日志发给客服解决。\n"
            "弹窗10秒后自动退出。",
            10000,
        )

    window = global_window
    if window is None:
        try:
            from .MainWindow import YunYinMaoMainWindow

            window = getattr(YunYinMaoMainWindow, "globalInstance", None)
        except Exception:
            window = None
    final_quit = getattr(window, "final_quit", None)
    if callable(final_quit):
        final_quit()
    elif app is not None:
        app.quit()


sys.excepthook = custom_excepthook
