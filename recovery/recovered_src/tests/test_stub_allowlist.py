from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# These are fallback/no-op methods, not missing translations.  New entries
# must be reviewed deliberately.
ALLOWED_STUBS = {
    ("py/com/yun/mao/cd/TaskHardStop.py", "__init__"),
    ("py/com/yun/mao/log/glog.py", "__init__"),
    ("py/com/yun/mao/log/glog.py", "connect"),
    ("py/com/yun/mao/log/glog.py", "emit"),
    ("py/com/yun/mao/log/glog.py", "flush"),
    ("py/com/yun/mao/monitor/MonitorSchedulerReport.py", "quit"),
    ("py/com/yun/mao/util/XAIKeyValidator.py", "__init__"),
    ("py/com/yun/mao/util/need/signals.py", "__init__"),
}


def _is_stub(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    body = list(node.body)
    while body and isinstance(body[0], ast.Expr) and isinstance(
        body[0].value, ast.Constant
    ) and isinstance(body[0].value.value, str):
        body = body[1:]
    if len(body) != 1:
        return False
    stmt = body[0]
    return isinstance(stmt, ast.Pass) or (
        isinstance(stmt, ast.Raise)
        and isinstance(stmt.exc, ast.Call)
        and isinstance(stmt.exc.func, ast.Name)
        and stmt.exc.func.id == "NotImplementedError"
    )


def test_stub_functions_are_only_known_fallbacks():
    found = set()
    for path in SRC.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        relative = str(path.relative_to(SRC)).replace("\\", "/")
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and _is_stub(node):
                found.add((relative, node.name))
    assert found == ALLOWED_STUBS


def test_no_docstring_only_functions_remain():
    docstring_only = set()
    for path in SRC.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        relative = str(path.relative_to(SRC)).replace("\\", "/")
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            body = list(node.body)
            while body and isinstance(body[0], ast.Expr) and isinstance(
                body[0].value, ast.Constant
            ) and isinstance(body[0].value.value, str):
                body = body[1:]
            if not body:
                docstring_only.add((relative, node.name))
    assert docstring_only == set()
