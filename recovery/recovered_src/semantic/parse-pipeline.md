# 解析流水线

## 输入

解析器消费 Telegram 消息对象或类消息字典。
`fea/_xx_zy_file.py` 将每条消息规范化为摘要：

```text
id, groupedId, msgType, durationSec, sizeMb,
text, hasButton, legal
```

它还会构建：

- `messages_to_digests(messages)`
- `build_parse_trace_id(ucode, nonce, ts, raw)`
- `build_channel_parse_payload(...)`
- `build_comment_parse_payload(...)`

`PARSE_API_VERSION = 702` 是已恢复的常量。

## 计划组装

`fea/_fs_jh_zb_file.assemble_parse_beans_from_messages(plan_data, messages)`：

1. 读取 `planId`、`requestId` 和 `groups`；
2. 按数值 `id` 为消息建立索引；
3. 校验每个组的 `uniId`、`msgIds` 和 `tartMsgId`；
4. 拼接组文本，并在可用时调用 `CommonCode.getGroupTextAndMessage`；
5. 输出 `ParseBean` 对象（恢复期间若不可用，则回退为可读的 dict）。

## 心跳结果

`fea/_yjx_hb_file.YjxHb` 是频道/评论结果：

```text
terminal : bool
msg      : str
beans    : list[ParseBean]
```

`yp_jx_pd_ch` 和 `yp_jx_pd_cm` 是重建后的编排函数：
它们构建 trace id、payload 和请求，然后调用
`assemble_parse_beans_from_messages`。网络执行不属于离线测试套件的一部分。
