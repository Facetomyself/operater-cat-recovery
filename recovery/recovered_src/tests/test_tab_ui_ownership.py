from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAB_DIR = ROOT / "src" / "py" / "com" / "yun" / "mao" / "tab"


def test_session_tab_reads_main_window_proxy_controls():
    source = (TAB_DIR / "mid_session_fun_tab.py").read_text(encoding="utf-8")
    for name in ("btn_proxy_setting", "cb_enable_proxy", "tabWidget_important"):
        assert f'getattr(self.ui, "{name}"' not in source
        assert f'getattr(_main_ui(self), "{name}"' in source
    assert '_main_ui(tab)' in source


def test_auto_tab_reads_main_window_log_and_monitor_widgets():
    source = (TAB_DIR / "mid_auto_yun_yin_tab.py").read_text(encoding="utf-8")
    for name in ("btn_close_left", "btn_close_right", "label_monitor_text"):
        assert f'getattr(self.ui, "{name}"' not in source
        assert f'getattr(_main_ui(self), "{name}"' in source
    assert 'widget_name in {"btn_close_left", "btn_close_right"}' in source


def test_comment_rule_btn_save_delegates_to_the_real_save_path():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "comment"
        / "ConfigCommentRuleDialog.py"
    ).read_text(encoding="utf-8")
    assert "def btnSave(self) -> None:" in source
    assert "self.saveCommentRule()" in source
    assert "self.ui.textEdit_text" not in source
