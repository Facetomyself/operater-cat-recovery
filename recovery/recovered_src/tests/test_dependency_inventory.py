from __future__ import annotations

import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS = ROOT / "requirements-recovered.txt"
INVENTORY = ROOT.parent / "agent-notes" / "dependency_inventory.json"
PYPROJECT = ROOT / "pyproject.toml"


def _requirement_names(path: Path) -> set[str]:
    names = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            names.add(line)
    return names


def test_runtime_dependency_sets_stay_in_sync():
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    inventory_names = set(inventory["third_party"])
    requirement_names = _requirement_names(REQUIREMENTS)
    pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    pyproject_names = set(
        pyproject["project"]["optional-dependencies"]["runtime"]
    )
    assert requirement_names == inventory_names
    assert pyproject_names == inventory_names
