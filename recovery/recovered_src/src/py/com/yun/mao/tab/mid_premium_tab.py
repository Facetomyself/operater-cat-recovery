# Recovered module: src.py.com.yun.mao.tab.mid_premium_tab
# Membership purchase tab.  The order fields, payment modes and UI names are
# exact constants; helper fallbacks are explicitly marked inferred.
from __future__ import annotations

import time
from typing import Any

from PyQt5.QtCore import Qt, QThreadPool

from ..dialog import ImageDialogHelper
from ..dialog.PremiumBigPriceDialog import PremiumBigPriceDialog
from ..dialog.PremiumDialog import PremiumDialog
from ..fea import _sq_jqm, _sq_ks
from ..fea._cj_dd_file import CreateOrderTask
from ..kv_nx.dv_r4_uw_l7 import tw_k2_sk
from ..prices import PaymentHelper, PaymentPriceCalculator, PremiumTipHtmlFormatter
from ..prices.PriceTableTextHelper import get_subscription_html_dark
from ..util.EnumClass import CARD_ADVANCED, CARD_BEGINNER, CARD_GEEK
from ..util.need import ShotUtils, signals, utils
from ..util.need.AllBeanDef import CreateOrderBean, PremiumEnumBean
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


def _checked(widget: Any) -> bool:
    try:
        return bool(widget.isChecked())
    except Exception:
        return False


def _set_enabled(widget: Any, enabled: bool) -> None:
    try:
        widget.setEnabled(bool(enabled))
    except Exception:
        return None


def _set_checked(widget: Any, checked: bool) -> None:
    try:
        widget.setChecked(bool(checked))
    except Exception:
        return None


class PremiumTab(MidBaseTab):
    ACCOUNT_EFFECTIVE_INTERVAL_SECOND = 1800

    def __init__(self, mainWindow: Any, ui: Any) -> None:
        super().__init__()
        self.mainWindow = mainWindow
        self.ui = ui
        self.order = None
        self.premiumEnum = None
        self.select_otype = ""
        self.select_grade = CARD_BEGINNER
        self.select_days = "1"
        self.select_ai = False
        self.select_pre_cost = ""
        self.select_desc = ""
        self.current_account_time = 0.0
        self.init()
        self.reset_values()

    def reset_values(self) -> None:
        self.order = None
        self.select_otype = ""
        self.select_grade = CARD_BEGINNER
        self.select_days = "1"
        self.select_ai = False
        self.select_pre_cost = ""
        self.select_desc = ""
        _set_checked(getattr(self.ui, "radioButton_beginner", None), True)
        _set_checked(getattr(self.ui, "radioButton_1_d", None), True)
        _set_checked(getattr(self.ui, "radioButton_ai_disable", None), True)

    def init(self) -> None:
        _connect(
            getattr(self.ui, "premium_btn_show_big", None),
            "clicked",
            self.on_premium_show_big_price,
        )
        _connect(
            getattr(self.ui, "btn_gen_order", None),
            "clicked",
            self.on_create_order,
        )
        _connect(
            getattr(self.ui, "premium_main_btn_jiao_chen", None),
            "clicked",
            self.onShouPremiumCourseDialog,
        )
        _connect(
            getattr(self.ui, "premium_main_btn_ai_effect_show", None),
            "clicked",
            self.on_ai_effect_show,
        )
        _connect(
            getattr(self.ui, "comboBox_payment_type", None),
            "currentIndexChanged",
            self.on_payment_changed,
        )
        for name in ("radioButton_beginner", "radioButton_advanced", "radioButton_geek"):
            _connect(getattr(self.ui, name, None), "toggled", self.on_grade_toggled)
        for name in ("radioButton_1_d", "radioButton_15_d", "radioButton_30_d", "radioButton_90_d"):
            _connect(getattr(self.ui, name, None), "toggled", self.on_days_toggled)
        for name in ("radioButton_ai_enable", "radioButton_ai_disable"):
            _connect(getattr(self.ui, name, None), "toggled", self.on_ai_toggled)

        for signal_name, slot in (
            ("cmd_create_order_success", self.on_create_order_success),
            ("cmd_create_order_failed", self.on_create_order_failed),
            ("cmd_check_order_stats", self.on_tab_check_order_stats),
            ("cmd_activate_code_stats", self.on_tab_activate_code_stats),
        ):
            signal = getattr(signals.global_ui_signal, signal_name, None)
            if signal is not None:
                try:
                    signal.connect(slot)
                except Exception as exc:
                    print("连接会员信号失败：", exc)
        corrupted = getattr(signals.global_ui_signal, "report_init_resp_corrupted", None)
        if corrupted is not None and callable(tw_k2_sk):
            try:
                corrupted.connect(tw_k2_sk)
            except Exception as exc:
                print("连接账号刷新异常信号失败：", exc)

        label = getattr(self.ui, "label_payment_tip_desc", None)
        if label is not None:
            label.setTextFormat(Qt.RichText)
        self.show_top_tip()
        self._set_up_account_info()
        self.setup_payment_enum()
        self._inner_update_payment_info()

    def on_tab_activate_code_stats(self, success: bool) -> None:
        _tip("激活码使用成功！" if success else "激活码使用失败，请重试！")

    def on_tab_check_order_stats(self, success: bool, content_oj: Any) -> None:
        if success:
            _tip("查询订单成功！")
        else:
            message = ""
            if isinstance(content_oj, dict):
                message = str(content_oj.get("msg", ""))
            _tip(message or "查询订单失败，请重试！")

    def on_premium_show_big_price(self) -> None:
        html = get_subscription_html_dark(self.select_desc or self.select_pre_cost)
        try:
            PremiumBigPriceDialog(self.mainWindow, "套餐价格表", html).exec_()
        except Exception as exc:
            print("打开发大价格表失败：", exc)

    def on_ai_effect_show(self) -> None:
        try:
            ImageDialogHelper.unifyShowYouKeAiCourse(self)
        except Exception as exc:
            print("打开 AI 效果展示失败：", exc)

    def onShouPremiumCourseDialog(self) -> None:
        try:
            ImageDialogHelper.unifyShowPremiumCourse(self)
        except Exception as exc:
            print("打开会员教程失败：", exc)

    def show_top_tip(self) -> None:
        text = "各位朋友，大家可以自助购买会员了，快来体验吧！"
        label = getattr(self.ui, "premium_right_top_tip", None)
        if label is not None:
            label.setText(text)

    def on_tab_show(self) -> None:
        self._set_up_account_info()
        self._inner_update_payment_info()

    def _set_up_account_info(self) -> None:
        try:
            account = _sq_jqm.current_account_info
        except Exception:
            account = None
        now = time.time()
        if account is None:
            print("需要更新账号信息")
            return
        if now - self.current_account_time < self.ACCOUNT_EFFECTIVE_INTERVAL_SECOND:
            return
        self.current_account_time = now

        def account_update() -> None:
            self._inner_update_payment_info()

        updater = getattr(_sq_ks, "kj_by_jy", None)
        if callable(updater):
            try:
                updater(account_update)
                return
            except Exception as exc:
                print("刷新账号信息失败：", exc)
        account_update()

    def _inner_update_payment_info(self) -> None:
        try:
            self.premiumEnum = PaymentHelper.gen_premiumEnumBean_info(
                getattr(_sq_jqm, "current_account_info", None)
            )
        except Exception:
            self.premiumEnum = PremiumEnumBean()
        if not self.premiumEnum or not getattr(self.premiumEnum, "models", None):
            _tip("信息获取失败，请你重启软件！")
            return
        mode = self.select_otype or "充值模式"
        operational = PaymentHelper.operational_tip_for_payment_mode(mode)
        status = PaymentHelper.gen_payment_tip(
            getattr(_sq_jqm, "current_account_info", None),
            self.premiumEnum,
        )
        banner = PremiumTipHtmlFormatter.build_account_type_banner_html(
            utils.gen_grade_card_str(self.select_grade),
            bool(getattr(self.premiumEnum, "remaining", 0)),
        )
        html = PremiumTipHtmlFormatter.build_combined_payment_tip_html(
            operational,
            status,
            banner,
        )
        label = getattr(self.ui, "label_payment_tip_desc", None)
        if label is not None:
            label.setText(html)
        self._refresh_combined_payment_tip()

    def on_grade_toggled(self, checked: bool) -> None:
        if not checked:
            return
        if _checked(getattr(self.ui, "radioButton_beginner", None)):
            self.select_grade = CARD_BEGINNER
        elif _checked(getattr(self.ui, "radioButton_advanced", None)):
            self.select_grade = CARD_ADVANCED
        elif _checked(getattr(self.ui, "radioButton_geek", None)):
            self.select_grade = CARD_GEEK
        self.on_calc_pre_cost_and_display()

    def on_ai_toggled(self, checked: bool) -> None:
        if not checked:
            return
        self.select_ai = _checked(getattr(self.ui, "radioButton_ai_enable", None))
        self.on_calc_pre_cost_and_display()

    def on_days_toggled(self, checked: bool) -> None:
        if not checked:
            return
        for name, days in (
            ("radioButton_1_d", "1"),
            ("radioButton_15_d", "15"),
            ("radioButton_30_d", "30"),
            ("radioButton_90_d", "90"),
        ):
            if _checked(getattr(self.ui, name, None)):
                self.select_days = days
                break
        self.on_calc_pre_cost_and_display()

    def on_payment_changed(self, index: int) -> None:
        combo = getattr(self.ui, "comboBox_payment_type", None)
        self.select_otype = str(combo.currentText() if combo is not None else "")
        if self.select_otype == "续费模式":
            self.set_grad_enable(False)
            self.set_ai_enable(False)
            self.set_day_enable(True)
        elif self.select_otype == "升级模式":
            self.set_grad_enable(True)
            self.set_ai_enable(True)
            self.set_day_enable(False)
        else:
            self.set_grad_enable(True)
            self.set_ai_enable(True)
            self.set_day_enable(True)
        self._inner_update_payment_info()
        _ = index

    def control_grad_stats(self, grade: Any) -> None:
        if grade == CARD_BEGINNER:
            _set_checked(getattr(self.ui, "radioButton_beginner", None), True)
        elif grade == CARD_ADVANCED:
            _set_checked(getattr(self.ui, "radioButton_advanced", None), True)
        elif grade == CARD_GEEK:
            _set_checked(getattr(self.ui, "radioButton_geek", None), True)

    def set_grad_enable(
        self,
        enable: bool,
        groups: Any = None,
        rb: Any = None,
    ) -> None:
        group = groups if groups is not None else getattr(self.ui, "grade_container_ww", None)
        if group is not None:
            _set_enabled(group, enable)
        if rb is not None:
            _set_enabled(rb, enable)

    def set_day_enable(
        self,
        enable: bool,
        groups: Any = None,
        rb: Any = None,
    ) -> None:
        group = groups if groups is not None else getattr(self.ui, "days_container_ww", None)
        if group is not None:
            _set_enabled(group, enable)
        if rb is not None:
            _set_enabled(rb, enable)

    def set_ai_enable(
        self,
        enable: bool,
        groups: Any = None,
        rb: Any = None,
    ) -> None:
        group = groups if groups is not None else getattr(self.ui, "ai_container_ww", None)
        if group is not None:
            _set_enabled(group, enable)
        if rb is not None:
            _set_enabled(rb, enable)

    def no_any_rb_check_fun(self, groups: Any, rb: Any) -> bool:
        if rb is not None and _checked(rb):
            return False
        for group in groups or []:
            for child in getattr(group, "findChildren", lambda *_: [])():
                if _checked(child):
                    return False
        return True

    def setup_payment_enum(self) -> None:
        try:
            premium_enum = PaymentHelper.gen_premiumEnumBean_info(
                getattr(_sq_jqm, "current_account_info", None)
            )
        except Exception:
            premium_enum = None
        self.premiumEnum = premium_enum
        combo = getattr(self.ui, "comboBox_payment_type", None)
        if combo is None:
            return
        models = list(getattr(premium_enum, "models", []) or [])
        combo.clear()
        if models:
            combo.addItems([str(item) for item in models])
            combo.setCurrentIndex(0)
        else:
            combo.addItems(["充值模式", "续费模式", "升级模式"])
            combo.setCurrentIndex(0)

    def _refresh_combined_payment_tip(self) -> None:
        mode = self.select_otype or "充值模式"
        operational = PaymentHelper.operational_tip_for_payment_mode(mode)
        status = PaymentHelper.gen_payment_tip(
            getattr(_sq_jqm, "current_account_info", None),
            self.premiumEnum,
        )
        banner = PremiumTipHtmlFormatter.build_account_type_banner_html(
            utils.gen_grade_card_str(self.select_grade),
            getattr(self.premiumEnum, "remaining", 0) > 0,
        )
        self.select_desc = PremiumTipHtmlFormatter.build_combined_payment_tip_html(
            operational,
            status,
            banner,
        )

    def on_calc_pre_cost_and_display(self) -> None:
        try:
            price_config = PaymentHelper.get_price_config()
        except Exception:
            price_config = {}
        try:
            result = PaymentPriceCalculator.gen_payment_price(
                getattr(_sq_jqm, "current_account_info", None),
                self.premiumEnum,
                text=self.select_otype or "充值模式",
                price_config=price_config,
                tart_days=self.select_days,
                tart_grade=self.select_grade,
                tart_ai=self.select_ai,
            )
        except Exception:
            result = {"price": 0, "tip": ""}
        price = result.get("price", 0) if isinstance(result, dict) else 0
        tip = result.get("tip", "") if isinstance(result, dict) else ""
        self.select_pre_cost = f"{price} U"
        self.select_desc = str(tip or "")
        label = getattr(self.ui, "label_pre_cost", None)
        if label is not None:
            label.setTextFormat(Qt.RichText)
            label.setText(
                PremiumTipHtmlFormatter.build_pre_cost_html(
                    tip,
                    self.select_pre_cost,
                    bool(price),
                )
            )
        self.display_prices_desc(
            getattr(self.ui, "premium_label_price", None),
            self.select_desc,
        )

    def on_create_order_failed(self, msg: str) -> None:
        _tip(str(msg or "创建订单失败，请重试！"))

    def on_create_order_success(self, order: Any) -> None:
        self.order = order
        onumber = str(getattr(order, "onumber", "") or "")
        odesc = str(getattr(order, "odesc", "") or "")
        amount = float(getattr(order, "amount", 0) or 0)
        print(
            "创建订单成功，订单号： ",
            onumber,
            " 订单描述： ",
            odesc,
            " 应实付： ",
            f"{amount:.3f}U",
        )
        try:
            PremiumDialog(self.mainWindow, "支付订单", order).exec_()
        except Exception as exc:
            print("打开支付窗口失败：", exc)
        _ = onumber

    def on_create_order(self) -> None:
        if not self.select_grade and not self.select_days:
            _tip("请先选择天数或者等级！")
            return
        try:
            account = _sq_jqm.current_account_info
        except Exception:
            account = None
        if account is None:
            _tip("信息获取失败，请你重启软件！")
            return
        shot = getattr(ShotUtils, "shot", None)
        if callable(shot):
            try:
                shot(millisecond=8000)
            except Exception:
                return None
        order_bean = CreateOrderBean(
            otype=self.select_otype or "充值模式",
            ucode=str(getattr(account, "ucode", "") or ""),
            amount=self.select_pre_cost,
            gradeStr=str(utils.select_grade_to_request_params(self.select_grade)),
            hoursStr=str(self.select_days),
            botStr="",
            aiStr="1" if self.select_ai else "0",
            odesc=str(self.select_desc or "").replace("\n", "").strip(),
        )
        try:
            task = CreateOrderTask((order_bean,))
            QThreadPool.globalInstance().start(task)
        except Exception as exc:
            print("创建订单任务启动失败：", exc)
            _tip("创建订单失败，请重试！")

    def display_prices_desc(self, label: Any, current_prices: Any = "") -> None:
        if label is None:
            return
        label.setTextFormat(Qt.RichText)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label.setStyleSheet("QLabel { background: transparent; }")
        try:
            label.setText(get_subscription_html_dark(current_prices))
        except Exception:
            label.setText(str(current_prices or ""))


__all__ = ["PremiumTab"]
