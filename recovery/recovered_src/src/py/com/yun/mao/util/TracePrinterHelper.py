# Recovered module: src.py.com.yun.mao.util.TracePrinterHelper
from __future__ import annotations

import os
import time
import traceback
from pathlib import Path


def get_format_date() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())


def get_format_time() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def gen_log_file() -> str:
    try:
        from ..config import YunYinMaoConfig

        base = Path(YunYinMaoConfig.multi_abs_log_dir)
    except Exception:
        base = Path.home() / "YunYinData" / "log"
    base.mkdir(parents=True, exist_ok=True)
    return str(base / (get_format_date() + "_error.log"))


def print_trace(stack_info: str | None = None) -> str:
    """Append the current exception trace and return the log path."""
    log_file = gen_log_file()
    text = stack_info or traceback.format_exc()
    try:
        from src.py.version_code import version_code
    except Exception:
        version_code = ""
    payload = (
        "详细异常栈追踪: \n"
        "--------------------------------------------------\n"
        "软件版本: " + str(version_code) + "\n"
        "时间: " + get_format_time() + "\n"
        + str(text)
        + "\n"
    )
    try:
        with open(log_file, "a", encoding="utf-8") as handle:
            handle.write(payload)
        print("发生了异常，异常信息已经记录到文件：" + log_file)
    except Exception:
        pass
    _ = os
    return log_file
