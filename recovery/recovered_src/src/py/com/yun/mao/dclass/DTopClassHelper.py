# Recovered module: src.py.com.yun.mao.dclass.DTopClassHelper
from __future__ import annotations

import dataclasses
import os
import tempfile
from typing import Any

from .DTopClass import (
    Ad,
    AdWrapper,
    AddDurationInfo,
    AdvancedFilterBean,
    AiEmployee,
    AiRefusedOption,
    AutoBean,
    AutoFlowBean,
    BaseFilterBean,
    BanYunBean,
    BotBean,
    CommentBean,
    CommentRuleBean,
    CompleteVersionOp,
    DownLoadBean,
    DurationMode,
    DurationFilterBean,
    ForwardActionBean,
    GridOpt,
    HuiYuanLink,
    Increase,
    Loop,
    ModelWrapper,
    PresentMode,
    Random,
    Replace,
    SizeFilterBean,
    Tail,
    Water,
    YouKeLink,
    YuLanBean,
    YuLanModeBean,
    YuLanResOp,
    YunAutoBean,
    YunPreViewBean,
)
from ..config import NewConfig, YunYinMaoConfig
from ..util.need.AllBeanDef import AiEmployeeBean


RESOURCE_TYPE_PHOTO = "photo"
RESOURCE_TYPE_VIDEO_PHOTO = "video_photo"
RESOURCE_TYPE_VIDEO = "video"
RESOURCE_TYPE_FILE = "file"
RESOURCE_TYPE_TEXT = "text"
ACTION_AUTO = "auto"
ACTION_DOWNLOAD = "download"

MESSAGE_NUMBER_DAN_WEI_GROUP = "group"
MESSAGE_NUMBER_DAN_WEI_SINGLE = "single"
MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT = "按组计算"
MESSAGE_NUMBER_DAN_WEI_SINGLE_TEXT = "按个计算"

MODEl_RANDOM = "random"
MODEl_INCREASE = "increase"
MODEl_LOOP = "loop"
TEXT_RANDOM_MODEL = "随机模式"
TEXT_INCREASE_MODEL = "顺序模式"
TEXT_LOOP_MODEL = "循环模式"

WATER_MODE_TEXT = "文字水印"
WATER_MODE_PIC = "图片水印"


def _value(obj: Any, name: str, default: Any = None) -> Any:
    if obj is None:
        return default
    value = getattr(obj, name, default)
    return value() if callable(value) else value


def _bool_text(value: Any) -> str:
    return "是" if value else "否"


def boolToStr(value: Any) -> str:
    return _bool_text(value)


def _filter(cls, dic):
    fields = {field.name for field in dataclasses.fields(cls)}
    return {key: value for key, value in (dic or {}).items() if key in fields}


def dic_to_Ad_obj(dic: dict):
    return Ad(**_filter(Ad, dic))


def dic_to_AdWrapper_obj(dic: dict):
    data = _filter(AdWrapper, dic)
    data["ades"] = [dic_to_Ad_obj(item) for item in (dic or {}).get("ades", [])]
    return AdWrapper(**data)


def dic_to_Water_obj(dic: dict):
    return Water(**_filter(Water, dic))


def dic_to_Employee_obj(dic: dict):
    return AiEmployeeBean(**_filter(AiEmployeeBean, dic))


def dic_to_DurationFilterBean(dic: dict):
    return DurationFilterBean(**_filter(DurationFilterBean, dic))


def dic_to_SizeFilterBean(dic: dict):
    return SizeFilterBean(**_filter(SizeFilterBean, dic))


def dic_to_BaseFilterBean(dic: dict):
    data = _filter(BaseFilterBean, dic)
    if isinstance(data.get("durationFilterBean"), dict):
        data["durationFilterBean"] = dic_to_DurationFilterBean(
            data["durationFilterBean"]
        )
    if isinstance(data.get("sizeFilterBean"), dict):
        data["sizeFilterBean"] = dic_to_SizeFilterBean(
            data["sizeFilterBean"]
        )
    return BaseFilterBean(**data)


def dic_to_AdvancedFilterBean(dic: dict):
    return AdvancedFilterBean(**_filter(AdvancedFilterBean, dic))


def _auto_source(dic: dict) -> dict:
    """Use the wire ``beanLike`` payload when the wrapper carries one."""

    bean_like = (dic or {}).get("beanLike")
    if not isinstance(bean_like, dict):
        return dict(dic or {})
    merged = dict(bean_like)
    for key in ("kid", "auto_type", "priority", "active"):
        if key in dic:
            merged.setdefault(key, dic[key])
    return merged


def _convert_auto_nested(data: dict) -> None:
    converters = (
        ("selfAdWrapper", dic_to_AdWrapper_obj),
        ("advancedFilterBean", dic_to_AdvancedFilterBean),
        ("baseFilter", dic_to_BaseFilterBean),
        ("water", dic_to_Water_obj),
        ("tail", dic_to_Tail_obj),
        ("replace", dic_to_Replace_obj),
        ("modelWrapper", dic_to_ModelWrapper_obj),
        ("forWardAction", dic_to_forWardAction),
        ("yuLanResOp", dic_to_yuLanResOp),
        ("aiEmployee", dic_to_aiEmployee),
        ("aiRefusedOpt", dic_to_aiRefusedOpt),
        ("grid", dic_to_GridOpt),
        ("commentRule", dic_to_CommentRuleBean_obj),
        ("huiYuanLink", dic_to_HuiYuanLink_obj),
        ("youKeLink", dic_to_YouKeLink_obj),
        ("yuLanModeBean", dic_to_yuLanModeBean_obj),
        ("durationInfo", dic_to_addDurationInfo_obj),
        ("completeVersionOp", dic_to_completeVersionOp),
        ("botBean", dic_to_botBean),
    )
    for key, converter in converters:
        if isinstance(data.get(key), dict):
            data[key] = converter(data[key])


def _build_auto_bean(
    cls,
    dic: dict,
    auto_type: int,
    priority: int,
    kid: str,
    active: bool,
):
    data = _filter(cls, dic)
    data["kid"] = str(kid or "")
    data["auto_type"] = int(auto_type or 0)
    data["priority"] = int(priority or 100)
    data["active"] = bool(active)
    _convert_auto_nested(data)
    return cls(**data)


def parse_ban_yun_flow(
    dic: dict,
    auto_type: int = 1,
    priority: int = 100,
    kid: str = "",
    active: bool = True,
) -> BanYunBean:
    return _build_auto_bean(BanYunBean, dic, auto_type, priority, kid, active)


def parse_auto_flow_or_yulan_flow(
    dic: dict,
    auto_type: int = 2,
    priority: int = 100,
    kid: str = "",
    active: bool = True,
):
    cls = YuLanBean if auto_type == 3 else AutoFlowBean
    return _build_auto_bean(cls, dic, auto_type, priority, kid, active)


def parse_down_load(
    dic: dict,
    auto_type: int = 4,
    priority: int = 100,
    kid: str = "",
    active: bool = True,
) -> DownLoadBean:
    return _build_auto_bean(DownLoadBean, dic, auto_type, priority, kid, active)


def parse_yun_auto(
    dic: dict,
    auto_type: int = 5,
    priority: int = 100,
    kid: str = "",
    active: bool = True,
) -> YunAutoBean:
    return _build_auto_bean(YunAutoBean, dic, auto_type, priority, kid, active)


def parse_yun_preview(
    dic: dict,
    auto_type: int = 6,
    priority: int = 100,
    kid: str = "",
    active: bool = True,
) -> YunPreViewBean:
    return _build_auto_bean(YunPreViewBean, dic, auto_type, priority, kid, active)


def dic_to_Auto_obj(dic: dict) -> AutoBean:
    source = _auto_source(dic)
    auto_type = int(source.get("auto_type", 0) or 0)
    priority = int(source.get("priority", 100) or 100)
    kid = str(source.get("kid", "") or "")
    active = bool(source.get("active", True))
    parser = {
        1: parse_ban_yun_flow,
        2: parse_auto_flow_or_yulan_flow,
        3: parse_auto_flow_or_yulan_flow,
        4: parse_down_load,
        5: parse_yun_auto,
        6: parse_yun_preview,
    }.get(auto_type, parse_ban_yun_flow)
    return parser(source, auto_type, priority, kid, active)


def dic_to_PresentMode_obj(dic: dict):
    return PresentMode(**_filter(PresentMode, dic))


def dic_to_DurationMode_obj(dic: dict):
    return DurationMode(**_filter(DurationMode, dic))


def dic_to_ModelWrapper_obj(dic: dict):
    return dic_to_modelWrapper(dic)


def dic_to_modelWrapper(dic: dict):
    data = _filter(ModelWrapper, dic)
    wrapper = ModelWrapper(**data)
    for key in ("startId", "endId", "wantCount", "numberMode"):
        if key in dic:
            setattr(wrapper, key, dic[key])
    return wrapper


def __has_dest_type(dest, dtype) -> bool:
    if dest is None:
        return False
    if isinstance(dest, str):
        values = dest.split(",")
    else:
        try:
            values = list(dest)
        except TypeError:
            values = [dest]
    return str(dtype) in [str(value).strip() for value in values]


def has_photo_type(dest) -> bool:
    return __has_dest_type(dest, RESOURCE_TYPE_PHOTO)


def has_video_photo_type(dest) -> bool:
    return __has_dest_type(dest, RESOURCE_TYPE_VIDEO_PHOTO)


def has_video_type(dest) -> bool:
    return __has_dest_type(dest, RESOURCE_TYPE_VIDEO)


def has_file_type(dest) -> bool:
    return __has_dest_type(dest, RESOURCE_TYPE_FILE)


def has_text_type(dest) -> bool:
    return __has_dest_type(dest, RESOURCE_TYPE_TEXT)


def has_signal_video_and_signal_photo_type(dest) -> bool:
    return has_video_type(dest) and has_photo_type(dest)


def get_action_text(action) -> str:
    if action == ACTION_AUTO:
        return "自动方式"
    return "强制下载方式"


def is_action_auto(action) -> bool:
    return action == ACTION_AUTO


def get_duration_text(duration) -> str:
    if duration:
        return "大于" + str(duration) + "分钟的视频"
    return ""


def get_number_model_text(number_mode) -> str:
    if number_mode == MESSAGE_NUMBER_DAN_WEI_GROUP:
        return MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT
    if number_mode == MESSAGE_NUMBER_DAN_WEI_SINGLE:
        return MESSAGE_NUMBER_DAN_WEI_SINGLE_TEXT
    return ""


def get_model_text(model) -> str:
    if model == MODEl_RANDOM:
        return TEXT_RANDOM_MODEL
    if model == MODEl_INCREASE:
        return TEXT_INCREASE_MODEL
    if model == MODEl_LOOP:
        return TEXT_LOOP_MODEL
    return ""


def get_present_text(presentMode) -> str:
    present = _value(presentMode, "present", presentMode)
    if present == NewConfig.FLOW_DURATION_SHORT:
        return "预览视频占比：10%"
    if present == NewConfig.FLOW_DURATION_MIDDLE:
        return "预览视频占比：20%"
    if present == NewConfig.FLOW_DURATION_LONG:
        return "预览视频占比：30%"
    if present:
        return "预览视频占比：" + str(present) + "%"
    return ""


def get_yulan_mode_text(yuLanModeBean) -> str:
    if yuLanModeBean is None:
        return ""
    res_type = _value(yuLanModeBean, "resType", "")
    prefix = ""
    if res_type == NewConfig.YU_LAN_RES_TYPE_PIC:
        prefix = " 图片资源 "
    elif res_type == NewConfig.YU_LAN_RES_TYPE_VIDEO:
        prefix = " 视频资源 "
    mode = _value(yuLanModeBean, "mode", "")
    if mode == NewConfig.FLOW_YU_LAN_MODEL_PRESENT:
        return (
            prefix
            + NewConfig.FLOW_YU_LAN_MODEL_PRESENT_TEXT
            + "， "
            + get_present_text(_value(yuLanModeBean, "presentMode", None))
        )
    if mode == NewConfig.FLOW_YU_LAN_MODEL_DURATION:
        duration_mode = _value(yuLanModeBean, "durationMode", None)
        return (
            prefix
            + NewConfig.FLOW_YU_LAN_MODEL_DURATION_TEXT
            + "， 预览视频时长介于 "
            + str(_value(duration_mode, "duration_min_second", 0))
            + " 到 "
            + str(_value(duration_mode, "duration_max_second", 0))
            + " 秒钟的随机值！"
        )
    return prefix


def gen_yulan_des(auto) -> str:
    return destes_to_str(_value(auto, "getYulanDestes", []))


def get_resource_text(dtype) -> str:
    if isinstance(dtype, str):
        values = [item.strip() for item in dtype.split(",") if item.strip()]
    else:
        values = list(dtype or [])
    text = []
    if RESOURCE_TYPE_VIDEO_PHOTO in values:
        text.append("仅包含视频的消息组")
    if RESOURCE_TYPE_PHOTO in values:
        text.append("图片")
    if RESOURCE_TYPE_VIDEO in values:
        text.append("视频")
    if RESOURCE_TYPE_FILE in values:
        text.append("文件")
    if RESOURCE_TYPE_TEXT in values:
        text.append("文本")
    return ",".join(text)


def gen_default_base_filter_bean() -> BaseFilterBean:
    return BaseFilterBean(
        durationFilterBean=DurationFilterBean(
            duration_min=YunYinMaoConfig.BASE_FILTER_DU_MIN,
            duration_max=YunYinMaoConfig.BASE_FILTER_DU_MAX,
        ),
        sizeFilterBean=SizeFilterBean(
            min=YunYinMaoConfig.BASE_FILTER_SIZE_MIN,
            max=YunYinMaoConfig.BASE_FILTER_SIZE_MAX,
        ),
    )


def gen_base_filter_desc(base) -> str:
    if base is None:
        return ""
    duration = _value(base, "durationFilterBean", None)
    size = _value(base, "sizeFilterBean", None)
    if duration is None or size is None:
        return ""
    return (
        "时长范围："
        + str(_value(duration, "min", 0))
        + " ~ "
        + str(_value(duration, "max", 0))
        + " 分钟；大小范围："
        + str(_value(size, "min", 0))
        + " ~ "
        + str(_value(size, "max", 0))
        + " MB"
    )


def get_ad_desc_text(adWrapper) -> str:
    if not _value(adWrapper, "adEnable", False):
        return "是否开启：否"
    if _value(adWrapper, "adIsBottomUp", False):
        text = "是否开启：是，是否置底：是,"
    else:
        text = "是否开启：是，是否置底：否,"
    return text + "是否删除历史广告：" + _bool_text(
        _value(adWrapper, "delete", False)
    )


def comment_ai_info(aiEmployee) -> str:
    if not aiEmployee or not _value(aiEmployee, "enable", False):
        return "AI文案：未开启"
    uid = _value(aiEmployee, "uid", 0)
    if not uid:
        return "AI文案：未开启"
    try:
        from . import LoadEmployeeClass

        name = LoadEmployeeClass.getAiEmployeeName(uid)
    except Exception:
        name = uid
    return "AI文案：开启，AI员工：" + str(name)


def ai_info(aiEmployee) -> str:
    return comment_ai_info(aiEmployee)


def replies_info(commentRule) -> str:
    if not commentRule or not _value(commentRule, "copyComment", False):
        return "没有开启评论区复刻"
    return (
        "是否开启评论区复刻："
        + _bool_text(True)
        + ", 期望复刻数量："
        + str(_value(commentRule, "wantCount", 0))
    )


def is_keep_source_text(bean) -> str:
    return _bool_text(
        _value(_value(bean, "advancedFilterBean", None), "keepSourceText", False)
    )


def is_delete_source_text(bean) -> str:
    return _bool_text(
        _value(_value(bean, "advancedFilterBean", None), "deleSourceText", False)
    )


def is_delete_link(bean) -> str:
    return _bool_text(
        _value(_value(bean, "advancedFilterBean", None), "deleLink", False)
    )


def is_use_contain_words(bean) -> str:
    values = _value(_value(bean, "advancedFilterBean", None), "containWords", [])
    return _bool_text(bool(values))


def is_filter_button(bean) -> str:
    return _bool_text(
        _value(_value(bean, "advancedFilterBean", None), "filterButton", False)
    )


def is_config_tail(bean) -> str:
    return _bool_text(bool(_value(_value(bean, "tail", None), "tail_text", "")))


def filter_words_to_str(words) -> str:
    values = words if isinstance(words, (list, tuple, set)) else [words]
    return "|".join(
        str(item).strip() for item in values if str(item or "").strip()
    )


def str_to_filter_words(text) -> list:
    if not text:
        return []
    return [
        item.strip()
        for item in str(text).split("|")
        if item.strip()
    ]


def destes_to_str(destes) -> str:
    values = destes if isinstance(destes, (list, tuple, set)) else [destes]
    return "\n".join(
        str(item).strip() for item in values if str(item or "").strip()
    )


def str_to_destes(text) -> list:
    if not text:
        return []
    return [
        item.strip()
        for item in str(text).split("\n")
        if item.strip()
    ]


def replaces_to_str(replaces) -> str:
    if hasattr(replaces, "replaces"):
        replaces = replaces.replaces
    values = replaces if isinstance(replaces, (list, tuple)) else [replaces]
    separator = getattr(NewConfig, "MAO_REPLACE_FU_HAO", "->")
    lines = []
    for item in values:
        if isinstance(item, (tuple, list)) and len(item) >= 2:
            text = f"{item[0]}{separator}{item[1]}"
        else:
            text = str(item)
        text = text.strip()
        if text:
            lines.append(text)
    return "\n".join(lines)


def str_to_replaces(text) -> list:
    if not text:
        return []
    separator = getattr(NewConfig, "MAO_REPLACE_FU_HAO", "->")
    result = []
    for line in str(text).split("\n"):
        line = line.strip()
        if not line:
            continue
        if separator in line:
            source, target = line.split(separator, 1)
            result.append(
                f"{source.strip()}{separator}{target.strip()}"
            )
        else:
            result.append(line)
    return result


def ad_file_to_str(files) -> str:
    text = ""
    for item in str(files or "").split("\n"):
        path = item.strip()
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as handle:
                text += handle.read()
    return text


def ad_str_to_file(text) -> str:
    """Write ad HTML to a temporary UTF-8 file and return its path."""

    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".html",
        delete=False,
    )
    try:
        handle.write(str(text or ""))
        return handle.name
    finally:
        handle.close()


def gen_huiyuan_link_text(huiYuanLink) -> str:
    if not huiYuanLink or not _value(huiYuanLink, "enable", False):
        return "未开启"
    text = "文案：" + str(_value(huiYuanLink, "text", ""))
    if _value(huiYuanLink, "enableCustomerLink", False):
        text += " 超级链接：" + str(
            _value(huiYuanLink, "customerHttpLink", "")
        )
    else:
        text += " 超级链接：会员群的资源链接"
    return text


def gen_youke_link_text(youKeLink) -> str:
    if not youKeLink or not _value(youKeLink, "enable", False):
        return "未开启"
    return (
        "文案："
        + str(_value(youKeLink, "text", ""))
        + " 超级链接："
        + str(_value(youKeLink, "httpLink", ""))
    )


def gen_op_text(yulanOp, cvOp, text) -> str:
    parts = []
    if _value(yulanOp, "picBlur", False):
        parts.append("开启了图片模糊")
    if _value(yulanOp, "spoiler", False):
        parts.append(" 开启了资源防止剧透")
    if _value(cvOp, "blockquote", False):
        parts.append(" 开启了块引用文本格式")
    link_text = _value(cvOp, "linkText", "")
    if link_text:
        parts.append(" 完整版链接文案【" + str(link_text) + "】")
    return "".join(parts)


def water_config_desc(water, pic, video, tip) -> str:
    if not water:
        return " 没开启水印，"
    parts = []
    if pic:
        parts.append("图片水印：开启，")
    else:
        parts.append("图片水印：关闭，")
    if video:
        parts.append("视频水印：开启，")
        duration = _value(water, "duration", 0)
        if duration:
            parts.append(str(duration) + "分钟内视频有效，")
    else:
        parts.append("视频水印：关闭，")
    mode = _value(water, "mode", "")
    if mode == WATER_MODE_TEXT:
        parts.append("水印文本：" + str(_value(water, "text", "")) + "，")
    elif mode == WATER_MODE_PIC:
        parts.append("图片水印，大小是 ")
        parts.append(str(_value(water, "picRatio", 0)))
        parts.append("%，图片水印资源是：")
        parts.append(os.path.basename(str(_value(water, "picPath", ""))))
        parts.append("，")
    return "".join(parts)


def auto_desc(beanLike) -> str:
    lines = []
    lines.append("名称：" + str(_value(beanLike, "getName", "")))
    lines.append("来源：" + str(_value(beanLike, "getSource", "")))
    lines.append("目标：" + destes_to_str(_value(beanLike, "getDestes", [])))
    dtype = _value(beanLike, "dtype", "")
    lines.append("资源类型：" + get_resource_text(dtype))
    model = _value(beanLike, "model", "")
    lines.append("模式选择：" + get_model_text(model))
    action = _value(_value(beanLike, "forWardAction", None), "action", "")
    lines.append("搬运方式：" + get_action_text(action))
    lines.append("评论区：" + replies_info(_value(beanLike, "commentRule", None)))
    lines.append(
        "评论区详情："
        + str(_value(beanLike, "replies_info_detail", ""))
    )
    lines.append("基础条件：" + gen_base_filter_desc(_value(beanLike, "baseFilter", None)))
    advanced = _value(beanLike, "advancedFilterBean", None)
    lines.append("是否保留原格式：" + is_keep_source_text(beanLike))
    lines.append("是否删除源文本：" + is_delete_source_text(beanLike))
    lines.append("是否删除外链：" + is_delete_link(beanLike))
    lines.append("是否使用了包含词：" + is_use_contain_words(beanLike))
    lines.append("是否丢弃带按钮资源：" + is_filter_button(beanLike))
    lines.append("是否有尾巴：" + is_config_tail(beanLike))
    lines.append(comment_ai_info(_value(beanLike, "aiEmployee", None)))
    water = _value(beanLike, "water", None)
    pic = bool(_value(water, "enPic", False))
    video = bool(_value(water, "enVideo", False))
    lines.append(water_config_desc(water, pic, video, ""))
    lines.append(
        "广告：" + get_ad_desc_text(_value(beanLike, "selfAdWrapper", None))
    )
    if _value(beanLike, "isYunAutoType", False) or _value(
        beanLike, "isYunPreViewType", False
    ):
        lines.append("私有仓库：" + str(_value(beanLike, "getDbChannel", "")))
        lines.append("预览目标：" + gen_yulan_des(beanLike))
    lines.append(
        "会员链接："
        + gen_huiyuan_link_text(_value(beanLike, "huiYuanLink", None))
    )
    lines.append(
        "游客链接："
        + gen_youke_link_text(_value(beanLike, "youKeLink", None))
    )
    if advanced is not None:
        words = _value(advanced, "containWords", [])
        if words:
            lines.append("包含词为：" + filter_words_to_str(words))
        else:
            lines.append("无包含词")
        exclude = _value(advanced, "excludeWords", [])
        if exclude:
            lines.append("排除词为：" + filter_words_to_str(exclude))
        else:
            lines.append("无排除词")
    return "\n".join(lines)


def genBeanFormatText(beanLike) -> str:
    lines = []
    if _value(beanLike, "is_ramdom_mode", False):
        lines.append(
            "随机模式，随机参数->期望数量："
            + str(_value(beanLike, "ramdom_want_count", 0))
            + " 计数方式: "
            + get_number_model_text(_value(beanLike, "ramdom_numberMode", ""))
        )
    elif _value(beanLike, "is_increase_mode", False):
        lines.append(
            "顺序模式，顺序参数->开始ID："
            + str(_value(beanLike, "increase_startId", 0))
            + " 期望数量："
            + str(_value(beanLike, "increase_want_count", 0))
            + " 计数方式: "
            + get_number_model_text(_value(beanLike, "increase_numberMode", ""))
        )
    elif _value(beanLike, "is_loop_mode", False):
        lines.append(
            "循环模式，循环参数->开始ID："
            + str(_value(beanLike, "loop_mode_startId", 0))
            + " 结束ID："
            + str(_value(beanLike, "loop_mode_endId", 0))
        )
    lines.append(auto_desc(beanLike))
    return "\n".join(lines)


def dic_to_Random_obj(dic: dict):
    return Random(**_filter(Random, dic))


def dic_to_Loop_obj(dic: dict):
    return Loop(**_filter(Loop, dic))


def dic_to_Increase_obj(dic: dict):
    return Increase(**_filter(Increase, dic))


def dic_to_forWardAction(dic: dict):
    data = _filter(ForwardActionBean, dic)
    data.setdefault("randon_sleep_min", 3)
    data.setdefault("randon_sleep_max", 5)
    return ForwardActionBean(**data)


def dic_to_baseFilter(dic: dict):
    return dic_to_BaseFilterBean(dic)


def dic_to_advancedFilterBean(dic: dict):
    return dic_to_AdvancedFilterBean(dic)


def dic_to_Tail_obj(dic: dict):
    return Tail(**_filter(Tail, dic))


def dic_to_Replace_obj(dic: dict):
    return Replace(**_filter(Replace, dic))


def dic_to_Comment_obj(dic: dict):
    return CommentBean(**_filter(CommentBean, dic))


def dic_to_CommentRuleBean_obj(dic: dict):
    data = _filter(CommentRuleBean, dic)
    data["wantCount"] = data.get("wantCount", 0) or 0
    converters = (
        ("forWardAction", dic_to_forWardAction),
        ("baseFilter", dic_to_BaseFilterBean),
        ("advancedFilterBean", dic_to_AdvancedFilterBean),
        ("tail", dic_to_Tail_obj),
        ("replace", dic_to_Replace_obj),
        ("water", dic_to_Water_obj),
        ("selfAdWrapper", dic_to_AdWrapper_obj),
        ("yuLanResOp", dic_to_yuLanResOp),
        ("aiEmployee", dic_to_Employee_obj),
        ("aiRefusedOpt", dic_to_aiRefusedOpt),
        ("grid", dic_to_GridOpt),
    )
    for key, converter in converters:
        if isinstance(data.get(key), dict):
            data[key] = converter(data[key])
    return CommentRuleBean(**data)


def dic_to_yuLanResOp(dic: dict):
    return YuLanResOp(**_filter(YuLanResOp, dic))


def dic_to_aiEmployee(dic: dict):
    return AiEmployee(**_filter(AiEmployee, dic))


def dic_to_aiRefusedOpt(dic: dict):
    return AiRefusedOption(**_filter(AiRefusedOption, dic))


def dic_to_GridOpt(dic: dict):
    data = _filter(GridOpt, dic)
    data.setdefault("number", 6)
    return GridOpt(**data)


def dic_to_botBean(dic: dict):
    return BotBean(**_filter(BotBean, dic))


def dic_to_completeVersionOp(dic: dict):
    return CompleteVersionOp(**_filter(CompleteVersionOp, dic))


def dic_to_addDurationInfo_obj(dic: dict):
    return AddDurationInfo(**_filter(AddDurationInfo, dic))


def dic_to_yuLanModeBean_obj(dic: dict):
    data = _filter(YuLanModeBean, dic)
    if isinstance(data.get("presentMode"), dict):
        data["presentMode"] = dic_to_PresentMode_obj(data["presentMode"])
    if isinstance(data.get("durationMode"), dict):
        data["durationMode"] = dic_to_DurationMode_obj(data["durationMode"])
    return YuLanModeBean(**data)


def dic_to_HuiYuanLink_obj(dic: dict):
    return HuiYuanLink(**_filter(HuiYuanLink, dic))


def dic_to_YouKeLink_obj(dic: dict):
    return YouKeLink(**_filter(YouKeLink, dic))
