# Catalog 明文（现场 rk 解开）

约束：rk / static key 只留在 `capture_lab/*.local`，不进对话、不进 public 仓。

## 主机

- `_p_dh` = `https://birder.jinsiqie.life/`（这就是线上 origin，不是第二台机）
- `_d_lh` = `https://localhost:8764/`（开发）
- `_r_u` **不是主机**，是注册路径 `/safeyunyinmaoV260701/saferegister`

恢复树里 `get_pro_duct_host() -> _r_u` 按「主机」理解是错的。官方 PE 打 birder，和这份 catalog 一致。

## 路径

| 键 | 值 |
| --- | --- |
| `_v_p_i_u` | `/r/spi` |
| `_v_ps_i_u` | `/r/spui` |
| `_v_u_i_u` | `/r/ui` |
| `_v_r_p_i_u` | `/r/roi` |
| `_v_s_c_i_u` | `/r/ca` |
| `_v_s_f_ms` | `/xb/fms` |
| `_f_c_u` | `/safeyunyinmaoV260701/safeFetchConfigV260125` |
| `_v_uu` | `/safeyunyinmaoV260701/safevcode260619` |
| `_r_bu` | `/safeyunyinmaoV260701/safereset` |
| `_s_r_u` | `/safeyunyinmaoV260701/safereport` |
| `_m_cu` | `/safeyunyinmaoV260701/safeMigrateCode` |
| `_s_ac_u` | `/safeyunyinmaoV260701/safeExperienceHour` |
| `_s_co_u` | `/safeyunyinmaoV260701/safeCreateOrderV260501` |
| `_s_co_r_u` | `/safeyunyinmaoV260701/safeCheckOrderAnRecharge` |
| `_s_p_ch_mu` | `/safeyunyinmaoV260701/safeparsechannelmessages` |
| `_s_p_co_mu` | `/safeyunyinmaoV260701/safeparsecommentmessages` |

## 公钥

- 引导 `tw_sjk_pk_pem`：bootstrap_init
- `_r_pk`：fp16 `54c404fbee66aa1b`（先前 RAM 候选）
- `_f_pk`：fp16 `e3c2336a82b436d6`（catalog 解开后新出现）

## 方法

PE 里 catalog 常量是套了一层 urlsafe-b64 的 Fernet 令牌；先解开这一层得到内层 `gAAAAA` 再做 Fernet。现场 `rk` 先解开 static key，再用 static key 解 21 条 catalog。

## URL 拼法

origin = `_p_dh` = `https://birder.jinsiqie.life/`

然后 path 直接接上去，例如心跳 `https://birder.jinsiqie.life/r/spi`。
离线拼表：`offline_protocol_lab/catalog_urls.py` → `capture_lab/catalog_urls.json`。

恢复树两处不要当原版：

1. `get_pro_duct_host()` 读 `_r_u`，但 `_r_u` 是注册 path，不是 origin。
2. `_r_url("r_spi")` 用字面量 `r_spi`，官方 catalog 是 `_v_p_i_u=/r/spi`。
