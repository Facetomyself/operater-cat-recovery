# Recovered module: src.py.com.yun.mao.util.need.QYunAutoItemQWidget
from __future__ import annotations

from ._FlowItemWidgetBase import FlowItemWidgetBase


class QYunAutoItemQWidget(FlowItemWidgetBase):
    UI_NAME = "q_yun_auto_item_widget.ui"
    TYPE_TEXT = "云自动"

    def updateAutoBeanUI(self):
        super().updateAutoBeanUI()
        data = self.data
        bean = getattr(data, "beanLike", None) or data
        self._set_text("label_dest", f"云仓库：{getattr(bean, 'db_channel', '')}")
        return None
