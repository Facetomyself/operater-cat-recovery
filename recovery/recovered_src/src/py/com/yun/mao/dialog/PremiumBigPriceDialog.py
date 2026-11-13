# Recovered module: src.py.com.yun.mao.dialog.PremiumBigPriceDialog
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

from PyQt5 import uic
from PyQt5.QtCore import Qt

from ..fea import _sq_jqm
from ..prices import PriceTableBiggerTextHelper
from ..util import ResourcePath
from ..util.need import utils
from ..util.need.BaseDialog import BaseDialog


class PremiumBigPriceDialog(BaseDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        uic.loadUi(ResourcePath.get_ui_path("premium_price_big_dialog.ui"), self)
        self.btn_premium_i_know.clicked.connect(self.on_close)
        current_prices = _sq_jqm.current_account_info.get_price_config()
        self.label_price_big_show.setText(
            PriceTableBiggerTextHelper.get_subscription_bigger_html_dark(
                current_prices
            )
        )
        self.label_price_big_show.setWordWrap(True)
        self.label_price_big_show.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label_price_big_show.setStyleSheet(
            "QLabel { background: transparent; }"
        )

    def on_close(self) -> None:
        self.close()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        screen_width, screen_height = utils.get_screen_size()
        window_width = int(screen_width * 4.0 / 10.0)
        window_height = int(screen_height * 15.0 / 20.0)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2) - 30
        self.setFixedSize(window_width, window_height)
        self.move(x_position, y_position)
