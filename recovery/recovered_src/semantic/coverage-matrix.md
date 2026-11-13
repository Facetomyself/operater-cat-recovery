# 语义覆盖矩阵

本矩阵将模块族映射到对应语义文档、离线测试和置信边界。它是导航辅助，
不代表每个函数体都与原始源码逐字节一致。

| 模块族 | 语义文档 | 测试/证据 | 置信度 |
| --- | --- | --- | --- |
| `fea._sq_chk`、`_sq_jqm`、`_sq_req`、`_sq_r_req`、`_sq_r_ca`、`_sq_ks`、`_sq_hj`、`_sq_qi` | `license-flow.md`、`proof-ledger.md` | 加密/载荷测试、union-code 测试 | 字段名和调用边界为高置信；端点细节为推断 |
| `fea._pl_wd_file` | `proof-ledger.md` | `test_pl_wd_file.py` | 帧布局精确；`_tg` 操作数顺序为推断 |
| `link._fds_*`、`_tw_*`、`_jmpz_cy` | `license-flow.md`、`risk-boundaries.md` | 导入冒烟测试、加密测试 | 解码链为高置信；不透明反调试辅助函数仅静态分析 |
| `auto.*` | `auto-flow-and-workers.md` | 语义辅助测试、UI 契约测试 | 编排/函数名精确；媒体/发布分支为推断 |
| `monitor.*`、`telefast.*` | `monitor-and-telefast.md` | 导入冒烟测试、速率/工具测试 | 调度/常量为精确；DC 认证和 flood 细节为推断 |
| `tab.*`、`dialog.*`、`tgaccount.*`、`proxy.*`、`ad.*`、`water.*`、`comment.*` | `ui-controllers-and-tabs.md` | 导入冒烟测试、widget 映射测试、`audit_tab_ui_refs.py`、`audit_ui_refs.py`、`audit_method_calls.py` | 控制器名精确；tab/页面归属和跨页面 UI 引用已审计；UI 布局和持久化细节为推断 |
| `bz_uc`、`kv_nx`、`rm_qh`、`wp_jt` | `obfuscated-packages.md` | `audit_obfuscated_signatures.py`、`audit_dispatch_coverage.py`、`test_*_dispatch.py` | 入口点/签名为精确；全部 91 个入口都有分派测试；命令操作数顺序和脱敏值为推断 |
| `fea._dr_vx_file`、`_qf_rn_file`、`_hb_yt_file`、`_cw_jm_file`、`_lk_ps_file`、`_yg_bn_file` | `risk-boundaries.md`、`proof-ledger.md` | `test_hidden_command_chain.py` | argv 形态及 shell/creationflags 契约为高置信；解码槽位语义为推断；仅静态分析 |
| `src.resource.ui.dyna.*` | `ui-resource-reconstruction.md`、`ui-text-inventory.md` | `test_dyna_ui_modules.py`、`test_ui_text_inventory.py`、`test_dyna_ui_runtime_stub.py`、`test_dyna_layout_edges.py` | widget 名称/类型以及 addWidget/addLayout 层级为高置信；几何/文本度量为推断 |
| `dclass.*`、`config.*`、`record.*`、`remember.*`、`prices.*` | `domain-model.md`、`order-and-item-flow.md` | dclass/载荷/prices 测试 | 字段和数据模型为高置信；生命周期边界情况为推断 |
| `mthread.*`、`login.*`、`log.*`、`util.*` | `engineering.md`、`monitor-and-telefast.md` | 导入冒烟测试、工具测试 | 生命周期/契约为高置信；UI 顺序为推断 |

## 证据来源

- `agent-notes/nuitka_module_table.json`
- `agent-notes/nuitka_constants.json`
- `agent-notes/function_map_full.json`
- `agent-notes/source_recovery_audit.json`
- `agent-notes/dependency_inventory.json`
- `recovered_src/module_index.json`
- `recovered_src/tests/`

## 阅读规则

如果某个模块出现在本矩阵中，但其函数体标记为 `inferred`，应将名称/签名视为
已恢复，将控制流视为行为级重建。不要执行反调试、命令分派或真实网络路径来
验证它们。
