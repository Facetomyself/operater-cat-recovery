# Recovered module: src.py.com.yun.mao.link._sjk_bao
# Licence bootstrap request-body builder.
from __future__ import annotations

import json
import random

from ..util.need import utils


def _rand_en(n: int) -> str:
    try:
        return utils.generate_random_en(n)
    except Exception:
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(alphabet) for _ in range(n))


def _unit_name() -> str:
    try:
        return utils.gen_unit_name_by_ns()
    except Exception:
        return "J" + _rand_en(6)


def sjk_zz_hb(version: str, exe_hash: str) -> str:
    """Build the JSON metadata block used by the bootstrap request."""
    user_id = _rand_en(5)
    email = f"john.doe{random.randint(1, 10)}@gail.com"
    details = {
        "name": _unit_name(),
        "contact": {
            "email": email,
            "phone": f"+1-202-555-{random.randint(10, 99)}",
        },
        "address": {
            "street": "742 Evergreen Terrace",
            "city": "Springfield",
            "random": random.randint(1, 100),
            "metadata": {
                "lat": 39.7817,
                "lon": -89.6501,
                "hash": "sha256:" + (exe_hash or "")[:50],
                "pre": version,
                "fake": _rand_en(5),
                "n": _rand_en(6),
                "h": _rand_en(6),
                "uc_ns": _unit_name(),
                "tags": ["residential", "verified"],
            },
        },
    }
    return json.dumps(
        {
            "userInfo": {
                "userId": user_id,
                "details": details,
            }
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
