# Recovered module: src.py.com.yun.mao.util.need.QBanYunFlowItemQWidget
from __future__ import annotations

from ._FlowItemWidgetBase import FlowItemWidgetBase


class QBanYunFlowItemQWidget(FlowItemWidgetBase):
    UI_NAME = "q_ban_yun_flow_item_widget.ui"
    TYPE_TEXT = "搬运流"

    def displayRepliesLabel(self):
        data = self.data
        bean = getattr(data, "beanLike", None) or data
        self._set_text("label_replies", f"评论区：{getattr(bean, 'replies_enable', '')}")
        detail = getattr(bean, "replies_info_detail", "")
        self._set_visible("label_replies_detail", bool(detail))
        self._set_text("label_replies_detail", f"评论区详情：{detail}" if detail else "")
        return None

    def updateAutoBeanUI(self):
        super().updateAutoBeanUI()
        self.displayRepliesLabel()
        return None
