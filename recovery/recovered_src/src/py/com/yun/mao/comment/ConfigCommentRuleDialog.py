# Recovered module: src.py.com.yun.mao.comment.ConfigCommentRuleDialog
# Reconstruction from Nuitka constants, method table, and offline Hex-Rays.
# UI/bean assembly is behavior-level where the exact original expression is
# not provable from the stripped binary; those spots are marked inferred.
from __future__ import annotations

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QListWidgetItem,
    QMenu,
    QShowEvent,
)

from src.py.com.yun.mao.ad import AddOrEditAdDialog, UIAdListOp
from src.py.com.yun.mao.auto import CMCode
from src.py.com.yun.mao.config import NewConfig, YunYinMaoConfig
from src.py.com.yun.mao.config.YunYinMaoConfig import COMMENT_WANT_COUNT_MAX
from src.py.com.yun.mao.dclass import DTopClassHelper
from src.py.com.yun.mao.dclass.DTopClass import (
    Ad,
    AdWrapper,
    AdvancedFilterBean,
    AiRefusedOption,
    CommentRuleBean,
    ForwardActionBean,
    GridOpt,
    Replace,
    Tail,
    Water,
    YuLanResOp,
)
from src.py.com.yun.mao.dialog import ImageDialogHelper
from src.py.com.yun.mao.fea import _sq_jqm
from src.py.com.yun.mao.tgaccount import AiEmployeeListDialog
from src.py.com.yun.mao.util import ResourcePath
from src.py.com.yun.mao.util.need import BaseDialog, CommonCode, ShotUtils, utils
from src.py.com.yun.mao.util.need.AllBeanDef import AiEmployeeBean


class ConfigCommentRuleDialog(BaseDialog):
    def __init__(
        self,
        parent=None,
        windowTitle: str | None = None,
        funBack=None,
        comment=None,
        ad=None,
    ) -> None:
        super().__init__(parent)
        self.commentRule = comment
        self.employee_id = getattr(comment, "employee_id", None) if comment else None
        self.temp_water_image_abs_path = ""
        self.temp_water_pic_ratio = 30
        self.adMap: dict[object, Ad] = {}
        self.selfAdWrapper = None
        self.ades: list[Ad] = []
        self.adId = getattr(ad, "adId", None) if ad else None
        self.aiEmployee = None
        self.uid = getattr(comment, "uid", None) if comment else None
        self.water = None
        self.picPath = ""
        self.picRatio = 30
        self.funBack = funBack
        if windowTitle:
            self.setWindowTitle(windowTitle)

        self.ui = uic.loadUi(
            ResourcePath.get_ui_path("by_comment_rule_config.ui"), self
        )
        self.ui.btn_save_yun_yin_item_comment.clicked.connect(self.saveCommentRule)
        self.ui.btn_add_ad_comment.clicked.connect(self.addCommentAd)
        self.ui.by_comment_res_btn_jiao_chen.clicked.connect(
            self.showResourceTypeDialog
        )
        self.ui.btn_by_com_config_res_op_jiao_chen.clicked.connect(
            self.showResOpDialog
        )
        self.ui.btn_banyun_com_select_ai_em.clicked.connect(self.on_select_ai_em)
        self.ui.btn_banyun_com_water_pic_jiao_chen.clicked.connect(
            self.on_show_pic_water_jiao_chen
        )
        self.ui.btn_banyun_com_water_select_pic.clicked.connect(self.on_select_pic)
        self.ui.btn_by_com_grid_jiao_chen.clicked.connect(self.on_grid_jiao_chen)
        self.ui.ban_yun_com_cover_jiao_chen.clicked.connect(
            self.on_random_cover_jiao_chen
        )
        self.ui.cb_banyun_com_water_mode.currentIndexChanged.connect(
            self.showWaterSelectMode
        )
        self.ui.cb_banyun_com_water_mode.setCurrentText(
            NewConfig.WATER_MODE_TIP_PIC
        )
        self.ui.listWidget_private_ad_list_comment.setContextMenuPolicy(
            Qt.CustomContextMenu
        )
        self.ui.listWidget_private_ad_list_comment.customContextMenuRequested.connect(
            self.shoeMenu
        )
        self.ui.label_banyun_com_ai_name.setText("当前选择：无")
        self.initCheckBoxControlQuYu()
        self.fillDefault()
        self.fillBeanIfNeed()
        self.fillAdList()

    def on_select_ai_em_callback(self, em) -> None:
        self.aiEmployee = em
        if em is not None:
            self.employee_id = getattr(em, "uid", self.employee_id)
        name = getattr(em, "name", "无") if em is not None else "无"
        self.ui.label_banyun_com_ai_name.setText("当前选择：" + str(name))

    def on_select_ai_em(self) -> None:
        if _sq_jqm.has_ai_ability_but_no_key():
            print("你还没有配置专属的AI API KEY")
            ImageDialogHelper.unifyShowInputApiKeyCourse(ShotUtils.shot(self))
            return
        dialog = AiEmployeeListDialog(self, self.on_select_ai_em_callback)
        dialog.exec()

    def showResourceTypeDialog(self) -> None:
        ImageDialogHelper.unifyShowResTypeCourse(ShotUtils.shot(self))

    def showResOpDialog(self) -> None:
        ImageDialogHelper.unifyShowPublishResOpCourse(ShotUtils.shot(self))

    def on_grid_jiao_chen(self) -> None:
        ImageDialogHelper.unifyShowGridCourse(ShotUtils.shot(self))

    def on_random_cover_jiao_chen(self) -> None:
        ImageDialogHelper.unifyShowRandomCoverCourse(ShotUtils.shot(self))

    def on_show_pic_water_jiao_chen(self) -> None:
        ImageDialogHelper.unifyShowPicWaterCourse(ShotUtils.shot(self))

    def on_select_pic(self) -> None:
        file_filter = "图片文件 (*.jpg *.jpeg *.png)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", file_filter
        )
        if not file_path:
            self.ui.label_banyun_com_water_pic_path.setText("未选择任何图片")
            self.ui.label_banyun_com_water_pic_path.setToolTip("")
            return
        self.temp_water_image_abs_path = file_path
        self.picPath = file_path
        self.set_elided_path(file_path)
        self.ui.label_banyun_com_water_pic_path.setToolTip(file_path)

    def set_elided_path(self, full_path: str) -> None:
        elided_text = CMCode.elide_path_middle(full_path, 40)
        self.ui.label_banyun_com_water_pic_path.setText(
            "图片路径：" + str(elided_text)
        )
        self.ui.label_banyun_com_water_pic_path.setToolTip(full_path)

    def showWaterSelectMode(self) -> None:
        mode = self.ui.cb_banyun_com_water_mode.currentText()
        if mode == NewConfig.WATER_MODE_TIP_TEXT:
            self.ui.text_water_wrapper.setVisible(True)
            self.ui.pic_water_wrapper.setVisible(False)
        else:
            self.ui.text_water_wrapper.setVisible(False)
            self.ui.pic_water_wrapper.setVisible(True)

    def changedWaterModeUIComponent(self) -> None:
        mode = self.ui.cb_banyun_com_water_mode.currentText()
        self.ui.cb_banyun_com_water_mode.setCurrentText(mode)
        self.showWaterSelectMode()

    def shoeMenu(self, pos) -> None:
        item = self.ui.listWidget_private_ad_list_comment.itemAt(pos)
        if item is None:
            return
        ad = item.data(Qt.UserRole)
        if ad is None:
            ad = item.data(32)
        menu = QMenu()
        edit = QAction("编辑私有广告", self)
        dele = QAction("删除私有广告", self)
        edit.triggered.connect(lambda: self.editItem(ad))
        dele.triggered.connect(lambda: self.deleteItem(ad))
        menu.addAction(edit)
        menu.addAction(dele)
        menu.exec_(
            self.ui.listWidget_private_ad_list_comment.mapToGlobal(pos)
        )

    def saveCommentRule(self) -> None:
        # inferred: field-by-field validation and bean assembly follow the
        # constant table order; the original 124 KB function could not be
        # decompiled by Hex-Rays.
        copyComment_want_count_str = (
            self.ui.lineEdit_number_group_comment.text().strip()
        )
        success, copyComment_want_count = utils.parse_int(
            copyComment_want_count_str
        )
        if not success:
            print("请输入期望复刻评论区媒体数量（按组计算），需要输入整数！")
            return
        if copyComment_want_count <= 0:
            print("期望复刻评论区媒体数量（按组计算） 必须大于0！")
            return
        max_count = getattr(
            YunYinMaoConfig, "COMMENT_WANT_COUNT_MAX", COMMENT_WANT_COUNT_MAX
        )
        if copyComment_want_count > max_count:
            print("期望复刻评论区媒体数量（按组计算）最大不能超过", max_count)
            return

        video_photo = self.ui.checkBox_video_photo_comment.isChecked()
        photo = self.ui.checkBox_photo_comment.isChecked()
        video = self.ui.checkBox_video_comment.isChecked()
        file = self.ui.checkBox_file_comment.isChecked()
        text = self.ui.checkBox_text_comment.isChecked()
        if not any((video_photo, photo, video, file, text)):
            print("资源类型必须选择一个！")
            return
        if video_photo:
            dtype = DTopClassHelper.RESOURCE_TYPE_VIDEO_PHOTO
        elif photo:
            dtype = DTopClassHelper.RESOURCE_TYPE_PHOTO
        elif video:
            dtype = DTopClassHelper.RESOURCE_TYPE_VIDEO
        elif file:
            dtype = DTopClassHelper.RESOURCE_TYPE_FILE
        else:
            dtype = DTopClassHelper.RESOURCE_TYPE_TEXT

        action_auto = self.ui.radioButton_action_auto_comment.isChecked()
        action_download = self.ui.radioButton_action_download_comment.isChecked()
        if not action_auto and not action_download:
            print("搬运方式必须选择一个！")
            return
        action = (
            DTopClassHelper.ACTION_AUTO
            if action_auto
            else DTopClassHelper.ACTION_DOWNLOAD
        )

        auto_sleep_min_str = (
            self.ui.lineEdit_auto_sleep_min_comment.text().strip()
        )
        success, auto_sleep_min = utils.parse_int(auto_sleep_min_str)
        if not success:
            print("请输入随机休眠最小值，需要输入整数！（单位秒）")
            return
        if auto_sleep_min <= 0:
            print("随机休眠最小值不能小于等于0！")
            return
        auto_sleep_max_str = (
            self.ui.lineEdit_auto_sleep_max_comment.text().strip()
        )
        success, auto_sleep_max = utils.parse_int(auto_sleep_max_str)
        if not success:
            print("请输入随机休眠最大值，需要输入整数！（单位秒）")
            return
        if auto_sleep_max < auto_sleep_min:
            print("随机休眠最大值不能小于最小值！")
            return

        duration_min_str = (
            self.ui.lineEdit_ban_yun_duration_min_comment.text().strip()
        )
        duration_max_str = (
            self.ui.lineEdit_ban_yun_duration_max_comment.text().strip()
        )
        size_min_str = self.ui.lineEdit_ban_yun_mb_min_comment.text().strip()
        size_max_str = self.ui.lineEdit_ban_yun_mb_max_comment.text().strip()
        baseFilter = CommonCode.gen_base_filter(
            duration_min_str, duration_max_str, size_min_str, size_max_str
        )

        ad_enable = self.ui.checkBox_ad_enable_comment.isChecked()
        keepSourceText = self.ui.checkBox_origin_source_text_comment.isChecked()
        deleSourceText = self.ui.checkBox_dele_source_text_comment.isChecked()
        deleLink = self.ui.checkBox_dele_link_comment.isChecked()
        filterButton = self.ui.checkBox_fliter_button_comment.isChecked()
        discardNoTextResource = (
            self.ui.checkBox_discard_no_text_resource.isChecked()
        )
        chaiZu = self.ui.checkBox_chai_zu.isChecked()
        containWords = CommonCode.str_to_filter_words(
            self.ui.lineEdit_fliter_words_comment_contain.text()
        )
        excludeWords = CommonCode.str_to_filter_words(
            self.ui.lineEdit_fliter_words_comment_exclude.text()
        )
        tail = Tail(
            tail_text=self.ui.textEdit_tail_text_comment.toPlainText()
        )
        replaces = CommonCode.str_to_replaces(
            self.ui.textEdit_replace_rule_comment.toPlainText()
        )
        replace = Replace(replaces=replaces)

        enPic = self.ui.checkBox_pic_water_comment.isChecked()
        enVideo = self.ui.checkBox_video_water_comment.isChecked()
        waterText = self.ui.lineEdit_water_text_comment.text()
        index = self.ui.comboBox_video_minute_comment.currentIndex()
        duration = CommonCode.parseVideoDuration(index)
        water_pic_path = self.temp_water_image_abs_path or self.picPath
        water_mode = self.ui.cb_banyun_com_water_mode.currentText()
        pic_ratio_str = (
            self.ui.line_edit_by_com_rule_water_pic_ratio.text().strip()
        )
        success, pic_ratio = utils.parse_int(pic_ratio_str)
        if not success or pic_ratio < 10 or pic_ratio > 90:
            print(
                "请输入正整数，表示图片水印图片缩放百分比，范围是10~90！"
                "建议是输入30！"
            )
            return
        if water_mode == NewConfig.WATER_MODE_TIP_PIC and not water_pic_path:
            print("请选择图片水印的图片资源！")
            return
        water = Water(
            enPic=enPic,
            enVideo=enVideo,
            text=waterText,
            mode=water_mode,
            picPath=water_pic_path,
            picRatio=pic_ratio,
            duration=duration,
        )

        selfAd = AdWrapper(
            adEnable=ad_enable,
            ades=list(self.adMap.values()),
        )
        advance = AdvancedFilterBean(
            keepSourceText=keepSourceText,
            deleSourceText=deleSourceText,
            deleLink=deleLink,
            filterButton=filterButton,
            discardNoTextResource=discardNoTextResource,
            chaiZu=chaiZu,
            containWords=containWords,
            excludeWords=excludeWords,
        )
        forWardAction = ForwardActionBean(
            action=action,
        )

        blur = self.ui.cb_by_com_config_pic_blur.isChecked()
        spoiler = self.ui.cb_by_com_config_spoiler.isChecked()
        radius_text = self.ui.by_com_config_pic_blur_radius.text().strip()
        success, radius = utils.parse_int(radius_text)
        if not success or radius < 1 or radius > 20:
            print(
                "请输入模糊数值，需要输入整数！（值越大越模糊，范围是1~20，"
                "建议输入3）"
            )
            return
        resOp = YuLanResOp(
            picBlur=blur,
            spoiler=spoiler,
            radius=radius,
        )

        ai_enable = self.ui.checkBox_banyun_com_ai_enable.isChecked()
        if ai_enable and self.aiEmployee is None:
            print("请选择AI员工！")
            return
        ai_employee = self.aiEmployee
        if ai_employee is None:
            ai_employee = AiEmployeeBean()
        ai_action = (
            "origin"
            if self.ui.radioButton_ai_banyun_com_use_source.isChecked()
            else "skip"
        )
        aiopt = AiRefusedOption(action=ai_action)

        gridNumber_str = self.ui.lineEdit_by_com_grid_number.text().strip()
        success, gridNumber = utils.parse_int(gridNumber_str)
        if not success or gridNumber < 0 or gridNumber > 10:
            print(
                "电报单组消息最多10个资源，补齐x宫格高清视频截图数，请填写整数！"
                "范围必须是0~10，如果不懂，请点击【教程】按钮查看说明！"
            )
            return
        randomCover = self.ui.cb_ban_yun_com_random_cover.isChecked()
        grid = GridOpt(number=gridNumber)

        commentRule = CommentRuleBean(
            copyComment=True,
            wantCount=copyComment_want_count,
            dtype=dtype,
            forWardAction=forWardAction,
            baseFilter=baseFilter,
            advancedFilterBean=advance,
            tail=tail,
            replace=replace,
            water=water,
            selfAdWrapper=selfAd,
            yuLanResOp=resOp,
            aiEmployee=ai_employee,
            aiRefusedOpt=aiopt,
            grid=grid,
            randomCover=randomCover,
        )
        self.commentRule = commentRule
        if self.funBack:
            self.funBack(commentRule)
        self.close()

    def comment_ad_call_back(self, ad) -> None:
        if ad is None:
            return
        self.adMap[getattr(ad, "adId", id(ad))] = ad
        self.fillAdList()

    def addCommentAd(self) -> None:
        dialog = AddOrEditAdDialog(
            self, "添加评论区私有广告", self.comment_ad_call_back
        )
        dialog.exec_()

    def editItem(self, ad) -> None:
        dialog = AddOrEditAdDialog(
            self, "编辑评论区私有广告", ad, self.comment_ad_call_back
        )
        dialog.exec_()

    def deleteItem(self, ad) -> None:
        key = getattr(ad, "adId", id(ad))
        self.adMap.pop(key, None)
        self.fillAdList()

    def fillAdList(self) -> None:
        fill = getattr(UIAdListOp, "fillAd2List", None)
        if fill is not None:
            fill(
                self.ui.listWidget_private_ad_list_comment,
                list(self.adMap.values()),
            )
            return
        self.ui.listWidget_private_ad_list_comment.clear()
        for ad in self.adMap.values():
            item = QListWidgetItem(getattr(ad, "name", ""))
            item.setData(Qt.UserRole, ad)
            self.ui.listWidget_private_ad_list_comment.addItem(item)

    def initCheckBoxControlQuYu(self) -> None:
        self.ui.checkBox_ad_enable_comment.stateChanged.connect(
            self.onAdEnableChanged
        )
        self.ui.checkBox_origin_source_text_comment.stateChanged.connect(
            self.onKeepSourceChanged
        )
        self.ui.checkBox_chai_zu.stateChanged.connect(
            self._chai_zu_component_states
        )
        self.ui.checkBox_video_photo_comment.stateChanged.connect(
            self.videoPhotoChanged
        )
        self.ui.checkBox_banyun_com_ai_enable.stateChanged.connect(
            self.onAiEnableChanged
        )

    def onAiEnableChanged(self, state) -> None:
        enable = state == Qt.Checked
        self.ui.horizontalGroupBox_ai_banyun_com.setEnabled(enable)

    def fillDefault(self) -> None:
        self.ui.checkBox_ad_enable_comment.setChecked(True)
        self.ui.checkBox_origin_source_text_comment.setChecked(True)
        self.ui.checkBox_dele_source_text_comment.setChecked(False)
        self.ui.checkBox_dele_link_comment.setChecked(False)
        self.ui.checkBox_fliter_button_comment.setChecked(False)
        self.ui.radioButton_action_auto_comment.setChecked(True)
        self.ui.radioButton_action_download_comment.setChecked(False)
        self.ui.lineEdit_auto_sleep_min_comment.setText("3")
        self.ui.lineEdit_auto_sleep_max_comment.setText("5")
        self.ui.lineEdit_ban_yun_duration_min_comment.setText(
            str(YunYinMaoConfig.BASE_FILTER_DU_MIN)
        )
        self.ui.lineEdit_ban_yun_duration_max_comment.setText(
            str(YunYinMaoConfig.BASE_FILTER_DU_MAX)
        )
        self.ui.lineEdit_ban_yun_mb_min_comment.setText(
            str(YunYinMaoConfig.BASE_FILTER_SIZE_MIN)
        )
        self.ui.lineEdit_ban_yun_mb_max_comment.setText(
            str(YunYinMaoConfig.BASE_FILTER_SIZE_MAX)
        )
        self.ui.checkBox_video_photo_comment.setChecked(True)
        self.ui.checkBox_photo_comment.setChecked(True)
        self.ui.checkBox_video_comment.setChecked(True)
        self.ui.checkBox_file_comment.setChecked(True)
        self.ui.checkBox_text_comment.setChecked(True)
        self.ui.by_com_config_pic_blur_radius.setText("3")
        self.ui.checkBox_banyun_com_ai_enable.setChecked(False)
        self.ui.label_banyun_com_ai_name.setText("当前选择：无")
        self.ui.radioButton_ai_banyun_com_skip_source.setChecked(True)
        self.ui.line_edit_by_com_rule_water_pic_ratio.setText("30")
        self.ui.lineEdit_by_com_grid_number.setText("6")
        self._chai_zu_component_states()

    def fillBeanIfNeed(self) -> None:
        bean = self.commentRule
        if bean is None:
            return
        self.ui.lineEdit_number_group_comment.setText(
            str(getattr(bean, "wantCount", ""))
        )
        dtype = getattr(bean, "dtype", None)
        self.ui.checkBox_video_photo_comment.setChecked(
            dtype == DTopClassHelper.RESOURCE_TYPE_VIDEO_PHOTO
        )
        self.ui.checkBox_photo_comment.setChecked(
            dtype == DTopClassHelper.RESOURCE_TYPE_PHOTO
        )
        self.ui.checkBox_video_comment.setChecked(
            dtype == DTopClassHelper.RESOURCE_TYPE_VIDEO
        )
        self.ui.checkBox_file_comment.setChecked(
            dtype == DTopClassHelper.RESOURCE_TYPE_FILE
        )
        self.ui.checkBox_text_comment.setChecked(
            dtype == DTopClassHelper.RESOURCE_TYPE_TEXT
        )
        forWardAction = getattr(bean, "forWardAction", None)
        if forWardAction is not None:
            action = getattr(forWardAction, "action", None)
            self.ui.radioButton_action_auto_comment.setChecked(
                action == DTopClassHelper.ACTION_AUTO
            )
            self.ui.radioButton_action_download_comment.setChecked(
                action == DTopClassHelper.ACTION_DOWNLOAD
            )
            self.ui.checkBox_origin_source_text_comment.setChecked(
                bool(getattr(forWardAction, "keepSourceText", False))
            )
            self.ui.checkBox_dele_source_text_comment.setChecked(
                bool(getattr(forWardAction, "deleSourceText", False))
            )
            self.ui.checkBox_dele_link_comment.setChecked(
                bool(getattr(forWardAction, "deleLink", False))
            )
            self.ui.checkBox_fliter_button_comment.setChecked(
                bool(getattr(forWardAction, "filterButton", False))
            )
            self.ui.checkBox_discard_no_text_resource.setChecked(
                bool(getattr(forWardAction, "discardNoTextResource", False))
            )
        advanced = getattr(bean, "advancedFilterBean", None)
        if advanced is not None:
            self.ui.lineEdit_fliter_words_comment_contain.setText(
                CommonCode.filter_words_to_str(
                    getattr(advanced, "containWords", [])
                )
            )
            self.ui.lineEdit_fliter_words_comment_exclude.setText(
                CommonCode.filter_words_to_str(
                    getattr(advanced, "excludeWords", [])
                )
            )
            self.ui.checkBox_chai_zu.setChecked(
                bool(getattr(advanced, "chaiZu", False))
            )
        tail = getattr(bean, "tail", None)
        if tail is not None:
            self.ui.textEdit_tail_text_comment.setPlainText(
                str(getattr(tail, "tail_text", ""))
            )
        replace = getattr(bean, "replace", None)
        if replace is not None:
            self.ui.textEdit_replace_rule_comment.setPlainText(
                CommonCode.replaces_to_str(
                    getattr(replace, "replaces", [])
                )
            )
        water = getattr(bean, "water", None)
        if water is not None:
            self.ui.checkBox_pic_water_comment.setChecked(
                bool(getattr(water, "enPic", False))
            )
            self.ui.checkBox_video_water_comment.setChecked(
                bool(getattr(water, "enVideo", False))
            )
            self.ui.lineEdit_water_text_comment.setText(
                str(getattr(water, "text", ""))
            )
            index = CommonCode.parseVideoIndex(
                getattr(water, "duration", None)
            )
            self.ui.comboBox_video_minute_comment.setCurrentIndex(index)
            mode = getattr(water, "mode", None)
            self.ui.cb_banyun_com_water_mode.setCurrentText(str(mode or ""))
            self.picPath = str(getattr(water, "picPath", ""))
            self.picRatio = int(getattr(water, "picRatio", 30) or 30)
            self.set_elided_path(self.picPath)
            self.ui.line_edit_by_com_rule_water_pic_ratio.setText(
                str(self.picRatio)
            )
        selfAdWrapper = getattr(bean, "selfAdWrapper", None)
        if selfAdWrapper is not None:
            values = getattr(selfAdWrapper, "ades", []) or []
            self.adMap = {
                getattr(ad, "adId", index): ad
                for index, ad in enumerate(values)
            }
        resOp = getattr(bean, "yuLanResOp", None)
        if resOp is not None:
            self.ui.cb_by_com_config_pic_blur.setChecked(
                bool(getattr(resOp, "picBlur", False))
            )
            self.ui.cb_by_com_config_spoiler.setChecked(
                bool(getattr(resOp, "spoiler", False))
            )
            self.ui.by_com_config_pic_blur_radius.setText(
                str(getattr(resOp, "radius", 3))
            )
        aiEmployee = getattr(bean, "aiEmployee", None)
        if aiEmployee is not None:
            self.aiEmployee = aiEmployee
            self.ui.checkBox_banyun_com_ai_enable.setChecked(True)
            self.ui.label_banyun_com_ai_name.setText(
                "当前选择：" + str(getattr(aiEmployee, "name", "无"))
            )
        aiRefusedOpt = getattr(bean, "aiRefusedOpt", None)
        if aiRefusedOpt is not None:
            self.ui.radioButton_ai_banyun_com_skip_source.setChecked(
                bool(aiRefusedOpt.is_skip_group())
            )
            self.ui.radioButton_ai_banyun_com_use_source.setChecked(
                bool(aiRefusedOpt.is_keep_origin_source())
            )
        grid = getattr(bean, "grid", None)
        if grid is not None:
            self.ui.lineEdit_by_com_grid_number.setText(
                str(getattr(grid, "number", 6))
            )
            self.ui.cb_ban_yun_com_random_cover.setChecked(
                bool(getattr(grid, "randomCover", False))
            )
        self.ui.checkBox_ad_enable_comment.setChecked(
            bool(
                getattr(
                    selfAdWrapper,
                    "adEnable",
                    getattr(bean, "adEnable", True),
                )
            )
        )
        self._chai_zu_component_states()
        self.videoPhotoChanged()

    def onAdEnableChanged(self, state) -> None:
        enable = state == Qt.Checked
        self.ui.checkBox_banyun_com_ai_enable.setEnabled(enable)
        self.ui.horizontalGroupBox_ai_banyun_com.setEnabled(enable)

    def _chai_zu_component_states(self) -> None:
        enabled = self.ui.checkBox_chai_zu.isChecked()
        for widget in (
            getattr(self.ui, "lineEdit_fliter_words_comment_contain", None),
            getattr(self.ui, "lineEdit_fliter_words_comment_exclude", None),
            getattr(self.ui, "checkBox_discard_no_text_resource", None),
        ):
            if widget is not None:
                widget.setEnabled(enabled)

    def videoPhotoChanged(self) -> None:
        video_photo = self.ui.checkBox_video_photo_comment.isChecked()
        self.ui.checkBox_photo_comment.setEnabled(not video_photo)
        self.ui.checkBox_video_comment.setEnabled(not video_photo)

    def onKeepSourceChanged(self, state) -> None:
        enable = state != Qt.Checked
        self.ui.checkBox_dele_source_text_comment.setEnabled(enable)
        self.ui.checkBox_dele_link_comment.setEnabled(enable)

    def showEvent(self, a0: QShowEvent) -> None:
        screen = QApplication.primaryScreen()
        if screen is not None:
            geometry = screen.availableGeometry()
            screen_width = geometry.width()
            screen_height = geometry.height()
        else:
            screen_width = 1920
            screen_height = 1080
        window_width = self.width()
        window_height = self.height()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.resize(window_width, window_height)
        self.move(x_position, y_position)
        super().showEvent(a0)

    def btnSave(self) -> None:
        """Compatibility alias for the recovered save entry point.

        The live ``by_comment_rule_config.ui`` button is wired to
        ``saveCommentRule``.  The original standalone ``btnSave`` body is not
        independently recoverable from the stripped method table, so keep the
        name as a safe delegation rather than reusing ad-editor widgets that
        do not exist on this dialog.
        """

        self.saveCommentRule()

