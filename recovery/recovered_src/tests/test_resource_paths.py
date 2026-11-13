from __future__ import annotations

from src.py.com.yun.mao.util import ResourcePath


def test_resource_paths_keep_expected_filenames():
    assert ResourcePath.get_ffmpeg_path().endswith("ffmpeg-win-x86_64-v7.1.exe")
    assert ResourcePath.get_magick_path().endswith("magick.exe")
    assert ResourcePath.get_ttf_path().endswith("ttf_song_jian_ti.TTF")
    assert ResourcePath.get_ui_path("main.ui").endswith("main.ui")
