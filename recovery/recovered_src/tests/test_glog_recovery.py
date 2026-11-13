from __future__ import annotations

import time
from pathlib import Path

from src.py.com.yun.mao.log import LocalLogSetting
from src.py.com.yun.mao.log.glog import GlobalLog, MAX_PENDING_UI_LINES


ROOT = Path(__file__).resolve().parents[1]


class _Browser:
    def __init__(self):
        self.lines = []

    def append(self, text):
        self.lines.append(text)


class _UI:
    def __init__(self):
        self.text_brow_log = _Browser()


def test_global_log_constructor_fields():
    log = GlobalLog(frozen_timeout_seconds=12)
    try:
        assert log.frozen_threshold_ms == 12000
        assert log._ui_attached is False
        assert log._ui_log_paused is False
        assert log.last_message_ended_with_newline is True
        assert log.last_log == []
    finally:
        log.cleanup()


def test_merge_tail_lines_removes_overlap():
    log = GlobalLog(frozen_timeout_seconds=1)
    try:
        merged = log._merge_tail_lines(
            ["a", "b", "c"],
            ["c", "d"],
            10,
        )
        assert merged == ["a", "b", "c", "d"]
    finally:
        log.cleanup()


def test_attach_ui_and_pause_queue(monkeypatch):
    monkeypatch.setattr(LocalLogSetting, "appendToLogInner", lambda text: None)
    log = GlobalLog()
    ui = _UI()
    try:
        log.attach_ui(ui)
        assert log.ui is ui
        assert log._ui_attached is True
        log.pause_ui_log()
        log.write("first\nsecond")
        assert log._pending_ui_lines == ["first", "second"]
        assert len(log._pending_ui_lines) <= MAX_PENDING_UI_LINES
        log.resume_ui_log()
        assert ui.text_brow_log.lines == ["first", "second"]
    finally:
        log.cleanup()


def test_global_log_emits_frozen_signal_on_timeout():
    log = GlobalLog(frozen_timeout_seconds=1)
    try:
        class _Signal:
            def __init__(self):
                self.emitted = False

            def emit(self):
                self.emitted = True

        signal = _Signal()
        log.frozeDetected = signal
        log.last_log_time = time.time() - 2
        log._on_frozen_timeout()
        assert signal.emitted is True
    finally:
        log.cleanup()


def test_global_log_cleanup_guards_active_thread():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "log"
        / "glog.py"
    ).read_text(encoding="utf-8")
    assert "self.log_thread.isActive()" in source
