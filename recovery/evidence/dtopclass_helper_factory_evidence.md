# DTopClassHelper 自动 Bean 工厂证据

## 发现来源

`src.py.com.yun.mao.dclass.DTopClassHelper` 常量块包含一段连续的工厂块：

```text
283 AUTO_BEAN_TYPE_OLD
284 auto_type
285 100
286 priority
287 parse_ban_yun_flow
288 AUTO_BEAN_TYPE_BAN_YUN
289 kid
290 active
291 yun_yin_bean
292 beanLike
293 AUTO_BEAN_TYPE_AUTO_FLOW
294 AUTO_BEAN_TYPE_YU_LAN_FLOW
295 flow_bean
296 parse_auto_flow_or_yulan_flow
297 AUTO_BEAN_TYPE_DOWN_LOAD_FLOW
298 parse_down_load
299 AUTO_BEAN_TYPE_YUN_AUTO
300 parse_yun_auto
301 AUTO_BEAN_TYPE_YUN_PRE_VIEW
302 parse_yun_preview
```

模块初始化反编译
（`agent-notes/decompiled/dtophelper2/init_0x05518250.c`）也引用了
`parse_ban_yun_flow`、`parse_auto_flow_or_yulan_flow`、`parse_down_load`、
`parse_yun_auto`、`parse_yun_preview`、`yun_yin_bean` 和 `flow_bean`。

## 重建后的分派

`dic_to_Auto_obj` 先解包传输层 `beanLike` 映射，再根据 `auto_type`
进行分派：

| `auto_type` | 工厂 | Bean |
| --- | --- | --- |
| 1 | `parse_ban_yun_flow` | `BanYunBean` |
| 2 | `parse_auto_flow_or_yulan_flow` | `AutoFlowBean` |
| 3 | `parse_auto_flow_or_yulan_flow` | `YuLanBean` |
| 4 | `parse_down_load` | `DownLoadBean` |
| 5 | `parse_yun_auto` | `YunAutoBean` |
| 6 | `parse_yun_preview` | `YunPreViewBean` |

默认分支（`AUTO_BEAN_TYPE_OLD`/未知）使用
`parse_ban_yun_flow`，这与常量顺序一致：`AUTO_BEAN_TYPE_OLD` 位于
BanYun 工厂之前。

## 置信度边界

- 函数名、字段名和 `auto_type` 判别值来自常量块与模块初始化证据。
- 工厂主体是行为层面的重建：它们应用标量身份字段，并递归复用已恢复的
  `dic_to_*` 转换器。
- 不声称原始 C 主体内部的精确操作数顺序；Python 调用契约由
  `tests/test_auto_factory.py` 固定。
- 反编译初始化带有 Hex-Rays 的“write access to const memory”警告，
  因此该初始化仅用作名称证据，不作为主体源码。

## 证据路径

- `agent-notes/nuitka_constants.json`
- `agent-notes/function_map_full.json`
- `agent-notes/decompiled/dtophelper2/init_0x05518250.c`
- `agent-notes/decompiled/dtophelper2/0x05564d50.c`
- `recovered_src/tests/test_auto_factory.py`
- `recovered_src/src/py/com/yun/mao/dclass/DTopClassHelper.py`
