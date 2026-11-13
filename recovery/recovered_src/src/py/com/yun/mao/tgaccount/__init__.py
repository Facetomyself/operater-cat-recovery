# Recovered package: src.py.com.yun.mao.tgaccount
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
NUITKA_PACKAGE_src_py_com_yun_mao_tgaccount = os.environ.get(
    "NUITKA_PACKAGE_src_py_com_yun_mao_tgaccount", "\\not_existing"
)

_CLASS_EXPORTS = {
    "AiEmployeeListDialog": ("AiEmployeeListDialog", "AiEmployeeListDialog"),
    "TGAuthAccount": ("TGAuthAccount", "TGAuthAccount"),
    "TgAccountListDialog": ("TgAccountListDialog", "TgAccountListDialog"),
}
_MODULE_EXPORTS = {"TGAuthAccountSetting"}

__all__ = [
    "AiEmployeeListDialog",
    "TGAuthAccount",
    "TGAuthAccountSetting",
    "TgAccountListDialog",
    "NUITKA_PACKAGE_src",
    "NUITKA_PACKAGE_src_py",
    "NUITKA_PACKAGE_src_py_com",
    "NUITKA_PACKAGE_src_py_com_yun",
    "NUITKA_PACKAGE_src_py_com_yun_mao",
    "NUITKA_PACKAGE_src_py_com_yun_mao_tgaccount",
    "path",
]


def __getattr__(name: str):
    # inferred: lazy exports preserve the original package namespace without
    # importing PyQt dialogs while the package itself is being imported.
    if name in _CLASS_EXPORTS:
        module_name, attribute = _CLASS_EXPORTS[name]
        module = importlib.import_module(f".{module_name}", __name__)
        value = getattr(module, attribute)
        globals()[name] = value
        return value
    if name in _MODULE_EXPORTS:
        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
