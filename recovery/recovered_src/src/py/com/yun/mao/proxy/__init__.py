# Recovered package: src.py.com.yun.mao.proxy
from __future__ import annotations

import importlib
import os


path = os.path.dirname(__file__)

NUITKA_PACKAGE_src = os.environ.get("NUITKA_PACKAGE_src", "\\not_existing")
NUITKA_PACKAGE_src_py = os.environ.get(
    "NUITKA_PACKAGE_src_py", "\\not_existing"
)
NUITKA_PACKAGE_src_py_com = os.environ.get(
    "NUITKA_PACKAGE_src_py_com", "\\not_existing"
)
NUITKA_PACKAGE_src_py_com_yun = os.environ.get(
    "NUITKA_PACKAGE_src_py_com_yun", "\\not_existing"
)
NUITKA_PACKAGE_src_py_com_yun_mao = os.environ.get(
    "NUITKA_PACKAGE_src_py_com_yun_mao", "\\not_existing"
)
NUITKA_PACKAGE_src_py_com_yun_mao_proxy = os.environ.get(
    "NUITKA_PACKAGE_src_py_com_yun_mao_proxy", "\\not_existing"
)

__all__ = [
    "ProxySettingDialog",
    "NUITKA_PACKAGE_src",
    "NUITKA_PACKAGE_src_py",
    "NUITKA_PACKAGE_src_py_com",
    "NUITKA_PACKAGE_src_py_com_yun",
    "NUITKA_PACKAGE_src_py_com_yun_mao",
    "NUITKA_PACKAGE_src_py_com_yun_mao_proxy",
    "path",
]


def __getattr__(name: str):
    # inferred: keep class access lazy so importing the package has no UI or
    # filesystem side effects.
    if name == "ProxySettingDialog":
        module = importlib.import_module(".ProxySettingDialog", __name__)
        value = module.ProxySettingDialog
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
