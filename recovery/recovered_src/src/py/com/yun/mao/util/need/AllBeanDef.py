# Recovered module: src.py.com.yun.mao.util.need.AllBeanDef
# Serializable request/UI/worker beans.  Field names are taken from the
# runtime signatures and Nuitka constants; this module intentionally keeps
# the Qt signal imports optional so pure-Python tests do not require PyQt5.
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


try:
    from PyQt5.QtCore import pyqtSignal
except Exception:
    class _Signal:
        def __get__(self, instance, owner):
            return None

    def pyqtSignal(*args, **kwargs):
        return _Signal()


@dataclass
class AiModelObj:
    name: str = ""
    price: str = ""


@dataclass
class MonitorSignalBean:
    updateTime: str = ""
    safeSource: str = ""
    queueSize: int = 0
    sended: int = 0
    total: int = 0
    sendedTotal: int = 0
    beanList: list = field(default_factory=list)


@dataclass
class MonitorSignalBeanWrapper:
    beanList: list = field(default_factory=list)


@dataclass
class MonitorTgMessageBean:
    message_id: int = 0
    safeSource: str = ""
    chat_id: int = 0
    group_id: int = 0
    group_key: str = ""
    is_text_msg: bool = False

    def __str__(self):
        return (
            "message_id: "
            + str(self.message_id)
            + " safeSource: "
            + str(self.safeSource)
            + " chat_id: "
            + str(self.chat_id)
            + " group_id: "
            + str(self.group_id)
            + " group_key: "
            + str(self.group_key)
            + " is_text_msg: "
            + str(self.is_text_msg)
        )


@dataclass
class ListUIAccountShowItemData:
    unin_id: str = ""
    select: bool = False
    account: Any = None


@dataclass
class AiEmployeeBean:
    uid: int = 0
    name: str = ""
    role: str = ""
    pre_text: str = ""
    sensitive: str = ""
    word_min: int = 0
    word_max: int = 0
    model: str = ""
    retry_count: int = 0


@dataclass
class AiEmployeeShowItemData:
    uid: int = 0
    aiBean: Optional[AiEmployeeBean] = None


@dataclass
class AiEmployeeListWrapper:
    employeeMap: dict = field(default_factory=dict)


@dataclass
class SleepArgs:
    sleep_min: int = 0
    sleep_max: int = 0


@dataclass
class FilterSessionItem:
    session_abs_path: str = ""
    topArgs: list = field(default_factory=list)
    autolist: list = field(default_factory=list)
    obtainFun: Any = None
    check_post_permission: bool = False
    delete_temp_files: bool = True
    down_load: Any = None
    up_load: Any = None
    finish_call: Any = None
    timing: Any = None
    convert_mode: str = ""
    stats_signal: Any = None


@dataclass
class BanYunUnProtectSendResult:
    has_exception: bool = False
    protect_content: bool = False
    real_time_message_id: int = 0
    send_success_count: int = 0
    orign_message: Any = None
    dest_id_map: Any = None
    ai_refused: bool = False

    def mark_ai_refused(self):
        self.ai_refused = True
        return self


@dataclass
class BanYunProtectSendResult:
    real_time_message_id: int = 0
    send_success_count: int = 0
    orign_message: Any = None
    dest_id_map: Any = None
    ai_refused: bool = False

    def mark_ai_refused(self):
        self.ai_refused = True
        return self


@dataclass
class FlowYunSendResult:
    real_time_message_id: int = 0
    send_success_count: int = 0
    orign_message: Any = None
    need_continue: bool = False
    dest_id_map: Any = None
    preview_id_map: Any = None

    def skip_group(self):
        self.need_continue = False
        return self


class ForeachLoopAction:
    CONTINUE = "continue"
    BREAK = "break"


@dataclass
class ParseGroupSendResult:
    real_time_message_id: int = 0
    need_sleep: bool = False
    send_count: int = 0
    send_group: int = 0
    sended_messages: Any = None
    need_continue: bool = False
    need_break: bool = False
    dest_id_map: Any = None
    preview_id_map: Any = None

    def skip_group(self):
        self.need_continue = False
        return self

    def stop_all(self):
        self.need_break = True
        return self

    @classmethod
    def from_unprotect_send(cls, bean):
        return cls(
            real_time_message_id=getattr(bean, "real_time_message_id", 0),
            send_count=getattr(bean, "send_success_count", 0),
            sended_messages=getattr(bean, "dest_id_map", None),
        )


@dataclass
class ForeachTotals:
    group_result: Any = None

    def apply_group_result(self, result):
        self.group_result = result
        return self

    def to_shared_results(self) -> dict:
        return {"group_result": self.group_result}

    def to_return_tuple(self):
        result = self.group_result
        if result is None:
            return 0, 0, 0, []
        return (
            getattr(result, "real_time_message_id", 0),
            getattr(result, "send_count", 0),
            getattr(result, "send_group", 0),
            list(getattr(result, "sended_messages", None) or []),
        )


@dataclass
class DTopClassWrapper:
    timing: Any = None
    autolist: list = field(default_factory=list)


@dataclass
class TgClientTaskSuperBean:
    session_abs_path: str = ""
    stats_signal: Any = None


@dataclass
class GenHtmlParamsBean(TgClientTaskSuperBean):
    post_link: str = ""


@dataclass
class PostAdTestBean(TgClientTaskSuperBean):
    channel_source: str = ""
    ad_html_text: str = ""
    ad_files: list = field(default_factory=list)


@dataclass
class MigrateCodeBean:
    old_u_code: str = ""
    new_u_code: str = ""
    cover_expri: bool = False
    force_cover_yun: bool = False


@dataclass
class CreateOrderBean:
    otype: str = ""
    ucode: str = ""
    amount: Any = None
    gradeStr: str = ""
    hoursStr: str = ""
    botStr: str = ""
    aiStr: str = ""
    odesc: str = ""

    def to_string(self) -> str:
        return (
            "CreateOrderBean("
            + ", ".join(
                f"{key}={value!r}"
                for key, value in vars(self).items()
            )
            + ")"
        )


@dataclass
class CheckOrderAndRechargeBean:
    ucode: str = ""
    onumber: str = ""


@dataclass
class PremiumEnumBean:
    models: list = field(default_factory=list)
    remaining: int = 0
    remaining_str: str = ""


@dataclass
class ActivateCodeBean:
    u_code: str = ""


@dataclass
class ParseBean:
    uniId: str = ""
    messages: list = field(default_factory=list)
    tart_text: str = ""
    tart_message: Any = None
    original_msg_ids: list = field(default_factory=list)
    source_main_msg_id: Any = None
    comment_to_msg_id: Any = None
    success: bool = False
    fake_success: bool = False
    # Compatibility aliases used by the recovery-side parse assembler.
    plan_id: str = ""
    request_id: str = ""
    uni_id: str = ""
    msg_ids: list = field(default_factory=list)
    text: str = ""
    parse_text: Any = None
    tart_text_alias: str = ""


@dataclass
class SendTarget:
    raw_dest: Any = None
    channel_key: str = ""
    channel_entity: Any = None
    user_topic_id: Any = None

    def is_comment_mode(self) -> bool:
        return bool(self.user_topic_id)


@dataclass
class UploadPartContext:
    path: str = ""
    file_id: Any = None
    parts: list = field(default_factory=list)
    file_size: int = 0
    part_size: int = 0
    is_large: bool = False


@dataclass
class SendResult:
    message_ids: list = field(default_factory=list)
    album_size: int = 0

    def should_count(self) -> bool:
        return bool(self.message_ids) or self.album_size > 0
