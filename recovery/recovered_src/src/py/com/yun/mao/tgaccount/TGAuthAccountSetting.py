# Recovered module: src.py.com.yun.mao.tgaccount.TGAuthAccountSetting
# Behaviour-level reconstruction from Nuitka constants and Hex-Rays.
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..config import YunYinMaoConfig
from ..util.need import utils
from .TGAuthAccount import TGAuthAccount, TGAuthAccountEncoder


# inferred: the original global is the on-disk filename; the account directory
# is resolved lazily so importing this module never creates folders.
AUTH_ACCOUNT_FILE = "session_account_list"

json_auth_account_map: dict[str, TGAuthAccount] = {}


def _auth_account_file() -> Path:
    return Path(YunYinMaoConfig.abs_tg_account_dir()) / AUTH_ACCOUNT_FILE


def _account_identity(account: Any) -> str:
    keys = ("session_file", "session", "userName", "phone")
    for key in keys:
        if isinstance(account, dict):
            value = account.get(key)
        else:
            value = getattr(account, key, None)
        if value:
            return str(value)
    return ""


def _account_from_mapping(values: dict[str, Any]) -> TGAuthAccount:
    return TGAuthAccount(
        session_file=values.get("session_file"),
        session=values.get("session"),
        nick=values.get("nick"),
        phone=values.get("phone"),
        userName=values.get("userName"),
    )


def updateToDisAuthAccountList() -> None:
    try:
        file_path = _auth_account_file()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            for session, account in json_auth_account_map.items():
                json_string = json.dumps(
                    account,
                    ensure_ascii=False,
                    cls=TGAuthAccountEncoder,
                )
                file.write(json_string + "\n")
    except Exception as exc:
        print("保存授权账号列表失败：", exc)


def getTgAccountList() -> list[TGAuthAccount]:
    return list(json_auth_account_map.values())


def addOrUpdateAccount(account: TGAuthAccount) -> None:
    key = _account_identity(account)
    if not key:
        return
    if not isinstance(account, TGAuthAccount):
        if isinstance(account, dict):
            account = _account_from_mapping(account)
        else:
            account = TGAuthAccount(
                session_file=getattr(account, "session_file", None),
                session=getattr(account, "session", None),
                nick=getattr(account, "nick", None),
                phone=getattr(account, "phone", None),
                userName=getattr(account, "userName", None),
            )
    json_auth_account_map[key] = account
    updateToDisAuthAccountList()


def deleteSession(session) -> None:
    session_text = str(session or "")
    abs_session_file = ""
    if session_text:
        abs_session_file = str(
            Path(YunYinMaoConfig.abs_tg_account_dir()) / session_text
        )
    if abs_session_file and Path(abs_session_file).exists():
        utils.safe_del_file(abs_session_file)

    session_name = Path(session_text).name
    for key, account in list(json_auth_account_map.items()):
        account_session_file = str(
            getattr(account, "session_file", "") or ""
        )
        account_session = str(getattr(account, "session", "") or "")
        if session_text in (key, account_session_file, account_session):
            json_auth_account_map.pop(key, None)
            continue
        if session_name and session_name in {
            Path(key).name,
            Path(account_session_file).name,
            Path(account_session).name,
        }:
            json_auth_account_map.pop(key, None)
    updateToDisAuthAccountList()


def loadFromDisAuthAccountList() -> list[TGAuthAccount]:
    json_auth_account_map.clear()
    file_path = _auth_account_file()
    if not file_path.exists():
        return getTgAccountList()
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                txt = line.strip()
                if not txt:
                    continue
                try:
                    dict_of_dicts = json.loads(txt)
                    if isinstance(dict_of_dicts, dict):
                        account = _account_from_mapping(dict_of_dicts)
                        key = _account_identity(account)
                        if key:
                            json_auth_account_map[key] = account
                except Exception as exc:
                    print("读取授权账号失败：", exc)
    except Exception as exc:
        print("读取授权账号列表失败：", exc)
    return getTgAccountList()
