# Recovered module: src.py.com.yun.mao.util.need.EditYunPreViewItemEditDialog
# Behaviour-level reconstruction from Nuitka constants, source signatures and
# offline Hex-Rays.  Cloud-preview's private warehouse field is the source.
from __future__ import annotations

from .EditAutoFlowItemEditDialog import (
    MODE_RANDOM_TEXT,
    MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
    WATER_MODE_PIC,
    _FlowEditorMixin,
)
from .BaseDialog import BaseDialog
from ...dclass.DTopClass import AUTO_BEAN_TYPE_YUN_PRE_VIEW, YunPreViewBean


class EditYunPreViewItemEditDialog(_FlowEditorMixin, BaseDialog):
    FORM_TITLE = "编辑云预览"
    UI_MODULE = "src.resource.ui.dyna.yun_preview_item"
    BEAN_CLASS = YunPreViewBean
    AUTO_TYPE = AUTO_BEAN_TYPE_YUN_PRE_VIEW
    BEAN_ATTR = "yunPreviewBean"
    WINDOW_RATIO = (3, 6, 10, 20)

    SAVE_BUTTON = "btn_save_yun_preview_item"
    ITEM_NAME_FIELD = "lineEdit_yun_preview_item_name"
    # inferred: the preview form has only the private warehouse field; it is
    # the bean's source value as well.
    SOURCE_FIELD = "lineEdit_yun_preview_db_channel"
    SOURCE_REQUIRED_MESSAGE = "请输入 云仓库频道！"
    PREVIEW_DEST_FIELD = "textEdit_yun_preview_yulan_dest_list"
    PRIORITY_FIELD = "lineEdit_priority"

    MODE_COMBO = "comboBox_yun_preview_select_mode"
    UNIT_COMBO = "comboBox_yun_preview_number_dan_wei"
    RANDOM_UNIT_COMBO = "comboBox_yun_preview_number_random_dan_wei"
    RANDOM_COUNT_FIELD = "lineEdit_yun_preview_random_want_count"
    INCREASE_START_FIELD = "lineEdit_yun_preview_increase_start_id"
    INCREASE_COUNT_FIELD = "lineEdit_yun_preview_increase_want_count"
    LOOP_START_FIELD = "lineEdit_yun_preview_loop_start_id"
    LOOP_END_FIELD = "lineEdit_yun_preview_loop_end_id"
    MODEL_FIELD = "text_model"
    NUMBER_MODEL_FIELD = "number_model"

    DURATION_MIN_FIELD = "lineEdit_yun_preview_duration_min"
    DURATION_MAX_FIELD = "lineEdit_yun_preview_duration_max"
    SIZE_MIN_FIELD = "lineEdit_yun_preview_mb_min"
    SIZE_MAX_FIELD = "lineEdit_yun_preview_mb_max"
    WORDS_CONTAIN_FIELD = "lineEdit_yun_preview_fliter_words_contain"
    WORDS_EXCLUDE_FIELD = "lineEdit_yun_preview_fliter_words_exclude"
    TAIL_FIELD = "textEdit_yun_preview_tail_text"
    REPLACE_FIELD = "textEdit_yun_preview_replace_rule"
    RESOURCE_FIELDS = {
        "video_photo": "checkBox_yun_preview_video_photo",
        "photo": "checkBox_yun_preview_photo",
        "video": "checkBox_yun_preview_video",
        "file": "checkBox_yun_preview_file",
        "text": "checkBox_yun_preview_text",
    }
    CHAI_ZU_CHECK = "checkBox_chai_zu"
    KEEP_SOURCE_CHECK = "cb_yun_preview_origin_source_text"
    AD_ENABLE_CHECK = "cb_yun_preview_ad_enable"

    AD_LIST = "listWidget_yun_preview_private_ad_list"
    AD_ADD_BUTTON = "btn_yun_preview_add_ad"
    AI_BUTTON = "btn_yunpre_select_ai_em"
    AI_CHECK = "checkBox_yunpre_ai_enable"
    AI_GROUP = "horizontalGroupBox_ai_yunpre"
    AI_LABEL = "label_yunpre_ai_name"
    AI_SKIP_RADIO = "radioButton_ai_yunpre_skip_source"
    AI_USE_RADIO = "radioButton_ai_yunpre_use_source"

    WATER_MODE_COMBO = "cb_yun_preview_water_mode"
    WATER_PATH_LABEL = "label_yun_preview_water_pic_path"
    WATER_SELECT_BUTTON = "btn_yun_preview_water_select_pic"
    WATER_RATIO_FIELD = "line_edit_yun_preview_water_pic_ratio"
    WATER_TEXT_FIELD = "lineEdit_cb_water_text"
    WATER_PIC_CHECK = "cb_yun_preview_pic_water"
    WATER_VIDEO_CHECK = "cb_yun_preview_video_water"
    WATER_DURATION_COMBO = "cb_yun_preview_video_minute"

    ACTION_AUTO_RADIO = "radioButton_yun_preview_action_au"
    ACTION_DOWNLOAD_RADIO = "radioButton_yun_preview_action_download"
    ACTION_SLEEP_MIN_FIELD = "lineEdit_yun_preview_sleep_min"
    ACTION_SLEEP_MAX_FIELD = "lineEdit_yun_preview_sleep_max"

    RESOP_BLUR_CHECK = "cb_yun_preview_pic_blur"
    RESOP_SPOILER_CHECK = "cb_yun_preview_spoiler"
    RESOP_RADIUS_FIELD = "yun_preview_pic_blur_radius"

    GRID_FIELD = "lineEdit_yun_preview_grid_number"
    GRID_COVER_FIELD = "cb_yun_preview_random_cover"

    YULAN_MODE_COMBO = "comboBox_yun_preview_select_yulan_mode"
    YULAN_RADIOS = (
        "radioButton_yun_preview_10",
        "radioButton_yun_preview_20",
        "radioButton_yun_preview_30",
        "radioButton_yun_preview_customer",
    )
    YULAN_CUSTOM_RADIO = "radioButton_yun_preview_customer"
    YULAN_CUSTOM_FIELD = "lineEdit_yun_preview_customer"
    YULAN_MIN_FIELD = "lineEdit_yun_preview_min_duration"
    YULAN_MAX_FIELD = "lineEdit_yun_preview_max_duration"

    ADD_DURATION_CHECK = "checkBox_yun_preview_add_duration_info"
    ADD_DURATION_BQ_CHECK = "checkBox_yun_preview_add_duration_info_bq"
    COMPLETE_VERSION_FIELD = "lineEdit_yun_preview_wan_zhen_ban_text"
    COMPLETE_BLOCKQUOTE_CHECK = "cb_yun_preview_block_quote"
    BOT_FIELD = "lineEdit_yun_preview_bot"
    BOT_ERROR_MESSAGE = "资源提取机器人名字格式不对，格式为 @xxxxbot"
    BOT_SERVICE_MESSAGE = "当前你没有开通BOT云猫机器人服务，暂时不能使用云预览功能！"

    RESOURCE_TUTORIAL_BUTTON = "btn_yun_preview_res_btn_jiao_chen"
    RESOP_TUTORIAL_BUTTON = "btn_yun_preview_res_op_jiao_chen"
    ACTION_TUTORIAL_BUTTON = "btn_yun_preview_action_jiao_chen"
    TOPIC_TUTORIAL_BUTTON = "yun_preview_btn_p_jiao_chen"
    PIC_WATER_TUTORIAL_BUTTON = "btn_yun_preview_water_pic_jiao_chen"
    GRID_TUTORIAL_BUTTON = "btn_yun_preview_grid_jiao_chen"
    COVER_TUTORIAL_BUTTON = "yun_preview_cover_jiao_chen"
    RES_OP_COURSE = "unifyShowResOpCourse"
    ACTION_COURSE = "unifyShowYunPreViewBanYunTypeCourse"
    TOPIC_COURSE = "unifyShowTopicCourse"

    SAVE_EDIT_MESSAGE = "更新云预览成功！"
    SAVE_ADD_MESSAGE = "添加云预览成功！"
    DEFAULT_TEXTS = {
        "lineEdit_priority": "100",
        "lineEdit_yun_preview_sleep_min": "3",
        "lineEdit_yun_preview_sleep_max": "5",
        "lineEdit_yun_preview_min_duration": "60",
        "lineEdit_yun_preview_max_duration": "120",
        "line_edit_yun_preview_water_pic_ratio": "30",
        "lineEdit_yun_preview_grid_number": "6",
        "lineEdit_yun_preview_wan_zhen_ban_text": "💋点我看完整版",
    }
    DEFAULT_CHECKS = {
        "checkBox_yun_preview_video_photo": True,
        "checkBox_yun_preview_photo": True,
        "checkBox_yun_preview_video": True,
        "checkBox_yun_preview_file": True,
        "checkBox_yun_preview_text": True,
        "cb_yun_preview_origin_source_text": True,
        "cb_yun_preview_ad_enable": True,
        "radioButton_yun_preview_action_au": True,
        "radioButton_ai_yunpre_skip_source": True,
        "radioButton_yun_preview_10": True,
        "cb_yun_preview_block_quote": True,
        "checkBox_yun_preview_add_duration_info_bq": True,
    }
    DEFAULT_COMBOS = {
        "comboBox_yun_preview_select_mode": MODE_RANDOM_TEXT,
        "comboBox_yun_preview_number_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "comboBox_yun_preview_number_random_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "cb_yun_preview_water_mode": WATER_MODE_PIC,
        "comboBox_yun_preview_select_yulan_mode": "按比例模式",
    }

    WIDGET_NAMES = (
        "yun_preview_btn_p_jiao_chen",
        "yun_preview_btn_db_channel_jiao_chen",
        "btn_yun_preview_res_btn_jiao_chen",
        "btn_yun_preview_action_jiao_chen",
        "btn_yun_preview_res_op_jiao_chen",
        "btn_yun_preview_wan_zhen_ban_jiao_chen",
        "btn_yun_preview_add_duration_jiao_chen",
        "btn_yunpre_select_ai_em",
        "btn_yun_preview_water_pic_jiao_chen",
        "btn_yun_preview_water_select_pic",
        "btn_yun_preview_grid_jiao_chen",
        "yun_preview_cover_jiao_chen",
        "btn_save_yun_preview_item",
        "btn_yun_preview_add_ad",
        "comboBox_yun_preview_number_dan_wei",
        "comboBox_yun_preview_number_random_dan_wei",
        "comboBox_yun_preview_select_mode",
        "comboBox_yun_preview_select_yulan_mode",
        "cb_yun_preview_water_mode",
        "listWidget_yun_preview_private_ad_list",
        "cb_yun_preview_origin_source_text",
        "cb_yun_preview_ad_enable",
        "radioButton_yun_preview_10",
        "radioButton_yun_preview_20",
        "radioButton_yun_preview_30",
        "radioButton_yun_preview_customer",
        "checkBox_yun_preview_video_photo",
        "checkBox_pb_yun_preview_video",
        "checkBox_yunpre_ai_enable",
        "horizontalGroupBox_ai_yunpre",
        "label_yunpre_ai_name",
        "lineEdit_yun_preview_customer",
        "yulan_qu",
        "yulan_qu_wrapper",
        "checkBox_chai_zu",
        "checkBox_yun_preview_photo",
        "checkBox_yun_preview_video",
        "checkBox_yun_preview_file",
        "checkBox_yun_preview_text",
        "cb_yun_preview_dele_source_text",
        "cb_yun_preview_dele_link",
        "cb_yun_preview_fliter_button",
        "checkBox_discard_no_text_resource",
        "checkBox_pb_yun_preview_picture",
        "lineEdit_yun_preview_random_want_count",
        "lineEdit_yun_preview_increase_start_id",
        "lineEdit_yun_preview_increase_want_count",
        "lineEdit_yun_preview_sleep_min",
        "lineEdit_yun_preview_sleep_max",
        "lineEdit_yun_preview_duration_min",
        "lineEdit_yun_preview_duration_max",
        "lineEdit_yun_preview_mb_min",
        "lineEdit_yun_preview_mb_max",
        "lineEdit_yun_preview_min_duration",
        "lineEdit_yun_preview_max_duration",
        "lineEdit_yun_preview_fliter_words_contain",
        "lineEdit_yun_preview_fliter_words_exclude",
        "lineEdit_yun_preview_loop_start_id",
        "lineEdit_yun_preview_loop_end_id",
        "lineEdit_yun_preview_db_channel",
        "lineEdit_yun_preview_item_name",
        "lineEdit_yun_preview_grid_number",
        "lineEdit_yun_preview_wan_zhen_ban_text",
        "lineEdit_yun_preview_bot",
        "lineEdit_cb_water_text",
        "lineEdit_priority",
        "line_edit_yun_preview_water_pic_ratio",
        "radioButton_yun_preview_action_au",
        "radioButton_yun_preview_action_download",
        "radioButton_ai_yunpre_skip_source",
        "radioButton_ai_yunpre_use_source",
        "label_yun_preview_water_pic_path",
        "text_water_wrapper",
        "pic_water_wrapper",
        "text_model",
        "number_model",
        "textEdit_yun_preview_yulan_dest_list",
        "textEdit_yun_preview_tail_text",
        "textEdit_yun_preview_replace_rule",
        "cb_yun_preview_pic_water",
        "cb_yun_preview_video_water",
        "cb_yun_preview_video_minute",
        "cb_yun_preview_spoiler",
        "cb_yun_preview_pic_blur",
        "cb_yun_preview_block_quote",
        "checkBox_yun_preview_add_duration_info",
        "checkBox_yun_preview_add_duration_info_bq",
        "cb_yun_preview_random_cover",
        "cb_yun_preview_ad_is_bottom_up",
        "cb_yun_preview_ad_delete",
        "yun_preview_pic_blur_radius",
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

    def _connect_specific_ui(self) -> None:
        self._connect(
            "yun_preview_btn_db_channel_jiao_chen",
            "clicked",
            self.showDbChannelDialog,
        )
        self._connect(
            "btn_yun_preview_wan_zhen_ban_jiao_chen",
            "clicked",
            self.on_show_bot_bq_font_jiao_chen,
        )
        self._connect(
            "btn_yun_preview_add_duration_jiao_chen",
            "clicked",
            self.on_show_duration_jiao_chen,
        )

    def _name_required_message(self) -> str:
        return "请给云预览取一个名字吧，方便你后续管理！"


__all__ = ["EditYunPreViewItemEditDialog"]
