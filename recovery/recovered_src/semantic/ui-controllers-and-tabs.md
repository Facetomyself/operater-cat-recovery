# UI 控制器、标签页与业务对话框

## 标签页控制器

`tab/` 是 `MainWindow` 与生成的 UI 对象之间的控制器层：

- `MidBaseTab`：由具体标签页共享的生命周期钩子（`on_tab_show`）。
- `AiEmployeeTab`：员工列表/编辑器、敏感词导入、模型信息。
- `AiTestTab`：测试输入/输出、完成桥接、提示 HTML。
- `ApiConfigTab`：API/模型配置控件。
- `AutoYunYinTab`：自动 flow 列表、flow 对话框分派、JSON/默认值辅助函数。
- `PremiumTab`：会员状态、价格对话框和权限检查。
- `SessionFunTab`：session/账户操作、代理设置、账户列表。
- `ToolBoxTab`：实用工具操作和结果解包。
- `gen_session_queue`：手机登录/请求验证码/session 生成循环。

标签页类拥有 `ui` 对象并连接信号；导入时不会创建目标的网络客户端或
Telegram 客户端。

## 对话框

- `PremiumDialog`、`PremiumBigPriceDialog`、`PremiumExitTipDialog`：会员
  定价与退出流程。
- `AiModelInfoPriceDialog`：模型定价表。
- `CourseImageDialog`：课程图片查看器。
- `ExpriActivatePermissionDialog`：权限激活提示。
- `ReceiveCodeDialog`：手机验证码 UI 和复制辅助函数。
- `ImageDialogHelper.unifyShow*Course`：具名课程链接分派表。

## 账户与代理

- `tgaccount.TGAuthAccount`：账户身份/session 模型。
- `TGAuthAccountEncoder`：持久化账户 JSON 结构。
- `TGAuthAccountSetting`：添加/更新/删除/加载 session 账户以及
  dis-auth 列表。
- `proxy.ProxySettingDialog`：代理分组/启用设置。

## 广告、水印与评论

- `ad.AdIdMapManager`：加密广告 id 映射的加载/获取/更新/写入。
- `AddOrEditAdDialog`、`ToolsBoxEditAdDialog`：广告文件传输和编辑。
- `UIAdListOp`：广告列表操作。
- `water.PicBlurUtils`、`PicWaterUtils`：高斯模糊和图像/文字水印绘制。
- `water.VideoBitUtils`：码率/fps 和文字裁剪辅助函数。
- `water.VideoWaterUtilsToSmallFile`：小文件视频水印的 ffmpeg 命令组装。
- `water.waterUtils`：文件大小路由和自动水印入口。
- `comment.ConfigCommentRuleDialog`：评论规则编辑器和保存路径。

ffmpeg、网络、Telegram 和 shell 路径仅为源码翻译。
恢复过程不会执行它们。

## 置信度

- 控制器/对话框的类名和方法名已从模块 init/constants 恢复。
- 信号接线和持久化路径在匹配多个常量和调用点的情况下具有高置信度。
- 生成的 UI 几何和精确标签位置仍属推断；参见
  `ui-resource-reconstruction.md`。

## 证据

- `src/py/com/yun/mao/{tab,dialog,tgaccount,proxy,ad,water,comment}/`
- `agent-notes/nuitka_constants.json`
- `agent-notes/function_map_full.json`
