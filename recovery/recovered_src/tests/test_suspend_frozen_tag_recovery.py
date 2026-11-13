from __future__ import annotations

from pathlib import Path

from src.py.com.yun.mao.util import SuspendFrozenTag


ROOT = Path(__file__).resolve().parents[1]


def test_frozen_resume_is_a_one_shot_flag():
    SuspendFrozenTag.check_frozen_timeout()
    SuspendFrozenTag.frozen_resume()
    assert SuspendFrozenTag.check_frozen_timeout() is True
    assert SuspendFrozenTag.check_frozen_timeout() is False


def test_clear_increase_group_progress_resets_state():
    SuspendFrozenTag.note_increase_group_progress("kid-1", [1, 2, 3])
    assert SuspendFrozenTag.current_increase_kid == "kid-1"
    assert SuspendFrozenTag.current_increase_next_start_id == 3
    SuspendFrozenTag.clear_increase_group_progress()
    assert SuspendFrozenTag.current_increase_kid == ""
    assert SuspendFrozenTag.current_increase_next_start_id == 0
    assert SuspendFrozenTag._increase_progress == {}


def test_note_increase_group_progress_records_next_start_id():
    SuspendFrozenTag.note_increase_group_progress("kid-2", [10, 15, 22])
    record = SuspendFrozenTag._increase_progress["kid-2"]
    assert record["parse_ids"] == [10, 15, 22]
    assert record["next_start_id"] == 22
    SuspendFrozenTag.clear_increase_group_progress()


def test_apply_increase_skip_on_frozen_forwards_last_id(monkeypatch):
    calls = []
    monkeypatch.setattr(
        SuspendFrozenTag,
        "_apply_increase_skip",
        lambda kid, next_id: calls.append((kid, next_id)) or True,
    )
    assert SuspendFrozenTag.apply_increase_skip_on_frozen("k", [1, 5, 7]) is True
    assert calls == [("k", 8)]
    assert SuspendFrozenTag.apply_increase_skip_on_frozen("k", []) is False


def test_frozen_recovery_tab_wires_skip_and_clear():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "tab"
        / "mid_auto_yun_yin_tab.py"
    ).read_text(encoding="utf-8")
    assert "SuspendFrozenTag.apply_increase_skip_on_frozen(" in source
    assert "SuspendFrozenTag.clear_increase_group_progress()" in source
    assert '"current_increase_kid"' in source


def test_foreach_to_send_records_increase_progress():
    source = (
        ROOT
        / "src"
        / "py"
        / "com"
        / "yun"
        / "mao"
        / "auto"
        / "AutoWorkerWrapper.py"
    ).read_text(encoding="utf-8")
    assert "SuspendFrozenTag.note_increase_group_progress(kid, parse_ids)" in source
