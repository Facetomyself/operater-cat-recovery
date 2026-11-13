# Recovered module: src.py.com.yun.mao.ad.AddOrEditAdDialog
# Behaviour-level reconstruction from Nuitka constants, Hex-Rays, and UI XML.
from __future__ import annotations

from typing import Callable

from PyQt5 import QtGui, uic

from ..dclass import DTopClassHelper
from ..dclass.DTopClass import Ad
from ..util import ResourcePath
from ..util.need import CommonCode, utils

try:
    from ..util.need.BaseDialog import BaseDialog
except (ImportError, AttributeError):
    from PyQt5.QtWidgets import QDialog as BaseDialog


CallbackType = Callable[[Ad], None]


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


class AddOrEditAdDialog(BaseDialog):
    def __init__(
        self,
        parent=None,
        windowTitle=None,
        funBack: CallbackType | None = None,
        ad: Ad | None = None,
        kid=None,
        comment=False,
    ) -> None:
        super().__init__(parent)
        self.funBack = funBack
        self.ad = ad
        self.kid = kid
        self.comment = comment
        self.adId = str(getattr(ad, "adId", "") or "")
        if not self.adId:
            if kid:
                self.adId = str(kid) + "-" + utils.gen_unit_name_by_ns()
            elif comment:
                self.adId = "comment-" + utils.gen_unit_name_by_ns()
            else:
                self.adId = "global-" + utils.gen_unit_name_by_ns()
        if windowTitle:
            self.setWindowTitle(windowTitle)
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("ad_add_edit.ui"),
            self,
        )
        self.ui.btn_save.clicked.connect(self.btnSave)
        self.ui.btn_cancel.clicked.connect(self.btnCancel)
        self.fillBeanIfNeed()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        screen_width, screen_height = utils.get_screen_size()
        # Recovered factors: width 4/10, height 3/10, center x /2, center y /6.
        window_width = int(screen_width * 4 / 10)
        window_height = int(screen_height * 3 / 10)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 6)
        self.resize(window_width, window_height)
        self.move(x_position, y_position)
        super().showEvent(a0)

    def fillBeanIfNeed(self) -> None:
        if self.ad is None:
            return
        self.ui.textEdit_text.setPlainText(
            _ad_file_to_str(getattr(self.ad, "text", ""))
        )
        files = getattr(self.ad, "files", []) or []
        if isinstance(files, str):
            files = [files]
        self.ui.textEdit_files.setText(
            "\n".join(str(item) for item in files)
        )
        self.ui.lineEdit_name.setText(str(getattr(self.ad, "name", "") or ""))

    def btnSave(self) -> None:
        text_html = self.ui.textEdit_text.toPlainText().strip()
        if not text_html:
            print("请输入广告文案！")
            return
        ad_file_text = self.ui.textEdit_files.toPlainText().strip()
        legal_files = _obtain_legal_files(ad_file_text)
        if ad_file_text and not legal_files:
            print("输入的媒体文件没有一个是合法的，请检查后重新输入！")
            return
        name = self.ui.lineEdit_name.text().strip()
        if not name:
            print("请输入 广告的名字吧 ！")
            return
        ad = Ad(
            adId=self.adId,
            files=legal_files,
            text=_ad_str_to_file(text_html),
            name=name,
        )
        if callable(self.funBack):
            self.funBack(ad)
        self.close()

    def btnCancel(self) -> None:
        self.close()
