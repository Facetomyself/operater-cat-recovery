# Recovered module: src.py.com.yun.mao.util.need.EditDownLoadItemEditDialog
# Behaviour-level reconstruction from Nuitka constants, source signatures and
# offline Hex-Rays.  This dialog only exposes source, type, mode, filters and
# watermark controls; target/channel publishing fields are intentionally absent.
from __future__ import annotations

from .EditAutoFlowItemEditDialog import (
    MODE_RANDOM_TEXT,
    MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
    WATER_MODE_PIC,
    _FlowEditorMixin,
)
from .BaseDialog import BaseDialog
from ...dclass.DTopClass import AUTO_BEAN_TYPE_DOWN_LOAD_FLOW, DownLoadBean


class EditDownLoadItemEditDialog(_FlowEditorMixin, BaseDialog):
    FORM_TITLE = "编辑下载流"
    UI_MODULE = "src.resource.ui.dyna.down_load_flow_item"
    BEAN_CLASS = DownLoadBean
    AUTO_TYPE = AUTO_BEAN_TYPE_DOWN_LOAD_FLOW
    BEAN_ATTR = "downloadbean"
    WINDOW_RATIO = (3, 7, 6, 14)

    SAVE_BUTTON = "btn_save_dl_item"
    ITEM_NAME_FIELD = "lineEdit_dl_name"
    SOURCE_FIELD = "dl_lineEdit_source"
    PRIORITY_FIELD = "lineEdit_priority"

    MODE_COMBO = "dl_comboBox_select_mode"
    UNIT_COMBO = "dl_comboBox_number_dan_wei"
    RANDOM_UNIT_COMBO = "dl_comboBox_number_random_dan_wei"
    RANDOM_COUNT_FIELD = "dl_lineEdit_random_want_count"
    INCREASE_START_FIELD = "dl_lineEdit_increase_start_id"
    INCREASE_COUNT_FIELD = "dl_lineEdit_increase_want_count"
    LOOP_START_FIELD = "dl_lineEdit_loop_start_id"
    LOOP_END_FIELD = "dl_lineEdit_loop_end_id"
    MODEL_FIELD = "text_model"
    NUMBER_MODEL_FIELD = "number_model"

    DURATION_MIN_FIELD = "lineEdit_down_load_duration_min"
    DURATION_MAX_FIELD = "lineEdit_down_load_duration_max"
    SIZE_MIN_FIELD = "lineEdit_down_load_mb_min"
    SIZE_MAX_FIELD = "lineEdit_down_load_mb_max"
    RESOURCE_FIELDS = {
        "video_photo": "dl_checkBox_video_photo",
        "photo": "dl_checkBox_photo",
        "video": "dl_checkBox_video",
        "file": "dl_checkBox_file",
    }

    WATER_MODE_COMBO = "cb_dl_water_mode"
    WATER_PATH_LABEL = "label_dl_water_pic_path"
    WATER_SELECT_BUTTON = "btn_dl_water_select_pic"
    WATER_RATIO_FIELD = "line_edit_dl_water_pic_ratio"
    WATER_TEXT_FIELD = "dl_lineEdit_water_text"
    WATER_PIC_CHECK = "dl_checkBox_pic_water"
    WATER_VIDEO_CHECK = "dl_checkBox_video_water"
    WATER_DURATION_COMBO = "dl_comboBox_video_minute"
    RANDOM_WRAPPER = "dl_random_com"
    INCREASE_WRAPPER = "dl_increase_com"
    LOOP_WRAPPER = "dl_loop_com"

    RESOURCE_TUTORIAL_BUTTON = "down_load_res_btn_jiao_chen"
    TOPIC_TUTORIAL_BUTTON = "down_load_topic_jiao_chen"
    PIC_WATER_TUTORIAL_BUTTON = "btn_dl_water_pic_jiao_chen"
    TOPIC_COURSE = "unifyShowTopicCourse"

    SAVE_EDIT_MESSAGE = "更新下载流成功！"
    SAVE_ADD_MESSAGE = "添加下载流成功！"
    DEFAULT_TEXTS = {
        "lineEdit_priority": "100",
        "line_edit_dl_water_pic_ratio": "30",
        "dl_lineEdit_random_want_count": "10",
        "dl_lineEdit_increase_start_id": "0",
    }
    DEFAULT_CHECKS = {
        "dl_checkBox_video_photo": True,
        "dl_checkBox_photo": True,
        "dl_checkBox_video": True,
        "dl_checkBox_file": True,
    }
    DEFAULT_COMBOS = {
        "dl_comboBox_select_mode": MODE_RANDOM_TEXT,
        "dl_comboBox_number_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "dl_comboBox_number_random_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "cb_dl_water_mode": WATER_MODE_PIC,
    }

    WIDGET_NAMES = (
        "btn_save_dl_item",
        "btn_dl_water_pic_jiao_chen",
        "btn_dl_water_select_pic",
        "down_load_res_btn_jiao_chen",
        "down_load_topic_jiao_chen",
        "label_dl_water_pic_path",
        "dl_lineEdit_source",
        "dl_lineEdit_random_want_count",
        "dl_lineEdit_increase_start_id",
        "dl_lineEdit_increase_want_count",
        "dl_lineEdit_loop_start_id",
        "dl_lineEdit_loop_end_id",
        "dl_lineEdit_fliter_words_contain",
        "dl_lineEdit_fliter_words_exclude",
        "dl_lineEdit_water_text",
        "lineEdit_dl_name",
        "dl_checkBox_video_photo",
        "dl_checkBox_photo",
        "dl_checkBox_video",
        "dl_checkBox_file",
        "dl_checkBox_pic_water",
        "dl_checkBox_video_water",
        "dl_comboBox_select_mode",
        "dl_comboBox_number_dan_wei",
        "dl_comboBox_number_random_dan_wei",
        "dl_comboBox_video_minute",
        "cb_dl_water_mode",
        "lineEdit_down_load_duration_min",
        "lineEdit_down_load_duration_max",
        "lineEdit_down_load_mb_min",
        "lineEdit_down_load_mb_max",
        "lineEdit_priority",
        "line_edit_dl_water_pic_ratio",
        "text_model",
        "number_model",
        "text_water_wrapper",
        "pic_water_wrapper",
        "dl_random_com",
        "dl_increase_com",
        "dl_loop_com",
    )

    def __init__(
        self,
        parent=None,
        windowTitle: str | None = None,
        autobean=None,
        isCopy: bool = False,
    ) -> None:
        super().__init__(parent, windowTitle, autobean, isCopy, None)

    def _name_required_message(self) -> str:
        return "请给下载流取一个名字吧，方便你后续管理！"


__all__ = ["EditDownLoadItemEditDialog"]
