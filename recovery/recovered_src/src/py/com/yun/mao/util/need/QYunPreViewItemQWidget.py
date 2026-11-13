# Recovered module: src.py.com.yun.mao.util.need.QYunPreViewItemQWidget
from __future__ import annotations

from ._FlowItemWidgetBase import FlowItemWidgetBase


class QYunPreViewItemQWidget(FlowItemWidgetBase):
    UI_NAME = "q_yun_preview_item_widget.ui"
    TYPE_TEXT = "云预览"

    def updateAutoBeanUI(self):
        super().updateAutoBeanUI()
        data = self.data
        bean = getattr(data, "beanLike", None) or data
        self._set_text("label_dest", f"云仓库：{getattr(bean, 'source', '')}")
        return None
