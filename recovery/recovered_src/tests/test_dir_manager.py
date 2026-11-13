from __future__ import annotations

from src.py.com.yun.mao.util import DirManager


def test_dev_and_release_path_selection(monkeypatch):
    monkeypatch.setattr(DirManager._sq_hj, "hj_dev_ok", lambda: True)
    assert DirManager.get_union_code_dir() == DirManager.union_code_debug
    assert DirManager.get_local_data_dir() == DirManager.local_data_debug
    monkeypatch.setattr(DirManager._sq_hj, "hj_dev_ok", lambda: False)
    assert DirManager.get_union_code_dir() == DirManager.union_code_release
    assert DirManager.get_local_data_dir() == DirManager.local_data_release


def test_init_path_creates_directory(tmp_path):
    result = DirManager.init_path("nested", tmp_path)
    assert (tmp_path / "nested").is_dir()
    assert result == str(tmp_path / "nested")


def test_hidden_helpers_are_safe_on_missing_paths(tmp_path):
    missing = tmp_path / "missing"
    assert DirManager.is_hidden(missing) is False
    assert DirManager.hid_file(missing) is False
    DirManager.set_hidden_recursive("missing", tmp_path)
