from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT.parent / "agent-notes" / "dyna_ui_text_inventory.json"


def test_ui_text_inventory_covers_all_dyna_forms():
    payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    assert payload["schema"] == "operater-cat-dyna-ui-text-inventory.v1"
    assert payload["module_count"] == 8
    names = {module["module"] for module in payload["modules"]}
    assert len(names) == 8
    assert all(
        module["entry_count"] > 0
        for module in payload["modules"]
    )
    for module in payload["modules"]:
        assert module["window_title"]
        assert module["text_entries"]
