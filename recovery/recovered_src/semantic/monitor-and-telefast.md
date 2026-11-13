# 监控与快速传输语义

## 监控

`monitor.TelegramMonitorWorker` 是带有三个 UI 信号的 `QThread`：
`log_signal`、`progress_signal` 和 `auth_signal`。其运行时依赖展示了监控路径：

- `AutoWorkerWrapper`、`ProcessCache`、`TopicUtils`、`GlobalWorkingLock`；
- `TaskHardStop` 用于停止契约；
- `AsyncDequeQueue` 用于事件投递；
- `RateTempClass`、`_sq_r_ca` 和 `YjxHb` 用于报告/状态节流；
- `MonitorFollowUp` 用于事件后工作。

`monitor.MonitorFollowUp` 重建 Telegram 后续规则：

- 相册回看（`ALBUM_LOOKBACK`）；
- 讨论回复锚点和频道帖子 id 提取；
- 镜像频道检测；
- 评论直播和 caption 同步决策；
- 从 Telegram entities 渲染 HTML。

`monitor.MonitorSchedulerReportThread` 是看门狗线程。它优先使用带每小时 cron
任务的 `apscheduler` 阻塞调度器，并在 APScheduler 不可用时回退到 60 秒的
`_sq_ks.start_report_inner()` 循环。

`HistoryMessageOpDialog` 和 `QHistoryMsgItemQWidget` 是 Qt 历史界面；它们的
widget 名称来自恢复出的 UI 树和 `history_message_list_op.ui` /
`q_history_item_widget.ui` 资源。

## Telefast

`telefast` 是传输/限速层：

- `RateLimiterClass`：`RateLimiter`、`UpRateLimiter`、`DownRateLimiter`；
- `RateTempClass`：每作用域临时速率状态；
- `RateLimiterHelper`：自动速率调度、flood 标记、衰减和 `changed_rate` 信号流；
- `CallBack`：上传/下载/water/预览进度格式化；
- `FastDownUpLoadUtils`：快速下载、部分下载和快速上传；
- `FastTelethon`：并行下载/上传发送器、DC 授权、分片大小归一化和流适配器。

自动速率调度是精确的：从 1/1 到 20/20 的 3 小时步进，并带一个 39 小时终止
条目。Flood 衰减和精确的 Telethon DC-auth 握手属于行为级重建。

## 安全

恢复过程不打开 Telegram 连接、不启动 ffmpeg、不启动目标，也不发出这些信号。
网络和文件传输分支是翻译后的源码，不是运行时测试装置。

## 证据

- `src/py/com/yun/mao/monitor/`
- `src/py/com/yun/mao/telefast/`
- `agent-notes/function_map_full.json`
- `agent-notes/nuitka_constants.json`
