# Recovered module: src.py.com.yun.mao.water.waterUtils
# Reconstruction from Nuitka constants and offline Hex-Rays.
from __future__ import annotations

import math
import os
import time

from src.py.com.yun.mao.cd import Working
from src.py.com.yun.mao.config import YunYinMaoConfig
from src.py.com.yun.mao.dclass.DTopClass import Water
from src.py.com.yun.mao.util import AccelUtils
from src.py.com.yun.mao.util.TracePrinterHelper import print_trace
from src.py.com.yun.mao.util.need import utils
from src.py.com.yun.mao.water import PicWaterUtils, VideoWaterUtilsToSmallFile
from src.py.com.yun.mao.water.VideoWaterUtilsToSmallFile import MOTION_RANDOM


def get_file_size_byte(file_path: str) -> int:
    return os.path.getsize(file_path)


def is_file_up_100m(input_file: str) -> bool:
    old_file_size = get_file_size_byte(input_file)
    old_mb = round(old_file_size / 1024 / 1024, 2)
    return old_mb > 100


def auto_add_water(
    input_file: str,
    water: Water,
    only_down_load: bool = False,
    accel_mode: str | None = None,
    motion: str = MOTION_RANDOM,
    output_file: str | None = None,
) -> bool:
    """Add a text or picture watermark to a supported picture/video file."""
    _, extension = os.path.splitext(input_file)
    lower_extension = extension.lower()
    old_name = os.path.basename(input_file)
    directory = os.path.dirname(input_file)
    water_image_path = getattr(water, "picPath", "")
    if only_down_load:
        YunYinMaoConfig.init_only_down_load_water_root()

    water_tag = getattr(YunYinMaoConfig, "WATER_TAG", "water")
    if not output_file:
        output_file = os.path.join(
            directory,
            f"{old_name}_{water_tag}_{int(time.time())}{extension}",
        )

    start = time.time()
    mode = getattr(water, "mode", None)

    if lower_extension in YunYinMaoConfig.PIC_MEDIA_FILE_LIST:
        if mode == YunYinMaoConfig.WATER_MODE_TEXT:
            print("正在为图片添加文字水印，水印为：", water.text, " 请稍后...")
            PicWaterUtils.water_text_mark(
                input_file, output_file, water.text
            )
        elif mode == YunYinMaoConfig.WATER_MODE_PIC:
            print("正在为图片添加图片水印，水印资源是：", water_image_path, "，请稍后...")
            if not os.path.exists(water_image_path):
                print(" 水印图片不存在！")
                print("添加失败！")
                return False
            PicWaterUtils.water_pic_mark(
                input_file,
                output_file,
                water_image_path,
                getattr(water, "picRatio", 30) / 100.0,
            )
        else:
            print("添加失败！")
            return False
        elapsed = round(time.time() - start, 2)
        print("图片 ", input_file, " 水印添加成功！耗时 ", elapsed, "秒")
        return True

    if lower_extension in YunYinMaoConfig.VIDEO_MEDIA_FILE_LIST:
        water_video_path = output_file
        if is_file_up_100m(input_file):
            o_size = get_file_size_byte(input_file)
            o_mb = round(o_size / 1024 / 1024, 2)
            print(
                "原来文件大小 ",
                o_mb,
                " Mb，智能移动水印以及智能压缩，可能会消耗比较长时间，"
                "如果你CPU频率比较高，那么会很快，请耐心等待...",
            )
        Working.need_stop = False
        accel_mode, motion = AccelUtils.effective_accel_mode_water(
            accel_mode, motion
        )
        if mode == YunYinMaoConfig.WATER_MODE_TEXT:
            print("正在加智能移动文字水印，水印为：", water.text)
            ok = VideoWaterUtilsToSmallFile.add_text_water(
                input_file,
                water_video_path,
                water.text,
                accel_mode,
                motion,
            )
        elif mode == YunYinMaoConfig.WATER_MODE_PIC:
            print("正在加智能移动图片水印，水印资源是：", water_image_path)
            if not os.path.exists(water_image_path):
                print(" 水印图片不存在！")
                print("添加失败！")
                return False
            ok = VideoWaterUtilsToSmallFile.add_picture_water(
                input_file,
                water_video_path,
                water_image_path,
                accel_mode,
                motion,
                getattr(water, "picRatio", 30) / 100.0,
            )
        else:
            print("添加失败！")
            return False

        if Working.need_stop:
            print("手动停止成功！")
            utils.safe_del_file(water_video_path)
            return False
        if not ok:
            utils.safe_del_file(water_video_path)
            print("添加失败！")
            return False
        gen_key_log(input_file, water_video_path, start)
        return True

    print("添加失败！")
    return False


def gen_key_log(input_file: str, output_file: str, start: float) -> str:
    try:
        old_file_size = get_file_size_byte(input_file)
        new_file_size = get_file_size_byte(output_file)
    except Exception as exc:
        print_trace(exc)
        return ""

    old_mb = round(old_file_size / 1024 / 1024, 2)
    new_mb = round(new_file_size / 1024 / 1024, 2)
    cha_zhi_mb = round(old_mb - new_mb, 2)
    present = round(cha_zhi_mb / old_mb * 100.0, 2) if old_mb else 0.0
    inter = max(0, int(time.time() - start))
    minute = math.floor(inter / 60)
    sec = inter - minute * 60
    log_ = (
        f"视频 {input_file} 添加移动水印成功，原来文件大小 {old_mb} Mb "
        f"水印文件大小 {new_mb} Mb 减少了 {cha_zhi_mb} Mb , "
        f"减少百分比：{present} %"
    )
    log_tip = f" 耗时 {minute} 分 {sec} 秒"
    all_log = log_ + log_tip
    print(all_log)
    return all_log
