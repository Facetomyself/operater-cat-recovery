# Recovered module: src.py.com.yun.mao.tgaccount.TGAuthAccount
# Behaviour-level reconstruction from Nuitka constants and signatures.
from __future__ import annotations

import json
from typing import Any


class TGAuthAccount:
    def __init__(
        self,
        session_file=None,
        session=None,
        nick=None,
        phone=None,
        userName=None,
    ) -> None:
        self.session_file = session_file
        self.session = session
        self.nick = nick
        self.phone = phone
        self.userName = userName


class TGAuthAccountEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, TGAuthAccount):
            return {
                "session_file": obj.session_file,
                "session": obj.session,
                "nick": obj.nick,
                "phone": obj.phone,
                "userName": obj.userName,
            }
        return super().default(obj)
