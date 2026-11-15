#!/usr/bin/env python3
"""Assemble official catalog URLs offline. No network."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urljoin, urlparse

LAB_DIR = Path(__file__).resolve().parent

def _live() -> Path:
    for live in (LAB_DIR.parent.parent / "live", LAB_DIR.parent / "capture_lab", LAB_DIR.parent.parent / "capture_lab"):
        if (live / "catalog_named_summary.json").exists():
            return live
    raise SystemExit("catalog_named_summary.json not found")

LIVE_DIR = _live()
SUMMARY = LIVE_DIR / "catalog_named_summary.json"
OUTPUT = LIVE_DIR / "catalog_urls.json"


def main() -> int:
    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    origin = data["_p_dh"]
    if origin.get("type") != "url":
        raise SystemExit("origin _p_dh is not a url")
    base = f"{origin['scheme']}://{origin['host']}/"
    rows = []
    for key, item in data.items():
        if item.get("type") == "path":
            url = urljoin(base, item["value"].lstrip("/"))
            rows.append({"key": key, "path": item["value"], "url": url})
        elif item.get("type") == "url":
            rows.append({"key": key, "path": item.get("path"), "url": f"{item['scheme']}://{item['host']}{item.get('path') or '/'}"})
        elif item.get("type") == "pem":
            rows.append({"key": key, "pem_fp16": item.get("fp16"), "bits": item.get("bits")})
    # heartbeat/report matrix using catalog paths, not recovered literals
    matrix = {
        "origin": base.rstrip("/"),
        "dev_origin": f"{data['_d_lh']['scheme']}://{data['_d_lh']['host']}",
        "bootstrap": f"{base.rstrip('/')}/xb/iil",
        "r_spi": urljoin(base, data["_v_p_i_u"]["value"].lstrip("/")),
        "r_spui": urljoin(base, data["_v_ps_i_u"]["value"].lstrip("/")),
        "r_ui": urljoin(base, data["_v_u_i_u"]["value"].lstrip("/")),
        "r_roi": urljoin(base, data["_v_r_p_i_u"]["value"].lstrip("/")),
        "r_ca": urljoin(base, data["_v_s_c_i_u"]["value"].lstrip("/")),
        "xb_fms": urljoin(base, data["_v_s_f_ms"]["value"].lstrip("/")),
        "register": urljoin(base, data["_r_u"]["value"].lstrip("/")),
        "experience": urljoin(base, data["_s_ac_u"]["value"].lstrip("/")),
    }
    payload = {
        "note": "offline assembly from decrypted catalog; do not fetch",
        "matrix": matrix,
        "rows": rows,
        "recovery_warning": [
            "get_pro_duct_host() -> _r_u is a path, not an origin",
            "origin is _p_dh = https://birder.jinsiqie.life/",
            "_r_url('r_spi') recovered literal is not catalog _v_p_i_u=/r/spi",
        ],
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(matrix, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
