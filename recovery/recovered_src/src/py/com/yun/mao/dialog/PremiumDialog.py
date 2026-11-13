# Recovered module: src.py.com.yun.mao.dialog.PremiumDialog
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
"""Premium recharge dialog.

inferred: polling cadence, the exact failure-tip branch, and QR logo placement.
"""
from __future__ import annotations

from PyQt5 import uic
from PyQt5.QtCore import QThreadPool, Qt, QTimer
from PyQt5.QtGui import QCloseEvent, QImage, QPixmap
from PyQt5.QtWidgets import QSizePolicy
from PIL import Image
import qrcode
from qrcode.main import QRCode

from ..fea import _sq_jqm
from ..fea._sq_jqm import ABILITY_ENABLE
from ..fea._jc_dd_cz_file import CheckOrderRechargeTask
from ..prices import PriceHtmlUtils
from ..prices.CreateOrderResponseClass import Order
from ..util import ResourcePath
from ..util.EnumClass import HUI_YUAN
from ..util.need import signals, utils
from ..util.need.AllBeanDef import CheckOrderAndRechargeBean
from ..util.need.BaseDialog import BaseDialog
from ..util.need.TipDialog import LARGE_SIZE

from .PremiumExitTipDialog import PremiumExitTipDialog


class PremiumDialog(BaseDialog):
    def __init__(self, parent=None, order: Order | None = None) -> None:
        super().__init__(parent)
        self.poll_count = 0
        self.max_attempts = 20
        self.interval_ms = 10000
        self.is_polling = False
        self.recharge_success = False
        uic.loadUi(ResourcePath.get_ui_path("premium_dialog.ui"), self)
        self.premium_btn_copy_onumber.clicked.connect(self.on_copy_onumber)
        self.premium_btn_copy_address.clicked.connect(self.on_copy_address)
        self.premium_btn_copy_contacts.clicked.connect(self.on_copy_contacts)
        self.premium_btn_copy_ucode.clicked.connect(self.on_copy_ucode)
        self.premium_btn_had_paied.clicked.connect(self.on_had_paied)
        self.order = order or Order()
        signals.global_ui_signal.cmd_check_order_stats.connect(
            self.on_check_order_stats
        )
        self._setup_timer()
        self.display_qr_code(self.order.address)
        self.display_address_amount()
        self.on_log("")

    def close_signals(self) -> None:
        try:
            signals.global_ui_signal.cmd_check_order_stats.disconnect(
                self.on_check_order_stats
            )
        except TypeError:
            return

    def _setup_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.do_poll)

    def on_copy_onumber(self) -> None:
        text_to_copy = str(getattr(self.order, "onumber", "") or "")
        if not utils.copy_text_to_clipboard(text_to_copy):
            print("复制失败，请重试！")
            return
        print("订单号复制成功！")

    def on_copy_address(self) -> None:
        text_to_copy = str(getattr(self.order, "address", "") or "")
        if not utils.copy_text_to_clipboard(text_to_copy):
            print("复制失败，请重试！")
            return
        print("TRC20-USDT地址复制成功！")

    def on_copy_contacts(self) -> None:
        text_to_copy = (
            "https://t.me/"
            + str(_sq_jqm.current_account_info.maoContacts or "").lstrip("@")
        )
        if not utils.copy_text_to_clipboard(text_to_copy):
            print("复制失败，请重试！")
            return
        print("客服联系方式复制成功！")

    def on_copy_ucode(self) -> None:
        text_to_copy = str(_sq_jqm.current_account_info.ucode or "")
        if not utils.copy_text_to_clipboard(text_to_copy):
            print("复制失败，请重试！")
            return
        print("机器码复制成功！")

    def on_had_paied(self) -> None:
        self.start_polling()

    def show_exit_box(self) -> None:
        def close_fun() -> None:
            self.close_signals()
            self.stop_polling()
            self.accept()

        dialog = PremiumExitTipDialog(self, close_fun)
        dialog.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        if not self.recharge_success:
            self.show_exit_box()
            event.ignore()
            return
        self.close_signals()
        self.stop_polling()
        event.accept()

    def reject(self) -> None:
        self.close()

    def display_address_amount(self) -> None:
        html_content = PriceHtmlUtils.get_full_payment_info_html(
            self.order.amount,
            str(_sq_jqm.current_account_info.maoContacts or ""),
        )
        address_html_content = PriceHtmlUtils.get_address_info_html(
            self.order.onumber,
            self.order.amount,
            self.order.address,
        )
        self.set_text_info(self.label_payment_info, html_content)
        self.set_text_info(self.label_address_info, address_html_content)

    def set_text_info(self, label, html_content: str) -> None:
        label.setTextFormat(Qt.RichText)
        label.setText(str(html_content or ""))
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        label.setOpenExternalLinks(True)

    def display_qr_code(self, qr_content: str) -> None:
        qr = QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(qr_content or ""))
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.convert("RGBA")
        qr_img = self.add_tron_usdt_logo(qr_img)
        qr_img_rgb = qr_img.convert("RGB")
        data = qr_img_rgb.tobytes()
        bytes_per_line = 3 * qr_img_rgb.width
        qimage = QImage(
            data,
            qr_img_rgb.width,
            qr_img_rgb.height,
            bytes_per_line,
            QImage.Format_RGB888,
        )
        pixmap = QPixmap.fromImage(qimage)
        self.label_qr_code.setScaledContents(True)
        self.label_qr_code.setAlignment(Qt.AlignCenter)
        target_size = 200
        scaled_pixmap = pixmap.scaled(
            target_size,
            target_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.label_qr_code.setPixmap(scaled_pixmap)
        self.label_qr_code.setFixedSize(200, 200)

    def add_tron_usdt_logo(self, qr_img):
        try:
            logo_path = ResourcePath.get_drawable_path("tether_usdt_logo_256.png")
            logo = Image.open(logo_path)
            logo_size = int(qr_img.size[0] * 0.22)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            pos = (
                (qr_img.size[0] - logo_size) // 2,
                (qr_img.size[1] - logo_size) // 2,
            )
            qr_img.paste(logo, pos, logo)
        except Exception as e:
            _ = e
        return qr_img

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        screen_width, screen_height = utils.get_screen_size()
        window_width = int(screen_width * 5.6 / 10.0)
        window_height = int(screen_height * 12.5 / 20.0)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2) - 30
        self.setFixedSize(window_width, window_height)
        self.move(x_position, y_position)

    def start_polling(self) -> None:
        if self.is_polling:
            return
        self.poll_count = 0
        self.is_polling = True
        self.timer.start(self.interval_ms)

    def stop_polling(self) -> None:
        self.is_polling = False
        self.timer.stop()

    def do_poll(self) -> None:
        if not self.is_polling:
            return
        if self.poll_count >= self.max_attempts:
            self.stop_polling()
            print("达到最大尝试次数，自动停止")
            return
        self.poll_count += 1
        self.premium_lb_lun_xun_stats.setText(
            "正在查询订单，请稍后...轮询次数：" + str(self.poll_count)
        )
        task = CheckOrderRechargeTask(
            CheckOrderAndRechargeBean(
                ucode=str(_sq_jqm.current_account_info.ucode or ""),
                onumber=str(self.order.onumber or ""),
            )
        )
        QThreadPool.globalInstance().start(task)

    def on_log(self, stats) -> None:
        if not stats:
            return
        msg = (
            "没有查询到支付订单！ 订单号： "
            + str(self.order.onumber or "")
            + " 订单描述： "
            + str(self.order.odesc or "")
            + " 应实付： "
            + format(float(self.order.amount or 0), ".3f")
            + "U，请再次点击【我已支付】"
        )
        signals.global_ui_signal.tip_dialog_size_cmd.emit(LARGE_SIZE)
        signals.global_ui_signal.tip_dialog_cmd.emit(
            PriceHtmlUtils.gen_recharge_failed_tip(msg)
        )

    def on_check_order_stats(self, success: bool, content_oj) -> None:
        if not success or not isinstance(content_oj, dict):
            self.on_log(content_oj)
            return
        data = content_oj.get("data", content_oj)
        if not isinstance(data, dict):
            data = content_oj
        grade = data.get("grade", HUI_YUAN)
        endTime = data.get("endRechargeTime", "")
        aiAbility = data.get("aiAbility", 0)
        ai_str = "有AI" if aiAbility == ABILITY_ENABLE else "无AI"
        card_str = _sq_jqm.current_account_info.gen_grade_card_str()
        _ = grade
        tip_str = (
            '\n            <div style="color: #e0e0e0; font-family: Microsoft YaHei, sans-serif; line-height: 1.5; font-size: 12pt;">\n'
            "                恭喜充值成功，<span style=\"color: #4caf50; font-weight: bold; font-size: 16pt\">重启软件</span>即可！<br>\n"
            "                订单号："
            + str(self.order.onumber or "")
            + " <br>\n"
            "                卡类型："
            + str(card_str)
            + " "
            + str(ai_str)
            + '<br>\n'
            '                有效期至：<span style="color: #ffeb3b; font-weight: bold;">'
            + str(endTime)
            + "</span> <br>\n"
            "            </div>\n"
            "            "
        )
        print(
            "恭喜充值成功，订单号： "
            + str(self.order.onumber or "")
            + " 已实付： "
            + format(float(self.order.amount or 0), ".3f")
            + "U ；卡类型： "
            + str(card_str)
            + " 有效期至： "
            + str(endTime)
        )
        signals.global_ui_signal.tip_dialog_cmd.emit(tip_str)
        signals.global_ui_signal.tip_dialog_restart_cmd.emit(LARGE_SIZE)
        self.recharge_success = True
        self.close()
