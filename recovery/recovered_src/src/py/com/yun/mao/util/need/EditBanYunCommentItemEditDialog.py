# Recovered module: src.py.com.yun.mao.util.need.EditBanYunCommentItemEditDialog
# Behaviour-level reconstruction from Nuitka constants, source signatures and
# offline Hex-Rays.  The form is instantiated only when a dialog is created.
from __future__ import annotations

from .EditAutoFlowItemEditDialog import (
    MODE_RANDOM_TEXT,
    MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
    WATER_MODE_PIC,
    _FlowEditorMixin,
)
from .BaseDialog import BaseDialog
from ...dclass.DTopClass import AUTO_BEAN_TYPE_BAN_YUN, BanYunBean


class EditBanYunCommentItemEditDialog(_FlowEditorMixin, BaseDialog):
    FORM_TITLE = "编辑搬运流"
    UI_MODULE = "src.resource.ui.dyna.ban_yun_flow_comment_item"
    BEAN_CLASS = BanYunBean
    AUTO_TYPE = AUTO_BEAN_TYPE_BAN_YUN
    BEAN_ATTR = "banyunbean"
    WINDOW_RATIO = (3, 6, 10, 20)

    SAVE_BUTTON = "btn_save_yun_yin_item"
    ITEM_NAME_FIELD = "lineEdit_yun_yin_name"
    SOURCE_FIELD = "lineEdit_source"
    DEST_FIELD = "textEdit_dest_list"
    PRIORITY_FIELD = "lineEdit_priority"

    MODE_COMBO = "comboBox_select_mode"
    UNIT_COMBO = "comboBox_number_dan_wei"
    RANDOM_UNIT_COMBO = "comboBox_number_random_dan_wei"
    RANDOM_COUNT_FIELD = "lineEdit_random_want_count"
    INCREASE_START_FIELD = "lineEdit_increase_start_id"
    INCREASE_COUNT_FIELD = "lineEdit_increase_want_count"
    LOOP_START_FIELD = "lineEdit_loop_start_id"
    LOOP_END_FIELD = "lineEdit_loop_end_id"
    MODEL_FIELD = "text_model"
    NUMBER_MODEL_FIELD = "number_model"

    DURATION_MIN_FIELD = "lineEdit_ban_yun_duration_min"
    DURATION_MAX_FIELD = "lineEdit_ban_yun_duration_max"
    SIZE_MIN_FIELD = "lineEdit_ban_yun_mb_min"
    SIZE_MAX_FIELD = "lineEdit_ban_yun_mb_max"
    WORDS_CONTAIN_FIELD = "lineEdit_fliter_words_contain"
    WORDS_EXCLUDE_FIELD = "lineEdit_fliter_words_exclude"
    TAIL_FIELD = "textEdit_tail_text"
    REPLACE_FIELD = "textEdit_replace_rule"
    RESOURCE_FIELDS = {
        "video_photo": "checkBox_video_photo",
        "photo": "checkBox_photo",
        "video": "checkBox_video",
        "file": "checkBox_file",
        "text": "checkBox_text",
    }
    CHAI_ZU_CHECK = "checkBox_chai_zu"
    KEEP_SOURCE_CHECK = "checkBox_origin_source_text"
    AD_ENABLE_CHECK = "checkBox_ad_enable"

    AD_LIST = "listWidget_private_ad_list"
    AD_ADD_BUTTON = "btn_add_ad"
    AI_BUTTON = "btn_banyun_select_ai_em"
    AI_CHECK = "checkBox_banyun_ai_enable"
    AI_GROUP = "horizontalGroupBox_ai_banyun"
    AI_LABEL = "label_banyun_ai_name"
    AI_SKIP_RADIO = "radioButton_ai_banyun_skip_source"
    AI_USE_RADIO = "radioButton_ai_banyun_use_source"

    WATER_MODE_COMBO = "cb_banyun_water_mode"
    WATER_PATH_LABEL = "label_banyun_water_pic_path"
    WATER_SELECT_BUTTON = "btn_banyun_water_select_pic"
    WATER_RATIO_FIELD = "line_edit_by_com_water_pic_ratio"
    WATER_TEXT_FIELD = "lineEdit_water_text"
    WATER_PIC_CHECK = "checkBox_pic_water"
    WATER_VIDEO_CHECK = "checkBox_video_water"
    WATER_DURATION_COMBO = "comboBox_video_minute"

    ACTION_AUTO_RADIO = "radioButton_action_auto"
    ACTION_DOWNLOAD_RADIO = "radioButton_action_download"
    ACTION_SLEEP_MIN_FIELD = "lineEdit_auto_sleep_min"
    ACTION_SLEEP_MAX_FIELD = "lineEdit_auto_sleep_max"

    RESOP_BLUR_CHECK = "cb_ban_yun_pic_blur"
    RESOP_SPOILER_CHECK = "cb_ban_yun_spoiler"
    RESOP_RADIUS_FIELD = "ban_yun_pic_blur_radius"

    GRID_FIELD = "lineEdit_ban_yun_grid_number"
    GRID_COVER_FIELD = "cb_ban_yun_random_cover"

    COPY_COMMENT_CHECK = "checkBox_copy_comment"
    COMMENT_CONFIG_BUTTON = "btn_config_comment_rule"

    RESOURCE_TUTORIAL_BUTTON = "ban_yun_res_btn_jiao_chen"
    RESOP_TUTORIAL_BUTTON = "btn_ban_yun_res_op_jiao_chen"
    TOPIC_TUTORIAL_BUTTON = "ban_yun_topic_jiao_chen"
    PIC_WATER_TUTORIAL_BUTTON = "btn_banyun_water_pic_jiao_chen"
    GRID_TUTORIAL_BUTTON = "btn_ban_yun_grid_jiao_chen"
    COVER_TUTORIAL_BUTTON = "ban_yun_cover_jiao_chen"
    RES_OP_COURSE = "unifyShowPublishResOpCourse"
    ACTION_COURSE = "unifyShowAutoFlowBanYunTypeCourse"
    TOPIC_COURSE = "unifyShowTopicCourse"

    SAVE_EDIT_MESSAGE = "更新搬运流成功！"
    SAVE_ADD_MESSAGE = "添加搬运流成功！"
    DEFAULT_TEXTS = {
        "lineEdit_priority": "100",
        "lineEdit_auto_sleep_min": "3",
        "lineEdit_auto_sleep_max": "5",
        "line_edit_by_com_water_pic_ratio": "30",
        "lineEdit_ban_yun_grid_number": "6",
    }
    DEFAULT_CHECKS = {
        "checkBox_video_photo": True,
        "checkBox_photo": True,
        "checkBox_video": True,
        "checkBox_file": True,
        "checkBox_text": True,
        "checkBox_origin_source_text": True,
        "checkBox_ad_enable": True,
        "radioButton_action_auto": True,
        "radioButton_ai_banyun_skip_source": True,
    }
    DEFAULT_COMBOS = {
        "comboBox_select_mode": MODE_RANDOM_TEXT,
        "comboBox_number_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "comboBox_number_random_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "cb_banyun_water_mode": WATER_MODE_PIC,
    }

    WIDGET_NAMES = (
        "btn_save_yun_yin_item",
        "btn_add_ad",
        "btn_config_comment_rule",
        "ban_yun_res_btn_jiao_chen",
        "btn_ban_yun_res_op_jiao_chen",
        "ban_yun_topic_jiao_chen",
        "btn_banyun_select_ai_em",
        "btn_banyun_water_pic_jiao_chen",
        "btn_banyun_water_select_pic",
        "btn_ban_yun_grid_jiao_chen",
        "ban_yun_cover_jiao_chen",
        "comboBox_number_dan_wei",
        "comboBox_number_random_dan_wei",
        "comboBox_select_mode",
        "cb_banyun_water_mode",
        "listWidget_private_ad_list",
        "checkBox_chai_zu",
        "checkBox_origin_source_text",
        "checkBox_ad_enable",
        "checkBox_copy_comment",
        "checkBox_video_photo",
        "checkBox_banyun_ai_enable",
        "horizontalGroupBox_ai_banyun",
        "label_banyun_ai_name",
        "checkBox_photo",
        "checkBox_video",
        "checkBox_file",
        "checkBox_text",
        "checkBox_dele_source_text",
        "checkBox_dele_link",
        "checkBox_fliter_button",
        "checkBox_discard_no_text_resource",
        "checkBox_pic_water",
        "checkBox_video_water",
        "checkBox_ad_is_bottom_up",
        "checkBox_ad_delete",
        "lineEdit_random_want_count",
        "lineEdit_increase_start_id",
        "lineEdit_increase_want_count",
        "lineEdit_auto_sleep_min",
        "lineEdit_auto_sleep_max",
        "lineEdit_ban_yun_duration_min",
        "lineEdit_ban_yun_duration_max",
        "lineEdit_ban_yun_mb_min",
        "lineEdit_ban_yun_mb_max",
        "lineEdit_priority",
        "lineEdit_source",
        "lineEdit_fliter_words_contain",
        "lineEdit_fliter_words_exclude",
        "lineEdit_loop_start_id",
        "lineEdit_loop_end_id",
        "lineEdit_water_text",
        "lineEdit_yun_yin_name",
        "lineEdit_ban_yun_grid_number",
        "line_edit_by_com_water_pic_ratio",
        "radioButton_action_auto",
        "radioButton_action_download",
        "radioButton_ai_banyun_skip_source",
        "radioButton_ai_banyun_use_source",
        "label_banyun_water_pic_path",
        "text_water_wrapper",
        "pic_water_wrapper",
        "text_model",
        "number_model",
        "textEdit_dest_list",
        "textEdit_tail_text",
        "textEdit_replace_rule",
        "comboBox_video_minute",
        "ban_yun_pic_blur_radius",
        "cb_ban_yun_spoiler",
        "cb_ban_yun_pic_blur",
        "cb_ban_yun_random_cover",
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
        return "请给搬运流取一个名字吧，方便你后续管理！"


__all__ = ["EditBanYunCommentItemEditDialog"]
