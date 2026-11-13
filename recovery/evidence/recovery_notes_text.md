# Operater-Cat CommonCode 文本恢复

范围：仅 `process_text_to_obj` 和 `safe_with_append_tail`。

状态：
- 仅静态分析。没有目标可执行文件、没有 payload 脚本、没有运行时导入。
- 未修改 `recovered_src`。
- 输出是可直接打补丁的 Python，以及显式的证据/推断标记。

## 1. 签名证据

`function_name_map_exact.json` 映射：

- `process_text_to_obj` -> RVA `0x5df4dd0`，名称常量索引 `685`
- `safe_with_append_tail` -> RVA `0x5df8400`，名称常量索引 `691`

模块 `src.py.com.yun.mao.util.need.CommonCode` 的 Nuitka 常量基址为
`0x148969580`。使用 `(addr - 0x148969580) // 8` 解析函数体中的 `qword_*`
引用，可得到下文使用的字面字符串。

常量/varname 证据：

- `process_text_to_obj` varnames:
  `('is_mark_down', 'text', 'deleSourceText', 'deleLink', 'replaces',
  'new_text', 'e', 'r', 'tt', 'source_text', 'replace_text')`
- `safe_with_append_tail` varnames:
  `('for_mat', 'source_text', 'tail_html', 'message', 'original_entities',
  'plain_tail_text', 'tail_entities', 'full_text', 'prefix_cu', 'entity',
  'combined_entities', 'html_text_has_tail', 'html_text_no_tail', 'temp',
  'text_has_tail')`
- 在模块初始化处观察到的 `safe_with_append_tail` 注解：
  `tail_html: str`、`message: Message`（Telethon message 类型常量 575）。
- `process_text_to_obj` 的返回注解是 `MessageMyObj`（注解和构造函数调用
  使用同一个全局加载）。

恢复出的类当前为：

```python
def __init__(self, for_mat: str, text: str, ai_refused: bool):
```

证据表明，两个恢复出的函数只使用两个位置参数调用 `MessageMyObj`。因此
原始构造函数必须是：

```python
def __init__(self, for_mat: str, text: str, ai_refused: bool = False):
```

这是下文补丁的前提，除非调用点显式传入 `False`。该默认值是强推断，
并不是类型注解常量直接打印出来的。

## 2. 可直接打补丁的 Python

以下代码面向
`recovered_src/src/py/com/yun/mao/util/need/CommonCode.py`。导入部分假设
现有的 `from . import utils` 保持不变。

```python
from telethon.extensions import html
from telethon.tl.types import Message

from ...config import {{SECRET_yiwyjonl}}
from ..CustomerHtmlFormat import code_unit_length, entities_to_html


class MessageMyObj:
    for_mat: str
    text: str
    ai_refused: bool

    def __init__(self, for_mat: str, text: str, ai_refused: bool = False):
        self.for_mat = for_mat
        self.text = text
        self.ai_refused = ai_refused


def process_text_to_obj(
    is_mark_down: bool,
    text: str,
    deleSourceText: bool,
    deleLink: bool,
    replaces,
) -> MessageMyObj:
    # Verified branch order: deleting the whole source wins over markdown mode.
    if deleSourceText:
        return MessageMyObj("html", "")

    # Verified: markdown mode returns the original text unchanged.
    if is_mark_down:
        return MessageMyObj("markdown", text)

    # Inferred safe fallback. The compiled path does not visibly assign a
    # fallback when utils.remove_links() raises, so the literal original could
    # raise UnboundLocalError at the return below. Keeping text is safer.
    new_text = text
    if deleLink:
        try:
            new_text = utils.remove_links(text)
        except Exception:
            pass

    # Verified replacement format: each item is split on the configured
    # "old->new" separator; malformed items are swallowed by the outer except.
    try:
        for r in replaces or ():
            if {{SECRET_yiwyjonl}}.MAO_REPLACE_FU_HAO in r:
                source_text, replace_text = r.split(
                    {{SECRET_yiwyjonl}}.MAO_REPLACE_FU_HAO
                )
                new_text = new_text.replace(source_text, replace_text)
    except Exception:
        pass

    return MessageMyObj("html", new_text)


def safe_with_append_tail(
    for_mat: str,
    source_text: str,
    tail_html: str,
    message: Message,
):
    # Verified: source is normalized and stripped; tail_html is not stripped.
    source_text = (source_text or "").strip()
    original_entities = message.entities or []

    # "markdown" is the Telethon Markdown input mode. The output is HTML text
    # with entities reconstructed from the original message plus the tail.
    if for_mat == "markdown":
        if tail_html:
            plain_tail_text, tail_entities = html.parse(tail_html)
            tail_entities = tail_entities or []

            # Two code units are added by the "\n\n" separator.
            full_text = source_text + "\n\n" + plain_tail_text
            prefix_cu = code_unit_length(source_text) + 2

            # Telethon entity offsets are UTF-16 code units. Shift only the
            # newly parsed tail entities, then concatenate original entities.
            for entity in tail_entities:
                entity.offset += prefix_cu

            combined_entities = original_entities + tail_entities
        else:
            full_text = source_text
            combined_entities = original_entities

        # Verified: both variants are rendered independently.
        html_text_has_tail = entities_to_html(
            full_text, combined_entities
        ).strip()
        html_text_no_tail = entities_to_html(
            source_text, original_entities
        ).strip()

        print(
            f"原文本模式搬运 safe html_text_has_tail ："
            f"{html_text_has_tail} length: {len(html_text_has_tail)}"
        )
        return (
            True,
            html_text_has_tail,
            combined_entities,
            html_text_no_tail,
        )

    # Non-markdown mode is plain concatenation, not HTML parsing.
    # There is no duplicate-tail detection and no separator added here.
    temp = ""
    if source_text.strip():
        temp += source_text
    if tail_html:
        temp += tail_html

    text_has_tail = temp.strip()
    print(
        f"不是原格式搬运 safe text_has_tail ："
        f"{text_has_tail} length: {len(text_has_tail)}"
    )
    return False, text_has_tail, original_entities, source_text
```

## 3. `process_text_to_obj` 控制流

由 `0x5df4dd0_CommonCode_process_text_to_obj.c` 和常量验证：

```text
if deleSourceText:
    return MessageMyObj("html", "")

if is_mark_down:
    return MessageMyObj("markdown", text)

if deleLink:
    new_text = utils.remove_links(text)
else:
    new_text = text

if replaces:
    for r in replaces:
        if "->" in r:
            old, new = r.split("->")
            new_text = new_text.replace(old, new)

return MessageMyObj("html", new_text)
```

重要后果：

- `deleSourceText=True` 会压制整条消息，即使 `is_mark_down=True`。
- `is_mark_down=True` 会在链接删除和替换处理之前返回；该路径上
  `deleLink` 和 `replaces` 被忽略。
- 正常分支始终返回 `for_mat="html"`，绝不会返回 "markdown"。
- 仅当 `deleLink` 为真时才调用 `utils.remove_links`。
- 替换规则使用 `{{SECRET_yiwyjonl}}.MAO_REPLACE_FU_HAO`，其恢复值为
  `"->"`（`{{SECRET_yiwyjonl}}.py:27`）。
- 只有包含 `"->"` 的替换项才会被使用。split 会解包为恰好两个名称，
  因此多余分隔符或畸形项会抛错，并被异常包装器吞掉。
- 该函数不执行空白剥离。Markdown 路径原样返回传入的 `text`。

该函数中的常量用途：

- `markdown` -> markdown 结果分支
- `html` -> 删除源内容和正常结果分支
- `MessageMyObj` -> 构造函数和返回注解
- `{{SECRET_yiwyjonl}}` + `MAO_REPLACE_FU_HAO` -> 替换分隔符
- `split`、`replace`、`new_text` -> 替换循环
- `remove_links` -> 链接清理
- `('html', '')` -> 字面量双参数构造函数回退

## 4. `safe_with_append_tail` 控制流

已验证签名：四个位置参数，没有第五个 `original_entities` 参数。C 主体只
读取 `a3+0`、`a3+8`、`a3+16` 和 `a3+24`；`original_entities` 是由
`message.entities` 派生的局部变量。

已验证的规范化：

```python
source_text = (source_text or "").strip()
original_entities = message.entities or []
```

`tail_html` 会做 truthiness 检查，并原样传给 `html.parse`。编译后的主体中
没有 `tail_html.strip()` 调用。

### Markdown/HTML 模式

条件为精确相等：

```python
if for_mat == "markdown":
```

字符串 `"html"` 不是该分支的触发条件。这一点很重要：传入
`for_mat="html"` 会进入纯拼接分支。

如果 `tail_html` 为真：

1. `plain_tail_text, tail_entities = html.parse(tail_html)`
2. `full_text = source_text + "\n\n" + plain_tail_text`
3. `prefix_cu = code_unit_length(source_text) + 2`
4. 对每个 tail entity：`entity.offset += prefix_cu`
5. `combined_entities = original_entities + tail_entities`

如果 `tail_html` 为假：

1. `full_text = source_text`
2. `combined_entities = original_entities`

随后，在两种情况下都执行：

```python
html_text_has_tail = entities_to_html(full_text, combined_entities).strip()
html_text_no_tail = entities_to_html(source_text, original_entities).strip()
```

返回：

```python
(True, html_text_has_tail, combined_entities, html_text_no_tail)
```

`+ 2` 是插入的 `"\n\n"` 的 UTF-16 长度。来自 `html.parse` 的偏移相对于
`plain_tail_text`；加上前缀长度后，它们相对于 `full_text`。

### 纯文本模式

当 `for_mat != "markdown"` 时：

```python
temp = ""
if source_text.strip():
    temp += source_text
if tail_html:
    temp += tail_html
text_has_tail = temp.strip()
```

返回：

```python
(False, text_has_tail, original_entities, source_text)
```

该分支不插入 `"\n\n"` 分隔符。没有成员测试、`endswith` 或相等检查，
因此这 **不会** 避免重复追加 tail。“safe” 部分只是 None/空值规范化和
一个回退变体。

## 5. `MessageMyObj` 构造

已验证的构造函数形式：

- `deleSourceText` 使用 `MessageMyObj("html", "")`
- Markdown 模式使用 `MessageMyObj("markdown", text)`
- 正常模式使用 `MessageMyObj("html", new_text)`

`process_text_to_obj` 中没有 `for_mat` 局部变量；格式字符串是内联传入的。

恢复出的类字段为：

```text
for_mat: str
text: str
ai_refused: bool
```

构造函数必须将 `ai_refused` 默认为 `False`。如果补丁只应用到这两个函数，
却保留当前需要三个必填参数的构造函数，那么上面的每次调用都会抛出
`TypeError`。

## 6. Telethon HTML/Markdown 处理

`safe_with_append_tail` 使用：

- `telethon.extensions.html.parse(tail_html)`
- resulting `(plain_tail_text, tail_entities)`
- `CustomerHtmlFormat.entities_to_html(full_text, entities)`
- `CustomerHtmlFormat.code_unit_length(source_text)`

恢复出的 `CustomerHtmlFormat.py` 已在第 10 行提供 `code_unit_length`，并在
第 126 行提供 `entities_to_html`。`entities_to_html` 会对文本做 HTML
转义，并渲染 Telethon entity 类，例如 bold/italic/pre/custom emoji。它使用
UTF-16 code-unit 偏移，与 C 前缀计算一致。

`process_text_to_obj` 不调用 Telethon HTML 解析。它只选择 Telethon 解析
模式字符串，并可选地删除链接/替换文本。

## 7. 推断或不确定项

显式标记这些项，以免补丁审查将它们当作字节级事实：

1. `MessageMyObj.ai_refused = False` 默认值：由全部三个双参数构造函数调用点
   强推断；注解常量本身没有显示默认值。
2. `utils.remove_links` 和替换循环周围的 `except Exception: pass`：C 异常
   路径会吞掉异常并继续，但确切源码语句可能是裸 `except:` 或空处理器。
   本次恢复使用 `except Exception`。
3. `remove_links` 抛错时的 `new_text = text` 回退：推断出的安全性改进。
   编译路径似乎会让该局部变量未绑定，并在返回时抛出 `UnboundLocalError`。
4. Debug 打印格式：由常量片段 `" length: "` 和两个中文前缀重建为
   f-string。C 通过 `format`/join 构建字符串；f-string 形式保留了确切
   空白。
5. `message` 注解是 `Message`（Telethon TL message），不是
   `MessageMyObj`。证据：访问 `.entities` 以及模块常量索引 575。
6. `entities_to_html` 和 `code_unit_length` 是从
   `..CustomerHtmlFormat` 导入的模块级名称；模块初始化导入列表包含
   `('entities_to_html', 'code_unit_length')`。
7. `html` 是 `telethon.extensions.html`；函数调用 `html.parse`。
8. 未发现对已存在 tail 的去重。如果产品期望幂等追加，该行为不在本函数中。

## 8. 验证状态

- 证据交叉检查：函数名映射、varnames、常量基址、注解和反编译分支结构
  全部一致。
- 未执行运行时验证。
- 上面的 Python 面向语法检查，供后续源码补丁使用；未导入，也未针对
  Telethon 执行。

