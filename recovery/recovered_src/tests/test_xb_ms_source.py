from __future__ import annotations

import ast
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "py"
    / "com"
    / "yun"
    / "mao"
    / "link"
    / "_xb_ms.py"
)


def _function_source(name: str) -> str:
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return ast.unparse(node)
    raise AssertionError(f"missing function {name}")


def test_resolve_url_uses_so_origin_and_two_stage_validation():
    source = _function_source("_resolve_url")
    assert 'tw_hq_by_k(\'SO\')' in source
    assert source.count("validate(") == 2
    assert "dev=hj_dev_ok()" in source


def test_post_once_uses_sjk_public_key_helper():
    source = _function_source("_post_once")
    assert "TwCtx.tw_sjk_pk_pem()" in source
    assert "SjkCli._sjk_db_qq(" in source
    assert "sjk_zz_hb(" in source
    assert "SjkCli._sjk_jb_xy(" in source
