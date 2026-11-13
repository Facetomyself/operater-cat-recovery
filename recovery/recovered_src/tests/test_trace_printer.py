from __future__ import annotations

import re

from src.py.com.yun.mao.config import YunYinMaoConfig
from src.py.com.yun.mao.util import TracePrinterHelper


def test_date_and_time_formats():
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", TracePrinterHelper.get_format_date())
    assert re.fullmatch(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
        TracePrinterHelper.get_format_time(),
    )


def test_print_trace_writes_error_log(tmp_path, monkeypatch):
    monkeypatch.setattr(
        YunYinMaoConfig,
        "multi_abs_log_dir",
        str(tmp_path),
        raising=False,
    )
    path = TracePrinterHelper.print_trace("custom stack")
    assert path.endswith("_error.log")
    content = open(path, "r", encoding="utf-8").read()
    assert "详细异常栈追踪" in content
    assert "custom stack" in content
