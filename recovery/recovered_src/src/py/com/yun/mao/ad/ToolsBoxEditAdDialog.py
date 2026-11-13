# Recovered module: src.py.com.yun.mao.ad.ToolsBoxEditAdDialog
# Behaviour-level reconstruction from Nuitka constants, Hex-Rays, and UI XML.
from __future__ import annotations

from typing import Callable, List

from PyQt5 import QtGui, uic

from ..dclass import DTopClassHelper
from ..util import ResourcePath
from ..util.need import CommonCode, utils

try:
    from ..util.need.BaseDialog import BaseDialog
except (ImportError, AttributeError):
    from PyQt5.QtWidgets import QDialog as BaseDialog


AdHtmlCallbackType = Callable[[str, List[str]], None]


def _ad_file_to_str(value) -> str:
    converter = getattr(DTopClassHelper, "ad_file_to_str", None)
    if callable(converter):
        return str(converter(value) or "")
    return "" if value is None else str(value)


def _ad_str_to_file(value) -> str:
    converter = getattr(CommonCode, "ad_str_to_file", None)
    if callable(converter):
        return str(converter(value) or "")
    return "" if value is None else str(value)


def _obtain_legal_files(text) -> list[str]:
    parser = getattr(CommonCode, "obtain_legal_files", None)
    if callable(parser):
        return list(parser(text) or [])
    return [line.strip() for line in str(text or "").splitlines() if line.strip()]


class ToolsBoxEditAdDialog(BaseDialog):
    def __init__(
        self,
        parent=None,
        windowTitle=None,
        funBack: AdHtmlCallbackType | None = None,
        ad_html="",
        ad_files=None,
    ) -> None:
        super().__init__(parent)
        self.funBack = funBack
        self.ad_html = ad_html
        self.ad_files = list(ad_files or [])
        if windowTitle:
            self.setWindowTitle(windowTitle)
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("tools_box_ad_edit.ui"),
            self,
        )
        self.ui.textEdit_tools_box_text.setPlainText(
            _ad_file_to_str(ad_html) if ad_html else ""
        )
        self.ui.textEdit_tools_box_mideas.setText(
            "\n".join(str(item) for item in self.ad_files)
        )
        self.ui.tools_box_ad_btn_save.clicked.connect(self.on_ad_btn_save)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        screen_width, screen_height = utils.get_screen_size()
        window_width = int(screen_width / 2)
        window_height = int(screen_height / 6)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 10)
        self.resize(window_width, window_height)
        self.move(x_position, y_position)
        super().showEvent(a0)

    def on_ad_btn_save(self) -> None:
        ad_file_text = self.ui.textEdit_tools_box_mideas.toPlainText().strip()
        legal_files = _obtain_legal_files(ad_file_text)
        if ad_file_text and not legal_files:
            print("输入的媒体文件没有一个是合法的，请检查后重新输入！")
            return
        text_html = _ad_str_to_file(
            self.ui.textEdit_tools_box_text.toPlainText().strip()
        )
        if callable(self.funBack):
            self.funBack(text_html, legal_files)
        self.close()
