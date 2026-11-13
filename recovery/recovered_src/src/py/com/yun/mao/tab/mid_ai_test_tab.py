# Recovered module: src.py.com.yun.mao.tab.mid_ai_test_tab
# The module contains one controller and a tiny QObject signal bridge.  The
# slot decorator body is present verbatim in the Nuitka constant table.
from __future__ import annotations

from typing import Any

from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QSizePolicy

from ..ai.AiTextGenStatus import AiTextGenStatus
from ..cd import Working
from ..dialog import ImageDialogHelper
from ..fea import _sq_jqm
from ..util import AI_INNER_DEF, AiTestTipHtmlHelper
try:
    from ..util.AITextGenTextRunnable import AITextGenTextRunnable
except ImportError:
    AITextGenTextRunnable = None
from ..util.need import ShotUtils, signals
from ..util.need.AllBeanDef import AiEmployeeBean
try:
    from ..util.need.CoolUtils import ButtonCooldownManager
except ImportError:
    ButtonCooldownManager = None
from .mid_base_tab import MidBaseTab


def _tip(text: str) -> None:
    try:
        signals.global_ui_signal.tip_dialog_cmd.emit(str(text or ""))
    except Exception:
        print(text)


def _connect(widget: Any, signal_name: str, slot: Any) -> None:
    try:
        signal = getattr(widget, signal_name, None)
        if signal is not None:
            signal.connect(slot)
    except Exception:
        return None


def _inner(name: str, default: str = "") -> str:
    return str(getattr(AI_INNER_DEF, name, default) or default)


class _AiTestFinishBridge(QObject):
    finished = pyqtSignal(object, str)

    def __init__(self, tab: Any, parent: Any = None) -> None:
        super().__init__(parent)
        self._tab = tab
        self.finished.connect(self._deliver)

    @pyqtSlot(object, str)
    def _deliver(self, status: AiTextGenStatus, output_text: str) -> None:
        self._tab._apply_ai_test_finish(status, output_text)


class AiTestTab(MidBaseTab):
    def __init__(self, mainWindow: Any, ui: Any) -> None:
        super().__init__()
        self.mainWindow = mainWindow
        manager_type = ButtonCooldownManager
        self.cooldown_manager = (
            getattr(mainWindow, "cooldown_manager", None)
            or (manager_type() if manager_type is not None else None)
        )
        self._finish_bridge = _AiTestFinishBridge(self, mainWindow)
        self.ui = ui
        self.init()

    def init(self) -> None:
        tips = getattr(AiTestTipHtmlHelper, "create_ai_test_platform_tip", None)
        label = getattr(self.ui, "label_ai_pre_test_tips", None)
        if label is not None and callable(tips):
            label.setText(tips())

        layout = getattr(label, "layout", lambda: None)()
        if layout is not None:
            for index, stretch in ((0, 0), (1, 2), (2, 0), (3, 3)):
                item = layout.itemAt(index)
                if item is not None:
                    layout.setStretch(index, stretch)

        for name in ("textEdit_ai_pre_test_input", "textEdit_ai_pre_test_output"):
            widget = getattr(self.ui, name, None)
            if widget is not None:
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        _connect(
            getattr(self.ui, "btn_ai_pre_test", None),
            "clicked",
            self.on_ai_test_click,
        )
        _connect(
            getattr(self.ui, "btn_ai_effect_show", None),
            "clicked",
            self.on_ai_effect_show,
        )
        _connect(
            getattr(self.ui, "comboBox_ai_pre_test_ch", None),
            "currentIndexChanged",
            self.on_ai_em_changed,
        )
        combo = getattr(self.ui, "comboBox_ai_pre_test_ch", None)
        if combo is not None:
            combo.setCurrentText("官方色情大师")
        self.on_ai_em_changed()

    def on_ai_em_changed(self, *_args: Any) -> None:
        combo = getattr(self.ui, "comboBox_ai_pre_test_ch", None)
        text = str(combo.currentText() if combo is not None else "官方色情大师")
        if text == "官方中文记者":
            placeholder = "在这里输入中文新闻文案，可以去电报新闻频道里面复制新闻文本，然后粘贴到这里。"
            button_text = "点击测试新闻文本同义转换效果⬇️"
        else:
            placeholder = "在这里输入色情文案，可以去电报色情频道里面复制色情文本，然后粘贴到这里。"
            button_text = "点击测试色情文本同义转换效果⬇️"
        input_widget = getattr(self.ui, "textEdit_ai_pre_test_input", None)
        if input_widget is not None:
            input_widget.setPlaceholderText(placeholder)
        button = getattr(self.ui, "btn_ai_pre_test", None)
        if button is not None:
            button.setText(button_text)

    def change_test_run_button(self, enable: bool) -> None:
        Working.Session_Working = bool(enable)
        button = getattr(self.ui, "btn_ai_pre_test", None)
        if button is not None:
            button.setEnabled(bool(enable))
        changed_widget = getattr(ShotUtils, "changed_widget", None)
        if callable(changed_widget) and button is not None:
            try:
                changed_widget(button, enable=enable)
            except Exception:
                return None

    def _apply_ai_test_finish(
        self,
        status: AiTextGenStatus,
        output_text: str,
    ) -> None:
        if status == AiTextGenStatus.REFUSED:
            output_text = "AI 拒绝生成该内容，请修改文案后重试。"
        elif status != AiTextGenStatus.SUCCESS:
            output_text = str(output_text or "")
        output = getattr(self.ui, "textEdit_ai_pre_test_output", None)
        if output is not None:
            output.setText(str(output_text or ""))
        self.change_test_run_button(True)

    def on_ai_effect_show(self) -> None:
        try:
            ImageDialogHelper.unifyShowYouKeAiCourse(self)
        except Exception as exc:
            print("打开 AI 效果展示失败：", exc)

    def is_sexy_ai(self) -> bool:
        combo = getattr(self.ui, "comboBox_ai_pre_test_ch", None)
        return str(combo.currentText() if combo is not None else "") != "官方中文记者"

    def on_ai_test_click(self) -> None:
        input_widget = getattr(self.ui, "textEdit_ai_pre_test_input", None)
        if input_widget is None:
            return
        input_source = str(input_widget.toPlainText() or "").strip()
        if not input_source:
            _tip("请输入文案！")
            return
        try:
            default_api_key = str(_sq_jqm.get_ai_default_api_key() or "").strip()
        except Exception:
            default_api_key = ""
        if not default_api_key:
            _tip("功能暂时不可用，请联系客服！")
            return

        if self.is_sexy_ai():
            employee_test = AiEmployeeBean(
                uid=10086,
                name="官方色情大师",
                role=_inner("SEXY_DEFAULT_ROLE"),
                pre_text=_inner("SEXY_DEFAULT_PRE_TEXT"),
                sensitive=_inner("SENSITIVE_DEFAULT"),
                word_min=20,
                word_max=100,
            )
        else:
            employee_test = AiEmployeeBean(
                uid=10087,
                name="官方中文记者",
                role=_inner("NEWS_DEFAULT_ROLE"),
                pre_text=_inner("NEWS_DEFAULT_PRE_TEXT"),
                sensitive=_inner("SENSITIVE_DEFAULT"),
                word_min=20,
                word_max=100,
            )
        try:
            employee_test.model = str(_sq_jqm.get_default_ai_model() or "")
        except Exception:
            employee_test.model = ""

        self.change_test_run_button(False)

        def finish_call(status: AiTextGenStatus, output_text: str = "") -> None:
            self._finish_bridge.finished.emit(status, str(output_text or ""))

        def button_callback() -> None:
            manager = self.cooldown_manager
            handle_click = getattr(manager, "handle_click", None)
            if callable(handle_click):
                try:
                    handle_click(1500)
                except Exception:
                    return None

        try:
            if AITextGenTextRunnable is None:
                raise RuntimeError("AITextGenTextRunnable 尚未恢复")
            runnable = AITextGenTextRunnable(
                default_api_key,
                input_source,
                employee_test,
                finish_call,
            )
            QThreadPool.globalInstance().start(runnable)
            button_callback()
        except Exception as exc:
            print("AI 测试启动失败：", exc)
            self._apply_ai_test_finish(AiTextGenStatus.FAILED, str(exc))


__all__ = ["AiTestTab"]
