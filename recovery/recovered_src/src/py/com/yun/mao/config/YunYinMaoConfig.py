# Recovered module: src.py.com.yun.mao.config.YunYinMaoConfig
# Path and multi-account policy reconstructed from runtime constants.
from __future__ import annotations

import os
from pathlib import Path



AI_GEN_MAX_TRY_COUNT = 1
BASE_FILTER_DU_MAX = 6000
BASE_FILTER_DU_MIN = 0
BASE_FILTER_SIZE_MAX = 100000
BASE_FILTER_SIZE_MIN = 0
COMMENT_WANT_COUNT_MAX = 1000
DEFAULT_DOWN_LOAD_RATE = 1
DEFAULT_UP_LOAD_RATE = 1
DOWNLOAD_MAX_SIZE = 10000
DOWNLOAD_TEMP_FOLDER = "download_temp_folder"
FETCH_MESSAGE_EXTEND_COUNT = 20
FILE_PART_PATCH_MAX_PER_N = 3
FILE_PART_PATCH_MAX_TOTAL = 50
FORWARD_MAX_SIZE = 20000
INCREASE_MODEL_WANT_COUNT_MAX = 1000
LOOP_MODE_REGION_COUNT_MAX = 1000
MAO_REPLACE_FU_HAO = "->"
MAX_CONNECTION_COUNT = 10
MAX_TRY_COUNT = 5
LOG_KEY_WORDS = [
    "下载了",
    "正在上传",
    "正在绘制水印",
    "正在生成预览视频",
]
MY_PHOTO_SUFFIX = ".jpg"
MY_VIDEO_SUFFIX = ".mp4"
PIC_MEDIA_FILE_LIST = [".jpg", ".jpeg", ".png"]
VIDEO_MEDIA_FILE_LIST = [".mp4", ".mov", ".avi", ".m4v"]
WATER_MODE_TEXT = "文字水印"
WATER_MODE_PIC = "图片水印"
YUAN_SHI_PIN_DURATION = ["原视频时长", "完整版", "视频时长", "完整版"]
PARSE_MESSAGE_WHILE_MAX_LOOP = 100
RANDOM_GROUP_FETCH_ID_BUFFER = 20
RAN_DOM_MESSAGE_TOP_ID = 200000
RAN_DOM_MODEL_WANT_COUNT_MAX = 1000
RATE_URL = (
    "https://telegra.ph/%E8%B6%85%E7%BA%A7%E4%B8%8B%E8%BD%BD"
    "%E4%B8%8A%E4%BC%A0%E9%80%9F%E7%8E%87%E9%85%8D%E7%BD%AE"
    "%E8%AF%B4%E6%98%8E-10-11"
)
SPLIT_FU_HAO_ = "，"
TOP_CACHE_GROUP = "top_cache_group"
WATER_TAG = "water"

multi_abs_yun_yin_dir = r"D:\reverse_ENV\workspace\YunYinData"
multi_abs_cache_dir = os.path.join(multi_abs_yun_yin_dir, "cache")
multi_abs_log_dir = os.path.join(multi_abs_yun_yin_dir, "log")
multi_abs_tgaccount_dir = os.path.join(multi_abs_yun_yin_dir, "tgaccount")


def _ensure(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def is_support_multi() -> bool:
    try:
        from ..fea import _sq_jqm

        return bool(_sq_jqm.current_account_info.is_multi_permission())
    except Exception:
        return False


def abs_cache_dir() -> str:
    return _ensure(multi_abs_cache_dir)


def abs_cache_only_multi_dir() -> str:
    return _ensure(os.path.join(multi_abs_cache_dir, "only_multi"))


def abs_tg_account_dir() -> str:
    return _ensure(multi_abs_tgaccount_dir)


def get_temp_folder() -> str:
    return _ensure(os.path.join(multi_abs_yun_yin_dir, DOWNLOAD_TEMP_FOLDER))


def get_windows_downloads_default_folder() -> str:
    return str(Path.home() / "Downloads")


def init_only_down_load_water_root() -> str:
    return _ensure(os.path.join(multi_abs_yun_yin_dir, WATER_TAG, "only_download"))


def yun_yin_ban_yun_folder() -> str:
    return _ensure(os.path.join(multi_abs_yun_yin_dir, "ban_yun"))


def yun_yin_ban_yun_folder_only_down_load() -> str:
    return _ensure(os.path.join(multi_abs_yun_yin_dir, "ban_yun", "only_download"))
