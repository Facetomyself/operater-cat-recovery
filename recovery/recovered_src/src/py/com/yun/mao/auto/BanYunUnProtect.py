# Recovered module: src.py.com.yun.mao.auto.BanYunUnProtect
# Reconstruction from Nuitka constants and the module init code object.
# The public signature and the branch names are confirmed by the init metadata;
# request payload details and a few fallbacks are marked inferred.
from __future__ import annotations

import importlib
import inspect
import traceback
from typing import Any, Dict, List, Optional, Sequence


def _optional_import(module_name: str, attribute: Optional[str] = None):
    try:
        module = importlib.import_module(module_name, __package__)
    except Exception:
        return None
    if attribute is None:
        return module
    return getattr(module, attribute, None)


async def _maybe_await(value):
    if inspect.isawaitable(value):
        return await value
    return value


async def _call_adapted(func, positional: Sequence[Any], values: Dict[str, Any]):
    if not callable(func):
        return None
    try:
        signature = inspect.signature(func)
    except (TypeError, ValueError):
        return await _maybe_await(func(*positional))
    kwargs = {
        key: value
        for key, value in values.items()
        if key in signature.parameters
        and signature.parameters[key].kind
        in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
    }
    return await _maybe_await(func(*positional, **kwargs))


def _stop_requested() -> bool:
    working = _optional_import("..cd", "Working")
    return bool(getattr(working, "need_stop", False)) if working else False


def _print_trace() -> None:
    helper = _optional_import("..util", "TracePrinterHelper")
    printer = getattr(helper, "print_trace", None)
    if callable(printer):
        try:
            printer()
            return
        except Exception:
            pass
    traceback.print_exc()


def _as_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _collect(value) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, (str, bytes, dict)):
        return [value]
    try:
        return list(value)
    except TypeError:
        return [value]


def _get_messages(parse) -> List[Any]:
    getter = getattr(parse, "getMessages", None)
    if callable(getter):
        try:
            value = getter()
            if not inspect.isawaitable(value) and value is not None:
                return list(value)
        except Exception:
            pass
    return list(getattr(parse, "messages", None) or [])


def _get_medias(parse) -> List[Any]:
    getter = getattr(parse, "getMedias", None)
    if callable(getter):
        try:
            value = getter()
            if not inspect.isawaitable(value) and value is not None:
                return list(value)
        except Exception:
            pass
    return list(getattr(parse, "medias", None) or [])


def _source_of(parse, auto) -> Any:
    getter = getattr(parse, "getSource", None)
    if callable(getter):
        try:
            value = getter()
            if value is not None:
                return value
        except Exception:
            pass
    return getattr(parse, "source", None) or getattr(auto, "source", None)


def _text_of(message) -> str:
    text = getattr(message, "text", None)
    if text is None:
        text = getattr(message, "message", None)
    return str(text or "")


def _result_class():
    return _optional_import(
        "..util.need.AllBeanDef", "BanYunUnProtectSendResult"
    )


def _new_result(**kwargs):
    cls = _result_class()
    result = cls() if callable(cls) else type("_UnProtectResult", (), {})()
    defaults = {
        "has_exception": False,
        "protect_content": False,
        "real_time_message_id": 0,
        "send_success_count": 0,
        "orign_message": None,
        "dest_id_map": {},
        "send_to_comment": False,
        "ai_refused": False,
    }
    for key, value in defaults.items():
        try:
            setattr(result, key, value)
        except Exception:
            pass
    for key, value in kwargs.items():
        try:
            setattr(result, key, value)
        except Exception:
            pass
    return result


def _targets(auto, dest_to_map) -> List[Any]:
    if isinstance(dest_to_map, dict) and dest_to_map:
        return list(dest_to_map.keys())
    getter = getattr(auto, "getDestes", None)
    if callable(getter):
        try:
            value = getter()
            if value is not None:
                return list(value)
        except Exception:
            pass
    return list(
        getattr(auto, "destes", None)
        or getattr(auto, "destinations", None)
        or []
    )


def _destination_value(dest, topic_id=0):
    converter = _optional_import("..dclass", "DTopClass")
    convert = getattr(converter, "convertDest", None) if converter else None
    value = dest
    if callable(convert):
        try:
            value = convert(dest)
        except Exception:
            value = dest
    if topic_id:
        return value, _as_int(topic_id)
    return value


async def send_message_un_protect(
    client,
    parse,
    auto,
    dest_to_map,
):
    """Publish parsed messages without Telegram protected-content mode.

    This is the only recovered function in the module.  The original checks
    the same text, media, comment and destination maps that the protected
    module uses, but sends ordinary messages/files instead of protected ones.
    """

    result = _new_result()
    messages = _get_messages(parse)
    medias = _get_medias(parse)
    orign_message = messages[0] if messages else None
    result.orign_message = orign_message

    try:
        ledger = _optional_import("..record", "CommentCopyLedger")
        should_skip = getattr(ledger, "should_skip_comment_group", None)
        if callable(should_skip) and should_skip(auto):
            return result
    except Exception:
        pass

    text = str(
        getattr(parse, "tart_text", None)
        or getattr(parse, "text", None)
        or ""
    )
    if not text and messages:
        text = "\n".join(filter(None, (_text_of(msg) for msg in messages)))

    logic = _optional_import("..ai", "TextProcessLogic")
    bean = getattr(parse, "beanLike", None) or getattr(parse, "bean", None)
    try:
        processor = getattr(logic, "process_text_to_obj", None) if logic else None
        if callable(processor):
            value = processor(text)
            if value is not None and not inspect.isawaitable(value):
                text = str(value)
        ai_processor = (
            getattr(logic, "process_text_by_ai_if_need", None) if logic else None
        )
        if callable(ai_processor):
            value = ai_processor(text, auto, bean)
            if inspect.isawaitable(value):
                value = await value
            if value is not None:
                text = str(value)
    except Exception:
        _print_trace()

    if bool(getattr(parse, "ai_refused", False)) or bool(
        getattr(bean, "ai_refused", False)
    ):
        result.ai_refused = True
        if not bool(getattr(parse, "is_keep_origin_source", False)):
            print("AI 拒绝生成文案，跳过本组消息，继续下一组...")
            return result
        print("AI 拒绝生成文案，将会使用源文案发布...")

    try:
        full_text_has_tail = bool(getattr(parse, "full_text_has_tail", False))
        for_mat = getattr(parse, "for_mat", None) or getattr(bean, "for_mat", None)
        target_for_mat = "html" if getattr(for_mat, "name", for_mat) == "HTML" else None
    except Exception:
        full_text_has_tail = False
        target_for_mat = None

    cmcode = _optional_import(".CMCode")
    flood = _optional_import("..util", "FloodGuard")
    with_retry = getattr(flood, "with_flood_retry", None) if flood else None
    send_message = getattr(client, "send_message", None)
    send_file = getattr(client, "send_file", None)
    topic_utils = _optional_import(".TopicUtils")
    parse_topic = (
        getattr(topic_utils, "parse_parseBean_topic_id", None)
        if topic_utils
        else None
    )

    dest_id_map: Dict[Any, Any] = {}
    any_comment_sent = False
    destes = _targets(auto, dest_to_map)

    async def _send_comment(dest, message_id, comment_to_id):
        nonlocal any_comment_sent
        if not comment_to_id:
            return False
        comment_text = text
        if not comment_text:
            return False
        try:
            sender = getattr(cmcode, "send_message_only", None) if cmcode else None
            value = await _call_adapted(
                sender,
                (),
                {
                    "auto": auto,
                    "client": client,
                    "dest": dest,
                    "text": comment_text,
                    "parse_mode": target_for_mat,
                    "reply_to": comment_to_id,
                    "prefix": "unprotect/send_message/comment/markdown"
                    if full_text_has_tail
                    else "unprotect/send_message/comment/plaintext",
                },
            )
            any_comment_sent = bool(value is not None)
            if any_comment_sent and dest is not None:
                try:
                    dest_id_map.setdefault(dest, []).append(message_id)
                except Exception:
                    pass
                try:
                    marker = getattr(ledger, "mark_after_send", None)
                    if callable(marker):
                        marker(
                            _source_of(parse, auto),
                            _as_int(getattr(parse, "source_main_msg_id", 0)),
                            message_id,
                            dest,
                            comment_to_id,
                            _as_int(getattr(value, "id", 0)),
                        )
                except Exception:
                    pass
            return any_comment_sent
        except Exception:
            _print_trace()
            return False

    for dest in destes:
        if _stop_requested():
            print("手动停止成功！")
            break
        topic_id = 0
        if isinstance(dest_to_map, dict):
            topic_id = _as_int(dest_to_map.get(dest))
        if not topic_id and callable(parse_topic):
            try:
                topic_id = _as_int(parse_topic(parse))
            except Exception:
                topic_id = 0
        target = _destination_value(dest, topic_id)
        channel_part = dest
        channel_entity = target
        try:
            entity_getter = getattr(client, "get_entity", None)
            if callable(entity_getter):
                channel_entity = await _maybe_await(entity_getter(channel_part))
        except Exception:
            channel_entity = target

        try:
            comment_helper = (
                getattr(cmcode, "obtain_comment_to_id", None) if cmcode else None
            )
            comment_to_id = None
            if callable(comment_helper):
                comment_to_id = comment_helper(auto, parse, channel_part)
                if inspect.isawaitable(comment_to_id):
                    comment_to_id = await comment_to_id
            if comment_to_id:
                for message in messages[:1]:
                    await _send_comment(
                        channel_entity,
                        _as_int(getattr(message, "id", 0)),
                        comment_to_id,
                    )
        except Exception:
            _print_trace()

        if text:
            try:
                sender = getattr(cmcode, "send_message_only", None) if cmcode else None
                value = await _call_adapted(
                    sender,
                    (),
                    {
                        "auto": auto,
                        "client": client,
                        "dest": channel_entity,
                        "text": text,
                        "parse_mode": target_for_mat,
                        "reply_to": topic_id or None,
                        "prefix": "unprotect/send_message/channel/markdown"
                        if full_text_has_tail
                        else "unprotect/send_message/channel/plaintext",
                    },
                )
                if value is None and callable(send_message):
                    value = await _maybe_await(
                        send_message(
                            channel_entity,
                            text,
                            parse_mode=target_for_mat,
                            reply_to=topic_id or None,
                        )
                    )
                if value is not None:
                    result.send_success_count += 1
                    sent_id = _as_int(getattr(value, "id", 0))
                    dest_id_map.setdefault(channel_part, []).append(sent_id)
                    try:
                        recorder = _optional_import(
                            "..record.PublishIdRecord",
                            "log_publish_success",
                        )
                        if callable(recorder):
                            recorder(channel_part, sent_id)
                    except Exception:
                        pass
            except Exception:
                _print_trace()
                result.has_exception = True

        for media in medias:
            path = (
                getattr(media, "path", None)
                or getattr(media, "file_path", None)
                or getattr(media, "upload_path", None)
                or (media if isinstance(media, str) else None)
            )
            if not path or not callable(send_file):
                continue
            try:
                kwargs = {
                    "caption": text or None,
                    "parse_mode": target_for_mat,
                    "reply_to": topic_id or None,
                }
                kwargs = {key: value for key, value in kwargs.items() if value is not None}
                if callable(with_retry):
                    value = await _maybe_await(
                        with_retry(
                            lambda: send_file(channel_entity, path, **kwargs),
                            prefix="unprotect/send_file/channel/media",
                        )
                    )
                else:
                    value = await _maybe_await(send_file(channel_entity, path, **kwargs))
                if value is not None:
                    result.send_success_count += 1
                    dest_id_map.setdefault(channel_part, []).append(
                        _as_int(getattr(value, "id", 0))
                    )
            except Exception as exc:
                err = _optional_import("telethon.errors", "ChatForwardsRestrictedError")
                if err and isinstance(exc, err):
                    result.protect_content = True
                    continue
                _print_trace()
                result.has_exception = True

    result.dest_id_map = dest_id_map
    result.send_to_comment = any_comment_sent
    result.real_time_message_id = max(
        (
            _as_int(getattr(message, "id", 0))
            for message in messages
            if _as_int(getattr(message, "id", 0))
        ),
        default=0,
    )
    return result
