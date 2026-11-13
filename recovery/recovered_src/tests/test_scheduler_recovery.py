from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/py/com/yun/mao/mthread/SchedulerThreadClass.py"


def test_my_job_calls_recovered_fs_by_pf_probe():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    my_job = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "my_job"
    )

    imported = {
        alias.name
        for node in ast.walk(my_job)
        if isinstance(node, ast.ImportFrom)
        and node.level == 2
        and node.module == "link._fds_rt"
        for alias in node.names
    }
    calls = {
        node.func.id
        for node in ast.walk(my_job)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
    }

    assert "fs_by_pf" in imported
    assert "fs_by_pf" in calls
