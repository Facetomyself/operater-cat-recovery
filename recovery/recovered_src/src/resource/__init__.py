# Recovered module: src.resource
from __future__ import annotations

import os


_PACKAGE_ROOT = os.environ.get(
    "NUITKA_PACKAGE_src",
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)
RESOURCE_ROOT_DIR = os.path.join(_PACKAGE_ROOT, "resource")
