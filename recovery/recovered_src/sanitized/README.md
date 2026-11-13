# 净化层

`src.py.com.yun.mao.sanitized` 是用于已恢复离线源码树的可选启用、
内存内中和器。忠实还原的模块不会在磁盘上被修改。

```python
from src.py.com.yun.mao.sanitized import neutralize

neutralize.apply()
# ... run offline analysis/tests ...
neutralize.restore()
```

它替换的内容：

- 卡密门禁：`_sq_jqm._zh_rd_code`、`_lk_gy_w.gy_jc_a1..a9`、
  `_lk_gy_r.gy_jc_b1`、`AutoBeanXXX.ensure_valid`、`_gy_*` 检查。
- 反调试：`FdsHhx` 检测和 `fh_*` 响应方法。
- 关机：`fea._*_file` 条目（`s_bq_sweep`、`g_wp_flush`、
  `k_dm_drain`、`n_lc_rinse`、`o_yt_purge`、`v_hz_scrub`）和 `_fdg_*`。
- 勒索：`ade._u_common.encrypt_log`、`ade._u_*`、`ade._ade_sing._ak`、
  `ade.ad_t.ad_t`。

它不会执行原始 `运营猫.exe`，不会联系远程
授权服务，也不会解密或加密用户文件。

归档代码和实现分析位于
`semantic/card-key-analysis.md` 和 `semantic/malicious-logic-analysis.md`。
