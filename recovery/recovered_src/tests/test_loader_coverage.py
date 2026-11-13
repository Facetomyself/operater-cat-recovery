from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_NOTES = ROOT.parent / "agent-notes"
TABLE = AGENT_NOTES / "nuitka_module_table.json"
AUDIT = AGENT_NOTES / "source_recovery_audit.json"


def _source_file(module_name: str) -> Path | None:
    relative = module_name.replace(".", "/")
    if relative.startswith("src/"):
        relative = relative[4:]
    base = ROOT / "src" / relative
    for candidate in (base.with_suffix(".py"), base / "__init__.py"):
        if candidate.exists():
            return candidate
    return None


def test_every_loader_entry_has_a_source_file():
    table = json.loads(TABLE.read_text(encoding="utf-8"))
    names = [
        entry["name"]
        for entry in table["entries"]
        if entry["name"] == "src.py.com.yun.mao"
        or entry["name"].startswith("src.py.com.yun.mao.")
        or entry["name"] == "src.resource"
        or entry["name"].startswith("src.resource.")
    ]
    assert len(names) == 357
    assert [name for name in names if _source_file(name) is None] == []


def test_source_recovery_audit_flags_are_complete():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["loader_entries_complete"] is True
    assert audit["dyna_modules_complete"] is True
    assert audit["modules_with_refs_but_no_functions"] == []
