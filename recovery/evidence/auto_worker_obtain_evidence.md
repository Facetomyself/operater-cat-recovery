# AutoWorker.obtainMessageAndParse 证据

仅静态证据；未执行目标。

## 来源

- 函数主体：`agent-notes/decompiled/targets/0x50e50f0_obtain_parse_body.c`。
- 模块常量：`agent-notes/nuitka_constants.json`，AutoWorker 常量
  105-159 与 varnames 元组 208。
- 当前源码：`recovered_src/src/py/com/yun/mao/auto/AutoWorker.py`。

## 恢复后的控制流

1. 通过 `gy_jc_a1` 守卫 `autoxxx`。
2. 使用 `dt_fetch_msg_04` /
   `dt_iwt_mod_03` 目录键解析 `_dtdm_gl.dt_hq_fn`。
3. 可选的随机模式会话重置，通过
   `RandomBucketManager.clear_session_tried_ranges` 完成。
4. 使用标签 `rg_aw_fetch_pre_start_01` /
   `rg_aw_fetch_pre_end_02` 进行动态抓取，处理 stop/None，然后调用
   `yp_jx_pd_ch(autoxxx, message_list_object, is_monitor=False)`。
5. 空结果进入重试循环；increase 模式写入
   `startId + wantCount`；random 模式报告会话已尝试窗口数。
6. 循环使用标签 `rg_aw_fetch_loop_start_05`、
   `rg_aw_fetch_loop_end_06`、`rg_aw_yp_ch_loop_start_07`、
   `rg_aw_yp_ch_loop_end_tpl_08` 重复抓取/解析。
7. 成功返回 `(True, resultList)`；终止/stop/None 路径返回
   `(False, None)`。

## 边界

确定：两阶段抓取/解析结构、fail-fast 分支、标签、stop 检查以及
`(bool, list-or-None)` 返回契约。

推断：空结果提示的确切格式以及 `mem_auto_for_writeback` 查找回退；
已恢复的仓库尚未将该 helper 作为稳定的模块级函数暴露出来。

## 内部编排

`inner_working` 现在遵循恢复后的调用顺序：生成/转换
`autoxxxList`，带 stop 检查和进程缓存更新地循环，调用
`obtainMessageAndParse`，对成功打印做门禁，用返回的解析列表创建
`foreachToSend`，轮询任务，提取四个结果字段，追加
`completeItemSummery`，发布私有/全局广告，休眠 2-5 秒，然后调用
`print_summery`。直接发布广告与 AutoWorker 模块常量一致。反编译的
foreach 主体
`agent-notes/decompiled/targets/0x51619d0_awr_foreach_body.c` 不包含
`process_ad_second_to_last` 或 `publish_*_ad` 引用，因此已从
`foreachToSend` 中移除重复的包装器调用。
