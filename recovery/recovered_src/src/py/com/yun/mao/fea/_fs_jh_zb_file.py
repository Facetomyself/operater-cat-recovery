# Recovered module: src.py.com.yun.mao.fea._fs_jh_zb_file
# Message-plan assembly helpers.
from __future__ import annotations

from typing import Any, Dict, Iterable, List

from ._xx_zy_file import parse_uni_id
from ..link._fds_jm import sec
from ..util.need import CommonCode


def _build_id_to_message(messages: Iterable[Any]) -> Dict[int, Any]:
    result: Dict[int, Any] = {}
    for message in messages or []:
        mid = getattr(message, "id", None)
        if mid is None and isinstance(message, dict):
            mid = message.get("id")
        if mid is not None:
            result[int(mid)] = message
    return result


def _message_text(message: Any) -> str:
    if isinstance(message, dict):
        return str(message.get("text", message.get("message", "")))
    return str(getattr(message, "text", getattr(message, "message", "")))


def _message_attr(message: Any, name: str, default=None):
    if isinstance(message, dict):
        return message.get(name, default)
    return getattr(message, name, default)


def assemble_parse_beans_from_messages(
    plan_data: dict,
    messages: Iterable[Any],
) -> List[Any]:
    """Assemble ``ParseBean`` objects from a plan and its source messages."""
    result: List[Any] = []
    plan_data = plan_data or {}
    plan_id = plan_data.get("planId", "")
    request_id = plan_data.get("requestId", "")
    groups = plan_data.get("groups") or []
    if not plan_id:
        print(sec("yp_log_asm_no_plan_22"))
        return result
    if not groups:
        print(sec("yp_log_asm_empty_23").format(plan_id, request_id))
        return result

    id_to_msg = _build_id_to_message(messages)
    if not id_to_msg:
        print(sec("yp_log_asm_no_msg_24").format(plan_id))
        return result

    for plan_group in groups:
        uni_id = plan_group.get("uniId", "")
        msg_ids = plan_group.get("msgIds") or []
        tart_msg_id = plan_group.get("tartMsgId")
        missing_msg_id = None
        filtered_messages = []
        for mid in msg_ids:
            msg = id_to_msg.get(int(mid)) if str(mid).lstrip("-").isdigit() else None
            if msg is None:
                missing_msg_id = mid
                break
            filtered_messages.append(msg)
        if missing_msg_id is not None:
            print(
                sec("yp_log_asm_miss_msg_25").format(
                    plan_id,
                    uni_id,
                    missing_msg_id,
                )
            )
            continue

        txt_msg = "\n".join(_message_text(m) for m in filtered_messages)
        try:
            parse_txt_msg = CommonCode.getGroupTextAndMessage(
                filtered_messages
            )
        except Exception:
            parse_txt_msg = (parse_uni_id(uni_id), None)
        tart_text, tart_message = parse_txt_msg
        if tart_msg_id is not None:
            tart_message = id_to_msg.get(int(tart_msg_id))
            tart_text = _message_text(tart_message) if tart_message else ""
        try:
            from ..util.need.AllBeanDef import ParseBean

            bean = ParseBean(
                plan_id=plan_id,
                request_id=request_id,
                uniId=uni_id,
                uni_id=uni_id,
                msg_ids=list(msg_ids),
                text=txt_msg,
                parse_text=parse_txt_msg,
                tart_text=tart_text,
                tart_message=tart_message,
                messages=filtered_messages,
            )
        except Exception:
            bean = {
                "plan_id": plan_id,
                "request_id": request_id,
                "uni_id": uni_id,
                "msg_ids": list(msg_ids),
                "text": txt_msg,
                "parse_text": parse_txt_msg,
                "tart_text": tart_text,
                "tart_message": tart_message,
                "messages": filtered_messages,
            }
        result.append(bean)
    print(
        sec("yp_log_asm_ok_27").format(
            plan_id,
            request_id,
            len(result),
        )
    )
    return result
