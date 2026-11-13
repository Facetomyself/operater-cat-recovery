# Recovered module: src.py.com.yun.mao.dclass.AutoBeanXXX
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from typing import Any, List

from ..jm._my_r_gk import jm_jz_r_pk
from ..jm._my_util import jm_yq_qm
from . import DTopClassHelper
from .DTopClass import AutoBean, _parse_source_parts
from .ExecCandidateHelper import compute_af


__all__ = [
    "AutoBeanXXX",
    "ExecutionTicket",
    "_build_item_sign_payload",
    "_exec_from_wire",
    "_ticket_from_wire",
    "_verify_sign_batch",
    "_verify_sign_item",
    "mem_auto_for_writeback",
]


def _build_item_sign_payload(ticket, kid: str, auto_type: int) -> str:
    """Build the item-level signing payload.

    The decompiled body formats eleven values and joins them with ``"|"``.
    The first nine are the ``ExecutionTicket`` fields in constant-pool order;
    the last two bind the payload to the ``kid``/``auto_type`` pair.
    """

    return "|".join(
        (
            str(ticket.ver),
            str(ticket.batch_id),
            str(ticket.etid),
            str(ticket.sn),
            str(ticket.af),
            str(ticket.uc_hash),
            str(ticket.mode),
            str(ticket.iat),
            str(ticket.exp),
            str(kid),
            str(auto_type),
        )
    )


def _verify_sign_item(kid: str, auto_type: int, ticket) -> bool:
    """Verify the per-item RSA/SHA-256 signature.

    The original signature order is ``(kid, auto_type, ticket)``; the
    decompiled body forwards ``(ticket, kid, auto_type)`` to
    :func:`_build_item_sign_payload`.
    """

    payload = _build_item_sign_payload(ticket, kid, auto_type)
    signature = bytes.fromhex(str(ticket.sign_item).strip())
    return jm_yq_qm(jm_jz_r_pk(), payload.encode("utf-8"), signature)


def _verify_sign_batch(
    batch_id: str,
    exp: int,
    server_nonce: str,
    kids: List[str],
    sign_batch: str,
) -> bool:
    """Verify the batch-level RSA/SHA-256 signature.

    The payload is ``batch_id|exp|server_nonce|kid1,kid2,...``; an empty
    ``sign_batch`` short-circuits to ``False`` before signature parsing.
    """

    if not sign_batch:
        return False
    payload = "|".join(
        (
            str(batch_id),
            str(exp),
            str(server_nonce),
            ",".join(str(kid) for kid in kids),
        )
    )
    signature = bytes.fromhex(str(sign_batch).strip())
    return jm_yq_qm(jm_jz_r_pk(), payload.encode("utf-8"), signature)


def _ticket_from_wire(exec_raw: Any, auto_type: int = 0, kid: str = "") -> ExecutionTicket:
    """Build an ``ExecutionTicket`` from the wire-side exec mapping.

    The decompiled body reads the eleven ticket fields through ``get`` with
    the recovered defaults.  ``auto_type``/``kid`` are kept for call-site
    compatibility with the original three-argument helper.
    """

    raw = exec_raw if isinstance(exec_raw, dict) else {}
    return ExecutionTicket(
        ver=int(raw.get("ver", 0) or 0),
        iat=int(raw.get("iat", 0) or 0),
        exp=int(raw.get("exp", 0) or 0),
        batch_id=str(raw.get("batch_id", "")),
        etid=str(raw.get("etid", "")),
        sn=str(raw.get("sn", "")),
        af=str(raw.get("af", "")),
        cfg_ver=int(raw.get("cfg_ver", 0) or 0),
        uc_hash=str(raw.get("uc_hash", "")),
        gh=str(raw.get("gh", "")),
        mode=str(raw.get("mode", "")),
        sign_item=str(raw.get("sign_item", "")),
    )


def _exec_from_wire(exec_raw: Any, auto_type: int = 0, kid: str = ""):
    """Rebuild the execution bean wrapper from the wire-side mapping.

    The decompiled body creates a five-key dict
    (``kid/auto_type/active/priority/beanLike``) and passes it through
    ``DTopClassHelper.dic_to_Auto_obj``.  The final ``beanLike`` lookup is
    kept as a compatibility fallback when the reconstructed bean class does
    not expose the original property.
    """

    if not isinstance(exec_raw, dict):
        return None
    wrapper = {
        "kid": kid,
        "auto_type": auto_type,
        "active": False,
        "priority": 100,
        "beanLike": exec_raw,
    }
    auto = DTopClassHelper.dic_to_Auto_obj(wrapper)
    if auto is None:
        return None
    return getattr(auto, "beanLike", auto)


@dataclass
class ExecutionTicket:
    ver: int = 0
    iat: int = 0
    exp: int = 0
    batch_id: str = ""
    etid: str = ""
    sn: str = ""
    af: str = ""
    cfg_ver: int = 0
    uc_hash: str = ""
    gh: str = ""
    mode: str = ""
    sign_item: str = ""

    @classmethod
    def from_raw(cls, raw: dict):
        return cls(
            ver=int(raw.get("ver", 0) or 0),
            iat=int(raw.get("iat", 0) or 0),
            exp=int(raw.get("exp", 0) or 0),
            batch_id=str(raw.get("batch_id", "")),
            etid=str(raw.get("etid", "")),
            sn=str(raw.get("sn", "")),
            af=str(raw.get("af", "")),
            cfg_ver=int(raw.get("cfg_ver", 0) or 0),
            uc_hash=str(raw.get("uc_hash", "")),
            gh=str(raw.get("gh", "")),
            mode=str(raw.get("mode", "")),
            sign_item=str(raw.get("sign_item", "")),
        )


class AutoBeanXXX:
    def __init__(self, kid: str = "", auto_type: int = 0, ticket=None, exec_obj=None):
        self.kid = str(kid)
        self.auto_type = int(auto_type or 0)
        self.ticket = ticket
        self.exec_obj = exec_obj

    @property
    def beanLike(self) -> bool:
        return True

    @classmethod
    def parse_wire(cls, batch_data: dict, source_beans: List[AutoBean], ucode: str):
        """Parse and verify the recovered wire batch.

        The decompiled body reads the batch fields, verifies the batch
        signature, then rebuilds each entry from its ticket/exec payloads and
        verifies the item signature, execution fingerprint, validity window
        and account binding.
        """

        if not isinstance(batch_data, dict):
            return False
        expected_keys = (
            "batch_id",
            "exp",
            "server_nonce",
            "sign_batch",
            "entries",
        )
        if any(key not in batch_data for key in expected_keys):
            return False
        entries = batch_data.get("entries") or []
        if not isinstance(entries, list):
            return False
        kids = [
            str((entry or {}).get("kid", "")).strip()
            for entry in entries
            if isinstance(entry, dict)
        ]
        if not _verify_sign_batch(
            str(batch_data.get("batch_id", "") or ""),
            int(batch_data.get("exp", 0) or 0),
            str(batch_data.get("server_nonce", "") or ""),
            kids,
            str(batch_data.get("sign_batch", "") or ""),
        ):
            return False

        by_kid = {
            str(getattr(bean, "kid", "")): bean for bean in source_beans or []
        }
        ordered = []
        for entry in entries:
            if not isinstance(entry, dict):
                return False
            if entry.get("truncated"):
                return False
            kid = str(entry.get("kid", "") or "").strip()
            if not kid:
                return False
            auto_type = int(entry.get("auto_type", 0) or 0)
            sign_kid = str(entry.get("kid", "") or "").strip() or kid
            ticket = _ticket_from_wire(auto_type, sign_kid, entry.get("ticket"))
            exec_dict = entry.get("exec")
            exec_obj = _exec_from_wire(auto_type, sign_kid, exec_dict)
            if exec_obj is None:
                exec_obj = by_kid.get(kid)
            if exec_obj is None:
                return False
            af_exec = compute_af(exec_obj)
            if str(af_exec).lower() != str(ticket.af).lower():
                return False
            xxx = cls(
                kid=kid,
                auto_type=auto_type,
                ticket=ticket,
                exec_obj=exec_obj,
            )
            if not _verify_sign_item(sign_kid, auto_type, ticket):
                return False
            if not xxx.ensure_valid(ucode):
                return False
            from ..link._lk_gy_w import gy_wc_hx

            gy_wc_hx(xxx, ucode)
            ordered.append(xxx)
        return ordered

    def ensure_valid(self, ucode: str) -> bool:
        ticket = self.ticket
        if ticket is None:
            return False
        raw_kid = str(self.kid or "")
        if not raw_kid or not ucode:
            return False
        now = int(time.time())
        uc_hash = hashlib.sha256(str(ucode).encode("utf-8")).hexdigest().lower()
        exp = int(getattr(ticket, "exp", 0) or 0)
        if exp and now > exp:
            return False
        bound_hash = str(getattr(ticket, "uc_hash", "") or "").lower()
        if bound_hash and bound_hash != uc_hash:
            return False
        exec_kid = str(getattr(self.exec_obj, "kid", "") or "")
        if exec_kid and exec_kid != raw_kid:
            return False
        if not _verify_sign_item(raw_kid, self.auto_type, ticket):
            return False
        return True

    def genTypeText(self) -> str:
        return {
            1: "【搬运流】",
            2: "【自动流】",
            3: "【预览流】",
            4: "【下载流】",
            5: "【云自动】",
            6: "【云预览】",
        }.get(self.auto_type, "")

    def getDbChannel(self):
        return getattr(self.exec_obj, "db_channel", "") if self.exec_obj else ""

    def getDbChannelOriginal(self):
        return getattr(self.exec_obj, "db_channel", None) if self.exec_obj else None

    def getDbChannelTopic(self):
        if self.exec_obj is not None and hasattr(self.exec_obj, "getDbChannelTopic"):
            return self.exec_obj.getDbChannelTopic()
        return _parse_source_parts(self.getDbChannel())[1]

    def convertDbChannel(self):
        return self.getDbChannel()

    def convertSource(self):
        return getattr(self.exec_obj, "source", "") if self.exec_obj else ""

    def convertSourceTopicId(self):
        return self.convertSource()

    def isBanYunType(self):
        return self.auto_type == 1

    def isAutoFlowType(self):
        return self.auto_type == 2

    def isYuLanFlowType(self):
        return self.auto_type == 3

    def isDownLoadFlowType(self):
        return self.auto_type == 4

    def isYunAutoType(self):
        return self.auto_type == 5

    def isYunPreViewType(self):
        return self.auto_type == 6

    def getDestes(self):
        return getattr(self.exec_obj, "destes", []) if self.exec_obj else []

    def getYulanDestes(self):
        return getattr(self.exec_obj, "yulan_destes", []) if self.exec_obj else []

    def getAdDest(self):
        getter = getattr(self.exec_obj, "getAdDest", None)
        return getter() if callable(getter) else self.getDestes()

    def getName(self):
        getter = getattr(self.exec_obj, "getName", None)
        if callable(getter):
            return getter()
        return str(getattr(self.exec_obj, "name", "") or "")

    def getSource(self):
        getter = getattr(self.exec_obj, "getSource", None)
        if callable(getter):
            return getter()
        return str(getattr(self.exec_obj, "source", "") or "")

    def is_ramdom_mode(self) -> bool:
        checker = getattr(self.exec_obj, "is_ramdom_mode", None)
        return bool(checker()) if callable(checker) else False

    def is_increase_mode(self) -> bool:
        checker = getattr(self.exec_obj, "is_increase_mode", None)
        return bool(checker()) if callable(checker) else False

    def is_loop_mode(self) -> bool:
        checker = getattr(self.exec_obj, "is_loop_mode", None)
        return bool(checker()) if callable(checker) else False

    def loop_mode_startId(self):
        getter = getattr(self.exec_obj, "loop_mode_startId", None)
        return getter() if callable(getter) else 0

    def loop_mode_endId(self):
        getter = getattr(self.exec_obj, "loop_mode_endId", None)
        return getter() if callable(getter) else 0

    def increase_want_count(self):
        getter = getattr(self.exec_obj, "increase_want_count", None)
        return getter() if callable(getter) else 0

    def ramdom_want_count(self):
        getter = getattr(self.exec_obj, "ramdom_want_count", None)
        return getter() if callable(getter) else 0

    def ramdom_numberMode(self):
        getter = getattr(self.exec_obj, "ramdom_numberMode", None)
        return getter() if callable(getter) else ""

    def increase_numberMode(self):
        getter = getattr(self.exec_obj, "increase_numberMode", None)
        return getter() if callable(getter) else ""

    def increase_startId(self):
        getter = getattr(self.exec_obj, "increase_startId", None)
        return getter() if callable(getter) else 0

    def printFailedTips(self):
        printer = getattr(self.exec_obj, "printFailedTips", None)
        return printer() if callable(printer) else None

    def need_start_by_new_group(self) -> bool:
        checker = getattr(self.exec_obj, "need_start_by_new_group", None)
        return bool(checker()) if callable(checker) else False

    def keepSourceText(self) -> bool:
        getter = getattr(self.exec_obj, "keepSourceText", None)
        return bool(getter()) if callable(getter) else False

    def filterButton(self) -> bool:
        getter = getattr(self.exec_obj, "filterButton", None)
        return bool(getter()) if callable(getter) else False

    def dtype(self):
        value = getattr(self.exec_obj, "dtype", "")
        return value() if callable(value) else value

    def containWords(self):
        getter = getattr(self.exec_obj, "containWords", None)
        return list(getter()) if callable(getter) else []

    def excludeWords(self):
        getter = getattr(self.exec_obj, "excludeWords", None)
        return list(getter()) if callable(getter) else []

    def model(self):
        getter = getattr(self.exec_obj, "model", None)
        return getter() if callable(getter) else str(getattr(self.exec_obj, "model", "") or "")

    def getSelfAdes(self):
        getter = getattr(self.exec_obj, "getSelfAdes", None)
        return list(getter()) if callable(getter) else []

    def adIsBottomUp(self) -> bool:
        getter = getattr(self.exec_obj, "adIsBottomUp", None)
        return bool(getter()) if callable(getter) else False

    def adIsDelete(self) -> bool:
        getter = getattr(self.exec_obj, "adIsDelete", None)
        return bool(getter()) if callable(getter) else False

    def parse_dest_one_at_name(self, dest):
        parser = getattr(self.exec_obj, "parse_dest_one_at_name", None)
        return parser(dest) if callable(parser) else dest

    def deleSourceText(self) -> bool:
        getter = getattr(self.exec_obj, "deleSourceText", None)
        return bool(getter()) if callable(getter) else False

    def deleLink(self) -> bool:
        getter = getattr(self.exec_obj, "deleLink", None)
        return bool(getter()) if callable(getter) else False

    def replaces(self):
        getter = getattr(self.exec_obj, "replaces", None)
        return list(getter()) if callable(getter) else []

    def tailText(self) -> str:
        getter = getattr(self.exec_obj, "tailText", None)
        return str(getter()) if callable(getter) else ""

    def needSendComment(self) -> bool:
        getter = getattr(self.exec_obj, "needSendComment", None)
        return bool(getter()) if callable(getter) else False

    def compute_af(self):
        return compute_af(self.exec_obj or self)


def mem_auto_for_writeback(autoxxx):
    """Resolve the persisted bean used for real-time increase writeback.

    inferred: the recovered caller accepts either a mapping or a callable;
    this implementation prefers the LoadDataClass bean and falls back to the
    wrapped execution object.
    """

    try:
        from .LoadDataClass import getAutoBeanById

        kid = str(getattr(autoxxx, "kid", "") or "")
        bean = getAutoBeanById(kid) if kid else None
        if bean is not None:
            return bean
    except Exception:
        pass
    return getattr(autoxxx, "exec_obj", None)
