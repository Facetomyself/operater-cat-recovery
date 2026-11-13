# Recovered module: src.py.com.yun.mao.fea._r_hb_file
# Result object used by the remote heartbeat / report endpoints.
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RemoteHb:
    """Normalized result of one remote heartbeat request.

    ``terminal`` tells callers not to retry, ``msg`` contains the server or
    transport error, and ``data`` is the decoded business object when present.
    """

    terminal: bool = False
    msg: str = ""
    data: Any = None

    @classmethod
    def success(cls, data: Any = None) -> "RemoteHb":
        return cls(terminal=False, msg="", data=data)

    @classmethod
    def failed_retry(cls, msg: str = "") -> "RemoteHb":
        return cls(terminal=False, msg=msg, data=None)

    @classmethod
    def failed_terminal(cls, msg: str = "") -> "RemoteHb":
        return cls(terminal=True, msg=msg, data=None)


def map_biz_fail_to_remote_hb(content_oj: dict) -> RemoteHb:
    """Map a decoded business failure envelope to ``RemoteHb``.

    The original module imports ``OPERATION_EX_CODE_ALLOW_AUTO_RETRY`` from
    ``_sq_req``.  The exact numeric allow-list is kept in that module's
    reconstruction; this function only performs the code-to-policy mapping.
    """
    try:
        from . import _sq_req

        code = content_oj.get("code") if isinstance(content_oj, dict) else None
        retry_msg = (
            content_oj.get("msg", "")
            if isinstance(content_oj, dict)
            else ""
        )
        if code in getattr(_sq_req, "OPERATION_EX_CODE_ALLOW_AUTO_RETRY", ()):
            return RemoteHb.failed_retry(retry_msg)
        terminal_msg = retry_msg or "remote business request failed"
        return RemoteHb.failed_terminal(terminal_msg)
    except Exception:
        return RemoteHb.failed_terminal("remote business request failed")
