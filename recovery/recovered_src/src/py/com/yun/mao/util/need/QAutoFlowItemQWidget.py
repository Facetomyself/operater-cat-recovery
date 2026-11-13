# Recovered module: src.py.com.yun.mao.util.need.QAutoFlowItemQWidget
from __future__ import annotations

from ._FlowItemWidgetBase import FlowItemWidgetBase


class QAutoFlowItemQWidget(FlowItemWidgetBase):
    UI_NAME = "q_auto_flow_item_widget.ui"
    TYPE_TEXT = "自动流"

    def displayActionLabel(self):
        return FlowItemWidgetBase.displayActionLabel(self)
