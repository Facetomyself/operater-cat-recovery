# 交付索引

## 根目录

- `PROTOCOL_CONTRACTS.md`：接口契约和关键代码块。
- `README.md`：快速开始和安全边界。
- `INDEX.md`：本索引。
- `CHECKSUMS.sha256`：交付文件校验和（生成后）。
- `verify_bundle.py`：一键跑离线 pytest 和协议 lab。

## 源码

- `recovered_src/src/`：完整恢复 Python 源码。
- `recovered_src/tests/`：离线测试。
- `recovered_src/semantic/`：20 份语义文档。
- `recovered_src/sanitized/`：反调试/卡密/破坏性路径的无害化层。
- `recovered_src/decompiled/`：Hex-Rays 证据和 Python 级重建。
- `recovered_src/MANIFEST.json`：源文件哈希/行数清单。
- `agent-notes/`：测试依赖的 Nuitka、函数映射、布局、依赖证据。
- `ui/`：测试依赖的静态 `.ui` 资源。

## 实验

- `offline_protocol_lab/run_lab.py`：离线协议实验入口。
- `offline_protocol_lab/fixtures/synthetic_responses.json`：合成响应。
- `offline_protocol_lab/run-output.json`：最近一次运行输出。
- `offline_protocol_lab/findings.md`：已验证字段流和恢复缺陷。

## 证据

- `evidence/function_map_full.json`
- `evidence/nuitka_constants.json`
- `evidence/nuitka_module_table.json`
- `evidence/source_signatures.json`
- `evidence/function_name_map_exact.json`
- `evidence/anti_debug_function_map.json`
- `evidence/dyna_ui_text_inventory.json`
- `evidence/*.md`：原有 agent-notes
