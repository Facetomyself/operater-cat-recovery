# Recovered module: src.py.com.yun.mao.tab.mid_api_config_tab
# Telegram API credential editor.  Cache keys and field names are exact.
from __future__ import annotations

from typing import Any

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

from ..config import InnerAppIdConfig, tabl_cache
from ..rm_qh.ps_g2_oq_f1 import be_s4_sk
from ..util.need import ShotUtils, signals, utils
from ..wp_jt.kn_b9_rt_i8 import kn_b9_sk
from .mid_base_tab import MidBaseTab


REGISTER_LINK = "https://my.telegram.org"


def _tip(text: str) -> None:
    try:
        signals.global_ui_signal.tip_dialog_cmd.emit(str(text or ""))
    except Exception:
        print(text)


def _connect(widget: Any, signal_name: str, slot: Any) -> None:
    try:
        signal = getattr(widget, signal_name, None)
        if signal is not None:
            signal.connect(slot)
    except Exception:
        return None


class ApiConfigTab(MidBaseTab):
    def __init__(self, mainWindow: Any, ui: Any) -> None:
        super().__init__()
        self.mainWindow = mainWindow
        self.ui = ui
        self.init()

    def init(self) -> None:
        _connect(
            getattr(self.ui, "btn_save_app_config", None),
            "clicked",
            self.save_app_config,
        )
        _connect(
            getattr(self.ui, "btn_go_to_link", None),
            "clicked",
            self.go_to_link,
        )

        crypto_broken = getattr(
            signals.global_ui_signal, "notify_crypto_ctx_broken", None
        )
        if crypto_broken is not None and callable(be_s4_sk):
            try:
                crypto_broken.connect(be_s4_sk)
            except Exception as exc:
                print("连接加密状态信号失败：", exc)

        marshal_halt = getattr(
            signals.global_ui_signal, "cmd_marshal_pipeline_halt", None
        )
        if marshal_halt is not None and callable(kn_b9_sk):
            try:
                marshal_halt.connect(kn_b9_sk)
            except Exception as exc:
                print("连接流水线信号失败：", exc)

        self.init_api_config()

    def go_to_link(self) -> None:
        biao_shi = ""
        try:
            biao_shi = str(
                tabl_cache.INSTANCE().read_cache(
                    tabl_cache.TEXT_BIAO_SHI,
                    tabl_cache.TEXT_BIAO_SHI_text,
                    "",
                )
                or ""
            )
        except Exception:
            biao_shi = ""
        url = REGISTER_LINK if biao_shi == "开发Debug" else REGISTER_LINK
        QDesktopServices.openUrl(QUrl(url))
        shot = getattr(ShotUtils, "shot", None)
        if callable(shot):
            try:
                shot()
            except Exception:
                return None

    def save_app_config(self) -> None:
        app_id_widget = getattr(self.ui, "lineEdit_api_app_id", None)
        app_hash_widget = getattr(self.ui, "lineEdit_api_app_hash", None)
        app_id = str(app_id_widget.text() if app_id_widget is not None else "").strip()
        app_hash = str(
            app_hash_widget.text() if app_hash_widget is not None else ""
        ).strip()
        if not app_id:
            _tip("请输入app_id")
            return
        if not app_hash:
            _tip("请输入app_hash")
            return
        success, number = utils.parse_int(app_id)
        if not success or number is None:
            _tip("请输入数字!")
            return
        try:
            tabl_cache.INSTANCE().update_cache(
                tabl_cache.API_FUN_TAB,
                tabl_cache.API_FUN_api_id,
                str(number),
            )
            tabl_cache.INSTANCE().update_cache(
                tabl_cache.API_FUN_TAB,
                tabl_cache.API_FUN_api_hash,
                app_hash,
            )
        except Exception as exc:
            _tip("更新失败：" + str(exc))
            return
        if app_id_widget is not None:
            app_id_widget.setText(str(number))
        if app_hash_widget is not None:
            app_hash_widget.setText(app_hash)
        _tip("更新完成！")
        self.init_api_config()

    def init_api_config(self) -> None:
        app_id_widget = getattr(self.ui, "lineEdit_api_app_id", None)
        app_hash_widget = getattr(self.ui, "lineEdit_api_app_hash", None)
        if app_id_widget is not None:
            try:
                app_id_widget.setText(str(InnerAppIdConfig.get_api_id() or ""))
            except Exception:
                app_id_widget.setText("")
        if app_hash_widget is not None:
            try:
                app_hash_widget.setText(str(InnerAppIdConfig.get_api_hash() or ""))
            except Exception:
                app_hash_widget.setText("")


__all__ = ["ApiConfigTab"]
