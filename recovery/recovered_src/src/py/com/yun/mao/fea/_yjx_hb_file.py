# Recovered module: src.py.com.yun.mao.fea._yjx_hb_file
# Channel/comment parse heartbeat helpers.
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, List, Optional

from . import _sq_jqm, _sq_req
from ._fs_jh_zb_file import assemble_parse_beans_from_messages
from ._xx_zy_file import (
    build_channel_parse_payload,
    build_comment_parse_payload,
    build_parse_trace_id,
    messages_to_digests,
)
from ..link._fds_jm import sec


@dataclass
class YjxHb:
    terminal: bool = False
    msg: str = ""
    beans: List[Any] = field(default_factory=list)

    @classmethod
    def success(cls, beans: Optional[List[Any]] = None) -> "YjxHb":
        return cls(terminal=False, msg="", beans=beans or [])

    @classmethod
    def failed_retry(cls, msg: str = "") -> "YjxHb":
        return cls(terminal=False, msg=msg, beans=[])

    @classmethod
    def failed_terminal(cls, msg: str = "") -> "YjxHb":
        return cls(terminal=True, msg=msg, beans=[])


def _yp_tm_uc(ucode: str) -> str:
    """Derive the parse-side account token from a machine code."""
    return hashlib.sha256(str(ucode or "").encode("utf-8")).hexdigest()


def _parse_result(result):
    if isinstance(result, tuple):
        if len(result) >= 2 and isinstance(result[0], bool):
            return result[0], result[1]
    if isinstance(result, dict):
        return bool(result.get("isSuccess", True)), result
    return bool(result), result


def _lookup(module, name, default=None):
    try:
        return getattr(module, name)
    except Exception:
        return default


def yp_jx_pd_ch(
    auto,
    message_list_object,
    is_monitor: bool = False,
) -> YjxHb:
    """Build and submit a channel parse request."""
    try:
        fs_yp_js = _lookup(__import__(
            "src.py.com.yun.mao.link._fds_rt",
            fromlist=["fs_yp_js"],
        ), "fs_yp_js", lambda: None)
        gy_jc_a4 = _lookup(__import__(
            "src.py.com.yun.mao.link._lk_gy_w",
            fromlist=["gy_jc_a4"],
        ), "gy_jc_a4", lambda: None)
        fs_yp_js()
        gy_jc_a4()
        message_digests = messages_to_digests(message_list_object)
        ucode = _sq_jqm.current_account_info.ucode
        request_id = build_parse_trace_id(
            ucode,
            _yp_tm_uc(ucode),
            "",
            str(len(message_digests)),
        )
        kid = getattr(auto, "kid", "") if not isinstance(auto, dict) else auto.get("kid", "")
        print(
            sec("yp_log_ch_start_tpl_10").format(
                request_id=request_id,
                kid=kid,
                is_monitor=is_monitor,
                count=len(message_digests),
            )
        )
        payload = build_channel_parse_payload(
            auto,
            message_digests,
            is_monitor,
            request_id,
            gy_jc_a4,
        )
        result = _sq_req.sq_yp_pd_ch(payload)
        success, content_oj = _parse_result(result)
        if not success:
            print(sec("yp_log_ch_req_fail_11"))
            return YjxHb.failed_retry("")
        code = content_oj.get("code") if isinstance(content_oj, dict) else None
        plan_data = content_oj.get("data", {}) if isinstance(content_oj, dict) else {}
        if not isinstance(plan_data, dict):
            return YjxHb.failed_terminal(sec("jqm_err_stop_04"))
        plan_id = plan_data.get("planId", "")
        server_groups = plan_data.get("groups") or []
        beans = assemble_parse_beans_from_messages(plan_data, message_list_object)
        if not beans:
            print(sec("yp_log_ch_asm_fail_13").format(
                request_id=request_id,
                plan_id=plan_id,
                server_groups=len(server_groups),
            ))
        print(sec("yp_log_ch_done_14").format(
            request_id=request_id,
            plan_id=plan_id,
            count=len(beans),
        ))
        _ = code
        return YjxHb.success(beans)
    except Exception as exc:
        print(sec("yp_log_ch_req_fail_11"), exc)
        return YjxHb.failed_retry(str(exc))


def yp_jx_pd_cm(
    comment_rule,
    replies,
) -> YjxHb:
    """Build and submit a comment parse request."""
    try:
        fs_yp_js = _lookup(__import__(
            "src.py.com.yun.mao.link._fds_rt",
            fromlist=["fs_yp_js"],
        ), "fs_yp_js", lambda: None)
        fs_yp_js()
        replies = list(replies or [])
        message_digests = messages_to_digests(replies)
        want_count = int(
            comment_rule.get("wantCount", 0)
            if isinstance(comment_rule, dict)
            else getattr(comment_rule, "wantCount", 0)
        )
        ucode = _sq_jqm.current_account_info.ucode
        request_id = build_parse_trace_id(
            ucode,
            _yp_tm_uc(ucode),
            "",
            str(len(message_digests)),
        )
        kid = (
            comment_rule.get("kid", "")
            if isinstance(comment_rule, dict)
            else getattr(comment_rule, "kid", "")
        )
        print(
            sec("yp_log_cm_start_tpl_17").format(
                request_id=request_id,
                count=want_count,
                kid=kid,
            )
        )
        payload = build_comment_parse_payload(
            comment_rule,
            message_digests,
            request_id,
        )
        result = _sq_req.sq_yp_pd_cm(payload)
        success, content_oj = _parse_result(result)
        if not success:
            print(sec("yp_log_cm_req_fail_18"))
            return YjxHb.failed_retry("")
        plan_data = content_oj.get("data", {}) if isinstance(content_oj, dict) else {}
        if not isinstance(plan_data, dict):
            return YjxHb.failed_terminal(sec("jqm_err_stop_04"))
        plan_id = plan_data.get("planId", "")
        server_groups = plan_data.get("groups") or []
        beans = assemble_parse_beans_from_messages(plan_data, replies)
        if not beans:
            print(sec("yp_log_cm_asm_fail_20").format(
                request_id=request_id,
                plan_id=plan_id,
                server_groups=len(server_groups),
            ))
        print(sec("yp_log_cm_done_21").format(
            request_id=request_id,
            plan_id=plan_id,
            count=len(beans),
        ))
        return YjxHb.success(beans)
    except Exception as exc:
        print(sec("yp_log_cm_req_fail_18"), exc)
        return YjxHb.failed_retry(str(exc))
