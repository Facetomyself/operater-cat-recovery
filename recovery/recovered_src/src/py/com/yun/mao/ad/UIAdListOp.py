# Recovered module: src.py.com.yun.mao.ad.UIAdListOp
# Behaviour-level reconstruction from Nuitka constants and signatures.
from __future__ import annotations

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from ..dclass.DTopClass import Ad


class UIAdListOp:
    @staticmethod
    def fillAd2List(adList: list[Ad], qlist_view: QListWidget) -> None:
        qlist_view.clear()
        for ad in adList or []:
            text = getattr(ad, "name", "")
            list_item = QListWidgetItem(str(text))
            list_item.setData(32, ad)
            list_item.setSizeHint(QSize(200, 50))
            qlist_view.addItem(list_item)
        qlist_view.update()
