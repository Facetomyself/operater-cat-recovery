# Recovered module: src.py.com.yun.mao.dialog.ImageDialogHelper
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

from .CourseImageDialog import CourseImageDialog
from ..util import ResourcePath


def unifyShowResTypeCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("resource_type_one_new.png")
    image2 = ResourcePath.get_drawable_path("resource_type_two_new.png")
    CourseImageDialog(parent, [image1, image2], "资源类型教程").exec()


def unifyShowJiuWeiMaoCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("bot001.png"),
        ResourcePath.get_drawable_path("bot002.png"),
        ResourcePath.get_drawable_path("bot003.png"),
        ResourcePath.get_drawable_path("bot004.png"),
        ResourcePath.get_drawable_path("bot005.png"),
        ResourcePath.get_drawable_path("bot006.png"),
        ResourcePath.get_drawable_path("bot007.png"),
        ResourcePath.get_drawable_path("bot008.png"),
    ]
    CourseImageDialog(parent, images, "文件存储分享机器人教程").exec()


def unifyShowWanZhenBanCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("blockquote_format_png_show.png")
    CourseImageDialog(parent, [image1], "完整版文案格式教程").exec()


def unifyShowDurationCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("yulan_res_duration_png_show_new.png")
    CourseImageDialog(parent, [image1], "添加时长教程").exec()


def unifyShowResOpCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("yulan_res_op_png_show.png")
    CourseImageDialog(parent, [image1], "预览频道资源操作教程").exec()


def unifyShowPublishResOpCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("yulan_res_op_png_show.png")
    CourseImageDialog(parent, [image1], "发布资源操作教程").exec()


def unifyShowYunPreViewBanYunTypeCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("yun_yulan_ban_yun_type_png_show.png")
    CourseImageDialog(parent, [image1], "云预览搬运方式教程").exec()


def unifyShowYulanFlowBanYunTypeCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("yulan_ban_yun_type_png_show.png")
    CourseImageDialog(parent, [image1], "预览流搬运方式教程").exec()


def unifyShowAutoFlowBanYunTypeCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("auto_ban_yun_type_png_show.png")
    CourseImageDialog(parent, [image1], "自动流搬运方式教程").exec()


def unifyShowYunAutoBanYunTypeCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("yun_auto_ban_yun_type_png_show.png")
    CourseImageDialog(parent, [image1], "云自动搬运方式教程").exec()


def unifyShowBqFontCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("com_no_bq_font.png"),
        ResourcePath.get_drawable_path("com_bq_font.png"),
    ]
    CourseImageDialog(parent, images, "会员，游客，时长，字体教程").exec()


def unifyShowBotBqFontCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("com_bot_no_bq_font.png"),
        ResourcePath.get_drawable_path("com_bot_bq_font.png"),
    ]
    CourseImageDialog(parent, images, "Bot链接，时长，字体教程").exec()


def unifyShowItemsCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("com_01_down_load.png"),
        ResourcePath.get_drawable_path("com_02_ban_yun.png"),
        ResourcePath.get_drawable_path("com_03_preview.png"),
        ResourcePath.get_drawable_path("com_04_auto.png"),
        ResourcePath.get_drawable_path("com_05_cloud_preview.png"),
        ResourcePath.get_drawable_path("com_06_cloud_auto.png"),
        ResourcePath.get_drawable_path("com_07_mode.png"),
    ]
    CourseImageDialog(parent, images, "不同条目详解教程").exec()


def unifyShowBanYunAndMonitorCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("com_banyun_monitor_show.png")
    CourseImageDialog(parent, [image1], "定时模式和监控模式 教程").exec()


def unifyShowTopicCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("0001-topic.png"),
        ResourcePath.get_drawable_path("0002-topic.png"),
        ResourcePath.get_drawable_path("0003-topic.png"),
        ResourcePath.get_drawable_path("0004-topic.png"),
        ResourcePath.get_drawable_path("0005-topic.png"),
        ResourcePath.get_drawable_path("0006-topic.png"),
    ]
    CourseImageDialog(parent, images, "话题获取和填写教程").exec()


def unifyShowAdCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("ad-001-ad.png"),
        ResourcePath.get_drawable_path("ad-002-ad.png"),
        ResourcePath.get_drawable_path("ad-003-ad.png"),
        ResourcePath.get_drawable_path("ad-004-ad.png"),
        ResourcePath.get_drawable_path("ad-005-ad.png"),
    ]
    CourseImageDialog(parent, images, "电报会员表情HTML教程").exec()


def unifyShowPremiumCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("p_com_items_jie_shi.png"),
        ResourcePath.get_drawable_path("p_card_type_jie_shi.png"),
        ResourcePath.get_drawable_path("p_ai_type_jie_shi.png"),
    ]
    CourseImageDialog(parent, images, "条目解释和购卡建议").exec()


def unifyShowPicWaterCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("pic_water_jc_001.png"),
        ResourcePath.get_drawable_path("pic_water_jc_002.png"),
        ResourcePath.get_drawable_path("pic_water_jc_003.png"),
        ResourcePath.get_drawable_path("pic_water_jc_004.png"),
        ResourcePath.get_drawable_path("san_texin.png"),
    ]
    CourseImageDialog(parent, images, "图片水印教程").exec()


def unifyShowInputApiKeyCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path(f"ai_course_{index:02d}.png")
        for index in range(1, 13)
    ]
    CourseImageDialog(parent, images, "配置AI员工API KEY").exec()


def unifyShowYouKeAiCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path(f"youke_ai_course_{index:02d}.png")
        for index in range(1, 7)
    ]
    CourseImageDialog(parent, images, "AI文案同义转换演示效果").exec()


def unifyShowQianYiCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("qianyi_001.png"),
        ResourcePath.get_drawable_path("qianyi_002.png"),
        ResourcePath.get_drawable_path("qianyi_003.png"),
    ]
    CourseImageDialog(parent, images, "迁移会员权限-连带迁移条目数据").exec()


def unifyShowAIRefuseCourse(parent) -> None:
    image1 = ResourcePath.get_drawable_path("ai_refuse_jiao_chen_001.png")
    CourseImageDialog(parent, [image1], "AI拒绝识别词-教程").exec()


def unifyShowRandomCoverCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("san_texin.png"),
        ResourcePath.get_drawable_path("cover_jiao_chen_01.png"),
        ResourcePath.get_drawable_path("cover_jiao_chen_02.png"),
    ]
    CourseImageDialog(parent, images, "随机视频封面-教程").exec()


def unifyShowGridCourse(parent) -> None:
    images = [
        ResourcePath.get_drawable_path("san_texin.png"),
        ResourcePath.get_drawable_path("grid_01.png"),
        ResourcePath.get_drawable_path("grid_02.png"),
        ResourcePath.get_drawable_path("grid_03.png"),
        ResourcePath.get_drawable_path("grid_04.png"),
        ResourcePath.get_drawable_path("grid_05.png"),
    ]
    CourseImageDialog(parent, images, "消息组宫格教程-教程").exec()
