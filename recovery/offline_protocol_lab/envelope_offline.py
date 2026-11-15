#!/usr/bin/env python3
"""Offline envelope + URL assembly using the live catalog. No network."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.parse import urljoin

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding

LAB_DIR = Path(__file__).resolve().parent

def _project_and_live() -> tuple[Path, Path]:
    here = LAB_DIR
    candidates = [
        here.parent.parent / "live",
        here.parent / "capture_lab",
        here.parent.parent / "capture_lab",
    ]
    for live in candidates:
        if (live / "catalog_named_plain.json").exists() or (live / "catalog_named_summary.json").exists():
            project = here.parent if (here.parent / "recovered_src").exists() else here.parent
            if not (project / "recovered_src").exists() and (here.parent / "recovered_src").exists():
                project = here.parent
            if (here.parent / "recovered_src").exists():
                project = here.parent
            elif (here.parent.parent / "recovery" / "recovered_src").exists():
                project = here.parent.parent / "recovery"
            return project, live
    raise SystemExit("live catalog not found; expected live/ or capture_lab/")

PROJECT_DIR, LIVE_DIR = _project_and_live()
RECOVERED_DIR = PROJECT_DIR / "recovered_src"
PLAIN = LIVE_DIR / "catalog_named_plain.json"
OUTPUT = LIVE_DIR / "envelope_offline.json"

if str(RECOVERED_DIR) not in sys.path:
    sys.path.insert(0, str(RECOVERED_DIR))


def main() -> int:
    from src.py.com.yun.mao.sanitized import neutralize

    neutralize.apply()
    catalog = json.loads(PLAIN.read_text(encoding="utf-8"))

    from src.py.com.yun.mao.link import _tw_ctx
    from src.py.com.yun.mao.jm import _my_gk, _my_r_gk, _my_util
    from src.py.com.yun.mao.fea import _sq_req

    def fake_hq(name: str) -> str:
        if name not in catalog:
            raise KeyError(name)
        return catalog[name]

    _tw_ctx.TwCtx.tw_hq_by_k = classmethod(lambda cls, name: fake_hq(name))

    origin = catalog["_p_dh"].rstrip("/")
    catalog_urls = {
        "spi": urljoin(origin + "/", catalog["_v_p_i_u"].lstrip("/")),
        "spui": urljoin(origin + "/", catalog["_v_ps_i_u"].lstrip("/")),
        "ui": urljoin(origin + "/", catalog["_v_u_i_u"].lstrip("/")),
        "roi": urljoin(origin + "/", catalog["_v_r_p_i_u"].lstrip("/")),
        "ca": urljoin(origin + "/", catalog["_v_s_c_i_u"].lstrip("/")),
        "fms": urljoin(origin + "/", catalog["_v_s_f_ms"].lstrip("/")),
        "register": urljoin(origin + "/", catalog["_r_u"].lstrip("/")),
        "experience": urljoin(origin + "/", catalog["_s_ac_u"].lstrip("/")),
    }
    recovered_literals = {
        "spi": origin + "/r_spi",
        "spui": origin + "/r_spui",
        "ui": origin + "/r_ui",
        "roi": origin + "/r_roi",
        "ca": origin + "/r_ca",
    }

    f_pk = _my_gk.jm_jz_gy_pk()
    r_pk = _my_r_gk.jm_jz_r_pk()
    aes_key = os.urandom(16)
    body = json.dumps({"lab": True, "uCode": "LAB-UCODE"}, separators=(",", ":"))
    ciphertext = _sq_req.sq_sc_aq_nr(body, aes_key)
    wrapped = _sq_req.sq_sc_aes_k(aes_key)
    roundtrip = _my_util.aes_decrypt(ciphertext, aes_key)
    envelope = {
        "v1c": ciphertext.hex(),
        "v2k": wrapped.hex(),
    }

    # Prove _f_pk encrypts 16-byte keys; private unwrap is impossible here.
    unwrapped_len = len(wrapped)

    # Sign/verify with a throwaway key to prove jm_yq_qm wiring, then show
    # catalog keys reject that signature (expected).
    priv_pem, pub_pem = _my_util.generate_rsa_keys()
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

    priv = load_pem_private_key(priv_pem, password=None)
    message = ciphertext
    sig = priv.sign(message, asymmetric_padding.PKCS1v15(), hashes.SHA256())
    verify_lab = _my_util.jm_yq_qm(pub_pem, message, sig)
    verify_f = _my_util.jm_yq_qm(f_pk, message, sig)
    verify_r = _my_util.jm_yq_qm(r_pk, message, sig)

    payload = {
        "network": "not-used",
        "origin": origin,
        "catalog_urls": catalog_urls,
        "recovered_literal_urls": recovered_literals,
        "url_delta": {
            key: {
                "catalog": catalog_urls[key],
                "recovered_literal": recovered_literals[key],
                "same": catalog_urls[key] == recovered_literals[key],
            }
            for key in recovered_literals
        },
        "envelope": {
            "v1c_bytes": len(ciphertext),
            "v2k_bytes": unwrapped_len,
            "aes_roundtrip_ok": roundtrip == body,
            "v1c_hex_prefix": envelope["v1c"][:16],
            "v2k_hex_prefix": envelope["v2k"][:16],
        },
        "keys": {
            "f_pk_loaded": True,
            "r_pk_loaded": True,
            "lab_self_sign_verifies": verify_lab,
            "catalog_f_pk_rejects_lab_sig": verify_f is False,
            "catalog_r_pk_rejects_lab_sig": verify_r is False,
        },
        "note": "v2k is RSA-PKCS1v15(_f_pk, aes_key). Cannot unwrap without server private key.",
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    neutralize.restore()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
