# Recovered module: src.py.com.yun.mao.util.need.QDownLoadFlowItemQWidget
from __future__ import annotations

from ._FlowItemWidgetBase import FlowItemWidgetBase


class QDownLoadFlowItemQWidget(FlowItemWidgetBase):
    UI_NAME = "q_down_load_flow_item_widget.ui"
    TYPE_TEXT = "下载流"

    def updateAutoBeanUI(self):
        super().updateAutoBeanUI()
        data = self.data
        bean = getattr(data, "beanLike", None) or data
        contain = getattr(bean, "containWords", "")
        exclude = getattr(bean, "excludeWords", "")
        self._set_text("dl_label_filter_max", getattr(bean, "baseFilter", ""))
        self._set_text("dl_label_filter_words", f"包含词为：{contain}，排除词为：{exclude}")
        water = getattr(bean, "water", None)
        self._set_text("dl_label_water_desc", "没开启水印" if not water else "")
        return None
