# Recovered module: src.py.com.yun.mao.water.VideoWaterUtilsToSmallFile
# Reconstruction from Nuitka constants and offline Hex-Rays.
# ffmpeg/moviepy pipelines below are behavior-level reconstructions and are
# marked inferred where the exact original expression cannot be proven.
from __future__ import annotations

import os
import random
import re
import subprocess
import time

from src.py.com.yun.mao.cd import Working, TaskHardStop
from src.py.com.yun.mao.telefast import CallBack
from src.py.com.yun.mao.util import AccelUtils, ResourcePath
from src.py.com.yun.mao.util.need import utils
from src.py.com.yun.mao.water import VideoBitUtils
from src.py.com.yun.mao.water.WaterConstants import DEFAULT_IMG_SCALE_RATIO

MOTION_RANDOM = "random"
MOTION_LISSAJOUS = "lissajous"
MOTION_BOUNCE = "bounce"
MOTION_CIRCLE = "circle"
MOTION_RANDOM_WALK = "random_walk"
MOTION_SPIRAL = "spiral"
_MOTION_STRATEGIES = [
    MOTION_LISSAJOUS,
    MOTION_BOUNCE,
    MOTION_CIRCLE,
    MOTION_RANDOM_WALK,
    MOTION_SPIRAL,
]
DEFAULT_CENTER_SAFE_RATIO = 0.5
_MSG_NO_GPU_ENCODER_FFMPEG = "no gpu encoder found in ffmpeg"
_STOPPED_BY_USER = "stopped by user"


def _call_optional(obj, name: str, *args, **kwargs):
    func = getattr(obj, name, None)
    if func is None:
        return None
    return func(*args, **kwargs)


def _resolve_ffmpeg() -> tuple[str, str]:
    result = AccelUtils.resolve_ffmpeg_bin()
    if isinstance(result, tuple):
        if len(result) >= 2:
            return result[0], result[1]
        return result[0], ""
    return result, ""


def _probe_meta(video_path: str) -> dict:
    result = AccelUtils.probe_video_meta_wrapper(video_path)
    if isinstance(result, dict):
        return result
    if isinstance(result, tuple):
        for item in result:
            if isinstance(item, dict):
                return item
    return {}


def _attempt_fields(attempt) -> tuple[str, str, str, object]:
    if isinstance(attempt, dict):
        name = str(attempt.get("name") or attempt.get("attempt_name") or "")
        encoder = str(attempt.get("encoder") or name)
        vendor = str(attempt.get("vendor") or "")
        params = attempt.get("params") or attempt.get("vendor_params") or []
        return name, encoder, vendor, params
    return str(attempt), str(attempt), "", []


def _failure(
    msg: str,
    duration: float = 0.0,
    width: int = 0,
    height: int = 0,
    fps: float = 0.0,
    bitrate: object = 0,
    filter_text: str = "",
    profiles=None,
    fail_reasons=None,
    cmd=None,
    run_code: int = -1,
    stderr_tail: str = "",
):
    return (
        False,
        msg,
        "",
        duration,
        width,
        height,
        fps,
        bitrate,
        filter_text,
        profiles or [],
        fail_reasons or [],
        "",
        "",
        [],
        "",
        cmd or [],
        run_code,
        stderr_tail,
    )


def _success(
    msg: str,
    encoder: str,
    vendor: str,
    vendor_params,
    attempt_name: str,
    duration: float,
    width: int,
    height: int,
    fps: float,
    bitrate: object,
    filter_text: str,
    profiles,
    fail_reasons,
    cmd,
    run_code: int,
    stderr_tail: str,
):
    return (
        True,
        msg,
        encoder,
        duration,
        width,
        height,
        fps,
        bitrate,
        filter_text,
        profiles,
        fail_reasons,
        vendor,
        encoder,
        vendor_params,
        attempt_name,
        cmd,
        run_code,
        stderr_tail,
    )


def _abort_if_stopped(output_path: str | None = None) -> None:
    if getattr(Working, "need_stop", False):
        print("手动停止成功！")
        if output_path and os.path.exists(output_path):
            utils.safe_del_file(output_path)
        raise TaskHardStop(_STOPPED_BY_USER)


def _safe_float(value, default_value: float = 0.0, min_value: float = 0.0) -> float:
    try:
        f = float(value)
    except (TypeError, ValueError):
        f = default_value
    return max(f, min_value)


def _safe_int(value, default_value: int = 0, min_value: int = 0) -> int:
    try:
        i = int(value)
    except (TypeError, ValueError):
        i = default_value
    return max(i, min_value)


def _escape_drawtext_text(text: str) -> str:
    text = "" if text is None else str(text)
    text = text.replace("\\", "\\\\")
    text = text.replace(":", "\\:")
    text = text.replace("'", "\\'")
    text = text.replace(",", "\\,")
    return text


def _normalize_font_for_ffmpeg(font_path: str) -> str:
    p = str(font_path or "").replace("\\", "/")
    if len(p) >= 2 and p[1] == ":":
        p = p[0] + "\\:" + p[2:]
    return p


def _normalize_image_path_for_ffmpeg(img_path: str) -> str:
    return _normalize_font_for_ffmpeg(img_path)


def _build_motion_xy(
    motion: str, fps: float, center_safe_ratio: float = DEFAULT_CENTER_SAFE_RATIO
) -> tuple[str, str]:
    fps = max(_safe_float(fps, 25.0, 1.0), 1.0)
    csr = max(0.1, min(0.9, _safe_float(center_safe_ratio, DEFAULT_CENTER_SAFE_RATIO)))
    edge_width = 1.0 - 2.0 * csr

    def clamp_x(expr: str) -> str:
        return f"min(max(({expr})\\,0)\\,w-text_w)"

    def clamp_y(expr: str) -> str:
        return f"min(max(({expr})\\,0)\\,h-text_h)"

    if motion == MOTION_RANDOM:
        selected = random.choice(_MOTION_STRATEGIES)
        print("随机选取水印轨迹策略：", selected)
        motion = selected

    if motion == MOTION_BOUNCE:
        px = f"abs(sin(2*PI*0.073*(t+0.3)/{fps}))"
        py = f"abs(sin(2*PI*0.051*t/{fps}))"
        rb = csr
        ew = edge_width
        x_expr = (
            f"if(lt({px}\\,0.5)\\,  (w-text_w)*{ew}*{px}*2\\,  "
            f"(w-text_w)*({rb}+{ew}*({px}-0.5)*2))"
        )
        y_expr = (
            f"if(lt({py}\\,0.5)\\,  (h-text_h)*{ew}*{py}*2\\,  "
            f"(h-text_h)*({rb}+{ew}*({py}-0.5)*2))"
        )
        return clamp_x(x_expr), clamp_y(y_expr)

    if motion == MOTION_CIRCLE:
        cp = "floor(mod(t/15\\,4))"
        co = csr
        co_r = 1.0 - csr
        hr = 0.05
        cx = (
            f"if(lt({cp}\\,1)\\, (w-text_w)*{co}\\,"
            f"if(lt({cp}\\,3)\\, (w-text_w)*{co_r}\\,"
            f"                   (w-text_w)*{co}))"
        )
        cy = (
            f"if(lt({cp}\\,2)\\, (h-text_h)*{co}\\,"
            f"                   (h-text_h)*{co_r})"
        )
        r = f"min((w-text_w)\\,(h-text_h))*{hr}"
        x_expr = f"{cx}+{r}*cos(2*PI*0.08*t/{fps})"
        y_expr = f"{cy}+{r}*sin(2*PI*0.08*t/{fps})"
        return clamp_x(x_expr), clamp_y(y_expr)

    if motion == MOTION_RANDOM_WALK:
        es = f"floor(mod(abs(sin(2*PI*0.017*t/{fps}))*4\\,4))"
        f1 = 0.061
        f2 = 0.043
        walk_param = f"abs(sin(2*PI*{f1}*t)+0.4*sin(2*PI*{f2}*t+1.3))/1.4"
        fixed_offset = f"round({walk_param}\\,7)"
        wp = csr
        fr = 0.5
        fo = 1.0 - csr
        x_expr = (
            f"if(lt({es}\\,1)\\, (w-text_w)*{wp}\\,"
            f"if(lt({es}\\,2)\\, (w-text_w)*{fr}\\,"
            f"if(lt({es}\\,3)\\, (w-text_w)*(1-{wp})\\,"
            f"                   (w-text_w)*{fo})))"
        )
        y_expr = (
            f"if(lt({es}\\,1)\\, (h-text_h)*{fo}\\,"
            f"if(lt({es}\\,2)\\, (h-text_h)*{wp}\\,"
            f"if(lt({es}\\,3)\\, (h-text_h)*{fr}\\,"
            f"                   (h-text_h)*(1-{wp}))))"
        )
        _ = fixed_offset
        return clamp_x(x_expr), clamp_y(y_expr)

    if motion == MOTION_SPIRAL:
        br = "min((w-text_w)\\,(h-text_h))"
        rmin = 0.05
        rrange = 0.5
        T = 20.0
        base_r = f"{br}*({rmin}+{rrange}*abs(sin(PI*t/{T})))"
        amp_r = 0.05
        cx = "(w-text_w)/2"
        cy = "(h-text_h)/2"
        ar = 0.05
        x_expr = (
            f"{cx}+{base_r}*cos(2*PI*0.065*t/{fps})*{amp_r}"
            f"+{br}*{ar}*sin(2*PI*0.095*t/{fps}+0.5)"
        )
        y_expr = (
            f"{cy}+{base_r}*sin(2*PI*0.065*t/{fps})*{amp_r}"
            f"+{br}*{ar}*sin(2*PI*0.127*t/{fps})"
        )
        return clamp_x(x_expr), clamp_y(y_expr)

    # inferred: lissajous is the default fallback trajectory.
    ar = max(0.05, min(0.5, (1.0 - 2.0 * csr) / 2.0 + 0.05))
    x_expr = (
        f"(w-text_w)/2 + min((w-text_w)\\,(h-text_h))*{ar}"
        f"*sin(2*PI*0.095*t/{fps}+0.5)"
    )
    y_expr = (
        f"(h-text_h)/2 + min((w-text_w)\\,(h-text_h))*{ar}"
        f"*sin(2*PI*0.127*t/{fps})"
    )
    return clamp_x(x_expr), clamp_y(y_expr)


def _build_motion_xy_for_overlay(
    motion: str, fps: float, center_safe_ratio: float = DEFAULT_CENTER_SAFE_RATIO
) -> tuple[str, str]:
    x_expr, y_expr = _build_motion_xy(motion, fps, center_safe_ratio)

    def _adapt(expr: str) -> str:
        expr = re.sub(r"(?<![a-zA-Z_])w(?![a-zA-Z_0-9])", "W", expr)
        expr = re.sub(r"(?<![a-zA-Z_])h(?![a-zA-Z_0-9])", "H", expr)
        return expr

    return _adapt(x_expr), _adapt(y_expr)


def _build_drawtext_filter(
    water_text: str,
    font: str,
    font_size: int,
    fps: float,
    motion: str,
    center_safe_ratio: float = DEFAULT_CENTER_SAFE_RATIO,
) -> str:
    safe_text = _escape_drawtext_text(water_text)
    safe_font = _normalize_font_for_ffmpeg(font)
    x_expr, y_expr = _build_motion_xy(motion, fps, center_safe_ratio)
    draw = (
        f"drawtext=fontfile='{safe_font}':text='{safe_text}':"
        f"fontsize={font_size}:fontcolor=white:x={x_expr}:y={y_expr}"
    )
    return f"format=yuv420p,{draw}"


def _build_overlay_filter(
    img_path: str,
    fps: float,
    motion: str,
    main_width: int,
    main_height: int,
    img_scale_ratio: float = DEFAULT_IMG_SCALE_RATIO,
    center_safe_ratio: float = DEFAULT_CENTER_SAFE_RATIO,
) -> str:
    safe_img = _normalize_image_path_for_ffmpeg(img_path)
    target_width = max(1, int(min(main_width, main_height) * img_scale_ratio))
    x_expr, y_expr = _build_motion_xy_for_overlay(
        motion, fps, center_safe_ratio
    )
    return (
        f"movie='{safe_img}',scale={target_width}:-1[wm];"
        f"[0:v][wm]overlay=x='{x_expr}':y='{y_expr}':format=auto,"
        f"format=yuv420p"
    )


def _run_ffmpeg_with_progress(cmd: list[str], total_duration: float):
    _call_optional(CallBack, "reset_water_progress")
    print("正在绘制水印，处理中...")
    kwargs = _call_optional(AccelUtils, "subprocess_no_console_kwargs")
    if not isinstance(kwargs, dict):
        kwargs = {}
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        **kwargs,
    )
    _call_optional(TaskHardStop, "register", process)
    stderr_lines: list[str] = []
    last_percent = -1.0
    last_heartbeat_ts = time.time()
    try:
        stderr = process.stderr
        if stderr is not None:
            for raw_line in stderr:
                line = (
                    raw_line.decode("utf-8", "ignore")
                    if isinstance(raw_line, bytes)
                    else raw_line
                )
                line = line.strip()
                if not line:
                    continue
                stderr_lines.append(line)
                del stderr_lines[:-100]
                if getattr(Working, "need_stop", False):
                    _call_optional(TaskHardStop, "mark_stopped")
                    process.kill()
                    return -1, _STOPPED_BY_USER
                if not line.startswith("out_time_ms="):
                    continue
                try:
                    out_time_ms = float(line.split("=", 1)[1])
                except (TypeError, ValueError):
                    continue
                current_sec = out_time_ms / 1000000.0
                pct_raw = (
                    current_sec / total_duration * 100.0
                    if total_duration > 0
                    else 0.0
                )
                percent = max(0.0, min(99.9, pct_raw))
                if percent - last_percent >= 1.0:
                    last_percent = percent
                    _call_optional(CallBack, "water_progress_bar", percent)
                now_ts = time.time()
                if now_ts - last_heartbeat_ts >= 2.0:
                    last_heartbeat_ts = now_ts
                    _call_optional(CallBack, "water_progress_bar", int(percent))
        return_code = process.wait()
        _call_optional(CallBack, "water_progress_bar_done")
        return return_code, "\n".join(stderr_lines[-20:])
    except Exception as exc:
        if process.poll() is None:
            process.kill()
        return -1, f"{exc}\n" + "\n".join(stderr_lines[-20:])
    finally:
        _call_optional(TaskHardStop, "unregister", process)


def _gpu_common(
    ffmpeg: str,
    video_path: str,
    output_path: str,
    filter_key: str,
    filter_text: str,
    fps: float,
    bitrate,
    duration: float,
    width: int,
    height: int,
    is_bitmap: bool,
):
    profiles = AccelUtils.detect_gpu_profiles()
    attempts = AccelUtils.build_gpu_encode_attempts(profiles)
    if not attempts:
        return _failure(
            _MSG_NO_GPU_ENCODER_FFMPEG,
            duration,
            width,
            height,
            fps,
            bitrate,
            filter_text,
            profiles,
        )
    fail_reasons: list[str] = []
    for attempt in attempts:
        _abort_if_stopped(output_path)
        attempt_name, encoder, vendor, vendor_params = _attempt_fields(attempt)
        cmd = [
            ffmpeg,
            "-y",
            "-fflags",
            "+genpts",
            "-i",
            video_path,
            "-progress",
            "pipe:2",
            "-nostats",
            filter_key,
            filter_text,
            "-r",
            str(fps),
            "-c:v",
            encoder,
            "-b:v",
            bitrate,
            "-pix_fmt",
            "yuv420p",
            "-map",
            "0:v:0",
            "-map",
            "0:a?",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            output_path,
        ]
        run_code, stderr_tail = _run_ffmpeg_with_progress(cmd, duration)
        if run_code == 0:
            msg = (
                f"GPU{'图片' if is_bitmap else '加速'}水印成功，编码器：{encoder}，"
                f"厂商：{vendor}，策略：{attempt_name}"
            )
            return _success(
                msg,
                encoder,
                vendor,
                vendor_params,
                attempt_name,
                duration,
                width,
                height,
                fps,
                bitrate,
                filter_text,
                profiles,
                fail_reasons,
                cmd,
                run_code,
                stderr_tail,
            )
        fail_reasons.append(
            f"{attempt_name} failed, code={run_code}, stderr={stderr_tail[-300:]}"
        )
    return _failure(
        "gpu pipeline failed: " + " | ".join(fail_reasons),
        duration,
        width,
        height,
        fps,
        bitrate,
        filter_text,
        profiles,
        fail_reasons,
    )


def _try_gpu_ffmpeg_water(
    video_path: str,
    output_path: str,
    water_text: str,
    motion: str,
    center_safe_ratio: float,
):
    ffmpeg, resolve_msg = _resolve_ffmpeg()
    if not ffmpeg:
        return _failure(resolve_msg or "ffmpeg path empty")
    if not AccelUtils.is_ffmpeg_available(ffmpeg):
        return _failure("ffmpeg 不可用")
    meta = _probe_meta(video_path)
    duration = _safe_float(meta.get("duration"), 0.01, 0.01)
    width = _safe_int(meta.get("width"), 1280, 1)
    height = _safe_int(meta.get("height"), 720, 1)
    font = ResourcePath.get_ttf_path("ttf_song_jian_ti.TTF")
    fps = _safe_float(VideoBitUtils.gen_fps_data(video_path, (24.0, 60.0, 0.75)), 24.0, 1.0)
    bitrate = VideoBitUtils.gen_bit_data(video_path, (1000, 5000, 0.7)) or "1800k"
    bitrate = f"{bitrate}k" if isinstance(bitrate, (int, float)) else str(bitrate)
    font_size = _safe_int(utils.water_font_size(width, height, 24), 24, 8)
    filter_text = _build_drawtext_filter(
        water_text, font, font_size, fps, motion, center_safe_ratio
    )
    return _gpu_common(
        ffmpeg,
        video_path,
        output_path,
        "-vf",
        filter_text,
        fps,
        bitrate,
        duration,
        width,
        height,
        False,
    )


def _try_gpu_bitmap_water(
    video_path: str,
    output_path: str,
    img_path: str,
    motion: str,
    img_scale_ratio: float,
    center_safe_ratio: float,
):
    ffmpeg, resolve_msg = _resolve_ffmpeg()
    if not ffmpeg:
        return _failure(resolve_msg or "ffmpeg path empty")
    if not AccelUtils.is_ffmpeg_available(ffmpeg):
        return _failure("ffmpeg 不可用")
    meta = _probe_meta(video_path)
    duration = _safe_float(meta.get("duration"), 0.01, 0.01)
    width = _safe_int(meta.get("width"), 1280, 1)
    height = _safe_int(meta.get("height"), 720, 1)
    fps = _safe_float(VideoBitUtils.gen_fps_data(video_path, (24.0, 60.0, 0.75)), 24.0, 1.0)
    bitrate = VideoBitUtils.gen_bit_data(video_path, (1000, 5000, 0.7)) or "1800k"
    bitrate = f"{bitrate}k" if isinstance(bitrate, (int, float)) else str(bitrate)
    filter_complex = _build_overlay_filter(
        img_path,
        fps,
        motion,
        width,
        height,
        img_scale_ratio,
        center_safe_ratio,
    )
    return _gpu_common(
        ffmpeg,
        video_path,
        output_path,
        "-filter_complex",
        filter_complex,
        fps,
        bitrate,
        duration,
        width,
        height,
        True,
    )


def _cpu_ffmpeg_watermark_libx264(
    video_path: str,
    output_path: str,
    water_text: str,
    motion: str,
    center_safe_ratio: float,
):
    ffmpeg, resolve_msg = _resolve_ffmpeg()
    if not ffmpeg:
        return _failure(resolve_msg or "ffmpeg path empty")
    if not AccelUtils.is_ffmpeg_available(ffmpeg):
        return _failure("ffmpeg 不可用")
    print("正在使用CPU水印...")
    if not AccelUtils.probe_ffmpeg_encoders(ffmpeg, "libx264"):
        return _failure("当前 ffmpeg 未包含 libx264 编码器")
    meta = _probe_meta(video_path)
    duration = _safe_float(meta.get("duration"), 0.01, 0.01)
    width = _safe_int(meta.get("width"), 1280, 1)
    height = _safe_int(meta.get("height"), 720, 1)
    font = ResourcePath.get_ttf_path("ttf_song_jian_ti.TTF")
    fps = _safe_float(VideoBitUtils.gen_fps_data(video_path, (24.0, 60.0, 0.75)), 24.0, 1.0)
    bitrate = VideoBitUtils.gen_bit_data(video_path, (1000, 5000, 0.7)) or "1800k"
    bitrate = f"{bitrate}k" if isinstance(bitrate, (int, float)) else str(bitrate)
    last_error = ""
    for index in range(0, 12):
        _abort_if_stopped(output_path)
        font_size = max(10, 24 - index)
        filter_text = _build_drawtext_filter(
            water_text, font, font_size, fps, motion, center_safe_ratio
        )
        cmd = [
            ffmpeg,
            "-y",
            "-fflags",
            "+genpts",
            "-i",
            video_path,
            "-progress",
            "pipe:2",
            "-nostats",
            "-vf",
            filter_text,
            "-r",
            str(fps),
            "-c:v",
            "libx264",
            "-b:v",
            bitrate,
            "-preset",
            "veryfast",
            "-threads",
            "4",
            "-pix_fmt",
            "yuv420p",
            "-map",
            "0:v:0",
            "-map",
            "0:a?",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            output_path,
        ]
        run_code, stderr_tail = _run_ffmpeg_with_progress(cmd, duration)
        if run_code == 0:
            print("CPU水印成功（libx264），字号=", font_size)
            return _success(
                "CPU水印成功（libx264）",
                "libx264",
                "",
                [],
                "cpu",
                duration,
                width,
                height,
                fps,
                bitrate,
                filter_text,
                [],
                [],
                cmd,
                run_code,
                stderr_tail,
            )
        last_error = stderr_tail[-500:]
    return _failure(
        "CPU FFmpeg 水印失败: " + last_error,
        duration,
        width,
        height,
        fps,
        bitrate,
    )


def _cpu_bitmap_watermark_libx264(
    video_path: str,
    output_path: str,
    img_path: str,
    motion: str,
    img_scale_ratio: float,
    center_safe_ratio: float,
):
    ffmpeg, resolve_msg = _resolve_ffmpeg()
    if not ffmpeg:
        return _failure(resolve_msg or "ffmpeg path empty")
    if not AccelUtils.is_ffmpeg_available(ffmpeg):
        return _failure("ffmpeg 不可用")
    print("正在使用CPU图片水印...")
    if not AccelUtils.probe_ffmpeg_encoders(ffmpeg, "libx264"):
        return _failure("当前 ffmpeg 未包含 libx264 编码器")
    meta = _probe_meta(video_path)
    duration = _safe_float(meta.get("duration"), 0.01, 0.01)
    width = _safe_int(meta.get("width"), 1280, 1)
    height = _safe_int(meta.get("height"), 720, 1)
    fps = _safe_float(VideoBitUtils.gen_fps_data(video_path, (24.0, 60.0, 0.75)), 24.0, 1.0)
    bitrate = VideoBitUtils.gen_bit_data(video_path, (1000, 5000, 0.7)) or "1800k"
    bitrate = f"{bitrate}k" if isinstance(bitrate, (int, float)) else str(bitrate)
    filter_complex = _build_overlay_filter(
        img_path,
        fps,
        motion,
        width,
        height,
        img_scale_ratio,
        center_safe_ratio,
    )
    last_error = ""
    for _ in range(0, 12):
        _abort_if_stopped(output_path)
        cmd = [
            ffmpeg,
            "-y",
            "-fflags",
            "+genpts",
            "-i",
            video_path,
            "-progress",
            "pipe:2",
            "-nostats",
            "-filter_complex",
            filter_complex,
            "-r",
            str(fps),
            "-c:v",
            "libx264",
            "-b:v",
            bitrate,
            "-preset",
            "veryfast",
            "-threads",
            "4",
            "-pix_fmt",
            "yuv420p",
            "-map",
            "0:v:0",
            "-map",
            "0:a?",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            output_path,
        ]
        run_code, stderr_tail = _run_ffmpeg_with_progress(cmd, duration)
        if run_code == 0:
            print("CPU图片水印成功（libx264）")
            return _success(
                "CPU图片水印成功（libx264）",
                "libx264",
                "",
                [],
                "cpu",
                duration,
                width,
                height,
                fps,
                bitrate,
                filter_complex,
                [],
                [],
                cmd,
                run_code,
                stderr_tail,
            )
        last_error = stderr_tail[-500:]
    return _failure(
        "CPU FFmpeg 图片水印失败: " + last_error,
        duration,
        width,
        height,
        fps,
        bitrate,
    )


def _cpu_fallback_add_water(
    video_path: str,
    output_path: str,
    water_text: str,
    motion: str,
    center_safe_ratio: float,
):
    return _cpu_ffmpeg_watermark_libx264(
        video_path, output_path, water_text, motion, center_safe_ratio
    )


def add_text_water(
    video_path: str,
    output_path: str,
    water_text: str,
    accel_mode: str | None = None,
    motion: str = MOTION_RANDOM,
    center_safe_ratio: float = DEFAULT_CENTER_SAFE_RATIO,
) -> bool:
    if not os.path.exists(video_path):
        print("输入视频不存在: ", video_path)
        return False
    if not output_path:
        print("输出路径不能为空")
        return False
    output_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_dir, exist_ok=True)
    mode = AccelUtils.normalize_accel_mode(accel_mode)
    if motion not in _MOTION_STRATEGIES and motion != MOTION_RANDOM:
        print("未知轨迹策略 '", motion, "'，已自动改为随机选取")
        motion = MOTION_RANDOM
    print(
        "开始视频水印处理，模式：",
        mode,
        "，轨迹：",
        motion,
        "，输入：",
        video_path,
        "，输出：",
        output_path,
    )
    start_ts = time.time()
    cpu_mode = getattr(AccelUtils, "ACCEL_MODE_CPU", "cpu")
    gpu_mode = getattr(AccelUtils, "ACCEL_MODE_GPU", "gpu")

    if mode == cpu_mode:
        print("当前为强制CPU模式，跳过GPU探测")
        ok, msg = _cpu_fallback_add_water(
            video_path, output_path, water_text, motion, center_safe_ratio
        )[:2]
        if ok:
            print("CPU水印处理完成，总耗时：", round(time.time() - start_ts, 2), " 秒")
            return True
        print("CPU水印失败：", msg)
        return False

    if mode == gpu_mode:
        print("正在使用GPU加速水印处理...")
        ok, msg = _try_gpu_ffmpeg_water(
            video_path, output_path, water_text, motion, center_safe_ratio
        )[:2]
        if ok:
            _call_optional(AccelUtils, "note_water_session_gpu_encode_success")
            print(
                "GPU水印处理完成，总耗时：",
                round(time.time() - start_ts, 2),
                " 秒，详情：",
                msg,
            )
            return True
        print("强制GPU模式失败：", msg)
        return False

    print("正在使用GPU加速水印处理...")
    ok, gpu_msg = _try_gpu_ffmpeg_water(
        video_path, output_path, water_text, motion, center_safe_ratio
    )[:2]
    if ok:
        _call_optional(AccelUtils, "note_water_session_gpu_encode_success")
        print(
            "GPU水印处理完成，总耗时：",
            round(time.time() - start_ts, 2),
            " 秒，详情：",
            gpu_msg,
        )
        return True
    print("未检测到可用GPU编码链路或GPU处理失败，自动回退CPU。原因：", gpu_msg)
    ok, msg = _cpu_fallback_add_water(
        video_path, output_path, water_text, motion, center_safe_ratio
    )[:2]
    if ok:
        _call_optional(
            AccelUtils,
            "note_water_session_auto_gpu_fallback_after_hw_failed",
        )
        print("CPU回退处理完成，总耗时：", round(time.time() - start_ts, 2), " 秒")
        return True
    print("CPU回退失败：", msg)
    return False


def add_picture_water(
    video_path: str,
    output_path: str,
    img_path: str,
    accel_mode: str | None = None,
    motion: str = MOTION_RANDOM,
    img_scale_ratio: float = DEFAULT_IMG_SCALE_RATIO,
    center_safe_ratio: float = DEFAULT_CENTER_SAFE_RATIO,
) -> bool:
    if not os.path.exists(video_path):
        print("输入视频不存在: ", video_path)
        return False
    if not output_path:
        print("输出路径不能为空")
        return False
    if not os.path.exists(img_path):
        print("水印图片不存在: ", img_path)
        return False
    output_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_dir, exist_ok=True)
    img_scale_ratio = max(0.05, min(0.9, _safe_float(img_scale_ratio, DEFAULT_IMG_SCALE_RATIO)))
    print(
        "即将给视频加图片水印，水印宽度占源视频短边 ",
        int(img_scale_ratio * 100),
        "%",
    )
    mode = AccelUtils.normalize_accel_mode(accel_mode)
    if motion not in _MOTION_STRATEGIES and motion != MOTION_RANDOM:
        print("未知轨迹策略 '", motion, "'，已自动改为随机选取")
        motion = MOTION_RANDOM
    print(
        "开始图片水印处理，模式：",
        mode,
        "，轨迹：",
        motion,
        "，缩放比例：",
        img_scale_ratio,
        "，输入：",
        video_path,
        "，输出：",
        output_path,
    )
    start_ts = time.time()
    cpu_mode = getattr(AccelUtils, "ACCEL_MODE_CPU", "cpu")
    gpu_mode = getattr(AccelUtils, "ACCEL_MODE_GPU", "gpu")

    if mode == cpu_mode:
        print("当前为强制CPU模式，跳过GPU探测")
        ok, msg = _cpu_bitmap_watermark_libx264(
            video_path,
            output_path,
            img_path,
            motion,
            img_scale_ratio,
            center_safe_ratio,
        )[:2]
        if ok:
            print("CPU图片水印处理完成，总耗时：", round(time.time() - start_ts, 2), " 秒")
            return True
        print("CPU图片水印失败：", msg)
        return False

    if mode == gpu_mode:
        print("正在使用GPU加速图片水印处理...")
        ok, msg = _try_gpu_bitmap_water(
            video_path,
            output_path,
            img_path,
            motion,
            img_scale_ratio,
            center_safe_ratio,
        )[:2]
        if ok:
            _call_optional(AccelUtils, "note_water_session_gpu_encode_success")
            print(
                "GPU图片水印处理完成，总耗时：",
                round(time.time() - start_ts, 2),
                " 秒，详情：",
                msg,
            )
            return True
        print("强制GPU模式失败：", msg)
        return False

    print("正在使用GPU加速图片水印处理...")
    ok, gpu_msg = _try_gpu_bitmap_water(
        video_path,
        output_path,
        img_path,
        motion,
        img_scale_ratio,
        center_safe_ratio,
    )[:2]
    if ok:
        _call_optional(AccelUtils, "note_water_session_gpu_encode_success")
        print(
            "GPU图片水印处理完成，总耗时：",
            round(time.time() - start_ts, 2),
            " 秒，详情：",
            gpu_msg,
        )
        return True
    print("未检测到可用GPU编码链路或GPU处理失败，自动回退CPU。原因：", gpu_msg)
    ok, msg = _cpu_bitmap_watermark_libx264(
        video_path,
        output_path,
        img_path,
        motion,
        img_scale_ratio,
        center_safe_ratio,
    )[:2]
    if ok:
        _call_optional(
            AccelUtils,
            "note_water_session_auto_gpu_fallback_after_hw_failed",
        )
        print("CPU回退图片水印处理完成，总耗时：", round(time.time() - start_ts, 2), " 秒")
        return True
    print("CPU回退图片水印失败：", msg)
    return False
