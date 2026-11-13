# Recovered module: src.py.com.yun.mao.tab.mid_toolbox_tab
# Toolbox tab: ad HTML generation, ad test posting and machine-code migration.
from __future__ import annotations

import json
import os
from typing import Any

from PyQt5.QtCore import Qt, QThreadPool

from ..ad.ToolsBoxEditAdDialog import ToolsBoxEditAdDialog
from ..config import YunYinMaoConfig, tabl_cache
from ..dclass import DTopClassHelper
from ..dialog import ImageDialogHelper
from ..fea._qy_hy_file import FeaMigrateCodeTask
from ..mthread.GenHtmlThread import GenHtmlThread
from ..mthread.PostHtmlADThread import PostHtmlADThread
from ..tgaccount.TGAuthAccount import TGAuthAccount
from ..util import TracePrinterHelper
from ..util.need import ShotUtils, signals, utils
from ..util.need.AllBeanDef import GenHtmlParamsBean, MigrateCodeBean, PostAdTestBean
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


def _changed_widget(widget: Any, enable: bool) -> None:
    if widget is None:
        return
    try:
        widget.setEnabled(bool(enable))
    except Exception:
        return None
    changed = getattr(ShotUtils, "changed_widget", None)
    if callable(changed):
        try:
            changed(widget, enable=enable)
        except Exception:
            return None


class ToolBoxTab(MidBaseTab):
    def __init__(self, mainWindow: Any, ui: Any) -> None:
        super().__init__()
        self.mainWindow = mainWindow
        self.ui = ui
        self.gen_html_thread = None
        self.post_ad_thread = None
        self.ad_html_source = ""
        self.ad_files: list[str] = []
        self.init()

    def init(self) -> None:
        _connect(
            getattr(self.ui, "tools_box_ad_jiao_chen", None),
            "clicked",
            self.on_show_ad_jiao_chen,
        )
        _connect(
            getattr(self.ui, "tools_btn_gen_html", None),
            "clicked",
            self.gen_html,
        )
        _connect(
            getattr(self.ui, "tools_move_permission", None),
            "clicked",
            self.move_permission,
        )
        _connect(
            getattr(self.ui, "tools_btn_edit_ad", None),
            "clicked",
            self.edit_ad,
        )
        _connect(
            getattr(self.ui, "tools_btn_post_ad", None),
            "clicked",
            self.post_ad,
        )
        _connect(
            getattr(self.ui, "btn_qian_yi_jiao_chen", None),
            "clicked",
            self.show_qian_yi_jiao_chen,
        )

        for signal_name, slot in (
            ("cmd_update_stats", self.on_update_stats),
            ("cmd_migrate_code_stats", self.on_migrate_code_stats),
            ("cmd_post_ad_stats", self.on_post_ad_stats),
        ):
            signal = getattr(signals.global_ui_signal, signal_name, None)
            if signal is not None:
                try:
                    signal.connect(slot)
                except Exception as exc:
                    print("连接工具箱信号失败：", exc)
        self.dis_play_config_tip()

    def on_post_ad_stats(self, data: Any) -> None:
        success, message = _unpack_result(data)
        if success:
            _tip(str(message or "发布测试广告成功！"))
        else:
            _tip(str(message or "发布测试广告失败，请查找原因！"))
        self.post_ad_thread = None
        self.lock_ui(False)

    def on_migrate_code_stats(self, success: bool, message: str = "") -> None:
        if success:
            _tip("迁移完成！")
        else:
            _tip(str(message or "迁移失败，请重试！"))
        self.lock_ui(False)

    def on_update_stats(self, data: Any) -> None:
        success, message = _unpack_result(data)
        if success and message:
            self.comment_ad_call_back(str(message), [])
            _tip("HTML 生成成功，已写入广告文本！")
        else:
            _tip(str(message or "HTML 生成失败，请查找原因！"))
        self.gen_html_thread = None
        self.lock_ui(False)

    def lock_ui(self, enable: bool) -> None:
        for name in (
            "tools_btn_gen_html",
            "tools_btn_post_ad",
            "tools_move_permission",
            "tools_btn_edit_ad",
        ):
            _changed_widget(getattr(self.ui, name, None), enable)

    def get_session_path(self) -> str:
        try:
            json_string = tabl_cache.INSTANCE().read_cache(
                tabl_cache.PROXY_SETTING_GROUP,
                tabl_cache.CURRENT_TASK_TG_ACCOUNT,
                "",
            )
        except Exception:
            json_string = ""
        if not json_string:
            _tip("请你切换到【自动运营】->任务账号设置->选择账号 配置电报账号！")
            return ""
        try:
            payload = json.loads(str(json_string))
            tg = TGAuthAccount(**payload) if isinstance(payload, dict) else payload
        except Exception:
            tg = None
        if tg is None:
            _tip("请你切换到【自动运营】->任务账号设置->选择账号 配置电报账号！")
            return ""
        session_file = str(getattr(tg, "session", "") or "")
        if not session_file:
            _tip("请你切换到【自动运营】->任务账号设置->选择账号 配置电报账号！")
            return ""
        if os.path.isabs(session_file):
            return session_file
        return os.path.join(str(YunYinMaoConfig.abs_tg_account_dir()), session_file)

    def comment_ad_call_back(
        self,
        ad_html: str,
        legal_files: list[str] | str | None = None,
    ) -> None:
        self.ad_html_source = str(ad_html or "")
        if isinstance(legal_files, str):
            self.ad_files = [legal_files] if legal_files else []
        else:
            self.ad_files = list(legal_files or [])
        try:
            cache = tabl_cache.INSTANCE()
            cache.update_cache(
                tabl_cache.MAIN_TOOLS_BOX_SECTION,
                tabl_cache.MAIN_TOOLS_BOX_AD_HTML_TEXT,
                DTopClassHelper.ad_str_to_file(self.ad_html_source),
            )
            cache.update_cache(
                tabl_cache.MAIN_TOOLS_BOX_SECTION,
                tabl_cache.MAIN_TOOLS_BOX_AD_FILES,
                "|".join(self.ad_files),
            )
        except Exception as exc:
            print("保存广告配置失败：", exc)
        self.dis_play_config_tip()

    def dis_play_config_tip(self) -> None:
        try:
            cache = tabl_cache.INSTANCE()
            html_file = cache.read_cache(
                tabl_cache.MAIN_TOOLS_BOX_SECTION,
                tabl_cache.MAIN_TOOLS_BOX_AD_HTML_TEXT,
                "",
            )
            files_text = cache.read_cache(
                tabl_cache.MAIN_TOOLS_BOX_SECTION,
                tabl_cache.MAIN_TOOLS_BOX_AD_FILES,
                "",
            )
            self.ad_html_source = (
                DTopClassHelper.ad_file_to_str(str(html_file or ""))
                if html_file
                else ""
            )
            self.ad_files = [item for item in str(files_text or "").split("|") if item]
            self.update_status_label(
                "有" if self.ad_html_source else "没",
                "有" if self.ad_files else "没",
                "当前配置： {}广告文本，{}广告媒体。",
                True,
            )
        except Exception as exc:
            print("读取广告配置失败：", exc)

    def update_status_label(
        self,
        ads_text: str,
        ads_media: str,
        text: str = "当前配置： {}广告文本，{}广告媒体。",
        highlighted: bool = False,
    ) -> None:
        label = getattr(self.ui, "label_ad_config_tip", None)
        if label is None:
            return
        try:
            label.setTextFormat(Qt.RichText)
        except Exception:
            return None
        if highlighted:
            ads_text = (
                '<span style="color:#00cc00;font-weight:bold;">有</span>'
                if ads_text == "有"
                else '<span style="color:#ff4444;font-weight:bold;">没</span>'
            )
            ads_media = (
                '<span style="color:#00cc00;font-weight:bold;">有</span>'
                if ads_media == "有"
                else '<span style="color:#ff4444;font-weight:bold;">没</span>'
            )
        try:
            label.setText(str(text or "").format(ads_text, ads_media))
        except Exception:
            label.setText(f"当前配置： {ads_text}广告文本，{ads_media}广告媒体。")

    def edit_ad(self) -> None:
        shot = getattr(ShotUtils, "shot", None)
        if callable(shot):
            try:
                shot()
            except Exception:
                return None
        try:
            dialog = ToolsBoxEditAdDialog(
                self.mainWindow,
                "编辑广告测试文案",
                self.comment_ad_call_back,
                self.ad_html_source,
                list(self.ad_files),
            )
            dialog.exec_()
        except Exception as exc:
            print("打开广告编辑窗口失败：", exc)

    def show_qian_yi_jiao_chen(self) -> None:
        try:
            ImageDialogHelper.unifyShowQianYiCourse(self)
        except Exception as exc:
            print("打开迁移教程失败：", exc)

    def on_show_ad_jiao_chen(self) -> None:
        try:
            ImageDialogHelper.unifyShowAdCourse(self)
        except Exception as exc:
            print("打开广告教程失败：", exc)

    def gen_html(self) -> None:
        post_link = str(
            getattr(self.ui, "lineEdit_tools_post_link", None).text()
            if getattr(self.ui, "lineEdit_tools_post_link", None) is not None
            else ""
        ).strip()
        if not post_link:
            _tip("请输入 帖子链接 ！")
            return
        if not post_link.startswith("https://t.me/"):
            _tip("帖子链接 必须是https开头的电报帖子链接！")
            return
        abs_session_file = self.get_session_path()
        if not abs_session_file:
            return
        try:
            params = GenHtmlParamsBean(
                session_abs_path=abs_session_file,
                stats_signal=signals.global_ui_signal.cmd_update_stats,
                post_link=post_link,
            )
            self.gen_html_thread = GenHtmlThread(params)
            self.lock_ui(False)
            self.gen_html_thread.start()
        except Exception as exc:
            self.lock_ui(True)
            TracePrinterHelper.print_trace(exc)
            _tip("HTML 生成启动失败：" + str(exc))

    def post_ad(self) -> None:
        post_link_text = str(
            getattr(self.ui, "lineEdit_tools_post_link", None).text()
            if getattr(self.ui, "lineEdit_tools_post_link", None) is not None
            else ""
        ).strip()
        ad_source = str(
            getattr(self.ui, "lineEdit_ad_post_source", None).text()
            if getattr(self.ui, "lineEdit_ad_post_source", None) is not None
            else ""
        ).strip()
        if not post_link_text:
            _tip("请输入 帖子链接 ！")
            return
        if not utils.is_legal_source(post_link_text):
            _tip("请输入 频道或者群组 ！")
            return
        utils.strict_check_source(ad_source)
        if not self.ad_html_source:
            _tip("请你先编辑广告文本！")
            return
        abs_session_file = self.get_session_path()
        if not abs_session_file:
            return
        try:
            params = PostAdTestBean(
                session_abs_path=abs_session_file,
                stats_signal=signals.global_ui_signal.cmd_post_ad_stats,
                channel_source=post_link_text,
                ad_html_text=self.ad_html_source,
                ad_files=list(self.ad_files),
            )
            self.post_ad_thread = PostHtmlADThread(params)
            self.lock_ui(False)
            self.post_ad_thread.start()
        except Exception as exc:
            self.lock_ui(True)
            TracePrinterHelper.print_trace(exc)
            _tip("发布测试广告启动失败：" + str(exc))

    def move_permission(self) -> None:
        old_widget = getattr(self.ui, "lineEdit_old_u_code", None)
        new_widget = getattr(self.ui, "lineEdit_new_u_code", None)
        old_u_code = str(old_widget.text() if old_widget is not None else "").strip()
        new_u_code = str(new_widget.text() if new_widget is not None else "").strip()
        if not old_u_code:
            _tip("请输入 旧机器码 ！")
            return
        if not new_u_code:
            _tip("请输入 新机器码 ！")
            return
        old_u_code = utils.clean_code(old_u_code)
        new_u_code = utils.clean_code(new_u_code)
        if old_u_code == new_u_code:
            _tip("新旧机器码不能相同！")
            return
        cover_expri = bool(
            getattr(self.ui, "cb_cover_expri", None).isChecked()
            if getattr(self.ui, "cb_cover_expri", None) is not None
            else False
        )
        force_cover_yun = bool(
            getattr(self.ui, "cb_cover_item_yun", None).isChecked()
            if getattr(self.ui, "cb_cover_item_yun", None) is not None
            else False
        )
        try:
            MigrateCodeBean(
                old_u_code=old_u_code,
                new_u_code=new_u_code,
                cover_expri=cover_expri,
                force_cover_yun=force_cover_yun,
            )
            task = FeaMigrateCodeTask(
                (old_u_code, new_u_code, cover_expri, force_cover_yun)
            )
            QThreadPool.globalInstance().start(task)
            self.lock_ui(False)
        except Exception as exc:
            TracePrinterHelper.print_trace(exc)
            _tip("迁移任务启动失败：" + str(exc))


def _unpack_result(data: Any) -> tuple[bool, Any]:
    if isinstance(data, (tuple, list)):
        if len(data) >= 2:
            return bool(data[0]), data[1]
        if data:
            return bool(data[0]), ""
    if isinstance(data, dict):
        return bool(data.get("success", False)), data.get("message", "")
    return bool(data), data


__all__ = ["ToolBoxTab"]
