# GitBook 原生平台的中文排版能力

核对日期：2026-11-19。本文只讨论 gitbook.com 托管的 GitBook 原生站点，不涉及旧版 GitBook CLI、HonKit、自建阅读器或浏览器扩展。此次仅记录调研结果，没有修改站点外观。

## 结论与建议

原生 GitBook 可以调整主题、配色、字体家族和页面宽度选项，但没有查到站点管理员可配置的正文字号/缩放比例、行距、段间距或任意像素正文宽度。官方明确规定：任何套餐都不能直接插入自定义 CSS、HTML 或 JS。因此，不能承诺仅靠原生设置把中文排版精确改成“18px、1.8 倍行距、固定段间距”。[站点定制及不可定制项](https://gitbook.com/docs/manage-your-site/customization#what-cannot-be-customized)、[公开定制 API](https://gitbook.com/docs/developers/gitbook-api/api-reference/docs-sites/site-customization/update-the-branding-and-visual-customization-settings-for-a-site)

建议先使用免费方案的基础设置：中文 UI、Clean 主题、正常正文宽度、清晰的章节层级和前后页导航。为一本以阅读为主的中文教材，预设拉丁字体之间的切换改善有限；只有明确需要让所有设备显示同一种中文字形时，再考虑支持自上传字体的套餐。

## 可以调什么，入口在哪里

进入 GitBook 侧栏中的站点，打开站点概览 → **Customization**。在此选择全站设置；如果对某个 section/variant 设置过覆盖值，它会继续覆盖全站值，需用 Reset 恢复继承。编辑后点击 **Save** 才会作用于已发布站点。[设置入口与保存](https://gitbook.com/docs/guides/customizing-your-site/how-to-customize-your-sites-theme)、[覆盖规则](https://gitbook.com/docs/manage-your-site/customization)

| 项目 | 官方已确认的能力 | 套餐与限制 |
| --- | --- | --- |
| 正文和 UI 字体 | Site styles → Font family → **Main font**；作用于正文及 UI | 预设字体选择标为 **Essential / Ultimate**，不属于普通 Free 的基础字体定制 |
| 页面标题及正文标题字体 | **Headings**；作用于 Page 标题和 H1/H2/H3；默认与 Main 相同 | 同属 Font family；可与正文分别选择字体家族，不等于可设置标题字号 |
| 代码字体 | **Monospace**；作用于代码块和 OpenAPI 块 | 预设字体选择标为 Essential / Ultimate |
| 自传中文字体 | **Add custom font**；常规和粗体字重都要提供；当前参考文档支持 `.woff`、`.woff2` | 该小节仅标 **Ultimate**；字体须有可用于网页嵌入的许可 |
| 正文字号 / title 字号 / 全站 scale | 未查到公开设置 | 公开 customization API 无 `fontSize`、`scale` 一类字段；不要把换字体误认为字号设置 |
| 行距 | 未查到公开设置 | 无独立 `lineHeight` 字段；源码中的排版类不是托管站点的配置入口 |
| 段间距 | 未查到公开设置 | 无独立段落 margin/gap 配置；不建议往正文插入空段落模拟全站样式 |
| 页面宽度 | 每页 **Page options → Layout** 中选择宽度，含 **Wide** | 页面文档未标专属付费套餐；不是任意 px 滑块，也不是全站中文行长设置 |
| 中文 UI | **Customization → Configure → Localize user interface / default language**，选择中文 | 基础配置文档未标付费限制；只翻译平台内建 UI，不翻译正文 |
| 主题及明暗模式 | Clean / Muted、主色、Tint、明暗模式开关与默认模式 | Clean 和 Muted 明确对所有站点可用；Bold / Gradient 为 Essential / Ultimate |
| 自定义 CSS / HTML / JS | 官方明确不支持直接注入 | **所有套餐都不支持**，不能通过升级解锁 |

字体能力及套餐标记来源：[Icons, colors, and themes → Site styles](https://gitbook.com/docs/manage-your-site/customization/icons-colors-and-themes#site-styles)。宽度来源：[Pages → Layout](https://gitbook.com/docs/create-content/content-structure/page#layout)。语言来源：[Extra configuration](https://gitbook.com/docs/manage-your-site/customization/extra-configuration#localize-user-interface)。未暴露的参数由上述产品文档与[公开定制 API schema](https://gitbook.com/docs/developers/gitbook-api/api-reference/docs-sites/site-customization/update-the-branding-and-visual-customization-settings-for-a-site)共同核对；结论是“未发现受支持的设置”，不是断言平台未来永远不会增加。

注意：一篇概览指南仍写自传字体要求 WOFF2，详细参考页则明确支持 WOFF 和 WOFF2。实际准备素材优先选 WOFF2；若已有 WOFF，以详细参考页及当前上传界面为准，本文不据此承诺任意字体文件都能上传。[概览指南](https://gitbook.com/docs/guides/customizing-your-site/how-to-make-a-great-looking-docs-site#fonts)、[详细参考](https://gitbook.com/docs/manage-your-site/customization/icons-colors-and-themes#custom-fonts)

## 中文字体：选 Noto Sans 不等于选思源黑体

官方公开 API 的预设正文字体包括 ABCFavorit、Inter、Roboto、Roboto Slab、Open Sans、Source Sans Pro、Lato、Ubuntu、Raleway、Merriweather、Overpass、Noto Sans、IBM Plex Serif、Poppins、Fira Sans。列表中没有 `Noto Sans SC` 或 `Noto Serif SC`。官方前端也把 `NotoSans` 映射为 Google Fonts 的 `noto-sans`，并非 `noto-sans-sc`。[API 字体枚举](https://gitbook.com/docs/developers/gitbook-api/api-reference/docs-sites/site-customization/update-the-branding-and-visual-customization-settings-for-a-site)、[字体定义源码](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/fonts/definitions.ts)

核对该源码提交的生成字体表，Noto Sans 的 Unicode 子集没有汉字常用区，字体链以 `system-ui, arial` 兜底；Inter 也使用这条兜底链。因此中文字符通常依赖浏览器及操作系统选择的可用字体，换 Inter / Roboto / Noto Sans 主要改变英文、数字及部分符号，不能据此保证汉字变成指定字体，也不能保证 Windows、macOS、Android 显示完全一致。[生成字体表](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/fonts/generated/faces.json)、[字体生成实现](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/fonts/default.ts)

如果具备 Ultimate，上传覆盖简体中文、拉丁字母、数学及标点字符的字体是原生路径；可评估 Noto Sans SC 等有合适许可的中文字体，同时提供 regular/bold。官方自传字体实现会在自定义字体后回退到 `sans-serif`，没有公开的编辑 CJK fallback 字体列表、逐语言指定字体或 Unicode 分片配置。没有核实字体上传大小上限、可变字体/CJK 超大字体的实际兼容性，选择前应在当前上传界面及真实页面验证。[自传字体实现](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/fonts/custom.ts)

## 宽度选项实际改变什么

官方文档特意说，Wide 为表格、卡片、代码等块提供更多空间。当前公开前端的普通内容容器是 `max-w-3xl`，Wide 容器是 `max-w-6xl`，而普通段落仍使用较窄的 `CONTENT_STYLE_REDUCED`；只有表格、图片、代码、tabs 等指定块会扩展。因此不能把 Wide 理解为“中文正文随窗口铺满”，也不应为了调整行长把所有页面盲目切 Wide。[容器源码](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/components/layout.ts)、[块宽度实现](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/components/DocumentView/Blocks.tsx)

字号和留白目前由前端固定的响应式样式控制，例如页面标题使用 `text-2xl` / `text-3xl` / `text-4xl`，正文块间隔在页面组件中指定。它们说明实现由平台管理，不能把源码值当作可写入 Git Sync 配置的参数。[页面标题实现](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/components/PageBody/PageHeader.tsx)、[页面块间距实现](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/components/PageBody/PageBody.tsx)

## 中文 language 设置的影响

官方确认语言设置会本地化搜索占位文字、按钮等非自定义 UI，不会自动翻译已有内容。公开前端还将内容 locale 写入 HTML 的 `lang` 属性，优先使用内容语言，旧 customization locale 作为兜底；该设置有助于浏览器和辅助技术理解页面语言。但未发现设置 `zh` 后自动加载中文字体、改变字号、行距或段间距的代码路径，不应把它当作“中文排版模式”。[产品说明](https://gitbook.com/docs/manage-your-site/customization/extra-configuration#localize-user-interface)、[locale 解析源码](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/intl/server.ts)、[HTML lang 和字体加载源码](https://github.com/GitbookIO/gitbook/blob/fa7d4a94f6d47cce5e2814ce74cf943bc5814413/packages/gitbook/src/components/RootLayout/CustomizationRootLayout.tsx)

## 免费和付费怎么选

- **Free 足以先完成**：GitHub Sync、按小节阅读、章节首页、基础主题/颜色、中文 UI、平台默认阅读版式；不为本次结构调整购买套餐。Free 官方包含 GitHub/GitLab Sync。[套餐说明](https://gitbook.com/docs/account-and-billing/plans)
- **Essential**：需要调整预设 Main / Headings / Monospace 字体、更多主题或品牌选项时再考虑。它解决不了任意 CSS、行距和段间距设置，也不支持自传中文字体。[字体及主题限制](https://gitbook.com/docs/manage-your-site/customization/icons-colors-and-themes)
- **Ultimate**：官方标注的自传字体路径；若主要目的是统一中文字体，需要评估这一档，而不是先购买 Essential。仍不支持直接插入 CSS。[字体限制](https://gitbook.com/docs/manage-your-site/customization/icons-colors-and-themes#custom-fonts)
- **Community**：符合条件的组织可申请免费享用 Ultimate 功能（SAML SSO 除外），并非个人学生或公开仓库自动获得。开源项目申请要求真正 OSS、有效 OSS LICENSE 等，不能为书稿擅自补一个开源许可来满足申请。个人笔记官方建议使用 Free。[Community 条件](https://gitbook.com/docs/account-and-billing/plans/community)
- **Sponsored**：不是确定可走的中文免费升级路线。官方说明仅对 Community 用户开放、需审核，且“主要语言不是英语”可能被拒；不把它计入本项目可保证的方案。[Sponsored 条件](https://gitbook.com/docs/account-and-billing/plans/community/sponsored-site-plan)

本调研没有登录用户的 GitBook 后台确认当前套餐，也没有试用自传中文字体或检查多设备实际字形。官方开源前端固定到 `fa7d4a94f6d47cce5e2814ce74cf943bc5814413`，可证明该版本的实现；托管服务上线版本和后续设置变化仍以当前后台为准。
