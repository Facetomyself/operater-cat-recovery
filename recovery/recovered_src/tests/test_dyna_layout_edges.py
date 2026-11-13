from __future__ import annotations

import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
EDGES = PROJECT / "agent-notes" / "dyna_layout_edges.json"
UI_DIR = PROJECT / "recovered_src" / "src" / "resource" / "ui" / "dyna"


def test_generated_forms_keep_recovered_layout_edges():
    payload = json.loads(EDGES.read_text(encoding="utf-8"))
    for module in payload["modules"]:
        name = module["module"]
        if name == "yun_yin_mao_main":
            # The main window has a dedicated renderer and is covered by
            # test_main_window_ui.py; the edit forms use the edge tree.
            continue
        source = (UI_DIR / f"{name}.py").read_text(encoding="utf-8")
        for parent, child in module["widget_edges"]:
            assert (
                f"self.{parent}.addWidget(self.{child})" in source
            ), f"{name}: {parent} addWidget {child}"
        for parent, child in module["layout_edges"]:
            assert (
                f"self.{parent}.addLayout(self.{child})" in source
            ), f"{name}: {parent} addLayout {child}"
        for layout, parent in module["layout_parent"].items():
            assert (
                f"self.{parent}.setLayout(self.{layout})" in source
            ), f"{name}: {parent} setLayout {layout}"
        assert f"Form.setLayout(self.{module['root_layout']})" in source


def test_main_tree_constructor_types_are_recovered():
    payload = json.loads(EDGES.read_text(encoding="utf-8"))
    module = next(
        item for item in payload["modules"] if item["module"] == "yun_yin_mao_main"
    )
    classes = {}

    def walk(node):
        if node.get("kind") == "widget":
            classes[node["name"]] = node["class"]
        for child in node.get("children", []):
            walk(child)

    walk(module["tree"])
    assert classes["tabWidget_important"] == "QTabWidget"
    assert classes["text_brow_log"] == "QTextBrowser"
    assert classes["menubar"] == "QMenuBar"
    assert classes["action_reset"] == "QAction"
