from __future__ import annotations

import sys
import types


def _install_fake_moviepy(monkeypatch):
    moviepy = types.ModuleType("moviepy")
    editor = types.ModuleType("moviepy.editor")

    class VideoFileClip:
        def __init__(self, *args, **kwargs):
            pass

    editor.VideoFileClip = VideoFileClip
    moviepy.editor = editor
    monkeypatch.setitem(sys.modules, "moviepy", moviepy)
    monkeypatch.setitem(sys.modules, "moviepy.editor", editor)


def test_filter_script_dir_uses_string_cache_path(monkeypatch, tmp_path):
    _install_fake_moviepy(monkeypatch)
    from src.py.com.yun.mao.auto import GenSegmentVideoOnePass

    monkeypatch.setattr(
        GenSegmentVideoOnePass.YunYinMaoConfig,
        "abs_cache_only_multi_dir",
        str(tmp_path),
        raising=False,
    )
    monkeypatch.setattr(
        GenSegmentVideoOnePass.utils,
        "init_folder",
        lambda path: True,
    )
    assert GenSegmentVideoOnePass._filter_complex_script_dir() == str(
        tmp_path / "_filter_complex_script_dir"
    )
