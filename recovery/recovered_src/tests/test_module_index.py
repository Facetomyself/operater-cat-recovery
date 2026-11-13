from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "module_index.json"


def test_module_index_is_complete():
    payload = json.loads(INDEX.read_text(encoding="utf-8"))
    assert payload["schema"] == "operater-cat-module-index.v2"
    assert payload["entry_count"] == 357
    assert payload["empty_count"] == 0
    assert (
        payload["body_count"]
        + payload["package_count"]
        + payload["constant_count"]
        == payload["entry_count"]
    )


def test_module_index_files_exist():
    payload = json.loads(INDEX.read_text(encoding="utf-8"))
    for record in payload["modules"]:
        assert record["file"] is not None
        assert (ROOT / record["file"]).exists()
