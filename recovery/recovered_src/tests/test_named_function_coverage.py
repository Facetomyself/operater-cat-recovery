from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FUNCTION_MAP = ROOT.parent / "agent-notes" / "function_map_full.json"


def _source_file(module_name: str) -> Path | None:
    relative = module_name.replace(".", "/")
    if relative.startswith("src/"):
        relative = relative[4:]
    base = ROOT / "src" / relative
    for candidate in (base.with_suffix(".py"), base / "__init__.py"):
        if candidate.exists():
            return candidate
    return None


def test_named_function_map_has_no_source_gaps():
    payload = json.loads(FUNCTION_MAP.read_text(encoding="utf-8"))
    missing = []
    for module in payload["modules"]:
        names = [
            item["name"]
            for item in module.get("functions", [])
            if isinstance(item.get("name"), str)
            and not item["name"].startswith("__candidate")
        ]
        if not names:
            continue
        path = _source_file(module["module"])
        if path is None:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        defs = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }
        absent = [name for name in names if name not in defs]
        if absent:
            missing.append({"module": module["module"], "missing": absent})
    assert missing == []
