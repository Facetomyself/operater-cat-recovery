# 主窗口 UI 恢复

范围：`src.resource.ui.dyna.yun_yin_mao_main`

使用的输入：

- `agent-notes/dyna_layout_edges.json`
- `agent-notes/dyna_ui_constants.json`
- `agent-notes/dyna_retranslate_pairs.json`
- `agent-notes/decompiled/targets/0x66a6e30_dyna_yun_yin_mao_main_init.c`
- `agent-notes/decompiled/targets/0x6689710_dyna_main_retranslateUi.c`
- `recovered_src/tests/test_main_window_ui.py`
- `recovered_src/tests/test_dyna_layout_edges.py`

## 证据摘要

- 从构造函数常量恢复出 161 个 widget 节点。
- 150 条 `addWidget` 边。
- 56 条 `addLayout` 边。
- 4 个标签页：`gen_session`、`tab`、`tools`、`api_fun`。
- 1 个滚动关系：`scrollArea -> scrollAreaWidgetContents`。
- `centralwidget` 拥有根布局 `verticalLayout_2`。
- 从 retranslate 函数恢复出 143 个文本三元组以及 4 个 `setTabText`
  三元组。

## 恢复后的结构

- `MainWindow -> centralwidget -> verticalLayout_2 -> verticalLayout`
- `verticalLayout_top`：头部标签、权限按钮、代理控件。
- `verticalLayout_mid`：`tabWidget_important`。
- `verticalLayout_bottom`：日志按钮和 `text_brow_log`。
- 标签页与标签：
  - `gen_session`: 账号功能
  - `tab`: 自动运营
  - `tools`: 工具箱
  - `api_fun`: API功能
- `tabWidget_important` 恢复 `setCurrentIndex(1)`。
- `tabWidget_important` 恢复 `setCurrentIndex(1)`。
- `monitor_container` 保留嵌套的 `scrollArea` /
  `scrollAreaWidgetContents` 关系。
- 菜单标题为 菜单；动作包括 重置运营猫、开发者中心、分隔符、
  复制机器码。`menu_operation` 作为恢复出的 `menu` 的兼容别名保留。

## 生成器行为

`_re/generate_dyna_ui_modules.py` 现在有两条路径：

- `render_main_from_tree`：当 `dyna_layout_edges.json` 包含主窗口构造图时
  使用。它会拆出特殊节点（`centralwidget`、标签页、滚动内容、菜单/动作），
  在发出 `addWidget`、`addLayout`、`addTab` 和 `setWidget` 调用前重建
  真实的 Qt 所有权树。
- `render_main`：作为没有布局证据环境下的回退路径保留。

`_re/extract_retranslate_pairs.py` 捕获 `setTabText(indexOf(page), text)`
模式，因此标签页标签与其余 UI 文本使用同一份 retranslate 证据。

## 验证

- `387 passed`
- `validate_all.py` 通过
- 加载器 `357/357`
- 精确函数 `492/492`
- 类方法 `1167/1167`

## 暂缓缺口

- `click_action_reset` 现在打开 `ResetBirdDialog`；`on_program_suspected_frozen`
  中的冻结恢复路径现在启动 `kai_shit_f_m_5s`。
- `bz_uc`、`kv_nx`、`rm_qh`、`wp_jt` 以及隐藏命令链中的深层分派/操作数
  顺序，暂缓到恶意逻辑阶段处理。
- `tests/test_stub_allowlist.py` 中的 8 个条目是有记录的 fallback
  no-op，不是缺失的 UI 翻译。
