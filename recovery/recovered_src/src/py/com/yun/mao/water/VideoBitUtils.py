# Recovered module: src.py.com.yun.mao.water.VideoBitUtils
# Reconstruction from Nuitka constants and offline Hex-Rays.
from __future__ import annotations

import math
import subprocess

import cv2
import numpy as np
from moviepy.video.VideoClip import TextClip

from src.py.com.yun.mao.util import ResourcePath


def get_video_bitrate(video_path: str) -> float:
    try:
        cap = cv2.VideoCapture(video_path)
        bit = cap.get(cv2.CAP_PROP_BITRATE)
        cap.release()
        return float(bit or 0)
    except Exception as e:
        print(e)
        return 0.0


def get_video_fps(video_path: str) -> float:
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        return float(fps or 0)
    except Exception as e:
        print(e)
        return 0.0


def change_bit(in_path: str, out_path: str, bit: str) -> None:
    try:
        ffmpeg = ResourcePath.get_ffmpeg_path()
        command = [
            ffmpeg,
            "-i",
            in_path,
            "-vcodec",
            "copy",
            "-acodec",
            "copy",
            "-b:v",
            str(bit),
            out_path,
        ]
        subprocess.run(command, check=True)
    except Exception as e:
        print(e)


def adjust_bitrate(
    source_bitrate: float,
    min_bitrate: float = 1000,
    max_bitrate: float = 5000,
    reduction_ratio: float = 0.7,
) -> int:
    try:
        src = float(source_bitrate)
    except (TypeError, ValueError):
        src = max(min_bitrate, 1e-06)
    src = max(src, 1.0)
    soft_end = max_bitrate * 0.93
    gentle_ratio = max(0.35, reduction_ratio)
    if src <= soft_end:
        return int(round(src))
    span = max_bitrate - soft_end
    if span <= 0:
        return int(round(max_bitrate))
    t = min(1.0, max(0.0, (src - soft_end) / span))
    effective = 1.0 - (1.0 - gentle_ratio) * t
    out = src * effective
    return int(round(max(min_bitrate, min(max_bitrate, out))))


def adjust_framerate(
    source_fps: float,
    min_fps: float = 24,
    max_fps: float = 60,
    reduction_ratio: float = 0.75,
) -> int:
    try:
        src = float(source_fps)
    except (TypeError, ValueError):
        src = max(min_fps, 1e-06)
    src = max(src, 1.0)
    soft_end = max_fps * 0.93
    gentle_ratio = max(0.35, reduction_ratio)
    if src <= soft_end:
        return round(src)
    span = max_fps - soft_end
    if span <= 0:
        return round(max_fps)
    t = min(1.0, max(0.0, (src - soft_end) / span))
    effective = 1.0 - (1.0 - gentle_ratio) * t
    out = src * effective
    return round(max(min_fps, min(max_fps, out)))


def gen_text_clip(
    water_text_: str, font_: str, font_size_: int
) -> TextClip:
    text_clip_ = TextClip(
        water_text_,
        font=font_,
        fontsize=font_size_,
        color="white",
    )
    return text_clip_


def gen_bit_data(
    video: str, bit: tuple[float, float, float] = (1000, 5000, 0.7)
) -> int:
    source_bitrate = get_video_bitrate(video)
    print("source bit ", source_bitrate, "")
    tar_bitrate = adjust_bitrate(source_bitrate, *bit)
    print(" ->tar bit params ", tar_bitrate, "k")
    return tar_bitrate


def gen_fps_data(
    video: str, fps: tuple[float, float, float] = (24, 60, 0.75)
) -> int:
    source_fps = get_video_fps(video)
    print("source fps ", source_fps, "")
    tart_fps = adjust_framerate(source_fps, *fps)
    print(" ->tar fps params ", tart_fps)
    return tart_fps


def animate_text(
    t: float, fps: float, text_width: int, video_size: tuple[int, int]
) -> tuple[int, int]:
    text_height = 110
    frequency_x = 0.1
    frequency_y = 0.12
    x_margin = 2
    y_margin = 10
    video_width, video_height = video_size
    start_x = (video_width - text_width) / 2
    start_y = (video_height - text_height) / 2
    amplitude_x = max(0, (video_width - text_width) / 2 - x_margin)
    amplitude_y = max(0, (video_height - text_height) / 2 - y_margin)
    phase_x = t * frequency_x * 2 * np.pi / max(fps, 1.0)
    phase_y = t * frequency_y * 2 * np.pi / max(fps, 1.0)
    x = start_x + amplitude_x * math.sin(phase_x)
    y = start_y + amplitude_y * math.sin(phase_y)
    return int(x), int(y)
