# 工程层

## 用途

恢复出的代码组织成常规 Python 源码树，便于阅读、diff 和离线测试。它不是
原始 Nuitka 启动器的重建，也不包含第三方运行时。

## 测试命令

在 `recovered_src` 下运行：

```powershell
python -m pytest -q
```

从工作区根目录执行单命令验证：

```powershell
D:\reverse_ENV\.venv\Scripts\python.exe D:\reverse_ENV\workspace\operater-cat\_re\validate_all.py
```

它会运行 `compileall`、dyna 布局边提取器、UI 模块生成器、源码清单、pytest、
源码统计、模块索引重建、源码覆盖审计和依赖审计，然后断言索引/审计不变量。

测试覆盖：

- AES/RSA 原语往返；
- `ItemMemStore` 脏代际和快照行为；
- `SqJqm`/`RemoteHb`/载荷字段契约；
- 解析摘要和计划组装的纯函数。
- 未安装 PyQt5/Telethon 时的纯模块导入冒烟测试；
- UI `Ui_Form`/`Ui_MainWindow` widget 映射契约。
- 所有八个生成的 `setupUi` 函数体的 fake-PyQt5 执行，包括嵌套布局挂载，
  且不加载打包的 Qt 扩展；
- 七个大型编辑表单的恢复 `addWidget`/`addLayout` 边覆盖。

没有测试会调用网络、启动 PyQt、执行 shell 命令或加载原始可执行文件。
`pytest -q` 当前报告来自 102 个文件的 455 个用例。

## 依赖清单

- `requirements-recovered.txt` 列出恢复树导入的第三方包。版本未恢复。
- `pyproject.toml` 暴露 `runtime` 和 `test` 可选依赖组；
  `requirements-dev.txt` 包含仅测试依赖。
- `tests/test_dependency_inventory.py` 保持 requirements 文件、依赖清单和
  `pyproject.toml` runtime 组同步。
- `_re/audit_constructor_calls.py` 根据显式 `__init__` 参数数量检查直接实例化
  的导入类，解析继承的 dataclass 字段并校验 dataclass 关键字名；它写入
  `agent-notes/constructor_call_audit.json`，`validate_all.py` 在任何发现上失败。
- `_re/audit_tab_ui_refs.py` 根据各 tab 控制器恢复出的页面或 `.ui` 文件检查
  其 `self.ui.*` 引用，并写入 `agent-notes/tab_ui_ref_audit.json`。
- `_re/audit_ui_refs.py` 根据静态 `.ui` widget 名称检查每个 `uic.loadUi`
  使用方，并写入 `agent-notes/ui_ref_audit.json`。
- `_re/audit_method_calls.py` 根据同类方法签名检查 `self.<method>(...)` 调用，
  并写入 `agent-notes/method_call_audit.json`。
- `_re/audit_item_widget_refs.py` 将 `ui/static` 列表项 widget 与 `Q*` 类对账；
  `label_*`/`dl_label_*` 双布局变体记录为可选兼容名称。
- `_re/audit_obfuscated_signatures.py` 将每个单入口混淆模块与其 Hex-Rays 签名
  比较；当前审计为 90 个模块、0 个发现、0 个缺失证据。
- `_re/audit_dispatch_coverage.py` 强制 91 个混淆入口模块中的每一个都被其
  包分派测试引用。
- Ruff `F401` 在整个恢复树中无告警；离线套件和导入契约测试仍是动态引用守卫。
- `_re/ida_decompile_idat.py` 从干净工作目录驱动便携版 `idat.exe`，并将
  Hex-Rays 伪代码写入 `agent-notes/decompiled/targets/`；`IDA_TARGET` 选择
  分析副本，不触碰原始数据库。
- `agent-notes/dependency_inventory.json` 记录导入每个包的模块。
- PyQt5、Telethon、aiohttp、Pillow、cryptography、moviepy、numpy、OpenCV、
  pywin32、APScheduler、openai、qrcode 和 html2text 是运行时依赖；均未内置。
- 离线套件有意避开第三方运行时；UI 模块使用 AST 契约检查，而不是导入 PyQt5。
- `MANIFEST.json` 固化每个源文件的 SHA-256，并由 `tests/test_manifest.py` 验证。

## 重建检查清单

1. 将原始目标和提取出的运行时保持在测试进程之外。
2. 源码编辑后重新运行 `python -m compileall -q recovered_src`。
3. 重新运行 `python -m pytest -q`。
4. 当函数体覆盖率变化时，更新 `agent-notes/source_stats.json` 和
   `RECOVERY_NOTES.md`。
5. 将仍属推断的行为记录在 `semantic/` 中，而不是把它呈现为精确的原始源码。
6. 当加载器表或导入发生变化时，重新运行 `_re/audit_source_coverage.py` 和
   `_re/audit_dependencies.py`。
