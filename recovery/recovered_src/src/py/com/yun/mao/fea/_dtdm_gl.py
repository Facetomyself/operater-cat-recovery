# Recovered module: src.py.com.yun.mao.fea._dtdm_gl
# Dynamic-module HMAC verification and worker dispatch.
from __future__ import annotations

import hashlib
import hmac

from ._dtdm_jz import DtdmJz
from ..link._fds_jm import sec
from ..link._fds_rt import fs_dt_mk
from ..link._tw_ctx import TwCtx


byte_code_iwt = None
dynamic_inner_work_task = None


def _dt_yq_mac(
    payload_b64: str,
    mac_hex: str,
    root_key: str = "",
) -> bool:
    """Verify the HMAC-SHA256 envelope used by dynamic worker payloads."""
    try:
        if not root_key:
            root_key = TwCtx.tw_hq_rk() or ""
        expected = hmac.new(
            str(root_key).encode("utf-8"),
            str(payload_b64).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(
            expected.lower(),
            str(mac_hex or "").strip().lower(),
        )
    except Exception:
        return False


def dt_hq_fn(func_name: str, module_name: str):
    """Resolve a public function from the decoded worker cache."""
    try:
        fs_dt_mk()
        namespace = DtdmJz.dt_hq_hc(module_name)
        if not isinstance(namespace, dict):
            return None
        return namespace.get(func_name)
    except Exception:
        return None


def dt_jz_dm(response_data: dict) -> bool:
    """Validate and decode a dynamic worker response."""
    global byte_code_iwt, dynamic_inner_work_task
    try:
        if not isinstance(response_data, dict):
            return False
        fs_dt_mk_value = response_data.get("fs_dt_mk", "")
        worker_key = response_data.get("worker_key", "")
        payload_b64 = (
            response_data.get("byte_code_iwt")
            or response_data.get("byte_code")
            or response_data.get("encoded_code")
            or ""
        )
        mac_hex = response_data.get("mac_hex", "")
        if not payload_b64:
            return False
        if mac_hex and not _dt_yq_mac(payload_b64, mac_hex):
            print(sec("dt_bc_fail_07"))
            return False
        byte_code_iwt = payload_b64
        code_key = worker_key or fs_dt_mk_value
        if not DtdmJz.dt_jz_xy(response_data, code_key):
            print(sec("dt_bc_fail_07"))
            return False
        dynamic_inner_work_task = dt_hq_fn(
            "dynamic_inner_work_task",
            code_key,
        )
        print(sec("dt_bc_ok_06"))
        return dynamic_inner_work_task is not None
    except Exception as exc:
        print(sec("dt_bc_fail_07"), exc)
        return False


def dt_qc_hc(response_data: dict | None = None) -> bool:
    """Clear a decoded worker namespace and its cached entry point."""
    global dynamic_inner_work_task
    dynamic_inner_work_task = None
    try:
        if isinstance(response_data, dict):
            key = response_data.get("worker_key", "")
            if key:
                DtdmJz.dt_qc_hc(key)
        else:
            DtdmJz.dt_js_hx()
        print(sec("dt_bc_clr_08"))
        return True
    except Exception:
        return False
