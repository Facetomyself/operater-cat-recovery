# UI 文本清单

## 已恢复内容

`agent-notes/dyna_ui_text_inventory.json` 保留八个生成 UI 模块的
`retranslateUi` 常量池：

| 模块 | 文本条目 |
| --- | ---: |
| `ai_employee_item` | 17 |
| `auto_flow_item` | 115 |
| `ban_yun_flow_comment_item` | 94 |
| `down_load_flow_item` | 54 |
| `yulan_flow_item` | 112 |
| `yun_auto_item` | 109 |
| `yun_preview_item` | 108 |
| `yun_yin_mao_main` | 144 |

每个条目都保留原始的 `("Form", text)` / `("MainWindow", text)` 上下文对。
JSON 还会记录 `setWindowTitle`、`setText`、`setPlaceholderText`、
`setItemText`、`setTabText`、`setCurrentText` 和 `setTitle` 的首次使用顺序。

## 精确配对

仅凭常量池会对方法名去重，因此无法证明 widget 到文本的分配。精确配对
来自 IDA 反编译的 `retranslateUi` qword 序列：

- `agent-notes/dyna_retranslate_pairs.json` 保存已恢复的
  widget/方法/文本三元组。
- `_re/extract_retranslate_pairs.py` 解析 IDA C 文件，按已知方法名对齐
  调用，并处理 `setItemText + index` 的额外常量。
- `_re/generate_dyna_ui_modules.py` 自动添加缺失的 widget，并输出对应的
  `retranslateUi` 调用。

通用门禁是 `tests/test_dyna_retranslate_pairs.py`；auto-flow 专用门禁是
`tests/test_auto_flow_exact_texts.py`。

## 剩余边界

`setItemText` 会连同已恢复的 index 一起输出；当 0/1 的小 index 常量不存在
于池中时，会从同一 combo 的调用顺序推断。恢复文本是字面量时
（`按组计算`），会输出 `setCurrentText`。`Ui_MainWindow` 现在创建
`gen_session` 标签页，并输出
`setTabText(indexOf(gen_session), "账号功能")`；占位标签页是推断出的
最小容器。`setupUi` 几何/布局仍是独立的推断边界。

## 重新生成

```powershell
D:\reverse_ENV\.venv\Scripts\python.exe D:\reverse_ENV\workspace\operater-cat\_re\build_ui_text_inventory.py
D:\reverse_ENV\.venv\Scripts\python.exe D:\reverse_ENV\workspace\operater-cat\_re\extract_retranslate_pairs.py
```

`tests/test_ui_text_inventory.py` 校验全部八个模块均存在且非空。
