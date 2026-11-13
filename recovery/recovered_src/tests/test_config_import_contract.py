from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def test_yunyinmaoconfig_is_a_module_not_a_class():
    from src.py.com.yun.mao.config import YunYinMaoConfig

    assert hasattr(YunYinMaoConfig, "abs_cache_dir")
    assert not hasattr(YunYinMaoConfig, "YunYinMaoConfig")


def test_no_source_imports_yunyinmaoconfig_from_its_own_module():
    bad = []
    for path in SRC.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if not (node.module or "").endswith("config.YunYinMaoConfig"):
                continue
            if any(alias.name == "YunYinMaoConfig" for alias in node.names):
                bad.append(
                    f"{path.relative_to(SRC)}:{node.lineno}"
                )
    assert bad == []
