# 运行时服务

## mthread

`mthread/` 包含长期运行的 Qt worker 层：

- `TgClientBaseAsyncTaskThread`：基础异步 Telegram 任务、worker 参数、
  调度器状态/图标信号以及登录结果解包。
- `SchedulerThreadClass`：调度器/worker 编排和工作锁集成。
- `SingleLongTaskThreadClass`：单个长任务的生命周期。
- `ReceiveCodeThread`：手机验证码请求路径与 worker 跟踪。
- `GenHtmlThread`：HTML 生成 worker。
- `PostHtmlADThread`：HTML/广告上传与完成统计。

worker 类共享 `_emit_stats`、`_emit_icon_state`、
`_set_scheduler_status` 和 `_unpack_login_result` 契约。导入时不会启动
Telegram 客户端。

## 登录与会话

- `login.SessionLoader`：session 文件发现、隐藏自动登录、
  `autologinWithSession` / `autologinWithSessionByHide`、隐身模式和
  断开连接处理。
- `login.ClientCacheHelper`：cache-client 持久化和安全断开。
- `login.NetTest`：`FastTelegramTestTask`/`FastNetTest` 连通性快速检查路径。

## 记录与内存

- `record.CommentCopyLedger`：comment-key 解析、来源/channel id、
  已复制检查以及目标缺失 id 并集。
- `record.PublishIdRecord`：已发布消息记录文件、消息链接构建器/解析器、
  记录列表完整性检查、高层发布映射构建以及包装后的 JSONL 查询。
- `ad.AdIdMapManager`：加密广告 id 映射持久化、去重更新和目标键辅助函数。
- `remember.RememberManager`：remember 映射的加载/获取/更新/清理/写入。
- `ad.AdIdMapManager` 和 `remember.RememberManager`：恢复密钥的加密映射
  持久化，以及离线往返检查。
- `remember.RandomBucketManager`：持久化随机范围、bucket 重叠检查、
  布局重建、session 已尝试窗口、耗尽 bucket 持久化以及重置/重启辅助函数。

## 配置

- `config.ConstantCache` / `config.TableCache`：由 INI 支撑的单例。
- `config.InnerAppIdConfig`：缓存的 `api_hash` / `api_id`。
- `config.net_config`：代理启用/主机/端口访问器。
- `config.NewConfig`：flow 时长/water/monitor 常量。
- `config.YunYinMaoConfig`：缓存/下载/账户/临时目录解析器。

## 日志

- `log.glog.GlobalLog`：挂接 UI 的日志门面、暂停/恢复、磁盘尾部合并和
  冻结超时状态。
- `log.LocalLogSetting`：日志文件路径，以及追加/读取/截断/删除辅助函数。
- `log.LogWorker`：延迟日志写入器。

除使用 PyQt5 进行 UI 挂接的部分外，日志和配置层都是纯逻辑且可离线测试。
proxy/record/remember 路径会接触本地文件，但不会由离线套件执行。

## 置信度

- 类/函数名称和参数契约已从模块常量和 init 表恢复。
- 在多个调用点一致时，文件布局和 worker 信号顺序具有高置信度；
  调度器/时序边界情况属于推断。
- 本文档不包含网络、Telegram、代理或目标执行。

## 证据

- `src/py/com/yun/mao/{mthread,login,proxy,record,remember,config,log}/`
- `agent-notes/function_map_full.json`
- `agent-notes/nuitka_constants.json`
