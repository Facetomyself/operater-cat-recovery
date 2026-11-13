# Recovered module: src.py.com.yun.mao.fea._sq_hj
from __future__ import annotations

from src.py.version_code import is_dev_version, is_prod_version


def hj_dev_ok() -> bool:
    return bool(is_dev_version())


def hj_prod_ok() -> bool:
    return bool(is_prod_version())
