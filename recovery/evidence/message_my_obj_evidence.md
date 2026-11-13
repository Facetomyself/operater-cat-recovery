# CommonCode.MessageMyObj 恢复证据

## 静态身份

- `CommonCode` 初始化 RVA：`0x5DA7520`
- 类命名空间构造：`sub_145D5A150`
- 类名槽位：`qword_148969DB0`（`MessageMyObj`）
- 注解槽位：`qword_14896AAB8`
- 恢复出的注解文本：
  `{'for_mat': {'builtin': 'str'}, 'text': {'builtin': 'str'}, 'ai_refused': {'builtin': 'bool'}}`
- 类命名空间包含 `__module__`、`__qualname__`、`__annotations__`
  和 `__init__`；未观察到 `__repr__`、`__eq__` 或 dataclass 标记。

## 赋值顺序

`sub_145D5A150` 接收四个对象（self 加三个构造值），并调用 Nuitka
属性设置 helper 三次：

1. `self.for_mat = for_mat`
2. `self.text = text`
3. `self.ai_refused = ai_refused`

这三次检查不是值比较，而是属性设置成功检查。恢复出的构造函数主体中没有
默认值。

## 调用方形态

静态 `process_text_inner` 代码入口（`sub_14514F210`）包含生成循环。其
拒绝分支使用源 bean 的 `for_mat` 和最后生成/拒绝的文本构造刷新对象，
并传入关键字形式的常量 `{'ai_refused': True}`。恢复出的源码形态为：

```python
TextCache.ALL_MESSAGE_REFUSED_LIST.append(
    MessageMyObj(obj.for_mat, tart, ai_refused=True)
)
```

非拒绝的终止分支将源 bean 追加到
`TextCache.ALL_MESSAGE_FAILED_LIST`。

恢复出的 Python 代码树现在与这一分叉保持一致：
`process_text_by_ai_if_need(text, auto, bean)` 执行账号、员工和 API key
检查，然后将 `(obj, aiBean, api_key)` 转发给 `process_text_inner`。业务
调用方保留恢复出的 `(text, auto, bean)` 契约。

## 产物

- `agent-notes/decompiled/targets/0x5da7520_commoncode_init.c`
- `agent-notes/decompiled/targets/0x5d5a150_message_my_obj_init.c`
- `agent-notes/nuitka_constants.json`
- `agent-notes/source_signatures.json`

未执行目标进程。这些观察仅为静态 IDA/Hex-Rays 与常量表证据。
