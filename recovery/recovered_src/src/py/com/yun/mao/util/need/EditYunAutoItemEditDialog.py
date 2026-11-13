# Recovered module: src.py.com.yun.mao.util.need.EditYunAutoItemEditDialog
# Behaviour-level reconstruction from Nuitka constants, source signatures and
# offline Hex-Rays.  Cloud-auto adds a private warehouse channel, a complete
# version link and BOT extraction fields on top of the common flow editor.
from __future__ import annotations

from .EditAutoFlowItemEditDialog import (
    MODE_RANDOM_TEXT,
    MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
    WATER_MODE_PIC,
    _FlowEditorMixin,
)
from .BaseDialog import BaseDialog
from ...dclass.DTopClass import AUTO_BEAN_TYPE_YUN_AUTO, YunAutoBean


class EditYunAutoItemEditDialog(_FlowEditorMixin, BaseDialog):
    FORM_TITLE = "编辑云自动"
    UI_MODULE = "src.resource.ui.dyna.yun_auto_item"
    BEAN_CLASS = YunAutoBean
    AUTO_TYPE = AUTO_BEAN_TYPE_YUN_AUTO
    BEAN_ATTR = "yunAutoBean"
    WINDOW_RATIO = (3, 6, 10, 20)

    SAVE_BUTTON = "btn_save_yun_auto_item"
    ITEM_NAME_FIELD = "lineEdit_yun_auto_item_name"
    SOURCE_FIELD = "lineEdit_yun_auto_source"
    DB_CHANNEL_FIELD = "lineEdit_yun_auto_db_channel"
    DB_CHANNEL_REQUIRED_MESSAGE = "请输入 云仓库频道！"
    PREVIEW_DEST_FIELD = "textEdit_yun_auto_yulan_dest_list"
    PRIORITY_FIELD = "lineEdit_priority"

    MODE_COMBO = "comboBox_yun_auto_select_mode"
    UNIT_COMBO = "comboBox_yun_auto_number_dan_wei"
    RANDOM_UNIT_COMBO = "comboBox_yun_auto_number_random_dan_wei"
    RANDOM_COUNT_FIELD = "lineEdit_yun_auto_random_want_count"
    INCREASE_START_FIELD = "lineEdit_yun_auto_increase_start_id"
    INCREASE_COUNT_FIELD = "lineEdit_yun_auto_increase_want_count"
    LOOP_START_FIELD = "lineEdit_yun_auto_loop_start_id"
    LOOP_END_FIELD = "lineEdit_yun_auto_loop_end_id"
    MODEL_FIELD = "text_model"
    NUMBER_MODEL_FIELD = "number_model"

    DURATION_MIN_FIELD = "lineEdit_yun_auto_duration_min"
    DURATION_MAX_FIELD = "lineEdit_yun_auto_duration_max"
    SIZE_MIN_FIELD = "lineEdit_yun_auto_mb_min"
    SIZE_MAX_FIELD = "lineEdit_yun_auto_mb_max"
    WORDS_CONTAIN_FIELD = "lineEdit_yun_auto_fliter_words_contain"
    WORDS_EXCLUDE_FIELD = "lineEdit_yun_auto_fliter_words_exclude"
    TAIL_FIELD = "textEdit_yun_auto_tail_text"
    REPLACE_FIELD = "textEdit_yun_auto_replace_rule"
    RESOURCE_FIELDS = {
        "video_photo": "checkBox_yun_auto_video_photo",
        "photo": "checkBox_yun_auto_photo",
        "video": "checkBox_yun_auto_video",
        "file": "checkBox_yun_auto_file",
        "text": "checkBox_yun_auto_text",
    }
    CHAI_ZU_CHECK = "checkBox_chai_zu"
    KEEP_SOURCE_CHECK = "cb_yun_auto_origin_source_text"
    AD_ENABLE_CHECK = "cb_yun_auto_ad_enable"

    AD_LIST = "listWidget_yun_auto_private_ad_list"
    AD_ADD_BUTTON = "btn_yun_auto_add_ad"
    AI_BUTTON = "btn_yunauto_select_ai_em"
    AI_CHECK = "checkBox_yunauto_ai_enable"
    AI_GROUP = "horizontalGroupBox_ai_yunauto"
    AI_LABEL = "label_yunauto_ai_name"
    AI_SKIP_RADIO = "radioButton_ai_yunauto_skip_source"
    AI_USE_RADIO = "radioButton_ai_yunauto_use_source"

    WATER_MODE_COMBO = "cb_yun_auto_water_mode"
    WATER_PATH_LABEL = "label_yun_auto_water_pic_path"
    WATER_SELECT_BUTTON = "btn_yun_auto_water_select_pic"
    WATER_RATIO_FIELD = "line_edit_yun_auto_water_pic_ratio"
    WATER_TEXT_FIELD = "lineEdit_cb_water_text"
    WATER_PIC_CHECK = "cb_yun_auto_pic_water"
    WATER_VIDEO_CHECK = "cb_yun_auto_video_water"
    WATER_DURATION_COMBO = "cb_yun_auto_video_minute"

    ACTION_AUTO_RADIO = "radioButton_yun_auto_action_au"
    ACTION_DOWNLOAD_RADIO = "radioButton_yun_auto_action_download"
    ACTION_SLEEP_MIN_FIELD = "lineEdit_yun_auto_sleep_min"
    ACTION_SLEEP_MAX_FIELD = "lineEdit_yun_auto_sleep_max"

    RESOP_BLUR_CHECK = "cb_yun_auto_pic_blur"
    RESOP_SPOILER_CHECK = "cb_yun_auto_spoiler"
    RESOP_RADIUS_FIELD = "yun_auto_pic_blur_radius"

    GRID_FIELD = "lineEdit_yun_auto_grid_number"
    GRID_COVER_FIELD = "cb_yun_auto_random_cover"

    YULAN_MODE_COMBO = "comboBox_yun_auto_select_yulan_mode"
    YULAN_RADIOS = (
        "radioButton_yun_auto_10",
        "radioButton_yun_auto_20",
        "radioButton_yun_auto_30",
        "radioButton_yun_auto_customer",
    )
    YULAN_CUSTOM_RADIO = "radioButton_yun_auto_customer"
    YULAN_CUSTOM_FIELD = "lineEdit_yun_auto_customer"
    YULAN_MIN_FIELD = "lineEdit_yun_auto_min_duration"
    YULAN_MAX_FIELD = "lineEdit_yun_auto_max_duration"

    ADD_DURATION_CHECK = "checkBox_yun_auto_add_duration_info"
    ADD_DURATION_BQ_CHECK = "checkBox_yun_auto_add_duration_info_bq"
    COMPLETE_VERSION_FIELD = "lineEdit_yun_auto_wan_zhen_ban_text"
    COMPLETE_BLOCKQUOTE_CHECK = "cb_yun_auto_block_quote"
    BOT_FIELD = "lineEdit_yun_auto_bot"
    BOT_SERVICE_MESSAGE = "当前你没有开通BOT云猫机器人服务，暂时不能使用云自动功能！"

    RESOURCE_TUTORIAL_BUTTON = "btn_yun_auto_res_btn_jiao_chen"
    RESOP_TUTORIAL_BUTTON = "btn_yun_auto_res_op_jiao_chen"
    ACTION_TUTORIAL_BUTTON = "btn_yun_auto_action_jiao_chen"
    TOPIC_TUTORIAL_BUTTON = "yun_auto_btn_p_jiao_chen"
    PIC_WATER_TUTORIAL_BUTTON = "btn_yun_auto_water_pic_jiao_chen"
    GRID_TUTORIAL_BUTTON = "btn_yun_auto_grid_jiao_chen"
    COVER_TUTORIAL_BUTTON = "yun_auto_cover_jiao_chen"
    RES_OP_COURSE = "unifyShowResOpCourse"
    ACTION_COURSE = "unifyShowYunAutoBanYunTypeCourse"
    TOPIC_COURSE = "unifyShowTopicCourse"

    SAVE_EDIT_MESSAGE = "更新云自动成功！"
    SAVE_ADD_MESSAGE = "添加云自动成功！"
    DEFAULT_TEXTS = {
        "lineEdit_priority": "100",
        "lineEdit_yun_auto_sleep_min": "3",
        "lineEdit_yun_auto_sleep_max": "5",
        "lineEdit_yun_auto_min_duration": "60",
        "lineEdit_yun_auto_max_duration": "120",
        "line_edit_yun_auto_water_pic_ratio": "30",
        "lineEdit_yun_auto_grid_number": "6",
        "lineEdit_yun_auto_wan_zhen_ban_text": "💋点我看完整版",
    }
    DEFAULT_CHECKS = {
        "checkBox_yun_auto_video_photo": True,
        "checkBox_yun_auto_photo": True,
        "checkBox_yun_auto_video": True,
        "checkBox_yun_auto_file": True,
        "checkBox_yun_auto_text": True,
        "cb_yun_auto_origin_source_text": True,
        "cb_yun_auto_ad_enable": True,
        "radioButton_yun_auto_action_au": True,
        "radioButton_ai_yunauto_skip_source": True,
        "radioButton_yun_auto_10": True,
        "cb_yun_auto_block_quote": True,
        "checkBox_yun_auto_add_duration_info_bq": True,
    }
    DEFAULT_COMBOS = {
        "comboBox_yun_auto_select_mode": MODE_RANDOM_TEXT,
        "comboBox_yun_auto_number_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "comboBox_yun_auto_number_random_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "cb_yun_auto_water_mode": WATER_MODE_PIC,
        "comboBox_yun_auto_select_yulan_mode": "按比例模式",
    }

    WIDGET_NAMES = (
        "yun_auto_btn_p_jiao_chen",
        "yun_auto_btn_db_channel_jiao_chen",
        "btn_yun_auto_res_btn_jiao_chen",
        "btn_yun_auto_action_jiao_chen",
        "btn_yun_auto_res_op_jiao_chen",
        "btn_yun_auto_wan_zhen_ban_jiao_chen",
        "btn_yun_auto_add_duration_jiao_chen",
        "btn_yunauto_select_ai_em",
        "btn_yun_auto_water_pic_jiao_chen",
        "btn_yun_auto_water_select_pic",
        "btn_yun_auto_grid_jiao_chen",
        "yun_auto_cover_jiao_chen",
        "btn_save_yun_auto_item",
        "btn_yun_auto_add_ad",
        "comboBox_yun_auto_number_dan_wei",
        "comboBox_yun_auto_number_random_dan_wei",
        "comboBox_yun_auto_select_mode",
        "comboBox_yun_auto_select_yulan_mode",
        "cb_yun_auto_water_mode",
        "listWidget_yun_auto_private_ad_list",
        "cb_yun_auto_origin_source_text",
        "cb_yun_auto_ad_enable",
        "radioButton_yun_auto_10",
        "radioButton_yun_auto_20",
        "radioButton_yun_auto_30",
        "radioButton_yun_auto_customer",
        "checkBox_yun_auto_video_photo",
        "checkBox_pb_yun_auto_video",
        "checkBox_yunauto_ai_enable",
        "horizontalGroupBox_ai_yunauto",
        "label_yunauto_ai_name",
        "lineEdit_yun_auto_customer",
        "yulan_qu",
        "yulan_qu_wrapper",
        "checkBox_chai_zu",
        "checkBox_yun_auto_photo",
        "checkBox_yun_auto_video",
        "checkBox_yun_auto_file",
        "checkBox_yun_auto_text",
        "cb_yun_auto_dele_source_text",
        "cb_yun_auto_dele_link",
        "cb_yun_auto_fliter_button",
        "checkBox_discard_no_text_resource",
        "checkBox_pb_yun_auto_picture",
        "lineEdit_yun_auto_random_want_count",
        "lineEdit_yun_auto_increase_start_id",
        "lineEdit_yun_auto_increase_want_count",
        "lineEdit_yun_auto_sleep_min",
        "lineEdit_yun_auto_sleep_max",
        "lineEdit_yun_auto_duration_min",
        "lineEdit_yun_auto_duration_max",
        "lineEdit_yun_auto_mb_min",
        "lineEdit_yun_auto_mb_max",
        "lineEdit_yun_auto_min_duration",
        "lineEdit_yun_auto_max_duration",
        "lineEdit_yun_auto_fliter_words_contain",
        "lineEdit_yun_auto_fliter_words_exclude",
        "lineEdit_yun_auto_loop_start_id",
        "lineEdit_yun_auto_loop_end_id",
        "lineEdit_yun_auto_source",
        "lineEdit_yun_auto_db_channel",
        "lineEdit_yun_auto_item_name",
        "lineEdit_yun_auto_grid_number",
        "lineEdit_yun_auto_wan_zhen_ban_text",
        "lineEdit_yun_auto_bot",
        "lineEdit_cb_water_text",
        "lineEdit_priority",
        "line_edit_yun_auto_water_pic_ratio",
        "radioButton_yun_auto_action_au",
        "radioButton_yun_auto_action_download",
        "radioButton_ai_yunauto_skip_source",
        "radioButton_ai_yunauto_use_source",
        "label_yun_auto_water_pic_path",
        "text_water_wrapper",
        "pic_water_wrapper",
        "text_model",
        "number_model",
        "textEdit_yun_auto_yulan_dest_list",
        "textEdit_yun_auto_tail_text",
        "textEdit_yun_auto_replace_rule",
        "cb_yun_auto_pic_water",
        "cb_yun_auto_video_water",
        "cb_yun_auto_video_minute",
        "cb_yun_auto_spoiler",
        "cb_yun_auto_pic_blur",
        "cb_yun_auto_block_quote",
        "checkBox_yun_auto_add_duration_info",
        "checkBox_yun_auto_add_duration_info_bq",
        "cb_yun_auto_random_cover",
        "cb_yun_auto_ad_is_bottom_up",
        "cb_yun_auto_ad_delete",
        "yun_auto_pic_blur_radius",
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
            "yun_auto_btn_db_channel_jiao_chen",
            "clicked",
            self.showDbChannelDialog,
        )
        self._connect(
            "btn_yun_auto_wan_zhen_ban_jiao_chen",
            "clicked",
            self.on_show_bot_bq_font_jiao_chen,
        )
        self._connect(
            "btn_yun_auto_add_duration_jiao_chen",
            "clicked",
            self.on_show_duration_jiao_chen,
        )

    def _name_required_message(self) -> str:
        return "请给云自动取一个名字吧，方便你后续管理！"


__all__ = ["EditYunAutoItemEditDialog"]
