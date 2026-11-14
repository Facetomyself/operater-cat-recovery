# operater-cat-recovery

`运营猫 9.6.3` 的静态恢复与接口分析工程。仓库把原项目、恢复源码、语义文档、
离线协议实验和逆向脚本分开归档，便于阅读、复现和后续补证。

## 状态

- Nuitka/Python 3.11 Windows 桌面程序静态恢复。
- 368 个恢复源文件、3127 个函数、262 个类。
- 20 份语义文档；离线套件 455 个用例通过。
- 卡密、授权票据、反调试和破坏性路径已归档；破坏性入口只做静态分析。
- 接口字段和关键代码块见 `docs/PROTOCOL_CONTRACTS.md`。

## 仓库结构

```text
docs/                 顶层文档、整体逻辑、接口契约、报告和恢复计划
original_project/     原项目整理目录；本地大文件在这里，public git 忽略
recovery/             恢复源码、测试、语义文档和离线协议 lab
analysis/scripts/     还原过程中使用的 Python/IDC/C 分析脚本
```

### `recovery/`

- `recovery/recovered_src/`：完整恢复源码和 455 个离线用例。
- `recovery/recovered_src/semantic/`：领域、授权、订单、UI、worker、反调试文档。
- `recovery/agent-notes/`：测试依赖的 Nuitka/函数映射/布局证据。
- `recovery/ui/`：测试依赖的静态 `.ui` 资源。
- `recovery/offline_protocol_lab/`：不联网的协议 harness 和合成 fixture。
- `recovery/verify_bundle.py`：恢复工程一键自测。

### `original_project/`

- `original_project/app/`：原项目文件（包含 `运营猫.exe`、DLL、运行时资源）。
- `original_project/BINARY_MANIFEST.json`：大文件/二进制路径、大小和 SHA-256。
- public git 不提交 `original_project/app/`；本地保留完整副本。

## 快速开始

```powershell
cd recovery/recovered_src
python -m pytest -q

cd ..\offline_protocol_lab
python run_lab.py

cd ..
python verify_bundle.py
```

## 文档入口

- `docs/PROTOCOL_CONTRACTS.md`：endpoint、请求/响应字段、关键代码块。
- `docs/OVERALL_LOGIC_AND_GAPS.md`：整体逻辑和缺口清单。
- `docs/NETWORK_VALIDATION.md`：本机连接验证、TLS 指纹和抓包结论。
- `docs/report.md`：安全与行为分析报告。
- `docs/triage.md`：快速分诊结论。
- `docs/RECOVERY_NOTES.md`：恢复方法和加载表突破。
- `docs/COVERAGE.md`：覆盖率、测试和审计指标。
- `docs/SOURCE_RECOVERY_PLAN.md`：后续恢复优先级。

## 安全边界

- 仓库不包含可执行文件的公开副本；本地 `original_project/app/` 仅作归档。
- 不执行 `运营猫.exe`、`static_hybrid*.exe` 或任何恢复入口。
- 不连接真实授权服务端，不使用真实账号、卡密或密钥。
- 离线实验只使用合成响应，验签路径在 transport 边界注入。
- `{{SECRET_*}}` 保持脱敏占位符。

## 权利说明

恢复内容是行为级分析，不是原始源码。原软件及其资源的权利归原权利人所有。
仓库不提供授权绕过、真实票据伪造或攻击服务；详见 `NOTICE.md`。
