# 还原源码树

本目录是对 `运营猫 9.6.3` 中应用层 Python 模块的还原结果。

它**不是**原始源码，也**不能按原产品直接运行**：

- 357/357 个 loader 表中的应用/资源条目都有对应源码文件或包
  `__init__.py`。
- 当前有 368 个源文件；AST 统计为 3127 个函数、262 个类。
- 323 个模块至少包含一个真实函数体或类体。
- `module_index.json` 索引全部 357 个 loader 条目：315 个 body、31 个
  package、11 个 constants、0 个 empty。
- 离线测试套件当前为 102 个测试文件、455 个用例。
- 静态审计全部零发现，并已纳入 `validate_all.py`：源码覆盖、精确函数名、
  类方法、构造调用（含 dataclass 关键字）、tab/page UI 引用、静态 `.ui`
  引用、同类方法调用参数、`Q*` item-widget 引用、未定义名称、混淆签名
  和混淆 dispatch 覆盖。
- `MANIFEST.json` 记录每个源文件的 SHA-256、行数和模块名。
- `agent-notes/dyna_ui_text_inventory.json` 保存恢复出的 UI 文本池。
- `agent-notes/dyna_setupui_trees.json` 保存 ai_employee 布局树证据。
- 生成的 UI 运行时测试会用假 PyQt5 执行全部八个表单体，widget 属性回归
  会在离线阶段失败。
- 显式的 `NotImplementedError` / `class body not captured` 空壳已清除。
- `src.resource.ui.dyna` 包和八个生成表单模块由 Nuitka 常量与对话框
  widget 映射还原。
- 部分 UI/业务体仍是行为级推断；见 `COVERAGE.md` 和 `semantic/`。
- 关键协议路径已还原：授权上报、AES/RSA 信封、item 快照/dirty 生成、
  订单/迁移/激活回调以及 parse-plan 组装。
- 第三方依赖没有随仓库打包；`requirements-recovered.txt` 列出树中出现的
  import，`agent-notes/dependency_inventory.json` 记录哪些模块使用它们。
- 敏感值已脱敏，加密目录值不会复制进文档。

建议从这些文件开始：

- `OVERALL_LOGIC_AND_GAPS.md`：整体分层、主链路、已有文档盘点以及
  P0/P1/P2 缺口清单。
- `RECOVERY_NOTES.md`：覆盖范围、方法、置信度和后续步骤。
- `SOURCE_RECOVERY_PLAN.md`：剩余还原优先级。
- `agent-notes/function_map_full.json`：模块 init 引用与名称。
- `agent-notes/function_name_map_exact.json`：从 57 个模块 init 常量槽
  解析出的 492 个精确名称；`exact_function_coverage.json` 跟踪剩余源码缺口。
- `agent-notes/anti_debug_function_map.json`：已核实的反调试映射。
- `src/py/com/yun/mao/fea/_sq_jqm.py` 和 `_sq_chk.py`：卡密/授权模型。
- `src/py/com/yun/mao/link/_fds_sj.py`、`_fds_jm.py`、`_fds_h_x.py`、
  `_fdg_*.py`：反调试/解码/dispatch 源码。
- `decompiled/SqJqm_recovered.py`：还原的账号模型。
- `decompiled/license_flow_recovered.py`：还原的 `parse_report` /
  `hy_jx_bc` 字段流。
- `decompiled/anti_debug_map.md`：解码后的反调试列表与响应层级。
- `decompiled/c_pseudocode/`：作为证据的原始 Hex-Rays 输出。
- `semantic/`：领域模型、授权/订单/解析流程、auto/monitor/telefast
  流水线、混淆包边界、UI 还原与工程说明。
- `tests/`：加密原语、dclass 快照、payload 契约、parse builder、纯模块
  import 和 UI widget map 的离线 pytest 检查。当前为 455 个用例。
- `sanitized/`：可选的卡密/恶意逻辑无害化层，详见
  `semantic/card-key-analysis.md` 与 `semantic/malicious-logic-analysis.md`。

在本目录运行：

```powershell
python -m compileall -q src
python -m pytest -q
```

完整门禁（编译、测试、统计、索引、覆盖率和依赖审计）请在工作区根目录运行
`_re/validate_all.py`。

不要运行原始目标，也不要让本源码树去连接原始目标。二进制带有反调试路径，
会调用 `shutdown.exe`。
