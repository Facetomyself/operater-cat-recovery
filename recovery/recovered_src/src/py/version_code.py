# Recovered module: src.py.version_code
# Small build-version gate used by both the bootstrap client and the
# encrypted configuration layer.
from __future__ import annotations


version_code = "9.6.3"


def is_dev_version() -> bool:
    text = str(version_code).lower()
    return "dev" in text or "debug" in text or text.endswith("-d")


def is_prod_version() -> bool:
    return not is_dev_version()
