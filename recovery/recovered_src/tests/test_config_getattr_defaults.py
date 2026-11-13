from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Attributes whose value is a callable or a dynamic path; a literal fallback
# is intentional and not comparable to the config value.
ALLOWED = {
    ("YunYinMaoConfig", "is_support_multi"),
    ("YunYinMaoConfig", "abs_cache_only_multi_dir"),
}


def test_config_getattr_literal_defaults_match():
    from src.py.com.yun.mao.config import NewConfig, YunYinMaoConfig

    classes = {
        "YunYinMaoConfig": YunYinMaoConfig,
        "NewConfig": NewConfig,
    }
    mismatches = []
    for path in SRC.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "getattr":
                continue
            if len(node.args) < 3:
                continue
            owner, key, default = node.args[:3]
            if not isinstance(owner, ast.Name) or owner.id not in classes:
                continue
            if not isinstance(key, ast.Constant) or not isinstance(
                key.value, str
            ):
                continue
            if not isinstance(default, ast.Constant):
                continue
            if (owner.id, key.value) in ALLOWED:
                continue
            actual = getattr(classes[owner.id], key.value, None)
            if actual is None or callable(actual):
                continue
            if actual != default.value:
                mismatches.append(
                    (
                        str(path.relative_to(SRC)),
                        node.lineno,
                        owner.id,
                        key.value,
                        actual,
                        default.value,
                    )
                )
    assert mismatches == []
