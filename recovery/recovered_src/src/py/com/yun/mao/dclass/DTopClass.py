# Recovered module: src.py.com.yun.mao.dclass.DTopClass
# Data classes for the bot's flow/auto/water/ad configuration.  Field names
# and type constants come from the Nuitka constants chunk; behavior is a
# readable reconstruction of the serialized model.
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Union


AUTO_BEAN_TYPE_OLD = 0
AUTO_BEAN_TYPE_BAN_YUN = 1
AUTO_BEAN_TYPE_AUTO_FLOW = 2
AUTO_BEAN_TYPE_YU_LAN_FLOW = 3
AUTO_BEAN_TYPE_DOWN_LOAD_FLOW = 4
AUTO_BEAN_TYPE_YUN_AUTO = 5
AUTO_BEAN_TYPE_YUN_PRE_VIEW = 6


def _text(value: Any) -> str:
    return "" if value is None else str(value)


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    return list(value) if not isinstance(value, str) else [value]


def _parse_source_parts(source: str):
    raw = _text(source).strip()
    if raw.startswith("https://t.me/c/"):
        parts = raw[len("https://t.me/c/") :].split("/")
        channel = parts[0] if parts else ""
        topic = parts[1] if len(parts) > 1 else ""
        return channel, topic
    return raw, ""


def convertDest(dest: str) -> str:
    from ..util.need import utils

    channel_part, _ = utils.parse_source_parts(dest)
    return utils.convertPrivateIdIfNeed(channel_part or "")


def convertDestTopic(dest: str) -> Union[int, str]:
    from ..util.need import utils

    _, topic_part = utils.parse_source_parts(dest)
    if not topic_part:
        return ""
    try:
        return int(topic_part)
    except (TypeError, ValueError):
        return topic_part


@dataclass
class AiRefusedOption:
    action: str = "skip"

    def is_skip_group(self) -> bool:
        return self.action == "skip"

    def is_keep_origin_source(self) -> bool:
        return self.action in ("keep", "origin")

    @classmethod
    def default_instance(cls) -> "AiRefusedOption":
        return cls()


@dataclass
class AddDurationInfo:
    addDurationInfo: bool = False
    blockquote: bool = False


@dataclass
class Increase:
    startId: int = 0
    wantCount: int = 0
    numberMode: str = ""


@dataclass
class Loop:
    startId: int = 0
    endId: int = 0


@dataclass
class Random:
    wantCount: int = 0
    numberMode: str = ""


@dataclass
class Tail:
    tail_text: str = ""


@dataclass
class Replace:
    replaces: list = field(default_factory=list)


@dataclass
class Ad:
    adId: str = ""
    files: list = field(default_factory=list)
    text: str = ""
    name: str = ""


@dataclass
class AdWrapper:
    adEnable: bool = False
    adIsBottomUp: bool = False
    delete: bool = False
    ades: list = field(default_factory=list)


@dataclass
class BotBean:
    user_name: str = ""


@dataclass
class CompleteVersionOp:
    blockquote: bool = False
    linkText: str = ""


@dataclass
class YuLanResOp:
    picBlur: bool = False
    spoiler: bool = False
    radius: int = 0


@dataclass
class AiEmployee:
    enable: bool = False
    uid: int = 0


@dataclass
class GridOpt:
    number: int = 0


@dataclass
class Water:
    enPic: bool = False
    enVideo: bool = False
    text: str = ""
    picPath: str = ""
    mode: str = ""
    duration: int = 0
    picRatio: int = 0


@dataclass
class CommentBean:
    copyComment: bool = False


@dataclass
class DurationFilterBean:
    duration_min: int = 0
    duration_max: int = 0
    duration_min_second: int = 0
    duration_max_second: int = 0

    def __post_init__(self) -> None:
        if not self.duration_min_second:
            self.duration_min_second = int(self.duration_min or 0) * 60
        if not self.duration_max_second:
            self.duration_max_second = int(self.duration_max or 0) * 60

    @property
    def min(self) -> int:
        return self.duration_min_second

    @property
    def max(self) -> int:
        return self.duration_max_second


@dataclass
class SizeFilterBean:
    min: int = 0
    max: int = 0


@dataclass
class BaseFilterBean:
    durationFilterBean: Optional[DurationFilterBean] = None
    sizeFilterBean: Optional[SizeFilterBean] = None


@dataclass
class ForwardActionBean:
    action: str = ""
    randon_sleep_min: int = 0
    randon_sleep_max: int = 0


@dataclass
class AdvancedFilterBean:
    keepSourceText: bool = True
    deleSourceText: bool = False
    deleLink: bool = False
    filterButton: bool = False
    discardNoTextResource: bool = False
    chaiZu: bool = False
    containWords: list = field(default_factory=list)
    excludeWords: list = field(default_factory=list)


@dataclass
class ModelWrapper:
    model: str = ""
    random: bool = False
    increase: bool = False
    loop: bool = False


@dataclass
class CommentRuleBean:
    copyComment: bool = False
    wantCount: int = 0
    dtype: str = ""
    forWardAction: Optional[ForwardActionBean] = None
    baseFilter: Optional[BaseFilterBean] = None
    advancedFilterBean: Optional[AdvancedFilterBean] = None
    tail: Optional[Tail] = None
    replace: Optional[Replace] = None
    water: Optional[Water] = None
    selfAdWrapper: Optional[AdWrapper] = None
    yuLanResOp: Optional[YuLanResOp] = None
    aiEmployee: Optional[AiEmployee] = None
    aiRefusedOpt: Optional[AiRefusedOption] = None
    grid: Optional[GridOpt] = None
    randomCover: bool = False


@dataclass
class HuiYuanLink:
    enable: bool = False
    text: str = ""
    enableCustomerLink: bool = False
    customerHttpLink: str = ""
    blockquote: bool = False


@dataclass
class YouKeLink:
    enable: bool = False
    text: str = ""
    httpLink: str = ""
    blockquote: bool = False


@dataclass
class PresentMode:
    present: str = ""


@dataclass
class DurationMode:
    resType: str = ""
    mode: str = ""
    presentMode: str = ""
    durationMode: str = ""


@dataclass
class YuLanModeBean:
    resType: str = ""
    mode: str = ""
    presentMode: str = ""
    durationMode: str = ""


@dataclass
class SuperFlowBean:
    name: str = ""
    source: str = ""
    destes: list = field(default_factory=list)
    yulan_destes: list = field(default_factory=list)
    dtype: str = ""
    modelWrapper: Optional[ModelWrapper] = None
    selfAdWrapper: Optional[AdWrapper] = None
    advancedFilterBean: Optional[AdvancedFilterBean] = None
    tail: Optional[Tail] = None
    replace: Optional[Replace] = None
    water: Optional[Water] = None
    huiYuanLink: Optional[HuiYuanLink] = None
    youKeLink: Optional[YouKeLink] = None
    yuLanModeBean: Optional[YuLanModeBean] = None
    baseFilter: Optional[BaseFilterBean] = None
    durationInfo: Optional[AddDurationInfo] = None
    forWardAction: Optional[ForwardActionBean] = None
    yuLanResOp: Optional[YuLanResOp] = None
    aiEmployee: Optional[AiEmployee] = None
    aiRefusedOpt: Optional[AiRefusedOption] = None
    grid: Optional[GridOpt] = None
    randomCover: bool = False

    def convertSource(self) -> str:
        return _text(self.source)

    def convertSourceTopicId(self) -> Union[int, str]:
        return _text(self.source)

    def is_ramdom_mode(self) -> bool:
        return bool(self.modelWrapper and self.modelWrapper.random)

    def is_increase_mode(self) -> bool:
        return bool(self.modelWrapper and self.modelWrapper.increase)

    def is_loop_mode(self) -> bool:
        return bool(self.modelWrapper and self.modelWrapper.loop)

    def need_start_by_new_group(self) -> bool:
        return bool(self.modelWrapper and self.modelWrapper.increase)

    def parse_dest_one_at_name(self, dest):
        return _text(dest)

    def parse_fist_dest_link(self):
        return _text(self.destes[0]) if self.destes else ""

    def parse_source_dest_link(self):
        return _text(self.source)

    def printFailedTips(self):
        from ..config.NewConfig import (
            INCREASE_FETCH_MESSAGE_WHILE_MAX_LOOP,
            RANDOM_FETCH_MESSAGE_WHILE_MAX_LOOP,
        )

        source = _text(self.convertSource())
        topic = _text(self.convertSourceTopicId())
        print(
            f"当前频道： {source}|{topic}"
            f" , 请注意，你配置的源群组是：{source}"
            f"  话题ID是：{topic}"
            " 你得进入源群组对应的话题，查看是否采集完了全部资源"
            " ， 采集消息失败了！请检查原因！"
        )
        print("检查指导： ")
        print("1、如果是私有频道，请确保你当前搬运的账号能访问私有频道/群组！")
        print("2、检查开始ID等参数，看看是否超过频道资源现有的最大资源ID！")
        print("3、检查源频道的资源是否被清除了，导致采集资源失败！")
        if self.is_ramdom_mode():
            print(
                "4、当前搬运模式为随机模式，如果是去重了"
                f"{RANDOM_FETCH_MESSAGE_WHILE_MAX_LOOP}"
                "次，通常是源频道资源已经采集完成了！"
            )
            print(
                "    4.1、你可以检查搬运的资源类型，"
                "或者检查搬运资源的过滤大小参数！"
            )
            print(
                "    4.2、如果你需要继续随机模式搬运频道资源，"
                "可以选中搬运流，鼠标点击右键【编辑条目】然后可以点击"
                "【清除资源记录】按钮，这样就可以继续随机模式搬运资源了！"
            )
        elif self.is_increase_mode():
            print(
                "4、当前搬运模式为顺序模式，如果是去重了"
                f"{INCREASE_FETCH_MESSAGE_WHILE_MAX_LOOP}"
                "次，通常是源频道资源已经采集完成了！"
            )
            print(
                "    4.2、如果你需要继续顺序模式搬运频道资源，"
                "可以选中搬运流，鼠标点击右键【编辑条目】然后可以点击"
                "【清除资源记录】按钮，这样就可以继续顺序模式搬运资源了！"
            )
        return None


@dataclass
class AutoBean(SuperFlowBean):
    kid: str = ""
    auto_type: int = AUTO_BEAN_TYPE_OLD
    active: bool = True
    priority: int = 100
    db_channel: str = ""
    commentRule: Optional[CommentRuleBean] = None
    completeVersionOp: Optional[CompleteVersionOp] = None
    botBean: Optional[BotBean] = None

    def genTypeText(self) -> str:
        if self.isBanYunType():
            return "【搬运流】"
        if self.isAutoFlowType():
            return "【自动流】"
        if self.isYuLanFlowType():
            return "【预览流】"
        if self.isDownLoadFlowType():
            return "【下载流】"
        if self.isYunAutoType():
            return "【云自动】"
        if self.isYunPreViewType():
            return "【云预览】"
        return ""

    def getDbChannel(self):
        return self.db_channel or self.source

    def getDbChannelOriginal(self):
        return self.db_channel

    def getDbChannelTopic(self):
        return _parse_source_parts(self.db_channel)[1]

    def convertDbChannel(self):
        return self.db_channel

    def isBanYunType(self) -> bool:
        return self.auto_type == AUTO_BEAN_TYPE_BAN_YUN

    def isAutoFlowType(self) -> bool:
        return self.auto_type == AUTO_BEAN_TYPE_AUTO_FLOW

    def isYuLanFlowType(self) -> bool:
        return self.auto_type == AUTO_BEAN_TYPE_YU_LAN_FLOW

    def isDownLoadFlowType(self) -> bool:
        return self.auto_type == AUTO_BEAN_TYPE_DOWN_LOAD_FLOW

    def isYunAutoType(self) -> bool:
        return self.auto_type == AUTO_BEAN_TYPE_YUN_AUTO

    def isYunPreViewType(self) -> bool:
        return self.auto_type == AUTO_BEAN_TYPE_YUN_PRE_VIEW

    def getAdDest(self):
        return self.getSelfAdes()

    def getName(self) -> str:
        return self.name

    def getSource(self) -> str:
        return self.source

    def dtype(self):
        return self.auto_type

    def getDestes(self):
        return list(self.destes)

    def getYulanDestes(self):
        return list(self.yulan_destes)

    def loop_mode_startId(self):
        return getattr(self.modelWrapper, "startId", 0) if self.modelWrapper else 0

    def loop_mode_endId(self):
        return getattr(self.modelWrapper, "endId", 0) if self.modelWrapper else 0

    def increase_want_count(self):
        return getattr(self.modelWrapper, "wantCount", 0) if self.modelWrapper else 0

    def ramdom_want_count(self):
        return getattr(self.modelWrapper, "wantCount", 0) if self.modelWrapper else 0

    def ramdom_numberMode(self):
        return getattr(self.modelWrapper, "numberMode", "") if self.modelWrapper else ""

    def increase_numberMode(self):
        return getattr(self.modelWrapper, "numberMode", "") if self.modelWrapper else ""

    def increase_startId(self):
        return getattr(self.modelWrapper, "startId", 0) if self.modelWrapper else 0

    def set_increase_startId(self, start_id: int):
        if self.modelWrapper is not None:
            self.modelWrapper.startId = int(start_id)

    def keepSourceText(self) -> bool:
        return bool(
            self.advancedFilterBean
            and self.advancedFilterBean.keepSourceText
        )

    def filterButton(self) -> bool:
        return bool(
            self.advancedFilterBean
            and self.advancedFilterBean.filterButton
        )

    def containWords(self):
        if not self.advancedFilterBean:
            return []
        return list(self.advancedFilterBean.containWords)

    def excludeWords(self):
        if not self.advancedFilterBean:
            return []
        return list(self.advancedFilterBean.excludeWords)

    def model(self):
        return self.modelWrapper.model if self.modelWrapper else ""

    def getSelfAdes(self):
        return list(self.selfAdWrapper.ades) if self.selfAdWrapper else []

    def adIsBottomUp(self) -> bool:
        return bool(self.selfAdWrapper and self.selfAdWrapper.adIsBottomUp)

    def adIsDelete(self) -> bool:
        return bool(self.selfAdWrapper and self.selfAdWrapper.delete)

    def deleSourceText(self) -> bool:
        return bool(
            self.advancedFilterBean
            and self.advancedFilterBean.deleSourceText
        )

    def deleLink(self) -> bool:
        return bool(
            self.advancedFilterBean
            and self.advancedFilterBean.deleLink
        )

    def replaces(self):
        return list(self.replace.replaces) if self.replace else []

    def tailText(self) -> str:
        return self.tail.tail_text if self.tail else ""

    def needSendComment(self) -> bool:
        return bool(self.commentRule and self.commentRule.copyComment)

    def is_ramdom_mode(self) -> bool:
        return bool(self.modelWrapper and self.modelWrapper.random)

    def is_increase_mode(self) -> bool:
        return bool(self.modelWrapper and self.modelWrapper.increase)

    def is_loop_mode(self) -> bool:
        return bool(self.modelWrapper and self.modelWrapper.loop)


class DownLoadBean(AutoBean):
    pass


class BanYunBean(AutoBean):
    pass


class YuLanBean(AutoBean):
    pass


class AutoFlowBean(AutoBean):
    pass


class YunPreViewBean(AutoBean):
    pass


class YunAutoBean(AutoBean):
    pass


@dataclass
class DTopClass:
    scheduler: Any = None
    autoMap: dict = field(default_factory=dict)
    globalAdWrapper: AdWrapper = field(default_factory=AdWrapper)
    water: Optional[Water] = None
