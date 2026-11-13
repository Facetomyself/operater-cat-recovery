# operater-cat 恢复交付包

这个目录是可直接拷走的单文件夹交付包，包含恢复源码、语义文档、接口契约、
离线测试和合成协议实验。

## 快速开始

```powershell
cd recovered_src
python -m pytest -q

cd ..\offline_protocol_lab
python run_lab.py

cd ..
python verify_bundle.py
```

`run_lab.py` 使用合成 fixture，不联网、不启动原始目标、不使用真实账号。

## 内容

- `PROTOCOL_CONTRACTS.md`：endpoint 矩阵、请求/响应字段、关键代码块和已知契约问题。
- `recovered_src/`：完整恢复源码、测试、语义文档、`OVERALL_LOGIC_AND_GAPS.md`、
  `RECOVERY_NOTES.md`、`COVERAGE.md`、`MANIFEST.json`。
- `offline_protocol_lab/`：离线协议 harness、合成 fixture 和运行输出。
- `agent-notes/`：测试所需的 Nuitka/函数映射/布局/依赖证据。
- `ui/`：测试所需的静态 Designer `.ui` 资源。
- `evidence/`：精选的审计 JSON 与原始 agent-notes Markdown。

## 安全边界

- 不包含 `运营猫.exe`、`static_hybrid*.exe` 或任何原始可执行文件。
- 不执行目标、不连接真实服务端、不伪造真实授权。
- `{{SECRET_*}}` 保持脱敏占位符。
- `recovered_src` 是行为级恢复，不是逐字节原始源码。

## 阅读顺序

1. `PROTOCOL_CONTRACTS.md`
2. `recovered_src/OVERALL_LOGIC_AND_GAPS.md`
3. `recovered_src/semantic/README.md`
4. `offline_protocol_lab/findings.md`
5. `recovered_src/RECOVERY_NOTES.md`
