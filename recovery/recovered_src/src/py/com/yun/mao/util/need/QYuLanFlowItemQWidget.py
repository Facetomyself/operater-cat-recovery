# Recovered module: src.py.com.yun.mao.util.need.QYuLanFlowItemQWidget
from __future__ import annotations

from ._FlowItemWidgetBase import FlowItemWidgetBase


class QYuLanFlowItemQWidget(FlowItemWidgetBase):
    UI_NAME = "q_yu_lan_flow_item_widget.ui"
    TYPE_TEXT = "预览流"

    def displayActionLabel(self):
        return FlowItemWidgetBase.displayActionLabel(self)
