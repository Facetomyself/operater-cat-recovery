# Recovered module: src.py.com.yun.mao.auto.GenSegmentVideoOnePass
# Reconstruction from Nuitka constants, runtime signatures, and offline
# Hex-Rays.  The ffmpeg command layout and the progress pipe are taken from
# the app string table; a few threshold/fallback details are marked inferred.
from __future__ import annotations

import os
import random
import subprocess
import tempfile
import time
from contextlib import suppress
from dataclasses import dataclass
from typing import Any, Callable

from src.py.com.yun.mao.cd import TaskHardStop, Working
from src.py.com.yun.mao.config import YunYinMaoConfig
from src.py.com.yun.mao.telefast import CallBack
from src.py.com.yun.mao.util import AccelUtils
from src.py.com.yun.mao.util.need import utils

_STOPPED_BY_USER = "用户停止任务"
_CPU_ENCODE_ARGS = [
    "-c:v",
    "libx264",
    "-preset",
    "fast",
    "-crf",
    "23",
    "-pix_fmt",
    "yuv420p",
]


class PreviewReason:
    """Reason codes used by :class:`PreviewResult`."""

    SUCCESS = "生成预览视频成功"
    SKIP_SHORTER_THAN_SEGMENT = "视频太短了，无需生成预览视频"
    SKIP_EXCEEDS_SOURCE_DURATION = "预览视频时长超过原视频时长，无需生成预览视频"
    FAIL_RUNTIME = "运行时失败"
    FAIL_DURATION_UNAVAILABLE = "无法获取视频时长"
    STOPPED_BY_USER = "用户停止任务"


@dataclass
class PreviewResult:
    ok: bool
    reason: str | None = None
    output_file: str | None = None
    detail: str | None = None


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


def _resolve_ffmpeg() -> tuple[str, str]:
    result = _call_optional(AccelUtils, "resolve_ffmpeg_bin")
    if isinstance(result, tuple):
        if not result:
            return "", ""
        if len(result) >= 2:
            return str(result[0] or ""), str(result[1] or "")
        return str(result[0] or ""), ""
    return str(result or ""), ""


def _filter_complex_script_dir() -> str | None:
    """Return the cache directory used for temp filter_complex scripts."""

    cache_dir = ""
    value = getattr(YunYinMaoConfig, "abs_cache_only_multi_dir", "")
    try:
        if callable(value):
            value = value()
        cache_dir = str(value or "")
    except Exception:
        cache_dir = ""
    if not cache_dir:
        return None
    path = os.path.join(cache_dir, "_filter_complex_script_dir")
    utils.init_folder(path)
    return path


def _build_filter_script_file(
    segment_pairs: list[tuple[float, float]],
) -> str:
    lines: list[str] = []
    va_inputs: list[str] = []
    for i, (start_t, end_t) in enumerate(segment_pairs):
        lines.append(
            f"[0:v]trim=start={start_t}:end={end_t},"
            f"setpts=PTS-STARTPTS[v{i}]"
        )
        lines.append(
            f"[0:a]atrim=start={start_t}:end={end_t},"
            f"asetpts=PTS-STARTPTS[a{i}]"
        )
        va_inputs.append(f"[v{i}][a{i}]")
    lines.append(
        "".join(va_inputs)
        + f"concat=n={len(segment_pairs)}:v=1:a=1[vout][aout]"
    )
    content = ";\n".join(lines) + ";\n"
    fd, path = tempfile.mkstemp(
        prefix="preview_fc_",
        suffix=".txt",
        dir=_filter_complex_script_dir(),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        with suppress(OSError):
            os.close(fd)
        raise
    return path


def _build_filter_script_file_video_only(
    segment_pairs: list[tuple[float, float]],
) -> str:
    lines: list[str] = []
    v_inputs: list[str] = []
    for i, (start_t, end_t) in enumerate(segment_pairs):
        lines.append(
            f"[0:v]trim=start={start_t}:end={end_t},"
            f"setpts=PTS-STARTPTS[v{i}]"
        )
        v_inputs.append(f"[v{i}]")
    lines.append(
        "".join(v_inputs)
        + f"concat=n={len(segment_pairs)}:v=1:a=0[vout]"
    )
    content = ";\n".join(lines) + ";\n"
    fd, path = tempfile.mkstemp(
        prefix="preview_fc_",
        suffix=".txt",
        dir=_filter_complex_script_dir(),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        with suppress(OSError):
            os.close(fd)
        raise
    return path


def _build_one_pass_cmd(
    ffmpeg: str,
    input_file: str,
    fc_path: str,
    has_audio: bool,
    encode_args: list[str],
    output_file: str,
) -> list[str]:
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        input_file,
        "-filter_complex_script",
        fc_path,
        "-map",
        "[vout]",
        "-progress",
        "pipe:2",
        "-nostats",
    ]
    if has_audio:
        cmd.extend(["-map", "[aout]", "-c:a", "aac"])
    else:
        cmd.append("-an")
    cmd.extend(str(item) for item in encode_args)
    cmd.extend(["-movflags", "+faststart", output_file])
    return cmd


def _cpu_encode_args() -> list[str]:
    return list(_CPU_ENCODE_ARGS)


def _gpu_attempt_encode_args(
    encoder: str, vendor_params: list[str]
) -> list[str]:
    args = ["-c:v", str(encoder or "")]
    args.extend(str(item) for item in (vendor_params or []))
    args.extend(["-pix_fmt", "yuv420p"])
    return args


def _run_with_progress(
    command: list[str],
    preview_total_seconds: float,
    process_cb: Callable[..., Any] | None = None,
) -> tuple[bool, str]:
    _call_optional(CallBack, "reset_preview_progress")
    print("正在生成预览视频，处理中...")
    kwargs = _call_optional(AccelUtils, "subprocess_no_console_kwargs")
    if not isinstance(kwargs, dict):
        kwargs = {}
    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        **kwargs,
    )
    _call_optional(TaskHardStop, "register", process)
    err_tail_lines: list[str] = []
    stopped_by_user = False
    last_heartbeat_ts = time.time()
    last_pct = -1.0
    started_ts = last_heartbeat_ts
    try:
        stderr = process.stderr
        if stderr is not None:
            for raw_line in stderr:
                line = (
                    raw_line.decode("utf-8", "ignore")
                    if isinstance(raw_line, bytes)
                    else str(raw_line)
                )
                line = line.strip()
                if not line:
                    continue
                err_tail_lines.append(line)
                del err_tail_lines[:-80]
                if getattr(Working, "need_stop", False):
                    stopped_by_user = True
                    if process.poll() is None:
                        process.kill()
                    print("手动停止成功！")
                    break
                if not line.startswith("out_time_ms="):
                    continue
                try:
                    out_time_us = float(line.split("=", 1)[1])
                except (TypeError, ValueError):
                    continue
                sec = out_time_us / 1000000.0
                ratio = (
                    sec / preview_total_seconds
                    if preview_total_seconds > 0
                    else 0.0
                )
                pct = min(0.999, max(0.0, ratio)) * 100.0
                now_ts = time.time()
                if pct - last_pct >= 1.0 or now_ts - last_heartbeat_ts >= 2.0:
                    last_pct = pct
                    last_heartbeat_ts = now_ts
                    execution_time = max(0.0, now_ts - started_ts)
                    if callable(process_cb):
                        process_cb(
                            sec,
                            preview_total_seconds,
                            now_ts,
                            execution_time,
                            pct,
                        )
                    else:
                        _call_optional(
                            CallBack,
                            "preview_progress_bar",
                            sec,
                            preview_total_seconds,
                            now_ts,
                            execution_time,
                            pct,
                        )
        returncode = process.wait()
        execution_time = max(0.0, time.time() - started_ts)
        _call_optional(
            CallBack,
            "preview_progress_bar_done",
            preview_total_seconds,
            execution_time,
        )
        if stopped_by_user:
            return False, _STOPPED_BY_USER
        ok = returncode == 0
        if ok:
            _call_optional(
                CallBack,
                "preview_progress_bar",
                preview_total_seconds,
                preview_total_seconds,
                execution_time=execution_time,
                pct_raw=100.0,
            )
        return ok, "\n".join(err_tail_lines[-55:])
    except Exception as exc:
        if process.poll() is None:
            process.kill()
        detail = "\n".join(err_tail_lines[-55:])
        return False, f"{exc}\n{detail}".strip()
    finally:
        _call_optional(TaskHardStop, "unregister", process)


def _segment_duration_for_index(
    index: int,
    total_segments: int,
    segment_duration: float,
    last_second: float,
) -> float:
    """Clamp the tail segment; other segments keep the configured length."""

    duration = max(0.0, _as_float(segment_duration, 0.0))
    last_second = max(0.0, _as_float(last_second, 0.0))
    if total_segments <= 0:
        return 0.0
    if index >= total_segments - 1:
        return min(duration, last_second) if duration > 0 else last_second
    return duration


def _select_segment_starts(
    total_duration: float,
    segment_duration: float,
) -> list[float]:
    """Pick non-overlapping segment starts across the whole source.

    The caller only consumes as many starts as needed for ``preview_duration``.
    The exact jitter policy is inferred from the recovered local names
    (``remaining_space`` / ``random_factor`` / ``safe_max_start``).
    """

    total_duration = max(0.0, _as_float(total_duration, 0.0))
    segment_duration = max(0.01, _as_float(segment_duration, 0.0))
    if total_duration <= 0 or segment_duration <= 0:
        return []
    num_segments = max(2, int(total_duration / segment_duration))
    segments: list[float] = []
    last_end_time = 0.0
    for _i in range(num_segments):
        max_start_time = max(0.0, total_duration - segment_duration)
        remaining_space = max_start_time - last_end_time
        if remaining_space <= 0:
            break
        slot_space = remaining_space / max(1, num_segments - _i)
        random_factor = random.randint(1, 99) / 100.0
        safe_max_start = last_end_time + slot_space * random_factor
        start_time = min(max_start_time, max(last_end_time, safe_max_start))
        segments.append(round(start_time, 3))
        last_end_time = start_time + segment_duration
    segments.sort()
    return segments


def get_video_duration(input_file: str) -> float:
    """Return the source duration in seconds, or ``0.0`` when unknown."""

    try:
        meta = _call_optional(
            AccelUtils, "probe_video_meta_wrapper", input_file
        )
    except Exception:
        return 0.0
    candidates: list[Any] = []
    if isinstance(meta, dict):
        candidates.extend(
            [
                meta.get("duration"),
                meta.get("total_duration"),
                meta.get("seconds"),
            ]
        )
        fmt = meta.get("format")
        if isinstance(fmt, dict):
            candidates.append(fmt.get("duration"))
    elif isinstance(meta, (tuple, list)):
        candidates.extend(meta)
    for candidate in candidates:
        duration = _as_float(candidate, 0.0)
        if duration > 0:
            return duration
    return 0.0


def _probe_has_audio(input_file: str) -> bool:
    """Best-effort audio detection; defaults to True when metadata is absent."""

    try:
        meta = _call_optional(
            AccelUtils, "probe_video_meta_wrapper", input_file
        )
    except Exception:
        return True
    if not isinstance(meta, dict):
        return True
    for key in ("has_audio", "hasAudio", "audio"):
        value = meta.get(key)
        if isinstance(value, bool):
            return value
    streams = meta.get("streams")
    if isinstance(streams, (list, tuple)):
        return any(
            str((item or {}).get("codec_type", "")).lower() == "audio"
            for item in streams
            if isinstance(item, dict)
        )
    return True


def _attempt_fields(attempt: Any) -> tuple[str, str, str, list[str]]:
    if isinstance(attempt, dict):
        name = str(
            attempt.get("name")
            or attempt.get("attempt_name")
            or attempt.get("encoder")
            or ""
        )
        encoder = str(attempt.get("encoder") or name)
        vendor = str(attempt.get("vendor") or "")
        params = attempt.get("vendor_params") or attempt.get("params") or []
        return name, encoder, vendor, [str(item) for item in params]
    if isinstance(attempt, (tuple, list)):
        values = list(attempt)
        while len(values) < 4:
            values.append("")
        vendor_params = values[3] if isinstance(values[3], (list, tuple)) else []
        return (
            str(values[0] or ""),
            str(values[1] or values[0] or ""),
            str(values[2] or ""),
            [str(item) for item in vendor_params],
        )
    name = str(attempt or "")
    return name, name, "", []


def _profile_fields(profile: Any) -> tuple[str, str]:
    if isinstance(profile, dict):
        encoder = str(profile.get("encoder") or profile.get("name") or "")
        vendor = str(profile.get("vendor") or "")
        return encoder, vendor
    if isinstance(profile, (tuple, list)) and profile:
        encoder = str(profile[0] or "")
        vendor = str(profile[1] or "") if len(profile) > 1 else ""
        return encoder, vendor
    return str(profile or ""), ""


def _normalize_profiles(profiles: Any) -> list[Any]:
    if isinstance(profiles, dict):
        return [profiles]
    if isinstance(profiles, (list, tuple)):
        return list(profiles)
    return []


def generate_preview(
    input_file: str,
    output_file: str,
    total_duration: float,
    segment_duration: float,
    preview_duration: float,
    process_cb: Callable[..., Any] | None = None,
    accel_mode: str | None = None,
) -> PreviewResult:
    """Build a one-pass concatenated preview with ffmpeg.

    The command uses ``-filter_complex_script`` plus ``-progress pipe:2``; GPU
    attempts come from ``AccelUtils.build_gpu_encode_attempts`` and fall back
    to libx264.  This function never executes ffmpeg at import time.
    """

    total_duration = max(0.0, _as_float(total_duration, 0.0))
    segment_duration = max(0.01, _as_float(segment_duration, 0.0))
    preview_duration = max(0.0, _as_float(preview_duration, 0.0))
    if total_duration <= 0:
        return PreviewResult(
            False,
            PreviewReason.FAIL_DURATION_UNAVAILABLE,
            output_file,
            "无法获取视频时长",
        )
    if total_duration <= segment_duration:
        return PreviewResult(
            False,
            PreviewReason.SKIP_SHORTER_THAN_SEGMENT,
            output_file,
            PreviewReason.SKIP_SHORTER_THAN_SEGMENT,
        )
    if preview_duration >= total_duration:
        return PreviewResult(
            False,
            PreviewReason.SKIP_EXCEEDS_SOURCE_DURATION,
            output_file,
            PreviewReason.SKIP_EXCEEDS_SOURCE_DURATION,
        )

    ffmpeg, ff_msg = _resolve_ffmpeg()
    if not ffmpeg:
        return PreviewResult(
            False,
            PreviewReason.FAIL_RUNTIME,
            output_file,
            ff_msg or "ffmpeg path empty",
        )
    ff_ok = _call_optional(AccelUtils, "is_ffmpeg_available", ffmpeg)
    if ff_ok is False:
        return PreviewResult(
            False,
            PreviewReason.FAIL_RUNTIME,
            output_file,
            ff_msg or "ffmpeg unavailable",
        )

    mode = _call_optional(AccelUtils, "normalize_accel_mode", accel_mode)
    mode = str(mode or accel_mode or getattr(AccelUtils, "ACCEL_MODE_AUTO", "auto"))
    cpu_mode = str(getattr(AccelUtils, "ACCEL_MODE_CPU", "cpu"))
    gpu_mode = str(getattr(AccelUtils, "ACCEL_MODE_GPU", "gpu"))
    auto_mode = str(getattr(AccelUtils, "ACCEL_MODE_AUTO", "auto"))

    gpu_profiles = _normalize_profiles(
        _call_optional(AccelUtils, "detect_gpu_profiles")
    )
    gpu_available = bool(gpu_profiles)
    selected_gpu = gpu_profiles[0] if gpu_profiles else None
    use_gpu = False
    if mode == cpu_mode:
        print("当前为强制CPU模式，跳过GPU编码器探测结果")
    elif mode == gpu_mode:
        if gpu_available:
            use_gpu = True
            encoder, vendor = _profile_fields(selected_gpu)
            print(f"当前为强制GPU模式，使用：{encoder} ({vendor})")
        else:
            print("当前为强制GPU模式，但未检测到可用GPU编码器，将自动回退CPU")
    else:
        if gpu_available:
            use_gpu = True
            encoder, vendor = _profile_fields(selected_gpu)
            print(
                "检测到GPU编码器，优先使用GPU预览加速：编码器="
                f"{encoder} (厂商={vendor})"
            )
        else:
            print("未检测到GPU编码器，将使用CPU生成预览视频")

    starts = _select_segment_starts(total_duration, segment_duration)
    if not starts:
        return PreviewResult(
            False,
            PreviewReason.FAIL_RUNTIME,
            output_file,
            "no valid segments",
        )

    seg_pairs: list[tuple[float, float]] = []
    preview_total = 0.0
    total_segments = len(starts)
    for i, start_time in enumerate(starts):
        remaining_preview = preview_duration - preview_total
        if remaining_preview <= 0:
            break
        duration = _segment_duration_for_index(
            i, total_segments, segment_duration, total_duration
        )
        duration = min(duration, remaining_preview, total_duration - start_time)
        if duration <= 0:
            continue
        end_time = min(total_duration, start_time + duration)
        seg_pairs.append((round(start_time, 3), round(end_time, 3)))
        preview_total += end_time - start_time
    if not seg_pairs:
        return PreviewResult(
            False,
            PreviewReason.FAIL_RUNTIME,
            output_file,
            "no valid segments",
        )

    source_has_audio = _probe_has_audio(input_file)
    has_audio = source_has_audio
    fc_path = (
        _build_filter_script_file(seg_pairs)
        if has_audio
        else _build_filter_script_file_video_only(seg_pairs)
    )
    start_ts = time.time()
    final_encode_desc = ""
    ok = False
    err = ""
    gpu_failed_in_auto = False
    try:
        if use_gpu:
            gpu_attempts = _normalize_profiles(
                _call_optional(
                    AccelUtils,
                    "build_gpu_encode_attempts",
                    gpu_profiles,
                )
            )
            if gpu_attempts:
                print(
                    f"将依次尝试 {len(gpu_attempts)} 种 GPU 编码策略，"
                    "再决定是否回退 CPU"
                )
                for attempt in gpu_attempts:
                    if getattr(Working, "need_stop", False):
                        return PreviewResult(
                            False,
                            PreviewReason.STOPPED_BY_USER,
                            output_file,
                            _STOPPED_BY_USER,
                        )
                    attempt_name, encoder, vendor, vendor_params = _attempt_fields(
                        attempt
                    )
                    encode_args = _gpu_attempt_encode_args(
                        encoder, vendor_params
                    )
                    cmd = _build_one_pass_cmd(
                        ffmpeg,
                        input_file,
                        fc_path,
                        has_audio,
                        encode_args,
                        output_file,
                    )
                    print(f"本次编码：GPU（{attempt_name or encoder}，{vendor}）")
                    ok, err = _run_with_progress(
                        cmd, preview_total, process_cb
                    )
                    if ok:
                        final_encode_desc = (
                            f"GPU（{attempt_name or encoder}，{vendor}）"
                        )
                        _call_optional(
                            AccelUtils,
                            "note_preview_session_gpu_encode_success",
                        )
                        break
                    print(
                        "ffmpeg encode failed: "
                        f"{(err or 'no stderr')[-2000:]}"
                    )
            if not ok:
                gpu_failed_in_auto = mode == auto_mode
                use_gpu = False

        if not use_gpu:
            print("本次编码：CPU（libx264）")
            encode_args = _cpu_encode_args()
            cmd = _build_one_pass_cmd(
                ffmpeg,
                input_file,
                fc_path,
                has_audio,
                encode_args,
                output_file,
            )
            ok, err = _run_with_progress(cmd, preview_total, process_cb)
            final_encode_desc = "CPU（libx264）"
            if not ok:
                if getattr(Working, "need_stop", False):
                    return PreviewResult(
                        False,
                        PreviewReason.STOPPED_BY_USER,
                        output_file,
                        _STOPPED_BY_USER,
                    )
                return PreviewResult(
                    False,
                    PreviewReason.FAIL_RUNTIME,
                    output_file,
                    (err or "no stderr")[-2000:],
                )

        if gpu_failed_in_auto:
            _call_optional(
                AccelUtils,
                "note_preview_session_auto_gpu_fallback_after_hw_failed",
            )
        elapsed = max(0.0, time.time() - start_ts)
        audio_desc = "（含音频）" if has_audio else "（无音频，源无音轨）"
        print(
            f"预览生成完成，视频编码：{final_encode_desc}，"
            f"耗时 {utils.format_time(int(elapsed))}{audio_desc}"
        )
        return PreviewResult(
            True,
            PreviewReason.SUCCESS,
            output_file,
            None,
        )
    finally:
        if fc_path:
            with suppress(Exception):
                utils.safe_del_file(fc_path)
        if not ok and getattr(Working, "need_stop", False):
            with suppress(Exception):
                utils.safe_del_file(output_file)


def auto_adapter_seg(input_file: str) -> float:
    """Choose a segment length from the source duration.

    The exact thresholds are inferred; the recovered constants show ``10`` as
    the fallback/default segment length and the caller prints the chosen
    per-segment duration.
    """

    duration = get_video_duration(input_file)
    try:
        if duration <= 0:
            return 10.0
        if duration <= 10:
            return max(1.0, duration / 2.0)
        if duration <= 60:
            return 3.0
        if duration <= 300:
            return 5.0
        return 10.0
    except Exception as e:
        print(f"无法获取视频时长：{e}")
        return 10.0
