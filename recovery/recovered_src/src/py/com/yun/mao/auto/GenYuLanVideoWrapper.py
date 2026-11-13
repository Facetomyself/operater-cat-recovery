# Recovered module: src.py.com.yun.mao.auto.GenYuLanVideoWrapper
# Reconstruction from Nuitka constants, runtime signatures, and offline
# Hex-Rays.  The public entry points and argument order are confirmed; a few
# adapter thresholds and metadata fallbacks are explicitly marked inferred.
from __future__ import annotations

import random
from typing import Any, Callable

from src.py.com.yun.mao.auto import GenSegmentVideoOnePass
from src.py.com.yun.mao.auto.GenSegmentVideoOnePass import (
    PreviewReason,
    PreviewResult,
)
from src.py.com.yun.mao.config import NewConfig
from src.py.com.yun.mao.util import AccelUtils
from src.py.com.yun.mao.util.need import utils


def _call_optional(obj: Any, name: str, *args, **kwargs):
    func = getattr(obj, name, None)
    if not callable(func):
        return None
    return func(*args, **kwargs)


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _effective_accel_mode(accel_mode: str | None) -> str | None:
    """Resolve the preview acceleration mode.

    ``AccelUtils.effective_accel_mode_preview`` is recovered only as a call
    site, so tuple/dict/plain-string returns are accepted (inferred).
    """

    func = getattr(AccelUtils, "effective_accel_mode_preview", None)
    if not callable(func):
        return accel_mode or getattr(AccelUtils, "ACCEL_MODE_AUTO", "auto")
    try:
        result = func(accel_mode)
    except TypeError:
        try:
            result = func(accel_mode=accel_mode)
        except TypeError:
            return accel_mode or getattr(AccelUtils, "ACCEL_MODE_AUTO", "auto")
    if isinstance(result, tuple):
        return result[0] if result else accel_mode
    if isinstance(result, dict):
        return (
            result.get("accel_mode")
            or result.get("mode")
            or accel_mode
        )
    return result or accel_mode


def auto_adapter(present: str) -> float:
    """Normalize a present mode/percentage into a preview-duration ratio."""

    text = str(present or "").strip()
    if text == NewConfig.FLOW_DURATION_SHORT:
        number_present = 0.1
    elif text == NewConfig.FLOW_DURATION_MIDDLE:
        number_present = 0.2
    elif text == NewConfig.FLOW_DURATION_LONG:
        number_present = 0.3
    else:
        number_present = (
            utils.safe_parse_to_int(text, 30) * 0.01
        )
    return max(0.01, min(1.0, number_present))


def generate_present_preview(
    input_file: str,
    output_file: str,
    present: str,
    process_cb: Callable[..., Any] | None = None,
    accel_mode: str | None = None,
    total_duration: float | None = None,
    preview_duration_ratio: float | None = None,
    segment_duration: float | None = None,
    preview_duration: float | None = None,
) -> PreviewResult:
    """Generate a percentage-based preview."""

    if total_duration is None:
        total_duration = GenSegmentVideoOnePass.get_video_duration(input_file)
    total_duration = max(0.0, _as_float(total_duration, 0.0))
    if total_duration <= 0:
        print("无法获取视频时长")
        return PreviewResult(
            False,
            PreviewReason.FAIL_DURATION_UNAVAILABLE,
            output_file,
        )
    if preview_duration_ratio is None:
        preview_duration_ratio = auto_adapter(present)
    preview_duration_ratio = max(
        0.01, min(1.0, _as_float(preview_duration_ratio, 0.1))
    )
    if segment_duration is None:
        segment_duration = GenSegmentVideoOnePass.auto_adapter_seg(input_file)
    segment_duration = max(0.01, _as_float(segment_duration, 3.0))
    if preview_duration is None:
        preview_duration = total_duration * preview_duration_ratio
    preview_duration = max(0.0, _as_float(preview_duration, 0.0))
    print(
        f"智能参数：比率：{preview_duration_ratio}"
        f"，单个片长：{segment_duration} 秒"
    )
    print(
        f"原视频时长: {utils.format_time(int(total_duration))}"
        f"，预览视频期望时长: {utils.format_time(int(preview_duration))}"
    )
    if preview_duration >= total_duration:
        return PreviewResult(
            False,
            PreviewReason.SKIP_EXCEEDS_SOURCE_DURATION,
            output_file,
        )
    accel_mode = _effective_accel_mode(accel_mode)
    return GenSegmentVideoOnePass.generate_preview(
        input_file,
        output_file,
        total_duration,
        segment_duration,
        preview_duration,
        process_cb,
        accel_mode,
    )


def generate_customer_preview(
    input_file: str,
    output_file: str,
    duration_min_second: int,
    duration_max_second: int,
    process_cb: Callable[..., Any] | None = None,
    accel_mode: str | None = None,
    total_duration: float | None = None,
    segment_duration: float | None = None,
    preview_duration: float | None = None,
) -> PreviewResult:
    """Generate a preview whose length is randomly chosen in the given range."""

    if total_duration is None:
        total_duration = GenSegmentVideoOnePass.get_video_duration(input_file)
    total_duration = max(0.0, _as_float(total_duration, 0.0))
    if total_duration <= 0:
        print("无法获取视频时长")
        return PreviewResult(
            False,
            PreviewReason.FAIL_DURATION_UNAVAILABLE,
            output_file,
        )
    min_second = max(1, utils.safe_parse_to_int(duration_min_second, 5))
    max_second = max(
        min_second, utils.safe_parse_to_int(duration_max_second, min_second)
    )
    if preview_duration is None:
        preview_duration = float(random.randint(min_second, max_second))
    preview_duration = max(0.0, _as_float(preview_duration, 0.0))
    if segment_duration is None:
        segment_duration = GenSegmentVideoOnePass.auto_adapter_seg(input_file)
    segment_duration = max(0.01, _as_float(segment_duration, 3.0))
    print(f"单个片长：{segment_duration} 秒")
    if preview_duration >= total_duration:
        return PreviewResult(
            False,
            PreviewReason.SKIP_EXCEEDS_SOURCE_DURATION,
            output_file,
        )
    accel_mode = _effective_accel_mode(accel_mode)
    return GenSegmentVideoOnePass.generate_preview(
        input_file,
        output_file,
        total_duration,
        segment_duration,
        preview_duration,
        process_cb,
        accel_mode,
    )
