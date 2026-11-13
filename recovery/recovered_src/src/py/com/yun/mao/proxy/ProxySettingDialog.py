# Recovered module: src.py.com.yun.mao.proxy.ProxySettingDialog
# Behaviour-level reconstruction from Nuitka constants and the UI XML.
from __future__ import annotations

from PyQt5 import QtGui, uic

from ..config import net_config, tabl_cache
from ..config.tabl_cache import (
    PROXY_SETTING_GROUP,
    PROXY_SETTING_ip,
    PROXY_SETTING_port,
)
from ..util import ResourcePath
from ..util.need import utils

try:
    from ..util.need.BaseDialog import BaseDialog
except (ImportError, AttributeError):
    from PyQt5.QtWidgets import QDialog as BaseDialog


class ProxySettingDialog(BaseDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("代理设置")
        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("proxy_setting.ui"),
            self,
        )
        self.ui.text_proxy_ip.setText(net_config.get_ip())
        self.ui.text_proxy_port.setText(net_config.get_port())
        self.ui.btn_proxy_save.clicked.connect(self.proxySave)
        self.ui.btn_proxy_cancel.clicked.connect(self.proxyCancel)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setWindowTitle(self.windowTitle())
        self.setFixedSize(350, 250)

    def proxySave(self) -> None:
        ip = self.ui.text_proxy_ip.text().strip()
        if not ip:
            print("请输入IP！")
            return
        port = self.ui.text_proxy_port.text().strip()
        if not port:
            print("请输入端口！")
            return
        parse_int = getattr(utils, "parse_int", None)
        if callable(parse_int):
            success, int_port = parse_int(port)
        else:
            try:
                int_port = int(port)
                success = True
            except (TypeError, ValueError):
                int_port = 0
                success = False
        if not success:
            print("请正确输入端口！！")
            return
        cache = tabl_cache.INSTANCE()
        update_cache = getattr(cache, "update_cache", None)
        write_cache = getattr(cache, "write_cache", None)
        writer = update_cache if callable(update_cache) else write_cache
        if not callable(writer):
            print("保存失败：缓存接口不可用！")
            return
        writer(
            PROXY_SETTING_GROUP,
            PROXY_SETTING_ip,
            ip,
        )
        writer(
            PROXY_SETTING_GROUP,
            PROXY_SETTING_port,
            int_port,
        )
        print("保存成功！")
        self.close()

    def proxyCancel(self) -> None:
        self.close()
