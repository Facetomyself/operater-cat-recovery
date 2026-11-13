#!/usr/bin/env python3
"""Verify the copied handoff bundle without touching the original project."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(label: str, args: list[str], cwd: Path) -> None:
    print(f"=== {label} ===")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(args, cwd=cwd, env=env)
    if result.returncode != 0:
        raise SystemExit(f"{label} failed with exit {result.returncode}")


def main() -> int:
    run(
        "offline pytest",
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
        ],
        ROOT / "recovered_src",
    )
    run(
        "offline protocol lab",
        [sys.executable, "run_lab.py"],
        ROOT / "offline_protocol_lab",
    )
    print("bundle verification OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
