from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"


def test_manifest_hashes_match_current_sources():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert payload["schema"] == "operater-cat-source-manifest.v1"
    assert payload["file_count"] == len(payload["files"])
    assert payload["file_count"] > 0
    for record in payload["files"]:
        path = ROOT / record["path"]
        raw = path.read_bytes()
        assert record["bytes"] == len(raw)
        assert record["lines"] == len(raw.decode("utf-8", "replace").splitlines())
        assert record["sha256"] == hashlib.sha256(raw).hexdigest()
