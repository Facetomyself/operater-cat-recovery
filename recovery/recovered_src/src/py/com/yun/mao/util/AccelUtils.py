# Recovered module: src.py.com.yun.mao.util.AccelUtils
# Reconstruction from Nuitka constants, source signatures, function maps, and
# the offline Hex-Rays module init.  Uncertain thresholds/edge choices are
# explicitly marked inferred.
from __future__ import annotations

import os
import random
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter

from src.py.com.yun.mao.util import ResourcePath
from src.py.com.yun.mao.util.moviepy_ffmpeg_patch import (
    apply_moviepy_ffmpeg_stderr_patch,
)
from moviepy.editor import VideoFileClip

apply_moviepy_ffmpeg_stderr_patch()

ACCEL_MODE_AUTO = "auto"
ACCEL_MODE_GPU = "gpu"
ACCEL_MODE_CPU = "cpu"

GPU_AUTO_CPU_LOCK_AFTER_FALLBACK_STREAK = 20

creationflags_no_console = int(
    getattr(subprocess, "CREATE_NO_WINDOW", 0) or 0
)

_runtime_auto_gpu_failure_streak_water = 0
_runtime_auto_gpu_exhausted_water = False
_runtime_auto_gpu_failure_streak_preview = 0
_runtime_auto_gpu_exhausted_preview = False

_COVER_MIN_FILE_BYTES = 1024  # inferred
_COVER_TOP_K = 8
_COVER_PREVIEW_WIDTH = 320
_COVER_JPEG_QUALITY_PREVIEW = 8  # inferred
_COVER_JPEG_QUALITY_HD = 2
_COVER_FFMPEG_TIMEOUT_SEC = 12.0
_COVER_FFMPEG_HD_TIMEOUT_SEC = 12.0  # inferred; names/values are adjacent
_COVER_CANDIDATE_COUNT = 5
_COVER_CANDIDATE_FAIL_ABORT = 3  # inferred
_COVER_END_EPS_SEC = 0.02
_COVER_SHORT_DURATION_SEC = 3.0  # inferred
_COVER_HEAD_RATIO = 0.08
_COVER_TAIL_RATIO = 0.45
_COVER_DHASH_SIZE = 32
_COVER_DHASH_THRESHOLD = 10


def normalize_accel_mode(accel_mode: str | None) -> str:
    mode = str(accel_mode or ACCEL_MODE_AUTO).strip().lower()
    if mode not in (ACCEL_MODE_AUTO, ACCEL_MODE_GPU, ACCEL_MODE_CPU):
        print(
            "未知加速模式 ",
            accel_mode,
            "，自动回退为 ",
            ACCEL_MODE_AUTO,
        )
        return ACCEL_MODE_AUTO
    return mode


def note_water_session_gpu_encode_success() -> None:
    global _runtime_auto_gpu_failure_streak_water
    global _runtime_auto_gpu_exhausted_water
    _runtime_auto_gpu_failure_streak_water = 0
    _runtime_auto_gpu_exhausted_water = False


def note_water_session_auto_gpu_fallback_after_hw_failed() -> None:
    global _runtime_auto_gpu_failure_streak_water
    global _runtime_auto_gpu_exhausted_water
    _runtime_auto_gpu_failure_streak_water += 1
    if (
        _runtime_auto_gpu_failure_streak_water
        >= GPU_AUTO_CPU_LOCK_AFTER_FALLBACK_STREAK
    ):
        _runtime_auto_gpu_exhausted_water = True


def effective_accel_mode_water(
    accel_mode: str | None,
    motion: Any = None,
) -> tuple[str, Any]:
    mode = normalize_accel_mode(accel_mode)
    if mode == ACCEL_MODE_AUTO and _runtime_auto_gpu_exhausted_water:
        mode = ACCEL_MODE_CPU
    return mode, motion


def note_preview_session_gpu_encode_success() -> None:
    global _runtime_auto_gpu_failure_streak_preview
    global _runtime_auto_gpu_exhausted_preview
    _runtime_auto_gpu_failure_streak_preview = 0
    _runtime_auto_gpu_exhausted_preview = False


def note_preview_session_auto_gpu_fallback_after_hw_failed() -> None:
    global _runtime_auto_gpu_failure_streak_preview
    global _runtime_auto_gpu_exhausted_preview
    _runtime_auto_gpu_failure_streak_preview += 1
    if (
        _runtime_auto_gpu_failure_streak_preview
        >= GPU_AUTO_CPU_LOCK_AFTER_FALLBACK_STREAK
    ):
        _runtime_auto_gpu_exhausted_preview = True


def effective_accel_mode_preview(accel_mode: str | None) -> str:
    mode = normalize_accel_mode(accel_mode)
    if mode == ACCEL_MODE_AUTO and _runtime_auto_gpu_exhausted_preview:
        return ACCEL_MODE_CPU
    return mode


def subprocess_no_console_kwargs() -> dict[str, int]:
    flags = int(creationflags_no_console or 0)
    if not flags:
        return {}
    return {"creationflags": flags}


def probe_ffmpeg_encoders(
    ffmpeg_path: str,
    encoder: str = "h264_nvenc",
) -> bool:
    try:
        result = subprocess.run(
            [str(ffmpeg_path), "-hide_banner", "-encoders"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=False,
            **subprocess_no_console_kwargs(),
        )
    except (OSError, ValueError):
        return False
    if result.returncode != 0:
        return False
    output = f"{result.stdout or ''}\n{result.stderr or ''}"
    return str(encoder or "").lower() in output.lower()


def is_ffmpeg_available(ffmpeg_path: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [str(ffmpeg_path), "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=False,
            timeout=_COVER_FFMPEG_TIMEOUT_SEC,
            **subprocess_no_console_kwargs(),
        )
    except Exception as exc:
        return False, f"ffmpeg unavailable: {exc}"
    if result.returncode == 0:
        return True, "ok"
    detail = (result.stderr or result.stdout or "").strip()
    if detail:
        return False, f"ffmpeg unavailable: {detail}"
    return False, "ffmpeg unavailable"


def resolve_ffmpeg_bin() -> str | None:
    try:
        ffmpeg = ResourcePath.get_ffmpeg_path()
    except Exception:
        print("ffmpeg exe not found")
        return None
    if not ffmpeg:
        print("ffmpeg exe not found")
        return None
    path = os.fspath(ffmpeg)
    if not os.path.isfile(path):
        print("ffmpeg exe not found")
        return None
    return path


def detect_gpu_profiles(
    ffmpeg_path: str = "",
) -> list[tuple[str, str, list[str]]]:
    ffmpeg = str(ffmpeg_path or resolve_ffmpeg_bin() or "")
    profiles: list[tuple[str, str, list[str]]] = []
    if not ffmpeg:
        return profiles
    encoders = {
        "h264_nvenc": ("nvidia", ["-preset", "p5", "-rc", "vbr"]),
        "h264_qsv": ("intel", []),
        "h264_amf": ("amd", ["-quality", "balanced"]),
    }
    for encoder, (vendor, vendor_params) in encoders.items():
        if probe_ffmpeg_encoders(ffmpeg, encoder):
            profiles.append((vendor, encoder, list(vendor_params)))
    return profiles


def build_gpu_encode_attempts(
    profiles: list[tuple[str, str, list[str]]],
) -> list[tuple[str, str, str, list[str]]]:
    attempts: list[tuple[str, str, str, list[str]]] = []
    for profile in profiles or []:
        if not isinstance(profile, (tuple, list)) or len(profile) < 2:
            continue
        vendor = str(profile[0] or "")
        encoder = str(profile[1] or "")
        vendor_params = list(profile[2]) if len(profile) > 2 else []
        if encoder == "h264_nvenc":
            attempts.append(
                (
                    "nvenc-vbr-p5",
                    encoder,
                    vendor,
                    list(vendor_params) + ["-profile:v", "high"],
                )
            )
            attempts.append(
                (
                    "nvenc-cbr-p4",
                    encoder,
                    vendor,
                    ["-preset", "p4", "-rc", "cbr", "-profile:v", "high"],
                )
            )
            attempts.append(
                (
                    "nvenc-vbr-p3-main",
                    encoder,
                    vendor,
                    ["-preset", "p3", "-rc", "vbr", "-profile:v", "main"],
                )
            )
        elif encoder == "h264_qsv":
            attempts.append(
                ("qsv-default-high", encoder, vendor, list(vendor_params))
            )
            attempts.append(
                (
                    "qsv-main-no-lookahead",
                    encoder,
                    vendor,
                    ["-look_ahead", "0", "-profile:v", "main"],
                )
            )
        elif encoder == "h264_amf":
            attempts.append(
                ("amf-balanced-high", encoder, vendor, list(vendor_params))
            )
            attempts.append(
                (
                    "amf-speed-main",
                    encoder,
                    vendor,
                    ["-quality", "speed", "-profile:v", "main"],
                )
            )
        else:
            attempts.append(
                ("default", encoder, vendor, list(vendor_params))
            )
    return attempts


def _ffmpeg_output_has_audio_stream(text: str) -> bool:
    return bool(
        re.search(
            r"Stream #\d+:\d+[^\n]*Audio:",
            text or "",
            re.IGNORECASE,
        )
    )


def _probe_video_meta(
    ffmpeg_path: str,
    input_file: str,
) -> tuple[float, int, int, bool]:
    cmd = [str(ffmpeg_path), "-nostdin", "-i", str(input_file)]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=8.0,
            check=False,
            **subprocess_no_console_kwargs(),
        )
    except subprocess.TimeoutExpired:
        print("ffmpeg probe timed out")
        return 0.0, 0, 0, False
    except Exception as exc:
        print("ffmpeg probe failed: ", exc)
        return 0.0, 0, 0, False

    text = f"{result.stdout or ''}\n{result.stderr or ''}".replace(
        "\r", "\n"
    )
    duration = 0.0
    width = 0
    height = 0
    dur_m = re.search(
        r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)",
        text,
    )
    if dur_m:
        h = int(dur_m.group(1))
        m = int(dur_m.group(2))
        s = float(dur_m.group(3))
        duration = h * 3600 + m * 60 + s
    else:
        print("cannot parse video duration from ffmpeg -i")

    res_m = re.search(r"Video:.*?(\d{3,})x(\d{2,})", text, re.DOTALL)
    if res_m:
        width = int(res_m.group(1))
        height = int(res_m.group(2))
    else:
        print("cannot parse video resolution from ffmpeg -i")

    has_audio = _ffmpeg_output_has_audio_stream(text)
    return float(duration), int(width), int(height), bool(has_audio)


def _read_video_attr(file_path: str) -> tuple[float, int, int]:
    try:
        video = VideoFileClip(str(file_path), audio=False)
    except (TypeError, ValueError):
        return 0.0, 0, 0
    try:
        duration = float(video.duration or 0.0)
        width, height = video.size
        return duration, int(width), int(height)
    except (TypeError, ValueError):
        return 0.0, 0, 0
    finally:
        try:
            video.close()
        except Exception:
            _ = None


def probe_video_meta_with_audio(
    input_file: str,
) -> tuple[float, int, int, bool]:
    ffmpeg = resolve_ffmpeg_bin()
    if ffmpeg:
        try:
            duration, width, height, has_audio = _probe_video_meta(
                ffmpeg, input_file
            )
            if duration > 0.0 and width > 0 and height > 0:
                return duration, width, height, has_audio
        except Exception as exc:
            print("ffmpeg probe failed: ", exc)
    try:
        duration, width, height = _read_video_attr(input_file)
        return duration, width, height, True
    except Exception:
        return 0.0, 0, 0, False


def probe_video_meta_wrapper(input_file: str) -> dict[str, Any]:
    duration, width, height, _ = probe_video_meta_with_audio(input_file)
    return {
        "duration": float(duration),
        "width": int(width),
        "height": int(height),
    }


def input_has_audio(ffmpeg: str, input_file: str) -> bool:
    try:
        result = subprocess.run(
            [str(ffmpeg), "-nostdin", "-i", str(input_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=8.0,
            check=False,
            **subprocess_no_console_kwargs(),
        )
    except Exception:
        return False
    text = f"{result.stdout or ''}\n{result.stderr or ''}"
    return _ffmpeg_output_has_audio_stream(text)


def _safe_duration(duration: Any) -> float:
    try:
        value = float(duration)
    except (TypeError, ValueError):
        return 0.0
    if value != value:
        return 0.0
    if value == float("inf") or value == float("-inf"):
        return 0.0
    return max(0.0, value)


def _is_nonempty_file(path: str) -> bool:
    try:
        return os.path.getsize(path) >= _COVER_MIN_FILE_BYTES
    except OSError:
        try:
            os.remove(path)
        except OSError:
            return False
        return False


def _is_readable_image(path: str) -> bool:
    try:
        with Image.open(path) as img:
            img.load()
            width, height = img.size
            return width > 0 and height > 0
    except Exception:
        return False


def _histogram_mean_var(hist: list[int]) -> tuple[float, float]:
    total = float(sum(hist))
    if total <= 0.0:
        return 0.0, 0.0
    mean = sum(index * count for index, count in enumerate(hist)) / total
    var = (
        sum(
            (index - mean) ** 2 * count
            for index, count in enumerate(hist)
        )
        / total
    )
    return float(mean), float(var)


def _score_cover_image(path: str) -> float:
    try:
        with Image.open(path) as img:
            img.load()
            rgb = img.convert("RGB")
            gray = rgb.convert("L")
            hist = gray.histogram()
            total = float(sum(hist))
            luma_mean, luma_var = _histogram_mean_var(hist)
            exposure = (
                sum(hist[18:237]) / total if total > 0.0 else 0.0
            )
            contrast = min(1.0, luma_var / 2800.0)
            edges = gray.filter(ImageFilter.FIND_EDGES)
            _, edge_var = _histogram_mean_var(edges.histogram())
            sharpness = min(1.0, edge_var / 2000.0)
            hsv = rgb.convert("HSV")
            sat_hist = hsv.split()[1].histogram()
            sat_mean, _ = _histogram_mean_var(sat_hist)
            color = min(1.0, sat_mean / 255.0)
            _ = luma_mean
            return float(
                exposure * 0.5
                + contrast * 0.25
                + sharpness * 0.15
                + color * 0.1
            )
    except Exception:
        return float("-inf")


def _image_dhash(img: Image.Image) -> int:
    size = _COVER_DHASH_SIZE
    gray = img.convert("L").resize(
        (size + 1, size),
        Image.Resampling.BILINEAR,
    )
    pixels = list(gray.getdata())
    width = gray.width
    value = 0
    for row in range(size):
        row_off = row * width
        for col in range(size):
            left = pixels[row_off + col]
            right = pixels[row_off + col + 1]
            value = (value << 1) | int(left > right)
    return int(value)


def _dhash_file(path: str) -> int | None:
    if not _is_nonempty_file(path):
        return None
    try:
        with Image.open(path) as img:
            img.load()
            return _image_dhash(img)
    except Exception:
        return None


def _dhash_distance(left: int, right: int) -> int:
    return int(left ^ right).bit_count()


def _hashes_too_similar(
    dhash: int,
    exclude_hashes: list[int],
    threshold: int = _COVER_DHASH_THRESHOLD,
) -> bool:
    return any(
        _dhash_distance(dhash, used) <= int(threshold)
        for used in (exclude_hashes or [])
    )


def _cover_sample_window(
    duration: float,
    end_eps: float = _COVER_END_EPS_SEC,
) -> tuple[float, float]:
    duration_value = _safe_duration(duration)
    end_eps_value = _safe_duration(end_eps)
    start = 0.0
    end = max(0.0, duration_value - end_eps_value)
    if duration_value > _COVER_SHORT_DURATION_SEC:
        start = min(end, duration_value * _COVER_HEAD_RATIO)
        end = max(start, end - duration_value * _COVER_TAIL_RATIO)
    return float(start), float(end)


def _cover_candidate_count(duration: float) -> int:
    duration_value = _safe_duration(duration)
    if duration_value <= 0.0:
        return 0
    if duration_value <= _COVER_SHORT_DURATION_SEC:
        return 1
    return _COVER_CANDIDATE_COUNT


def _cover_slot_window(
    duration: float,
    slot_index: int,
    slot_count: int,
) -> tuple[float, float]:
    start, end = _cover_sample_window(duration)
    count = max(1, int(slot_count or 1))
    index = max(0, min(count - 1, int(slot_index or 0)))
    span = max(0.0, end - start) / count
    slot_start = start + span * index
    slot_end = slot_start + span
    return float(slot_start), float(slot_end)


def _cover_min_gap(
    duration: float,
    exclude_count: int,
    window: tuple[float, float] | None,
) -> float:
    start, end = window or _cover_sample_window(duration)
    span = max(0.0, end - start)
    excluded = max(0, int(exclude_count or 0))
    usable = max(1, _COVER_CANDIDATE_COUNT - excluded)
    by_split = span / usable if usable else span
    gap = min(3.0, max(_COVER_HEAD_RATIO, by_split))
    gap = max(_COVER_HEAD_RATIO, min(gap, by_split * 0.45))
    slot_span = span / max(1, _COVER_CANDIDATE_COUNT)
    return float(max(0.0, min(gap, slot_span)))


def _cover_candidate_times(
    duration: float,
    count: int | None = None,
    window: tuple[float, float] | None = None,
) -> list[float]:
    sample_count = int(count or _cover_candidate_count(duration))
    if sample_count <= 0:
        return []
    start, end = window or _cover_sample_window(duration)
    span = max(0.0, end - start)
    if span <= 0.0:
        return [float(max(0.0, start))]
    times: list[float] = []
    for index in range(sample_count):
        bucket_start = start + span * index / sample_count
        bucket_end = start + span * (index + 1) / sample_count
        times.append(float(random.uniform(bucket_start, bucket_end)))
    return times


def _fallback_cover_time(duration: float) -> float:
    value = _safe_duration(duration) * 0.5
    return float(min(2.0, max(0.0, value)))


def _time_too_close(
    t: float,
    exclude_times: list[float],
    min_gap: float,
) -> bool:
    return any(
        abs(float(t) - float(used)) < float(min_gap or 0.0)
        for used in (exclude_times or [])
    )


def _fallback_cover_time_away(
    duration: float,
    exclude_times: list[float],
    min_gap: float,
    window: tuple[float, float] | None,
) -> float:
    if not exclude_times:
        return _fallback_cover_time(duration)
    start, end = window or _cover_sample_window(duration)
    mid = (start + end) / 2.0
    candidates = [
        start + (end - start) * index / 8.0 for index in range(9)
    ]
    best = mid
    best_dist = -1.0
    for index, t in enumerate(candidates):
        _ = index
        dist = min(
            (abs(t - float(used)) for used in exclude_times),
            default=1000000000.0,
        )
        if dist > best_dist:
            best = t
            best_dist = dist
    if _time_too_close(best, exclude_times, min_gap):
        return float(min(end, max(start, mid)))
    return float(best)


def _pick_highlight_time(
    scored: list[tuple[float, float]],
    top_k: int = _COVER_TOP_K,
) -> float | None:
    ranked = sorted(
        scored or [],
        key=lambda item: item[0],
        reverse=True,
    )[: max(1, int(top_k or 1))]
    if not ranked:
        return None
    chosen = random.choice(ranked)
    return float(chosen[1])


def _pick_diverse_cover(
    scored: list[tuple[float, float, int]],
    exclude_times: list[float],
    exclude_hashes: list[int],
    min_gap: float,
    top_k: int = _COVER_TOP_K,
) -> tuple[float, float, int] | None:
    usable: list[tuple[float, float, int]] = []
    for item in scored or []:
        if not isinstance(item, (tuple, list)) or len(item) < 3:
            continue
        score, t, dhash = item[0], item[1], item[2]
        if _time_too_close(t, exclude_times, min_gap):
            continue
        if _hashes_too_similar(int(dhash), exclude_hashes):
            continue
        if any(
            abs(float(t) - float(other[1])) < float(min_gap or 0.0)
            for other in usable
        ):
            continue
        usable.append((float(score), float(t), int(dhash)))
    pool = usable or [
        (float(item[0]), float(item[1]), int(item[2]))
        for item in (scored or [])
        if isinstance(item, (tuple, list)) and len(item) >= 3
    ]
    far = [
        item
        for item in pool
        if not _time_too_close(item[1], exclude_times, min_gap)
    ]
    ranked = sorted(
        far or pool,
        key=lambda item: item[0],
        reverse=True,
    )[: max(1, int(top_k or 1))]
    if not ranked:
        return None
    unique: list[tuple[float, float, int]] = []
    for item in ranked:
        if _hashes_too_similar(item[2], exclude_hashes):
            continue
        unique.append(item)
    return random.choice(unique or ranked)


def _build_cover_ffmpeg_cmd(
    ffmpeg: str,
    video_path: str,
    out_path: str,
    t: float,
    scale_width: int | None,
    quality: int,
) -> list[str]:
    seek = f"{max(0.0, _safe_duration(t)):.3f}"
    cmd = [
        str(ffmpeg),
        "-y",
        "-loglevel",
        "error",
        "-ss",
        seek,
        "-i",
        os.fspath(video_path),
        "-an",
        "-sn",
        "-dn",
        "-frames:v",
        "1",
        "-q:v",
        str(int(quality)),
        "-threads",
        "1",
    ]
    if scale_width:
        cmd.extend(["-vf", f"scale={int(scale_width)}:-2"])
    cmd.append(os.fspath(out_path))
    return cmd


def _safe_unlink(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        return


def _ffmpeg_extract_frame(
    ffmpeg: str,
    video_path: str,
    out_path: str,
    t: float,
    scale_width: int | None = None,
    quality: int = _COVER_JPEG_QUALITY_HD,
    timeout: float = _COVER_FFMPEG_TIMEOUT_SEC,
) -> bool:
    cmd = _build_cover_ffmpeg_cmd(
        ffmpeg,
        video_path,
        out_path,
        t,
        scale_width,
        quality,
    )
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=float(timeout),
            check=False,
            **subprocess_no_console_kwargs(),
        )
    except subprocess.TimeoutExpired:
        print("ffmpeg 截帧超时: t=", round(_safe_duration(t), 3), "s")
        _safe_unlink(out_path)
        return False
    except Exception:
        _safe_unlink(out_path)
        return False
    if result.returncode != 0:
        _safe_unlink(out_path)
        return False
    if not _is_nonempty_file(out_path):
        _safe_unlink(out_path)
        return False
    return True


def _normalize_exclude_times(
    values: list[float] | None,
) -> list[float]:
    times: list[float] = []
    for item in values or []:
        value = _safe_duration(item)
        if value not in times:
            times.append(value)
    return times


def _normalize_exclude_hashes(
    values: list[int] | None,
) -> list[int]:
    hashes: list[int] = []
    for item in values or []:
        try:
            value = int(item)
        except (TypeError, ValueError):
            continue
        if value not in hashes:
            hashes.append(value)
    return hashes


def _score_cover_preview_file(path: str) -> float:
    if not _is_nonempty_file(path):
        return float("-inf")
    return _score_cover_image(path)


def _extract_highlight_cover(
    video_path: str,
    thumb_path: str,
    exclude_times: list[float] | None = None,
    exclude_hashes: list[int] | None = None,
    slot_index: int = 0,
    slot_count: int = 1,
) -> tuple[bool, float | None, int | None]:
    ffmpeg = resolve_ffmpeg_bin()
    if not ffmpeg:
        return False, None, None
    duration, _, _, _ = probe_video_meta_with_audio(video_path)
    duration = _safe_duration(duration)
    if duration <= 0.0:
        return False, None, None

    used_times = _normalize_exclude_times(exclude_times)
    used_hashes = _normalize_exclude_hashes(exclude_hashes)
    window = _cover_slot_window(duration, slot_index, slot_count)
    min_gap = _cover_min_gap(duration, len(used_times), window)
    times = _cover_candidate_times(duration, window=window)
    tmp_dir = tempfile.mkdtemp(prefix="yym_cover_")
    scored: list[tuple[float, float, int]] = []
    fail_streak = 0
    chosen_t: float | None = None
    chosen_hash: int | None = None
    try:
        for index, t in enumerate(times):
            preview = os.path.join(tmp_dir, f"c{index}.jpg")
            if not _ffmpeg_extract_frame(
                ffmpeg,
                video_path,
                preview,
                t,
                _COVER_PREVIEW_WIDTH,
                _COVER_JPEG_QUALITY_PREVIEW,
                _COVER_FFMPEG_TIMEOUT_SEC,
            ):
                fail_streak += 1
                if fail_streak >= _COVER_CANDIDATE_FAIL_ABORT:
                    break
                continue
            fail_streak = 0
            preview_hash = _dhash_file(preview)
            if preview_hash is None:
                continue
            score = _score_cover_preview_file(preview)
            if score == float("-inf"):
                continue
            scored.append((float(score), float(t), int(preview_hash)))

        picked = _pick_diverse_cover(
            scored,
            used_times,
            used_hashes,
            min_gap,
            _COVER_TOP_K,
        )
        if picked is not None:
            _, chosen_t, chosen_hash = picked
        else:
            chosen_t = _fallback_cover_time_away(
                duration,
                used_times,
                min_gap,
                window,
            )

        hd_candidates = sorted(
            scored,
            key=lambda item: item[0],
            reverse=True,
        )[:3]
        if not hd_candidates:
            hd_candidates = [(0.0, float(chosen_t or 0.0), 0)]
        ok = False
        for item in hd_candidates:
            t = float(item[1])
            if _ffmpeg_extract_frame(
                ffmpeg,
                video_path,
                thumb_path,
                t,
                None,
                _COVER_JPEG_QUALITY_HD,
                _COVER_FFMPEG_HD_TIMEOUT_SEC,
            ):
                if _is_readable_image(thumb_path):
                    chosen_t = t
                    chosen_hash = int(item[2]) or chosen_hash
                    ok = True
                    break
        if not ok:
            t = float(chosen_t or _fallback_cover_time(duration))
            ok = _ffmpeg_extract_frame(
                ffmpeg,
                video_path,
                thumb_path,
                t,
                None,
                _COVER_JPEG_QUALITY_HD,
                _COVER_FFMPEG_HD_TIMEOUT_SEC,
            ) and _is_readable_image(thumb_path)
            if ok:
                chosen_t = t
        return bool(ok), chosen_t, chosen_hash
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _extract_cover_moviepy_fallback(
    video_path: str,
    thumb_path: str,
    t: float,
) -> bool:
    video = None
    try:
        video = VideoFileClip(str(video_path), audio=False)
        duration = float(video.duration or 0.0)
        frame_t = max(
            0.0,
            min(_safe_duration(t), max(0.0, duration - 0.001)),
        )
        video.save_frame(str(thumb_path), t=frame_t)
    except Exception:
        _safe_unlink(thumb_path)
        return False
    finally:
        if video is not None:
            try:
                video.close()
            except Exception:
                _ = None
    return _is_readable_image(thumb_path)


def extract_first_cover_image(
    video_path: str,
    thumb_path: str | None = None,
) -> str | None:
    video_path_str = os.fspath(video_path)
    thumb_path_str = (
        os.fspath(thumb_path)
        if thumb_path
        else gene_thumb_path(video_path_str)
    )
    ffmpeg = resolve_ffmpeg_bin()
    try:
        if ffmpeg and _ffmpeg_extract_frame(
            ffmpeg,
            video_path_str,
            thumb_path_str,
            0.0,
            None,
            _COVER_JPEG_QUALITY_HD,
            _COVER_FFMPEG_HD_TIMEOUT_SEC,
        ) and _is_readable_image(thumb_path_str):
            print("成功获取视频第一帧高清截图")
            return thumb_path_str
    except Exception:
        _ = None
    print("视频第一帧 ffmpeg 截图失败，使用 moviepy 第一帧高清截图")
    try:
        if _extract_cover_moviepy_fallback(
            video_path_str,
            thumb_path_str,
            0.0,
        ) and _is_readable_image(thumb_path_str):
            return thumb_path_str
    except Exception:
        return None
    return None


def extract_random_cover_image(
    video_path: str,
    output_file: str | None = None,
    exclude_times: list[float] | None = None,
    exclude_hashes: list[int] | None = None,
    slot_index: int = 0,
    slot_count: int = 1,
) -> str | None:
    video_path_str = os.fspath(video_path)
    thumb_path_str = (
        os.fspath(output_file)
        if output_file
        else gene_thumb_path(video_path_str)
    )
    ok, _, _ = _extract_highlight_cover(
        video_path_str,
        thumb_path_str,
        exclude_times,
        exclude_hashes,
        slot_index,
        slot_count,
    )
    if ok and _is_readable_image(thumb_path_str):
        print("成功获取随机视频高清截图")
        return thumb_path_str
    print("随机视频高清截图获取失败，使用第一帧高清截图")
    return extract_first_cover_image(video_path_str, thumb_path_str)


def gene_thumb_path(video_path: str) -> str:
    try:
        path = Path(video_path)
        parts = path.parts
        directory = "/".join(parts[:-1])
        filename = path.stem
        old_name = path.name
        old_extension = path.suffix
        new_extension = ".jpg"
        new_name = f"{filename}{old_extension}{new_extension}"
        if not directory:
            directory = "."
        thumb_path = Path(directory).joinpath(new_name)
        _ = old_name
        return str(thumb_path)
    except Exception:
        return f"{os.fspath(video_path)}.jpg"


def check_watermark_image(img_path: str) -> None:
    try:
        with Image.open(img_path) as img:
            w, h = img.size
            ratio = float(w) / float(h) if h else 0.0
            print("尺寸: ", f"{w}×{h}")
            print("宽高比: ", f"{ratio:.2f}:1")
            print("格式: ", img.format)
            print("通道: ", img.mode)
            if w < 800:
                print("⚠️  宽度过小，建议 ≥1200px")
            if img.mode != "RGBA":
                print("⚠️  建议使用 PNG 带透明通道（RGBA）")
            if ratio < 0.2 or ratio > (1.0 / 0.2):
                print("⚠️  宽高比过于极端")
            print("✅ 规格合格")
    except Exception as exc:
        print("水印图片检查失败: ", exc)
