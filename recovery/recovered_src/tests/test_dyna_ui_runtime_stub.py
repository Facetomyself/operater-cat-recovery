from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "src" / "resource" / "ui" / "dyna"


class _DummyMeta(type):
    def __getattr__(cls, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return _Dummy()


class _Dummy(metaclass=_DummyMeta):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return _Dummy(*args, **kwargs)

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)

        def noop(*args, **kwargs):
            return _Dummy()

        return noop


def _install_fake_pyqt5() -> None:
    package = types.ModuleType("PyQt5")
    for name in ("QtCore", "QtGui", "QtWidgets"):
        module = types.ModuleType(f"PyQt5.{name}")
        module.__getattr__ = lambda attr: _Dummy
        setattr(package, name, module)
        sys.modules[f"PyQt5.{name}"] = module
    sys.modules["PyQt5"] = package


def test_generated_ui_modules_execute_with_stub_qt():
    _install_fake_pyqt5()
    for name in (
        "ai_employee_item",
        "auto_flow_item",
        "ban_yun_flow_comment_item",
        "down_load_flow_item",
        "yulan_flow_item",
        "yun_auto_item",
        "yun_preview_item",
        "yun_yin_mao_main",
    ):
        module = importlib.import_module(f"src.resource.ui.dyna.{name}")
        class_name = "Ui_MainWindow" if name == "yun_yin_mao_main" else "Ui_Form"
        ui = getattr(module, class_name)()
        ui.setupUi(_Dummy())
