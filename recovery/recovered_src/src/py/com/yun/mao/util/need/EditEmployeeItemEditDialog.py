# Recovered module: src.py.com.yun.mao.util.need.EditEmployeeItemEditDialog
# Behaviour-level reconstruction from Nuitka constants, source signatures and
# offline Hex-Rays.  The AI test bridge keeps QRunnable work off the UI thread
# and creates no widgets or files at import time.
from __future__ import annotations

import importlib
import re
from pathlib import Path
from typing import Any

from PyQt5 import QtGui
from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QAbstractScrollArea,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from . import utils
from .AllBeanDef import AiEmployeeBean
from .BaseDialog import BaseDialog
from .. import AI_INNER_DEF


# inferred: short fallbacks only; AI_INNER_DEF values win when available.
_SEXY_ROLE_FALLBACK = "你是一个擅长中文文案同义改写的写作助手。"
_SEXY_PRE_FALLBACK = (
    "请根据下面的文案，写一段$length字以内的中文文案，"
    "保持原意并让表达自然流畅。"
)
_NEWS_ROLE_FALLBACK = "你是一位资深中文新闻主笔，擅长把事实改写成自然、抓人的短视频文案。"
_NEWS_PRE_FALLBACK = (
    "请根据下面的新闻文案，写一段$length字以内的中文短视频文案，"
    "保持事实不变并使用日常口语表达。"
)
_SENSITIVE_FALLBACK = "敏感词"


class _AiTestFinishBridge(QObject):
    finished = pyqtSignal(object, str)

    def __init__(self, tab) -> None:
        super().__init__()
        self._tab = tab
        self.finished.connect(self._deliver)

    @pyqtSlot(object, str)
    def _deliver(self, status, output_text: str) -> None:
        self._tab._apply_ai_em_test_finish(status, output_text)


class EditEmployeeItemEditDialog(BaseDialog):
    _REF_DIALOG_W = 980
    _REF_DIALOG_H = 794
    _BASE_ROLE_H = 72
    _BASE_PRE_H = 88
    _BASE_SENS_H = 52
    _BASE_TEST_H = 120

    UI_MODULE = "src.resource.ui.dyna.ai_employee_item"
    WIDGET_NAMES = (
        "btn_em_import_sensitive",
        "btn_em_save",
        "btn_em_test",
        "btn_show_model_info",
        "btn_em_sexy_init",
        "btn_em_news_init",
        "textEdit_em_test_input",
        "textEdit_em_role_display",
        "textEdit_em_pre_text_display",
        "textEdit_em_sensitive_word_display",
        "textEdit_em_test_output",
        "comboBox_em_select_model",
        "lineEdit_em_word_min",
        "lineEdit_em_word_max",
        "lineEdit_em_retry_count",
        "lineEdit_em_name",
        "label_em_role",
        "label_em_pre_text",
        "label_em_sensitive",
        "label_em_model",
        "label_em_name",
    )

    def __init__(
        self,
        parent=None,
        windowTitle: str | None = None,
        employee: AiEmployeeBean | None = None,
        isCopy: bool = False,
        readOnly: bool = False,
    ) -> None:
        super().__init__(parent)
        self._tab = self
        self.edit_mode = employee is not None and not bool(isCopy)
        self.employee = employee
        self.isCopy = bool(isCopy)
        self.readOnly = bool(readOnly)
        self._finish_bridge: _AiTestFinishBridge | None = None
        self._ai_test_runnable = None
        if windowTitle:
            self.setWindowTitle(windowTitle)
        self.cooldown_manager = None
        try:
            from .CoolUtils import ButtonCooldownManager

            self.cooldown_manager = ButtonCooldownManager()
        except Exception:
            self.cooldown_manager = None

        self.ui = self._load_ui()
        self._install_text_edit_no_document_grow()
        self._connect_signals()
        self.fillDefault()
        self.fillBeanIfNeed()
        self.apply_readonly()

    def _load_ui(self):
        try:
            module = importlib.import_module(self.UI_MODULE)
            form = module.Ui_Form()
            form.setupUi(self)
            return form
        except Exception:
            return self._build_fallback_ui()

    def _build_fallback_ui(self):
        # inferred: field-compatible fallback for the missing generated Ui_Form.
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
            lower = name.lower()
            if "textedit" in lower:
                widget = QTextEdit(content)
                widget.setMinimumHeight(64)
            elif "combobox" in lower:
                widget = QComboBox(content)
            elif "lineedit" in lower:
                widget = QLineEdit(content)
            elif lower.startswith("label_"):
                widget = QLabel(name, content)
                widget.setWordWrap(True)
            else:
                widget = QPushButton(name, content)
            widget.setObjectName(name)
            setattr(ui, name, widget)
            form.addRow(name, widget)
        ui.horizontalLayout = QVBoxLayout()
        ui.verticalLayout = QVBoxLayout()
        ui.verticalLayout_3 = QVBoxLayout()
        ui.verticalLayout_2 = QVBoxLayout()
        ui.horizontalLayout_8 = QVBoxLayout()
        ui.horizontalLayout_6 = QVBoxLayout()
        ui.horizontalLayout_2 = QVBoxLayout()
        return ui

    def _widget(self, name: str | None):
        if not name:
            return None
        return getattr(getattr(self, "ui", None), name, None)

    def _line(self, name: str | None) -> str:
        widget = self._widget(name)
        if widget is None:
            return ""
        try:
            return str(widget.text() or "").strip()
        except Exception:
            return ""

    def _plain(self, name: str | None) -> str:
        widget = self._widget(name)
        if widget is None:
            return ""
        try:
            return str(widget.toPlainText() or "").strip()
        except Exception:
            return ""

    def _set_line(self, name: str | None, value: Any) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        try:
            widget.setText("" if value is None else str(value))
        except Exception:
            return

    def _set_plain(self, name: str | None, value: Any) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        try:
            widget.setPlainText("" if value is None else str(value))
        except Exception:
            return

    def _combo_text(self, name: str | None) -> str:
        widget = self._widget(name)
        if not isinstance(widget, QComboBox):
            return ""
        try:
            return str(widget.currentText() or "").strip()
        except Exception:
            return ""

    def _set_combo_text(self, name: str | None, value: Any) -> None:
        widget = self._widget(name)
        if not isinstance(widget, QComboBox):
            return
        text = str(value or "")
        try:
            index = widget.findText(text)
            if index < 0 and text:
                widget.addItem(text)
                index = widget.count() - 1
            if index >= 0:
                widget.setCurrentIndex(index)
        except Exception:
            return

    def _connect(self, name: str | None, signal: str, slot) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        try:
            getattr(widget, signal).connect(slot)
        except Exception:
            return

    def _connect_signals(self) -> None:
        self._connect("btn_em_import_sensitive", "clicked", self.on_em_import_sensitive)
        self._connect("btn_em_save", "clicked", self.on_em_save)
        self._connect("btn_em_test", "clicked", self.on_em_test)
        self._connect("btn_show_model_info", "clicked", self.on_show_model_info)
        self._connect("btn_em_sexy_init", "clicked", self.on_em_sexy_init)
        self._connect("btn_em_news_init", "clicked", self.on_em_news_init)

    def _model_names(self) -> list[str]:
        names: list[str] = []
        try:
            from ...fea import _sq_jqm

            raw_models = _sq_jqm.get_ai_model_list()
        except Exception:
            raw_models = []
        for item in raw_models or []:
            if isinstance(item, dict):
                name = item.get("name", item.get("model", ""))
            else:
                name = getattr(item, "name", getattr(item, "model", item))
            text = str(name or "").strip()
            if text and text not in names:
                names.append(text)
        return names

    def _default_model(self) -> str:
        try:
            from ...fea import _sq_jqm

            model = _sq_jqm.get_default_ai_model()
            if isinstance(model, dict):
                return str(model.get("name", model.get("model", "")) or "")
            if model is not None:
                return str(getattr(model, "name", getattr(model, "model", model)) or "")
        except Exception:
            _ = None
        return "grok-4-1-fast"

    def _sensitive_defaults(self) -> list[str]:
        raw = str(getattr(AI_INNER_DEF, "SENSITIVE_DEFAULT", "") or "")
        values = re.split(r"[|\n,，]+", raw)
        return [item.strip() for item in values if item.strip()] or [_SENSITIVE_FALLBACK]

    def _parse_sensitive(self, text: str | None = None) -> list[str]:
        raw = self._plain("textEdit_em_sensitive_word_display") if text is None else text
        return list(dict.fromkeys(
            item.strip()
            for item in re.split(r"[|\n,，]+", str(raw or ""))
            if item.strip()
        ))

    def fillDefault(self) -> None:
        self._set_line("lineEdit_em_word_min", "20")
        self._set_line("lineEdit_em_word_max", "100")
        self._set_line("lineEdit_em_retry_count", "1")
        self._set_plain(
            "textEdit_em_test_input",
            "",
        )
        self._set_plain(
            "textEdit_em_test_output",
            "",
        )
        self._set_placeholder(
            "textEdit_em_test_input",
            "这里输入测试文案，用于AI员工测试",
        )
        self._set_placeholder(
            "textEdit_em_test_output",
            "这里会输出AI生成的文案",
        )
        if not self._plain("textEdit_em_sensitive_word_display"):
            self._set_plain(
                "textEdit_em_sensitive_word_display",
                "|\n".join(self._sensitive_defaults()),
            )
        for name in ("btn_em_sexy_init", "btn_em_news_init"):
            widget = self._widget(name)
            if widget is not None:
                try:
                    widget.setVisible(not self.readOnly)
                except Exception:
                    _ = None
        self.reset_fill_comboBox_component()

    def _set_placeholder(self, name: str | None, text: str) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        try:
            widget.setPlaceholderText(text)
        except Exception:
            return

    def fillBeanIfNeed(self) -> None:
        employee = self.employee
        if employee is None:
            return
        name = str(getattr(employee, "name", "") or "")
        if self.isCopy and name and "(复制)" not in name:
            name += "(复制)"
        self._set_line("lineEdit_em_name", name)
        self._set_plain("textEdit_em_role_display", getattr(employee, "role", ""))
        self._set_plain("textEdit_em_pre_text_display", getattr(employee, "pre_text", ""))
        self._set_plain(
            "textEdit_em_sensitive_word_display",
            "|\n".join(
                item.strip()
                for item in str(getattr(employee, "sensitive", "") or "").split("|")
                if item.strip()
            ),
        )
        self._set_line("lineEdit_em_word_min", getattr(employee, "word_min", 20))
        self._set_line("lineEdit_em_word_max", getattr(employee, "word_max", 100))
        self._set_line("lineEdit_em_retry_count", getattr(employee, "retry_count", 1))
        self.display_model_component_with_employee(employee)

    def display_model_component_with_employee(self, employee=None) -> None:
        combo = self._widget("comboBox_em_select_model")
        if not isinstance(combo, QComboBox):
            return
        current = str(getattr(employee, "model", "") or "") if employee is not None else ""
        names = self._model_names()
        combo.blockSignals(True)
        try:
            combo.clear()
            combo.addItem("")
            for name in names:
                combo.addItem(name)
            if current:
                self._set_combo_text("comboBox_em_select_model", current)
            else:
                self._set_combo_text(
                    "comboBox_em_select_model",
                    self._default_model(),
                )
        finally:
            combo.blockSignals(False)

    def reset_fill_comboBox_component(self) -> None:
        employee = self.employee
        self.display_model_component_with_employee(employee)

    def apply_readonly(self) -> None:
        if not self.readOnly:
            return
        for name in (
            "textEdit_em_role_display",
            "textEdit_em_pre_text_display",
            "textEdit_em_sensitive_word_display",
            "textEdit_em_test_input",
            "textEdit_em_test_output",
        ):
            widget = self._widget(name)
            if widget is not None:
                try:
                    widget.setReadOnly(True)
                except Exception:
                    _ = None
        for name in (
            "lineEdit_em_name",
            "lineEdit_em_word_min",
            "lineEdit_em_word_max",
            "lineEdit_em_retry_count",
        ):
            widget = self._widget(name)
            if widget is not None:
                try:
                    widget.setReadOnly(True)
                except Exception:
                    _ = None
        for name in (
            "btn_em_import_sensitive",
            "btn_em_save",
            "btn_em_test",
            "btn_em_sexy_init",
            "btn_em_news_init",
        ):
            widget = self._widget(name)
            if widget is not None:
                try:
                    widget.setEnabled(False)
                except Exception:
                    _ = None
        combo = self._widget("comboBox_em_select_model")
        if combo is not None:
            try:
                combo.setEnabled(False)
            except Exception:
                _ = None

    def on_show_model_info(self) -> None:
        try:
            from ...dialog.AiModelInfoPriceDialog import AiModelInfoPriceDialog

            AiModelInfoPriceDialog(self).exec_()
        except Exception as exc:
            print("打开AI模型信息失败：", exc)

    def on_em_import_sensitive(self) -> None:
        if self.readOnly:
            return
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "导入敏感词",
            "",
            "文本文件 (*.txt);;所有文件 (*)",
        )
        if not file_path:
            return
        try:
            text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            print("读取敏感词文件失败：", exc)
            return
        words = set(self._sensitive_defaults())
        words.update(self._parse_sensitive(text))
        self._set_plain(
            "textEdit_em_sensitive_word_display",
            "|\n".join(sorted(words)),
        )

    def check_params(self):
        role = self._plain("textEdit_em_role_display")
        if not role:
            print("请输入AI员工角色描述！")
            return None
        pre = self._plain("textEdit_em_pre_text_display")
        if not pre:
            print("请输入AI员工前置描述语！")
            return None
        if "写一段$length字以内" not in pre:
            print("注意，前置文案必须包含 【写一段$length字以内】 这个文本！")
            return None
        sensitive = self._parse_sensitive()
        if not sensitive:
            print("请输入AI敏感词！")
            return None
        if not any(item.strip() for item in sensitive):
            print("请输入有效的AI敏感词！")
            return None
        ok, min_count = utils.parse_int(self._line("lineEdit_em_word_min")) if hasattr(
            utils, "parse_int"
        ) else _parse_int(self._line("lineEdit_em_word_min"))
        if not ok or min_count < 10:
            print("请输入最小的文本长度，输入整数，但是必须大于等于10！")
            return None
        ok, max_count = utils.parse_int(self._line("lineEdit_em_word_max")) if hasattr(
            utils, "parse_int"
        ) else _parse_int(self._line("lineEdit_em_word_max"))
        if not ok or max_count <= min_count:
            print("请输入最大的文本长度，输入整数，必须大于前面的最小值！")
            return None
        if max_count >= 1000:
            print("请输入最大的文本长度，输入整数，必须小于1000！")
            return None
        ok, retry_count = utils.parse_int(self._line("lineEdit_em_retry_count")) if hasattr(
            utils, "parse_int"
        ) else _parse_int(self._line("lineEdit_em_retry_count"))
        if not ok or retry_count <= 0 or retry_count > 5:
            print("请输入AI生成失败之后最大重试次数，建议1~5次即可！")
            return None
        model = self._combo_text("comboBox_em_select_model")
        if not model:
            print("请先选择模型！")
            return None
        return {
            "role": role,
            "pre": pre,
            "sensitive": "|".join(sensitive),
            "min_count": min_count,
            "max_count": max_count,
            "model": model,
            "retry_count": retry_count,
        }

    def on_em_test(self) -> None:
        try:
            from ...cd import Working
        except Exception:
            Working = None
        if Working is not None and getattr(Working, "Session_Working", False):
            print("任务正在进行中，不能测试！")
            return
        params = self.check_params()
        if params is None:
            return
        input_str = self._plain("textEdit_em_test_input")
        if not input_str:
            print("请输入测试文案！")
            return
        api_key = ""
        try:
            from ...config import tabl_cache

            api_key = str(
                tabl_cache.INSTANCE().read_cache(
                    tabl_cache.AI_EMPLOYEE_GROUP,
                    tabl_cache.AI_EMPLOYEE_API_KEY,
                    "",
                )
                or ""
            )
        except Exception:
            api_key = ""
        if not api_key:
            print("请先到【AI员工管理】tab，配置你的 API_KEY !")
            return
        valid_key, _ = utils.validate_xai_api_key(api_key)
        if not valid_key:
            print("请先到【AI员工管理】tab，配置你的 API_KEY !")
            return
        employee_test = AiEmployeeBean(
            uid=10086,
            name="AI员工测试",
            role=params["role"],
            pre_text=params["pre"],
            sensitive=params["sensitive"],
            word_min=params["min_count"],
            word_max=params["max_count"],
            model=params["model"],
            retry_count=params["retry_count"],
        )
        self._finish_bridge = _AiTestFinishBridge(self)

        def button_callback() -> None:
            try:
                from ...util.AITextGenTextRunnable import AITextGenTextRunnable

                runnable = AITextGenTextRunnable(
                    api_key,
                    input_str,
                    employee_test,
                    self._finish_bridge.finished.emit,
                    True,
                )
                self._ai_test_runnable = runnable
                QThreadPool.globalInstance().start(runnable)
            except Exception as exc:
                print("启动AI测试失败：", exc)

        button = self._widget("btn_em_test")
        if self.cooldown_manager is not None:
            self.cooldown_manager.handle_click(button, 1500, button_callback)
        else:
            button_callback()

    def _apply_ai_em_test_finish(self, status, output_text: str) -> None:
        try:
            from ...ai.AiTextGenStatus import AiTextGenStatus
        except Exception:
            AiTextGenStatus = None
        text = str(output_text or "")
        if AiTextGenStatus is not None and status == AiTextGenStatus.REFUSED:
            text = "AI 拒绝生成该内容，请修改文案后重试。"
        elif AiTextGenStatus is not None and status != AiTextGenStatus.SUCCESS and not text:
            text = "AI生成失败，请稍后重试。"
        self._set_plain("textEdit_em_test_output", text)
        widget = self._widget("btn_em_test")
        if widget is not None:
            try:
                widget.setEnabled(not self.readOnly)
            except Exception:
                _ = None
        self._ai_test_runnable = None

    def on_em_save(self) -> None:
        if self.readOnly:
            return
        params = self.check_params()
        if params is None:
            return
        name = self._line("lineEdit_em_name")
        if not name:
            print("请输入 AI 员工的名字 ！")
            return
        if self.isCopy and "(复制)" not in name:
            name += "(复制)"
        employee = self.employee
        if employee is None or self.isCopy or not self.edit_mode:
            generated = str(utils.gen_id_by_ns())
            uid = _safe_int(generated[-12:], 0)
            employee = AiEmployeeBean(uid=uid)
            message = "添加【" + name + "】成功！"
        else:
            message = "更新 【" + name + "】 成功！"
        employee.name = name
        employee.role = params["role"]
        employee.pre_text = params["pre"]
        employee.sensitive = params["sensitive"]
        employee.word_min = params["min_count"]
        employee.word_max = params["max_count"]
        employee.model = params["model"]
        employee.retry_count = params["retry_count"]
        try:
            from ...dclass import LoadEmployeeClass

            LoadEmployeeClass.addOrUpdate(employee)
        except Exception as exc:
            print("保存AI员工失败：", exc)
            return
        print(message)
        try:
            from . import signals

            signals.global_ui_signal.signal_employee_data_changed.emit()
        except Exception:
            _ = None
        self.close()

    def on_em_sexy_init(self) -> None:
        role = str(getattr(AI_INNER_DEF, "SEXY_DEFAULT_ROLE", "") or _SEXY_ROLE_FALLBACK)
        pre = str(
            getattr(AI_INNER_DEF, "SEXY_DEFAULT_PRE_TEXT", "")
            or _SEXY_PRE_FALLBACK
        )
        self._set_plain("textEdit_em_role_display", role)
        self._set_plain("textEdit_em_pre_text_display", pre)
        self._set_plain(
            "textEdit_em_sensitive_word_display",
            "|\n".join(self._sensitive_defaults()),
        )
        self._set_placeholder(
            "textEdit_em_test_input",
            "在这里输入色情文案，可以去电报色情频道里面复制色情文本，然后粘贴到这里。",
        )
        self._set_button_text("btn_em_test", "点击测试色情文案同义转换效果⬇️")

    def on_em_news_init(self) -> None:
        role = str(getattr(AI_INNER_DEF, "NEWS_DEFAULT_ROLE", "") or _NEWS_ROLE_FALLBACK)
        pre = str(
            getattr(AI_INNER_DEF, "NEWS_DEFAULT_PRE_TEXT", "")
            or _NEWS_PRE_FALLBACK
        )
        self._set_plain("textEdit_em_role_display", role)
        self._set_plain("textEdit_em_pre_text_display", pre)
        self._set_plain(
            "textEdit_em_sensitive_word_display",
            "|\n".join(self._sensitive_defaults()),
        )
        self._set_placeholder(
            "textEdit_em_test_input",
            "在这里输入中文新闻文案，可以去电报新闻频道里面复制新闻文本，然后粘贴到这里。",
        )
        self._set_button_text("btn_em_test", "点击测试新闻文案同义转换效果⬇️")

    def _set_button_text(self, name: str | None, text: str) -> None:
        widget = self._widget(name)
        if widget is None:
            return
        try:
            widget.setText(text)
        except Exception:
            return

    def _install_text_edit_no_document_grow(self) -> None:
        for name in (
            "textEdit_em_role_display",
            "textEdit_em_pre_text_display",
            "textEdit_em_sensitive_word_display",
            "textEdit_em_test_input",
            "textEdit_em_test_output",
        ):
            widget = self._widget(name)
            if widget is None:
                continue
            try:
                widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                widget.setMinimumHeight(48)
            except Exception:
                continue

    def _apply_ai_employee_fill_vertical_space(self) -> None:
        for name in (
            "horizontalLayout",
            "verticalLayout",
            "verticalLayout_3",
            "verticalLayout_2",
            "horizontalLayout_8",
            "horizontalLayout_6",
            "horizontalLayout_2",
        ):
            layout = getattr(self.ui, name, None)
            if layout is None or not hasattr(layout, "setStretch"):
                continue
            try:
                count = int(layout.count())
                if count > 0:
                    layout.setStretch(count - 1, 1)
            except Exception:
                continue

    def _apply_responsive_editor_heights(self) -> None:
        window_w = max(200, int(self.width() or self._REF_DIALOG_W))
        window_h = max(200, int(self.height() or self._REF_DIALOG_H))
        scale = max(1.0, min(window_w / float(self._REF_DIALOG_W), 1.35))
        heights = (
            ("textEdit_em_role_display", self._BASE_ROLE_H),
            ("textEdit_em_pre_text_display", self._BASE_PRE_H),
            ("textEdit_em_sensitive_word_display", self._BASE_SENS_H),
            ("textEdit_em_test_output", self._BASE_TEST_H),
        )
        for name, base_height in heights:
            widget = self._widget(name)
            if widget is None:
                continue
            try:
                target = max(48, int(round(base_height * scale)))
                widget.setMinimumHeight(target)
                widget.setMaximumHeight(max(target, int(window_h * 0.52)))
            except Exception:
                continue
        combo = self._widget("comboBox_em_select_model")
        if combo is not None:
            try:
                combo_width = max(200, min(int(window_w * 0.36), 420))
                combo.setMinimumWidth(combo_width)
                combo.setMaximumWidth(combo_width)
            except Exception:
                _ = None
        self._apply_ai_employee_fill_vertical_space()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        screen_width, screen_height = utils.get_screen_size()
        window_w = int(screen_width * 10.0 / 20.0)
        window_h = int(screen_height * 13.5 / 20.0) - 30
        x_position = int((screen_width - window_w) / 2)
        y_position = int((screen_height - window_h) / 2) - 30
        self.resize(window_w, window_h)
        self.move(x_position, y_position)
        self._apply_responsive_editor_heights()
        super().showEvent(a0)


def _parse_int(value: Any) -> tuple[bool, int]:
    try:
        return True, int(str(value or "").strip())
    except (TypeError, ValueError):
        return False, 0


def _safe_int(value: Any, default: int = 0) -> int:
    ok, number = _parse_int(value)
    return number if ok else default


__all__ = ["EditEmployeeItemEditDialog"]
