# Recovered module: src.py.com.yun.mao.fea._sq_bao
# Licence-order payload builders reconstructed from the function names,
# varnames and constant names. Business-field names are exact where observed.
from __future__ import annotations

import json


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _gen_parse_fack_content(u_code: str, parse_payload: dict) -> str:
    return _json({"uCode": u_code, "parse_payload": parse_payload})


def _kh_meta_bv_bx_dict() -> dict:
    return {"bv": "9.6.3", "bx": "recovered"}


def _kh_meta_bv_bx_snippet() -> str:
    return _json(_kh_meta_bv_bx_dict())


def gen_create_order_content(*args, **kwargs) -> str:
    return _json({"order": [repr(item) for item in args]})


def gen_check_order_content(json_content: str) -> str:
    return json_content


def gen_migrate_code_content(
    code_from: str,
    code_to: str,
    cover_expri: bool,
    force_cover_yun: bool,
    json_content: str,
) -> str:
    return _json(
        {
            "code_from": code_from,
            "code_to": code_to,
            "cover_expri": cover_expri,
            "force_cover_yun": force_cover_yun,
            "payload": json_content,
        }
    )


def zq_cz_hb(reset: str, json_content: str) -> str:
    return _json({"reset": reset, "payload": json_content})


def zq_jy_hb(uCode: str, json_content: str) -> str:
    return _json({"uCode": uCode, "payload": json_content})


def zq_pz_hb(json_content: str) -> str:
    return json_content


def zq_yp_ch_hb(u_code: str, parse_payload: dict) -> str:
    return _gen_parse_fack_content(u_code, parse_payload)


def zq_yp_cm_hb(json_content: str) -> str:
    return json_content


def zq_zc_hb(pre: str, fake: str) -> str:
    return _json({"pre": pre, "fake": fake})
