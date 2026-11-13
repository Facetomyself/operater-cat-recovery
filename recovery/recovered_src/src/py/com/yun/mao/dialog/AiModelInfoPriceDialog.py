# Recovered module: src.py.com.yun.mao.dialog.AiModelInfoPriceDialog
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy

from ..fea import _sq_jqm
from ..prices import AiModelInfoGenHelper
from ..util import ResourcePath
from ..util.need import utils
from ..util.need.BaseDialog import BaseDialog


class AiModelInfoPriceDialog(BaseDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        uic.loadUi(ResourcePath.get_ui_path("ai_model_info_price.ui"), self)
        self.btn_premium_i_know.clicked.connect(self.on_close)
        self.label_model_info_show.setText(
            AiModelInfoGenHelper.create_model_price_table(
                _sq_jqm.current_account_info.modelList
            )
        )
        self.label_model_info_show.setWordWrap(True)
        self.label_model_info_show.setTextFormat(Qt.RichText)
        self.label_model_info_show.setAlignment(Qt.AlignCenter)
        self.label_model_info_show.setStyleSheet(
            "QLabel { background: transparent; }"
        )
        self.label_model_info_show.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

    def on_close(self) -> None:
        self.close()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        screen_width, screen_height = utils.get_screen_size()
        window_width = int(screen_width * 4.0 / 10.0)
        window_height = int(screen_height * 8.0 / 20.0)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2) - 30
        self.setFixedSize(window_width, window_height)
        self.move(x_position, y_position)
