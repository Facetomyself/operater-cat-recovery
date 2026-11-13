# Recovered module: src.py.com.yun.mao.tab.gen_session_queue
# Telegram login queue recovered from the command/constant sequence.  The
# queue protocol and the exception branches are evidence-backed; the small
# callback adapters marked inferred keep the original UI contract.
from __future__ import annotations

import asyncio
import inspect
import os
from queue import Empty, Queue
from threading import Thread
from typing import Any, Callable, Optional
from pathlib import Path

from telethon.errors import (
    IncompleteReadError,
    PasswordHashInvalidError,
    PhoneCodeInvalidError,
    PhonePasswordFloodError,
    SessionPasswordNeededError,
)
from telethon.sync import TelegramClient

from ..config import InnerAppIdConfig, YunYinMaoConfig, net_config
from ..tgaccount.TGAuthAccount import TGAuthAccount
from ..tgaccount import TGAuthAccountSetting
from ..util.need import signals


GEN_SESSION_QUEUE_STOP = "GEN_SESSION_QUEUE_STOP"

gen_session_cmd_queue: "Queue[dict[str, Any] | str]" = Queue()
gen_session_loop_message: Optional[Thread] = None
GEN_SESSION_QUEUE_LOOP: Optional[asyncio.AbstractEventLoop] = None
client_map: dict[str, TelegramClient] = {}


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _account_dir() -> str:
    try:
        return str(YunYinMaoConfig.abs_tg_account_dir())
    except Exception:
        base = Path.home() / "YunYinData" / "tgaccount"
        base.mkdir(parents=True, exist_ok=True)
        return str(base)


def _proxy_config() -> Optional[dict[str, Any]]:
    try:
        if not net_config.enable_proxy():
            return None
        config = net_config.get_proxy_config()
        enabled = str(config.get("enable", "")).lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        if not enabled:
            return None
        return {
            "proxy_type": "socks5",
            "addr": str(config.get("ip", "")),
            "port": _safe_int(config.get("port"), 0),
            "rdns": True,
        }
    except Exception:
        return None


def connectException(prefix: str, exc: BaseException) -> None:
    text = f"{prefix}  {exc}"
    if isinstance(exc, IncompleteReadError):
        text += "  IncompleteReadError 远程关闭了链接，请开启代理重试，或者检测代理的IP端口是否设置正确！"
    elif isinstance(exc, ConnectionError):
        text += "  ConnectionError 链接错误，请开启代理重试，或者检测代理的IP端口是否设置正确！"
    elif "Failed to connect" in str(exc):
        text += "  Failed to connect 链接OS错误，请开启代理重试，或者检测代理的IP端口是否设置正确！"
    elif isinstance(exc, PhonePasswordFloodError):
        text += "  你已经尝试太多次登录了，请稍后再试，或者换账号再试吧！"
    elif isinstance(exc, PhoneCodeInvalidError):
        text += "  验证码输入错误！"
    else:
        text += "  链接异常，请开启代理重试，或者检测代理的IP端口是否设置正确！"
    print(text)


async def obtain(phone: str) -> Optional[TelegramClient]:
    """Create and connect a Telethon client for ``phone``."""
    phone = str(phone or "").strip()
    if not phone:
        return None
    print("debug 初始化账号 : ", phone)
    session_file = os.path.join(_account_dir(), f"{phone}.session")
    try:
        client = TelegramClient(
            session_file,
            InnerAppIdConfig.get_api_id(),
            InnerAppIdConfig.get_api_hash(),
            proxy=_proxy_config(),
        )
        client_map[phone] = client
        await _maybe_await(client.connect())
        print("debug 网络状态 : ", client.is_connected())
        if not client.is_connected():
            raise ConnectionError("Telegram client is not connected")
        return client
    except Exception as exc:
        connectException("debug 连接失败，请关闭软件或者开启代理网络重试！", exc)
        return None


async def safe_disconnect(client: Optional[TelegramClient]) -> None:
    if client is None:
        return
    try:
        await _maybe_await(client.disconnect())
    except Exception as exc:
        print("发送异常，可能是闪退了", exc)


async def disconnect_all_session_client() -> None:
    for phone, client in list(client_map.items()):
        try:
            await safe_disconnect(client)
        finally:
            client_map.pop(phone, None)


def get_name(me: Any) -> str:
    first_name = str(getattr(me, "first_name", "") or "")
    last_name = str(getattr(me, "last_name", "") or "")
    name = f"{first_name} {last_name}".strip()
    return name or str(getattr(me, "username", "") or "")


async def request_code(phone: str) -> bool:
    client = await obtain(phone)
    if client is None:
        return False
    try:
        print("debug 请求验证码")
        await _maybe_await(client.send_code_request(phone))
        return True
    except Exception as exc:
        connectException("debug 网络链接失败，请重试！", exc)
        await safe_disconnect(client)
        return False


async def phone_login(
    phone: str,
    code: str,
    two_pass: str = "",
    phone_login_callback: Optional[Callable[[str], None]] = None,
    finish_call: Optional[Callable[..., None]] = None,
) -> bool:
    """Complete a queued phone login, including the two-step password branch."""
    phone = str(phone or "").strip()
    code = str(code or "").strip()
    two_pass = str(two_pass or "").strip()
    client = client_map.get(phone) or await obtain(phone)
    if client is None:
        if finish_call is not None:
            finish_call(False, "")
        return False

    try:
        print("debug 登录...")
        try:
            await _maybe_await(client.sign_in(phone, code))
        except SessionPasswordNeededError:
            print("debug 需要两步验证码")
            if not two_pass:
                if phone_login_callback is not None:
                    phone_login_callback("请输入两步验证码！！")
                return False
            print("debug 校验两步验证码")
            try:
                await _maybe_await(client.sign_in(password=two_pass))
            except PasswordHashInvalidError:
                if phone_login_callback is not None:
                    phone_login_callback("两步验证码错误！")
                return False

        authorized = await _maybe_await(client.is_user_authorized())
        print("debug 授权状态 : ", authorized)
        me = await _maybe_await(client.get_me())
        if not authorized or me is None:
            raise RuntimeError("账号未授权")

        name = get_name(me)
        session_name = f"{phone}.session"
        print("debug 账户 : ", name, " 登录成功")
        account = TGAuthAccount()
        setattr(account, "username", phone)
        setattr(account, "nick", name)
        setattr(account, "session", session_name)
        try:
            save = getattr(client.session, "save", None)
            if callable(save):
                save()
        except Exception as exc:
            print("保存 Telegram session 失败：", exc)
        try:
            TGAuthAccountSetting.addOrUpdateAccount(account)
        except Exception as exc:
            print("保存账号失败：", exc)
        try:
            signals.global_ui_signal.update_account_list.emit("")
        except Exception:
            return None
        if finish_call is not None:
            finish_call(True, name)
        return True
    except Exception as exc:
        connectException("debug OSError网络链接失败，请重试！", exc)
        if phone_login_callback is not None:
            phone_login_callback("debug 网络链接失败，请重试！")
        if finish_call is not None:
            finish_call(False, "")
        return False


async def gen_session_loop(cmd_queue: "Queue[Any]") -> None:
    """Consume queue commands until the stop sentinel is received."""
    while True:
        try:
            task = await asyncio.to_thread(cmd_queue.get, True, 1.0)
        except Empty:
            await asyncio.sleep(0)
            continue
        except asyncio.CancelledError:
            break

        if task == GEN_SESSION_QUEUE_STOP:
            break
        if not isinstance(task, dict):
            continue

        cmd = str(task.get("cmd", ""))
        if cmd == "requestCode":
            await request_code(str(task.get("phone", "")))
        elif cmd == "phoneLogin":
            await phone_login(
                str(task.get("phone", "")),
                str(task.get("code", "")),
                str(task.get("psw", "")),
                task.get("callBack"),
                task.get("finish_call"),
            )


def check_queue(cmd_queue: "Queue[Any]") -> None:
    """Thread entry point that owns the asyncio queue loop."""
    global GEN_SESSION_QUEUE_LOOP
    loop = asyncio.new_event_loop()
    GEN_SESSION_QUEUE_LOOP = loop
    asyncio.set_event_loop(loop)
    task = loop.create_task(gen_session_loop(cmd_queue))
    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        task.cancel()
    finally:
        try:
            task.cancel()
        except Exception as exc:
            print("取消会话队列任务失败：", exc)
        try:
            loop.stop()
        finally:
            loop.close()
            GEN_SESSION_QUEUE_LOOP = None


gen_session_loop_message = Thread(
    target=check_queue,
    args=(gen_session_cmd_queue,),
    name="gen-session-queue",
)
gen_session_loop_message.start()


class GenSessionQueue:
    def __init__(self) -> None:
        self.thread = gen_session_loop_message

    def send_stop_send(self) -> None:
        gen_session_cmd_queue.put(GEN_SESSION_QUEUE_STOP)

    def requestCode(self, phone: str) -> None:
        gen_session_cmd_queue.put(
            {"cmd": "requestCode", "phone": str(phone or "").strip()}
        )

    def phoneLogin(
        self,
        phone: str,
        code: str,
        two_pass: str = "",
        phone_login_callback: Optional[Callable[[str], None]] = None,
        finish_call: Optional[Callable[..., None]] = None,
    ) -> None:
        gen_session_cmd_queue.put(
            {
                "cmd": "phoneLogin",
                "phone": str(phone or "").strip(),
                "code": str(code or "").strip(),
                "psw": str(two_pass or "").strip(),
                "callBack": phone_login_callback,
                "finish_call": finish_call,
            }
        )


__all__ = [
    "GEN_SESSION_QUEUE_LOOP",
    "GEN_SESSION_QUEUE_STOP",
    "GenSessionQueue",
    "check_queue",
    "client_map",
    "connectException",
    "disconnect_all_session_client",
    "gen_session_cmd_queue",
    "gen_session_loop",
    "gen_session_loop_message",
    "get_name",
    "obtain",
    "phone_login",
    "request_code",
    "safe_disconnect",
]
