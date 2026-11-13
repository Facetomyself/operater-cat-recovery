from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Literal fallbacks that are intentionally not part of the encoded catalog.
ALLOWED_MISSING = {"", "cloud item decode fail"}


def _sec_keys() -> set[str]:
    keys: set[str] = set()
    for path in SRC.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name):
                continue
            if node.func.id != "sec" or not node.args:
                continue
            value = node.args[0]
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                keys.add(value.value)
    return keys


def test_every_sec_key_resolves_to_a_catalog_message():
    from src.py.com.yun.mao.link import _fds_sj

    keys = _sec_keys()
    assert keys
    missing = keys - set(_fds_sj.SEC_MSGS) - ALLOWED_MISSING
    assert missing == set()
