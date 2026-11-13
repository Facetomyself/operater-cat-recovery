from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
UI_DIR = ROOT.parent / "ui" / "static"
UI_REF = re.compile(r"""['"]([^'"]+\.ui)['"]""")


def test_referenced_ui_files_exist_and_parse():
    references = set()
    for path in SOURCE.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="replace")
        references.update(UI_REF.findall(text))

    assert references
    missing = sorted(name for name in references if not (UI_DIR / name).is_file())
    assert missing == []

    widget_count = 0
    for name in sorted(references):
        tree = ET.parse(UI_DIR / name)
        widget_count += len(tree.findall(".//widget"))
    assert widget_count > 0


def test_receive_code_dialog_binds_self_ui():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "dialog"
        / "ReceiveCodeDialog.py"
    ).read_text(encoding="utf-8")
    assert 'self.ui = uic.loadUi(' in source
    assert '"receive_code_dialog.ui"' in source


def test_experience_dialog_binds_self_ui():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "dialog"
        / "ExpriActivatePermissionDialog.py"
    ).read_text(encoding="utf-8")
    assert 'self.ui = uic.loadUi(' in source
    assert '"self_experience_dialog.ui"' in source


def test_tip_dialog_show_event_uses_recovered_size_factors():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "util"
        / "need"
        / "TipDialog.py"
    ).read_text(encoding="utf-8")
    assert "screen_width * 5.0 / 6.0" in source
    assert "screen_height * 2.5 / 6.0" in source
    assert "screen_width * 1.2 / 4.0" in source
    assert "screen_height * 1.5 / 6.0" in source


def test_add_edit_ad_show_event_uses_recovered_factors():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "ad"
        / "AddOrEditAdDialog.py"
    ).read_text(encoding="utf-8")
    assert "screen_width * 4 / 10" in source
    assert "screen_height * 3 / 10" in source
    assert "(screen_width - window_width) / 2" in source
    assert "(screen_height - window_height) / 6" in source


def test_course_image_dialog_show_event_uses_recovered_factors():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "dialog"
        / "CourseImageDialog.py"
    ).read_text(encoding="utf-8")
    assert "setMinimumSize(1080, 768)" in source
    assert "(screen_width - self.width()) / 2" in source
    assert "(screen_height - self.height()) / 8" in source


def test_history_message_op_dialog_show_event_uses_recovered_factors():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "monitor"
        / "HistoryMessageOpDialog.py"
    ).read_text(encoding="utf-8")
    assert "screen_width * 3 / 5" in source
    assert "screen_height * 7 / 10" in source
    assert "(screen_width - window_width) / 2" in source
    assert "(screen_height - window_height) / 6" in source


def test_premium_big_price_dialog_show_event_factors():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "dialog"
        / "PremiumBigPriceDialog.py"
    ).read_text(encoding="utf-8")
    assert "screen_width * 4.0 / 10.0" in source
    assert "screen_height * 15.0 / 20.0" in source
    assert "(screen_height - window_height) / 2) - 30" in source


def test_ai_model_info_price_dialog_show_event_factors():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "dialog"
        / "AiModelInfoPriceDialog.py"
    ).read_text(encoding="utf-8")
    assert "screen_width * 4.0 / 10.0" in source
    assert "screen_height * 8.0 / 20.0" in source
    assert "(screen_height - window_height) / 2) - 30" in source


def test_expri_activate_permission_dialog_show_event_factors():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "dialog"
        / "ExpriActivatePermissionDialog.py"
    ).read_text(encoding="utf-8")
    assert "int(screen_width / 2)" in source
    assert "int(screen_height / 6)" in source
    assert "(screen_height - window_height) / 10" in source


def test_premium_dialog_show_event_factors():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "dialog"
        / "PremiumDialog.py"
    ).read_text(encoding="utf-8")
    assert "screen_width * 5.6 / 10.0" in source
    assert "screen_height * 12.5 / 20.0" in source
    assert "(screen_height - window_height) / 2) - 30" in source


def test_receive_code_dialog_fixed_size():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "dialog"
        / "ReceiveCodeDialog.py"
    ).read_text(encoding="utf-8")
    assert "_DIALOG_WIDTH = 540" in source
    assert "_DIALOG_HEIGHT = 300" in source
