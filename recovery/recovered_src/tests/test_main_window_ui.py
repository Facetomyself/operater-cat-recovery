from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "src" / "resource" / "ui" / "dyna" / "yun_yin_mao_main.py"
MAIN_WINDOW = ROOT / "src" / "py" / "com" / "yun" / "mao" / "MainWindow.py"


def _method(tree: ast.Module, name: str) -> ast.FunctionDef:
    cls = next(
        node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Ui_MainWindow"
    )
    return next(
        node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == name
    )


def test_main_window_adds_gen_session_tab():
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    setup = _method(tree, "setupUi")
    assigned = {
        node.targets[0].attr
        for node in ast.walk(setup)
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Attribute)
        and isinstance(node.targets[0].value, ast.Name)
        and node.targets[0].value.id == "self"
    }
    assert "gen_session" in assigned
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "addTab"
        for node in ast.walk(setup)
    )


def test_main_window_sets_account_tab_text():
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    retranslate = _method(tree, "retranslateUi")
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "setTabText"
        and any(
            isinstance(arg, ast.Constant) and arg.value == "账号功能"
            for arg in ast.walk(node)
        )
        for node in ast.walk(retranslate)
    )


def test_main_window_keeps_recovered_constructor_graph():
    payload = json.loads(
        (ROOT.parent / "agent-notes" / "dyna_layout_edges.json").read_text(
            encoding="utf-8"
        )
    )
    module = next(
        item for item in payload["modules"] if item["module"] == "yun_yin_mao_main"
    )
    source = MODULE.read_text(encoding="utf-8")
    for parent, child in module["widget_edges"]:
        assert f"self.{parent}.addWidget(self.{child})" in source
    for parent, child in module["layout_edges"]:
        assert f"self.{parent}.addLayout(self.{child})" in source
    for parent, child in module["tab_edges"]:
        assert f"self.{parent}.addTab(self.{child}, '')" in source
    for parent, child in module["scroll_edges"]:
        assert f"self.{parent}.setWidget(self.{child})" in source
    assert "self.centralwidget.setLayout(self.verticalLayout_2)" in source
    assert "MainWindow.setCentralWidget(self.centralwidget)" in source
    assert "MainWindow.setMenuBar(self.menubar)" in source
    assert "self.menu_operation = self.menu" in source

    tree = ast.parse(source)
    setup = _method(tree, "setupUi")
    assigned = [
        node.targets[0].attr
        for node in ast.walk(setup)
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Attribute)
        and isinstance(node.targets[0].value, ast.Name)
        and node.targets[0].value.id == "self"
    ]
    assert assigned.count("centralwidget") == 1
    assert assigned.count("tabWidget_important") == 1
    assert assigned.count("gen_session") == 1


def test_main_window_exposes_recovered_foreground_helper():
    tree = ast.parse(MAIN_WINDOW.read_text(encoding="utf-8"))
    functions = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    assert "bring_window_to_front" in functions
    method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.name == "_bring_main_window_to_front"
    )
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "bring_window_to_front"
        for node in ast.walk(method)
    )


def test_main_window_wires_the_four_core_tab_controllers():
    tree = ast.parse(MAIN_WINDOW.read_text(encoding="utf-8"))
    method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "init_view"
    )
    calls = {
        (node.func.id, ast.unparse(node.args[1]) if len(node.args) > 1 else "")
        for node in ast.walk(method)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and len(node.args) >= 2
    }
    assert ("SessionFunTab", "self.ui.gen_session") in calls
    assert ("AutoYunYinTab", "self.ui.tab") in calls
    assert ("ToolBoxTab", "self.ui.tools") in calls
    assert ("ApiConfigTab", "self.ui.api_fun") in calls
    registered = {
        node.targets[0].slice.value: node.value.attr
        for node in ast.walk(method)
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Subscript)
        and isinstance(node.targets[0].value, ast.Attribute)
        and node.targets[0].value.attr == "tab_controllers"
        and isinstance(node.targets[0].slice, ast.Constant)
        and isinstance(node.value, ast.Attribute)
    }
    assert registered["账号功能"] == "session_fun_tab"
    assert registered["自动运营"] == "auto_yun_yin_tab"
    assert registered["工具箱"] == "app_toolbox_tab"
    assert registered["API功能"] == "app_config_tab"


def test_main_window_loads_controller_tabs_into_qwidget_pages():
    tree = ast.parse(MAIN_WINDOW.read_text(encoding="utf-8"))
    method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "_add_controller_tab"
    )
    calls = [node for node in ast.walk(method) if isinstance(node, ast.Call)]
    assert any(
        isinstance(call.func, ast.Name) and call.func.id == "QWidget"
        for call in calls
    )
    assert any(
        isinstance(call.func, ast.Attribute)
        and call.func.attr == "loadUi"
        for call in calls
    )
    assert any(
        isinstance(call.func, ast.Attribute)
        and call.func.attr == "addTab"
        for call in calls
    )


def test_main_window_uses_recovered_instance_id_for_single_instance_server():
    tree = ast.parse(MAIN_WINDOW.read_text(encoding="utf-8"))
    source = MAIN_WINDOW.read_text(encoding="utf-8")
    assert "CMCode.r_instance_id()" in source
    assert "self.server_name = f\"{self.soft_name}_{CMCode.r_instance_id()}\"" in source
    setup = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "setup_single_instance"
    )
    assert any(
        isinstance(node, ast.Attribute)
        and node.attr == "server_name"
        and isinstance(node.value, ast.Name)
        and node.value.id == "self"
        for node in ast.walk(setup)
    )


def test_main_window_uses_recovered_biao_shi_cache_group_and_task_guard():
    source = MAIN_WINDOW.read_text(encoding="utf-8")
    assert 'cache.read_cache(TEXT_BIAO_SHI, TEXT_BIAO_SHI_text, "")' in source
    assert "TEXT_BIAO_SHI, TEXT_BIAO_SHI_text, str(text)" in source
    assert "if Working.Session_Working:" in source


def test_main_window_uses_tip_dialog_constructor_contract():
    tree = ast.parse(MAIN_WINDOW.read_text(encoding="utf-8"))
    methods = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    }
    for name in ("showTipDialog", "showTipDialogBySize", "showTipDialogByRestart"):
        method = methods[name]
        assert not any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "setText"
            for node in ast.walk(method)
        )
    restart = methods["showTipDialogByRestart"]
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "TipDialog"
        and any(keyword.arg == "restart" for keyword in node.keywords)
        for node in ast.walk(restart)
    )


def test_main_window_uses_mini_tip_close_callbacks():
    tree = ast.parse(MAIN_WINDOW.read_text(encoding="utf-8"))
    method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "show_message_box"
    )
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "MiniTipDialog"
        and len(node.args) == 4
        for node in ast.walk(method)
    )
    source = ast.get_source_segment(MAIN_WINDOW.read_text(encoding="utf-8"), method)
    assert "final_quit()" in source
    assert "pause_ui_log()" in source


def test_main_window_traces_ui_initialization_failures():
    source = MAIN_WINDOW.read_text(encoding="utf-8")
    assert 'print("创建服务器或初始化时出错: ")' in source
    assert "TracePrinterHelper.print_trace()" in source
    assert "self.glog.frozeDetected.connect(self._froze_connected)" in source


def test_main_window_final_quit_stops_auto_tasks():
    source = MAIN_WINDOW.read_text(encoding="utf-8")
    assert "self.auto_yun_yin_tab.final_stop_quit()" in source
    assert 'self.glog.write("异常引发强制停止任务\\n")' in source
    assert "self.session_fun_tab.gen_session_queue.send_stop_send()" in source


def test_dirty_item_save_uses_async_callback_and_loading_close_permission():
    source = MAIN_WINDOW.read_text(encoding="utf-8")
    assert 'LoadingDialog(self, "进行合法性校验，请稍候...")' in source
    assert "save_fun(after)" in source
    assert "loading.allow_close()" in source
    assert "after(False)" in source


def test_bring_main_window_to_front_guards_the_gui_thread():
    source = MAIN_WINDOW.read_text(encoding="utf-8")
    assert "QThread.currentThread() is not app_thread" in source
    assert "QCoreApplication.instance().thread()" in source


def test_click_action_reset_opens_reset_bird_dialog():
    tree = ast.parse(MAIN_WINDOW.read_text(encoding="utf-8"))
    method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "click_action_reset"
    )
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "ResetBirdDialog"
        and len(node.args) == 1
        and isinstance(node.args[0], ast.Name)
        and node.args[0].id == "self"
        for node in ast.walk(method)
    )
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "exec"
        for node in ast.walk(method)
    )


def test_program_suspected_frozen_runs_xb_probe_with_exception_print():
    source = MAIN_WINDOW.read_text(encoding="utf-8")
    tree = ast.parse(source)
    method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.name == "on_program_suspected_frozen"
    )
    segment = ast.get_source_segment(source, method)
    assert "self.re_try_fetch_zw_t.start(500)" in segment
    assert "kai_shit_f_m_5s()" in segment
    assert "except Exception as e:" in segment
    assert "print(e)" in segment
