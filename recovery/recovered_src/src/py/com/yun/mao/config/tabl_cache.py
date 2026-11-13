# Recovered module: src.py.com.yun.mao.config.tabl_cache
# ConfigParser-backed cache reconstructed from the module constants.
from __future__ import annotations

import configparser
from pathlib import Path


AI_EMPLOYEE_API_KEY = "new_ai_employee_api_key"
AI_EMPLOYEE_GROUP = "ai_employee_group"
AI_REFUSE_TOKEN_LIST = "new_ai_refuse_token_list"
API_FUN_TAB = "api_fun_group"
API_FUN_api_id = "api_id"
API_FUN_api_hash = "api_hash"
CHECK_POST_PERMISSION = "CHECK_POST_PERMISSION"
CURRENT_TASK_TG_ACCOUNT = "CURRENT_TASK_TG_ACCOUNT_"
DOWNLOAD_TEMP_FOLDER = "download_temp_folder"
DOWN_CONFIG_RATE = "down_config_rate_"
INI_FILE_PATH = r"D:\reverse_ENV\workspace\YunYinData\cache\tab_cache.ini"
LAST_FLOOD_TIME = "last_flood_time"
LAST_TAB_INDEX = "LAST_TAB_INDEX"
LOGGER_MODEL = "logger_model"
MAIN_BANYUN_MONITOR_OPTION = "main_banyun_monitor_option"
MAIN_BANYUN_MONITOR_SECTION = "main_banyun_monitor_section"
MAIN_TOOLS_BOX_AD_FILES = "main_tools_box_ad_files"
MAIN_TOOLS_BOX_AD_HTML_TEXT = "main_tools_box_ad_html_text"
MAIN_TOOLS_BOX_AD_SOURCE_LINK = "main_tools_box_ad_source_link"
MAIN_TOOLS_BOX_POST_LINK = "main_tools_box_post_link"
MAIN_TOOLS_BOX_SECTION = "main_tools_box_section"
MAIN_YUN_YIN_TAB_AUTO_CHANGE_RATE = "main_yun_yin_tab_auto_change_rate"
MAIN_YUN_YIN_TAB_SECTION = "main_yun_yin_tab_section"
PROXY_SETTING_GROUP = "proxy_setting_group"
PROXY_SETTING_enable = "proxy_enable"
PROXY_SETTING_ip = "proxy_ip"
PROXY_SETTING_port = "proxy_port"
TEXT_BIAO_SHI = "biao_shi"
TEXT_BIAO_SHI_text = "TEXT_BIAO_SHI_text"
TOP_CACHE_GROUP = "top_cache_group"
UP_CONFIG_RATE = "up_config_rate_"


def abs_cache_file() -> str:
    return INI_FILE_PATH


def create_ini_if_need() -> None:
    path = Path(INI_FILE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")


def singleton(cls):
    instance = None

    def get_instance(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    get_instance.__name__ = "get_instance"
    return get_instance


@singleton
class TableCache:
    def __init__(self) -> None:
        self.init()

    def init(self):
        create_ini_if_need()
        self.config = configparser.ConfigParser()
        self.config.read(abs_cache_file(), encoding="utf-8")
        return self

    def update_cache(self):
        return self.init()

    def read_cache(self, section: str, key: str, default=None):
        try:
            value = self.config.get(section, key)
        except (configparser.Error, KeyError):
            return default
        return value

    def write_cache(self, section: str, key: str, value: object) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        with open(abs_cache_file(), "w", encoding="utf-8") as handle:
            self.config.write(handle)

    def get(self, section: str, key: str, default=None):
        return self.read_cache(section, key, default)

    def set(self, section: str, key: str, value: object) -> None:
        self.write_cache(section, key, value)


def INSTANCE():
    return tableCache


tableCache = TableCache()
