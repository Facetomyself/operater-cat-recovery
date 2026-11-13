# Recovered module: src.py.com.yun.mao.util.need.EditAutoFlowItemEditDialog
# Behaviour-level reconstruction from Nuitka constants, source signatures and
# the offline Hex-Rays targets.  The shared editor mixin below is inferred
# plumbing: original code duplicated it in every dialog.  It creates no Qt
# widgets, files or network objects at import time.
from __future__ import annotations

import copy
import importlib
import re
from pathlib import Path
from typing import Any

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from . import CommonCode, utils
from .BaseDialog import BaseDialog
from ...dclass.DTopClass import (
    AUTO_BEAN_TYPE_AUTO_FLOW,
    AddDurationInfo,
    AdWrapper,
    AdvancedFilterBean,
    AiEmployee,
    AiRefusedOption,
    AutoFlowBean,
    BaseFilterBean,
    CompleteVersionOp,
    DurationFilterBean,
    DurationMode,
    ForwardActionBean,
    GridOpt,
    HuiYuanLink,
    ModelWrapper,
    PresentMode,
    Replace,
    SizeFilterBean,
    Tail,
    Water,
    YouKeLink,
    YuLanModeBean,
    YuLanResOp,
)


RESOURCE_TYPE_VIDEO_PHOTO = "video_photo"
RESOURCE_TYPE_PHOTO = "photo"
RESOURCE_TYPE_VIDEO = "video"
RESOURCE_TYPE_FILE = "file"
RESOURCE_TYPE_TEXT = "text"
ACTION_AUTO = "auto"
ACTION_DOWNLOAD = "download"
MODE_RANDOM_TEXT = "随机模式"
MODE_INCREASE_TEXT = "顺序模式"
MODE_LOOP_TEXT = "循环模式"
MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT = "按组计算"
MESSAGE_NUMBER_DAN_WEI_SINGLE_TEXT = "按个计算"
MODE_NUMBER_GROUP = "group"
MODE_NUMBER_SINGLE = "single"
WATER_MODE_TEXT = "文字水印"
WATER_MODE_PIC = "图片水印"
YULAN_MODE_PRESENT_TEXT = "按比例模式"
YULAN_MODE_DURATION_TEXT = "自定义时长模式"
YULAN_MODE_PRESENT = "present_model"
YULAN_MODE_DURATION = "duration_model"
YULAN_RES_TYPE_VIDEO = "video"


def _parse_int(value: Any) -> tuple[bool, int]:
    text = str(value or "").strip()
    try:
        return True, int(text)
    except (TypeError, ValueError):
        return False, 0


def _safe_int(value: Any, default: int = 0) -> int:
    ok, number = _parse_int(value)
    return number if ok else default


def _split_destes(text: str) -> list[str]:
    result: list[str] = []
    for line in str(text or "").replace("，", "\n").splitlines():
        item = line.strip()
        if item:
            result.append(item)
    return result


def _join_destes(values: Any) -> str:
    return "\n".join(str(item).strip() for item in values or [] if str(item).strip())


def _split_words(text: str) -> list[str]:
    values = re.split(r"[\n,，|]+", str(text or ""))
    return [item.strip() for item in values if item.strip()]


def _join_words(values: Any) -> str:
    return "，".join(str(item).strip() for item in values or [] if str(item).strip())


def _split_replaces(text: str) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for raw_line in str(text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "->" in line:
            old, new = line.split("->", 1)
        elif "→" in line:
            old, new = line.split("→", 1)
        else:
            continue
        old = old.strip()
        new = new.strip()
        if old:
            result.append((old, new))
    return result


def _join_replaces(values: Any) -> str:
    lines: list[str] = []
    for item in values or []:
        if isinstance(item, dict):
            old = item.get("old", item.get("source", ""))
            new = item.get("new", item.get("target", ""))
        elif isinstance(item, (tuple, list)) and len(item) >= 2:
            old, new = item[0], item[1]
        else:
            old, new = item, ""
        lines.append(f"{old} -> {new}")
    return "\n".join(lines)


def _video_duration(index: int) -> int:
    try:
        return int(CommonCode.parseVideoDuration(index))
    except Exception:
        return 60


def _video_duration_index(duration: Any) -> int:
    try:
        return int(CommonCode.parseVideoIndex(duration))
    except Exception:
        return 0


def _number_mode_text(number_mode: Any) -> str:
    return (
        MESSAGE_NUMBER_DAN_WEI_SINGLE_TEXT
        if str(number_mode or "") == MODE_NUMBER_SINGLE
        else MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT
    )


def _number_mode_value(text: Any) -> str:
    return (
        MODE_NUMBER_SINGLE
        if str(text or "").strip() == MESSAGE_NUMBER_DAN_WEI_SINGLE_TEXT
        else MODE_NUMBER_GROUP
    )


class _FlowEditorMixin:
    """Shared form, validation and persistence behavior for flow editors."""

    FORM_TITLE = "编辑条目"
    UI_MODULE = ""
    WIDGET_NAMES: tuple[str, ...] = ()
    WINDOW_RATIO = (3, 6, 10, 20)
    BEAN_CLASS = None
    AUTO_TYPE = 0
    BEAN_ATTR = "autobean"
    SAVE_EDIT_MESSAGE = "更新成功！"
    SAVE_ADD_MESSAGE = "添加成功！"

    SAVE_BUTTON: str | None = None
    ITEM_NAME_FIELD: str | None = None
    SOURCE_FIELD: str | None = None
    SOURCE_REQUIRED_MESSAGE = "请输入 来源频道/群组 ！"
    DB_CHANNEL_FIELD: str | None = None
    DB_CHANNEL_REQUIRED_MESSAGE = "请输入 云仓库频道！"
    DEST_FIELD: str | None = None
    DEST_REQUIRED_MESSAGE = "请输入 目标频道/群组！"
    PREVIEW_DEST_FIELD: str | None = None
    PREVIEW_DEST_REQUIRED_MESSAGE = "请输入 预览频道/群组！"
    PRIORITY_FIELD: str | None = "lineEdit_priority"
    PRIORITY_MESSAGE = "优先级必须是数字！数字越大，优先级越高，排序越靠前！"

    MODE_COMBO: str | None = None
    UNIT_COMBO: str | None = None
    RANDOM_UNIT_COMBO: str | None = None
    RANDOM_COUNT_FIELD: str | None = None
    INCREASE_START_FIELD: str | None = None
    INCREASE_COUNT_FIELD: str | None = None
    LOOP_START_FIELD: str | None = None
    LOOP_END_FIELD: str | None = None
    MODEL_FIELD: str | None = None
    NUMBER_MODEL_FIELD: str | None = None

    DURATION_MIN_FIELD: str | None = None
    DURATION_MAX_FIELD: str | None = None
    SIZE_MIN_FIELD: str | None = None
    SIZE_MAX_FIELD: str | None = None
    WORDS_CONTAIN_FIELD: str | None = None
    WORDS_EXCLUDE_FIELD: str | None = None
    TAIL_FIELD: str | None = None
    REPLACE_FIELD: str | None = None
    RESOURCE_FIELDS: dict[str, str] = {}
    CHAI_ZU_CHECK: str | None = None
    KEEP_SOURCE_CHECK: str | None = None
    AD_ENABLE_CHECK: str | None = None

    AD_LIST: str | None = None
    AD_ADD_BUTTON: str | None = None
    AI_BUTTON: str | None = None
    AI_CHECK: str | None = None
    AI_GROUP: str | None = None
    AI_LABEL: str | None = None
    AI_SKIP_RADIO: str | None = None
    AI_USE_RADIO: str | None = None

    WATER_MODE_COMBO: str | None = None
    WATER_PATH_LABEL: str | None = None
    WATER_SELECT_BUTTON: str | None = None
    WATER_RATIO_FIELD: str | None = None
    WATER_TEXT_FIELD: str | None = None
    WATER_PIC_CHECK: str | None = None
    WATER_VIDEO_CHECK: str | None = None
    WATER_DURATION_COMBO: str | None = None
    RANDOM_WRAPPER = "random_com"
    INCREASE_WRAPPER = "increase_com"
    LOOP_WRAPPER = "loop_com"
    PRESENT_CONTAINER = "present_container"
    DURATION_CONTAINER = "duration_container"
    TEXT_WATER_WRAPPER = "text_water_wrapper"
    PIC_WATER_WRAPPER = "pic_water_wrapper"

    ACTION_AUTO_RADIO: str | None = None
    ACTION_DOWNLOAD_RADIO: str | None = None
    ACTION_SLEEP_MIN_FIELD: str | None = None
    ACTION_SLEEP_MAX_FIELD: str | None = None

    RESOP_BLUR_CHECK: str | None = None
    RESOP_SPOILER_CHECK: str | None = None
    RESOP_RADIUS_FIELD: str | None = None

    GRID_FIELD: str | None = None
    GRID_COVER_FIELD: str | None = None

    YULAN_MODE_COMBO: str | None = None
    YULAN_RADIOS: tuple[str, ...] = ()
    YULAN_CUSTOM_RADIO: str | None = None
    YULAN_CUSTOM_FIELD: str | None = None
    YULAN_MIN_FIELD: str | None = None
    YULAN_MAX_FIELD: str | None = None

    HUIYUAN_ENABLE_CHECK: str | None = None
    HUIYUAN_TEXT_FIELD: str | None = None
    HUIYUAN_CUSTOMER_CHECK: str | None = None
    HUIYUAN_LINK_FIELD: str | None = None
    HUIYUAN_BQ_CHECK: str | None = None
    YOUKE_ENABLE_CHECK: str | None = None
    YOUKE_TEXT_FIELD: str | None = None
    YOUKE_LINK_FIELD: str | None = None
    YOUKE_BQ_CHECK: str | None = None

    ADD_DURATION_CHECK: str | None = None
    ADD_DURATION_BQ_CHECK: str | None = None

    COMPLETE_VERSION_FIELD: str | None = None
    COMPLETE_BLOCKQUOTE_CHECK: str | None = None
    BOT_FIELD: str | None = None
    BOT_ERROR_MESSAGE = "资源提取机器人名字格式不对，格式为 @xxxbot"
    BOT_SERVICE_MESSAGE = "当前你没有开通BOT云猫机器人服务，暂时不能使用云自动功能！"

    COPY_COMMENT_CHECK: str | None = None
    COMMENT_CONFIG_BUTTON: str | None = None

    RESOURCE_TUTORIAL_BUTTON: str | None = None
    RESOP_TUTORIAL_BUTTON: str | None = None
    ACTION_TUTORIAL_BUTTON: str | None = None
    TOPIC_TUTORIAL_BUTTON: str | None = None
    PIC_WATER_TUTORIAL_BUTTON: str | None = None
    GRID_TUTORIAL_BUTTON: str | None = None
    COVER_TUTORIAL_BUTTON: str | None = None
    HUIYUAN_TUTORIAL_BUTTON: str | None = None
    YOUKE_TUTORIAL_BUTTON: str | None = None

    RES_OP_COURSE = "unifyShowPublishResOpCourse"
    ACTION_COURSE = "unifyShowAutoFlowBanYunTypeCourse"
    TOPIC_COURSE = "unifyShowTopicCourse"

    DEFAULT_TEXTS: dict[str, str] = {}
    DEFAULT_CHECKS: dict[str, bool] = {}
    DEFAULT_COMBOS: dict[str, str] = {}

    def __init__(
        self,
        parent=None,
        windowTitle: str | None = None,
        autobean=None,
        isCopy: bool = False,
        employee_id=None,
    ) -> None:
        super().__init__(parent, windowTitle or self.FORM_TITLE)
        self.edit_mode = autobean is not None and not bool(isCopy)
        self.autobean = autobean
        self.isCopy = bool(isCopy)
        self.employee_id = employee_id
        self.temp_water_image_abs_path = ""
        self.temp_water_pic_ratio = 30
        self.adMap: dict[Any, Any] = {}
        self.selfAdWrapper = None
        self.ades: list[Any] = []
        self.adId = None
        self.aiEmployee = None
        self.uid = None
        self.water = None
        self.picPath = ""
        self.picRatio = 30
        self.commentRule = None
        self._common_ui_connected = False

        bean = self._coerce_bean(autobean)
        if bean is not None:
            if self.isCopy:
                bean = copy.deepcopy(bean)
                bean.kid = ""
            if not str(getattr(bean, "kid", "") or ""):
                bean.kid = utils.gen_unit_name_by_ns()
            self.kid = str(getattr(bean, "kid", "") or "")
            self.aiEmployee = getattr(bean, "aiEmployee", None)
            self.uid = getattr(self.aiEmployee, "uid", None)
            self.water = getattr(bean, "water", None)
            self.picPath = str(getattr(self.water, "picPath", "") or "")
            self.picRatio = int(getattr(self.water, "picRatio", 30) or 30)
            self.commentRule = getattr(bean, "commentRule", None)
            if not self.employee_id and self.aiEmployee is not None:
                self.employee_id = getattr(self.aiEmployee, "uid", None)
        else:
            self.kid = utils.gen_unit_name_by_ns()

        setattr(self, self.BEAN_ATTR, bean)
        self.ui = self._load_form()
        self._connect_common_ui()
        self._connect_specific_ui()
        self.defaultFill()
        self.fillBeanIfNeed()
        self.fillAdList()

    def _coerce_bean(self, source):
        if source is not None and getattr(source, "beanLike", False):
            source = getattr(source, "exec_obj", None) or source
        if source is not None and hasattr(source, "auto_type"):
            return source
        cls = self.BEAN_CLASS
        if cls is None:
            return None
        return cls(auto_type=self.AUTO_TYPE)

    def _load_form(self):
        if self.UI_MODULE:
            try:
                module = importlib.import_module(self.UI_MODULE)
                form = module.Ui_Form()
                form.setupUi(self)
                return form
            except Exception:
                # The dynamic generated UI module is not present in the
                # recovered tree.  Fall back to a field-compatible form.
                return self._build_fallback_form()
        return self._build_fallback_form()

    def _build_fallback_form(self):
        # inferred: the generated src.resource.ui.dyna Ui_Form module is not
        # present in the recovered tree; keep the same object names.
        ui = QWidget()
        ui.setObjectName("ui")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        content = QWidget(scroll)
        form = QFormLayout(content)
        form.setContentsMargins(10, 8, 10, 8)
        form.setSpacing(6)
        scroll.setWidget(content)
        outer.addWidget(scroll)
        ui._content = content
        ui._form = form
        for name in self.WIDGET_NAMES:
            widget = self._make_widget(name, content)
            setattr(ui, name, widget)
            form.addRow(name, widget)
        return ui

    def _make_widget(self, name: str, parent):
        lower = name.lower()
        if "textedit" in lower or "text_edit" in lower:
            widget = QTextEdit(parent)
            widget.setMinimumHeight(64)
        elif "combobox" in lower:
            widget = QComboBox(parent)
            self._configure_combo(name, widget)
        elif "video_minute" in lower:
            widget = QComboBox(parent)
            self._configure_combo(name, widget)
        elif lower.startswith(("cb_", "dl_cb_")) and lower.endswith("_mode"):
            widget = QComboBox(parent)
            self._configure_combo(name, widget)
        elif (
            lower.startswith(("checkbox_", "dl_checkbox_", "cb_", "dl_cb_"))
            and not lower.endswith("_mode")
        ):
            widget = QCheckBox(parent)
            widget.setText(name)
        elif "radiobutton" in lower:
            widget = QRadioButton(parent)
            widget.setText(name)
        elif "listediting" in lower or "listwidget" in lower:
            widget = QListWidget(parent)
            widget.setMinimumHeight(80)
        elif "lineedit" in lower or "line_edit" in lower:
            widget = QLineEdit(parent)
        elif lower in ("text_model", "number_model", "yulan_text_model"):
            widget = QLineEdit(parent)
        elif lower.endswith("_radius"):
            widget = QLineEdit(parent)
        elif lower.startswith(("btn_", "pushbutton_", "dl_btn_")):
            widget = QPushButton(name, parent)
        elif lower.startswith(("label_", "dl_label_")):
            widget = QLabel(name, parent)
            widget.setWordWrap(True)
        elif lower.startswith(("horizontalgroupbox_", "groupbox_")):
            widget = QGroupBox(name, parent)
        else:
            widget = QWidget(parent)
        widget.setObjectName(name)
        return widget

    @staticmethod
    def _configure_combo(name: str, combo: QComboBox) -> None:
        lower = name.lower()
        if "water_mode" in lower:
            combo.addItems([WATER_MODE_PIC, WATER_MODE_TEXT])
        elif "select_yulan_mode" in lower or "select_auto_flow_mode" in lower:
            combo.addItems([YULAN_MODE_PRESENT_TEXT, YULAN_MODE_DURATION_TEXT])
        elif "video_minute" in lower:
            for text, value in (
                ("不限制", 0),
                ("15分钟", 15),
                ("30分钟", 30),
                ("60分钟", 60),
            ):
                combo.addItem(text, value)
            combo.setCurrentIndex(3)
        elif "number_dan_wei" in lower or "number_random_dan_wei" in lower:
            combo.addItems([MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT, MESSAGE_NUMBER_DAN_WEI_SINGLE_TEXT])
        elif "select_mode" in lower:
            combo.addItems([MODE_RANDOM_TEXT, MODE_INCREASE_TEXT, MODE_LOOP_TEXT])

    def _widget(self, name: str | None):
        if not name:
            return None
        return getattr(getattr(self, "ui", None), name, None)

    def _text(self, name: str | None) -> str:
        widget = self._widget(name)
        if widget is None:
            return ""
        try:
            if hasattr(widget, "toPlainText"):
                return str(widget.toPlainText() or "").strip()
            if hasattr(widget, "text"):
                value = widget.text()
                if callable(value):
                    value = value()
                return str(value or "").strip()
            if hasattr(widget, "currentText"):
                return str(widget.currentText() or "").strip()
        except Exception:
            return ""
        return ""

    def _set_text(self, name: str | None, value: Any) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        text = "" if value is None else str(value)
        try:
            if hasattr(widget, "setPlainText"):
                widget.setPlainText(text)
            elif hasattr(widget, "setText"):
                widget.setText(text)
        except Exception:
            return

    def _checked(self, name: str | None) -> bool:
        widget = self._widget(name)
        if widget is None:
            return False
        try:
            return bool(widget.isChecked())
        except Exception:
            return False

    def _set_checked(self, name: str | None, value: bool) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        try:
            widget.setChecked(bool(value))
        except Exception:
            return

    def _set_enabled(self, name: str | None, value: bool) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        try:
            widget.setEnabled(bool(value))
        except Exception:
            return

    def _set_visible(self, name: str | None, value: bool) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        try:
            widget.setVisible(bool(value))
        except Exception:
            return

    def _combo(self, name: str | None):
        widget = self._widget(name)
        return widget if isinstance(widget, QComboBox) else None

    def _combo_text(self, name: str | None) -> str:
        combo = self._combo(name)
        if combo is None:
            return ""
        try:
            return str(combo.currentText() or "")
        except Exception:
            return ""

    def _set_combo_text(self, name: str | None, value: Any) -> None:
        combo = self._combo(name)
        if combo is None:
            return
        text = str(value or "")
        try:
            index = combo.findText(text)
            if index < 0:
                combo.addItem(text)
                index = combo.count() - 1
            combo.setCurrentIndex(index)
        except Exception:
            return

    def _combo_index(self, name: str | None) -> int:
        combo = self._combo(name)
        if combo is None:
            return 0
        try:
            return int(combo.currentIndex())
        except Exception:
            return 0

    def _combo_data(self, name: str | None, default=None):
        combo = self._combo(name)
        if combo is None:
            return default
        try:
            data = combo.currentData()
            return default if data is None else data
        except Exception:
            return default

    def _connect(self, name: str | None, signal: str, slot) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        try:
            getattr(widget, signal).connect(slot)
        except Exception:
            return

    def _connect_common_ui(self) -> None:
        if self._common_ui_connected:
            return
        self._common_ui_connected = True
        self._connect(self.SAVE_BUTTON, "clicked", self.saveYunYinItem)
        self._connect(self.AD_ADD_BUTTON, "clicked", self.addAd)
        self._connect(self.MODE_COMBO, "currentIndexChanged", self.changedModeUIComponent)
        self._connect(self.YULAN_MODE_COMBO, "currentIndexChanged", self.changedYulanModeUIComponent)
        self._connect(self.WATER_MODE_COMBO, "currentIndexChanged", self.changedWaterModeUIComponent)
        self._connect(self.AI_BUTTON, "clicked", self.on_select_ai_em)
        self._connect(self.WATER_SELECT_BUTTON, "clicked", self.on_select_pic)
        self._connect(self.RESOURCE_TUTORIAL_BUTTON, "clicked", self.showResourceTypeDialog)
        self._connect(self.RESOP_TUTORIAL_BUTTON, "clicked", self.showResOpDialog)
        self._connect(self.ACTION_TUTORIAL_BUTTON, "clicked", self.showActionTypeDialog)
        self._connect(self.TOPIC_TUTORIAL_BUTTON, "clicked", self.on_show_topic_jiao_chen)
        self._connect(self.PIC_WATER_TUTORIAL_BUTTON, "clicked", self.on_show_pic_water_jiao_chen)
        self._connect(self.GRID_TUTORIAL_BUTTON, "clicked", self.on_grid_jiao_chen)
        self._connect(self.COVER_TUTORIAL_BUTTON, "clicked", self.on_random_cover_jiao_chen)
        self._connect(self.HUIYUAN_TUTORIAL_BUTTON, "clicked", self.on_show_bq_font_jiao_chen)
        self._connect(self.YOUKE_TUTORIAL_BUTTON, "clicked", self.on_show_bq_font_jiao_chen)
        self._connect(self.AI_CHECK, "stateChanged", self.onAiEnableChanged)
        self._connect(self.AD_ENABLE_CHECK, "stateChanged", self.onAdEnableChanged)
        self._connect(self.KEEP_SOURCE_CHECK, "stateChanged", self.onKeepSourceChanged)
        self._connect(self.CHAI_ZU_CHECK, "stateChanged", self._chai_zu_component_states)
        self._connect(self.COPY_COMMENT_CHECK, "stateChanged", self.onCopyCommentChanged)
        self._connect(
            self.COMMENT_CONFIG_BUTTON,
            "clicked",
            self.configCommentRule,
        )
        self._connect(
            self.RESOURCE_FIELDS.get("video_photo"),
            "stateChanged",
            self.videoPhotoChanged,
        )
        self._connect(
            self.RESOURCE_FIELDS.get("photo"),
            "stateChanged",
            self.yunAutoChannelResTypeChanged,
        )
        self._connect(
            self.RESOURCE_FIELDS.get("video"),
            "stateChanged",
            self.yunAutoChannelResTypeChanged,
        )
        self._connect(
            self.HUIYUAN_ENABLE_CHECK,
            "stateChanged",
            self.onHuiYuanEnableChanged,
        )
        self._connect(
            self.HUIYUAN_CUSTOMER_CHECK,
            "stateChanged",
            self.onHuiYuanCustomerLinkChanged,
        )
        self._connect(self.YOUKE_ENABLE_CHECK, "stateChanged", self.onYouKeEnableChanged)
        for name in self.YULAN_RADIOS:
            self._connect(name, "toggled", self.yulanVideoCustomerChanged)

        widget = self._widget(self.AD_LIST)
        if widget is not None:
            try:
                widget.setContextMenuPolicy(Qt.CustomContextMenu)
                widget.customContextMenuRequested.connect(self.shoeMenu)
            except Exception:
                _ = None

        if self.AI_LABEL:
            self._set_text(self.AI_LABEL, "当前选择：无")

    def _connect_specific_ui(self) -> None:
        """Hook for dialog-specific signals; most are covered by class attrs."""
        return None

    def defaultFill(self) -> None:
        for name, value in self.DEFAULT_TEXTS.items():
            self._set_text(name, value)
        for name, value in self.DEFAULT_CHECKS.items():
            self._set_checked(name, value)
        for name, value in self.DEFAULT_COMBOS.items():
            self._set_combo_text(name, value)

        try:
            from ...config import YunYinMaoConfig

            duration_min = getattr(YunYinMaoConfig, "BASE_FILTER_DU_MIN", 0)
            duration_max = getattr(YunYinMaoConfig, "BASE_FILTER_DU_MAX", 6000)
            size_min = getattr(YunYinMaoConfig, "BASE_FILTER_SIZE_MIN", 0)
            size_max = getattr(YunYinMaoConfig, "BASE_FILTER_SIZE_MAX", 100000)
        except Exception:
            duration_min, duration_max = 0, 6000
            size_min, size_max = 0, 100000

        self._set_text(self.DURATION_MIN_FIELD, str(duration_min))
        self._set_text(self.DURATION_MAX_FIELD, str(duration_max))
        self._set_text(self.SIZE_MIN_FIELD, str(size_min))
        self._set_text(self.SIZE_MAX_FIELD, str(size_max))
        self._set_text(self.PRIORITY_FIELD, "100")
        self._set_text(self.WATER_RATIO_FIELD, "30")
        self._set_text(self.RESOP_RADIUS_FIELD, "3")
        self._set_text(self.RANDOM_COUNT_FIELD, "10")
        self._set_text(self.INCREASE_START_FIELD, "0")
        self._set_text(self.ACTION_SLEEP_MIN_FIELD, "3")
        self._set_text(self.ACTION_SLEEP_MAX_FIELD, "5")
        self._set_text(self.YULAN_MIN_FIELD, "60")
        self._set_text(self.YULAN_MAX_FIELD, "120")
        self._set_text(self.GRID_FIELD, "6")
        self._set_combo_text(self.MODE_COMBO, MODE_RANDOM_TEXT)
        self._set_combo_text(self.UNIT_COMBO, MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT)
        self._set_combo_text(
            self.RANDOM_UNIT_COMBO,
            MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        )
        self._set_combo_text(self.WATER_MODE_COMBO, WATER_MODE_PIC)
        self._set_combo_text(self.YULAN_MODE_COMBO, YULAN_MODE_PRESENT_TEXT)
        self._set_checked(self.AD_ENABLE_CHECK, True)
        self._set_checked(self.KEEP_SOURCE_CHECK, True)
        for name in self.RESOURCE_FIELDS.values():
            self._set_checked(name, True)
        if self.AI_CHECK:
            self._set_checked(self.AI_CHECK, False)
        if self.AI_SKIP_RADIO:
            self._set_checked(self.AI_SKIP_RADIO, True)
        self._set_text(self.WATER_PATH_LABEL, "未选择任何图片")
        self._set_text(self.AI_LABEL, "当前选择：无")
        self.showSelectMode()
        self.showYulanSelectMode()
        self.showWaterSelectMode()
        self._chai_zu_component_states()
        self.videoPhotoChanged()
        self.onAiEnableChanged(Qt.Checked if self._checked(self.AI_CHECK) else Qt.Unchecked)
        self.onAdEnableChanged(Qt.Checked if self._checked(self.AD_ENABLE_CHECK) else Qt.Unchecked)
        self.onHuiYuanEnableChanged(
            Qt.Checked if self._checked(self.HUIYUAN_ENABLE_CHECK) else Qt.Unchecked
        )
        self.onYouKeEnableChanged(
            Qt.Checked if self._checked(self.YOUKE_ENABLE_CHECK) else Qt.Unchecked
        )
        self.onHuiYuanCustomerLinkChanged(
            Qt.Checked if self._checked(self.HUIYUAN_CUSTOMER_CHECK) else Qt.Unchecked
        )
        self.onCopyCommentChanged(
            Qt.Checked if self._checked(self.COPY_COMMENT_CHECK) else Qt.Unchecked
        )
        self.yulanVideoCustomerChanged()

    def fillBeanIfNeed(self) -> None:
        bean = getattr(self, self.BEAN_ATTR, None)
        if bean is None:
            return
        self._fill_common_controls(bean)

    def _fill_common_controls(self, bean) -> None:
        name = str(getattr(bean, "name", "") or "")
        if self.isCopy and name and "(复制)" not in name:
            name += "(复制)"
        self._set_text(self.ITEM_NAME_FIELD, name)
        self._set_text(self.SOURCE_FIELD, getattr(bean, "source", ""))
        self._set_text(self.DB_CHANNEL_FIELD, getattr(bean, "db_channel", ""))
        self._set_text(self.DEST_FIELD, _join_destes(getattr(bean, "destes", [])))
        self._set_text(
            self.PREVIEW_DEST_FIELD,
            _join_destes(getattr(bean, "yulan_destes", [])),
        )
        self._set_text(self.PRIORITY_FIELD, str(getattr(bean, "priority", 100)))

        dtype = str(getattr(bean, "dtype", "") or "")
        if dtype:
            for key, field_name in self.RESOURCE_FIELDS.items():
                if key == "video_photo":
                    checked = dtype == RESOURCE_TYPE_VIDEO_PHOTO
                elif key == "photo":
                    checked = dtype == RESOURCE_TYPE_PHOTO
                elif key == "video":
                    checked = dtype == RESOURCE_TYPE_VIDEO
                elif key == "file":
                    checked = dtype == RESOURCE_TYPE_FILE
                else:
                    checked = dtype == RESOURCE_TYPE_TEXT
                self._set_checked(field_name, checked)

        self._fill_model_controls(getattr(bean, "modelWrapper", None))
        self._fill_filter_controls(bean)
        self._fill_water(getattr(bean, "water", None))
        self._fill_action(getattr(bean, "forWardAction", None))
        self._fill_resop(getattr(bean, "yuLanResOp", None))
        self._fill_yulan_mode(getattr(bean, "yuLanModeBean", None))
        self._fill_links(bean)
        self._fill_duration_info(getattr(bean, "durationInfo", None))
        self._fill_ai(
            getattr(bean, "aiEmployee", None),
            getattr(bean, "aiRefusedOpt", None),
        )
        self._fill_grid(getattr(bean, "grid", None), getattr(bean, "randomCover", False))
        self._fill_ads(getattr(bean, "selfAdWrapper", None))
        self._fill_comment(getattr(bean, "commentRule", None))
        self._fill_complete_version(getattr(bean, "completeVersionOp", None))
        self._fill_bot(getattr(bean, "botBean", None))

        self.showSelectMode()
        self.showYulanSelectMode()
        self.showWaterSelectMode()
        self._chai_zu_component_states()
        self.videoPhotoChanged()
        self.onAiEnableChanged(Qt.Checked if self._checked(self.AI_CHECK) else Qt.Unchecked)
        self.onCopyCommentChanged(
            Qt.Checked if self._checked(self.COPY_COMMENT_CHECK) else Qt.Unchecked
        )

    def _fill_model_controls(self, model) -> None:
        if model is None:
            return
        self._set_text(self.MODEL_FIELD, getattr(model, "model", ""))
        number_mode = getattr(model, "numberMode", "")
        self._set_text(self.NUMBER_MODEL_FIELD, number_mode)
        if getattr(model, "random", False):
            self._set_combo_text(self.MODE_COMBO, MODE_RANDOM_TEXT)
            self._set_text(self.RANDOM_COUNT_FIELD, getattr(model, "wantCount", ""))
            self._set_combo_text(
                self.RANDOM_UNIT_COMBO,
                _number_mode_text(number_mode),
            )
        elif getattr(model, "increase", False):
            self._set_combo_text(self.MODE_COMBO, MODE_INCREASE_TEXT)
            self._set_text(self.INCREASE_START_FIELD, getattr(model, "startId", ""))
            self._set_text(self.INCREASE_COUNT_FIELD, getattr(model, "wantCount", ""))
            self._set_combo_text(self.UNIT_COMBO, _number_mode_text(number_mode))
        elif getattr(model, "loop", False):
            self._set_combo_text(self.MODE_COMBO, MODE_LOOP_TEXT)
            self._set_text(self.LOOP_START_FIELD, getattr(model, "startId", ""))
            self._set_text(self.LOOP_END_FIELD, getattr(model, "endId", ""))

    def _fill_filter_controls(self, bean) -> None:
        advanced = getattr(bean, "advancedFilterBean", None)
        if advanced is not None:
            self._set_text(
                self.WORDS_CONTAIN_FIELD,
                _join_words(getattr(advanced, "containWords", [])),
            )
            self._set_text(
                self.WORDS_EXCLUDE_FIELD,
                _join_words(getattr(advanced, "excludeWords", [])),
            )
        base = getattr(bean, "baseFilter", None)
        if base is not None:
            duration = getattr(base, "durationFilterBean", None)
            size = getattr(base, "sizeFilterBean", None)
            if duration is not None:
                self._set_text(self.DURATION_MIN_FIELD, getattr(duration, "min", ""))
                self._set_text(self.DURATION_MAX_FIELD, getattr(duration, "max", ""))
            if size is not None:
                self._set_text(self.SIZE_MIN_FIELD, getattr(size, "min", ""))
                self._set_text(self.SIZE_MAX_FIELD, getattr(size, "max", ""))
            self._set_checked(self.KEEP_SOURCE_CHECK, bool(getattr(base, "keepSourceText", True)))
            self._set_checked(
                self._find_field("dele_source_text"),
                bool(getattr(base, "deleSourceText", False)),
            )
            self._set_checked(
                self._find_field("dele_link"),
                bool(getattr(base, "deleLink", False)),
            )
            self._set_checked(
                self._find_field("fliter_button"),
                bool(getattr(base, "filterButton", False)),
            )
            self._set_checked(
                "checkBox_discard_no_text_resource",
                bool(getattr(base, "discardNoTextResource", False)),
            )
            self._set_checked(self.CHAI_ZU_CHECK, bool(getattr(base, "chaiZu", False)))
        tail = getattr(bean, "tail", None)
        if tail is not None:
            self._set_text(self.TAIL_FIELD, getattr(tail, "tail_text", ""))
        replace = getattr(bean, "replace", None)
        if replace is not None:
            self._set_text(
                self.REPLACE_FIELD,
                _join_replaces(getattr(replace, "replaces", [])),
            )

    def _find_field(self, keyword: str) -> str | None:
        for name in self.WIDGET_NAMES:
            lower = name.lower()
            if keyword in lower and (
                lower.startswith("checkbox_")
                or lower.startswith("cb_")
                or lower.startswith("dl_checkbox_")
                or lower.startswith("dl_cb_")
            ):
                return name
        return None

    def _fill_water(self, water) -> None:
        if water is None:
            return
        self.water = water
        self._set_checked(self.WATER_PIC_CHECK, bool(getattr(water, "enPic", False)))
        self._set_checked(self.WATER_VIDEO_CHECK, bool(getattr(water, "enVideo", False)))
        self._set_text(self.WATER_TEXT_FIELD, getattr(water, "text", ""))
        self._set_combo_text(
            self.WATER_MODE_COMBO,
            getattr(water, "mode", "") or WATER_MODE_PIC,
        )
        self._set_text(self.WATER_RATIO_FIELD, str(getattr(water, "picRatio", 30) or 30))
        self.picPath = str(getattr(water, "picPath", "") or "")
        self.picRatio = int(getattr(water, "picRatio", 30) or 30)
        if self.picPath:
            self.set_elided_path(self.picPath)
        else:
            self._set_text(self.WATER_PATH_LABEL, "未选择任何图片")
        combo = self._combo(self.WATER_DURATION_COMBO)
        if combo is not None:
            try:
                index = combo.findData(int(getattr(water, "duration", 60) or 0))
                combo.setCurrentIndex(index if index >= 0 else _video_duration_index(
                    getattr(water, "duration", 60)
                ))
            except Exception:
                _ = None

    def _fill_action(self, action) -> None:
        if action is None:
            return
        value = str(getattr(action, "action", "") or "")
        self._set_checked(self.ACTION_AUTO_RADIO, value == ACTION_AUTO)
        self._set_checked(self.ACTION_DOWNLOAD_RADIO, value == ACTION_DOWNLOAD)
        self._set_text(
            self.ACTION_SLEEP_MIN_FIELD,
            getattr(action, "randon_sleep_min", ""),
        )
        self._set_text(
            self.ACTION_SLEEP_MAX_FIELD,
            getattr(action, "randon_sleep_max", ""),
        )

    def _fill_resop(self, resop) -> None:
        if resop is None:
            return
        self._set_checked(self.RESOP_BLUR_CHECK, bool(getattr(resop, "picBlur", False)))
        self._set_checked(self.RESOP_SPOILER_CHECK, bool(getattr(resop, "spoiler", False)))
        self._set_text(self.RESOP_RADIUS_FIELD, str(getattr(resop, "radius", 3) or 3))

    def _fill_yulan_mode(self, mode_bean) -> None:
        if mode_bean is None or not self.YULAN_MODE_COMBO:
            return
        mode = str(getattr(mode_bean, "mode", "") or "")
        self._set_combo_text(
            self.YULAN_MODE_COMBO,
            YULAN_MODE_DURATION_TEXT if mode == YULAN_MODE_DURATION else YULAN_MODE_PRESENT_TEXT,
        )
        present_obj = getattr(mode_bean, "presentMode", None)
        present = getattr(present_obj, "present", present_obj)
        if present not in (None, ""):
            text = str(present)
            matched = False
            for name in self.YULAN_RADIOS:
                value = self._radio_value(name)
                if value and value == text:
                    self._set_checked(name, True)
                    matched = True
                    break
            if not matched and self.YULAN_CUSTOM_RADIO:
                self._set_checked(self.YULAN_CUSTOM_RADIO, True)
                self._set_text(self.YULAN_CUSTOM_FIELD, text)
        duration_obj = getattr(mode_bean, "durationMode", None)
        if duration_obj is not None:
            self._set_text(
                self.YULAN_MIN_FIELD,
                getattr(duration_obj, "duration_min_second", ""),
            )
            self._set_text(
                self.YULAN_MAX_FIELD,
                getattr(duration_obj, "duration_max_second", ""),
            )
        self.yulanVideoCustomerChanged()

    def _fill_links(self, bean) -> None:
        huiyuan = getattr(bean, "huiYuanLink", None)
        if huiyuan is not None:
            self._set_checked(
                self.HUIYUAN_ENABLE_CHECK,
                bool(getattr(huiyuan, "enable", False)),
            )
            self._set_text(self.HUIYUAN_TEXT_FIELD, getattr(huiyuan, "text", ""))
            self._set_checked(
                self.HUIYUAN_CUSTOMER_CHECK,
                bool(getattr(huiyuan, "enableCustomerLink", False)),
            )
            self._set_text(
                self.HUIYUAN_LINK_FIELD,
                getattr(huiyuan, "customerHttpLink", ""),
            )
            self._set_checked(
                self.HUIYUAN_BQ_CHECK,
                bool(getattr(huiyuan, "blockquote", False)),
            )
        youke = getattr(bean, "youKeLink", None)
        if youke is not None:
            self._set_checked(self.YOUKE_ENABLE_CHECK, bool(getattr(youke, "enable", False)))
            self._set_text(self.YOUKE_TEXT_FIELD, getattr(youke, "text", ""))
            self._set_text(self.YOUKE_LINK_FIELD, getattr(youke, "httpLink", ""))
            self._set_checked(self.YOUKE_BQ_CHECK, bool(getattr(youke, "blockquote", False)))
        self.onHuiYuanEnableChanged(
            Qt.Checked if self._checked(self.HUIYUAN_ENABLE_CHECK) else Qt.Unchecked
        )
        self.onHuiYuanCustomerLinkChanged(
            Qt.Checked if self._checked(self.HUIYUAN_CUSTOMER_CHECK) else Qt.Unchecked
        )
        self.onYouKeEnableChanged(
            Qt.Checked if self._checked(self.YOUKE_ENABLE_CHECK) else Qt.Unchecked
        )

    def _fill_duration_info(self, info) -> None:
        if info is None:
            return
        self._set_checked(
            self.ADD_DURATION_CHECK,
            bool(getattr(info, "addDurationInfo", False)),
        )
        self._set_checked(
            self.ADD_DURATION_BQ_CHECK,
            bool(getattr(info, "blockquote", False)),
        )

    def _fill_ai(self, employee, refused) -> None:
        if employee is not None:
            self.aiEmployee = employee
            self._set_checked(self.AI_CHECK, bool(getattr(employee, "enable", False)))
            name = getattr(employee, "name", "")
            if not name:
                try:
                    from ...dclass import LoadEmployeeClass

                    name = LoadEmployeeClass.getAiEmployeeName(
                        getattr(employee, "uid", "")
                    )
                except Exception:
                    name = "无"
            self._set_text(self.AI_LABEL, "当前选择：" + str(name or "无"))
        if refused is not None:
            skip = False
            keep = False
            try:
                skip = bool(refused.is_skip_group())
                keep = bool(refused.is_keep_origin_source())
            except Exception:
                action = str(getattr(refused, "action", "") or "")
                skip = action == "skip"
                keep = action in ("origin", "keep")
            self._set_checked(self.AI_SKIP_RADIO, skip)
            self._set_checked(self.AI_USE_RADIO, keep)
        self.onAiEnableChanged(Qt.Checked if self._checked(self.AI_CHECK) else Qt.Unchecked)

    def _fill_grid(self, grid, random_cover: bool) -> None:
        if grid is not None:
            self._set_text(self.GRID_FIELD, str(getattr(grid, "number", 6) or 0))
        self._set_checked(self.GRID_COVER_FIELD, bool(random_cover))

    def _fill_ads(self, wrapper) -> None:
        if wrapper is None:
            return
        self.selfAdWrapper = wrapper
        ads = getattr(wrapper, "ades", None)
        if not ads:
            ads = getattr(wrapper, "values", [])
        self.adMap = {
            getattr(ad, "adId", index): ad
            for index, ad in enumerate(ads or [])
        }
        self._set_checked(self.AD_ENABLE_CHECK, bool(getattr(wrapper, "adEnable", True)))
        self._set_checked(
            self._find_field("ad_is_bottom_up"),
            bool(getattr(wrapper, "adIsBottomUp", False)),
        )
        self._set_checked(
            self._find_field("ad_delete"),
            bool(getattr(wrapper, "delete", False)),
        )
        self.onAdEnableChanged(Qt.Checked if self._checked(self.AD_ENABLE_CHECK) else Qt.Unchecked)

    def _fill_comment(self, comment) -> None:
        if comment is None:
            return
        self.commentRule = comment
        self._set_checked(
            self.COPY_COMMENT_CHECK,
            bool(getattr(comment, "copyComment", False)),
        )
        self.onCopyCommentChanged(
            Qt.Checked if self._checked(self.COPY_COMMENT_CHECK) else Qt.Unchecked
        )

    def _fill_complete_version(self, op) -> None:
        if op is None:
            return
        self._set_text(self.COMPLETE_VERSION_FIELD, getattr(op, "linkText", ""))
        self._set_checked(
            self.COMPLETE_BLOCKQUOTE_CHECK,
            bool(getattr(op, "blockquote", False)),
        )

    def _fill_bot(self, bot) -> None:
        if bot is None:
            return
        self._set_text(self.BOT_FIELD, getattr(bot, "user_name", ""))

    def showSelectMode(self, *_args) -> None:
        index = self._combo_index(self.MODE_COMBO)
        text = self._combo_text(self.MODE_COMBO)
        random_mode = text == MODE_RANDOM_TEXT or (not text and index == 0)
        increase_mode = text == MODE_INCREASE_TEXT or (not text and index == 1)
        loop_mode = text == MODE_LOOP_TEXT or (not text and index == 2)
        self._set_visible(self.RANDOM_WRAPPER, random_mode)
        self._set_visible(self.INCREASE_WRAPPER, increase_mode)
        self._set_visible(self.LOOP_WRAPPER, loop_mode)

    def changedModeUIComponent(self, *_args) -> None:
        self.showSelectMode()

    def showYulanSelectMode(self, *_args) -> None:
        mode = self._combo_text(self.YULAN_MODE_COMBO)
        duration_mode = mode == YULAN_MODE_DURATION_TEXT
        if self.YULAN_MODE_COMBO:
            self._set_visible(self.PRESENT_CONTAINER, not duration_mode)
            self._set_visible(self.DURATION_CONTAINER, duration_mode)

    def changedYulanModeUIComponent(self, *_args) -> None:
        self.showYulanSelectMode()

    def showWaterSelectMode(self, *_args) -> None:
        mode = self._combo_text(self.WATER_MODE_COMBO)
        text_mode = mode == WATER_MODE_TEXT
        self._set_visible(self.TEXT_WATER_WRAPPER, text_mode)
        self._set_visible(self.PIC_WATER_WRAPPER, not text_mode)

    def changedWaterModeUIComponent(self, *_args) -> None:
        self.showWaterSelectMode()

    def initCheckBoxControlQuYu(self) -> None:
        self._connect_common_ui()

    def onAiEnableChanged(self, state=None, *_args) -> None:
        self._set_enabled(self.AI_GROUP, bool(state))

    def onAdEnableChanged(self, state=None, *_args) -> None:
        self._set_enabled(self.AD_LIST, bool(state))

    def onKeepSourceChanged(self, state=None, *_args) -> None:
        if bool(state):
            self._set_checked(self._find_field("dele_source_text"), False)

    def onCopyCommentChanged(self, state=None, *_args) -> None:
        self._set_enabled(self.COMMENT_CONFIG_BUTTON, bool(state))

    def _chai_zu_component_states(self, *_args) -> None:
        chai_zu = self._checked(self.CHAI_ZU_CHECK)
        for key in ("photo", "video"):
            widget = self._widget(self.RESOURCE_FIELDS.get(key))
            if widget is None:
                continue
            try:
                policy = widget.sizePolicy()
                policy.setRetainSizeWhenHidden(True)
                widget.setSizePolicy(policy)
                widget.setVisible(not chai_zu)
            except Exception:
                continue

    def videoPhotoChanged(self, *_args) -> None:
        video_photo = self._checked(self.RESOURCE_FIELDS.get("video_photo"))
        self._set_enabled(self.RESOURCE_FIELDS.get("photo"), not video_photo)
        self._set_enabled(self.RESOURCE_FIELDS.get("video"), not video_photo)

    def flowVideoPhotoChanged(self, *_args) -> None:
        return self.videoPhotoChanged(*_args)

    def howBqFontCourse(self) -> None:
        return self._run_course("unifyShowBqFontCourse")

    def yulanVideoPhotoChanged(self, *_args) -> None:
        self.videoPhotoChanged()

    def yunAutoVideoPhotoTypeChanged(self, *_args) -> None:
        self.videoPhotoChanged()

    def yunAutoChannelResTypeChanged(self, *_args) -> None:
        self.videoPhotoChanged()

    def yulanVideoCustomerChanged(self, *_args) -> None:
        custom = self._checked(self.YULAN_CUSTOM_RADIO)
        self._set_enabled(self.YULAN_CUSTOM_FIELD, custom)

    def onHuiYuanEnableChanged(self, state=None, *_args) -> None:
        enabled = bool(state)
        self._set_enabled(self.HUIYUAN_TEXT_FIELD, enabled)
        self._set_enabled(self.HUIYUAN_CUSTOMER_CHECK, enabled)
        self._set_enabled(self.HUIYUAN_BQ_CHECK, enabled)
        self.onHuiYuanCustomerLinkChanged(
            Qt.Checked if self._checked(self.HUIYUAN_CUSTOMER_CHECK) else Qt.Unchecked
        )

    def onHuiYuanCustomerLinkChanged(self, state=None, *_args) -> None:
        enabled = bool(state) and self._checked(self.HUIYUAN_ENABLE_CHECK)
        self._set_enabled(self.HUIYUAN_LINK_FIELD, enabled)

    def onYouKeEnableChanged(self, state=None, *_args) -> None:
        enabled = bool(state)
        self._set_enabled(self.YOUKE_TEXT_FIELD, enabled)
        self._set_enabled(self.YOUKE_LINK_FIELD, enabled)
        self._set_enabled(self.YOUKE_BQ_CHECK, enabled)

    def on_select_ai_em_callback(self, em) -> None:
        self.aiEmployee = em
        if em is not None:
            self.employee_id = getattr(em, "uid", self.employee_id)
        name = getattr(em, "name", "无") if em is not None else "无"
        self._set_text(self.AI_LABEL, "当前选择：" + str(name))

    def on_select_ai_em(self) -> None:
        try:
            from ...fea import _sq_jqm
        except Exception:
            _sq_jqm = None
        if _sq_jqm is not None:
            try:
                if _sq_jqm.has_ai_ability_but_no_key():
                    print("你还没有配置专属的AI API KEY")
                    self._run_course("unifyShowInputApiKeyCourse")
                    return
            except Exception:
                _ = None
        try:
            from ...tgaccount import AiEmployeeListDialog

            dialog = AiEmployeeListDialog(self, self.on_select_ai_em_callback)
            dialog.exec_()
        except Exception as exc:
            print("打开AI员工列表失败：", exc)

    def on_select_pic(self) -> None:
        file_filter = "图片文件 (*.jpg *.jpeg *.png)"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            file_filter,
        )
        if not file_path:
            self._set_text(self.WATER_PATH_LABEL, "未选择任何图片")
            widget = self._widget(self.WATER_PATH_LABEL)
            if widget is not None:
                try:
                    widget.setToolTip("")
                except Exception:
                    _ = None
            return
        self.temp_water_image_abs_path = file_path
        self.picPath = file_path
        self.set_elided_path(file_path)

    def set_elided_path(self, full_path: str) -> None:
        try:
            from ...auto import CMCode

            elided_text = CMCode.elide_path_middle(full_path, 40)
        except Exception:
            elided_text = full_path
        self._set_text(self.WATER_PATH_LABEL, "图片路径：" + str(elided_text))
        widget = self._widget(self.WATER_PATH_LABEL)
        if widget is not None:
            try:
                widget.setToolTip(full_path)
            except Exception:
                _ = None

    def _run_course(self, function_name: str) -> None:
        try:
            from ...dialog import ImageDialogHelper
            from . import ShotUtils

            function = getattr(ImageDialogHelper, function_name)
            function(ShotUtils.shot(self))
        except Exception as exc:
            print("打开教程失败：", exc)

    def showResOpDialog(self) -> None:
        self._run_course(self.RES_OP_COURSE)

    def showYulanResOpDialog(self) -> None:
        return self.showResOpDialog()

    def showBotBqFontCourse(self) -> None:
        return self._run_course("unifyShowBqFontCourse")

    def showActionTypeDialog(self) -> None:
        self._run_course(self.ACTION_COURSE)

    def on_show_topic_jiao_chen(self) -> None:
        self._run_course(self.TOPIC_COURSE)

    def showChannelTopicDialog(self) -> None:
        self._run_course(self.TOPIC_COURSE)

    def showDbChannelDialog(self) -> None:
        self._run_course(self.TOPIC_COURSE)

    def showResourceTypeDialog(self) -> None:
        self._run_course("unifyShowResTypeCourse")

    def on_grid_jiao_chen(self) -> None:
        self._run_course("unifyShowGridCourse")

    def on_random_cover_jiao_chen(self) -> None:
        self._run_course("unifyShowRandomCoverCourse")

    def on_show_pic_water_jiao_chen(self) -> None:
        self._run_course("unifyShowPicWaterCourse")

    def on_show_bq_font_jiao_chen(self) -> None:
        self._run_course("unifyShowBqFontCourse")

    def on_show_bot_bq_font_jiao_chen(self) -> None:
        self._run_course("unifyShowBotBqFontCourse")

    def on_show_duration_jiao_chen(self) -> None:
        self._run_course("unifyShowDurationCourse")

    def shoeMenu(self, pos) -> None:
        widget = self._widget(self.AD_LIST)
        if widget is None:
            return
        item = widget.itemAt(pos)
        if item is None:
            return
        ad = item.data(Qt.UserRole)
        if ad is None:
            ad = item.data(32)
        menu = QMenu(widget)
        edit = QAction("编辑私有广告", menu)
        delete = QAction("删除私有广告", menu)
        edit.triggered.connect(lambda _=False, value=ad: self.editItem(value))
        delete.triggered.connect(lambda _=False, value=ad: self.deleteItem(value))
        menu.addAction(edit)
        menu.addAction(delete)
        menu.exec_(widget.mapToGlobal(pos))

    def addAd(self) -> None:
        try:
            from ...ad import AddOrEditAdDialog

            dialog = AddOrEditAdDialog(
                self,
                "添加私有广告",
                self.ad_call_back,
                None,
                self.kid,
            )
            dialog.exec_()
        except Exception as exc:
            print("添加私有广告失败：", exc)

    def editItem(self, ad) -> None:
        if ad is None:
            return
        try:
            from ...ad import AddOrEditAdDialog

            dialog = AddOrEditAdDialog(
                self,
                "编辑私有广告",
                self.ad_call_back,
                ad,
                self.kid,
            )
            dialog.exec_()
        except Exception as exc:
            print("编辑私有广告失败：", exc)

    def deleteItem(self, ad) -> None:
        if ad is None:
            return
        key = getattr(ad, "adId", id(ad))
        self.adMap.pop(key, None)
        self.fillAdList()

    def ad_call_back(self, ad) -> None:
        if ad is None:
            return
        self.adMap[getattr(ad, "adId", id(ad))] = ad
        self.fillAdList()

    def fillAdList(self) -> None:
        widget = self._widget(self.AD_LIST)
        if widget is None:
            return
        ads = list(self.adMap.values())
        try:
            from ...ad import UIAdListOp

            UIAdListOp.fillAd2List(ads, widget)
        except Exception:
            try:
                widget.clear()
                for ad in ads:
                    item = QListWidgetItem(str(getattr(ad, "name", "") or ""))
                    item.setData(Qt.UserRole, ad)
                    widget.addItem(item)
            except Exception:
                return

    def configCommentRule(self) -> None:
        try:
            from ...comment.ConfigCommentRuleDialog import ConfigCommentRuleDialog

            dialog = ConfigCommentRuleDialog(
                self,
                "配置评论区复刻规则",
                self.comment_rule_call_back,
                self.commentRule,
            )
            dialog.exec_()
        except Exception as exc:
            print("打开评论区复刻规则失败：", exc)

    def comment_rule_call_back(self, rule) -> None:
        self.commentRule = rule
        print("更新评论区搬运规则成功！")

    def saveYunYinItem(self) -> None:
        context = self._collect_common_save_values()
        if context is None:
            return
        bean = getattr(self, self.BEAN_ATTR, None)
        if bean is None:
            bean = self._coerce_bean(None)
            setattr(self, self.BEAN_ATTR, bean)
        self._apply_common_bean_fields(bean, context)
        self._persist_bean(bean)

    def _collect_common_save_values(self):
        identity = self._read_identity()
        if identity is None:
            return None
        dtype = self._build_dtype()
        if dtype is None:
            return None
        model = self._build_model_wrapper()
        if model is None:
            return None
        filters = self._build_filter_bundle()
        water = self._build_water()
        if water is None:
            return None
        action = self._build_action()
        if self.ACTION_AUTO_RADIO and action is None:
            return None
        resop = self._build_res_op()
        if self.RESOP_RADIUS_FIELD and resop is None:
            return None
        yulan_mode = self._build_yulan_mode()
        if self.YULAN_MODE_COMBO and yulan_mode is None:
            return None
        links = self._build_links()
        if links is None:
            return None
        comment = self._build_comment_rule()
        if self.COPY_COMMENT_CHECK and comment is None:
            return None
        complete = self._build_complete_version()
        if self.COMPLETE_VERSION_FIELD and complete is None:
            return None
        bot = self._build_bot()
        if self.BOT_FIELD and bot is None:
            return None
        ai = self._build_ai()
        if ai is None:
            return None
        grid, random_cover = self._build_grid()
        ads = self._build_ads()
        name_priority = self._read_name_priority()
        if name_priority is None:
            return None
        name, priority = name_priority
        return {
            **identity,
            "dtype": dtype,
            "model": model,
            "base_filter": filters[0],
            "advanced_filter": filters[1],
            "tail": filters[2],
            "replace": filters[3],
            "duration_info": self._build_duration_info(),
            "water": water,
            "action": action,
            "resop": resop,
            "yulan_mode": yulan_mode,
            "huiyuan_link": links[0],
            "youke_link": links[1],
            "comment_rule": comment,
            "complete_version": complete,
            "bot": bot,
            "ai_employee": ai[0],
            "ai_refused": ai[1],
            "grid": grid,
            "random_cover": random_cover,
            "ads": ads,
            "name": name,
            "priority": priority,
        }

    def _read_identity(self):
        source = self._text(self.SOURCE_FIELD)
        if not source:
            print(self.SOURCE_REQUIRED_MESSAGE)
            return None
        if not utils.is_legal_source(source):
            print(self.SOURCE_REQUIRED_MESSAGE)
            return None
        try:
            valid, _ = utils.strict_check_source(source, self.SOURCE_REQUIRED_MESSAGE)
        except Exception:
            valid = True
        if not valid:
            print(self.SOURCE_REQUIRED_MESSAGE)
            return None

        db_channel = self._text(self.DB_CHANNEL_FIELD)
        if self.DB_CHANNEL_FIELD and not db_channel:
            print(self.DB_CHANNEL_REQUIRED_MESSAGE)
            return None
        destes: list[str] = []
        if self.DEST_FIELD:
            dest_text = self._text(self.DEST_FIELD)
            destes = _split_destes(dest_text)
            if not destes:
                print(self.DEST_REQUIRED_MESSAGE)
                return None
        yulan_destes: list[str] = []
        if self.PREVIEW_DEST_FIELD:
            preview_text = self._text(self.PREVIEW_DEST_FIELD)
            yulan_destes = _split_destes(preview_text)
            if not yulan_destes:
                print(self.PREVIEW_DEST_REQUIRED_MESSAGE)
                return None
        return {
            "source": source,
            "db_channel": db_channel,
            "destes": destes,
            "yulan_destes": yulan_destes,
        }

    def _read_name_priority(self):
        name = self._text(self.ITEM_NAME_FIELD)
        if not name:
            print(self._name_required_message())
            return None
        if self.isCopy and "(复制)" not in name:
            name += "(复制)"
        priority_text = self._text(self.PRIORITY_FIELD)
        priority = 100
        if priority_text:
            ok, value = _parse_int(priority_text)
            if not ok:
                print(self.PRIORITY_MESSAGE)
                return None
            priority = value
        return name, priority

    def _name_required_message(self) -> str:
        return "请给条目取一个名字吧，方便你后续管理！"

    def _build_dtype(self) -> str | None:
        if self._checked(self.RESOURCE_FIELDS.get("video_photo")):
            return RESOURCE_TYPE_VIDEO_PHOTO
        if self._checked(self.RESOURCE_FIELDS.get("photo")):
            return RESOURCE_TYPE_PHOTO
        if self._checked(self.RESOURCE_FIELDS.get("video")):
            return RESOURCE_TYPE_VIDEO
        if self._checked(self.RESOURCE_FIELDS.get("file")):
            return RESOURCE_TYPE_FILE
        if self._checked(self.RESOURCE_FIELDS.get("text")):
            return RESOURCE_TYPE_TEXT
        print("资源类型必须选择一个！")
        return None

    def _build_model_wrapper(self) -> ModelWrapper | None:
        model_text = self._text(self.MODEL_FIELD)
        if not self.MODE_COMBO:
            return ModelWrapper(model=model_text)
        text = self._combo_text(self.MODE_COMBO)
        index = self._combo_index(self.MODE_COMBO)
        random_mode = text == MODE_RANDOM_TEXT or (not text and index == 0)
        increase_mode = text == MODE_INCREASE_TEXT or (not text and index == 1)
        loop_mode = text == MODE_LOOP_TEXT or (not text and index == 2)
        wrapper = ModelWrapper(
            model=model_text,
            random=random_mode,
            increase=increase_mode,
            loop=loop_mode,
        )
        try:
            from ...config import YunYinMaoConfig

            random_max = getattr(YunYinMaoConfig, "RAN_DOM_MODEL_WANT_COUNT_MAX", 1000)
            increase_max = getattr(YunYinMaoConfig, "INCREASE_MODEL_WANT_COUNT_MAX", 1000)
            loop_max = getattr(YunYinMaoConfig, "LOOP_MODE_REGION_COUNT_MAX", 1000)
        except Exception:
            random_max = increase_max = loop_max = 1000

        if random_mode:
            ok, count = _parse_int(self._text(self.RANDOM_COUNT_FIELD))
            if not ok:
                print("请输入随机模式期望数量，需要输入整数！")
                return None
            if count <= 0:
                print("随机模式期望数量 必须大于0！")
                return None
            if count > random_max:
                print("随机模式期望数量最大不能超过", random_max)
                return None
            wrapper.wantCount = count
            wrapper.numberMode = _number_mode_value(
                self._combo_text(self.RANDOM_UNIT_COMBO)
            )
        elif increase_mode:
            ok, start_id = _parse_int(self._text(self.INCREASE_START_FIELD))
            if not ok:
                print("请输入顺序模式开始ID，需要输入整数！")
                return None
            if start_id < 0:
                print("顺序模式开始ID 必须大于或等于0！")
                return None
            ok, want_count = _parse_int(self._text(self.INCREASE_COUNT_FIELD))
            if not ok:
                print("请输入顺序模式期望数量，需要输入整数！")
                return None
            if want_count <= 0:
                print("顺序模式期望数量 必须大于0！")
                return None
            if want_count > increase_max:
                print("顺序模式期望数量最大不能超过", increase_max, "！")
                return None
            wrapper.startId = start_id
            wrapper.wantCount = want_count
            wrapper.numberMode = _number_mode_value(self._combo_text(self.UNIT_COMBO))
        elif loop_mode:
            ok, start_id = _parse_int(self._text(self.LOOP_START_FIELD))
            if not ok:
                print("请输入循环模式开始ID，需要输入整数！")
                return None
            if start_id < 0:
                print("循环模式开始ID 必须大于或等于0！")
                return None
            ok, end_id = _parse_int(self._text(self.LOOP_END_FIELD))
            if not ok:
                print("请输入循环模式结束ID，需要输入整数！")
                return None
            if end_id <= 0:
                print("循环模式结束ID 必须大于0！")
                return None
            if end_id <= start_id:
                print("循环模式结束ID 必须大于 开始ID！")
                return None
            if end_id - start_id > loop_max:
                print("循环模式开始ID和结束ID间隔不能大于", loop_max)
                return None
            wrapper.startId = start_id
            wrapper.endId = end_id
        return wrapper

    def _build_filter_bundle(self):
        duration_min = _safe_int(self._text(self.DURATION_MIN_FIELD), 0)
        duration_max = _safe_int(self._text(self.DURATION_MAX_FIELD), 6000)
        size_min = _safe_int(self._text(self.SIZE_MIN_FIELD), 0)
        size_max = _safe_int(self._text(self.SIZE_MAX_FIELD), 100000)
        duration_filter = DurationFilterBean(
            duration_min=duration_min,
            duration_max=duration_max,
            duration_min_second=duration_min * 60,
            duration_max_second=duration_max * 60,
        )
        size_filter = SizeFilterBean(min=size_min, max=size_max)
        contain_words = _split_words(self._text(self.WORDS_CONTAIN_FIELD))
        exclude_words = _split_words(self._text(self.WORDS_EXCLUDE_FIELD))
        base_filter = BaseFilterBean(
            durationFilterBean=duration_filter,
            sizeFilterBean=size_filter,
        )
        advanced = AdvancedFilterBean(
            keepSourceText=self._checked(self.KEEP_SOURCE_CHECK),
            deleSourceText=self._checked(self._find_field("dele_source_text")),
            deleLink=self._checked(self._find_field("dele_link")),
            filterButton=self._checked(self._find_field("fliter_button")),
            discardNoTextResource=self._checked(
                "checkBox_discard_no_text_resource"
            ),
            chaiZu=self._checked(self.CHAI_ZU_CHECK),
            containWords=contain_words,
            excludeWords=exclude_words,
        )
        tail = Tail(tail_text=self._text(self.TAIL_FIELD))
        replace = Replace(replaces=_split_replaces(self._text(self.REPLACE_FIELD)))
        return base_filter, advanced, tail, replace

    def _build_duration_info(self):
        if not self.ADD_DURATION_CHECK:
            return None
        return AddDurationInfo(
            addDurationInfo=self._checked(self.ADD_DURATION_CHECK),
            blockquote=self._checked(self.ADD_DURATION_BQ_CHECK),
        )

    def _build_water(self) -> Water | None:
        if not self.WATER_MODE_COMBO:
            return None
        mode = self._combo_text(self.WATER_MODE_COMBO) or WATER_MODE_PIC
        en_pic = self._checked(self.WATER_PIC_CHECK)
        en_video = self._checked(self.WATER_VIDEO_CHECK)
        ok, ratio = _parse_int(self._text(self.WATER_RATIO_FIELD))
        if not ok or ratio < 10 or ratio > 90:
            print(
                "请输入正整数，表示图片水印图片缩放百分比，范围是10~90！"
                "建议是输入30！"
            )
            return None
        water_pic_path = self.temp_water_image_abs_path or self.picPath
        if mode == WATER_MODE_PIC and (en_pic or en_video):
            if not water_pic_path:
                print("请选择图片水印的图片资源！")
                return None
            if not Path(water_pic_path).exists():
                print("图片水印的图片资源不存在：", water_pic_path)
                return None
        water_text = self._text(self.WATER_TEXT_FIELD)
        if mode == WATER_MODE_TEXT and (en_pic or en_video) and not water_text:
            print("请输入水印，支持中文，英文！")
            return None
        duration = self._combo_data(self.WATER_DURATION_COMBO)
        if duration is None:
            duration = _video_duration(self._combo_index(self.WATER_DURATION_COMBO))
        return Water(
            enPic=en_pic,
            enVideo=en_video,
            text=water_text,
            picPath=water_pic_path,
            mode=mode,
            duration=_safe_int(duration, 60),
            picRatio=ratio,
        )

    def _build_action(self):
        if not self.ACTION_AUTO_RADIO:
            return None
        action_auto = self._checked(self.ACTION_AUTO_RADIO)
        action_download = self._checked(self.ACTION_DOWNLOAD_RADIO)
        if not action_auto and not action_download:
            print("搬运方式必须选择一个！")
            return None
        ok, sleep_min = _parse_int(self._text(self.ACTION_SLEEP_MIN_FIELD))
        if not ok:
            print("请输入随机休眠最小值，需要输入整数！（单位秒）")
            return None
        if sleep_min <= 0:
            print("随机休眠最小值不能小于等于0！")
            return None
        ok, sleep_max = _parse_int(self._text(self.ACTION_SLEEP_MAX_FIELD))
        if not ok:
            print("请输入随机休眠最大值，需要输入整数！（单位秒）")
            return None
        if sleep_max < sleep_min:
            print("随机休眠最大值不能小于最小值！")
            return None
        return ForwardActionBean(
            action=ACTION_AUTO if action_auto else ACTION_DOWNLOAD,
            randon_sleep_min=sleep_min,
            randon_sleep_max=sleep_max,
        )

    def _build_res_op(self):
        if not self.RESOP_RADIUS_FIELD:
            return None
        ok, radius = _parse_int(self._text(self.RESOP_RADIUS_FIELD))
        if not ok or radius < 1 or radius > 20:
            print(
                "请输入模糊数值，需要输入整数！（值越大越模糊，范围是1~20，"
                "建议输入3）"
            )
            return None
        return YuLanResOp(
            picBlur=self._checked(self.RESOP_BLUR_CHECK),
            spoiler=self._checked(self.RESOP_SPOILER_CHECK),
            radius=radius,
        )

    def _selected_yulan_radio(self) -> str | None:
        for name in self.YULAN_RADIOS:
            if self._checked(name):
                return name
        return None

    def _radio_value(self, name: str | None) -> str:
        if not name:
            return ""
        if "10" in name:
            return "10"
        if "20" in name:
            return "20"
        if "30" in name:
            return "30"
        if "customer" in name:
            return self._text(self.YULAN_CUSTOM_FIELD)
        return ""

    def _build_yulan_mode(self):
        if not self.YULAN_MODE_COMBO:
            return None
        mode_text = self._combo_text(self.YULAN_MODE_COMBO)
        if mode_text != YULAN_MODE_DURATION_TEXT:
            selected = self._selected_yulan_radio()
            if selected is None:
                print("请勾选预览视频的占比！")
                return None
            present = self._radio_value(selected)
            if selected == self.YULAN_CUSTOM_RADIO:
                ok, ratio = _parse_int(present)
                if not ok:
                    print("请输入自定义视频占比，输入范围1~99，需要输入整数！")
                    return None
                if ratio < 1:
                    print("不能小于1，请输入自定义视频占比，输入范围1~99，需要输入整数！")
                    return None
                if ratio > 99:
                    print("不能超过99，请输入自定义视频占比，输入范围1~99，需要输入整数！")
                    return None
                present = str(ratio)
            return YuLanModeBean(
                resType=YULAN_RES_TYPE_VIDEO,
                mode=YULAN_MODE_PRESENT,
                presentMode=PresentMode(present=str(present)),
            )

        ok, duration_min = _parse_int(self._text(self.YULAN_MIN_FIELD))
        if not ok:
            print("请输入预览视频随机时长最小值，需要输入整数！（单位秒钟）")
            return None
        if duration_min <= 0:
            print("预览视频 随机时长最小值不能小于等于0！")
            return None
        ok, duration_max = _parse_int(self._text(self.YULAN_MAX_FIELD))
        if not ok:
            print("请输入预览视频随机时长最大值，需要输入整数！（单位秒钟）")
            return None
        if duration_max < duration_min:
            print("预览视频 随机时长最大值不能小于最小值！")
            return None
        duration_mode = DurationMode(
            resType=YULAN_RES_TYPE_VIDEO,
            presentMode="",
            durationMode=YULAN_MODE_DURATION,
        )
        duration_mode.duration_min_second = duration_min
        duration_mode.duration_max_second = duration_max
        return YuLanModeBean(
            resType=YULAN_RES_TYPE_VIDEO,
            mode=YULAN_MODE_DURATION,
            durationMode=duration_mode,
        )

    def _build_links(self):
        if not self.HUIYUAN_ENABLE_CHECK:
            return None, None
        huiyuan = None
        if self.HUIYUAN_ENABLE_CHECK:
            enable = self._checked(self.HUIYUAN_ENABLE_CHECK)
            text = self._text(self.HUIYUAN_TEXT_FIELD)
            custom = self._checked(self.HUIYUAN_CUSTOMER_CHECK)
            link = self._text(self.HUIYUAN_LINK_FIELD)
            if enable and not text:
                print("请输入会员超级链接的文案！")
                return None
            if custom and not link.startswith("http"):
                print("自定义会员超级链接 必须要输入http开头的超级链接！")
                return None
            huiyuan = HuiYuanLink(
                enable=enable,
                text=text,
                enableCustomerLink=custom,
                customerHttpLink=link,
                blockquote=self._checked(self.HUIYUAN_BQ_CHECK),
            )
        youke = None
        if self.YOUKE_ENABLE_CHECK:
            enable = self._checked(self.YOUKE_ENABLE_CHECK)
            text = self._text(self.YOUKE_TEXT_FIELD)
            link = self._text(self.YOUKE_LINK_FIELD)
            if enable and not text:
                print("请输入游客超级链接的文案！")
                return None
            if enable and link and not link.startswith("http"):
                print("游客超级链接 必须要输入http开头的超级链接！")
                return None
            youke = YouKeLink(
                enable=enable,
                text=text,
                httpLink=link,
                blockquote=self._checked(self.YOUKE_BQ_CHECK),
            )
        return huiyuan, youke

    def _build_comment_rule(self):
        if not self.COPY_COMMENT_CHECK:
            return None
        copy_comment = self._checked(self.COPY_COMMENT_CHECK)
        if copy_comment and self.commentRule is None:
            print("你勾选了复刻评论区，请配置一下评论区复刻规则！")
            return None
        rule = self.commentRule
        if rule is None:
            from ...dclass.DTopClass import CommentRuleBean

            rule = CommentRuleBean(copyComment=False, wantCount=0)
        rule.copyComment = copy_comment
        self.commentRule = rule
        return rule

    def _build_complete_version(self):
        if not self.COMPLETE_VERSION_FIELD:
            return None
        text = self._text(self.COMPLETE_VERSION_FIELD)
        if not text:
            print("必须要输入完整版本链接文案！")
            return None
        return CompleteVersionOp(
            blockquote=self._checked(self.COMPLETE_BLOCKQUOTE_CHECK),
            linkText=text,
        )

    def _build_bot(self):
        if not self.BOT_FIELD:
            return None
        bot_name = self._text(self.BOT_FIELD)
        try:
            from ...fea import _sq_jqm

            has_bot = bool(_sq_jqm.current_account_info.has_bot_ability())
        except Exception:
            has_bot = True
        if not has_bot:
            print(self.BOT_SERVICE_MESSAGE)
            return None
        if not utils.is_valid_bot(bot_name):
            print(self.BOT_ERROR_MESSAGE)
            return None
        from ...dclass.DTopClass import BotBean

        return BotBean(user_name=bot_name)

    def _build_ai(self):
        if not self.AI_CHECK:
            return None, None
        enable = self._checked(self.AI_CHECK)
        employee = self.aiEmployee
        if enable and employee is None:
            print("请选择AI员工！")
            return None
        uid = getattr(employee, "uid", self.employee_id) if employee is not None else 0
        ai_employee = AiEmployee(enable=enable, uid=_safe_int(uid, 0))
        if self._checked(self.AI_USE_RADIO):
            action = "origin"
        else:
            action = "skip"
        return ai_employee, AiRefusedOption(action=action)

    def _build_grid(self):
        if not self.GRID_FIELD:
            return None, self._checked(self.GRID_COVER_FIELD)
        ok, number = _parse_int(self._text(self.GRID_FIELD))
        if not ok or number < 0 or number > 10:
            print(
                "电报单组消息最多10个资源，补齐x宫格高清视频截图数，请填写整数！"
                "范围必须是0~10，如果不懂，请点击【教程】按钮查看说明！"
            )
            return None, False
        return GridOpt(number=number), self._checked(self.GRID_COVER_FIELD)

    def _build_ads(self):
        if not self.AD_LIST:
            return None
        return AdWrapper(
            adEnable=self._checked(self.AD_ENABLE_CHECK),
            adIsBottomUp=self._checked(self._find_field("ad_is_bottom_up")),
            delete=self._checked(self._find_field("ad_delete")),
            ades=list(self.adMap.values()),
        )

    def _apply_common_bean_fields(self, bean, context) -> None:
        bean.name = context["name"]
        bean.source = context["source"]
        if context["db_channel"]:
            bean.db_channel = context["db_channel"]
        bean.destes = context["destes"]
        bean.yulan_destes = context["yulan_destes"]
        bean.dtype = context["dtype"]
        bean.modelWrapper = context["model"]
        bean.baseFilter = context["base_filter"]
        bean.advancedFilterBean = context["advanced_filter"]
        bean.tail = context["tail"]
        bean.replace = context["replace"]
        bean.water = context["water"]
        bean.forWardAction = context["action"]
        bean.yuLanResOp = context["resop"]
        bean.yuLanModeBean = context["yulan_mode"]
        if context["huiyuan_link"] is not None:
            bean.huiYuanLink = context["huiyuan_link"]
        if context["youke_link"] is not None:
            bean.youKeLink = context["youke_link"]
        if context["duration_info"] is not None:
            bean.durationInfo = context["duration_info"]
        if context["comment_rule"] is not None:
            bean.commentRule = context["comment_rule"]
        if context["complete_version"] is not None:
            bean.completeVersionOp = context["complete_version"]
        if context["bot"] is not None:
            bean.botBean = context["bot"]
        if context["ai_employee"] is not None:
            bean.aiEmployee = context["ai_employee"]
        if context["ai_refused"] is not None:
            bean.aiRefusedOpt = context["ai_refused"]
        if context["grid"] is not None:
            bean.grid = context["grid"]
        if context["ads"] is not None:
            bean.selfAdWrapper = context["ads"]
        bean.randomCover = bool(context["random_cover"])
        bean.priority = int(context["priority"])
        bean.active = True
        bean.auto_type = self.AUTO_TYPE
        if not getattr(bean, "kid", ""):
            bean.kid = self.kid

    def _persist_bean(self, bean) -> None:
        if not self.edit_mode:
            try:
                from ...dclass import LoadDataClass
                from ...fea import _sq_jqm

                limit = int(getattr(_sq_jqm.current_account_info, "limit", 0) or 0)
                if limit and len(LoadDataClass.getAutoMap()) >= limit:
                    print("当前版本条目数量已达上限！")
                    return
            except Exception:
                _ = None
        try:
            from ...dclass import LoadDataClass

            LoadDataClass.addOrUpdate(bean)
        except Exception as exc:
            print("保存条目失败：", exc)
            return
        print(self.SAVE_EDIT_MESSAGE if self.edit_mode else self.SAVE_ADD_MESSAGE)
        try:
            from . import signals

            signals.global_ui_signal.signal_yun_yin_data_changed.emit()
        except Exception:
            _ = None
        self.close()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        screen_width, screen_height = utils.get_screen_size()
        width_num, width_den, height_num, height_den = self.WINDOW_RATIO
        window_width = int(screen_width * width_num / width_den)
        window_height = int(screen_height * height_num / height_den)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.resize(window_width, window_height)
        self.move(x_position, y_position)
        super().showEvent(a0)


class EditAutoFlowItemEditDialog(_FlowEditorMixin, BaseDialog):
    FORM_TITLE = "编辑自动流"
    UI_MODULE = "src.resource.ui.dyna.auto_flow_item"
    BEAN_CLASS = AutoFlowBean
    AUTO_TYPE = AUTO_BEAN_TYPE_AUTO_FLOW
    BEAN_ATTR = "autoflowbean"
    WINDOW_RATIO = (3, 6, 10, 20)

    SAVE_BUTTON = "btn_save_flow_item"
    ITEM_NAME_FIELD = "lineEdit_flow_item_name"
    SOURCE_FIELD = "lineEdit_flow_source"
    DEST_FIELD = "textEdit_flow_dest_list"
    PREVIEW_DEST_FIELD = "textEdit_flow_auto_flow_dest_list"
    PRIORITY_FIELD = "lineEdit_priority"

    MODE_COMBO = "comboBox_flow_select_mode"
    UNIT_COMBO = "comboBox_flow_number_dan_wei"
    RANDOM_UNIT_COMBO = "comboBox_flow_number_random_dan_wei"
    RANDOM_COUNT_FIELD = "lineEdit_flow_random_want_count"
    INCREASE_START_FIELD = "lineEdit_flow_increase_start_id"
    INCREASE_COUNT_FIELD = "lineEdit_flow_increase_want_count"
    LOOP_START_FIELD = "lineEdit_flow_loop_start_id"
    LOOP_END_FIELD = "lineEdit_flow_loop_end_id"
    MODEL_FIELD = "text_model"
    NUMBER_MODEL_FIELD = "number_model"

    DURATION_MIN_FIELD = "lineEdit_auto_duration_min"
    DURATION_MAX_FIELD = "lineEdit_auto_duration_max"
    SIZE_MIN_FIELD = "lineEdit_auto_mb_min"
    SIZE_MAX_FIELD = "lineEdit_auto_mb_max"
    WORDS_CONTAIN_FIELD = "lineEdit_flow_fliter_words_contain"
    WORDS_EXCLUDE_FIELD = "lineEdit_flow_fliter_words_exclude"
    TAIL_FIELD = "textEdit_flow_tail_text"
    REPLACE_FIELD = "textEdit_flow_replace_rule"
    RESOURCE_FIELDS = {
        "video_photo": "checkBox_flow_video_photo",
        "photo": "checkBox_flow_photo",
        "video": "checkBox_flow_video",
        "file": "checkBox_flow_file",
        "text": "checkBox_flow_text",
    }
    CHAI_ZU_CHECK = "checkBox_chai_zu"
    KEEP_SOURCE_CHECK = "cb_flow_origin_source_text"
    AD_ENABLE_CHECK = "cb_flow_ad_enable"

    AD_LIST = "listWidget_flow_private_ad_list"
    AD_ADD_BUTTON = "btn_flow_add_ad"
    AI_BUTTON = "btn_auto_select_ai_em"
    AI_CHECK = "checkBox_auto_ai_enable"
    AI_GROUP = "horizontalGroupBox_ai_auto"
    AI_LABEL = "label_auto_ai_name"
    AI_SKIP_RADIO = "radioButton_ai_auto_skip_source"
    AI_USE_RADIO = "radioButton_ai_auto_use_source"

    WATER_MODE_COMBO = "cb_flow_water_mode"
    WATER_PATH_LABEL = "label_flow_water_pic_path"
    WATER_SELECT_BUTTON = "btn_flow_water_select_pic"
    WATER_RATIO_FIELD = "line_edit_auto_flow_water_pic_ratio"
    WATER_TEXT_FIELD = "lineEdit_cb_water_text"
    WATER_PIC_CHECK = "cb_flow_pic_water"
    WATER_VIDEO_CHECK = "cb_flow_video_water"
    WATER_DURATION_COMBO = "cb_flow_video_minute"

    ACTION_AUTO_RADIO = "radioButton_auto_flow_action_auto"
    ACTION_DOWNLOAD_RADIO = "radioButton_auto_flow_action_download"
    ACTION_SLEEP_MIN_FIELD = "lineEdit_auto_flow_sleep_min"
    ACTION_SLEEP_MAX_FIELD = "lineEdit_auto_flow_sleep_max"

    RESOP_BLUR_CHECK = "cb_auto_flow_pic_blur"
    RESOP_SPOILER_CHECK = "cb_auto_flow_spoiler"
    RESOP_RADIUS_FIELD = "auto_flow_pic_blur_radius"

    GRID_FIELD = "lineEdit_auto_grid_number"
    GRID_COVER_FIELD = "cb_auto_random_cover"

    YULAN_MODE_COMBO = "comboBox_auto_flow_select_auto_flow_mode"
    YULAN_RADIOS = (
        "radioButton_auto_flow_10",
        "radioButton_auto_flow_20",
        "radioButton_auto_flow_30",
        "radioButton_auto_flow_customer",
    )
    YULAN_CUSTOM_RADIO = "radioButton_auto_flow_customer"
    YULAN_CUSTOM_FIELD = "lineEdit_auto_flow_customer"
    YULAN_MIN_FIELD = "lineEdit_auto_flow_min_duration"
    YULAN_MAX_FIELD = "lineEdit_auto_flow_max_duration"

    HUIYUAN_ENABLE_CHECK = "cb_flow_hui_yuan_link"
    HUIYUAN_TEXT_FIELD = "lineEdit_flow_hui_yuan_tip_text"
    HUIYUAN_CUSTOMER_CHECK = "cb_flow_hui_yuan_customer_link"
    HUIYUAN_LINK_FIELD = "lineEdit_flow_hui_yuan_tip_text_link"
    HUIYUAN_BQ_CHECK = "cb_flow_hui_yuan_link_bq"
    YOUKE_ENABLE_CHECK = "cb_flow_you_ke_link"
    YOUKE_TEXT_FIELD = "lineEdit_flow_you_ke_tip_text"
    YOUKE_LINK_FIELD = "lineEdit_flow_you_ke_tip_text_link"
    YOUKE_BQ_CHECK = "cb_flow_you_ke_link_bq"

    ADD_DURATION_CHECK = "checkBox_auto_add_duration_info"
    ADD_DURATION_BQ_CHECK = "checkBox_auto_add_duration_info_bq"

    RESOURCE_TUTORIAL_BUTTON = "auto_res_btn_jiao_chen"
    RESOP_TUTORIAL_BUTTON = "btn_auto_flow_res_op_jiao_chen"
    ACTION_TUTORIAL_BUTTON = "btn_auto_flow_action_jiao_chen"
    TOPIC_TUTORIAL_BUTTON = "auto_flow_topic_jiao_chen"
    PIC_WATER_TUTORIAL_BUTTON = "btn_flow_water_pic_jiao_chen"
    GRID_TUTORIAL_BUTTON = "btn_auto_grid_jiao_chen"
    COVER_TUTORIAL_BUTTON = "auto_cover_jiao_chen"
    HUIYUAN_TUTORIAL_BUTTON = "btn_flow_hui_yuan_link_jc"
    YOUKE_TUTORIAL_BUTTON = "btn_flow_you_ke_link_jc"
    RES_OP_COURSE = "unifyShowPublishResOpCourse"
    ACTION_COURSE = "unifyShowAutoFlowBanYunTypeCourse"
    TOPIC_COURSE = "unifyShowTopicCourse"

    SAVE_EDIT_MESSAGE = "更新自动流成功！"
    SAVE_ADD_MESSAGE = "添加自动流成功！"
    DEFAULT_TEXTS = {
        "lineEdit_priority": "100",
        "lineEdit_auto_flow_sleep_min": "3",
        "lineEdit_auto_flow_sleep_max": "5",
        "lineEdit_auto_flow_min_duration": "60",
        "lineEdit_auto_flow_max_duration": "120",
        "line_edit_auto_flow_water_pic_ratio": "30",
        "lineEdit_auto_grid_number": "6",
        "lineEdit_flow_hui_yuan_tip_text": "💋会员点我看完整版",
        "lineEdit_flow_you_ke_tip_text": "😍游客点我上车",
    }
    DEFAULT_CHECKS = {
        "checkBox_flow_video_photo": True,
        "checkBox_flow_photo": True,
        "checkBox_flow_video": True,
        "checkBox_flow_file": True,
        "checkBox_flow_text": True,
        "cb_flow_origin_source_text": True,
        "cb_flow_ad_enable": True,
        "radioButton_auto_flow_action_auto": True,
        "radioButton_ai_auto_skip_source": True,
        "radioButton_auto_flow_10": True,
        "cb_flow_hui_yuan_link_bq": True,
        "cb_flow_you_ke_link_bq": True,
        "checkBox_auto_add_duration_info_bq": True,
    }
    DEFAULT_COMBOS = {
        "comboBox_flow_select_mode": MODE_RANDOM_TEXT,
        "comboBox_flow_number_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "comboBox_flow_number_random_dan_wei": MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT,
        "cb_flow_water_mode": WATER_MODE_PIC,
        "comboBox_auto_flow_select_auto_flow_mode": YULAN_MODE_PRESENT_TEXT,
    }

    WIDGET_NAMES = (
        "btn_flow_hui_yuan_link_jc",
        "btn_flow_you_ke_link_jc",
        "btn_show_duration_dialog",
        "auto_res_btn_jiao_chen",
        "btn_auto_flow_res_op_jiao_chen",
        "btn_auto_flow_action_jiao_chen",
        "auto_flow_topic_jiao_chen",
        "btn_auto_select_ai_em",
        "btn_flow_water_pic_jiao_chen",
        "btn_flow_water_select_pic",
        "btn_auto_grid_jiao_chen",
        "auto_cover_jiao_chen",
        "btn_save_flow_item",
        "btn_flow_add_ad",
        "comboBox_flow_number_dan_wei",
        "comboBox_flow_number_random_dan_wei",
        "comboBox_flow_select_mode",
        "comboBox_auto_flow_select_auto_flow_mode",
        "cb_flow_water_mode",
        "listWidget_flow_private_ad_list",
        "cb_flow_origin_source_text",
        "cb_flow_ad_enable",
        "cb_flow_hui_yuan_link",
        "lineEdit_flow_hui_yuan_tip_text",
        "cb_flow_hui_yuan_customer_link",
        "lineEdit_flow_hui_yuan_tip_text_link",
        "cb_flow_you_ke_link",
        "lineEdit_flow_you_ke_tip_text",
        "lineEdit_flow_you_ke_tip_text_link",
        "radioButton_auto_flow_10",
        "radioButton_auto_flow_20",
        "radioButton_auto_flow_30",
        "radioButton_auto_flow_customer",
        "checkBox_flow_video_photo",
        "checkBox_pb_auto_flow_video",
        "checkBox_auto_ai_enable",
        "horizontalGroupBox_ai_auto",
        "label_auto_ai_name",
        "label_flow_water_pic_path",
        "lineEdit_auto_flow_customer",
        "yulan_qu",
        "yulan_qu_wrapper",
        "checkBox_chai_zu",
        "checkBox_flow_photo",
        "checkBox_flow_video",
        "checkBox_flow_file",
        "lineEdit_flow_random_want_count",
        "cb_flow_dele_source_text",
        "cb_flow_dele_link",
        "cb_flow_fliter_button",
        "lineEdit_flow_increase_start_id",
        "lineEdit_flow_increase_want_count",
        "lineEdit_auto_duration_min",
        "lineEdit_auto_duration_max",
        "lineEdit_auto_mb_min",
        "lineEdit_auto_mb_max",
        "checkBox_flow_text",
        "lineEdit_auto_flow_min_duration",
        "lineEdit_auto_flow_max_duration",
        "lineEdit_auto_flow_sleep_min",
        "lineEdit_auto_flow_sleep_max",
        "radioButton_auto_flow_action_auto",
        "radioButton_auto_flow_action_download",
        "checkBox_pb_auto_flow_picture",
        "auto_flow_pic_blur_radius",
        "cb_flow_hui_yuan_link_bq",
        "cb_flow_you_ke_link_bq",
        "checkBox_auto_add_duration_info_bq",
        "lineEdit_priority",
        "radioButton_ai_auto_skip_source",
        "radioButton_ai_auto_use_source",
        "line_edit_auto_flow_water_pic_ratio",
        "lineEdit_auto_grid_number",
        "cb_flow_ad_is_bottom_up",
        "cb_flow_ad_delete",
        "present_container",
        "duration_container",
        "text_water_wrapper",
        "pic_water_wrapper",
        "random_com",
        "increase_com",
        "loop_com",
        "text_model",
        "number_model",
        "lineEdit_flow_source",
        "textEdit_flow_dest_list",
        "textEdit_flow_auto_flow_dest_list",
        "lineEdit_flow_fliter_words_contain",
        "lineEdit_flow_fliter_words_exclude",
        "lineEdit_flow_loop_start_id",
        "lineEdit_flow_loop_end_id",
        "checkBox_discard_no_text_resource",
        "textEdit_flow_tail_text",
        "cb_flow_pic_water",
        "cb_flow_video_water",
        "cb_flow_video_minute",
        "lineEdit_cb_water_text",
        "textEdit_flow_replace_rule",
        "checkBox_auto_add_duration_info",
        "cb_auto_flow_spoiler",
        "cb_auto_flow_pic_blur",
        "cb_auto_random_cover",
        "lineEdit_flow_item_name",
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


__all__ = ["EditAutoFlowItemEditDialog"]
