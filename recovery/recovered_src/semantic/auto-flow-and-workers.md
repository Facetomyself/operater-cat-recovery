# 自动流程与 worker 语义

## 范围

本文覆盖恢复出的 `auto` 包：

- `AutoWorker.py`、`AutoWorkerWrapper.py`
- `FlowProcess.py`、`YunProcess.py`、`BanYunProtect.py`
- `DownLoadProcess.py`、`DownLoadBizHelper.py`
- `GenSegmentVideoOnePass.py`、`GenYuLanVideoWrapper.py`
- `IsoBmffFirstFrameParser.py`、`VideoFirstFrameCoverHelper.py`

函数名和参数数量从 Nuitka 模块 init 恢复。常量或 Hex-Rays 中不存在的
媒体/发布分支在源码中标记为 `inferred`。

## Worker 编排

`AutoWorker.worker_start_inner` 是入口包装器。`inner_working` 构建每个组的
执行上下文，`obtainMessageAndParse` 解析源消息和解析计划。`AutoWorkerWrapper`
承载结果对象：

- `_GroupResult`：消息 id、发送计数、目标/预览映射、AI 拒绝和保护内容标志。
- `_FlowResult`：组结果的流程级子集。
- `_ProtectResult`：保护发送结果。
- `_ForeachTotals`：多组运行的聚合计数器。

结果对象暴露 `skip_group`、`stop_all`、`mark_ai_refused` 及相关状态迁移。
这些是流程处理器使用的稳定契约。`foreachToSend` 还会把每个成功的组结果交给
`PublishIdRecord.append_if_complete`，后者解析源/目标链接并将包装后的记录入队；
映射失败会记录日志，但不停止其余组。

`obtainMessageAndParse` 使用恢复出的动态获取/解析状态机：`gy_jc_a1` 门禁、
`dt_hq_fn` 获取解析、`yp_jx_pd_ch` 频道/评论解析、stop/None/terminal 退出、
递增起始 id 回写和随机桶重试上报。`inner_working` 现在将该解析列表接入
`foreachToSend`、直接广告发布和摘要收尾；其余分支顺序细节属于行为级重建。

## 流程族

- `FlowProcess`：普通和 Markdown 文本发布、目标解析、视频时长限制、预览文本
  生成和临时文件清理。
- `BanYunProtect`：保护内容发送、媒体/文本提取、目标解析和清理。六个模块级
  函数及其参数列表由 init 表确认。
- `YunProcess`：云端目标/预览映射、资源发布、云端文本发布和清理。两个全局 id
  映射是恢复出的跨步骤状态。
- `DownLoadProcess` / `DownLoadBizHelper`：文件路径预留、后缀和文档名处理、
  图片下载、快速/普通重试，以及媒体资源的可选 MD5 重写。

## 首帧封面

`IsoBmffFirstFrameParser` 是纯 ISO-BMFF 读取器：

- box 迭代及 `moov/trak/stbl` 遍历；
- `stco/co64`、`stsc`、`stsz`、`stss` 解析；
- 首个同步样本偏移计算；
- 容器检测和尾部元数据估算。

`VideoFirstFrameCoverHelper` 使用该分析来：

- 下载头/尾字节范围；
- 组装稀疏临时 MP4；
- 仅在函数体内使用 ffmpeg 提取首帧；
- 回退到 Telegram 缩略图。

恢复过程从不运行 ffmpeg 或目标。`MAX_*` 字面量和尾部合并重试细节在数值池
无法证明符号顺序处属于推断。

## 证据

- `agent-notes/function_map_full.json`
- `agent-notes/nuitka_constants.json`
- `agent-notes/decompiled/targets/`
- `src/py/com/yun/mao/auto/` 下的源文件
