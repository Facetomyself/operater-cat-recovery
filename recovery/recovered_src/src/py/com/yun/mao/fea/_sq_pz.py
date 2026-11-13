# Recovered module: src.py.com.yun.mao.fea._sq_pz
# Certificate-pin catalog helpers.
from __future__ import annotations

from ..link._fds_jm import sec


# The original catalog is assembled from an obfuscated configuration entry at
# runtime.  Keep the public container and normalization rules readable here;
# the encrypted host/fingerprint values are intentionally not guessed.
YC_ZW_HC_LB: list[tuple[str, str]] = []


def _normalize_hex(value: object) -> str:
    text = str(value or "").strip().upper().replace(":", "").replace(" ", "")
    return "".join(ch for ch in text if ch in "0123456789ABCDEF")


def a_r_zw_md(s_j_k_k_f_uck: str | None = None) -> None:
    """Decode one encrypted catalog seed into ``YC_ZW_HC_LB``.

    The exact binary seed is still pending; callers can pass an already
    decoded value for offline inspection without touching the target.
    """
    if not s_j_k_k_f_uck:
        try:
            s_j_k_k_f_uck = sec("s_j_k_k_f_uck")
        except Exception:
            return None
    for line in str(s_j_k_k_f_uck).replace("\r", "\n").split("\n"):
        line = line.strip()
        if not line:
            continue
        if "|" in line:
            host, fp = line.split("|", 1)
        elif "," in line:
            host, fp = line.split(",", 1)
        else:
            host, fp = line, ""
        if host:
            YC_ZW_HC_LB.append((host.strip(), _normalize_hex(fp)))
    return None


def cz_zw_hc_sj(md5s: list[str] | None = None):
    """Return the normalized pin list, optionally populated from ``md5s``."""
    if md5s:
        for item in md5s:
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                YC_ZW_HC_LB.append((str(item[0]), _normalize_hex(item[1])))
            else:
                YC_ZW_HC_LB.append((str(item), ""))
    return YC_ZW_HC_LB or None


def jx_zw_it_hf_x(md5s: list[str] | None = None) -> bool:
    """Validate that every supplied fingerprint is a hexadecimal digest."""
    for item in md5s or []:
        fp = _normalize_hex(item)
        if not fp or len(fp) not in (32, 40, 64):
            return False
    return True
