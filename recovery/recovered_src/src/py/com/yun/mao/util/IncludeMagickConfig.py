# Recovered module: src.py.com.yun.mao.util.IncludeMagickConfig
from __future__ import annotations

from . import ResourcePath


IMAGEMAGICK_BINARY = ResourcePath.get_magick_path()


def setup_magick_config(imagemagick_binary: str = IMAGEMAGICK_BINARY) -> None:
    try:
        from moviepy.config import change_settings

        change_settings({"IMAGEMAGICK_BINARY": str(imagemagick_binary)})
    except Exception:
        return None
    return None
