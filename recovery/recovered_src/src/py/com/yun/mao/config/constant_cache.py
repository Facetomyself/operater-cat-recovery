# Recovered module: src.py.com.yun.mao.config.constant_cache
from __future__ import annotations

import configparser
from pathlib import Path


ALL_CACHE_CONFIG_PATH = r"D:\reverse_ENV\workspace\operater-cat\constant.ini"
CONSTANT = "constant"
CONSTANT_LINK = "constant_link"
SOFT_NAME = "soft_name"
U_CODE_PRE = "u_code_pre"


def create_ini_if_need() -> None:
    path = Path(ALL_CACHE_CONFIG_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[constant]\n", encoding="utf-8")


def singleton(cls):
    instance = None

    def get_instance(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return get_instance


@singleton
class ConstantCache:
    def __init__(self) -> None:
        self.init()

    def init(self):
        create_ini_if_need()
        self.config = configparser.ConfigParser()
        self.config.read(ALL_CACHE_CONFIG_PATH, encoding="utf-8")
        return self

    def update_cache(self):
        return self.init()

    def get(self, key: str, default=None):
        try:
            return self.config.get(CONSTANT, key)
        except (configparser.Error, KeyError):
            return default

    def read_cache(self, key: str, default=None):
        return self.get(key, default)

    def set(self, key: str, value: object) -> None:
        if not self.config.has_section(CONSTANT):
            self.config.add_section(CONSTANT)
        self.config.set(CONSTANT, key, str(value))
        with open(ALL_CACHE_CONFIG_PATH, "w", encoding="utf-8") as handle:
            self.config.write(handle)


INSTANCE = ConstantCache()
