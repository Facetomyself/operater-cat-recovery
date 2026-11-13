# UI 资源重建

## 范围

发行包为列表项 widget 和少量对话框提供了 `ui/static/*.ui`，但没有提供以下
模块的 Qt Designer 源文件：

- `src.resource.ui.dyna.ai_employee_item`
- `src.resource.ui.dyna.auto_flow_item`
- `src.resource.ui.dyna.ban_yun_flow_comment_item`
- `src.resource.ui.dyna.down_load_flow_item`
- `src.resource.ui.dyna.yulan_flow_item`
- `src.resource.ui.dyna.yun_auto_item`
- `src.resource.ui.dyna.yun_preview_item`
- `src.resource.ui.dyna.yun_yin_mao_main`

对话框类仍会导入这些模块并调用 `Ui_Form().setupUi()`。
如果这些模块缺失，每个编辑对话框都会被迫使用程序化回退方案。

## 证据

- `agent-notes/nuitka_module_table.json` 包含九个 loader 条目及其 init RVA。
- `agent-notes/dyna_ui_constants.json` 从 Nuitka constants blob
  （`0x8A7A158`，大小 `0x11C023B`）解码而来。它保留 Qt 类名、对象名、
  顶层 `resize` 元组、样式表和 retranslate 字符串池。
- 每个 `Edit*Dialog.py` 类都带有自己的 `UI_MODULE` 和 `WIDGET_NAMES`。
  生成的 form 模块将该契约作为权威 widget 列表。
- `ui/static/q_*_widget.ui` 仍是列表项 widget 的权威来源；它与编辑表单
  相互独立。

## 重建

- `_re/decode_dyna_ui.py` 解码此前 constants 扫描过滤掉的
  `src.resource.ui.dyna.*` chunk。
- `_re/generate_dyna_ui_modules.py` 生成九个 Python 模块。
- Widget 名称是精确的。Widget 类由对话框使用映射和 Qt 命名惯例推断。
- `_re/extract_dyna_layout.py` 扫描每个大型 `setupUi` 函数，并读取指向
  模块常量池的有序 qword 引用。它恢复真实的 `addWidget` 和 `addLayout`
  边（每个大型表单有 100+ 个 widget 边）以及布局到 widget 的
  `setLayout` 父级。
- 表单生成器现在为七个编辑表单输出已恢复的嵌套布局树。在 setup 池中
  没有创建调用时，`text_model` 和 `number_model` 会作为尾部兼容 widget
  保留。
- `_re/extract_dyna_layout.py` 还会从有序常量引用中恢复 `setMinimumSize` /
  `setMaximumSize` 对；生成器将它们输出为 `_SIZE_CONSTRAINTS`，并在
  `_make_widget` 中应用。
- Designer 几何、字体度量、spacer 和 tab 顺序仍不在声明范围内；
  已恢复的结构是 widget/布局层级。
- `yun_yin_mao_main.Ui_MainWindow` 重建 `MainWindow` 使用的主窗口界面：
  顶部状态行、`tabWidget_important`、`text_brow_log`、日志按钮、
  标识符字段、菜单栏以及重置/复制操作。

## 限制

- 仅凭去重后的 Nuitka 常量池，无法恢复精确的 Designer XML、绝对
  `setGeometry` 矩形、spacer 几何、字体度量和 tab 顺序。已恢复的每个
  widget 最小/最大尺寸约束会输出，但它们不能替代绝对几何。
- `auto_flow_item` constants chunk 有 679 个值，但没有任何
  `setGeometry` 条目；其他大型编辑表单也是同样模式。因此几何并不藏在
  常量池中——它位于 Hex-Rays 无法反编译的超大 `setupUi` 函数体内。
- `auto_flow_item` init 将 `sub_14622C360` 传给
  `Nuitka_Function_New` 用于 `setupUi`，将 `sub_1462B3E90` 传给
  `retranslateUi`。静态镜像中 `setupUi` 的 pdata 范围为
  `0x87b2a`，Hex-Rays 在该范围失败；因此生成的 form 使用常量顺序重建，
  而不宣称函数体逐字节一致。
- radare2 `pdc` 可以反汇编同一函数，并确认开头的常量序列
  （`resize`、`QtGui/QFont`、`setStyleSheet`），但输出是 3000+ 行
  底层伪 C，包含 616 个返回点，不能作为可用的 Python 源码重建。
- `ai_employee_item.setupUi`（0x61B9C20）确实成功反编译（12,071 行，
  511 个 qword 引用）。`agent-notes/dyna_setupui_trees.json` 现在保存
  其恢复后的布局树。生成的 `ai_employee_item` form 现在使用该嵌套布局树；
  对话框契约中的五个旧 `label_em_*` 名称会作为隐藏兼容 widget 输出。
  七个大型 form 使用 `agent-notes/dyna_layout_edges.json`，并由
  fake-Qt 运行时测试验证。

### setupUi 反编译状态

| 模块 | setupUi RVA | IDA 范围 | Hex-Rays |
| --- | --- | ---: | --- |
| `ai_employee_item` | `0x61B9C20` | `0xDDAB` | OK，布局树已恢复 |
| `auto_flow_item` | `0x622C360` | `0x87B2A` | 失败 |
| `ban_yun_flow_comment_item` | `0x62C27C0` | `0x69303` | 失败 |
| `down_load_flow_item` | `0x63371A0` | `0x2D20B` | 失败 |
| `yulan_flow_item` | `0x6371140` | `0x80CB3` | 失败 |
| `yun_auto_item` | `0x6400140` | `0x94CDD` | 失败 |
| `yun_preview_item` | `0x64A6D10` | `0x80383` | 失败 |
| `yun_yin_mao_main` | `0x6534AE0` | `0x154C2E` | 失败 |

这些失败是反编译器在已恢复静态镜像上的容量问题（`MERR_FUNCSIZE`），
并非缺少函数指针。布局边提取器直接基于指令常量引用工作，绕过反编译器
限制；主窗口保留其专用的行为级渲染器。
- `retranslateUi` 保留已恢复的窗口标题契约，但不宣称精确标签位置。
  对话框字段默认值和 combo 项由对话框 mixin 在运行时填充。
- 捆绑的 `PyQt5` 扩展模块面向原始内嵌 Python。离线套件使用 AST 契约
  校验类型映射和文本池，并针对最小 fake `PyQt5` 模块执行每个生成的
  `setupUi`。

## 验证

- `recovered_src/tests/test_dyna_ui_modules.py` 检查全部九个模块、
  `Ui_Form`/`Ui_MainWindow` 类、`setupUi`/`retranslateUi`，以及针对每个
  对话框 `WIDGET_NAMES` 的精确 `_TYPE_MAP` 覆盖。
- `_re/audit_source_coverage.py` 写入
  `agent-notes/source_recovery_audit.json`；报告 `357/357` 个 loader 条目
  存在，`9/9` 个 dyna 模块存在。
- `tests/test_dyna_ui_runtime_stub.py` 导入全部八个 form 模块，并使用
  fake Qt 模块运行 `setupUi`，在不启动 Qt 的情况下捕获缺失属性名和
  无效的生成调用序列。
- `tests/test_dyna_layout_edges.py` 固定七个编辑表单中每个已恢复的
  `addWidget`、`addLayout` 和布局 `setLayout` 边。
