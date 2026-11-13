# Recovered module: src.py.com.yun.mao.util.ResourcePath
# Path candidates are taken directly from the module constants.
from __future__ import annotations

from pathlib import Path

from src.resource import RESOURCE_ROOT_DIR


def _first_existing(possible_paths) -> str:
    paths = [Path(item) for item in possible_paths]
    for path in paths:
        if path.exists():
            return str(path)
    return str(paths[0]) if paths else ""


def get_ui_path(ui_filename: str) -> str:
    return _first_existing(
        (
            Path(RESOURCE_ROOT_DIR) / "ui" / "static" / ui_filename,
            Path("ui") / "static" / ui_filename,
        )
    )


def get_ico_path(ico_filename: str) -> str:
    return _first_existing(
        (
            Path(RESOURCE_ROOT_DIR) / "ico" / ico_filename,
            Path("ico") / ico_filename,
        )
    )


def get_drawable_path(name: str) -> str:
    return _first_existing(
        (
            Path(RESOURCE_ROOT_DIR) / "drawable" / name,
            Path("drawable") / name,
        )
    )


def drawable_is_exists(name: str) -> bool:
    return Path(get_drawable_path(name)).exists()


def ico_is_exists(icon_name: str) -> bool:
    return Path(get_ico_path(icon_name)).exists()


def _third_path(filename: str) -> str:
    return _first_existing(
        (
            Path(RESOURCE_ROOT_DIR) / "third" / filename,
            Path("third") / filename,
            Path(filename),
        )
    )


def get_ffmpeg_path() -> str:
    return _third_path("ffmpeg-win-x86_64-v7.1.exe")


def get_magick_path() -> str:
    return _third_path("magick.exe")


def get_ttf_path() -> str:
    return _third_path("ttf_song_jian_ti.TTF")
