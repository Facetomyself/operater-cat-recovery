# Recovered module: src.py.com.yun.mao.login.SessionLoader
# Telegram session discovery/login helpers reconstructed from the runtime
# constants and varnames.
from __future__ import annotations

import asyncio
import os

from telethon import TelegramClient, errors, functions
from telethon.tl.functions.account import GetPrivacyRequest, SetPrivacyRequest
from telethon.tl.types import (
    InputPrivacyKeyStatusTimestamp,
    InputPrivacyValueDisallowAll,
    PrivacyValueDisallowAll,
)

from . import ClientCacheHelper
from ..config import InnerAppIdConfig, net_config
from ..fea import _sq_jqm
from ..util import FloodGuard
from ..util.need import CommonCode, utils


__all__ = [
    "SessionLoader",
    "list_session_file",
    "ramdom_message",
    "connectException",
    "set_invisible_mode",
    "autologinWithSession",
    "autologinWithSessionByHide",
]


SESSION_FILE = ".session"


class SessionLoader:
    def __init__(self, list_session: bool = False):
        self.list_session = list_session

    def is_contain(self, session) -> bool:
        if isinstance(self.list_session, bool):
            return bool(self.list_session)
        target = str(session or "").lower()
        for existing in self.list_session or ():
            if str(existing or "").lower() in target:
                return True
        return False


def list_session_file(dir_path: str) -> list[str]:
    path_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(SESSION_FILE):
                path_list.append(os.path.join(root, file))
    return path_list


def ramdom_message(full_name: str) -> str:
    msg = utils.generate_random_chinese(10) + " say " + full_name
    return msg


def connectException(e: BaseException, prefix: str = ""):
    error_text = str(e)
    if "IncompleteReadError" in error_text:
        message = (
            "  IncompleteReadError 远程关闭了链接，请开启代理重试，"
            "或者检测代理的IP端口是否设置正确！"
        )
    elif "ConnectionError" in error_text:
        message = (
            "  ConnectionError 链接错误，请开启代理重试，"
            "或者检测代理的IP端口是否设置正确！"
        )
    elif "Failed to connect" in error_text:
        message = (
            "  Failed to connect 链接OS错误，请开启代理重试，"
            "或者检测代理的IP端口是否设置正确！"
        )
    elif isinstance(e, errors.PhonePasswordFloodError):
        message = "  你已经尝试太多次登录了，请稍后再试，或者换账号再试吧！"
    elif isinstance(e, errors.AuthKeyDuplicatedError):
        message = (
            "  AuthKeyDuplicatedError 链接异常，请开启代理重试，"
            "或者检测代理的IP端口是否设置正确！"
        )
    else:
        message = "  链接异常，请开启代理重试，或者检测代理的IP端口是否设置正确！"
    print(("debug " + prefix + message).strip())
    return e


async def set_invisible_mode(client: TelegramClient):
    try:
        key = InputPrivacyKeyStatusTimestamp()
        current_privacy = await FloodGuard.with_flood_retry(
            lambda: client(GetPrivacyRequest(key)),
            prefix="set_invisible_mode/GetPrivacyRequest",
        )
        rules = getattr(current_privacy, "rules", None) or []
        if any(
            isinstance(rule, PrivacyValueDisallowAll) for rule in rules
        ):
            return True
        result = await FloodGuard.with_flood_retry(
            lambda: client(
                SetPrivacyRequest(
                    key,
                    [InputPrivacyValueDisallowAll()],
                )
            ),
            prefix="set_invisible_mode/SetPrivacyRequest",
        )
        _ = current_privacy, result
    except Exception as exc:
        print("设置隐身模式失败: ", exc)
        return False
    return True


def _is_dead_exception(error: BaseException) -> bool:
    name = error.__class__.__name__.lower()
    return any(
        token in name
        for token in (
            "authkeyunregistered",
            "userdeactivated",
            "sessionrevoked",
            "authkeyduplicated",
        )
    )


def _is_band_exception(error: BaseException) -> bool:
    name = error.__class__.__name__.lower()
    return any(
        token in name
        for token in ("banned", "forbidden", "peerflood", "channelprivate")
    )


async def _login_once(
    session: str,
    normal_list=None,
    dead_list=None,
    banned_list=None,
    login_failed=None,
    normal_disconnect: bool = False,
):
    normal_list = [] if normal_list is None else normal_list
    dead_list = [] if dead_list is None else dead_list
    banned_list = [] if banned_list is None else banned_list
    login_failed = [] if login_failed is None else login_failed
    _phone_suf, phone = utils.split_session(session)
    print("debug 准备登录账号 : ", phone)
    proxy = net_config.get_proxy_config() if net_config.enable_proxy() else None
    client = TelegramClient(
        session,
        InnerAppIdConfig.get_api_id(),
        InnerAppIdConfig.get_api_hash(),
        proxy=proxy,
    )
    try:
        await client.connect()
    except asyncio.exceptions.CancelledError:
        raise
    except Exception as exc:
        print("debug 连接失败，请关闭软件或者开启代理网络重试！")
        connectException(exc, "连接失败")
        login_failed.append(session)
        return None, None
    net_status = client.is_connected()
    print("debug 网络状态 : ", net_status)
    if not net_status:
        login_failed.append(session)
        await CommonCode.safe_disconnect(client)
        return None, None
    auth_success = await client.is_user_authorized()
    print("debug 是否登录授权成功 : ", auth_success)
    if not auth_success:
        print("debug 当前账号授权失败！")
        login_failed.append(session)
        await CommonCode.safe_disconnect(client)
        return None, None
    try:
        await client(functions.updates.GetStateRequest())
    except errors.RPCError as error:
        if _is_dead_exception(error):
            dead_list.append(session)
        elif _is_band_exception(error):
            banned_list.append(session)
        else:
            print("debug 出现其他错误！")
            connectException(error, "登录状态检查失败")
        await CommonCode.safe_disconnect(client)
        return None, None
    me = await client.get_me()
    full_name = str(getattr(me, "full_name", "") or "")
    print("debug 当前登录账号 : ", full_name)
    try:
        at_name = str(
            getattr(_sq_jqm.current_account_info, "sendAtName", "") or ""
        ).strip()
        if at_name:
            msg = ramdom_message(full_name)
            await client.send_message(at_name, msg)
    except Exception as exc:
        connectException(exc, "启动问候")
    await set_invisible_mode(client)
    ClientCacheHelper.save_cache_client(client)
    normal_list.append(session)
    if normal_disconnect:
        await client.disconnect()
    return client, me


async def autologinWithSession(
    session: str,
    normal_list=None,
    dead_list=None,
    banned_list=None,
    login_failed=None,
    normal_disconnect: bool = False,
):
    normal_list = [] if normal_list is None else normal_list
    dead_list = [] if dead_list is None else dead_list
    banned_list = [] if banned_list is None else banned_list
    login_failed = [] if login_failed is None else login_failed
    try:
        return await _login_once(
            session,
            normal_list,
            dead_list,
            banned_list,
            login_failed,
            normal_disconnect,
        )
    except (errors.PhonePasswordFloodError, errors.AuthKeyDuplicatedError) as exc:
        connectException(exc, "debug 当前账号授权失败！")
        return None, None
    except Exception as exc:
        connectException(exc, "debug 出现其他错误！")
        return None, None


async def autologinWithSessionByHide(
    session: str,
    normal_list=None,
    dead_list=None,
    banned_list=None,
    login_failed=None,
    normal_disconnect: bool = False,
):
    client, me = await autologinWithSession(
        session,
        normal_list,
        dead_list,
        banned_list,
        login_failed,
        normal_disconnect,
    )
    if client is not None:
        try:
            await client.disconnect()
        except Exception:
            pass
    return client, me
