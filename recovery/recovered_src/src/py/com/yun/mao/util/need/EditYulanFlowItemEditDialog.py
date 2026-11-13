# Recovered module: src.py.com.yun.mao.util.need.EditYulanFlowItemEditDialog
# Behaviour-level reconstruction from Nuitka constants, source signatures and
# offline Hex-Rays.  Preview resources are stored in ``yulan_destes``.
from __future__ import annotations

from .EditAutoFlowItemEditDialog import (
    MODE_RANDOM_TEXT,
    MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
    WATER_MODE_PIC,
    _FlowEditorMixin,
)
from .BaseDialog import BaseDialog
from ...dclass.DTopClass import AUTO_BEAN_TYPE_YU_LAN_FLOW, YuLanBean


class EditYulanFlowItemEditDialog(_FlowEditorMixin, BaseDialog):
    FORM_TITLE = "编辑预览流"
    UI_MODULE = "src.resource.ui.dyna.yulan_flow_item"
    BEAN_CLASS = YuLanBean
    AUTO_TYPE = AUTO_BEAN_TYPE_YU_LAN_FLOW
    BEAN_ATTR = "yulanbean"
    WINDOW_RATIO = (9, 20, 6, 10)

    SAVE_BUTTON = "btn_save_yulan_item"
    ITEM_NAME_FIELD = "lineEdit_yulan_item_name"
    SOURCE_FIELD = "lineEdit_yulan_source"
    PREVIEW_DEST_FIELD = "textEdit_yulan_yulan_dest_list"
    PRIORITY_FIELD = "lineEdit_priority"

    MODE_COMBO = "comboBox_yulan_select_mode"
    UNIT_COMBO = "comboBox_yulan_number_dan_wei"
    RANDOM_UNIT_COMBO = "comboBox_yulan_number_random_dan_wei"
    RANDOM_COUNT_FIELD = "lineEdit_yulan_random_want_count"
    INCREASE_START_FIELD = "lineEdit_yulan_increase_start_id"
    INCREASE_COUNT_FIELD = "lineEdit_yulan_increase_want_count"
    LOOP_START_FIELD = "lineEdit_yulan_loop_start_id"
    LOOP_END_FIELD = "lineEdit_yulan_loop_end_id"
    MODEL_FIELD = "text_model"
    NUMBER_MODEL_FIELD = "number_model"

    DURATION_MIN_FIELD = "lineEdit_yulan_duration_min"
    DURATION_MAX_FIELD = "lineEdit_yulan_duration_max"
    SIZE_MIN_FIELD = "lineEdit_yulan_mb_min"
    SIZE_MAX_FIELD = "lineEdit_yulan_mb_max"
    WORDS_CONTAIN_FIELD = "lineEdit_yulan_fliter_words_contain"
    WORDS_EXCLUDE_FIELD = "lineEdit_yulan_fliter_words_exclude"
    TAIL_FIELD = "textEdit_yulan_tail_text"
    REPLACE_FIELD = "textEdit_yulan_replace_rule"
    RESOURCE_FIELDS = {
        "video_photo": "checkBox_yulan_video_photo",
        "photo": "checkBox_yulan_photo",
        "video": "checkBox_yulan_video",
        "file": "checkBox_yulan_file",
        "text": "checkBox_yulan_text",
    }
    CHAI_ZU_CHECK = "checkBox_chai_zu"
    KEEP_SOURCE_CHECK = "cb_yulan_origin_source_text"
    AD_ENABLE_CHECK = "cb_yulan_ad_enable"

    AD_LIST = "listWidget_yulan_private_ad_list"
    AD_ADD_BUTTON = "btn_yulan_add_ad"
    AI_BUTTON = "btn_yulan_select_ai_em"
    AI_CHECK = "checkBox_yulan_ai_enable"
    AI_GROUP = "horizontalGroupBox_ai_yulan"
    AI_LABEL = "label_yulan_ai_name"
    AI_SKIP_RADIO = "radioButton_ai_yulan_skip_source"
    AI_USE_RADIO = "radioButton_ai_yulan_use_source"

    WATER_MODE_COMBO = "cb_yulan_water_mode"
    WATER_PATH_LABEL = "label_yulan_water_pic_path"
    WATER_SELECT_BUTTON = "btn_yulan_water_select_pic"
    WATER_RATIO_FIELD = "line_edit_yulan_flow_water_pic_ratio"
    WATER_TEXT_FIELD = "lineEdit_cb_water_text"
    WATER_PIC_CHECK = "cb_yulan_pic_water"
    WATER_VIDEO_CHECK = "cb_yulan_video_water"
    WATER_DURATION_COMBO = "cb_yulan_video_minute"

    ACTION_AUTO_RADIO = "radioButton_yulan_action_auto"
    ACTION_DOWNLOAD_RADIO = "radioButton_yulan_action_download"
    ACTION_SLEEP_MIN_FIELD = "lineEdit_yulan_sleep_min"
    ACTION_SLEEP_MAX_FIELD = "lineEdit_yulan_sleep_max"

    RESOP_BLUR_CHECK = "cb_yulan_pic_blur"
    RESOP_SPOILER_CHECK = "cb_yulan_spoiler"
    RESOP_RADIUS_FIELD = "yulan_pic_blur_radius"

    GRID_FIELD = "lineEdit_yulan_grid_number"
    GRID_COVER_FIELD = "cb_yulan_random_cover"

    YULAN_MODE_COMBO = "comboBox_yulan_select_yulan_mode"
    YULAN_RADIOS = (
        "radioButton_yulan_10",
        "radioButton_yulan_20",
        "radioButton_yulan_30",
        "radioButton_yulan_customer",
    )
    YULAN_CUSTOM_RADIO = "radioButton_yulan_customer"
    YULAN_CUSTOM_FIELD = "lineEdit_yulan_customer"
    YULAN_MIN_FIELD = "lineEdit_yulan_min_duration"
    YULAN_MAX_FIELD = "lineEdit_yulan_max_duration"

    HUIYUAN_ENABLE_CHECK = "cb_yulan_hui_yuan_link"
    HUIYUAN_TEXT_FIELD = "lineEdit_yulan_hui_yuan_tip_text"
    HUIYUAN_CUSTOMER_CHECK = "cb_yulan_hui_yuan_customer_link"
    HUIYUAN_LINK_FIELD = "lineEdit_yulan_hui_yuan_tip_text_link"
    HUIYUAN_BQ_CHECK = "cb_yulan_hui_yuan_link_bq"
    YOUKE_ENABLE_CHECK = "cb_yulan_you_ke_link"
    YOUKE_TEXT_FIELD = "lineEdit_yulan_you_ke_tip_text"
    YOUKE_LINK_FIELD = "lineEdit_yulan_you_ke_tip_text_link"
    YOUKE_BQ_CHECK = "cb_yulan_you_ke_link_bq"

    ADD_DURATION_CHECK = "checkBox_yulan_add_duration_info"
    ADD_DURATION_BQ_CHECK = "checkBox_yulan_add_duration_info_bq"

    RESOURCE_TUTORIAL_BUTTON = "yulan_res_btn_jiao_chen"
    RESOP_TUTORIAL_BUTTON = "btn_yulan_res_op_jiao_chen"
    ACTION_TUTORIAL_BUTTON = "btn_yulan_action_jiao_chen"
    TOPIC_TUTORIAL_BUTTON = "yulan_topic_jiao_chen"
    PIC_WATER_TUTORIAL_BUTTON = "btn_yulan_water_pic_jiao_chen"
    GRID_TUTORIAL_BUTTON = "btn_yulan_grid_jiao_chen"
    COVER_TUTORIAL_BUTTON = "yulan_cover_jiao_chen"
    HUIYUAN_TUTORIAL_BUTTON = "btn_yulan_hui_yuan_link_jc"
    YOUKE_TUTORIAL_BUTTON = "btn_yulan_you_ke_link_jc"
    RES_OP_COURSE = "unifyShowPublishResOpCourse"
    ACTION_COURSE = "unifyShowYulanFlowBanYunTypeCourse"
    TOPIC_COURSE = "unifyShowTopicCourse"

    SAVE_EDIT_MESSAGE = "更新预览流成功！"
    SAVE_ADD_MESSAGE = "添加预览流成功！"
    DEFAULT_TEXTS = {
        "lineEdit_priority": "100",
        "lineEdit_yulan_sleep_min": "3",
        "lineEdit_yulan_sleep_max": "5",
        "lineEdit_yulan_min_duration": "60",
        "lineEdit_yulan_max_duration": "120",
        "line_edit_yulan_flow_water_pic_ratio": "30",
        "lineEdit_yulan_grid_number": "6",
        "lineEdit_yulan_hui_yuan_tip_text": "💋会员点我看完整版",
        "lineEdit_yulan_you_ke_tip_text": "😍游客点我上车",
    }
    DEFAULT_CHECKS = {
        "checkBox_yulan_video_photo": True,
        "checkBox_yulan_photo": True,
        "checkBox_yulan_video": True,
        "checkBox_yulan_file": True,
        "checkBox_yulan_text": True,
        "cb_yulan_origin_source_text": True,
        "cb_yulan_ad_enable": True,
        "radioButton_yulan_action_auto": True,
        "radioButton_ai_yulan_skip_source": True,
        "radioButton_yulan_10": True,
        "cb_yulan_hui_yuan_link_bq": True,
        "cb_yulan_you_ke_link_bq": True,
        "checkBox_yulan_add_duration_info_bq": True,
    }
    DEFAULT_COMBOS = {
        "comboBox_yulan_select_mode": MODE_RANDOM_TEXT,
        "comboBox_yulan_number_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "comboBox_yulan_number_random_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "cb_yulan_water_mode": WATER_MODE_PIC,
        "comboBox_yulan_select_yulan_mode": "按比例模式",
    }

    WIDGET_NAMES = (
        "btn_yulan_hui_yuan_link_jc",
        "btn_yulan_you_ke_link_jc",
        "btn_show_duration_dialog",
        "yulan_res_btn_jiao_chen",
        "btn_yulan_res_op_jiao_chen",
        "btn_yulan_action_jiao_chen",
        "yulan_topic_jiao_chen",
        "btn_yulan_select_ai_em",
        "btn_yulan_water_pic_jiao_chen",
        "btn_yulan_water_select_pic",
        "btn_yulan_grid_jiao_chen",
        "yulan_cover_jiao_chen",
        "btn_save_yulan_item",
        "btn_yulan_add_ad",
        "comboBox_yulan_number_dan_wei",
        "comboBox_yulan_number_random_dan_wei",
        "comboBox_yulan_select_mode",
        "comboBox_yulan_select_yulan_mode",
        "cb_yulan_water_mode",
        "listWidget_yulan_private_ad_list",
        "cb_yulan_origin_source_text",
        "cb_yulan_ad_enable",
        "cb_yulan_hui_yuan_link",
        "lineEdit_yulan_hui_yuan_tip_text",
        "cb_yulan_hui_yuan_customer_link",
        "lineEdit_yulan_hui_yuan_tip_text_link",
        "cb_yulan_you_ke_link",
        "lineEdit_yulan_you_ke_tip_text",
        "lineEdit_yulan_you_ke_tip_text_link",
        "radioButton_yulan_10",
        "radioButton_yulan_20",
        "radioButton_yulan_30",
        "radioButton_yulan_customer",
        "checkBox_yulan_video_photo",
        "checkBox_pb_yulan_video",
        "checkBox_yulan_ai_enable",
        "horizontalGroupBox_ai_yulan",
        "label_yulan_ai_name",
        "lineEdit_yulan_customer",
        "yulan_qu",
        "yulan_qu_wrapper",
        "checkBox_chai_zu",
        "checkBox_yulan_photo",
        "checkBox_yulan_video",
        "checkBox_yulan_file",
        "checkBox_yulan_text",
        "cb_yulan_dele_source_text",
        "cb_yulan_dele_link",
        "cb_yulan_fliter_button",
        "checkBox_discard_no_text_resource",
        "checkBox_pb_yulan_picture",
        "checkBox_yulan_add_duration_info_bq",
        "checkBox_yulan_add_duration_info",
        "lineEdit_yulan_random_want_count",
        "lineEdit_yulan_increase_start_id",
        "lineEdit_yulan_increase_want_count",
        "lineEdit_yulan_duration_min",
        "lineEdit_yulan_duration_max",
        "lineEdit_yulan_mb_min",
        "lineEdit_yulan_mb_max",
        "lineEdit_yulan_min_duration",
        "lineEdit_yulan_max_duration",
        "lineEdit_yulan_sleep_min",
        "lineEdit_yulan_sleep_max",
        "lineEdit_yulan_fliter_words_contain",
        "lineEdit_yulan_fliter_words_exclude",
        "lineEdit_yulan_loop_start_id",
        "lineEdit_yulan_loop_end_id",
        "lineEdit_yulan_source",
        "lineEdit_yulan_item_name",
        "lineEdit_yulan_grid_number",
        "line_edit_yulan_flow_water_pic_ratio",
        "lineEdit_cb_water_text",
        "lineEdit_priority",
        "radioButton_yulan_action_auto",
        "radioButton_yulan_action_download",
        "radioButton_ai_yulan_skip_source",
        "radioButton_ai_yulan_use_source",
        "label_yulan_water_pic_path",
        "text_water_wrapper",
        "pic_water_wrapper",
        "text_model",
        "number_model",
        "yulan_text_model",
        "textEdit_yulan_yulan_dest_list",
        "textEdit_yulan_tail_text",
        "textEdit_yulan_replace_rule",
        "cb_yulan_pic_water",
        "cb_yulan_video_water",
        "cb_yulan_video_minute",
        "cb_yulan_spoiler",
        "cb_yulan_pic_blur",
        "cb_yulan_random_cover",
        "cb_yulan_ad_is_bottom_up",
        "cb_yulan_ad_delete",
        "cb_yulan_hui_yuan_link_bq",
        "cb_yulan_you_ke_link_bq",
        "yulan_pic_blur_radius",
        "present_container",
        "duration_container",
        "random_com",
        "increase_com",
        "loop_com",
    )

    def __init__(
        self,
        parent=None,
        windowTitle: str | None = None,
        autobean=None,
        isCopy: bool = False,
        employee_id=None,
    ) -> None:
        super().__init__(parent, windowTitle, autobean, isCopy, employee_id)

    def _name_required_message(self) -> str:
        return "请给自动流取一个名字吧，方便你后续管理！"


__all__ = ["EditYulanFlowItemEditDialog"]
