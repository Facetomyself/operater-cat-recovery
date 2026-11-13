# Recovered module: src.py.com.yun.mao.fea._dtdm_jz
# Dynamic worker-module decoder.  The recovered implementation is kept
# explicit for analysis; it is not executed by the recovery pipeline.
from __future__ import annotations

import base64
import gzip
import hashlib
import marshal
from typing import Any, Dict, Optional

from ..link._fds_jm import sec


class DtdmJz:
    _code_cache: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def dt_jz_xy(cls, response_data: dict, code_key: str) -> str:
        """Decode, unmarshal and namespace-load one worker module."""
        from ..link._fds_tan import wb_dt_zx

        wb_dt_zx()
        if code_key in cls._code_cache:
            print(sec("dt_jz_cache_tpl_09").format(code_key=code_key))
            return code_key
        if not isinstance(response_data, dict):
            print(sec("dt_jz_fld_miss_tpl_10"))
            return ""
        encoded_code = (
            response_data.get("byte_code_iwt")
            or response_data.get("byte_code")
            or response_data.get("encoded_code")
            or ""
        )
        if not encoded_code:
            print(sec("dt_jz_fld_miss_tpl_10"))
            return ""
        try:
            bytecode = cls._decode_and_decompress(str(encoded_code))
            module_name = "dtdm_" + hashlib.sha256(
                str(code_key).encode("utf-8")
            ).hexdigest()[:16]
            code_namespace = cls._dt_zx_zj(bytecode, module_name)
            cls._code_cache[code_key] = code_namespace
            print(
                sec("dt_jz_ok_tpl_13").format(
                    code_key=code_key,
                    count=len(code_namespace),
                )
            )
            return module_name
        except Exception as exc:
            print(sec("dt_jz_run_fail_tpl_12"), exc)
            return ""

    @classmethod
    def _decode_and_decompress(cls, encoded_code: str) -> bytes:
        try:
            raw = base64.b64decode(encoded_code)
        except Exception as exc:
            print(sec("dt_jz_dec_fail_tpl_11"), exc)
            raise
        try:
            return gzip.decompress(raw)
        except Exception as exc:
            print(sec("dt_jz_gz_fail_tpl_14"), exc)
            return raw

    @classmethod
    def _dt_zx_zj(cls, bytecode: bytes, module_name: str) -> Dict[str, Any]:
        try:
            code_object = marshal.loads(bytecode)
        except Exception as exc:
            print(sec("dt_byte_fail_tpl_04"), exc)
            raise
        namespace: Dict[str, Any] = {
            "__name__": module_name,
            "__builtins__": __builtins__,
        }
        exec(code_object, namespace)
        return {
            name: value
            for name, value in namespace.items()
            if callable(value) and not name.startswith("_")
        }

    @classmethod
    def dt_qc_hc(cls, code_key: str) -> None:
        cls._code_cache.pop(code_key, None)
        print(sec("dt_jz_clr_15").format(code_key=code_key))

    @classmethod
    def dt_hq_hc(cls, code_key: str) -> Optional[Dict[str, Any]]:
        return cls._code_cache.get(code_key)

    @classmethod
    def dt_js_hx(cls) -> None:
        cls._code_cache.clear()
