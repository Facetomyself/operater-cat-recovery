# Recovered module: src.py.com.yun.mao.util.need.FileUtils
from __future__ import annotations

from pathlib import Path


def read_line(path: str | Path, at_name: str = "") -> str:
    try:
        with open(path, "r", encoding="utf-8") as file:
            line = file.readline().strip()
        if at_name and at_name in line:
            return line.split(at_name, 1)[-1]
        return line
    except Exception:
        return ""


def truncate_string(s: str, length: int = 10) -> str:
    text = str(s or "")
    return text if len(text) <= length else text[:length] + "..."
