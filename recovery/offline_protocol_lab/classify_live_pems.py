#!/usr/bin/env python3
"""Classify PEMs dumped from the live guest RAM against the bootstrap init key.

Offline only. Does not print PEM bodies. Does not touch the network.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

from cryptography.hazmat.primitives import serialization

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
PEM_DIR = LIVE_DIR / "pems"
SECRETS = PROJECT_DIR / "_re" / "runtime_secrets.txt"
OUTPUT = LIVE_DIR / "pems" / "classify.json"


def _fp(pem: bytes) -> tuple[int, str]:
    key = serialization.load_pem_public_key(pem)
    der = key.public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return key.key_size, hashlib.sha256(der).hexdigest()


def _bootstrap_fp() -> str:
    text = SECRETS.read_text(encoding="utf-8", errors="replace")
    match = re.search(
        r"tw_sjk_pk_pem = ('-----BEGIN PUBLIC KEY-----.*-----END PUBLIC KEY-----')",
        text,
        re.S,
    )
    if not match:
        raise SystemExit("bootstrap pem missing from runtime_secrets.txt")
    _, digest = _fp(ast.literal_eval(match.group(1)).encode())
    return digest


def main() -> int:
    boot = _bootstrap_fp()
    rows = []
    for path in sorted(PEM_DIR.glob("pk_*.pem")):
        raw = path.read_bytes()
        parts = re.findall(
            br"-----BEGIN PUBLIC KEY-----.*?-----END PUBLIC KEY-----",
            raw,
            re.S,
        )
        if not parts:
            rows.append({"file": path.name, "ok": False, "error": "no-pem"})
            continue
        for index, pem in enumerate(parts, 1):
            try:
                bits, digest = _fp(pem)
            except Exception as exc:
                rows.append(
                    {
                        "file": path.name,
                        "part": index,
                        "ok": False,
                        "error": type(exc).__name__,
                    }
                )
                continue
            rows.append(
                {
                    "file": path.name,
                    "part": index,
                    "ok": True,
                    "bits": bits,
                    "fp16": digest[:16],
                    "role": "bootstrap_init" if digest == boot else "catalog_candidate",
                }
            )
    payload = {
        "bootstrap_fp16": boot[:16],
        "keys": rows,
        "unique_roles": sorted({row["role"] for row in rows if row.get("ok")}),
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
