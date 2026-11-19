# CSAPP GitBook

《深入理解计算机系统》第三版中文阅读站：整合 [SunnyMaria/csapp-zh-markdown](https://github.com/SunnyMaria/csapp-zh-markdown) 的正文和 [Hansimov/csapp](https://github.com/Hansimov/csapp) 的补充资料，用 HonKit 构建 GitBook 风格站点。

**[在线阅读](https://sugarmgp.github.io/csapp-gitbook/)** · [书籍目录](book/SUMMARY.md) · [资料来源与权利归属](book/SOURCES.md) · [调研记录](docs/source-research.md)

收录前言、第 1—12 章、附录 A、参考文献、238 道原书练习题答案、8 个实验的中文说明及自学包，以及 Performance Lab、实验 FAQ、Data/Bomb Lab 补充 README 和示例代码包。保留逐节阅读与整章阅读，支持中文全文搜索、字体调整、深色模式和手机阅读。

“完整”指上游已有正文的小节覆盖和配套资料完整，不代表逐字校对了正版出版物，也不包含家庭作业或实验解答。

## 本地阅读

需要 Node.js 24 和 Python 3.13。

```sh
npm ci
npm run serve
```

访问 http://localhost:4000。只构建静态网页：

```sh
npm test
npm run build
npm run check
```

生成结果在 `_book/`，可用任意静态服务器托管。

## 自动化

- 推送到 `main`：校验内容、构建并发布 GitHub Pages。
- Pull Request：执行相同校验和构建。
- 每周一北京时间 09:23：检查两个上游的新版本，通过校验后生成更新 PR，人工合并后发布。
- Actions → **Sync upstream** → **Run workflow**：随时手动检查上游。

没有上游变化时不创建 PR。本仓库已允许 GitHub Actions 创建 Pull Request；新建副本时需在 Settings → Actions → General 中启用该权限。GitHub 的定时任务可能延迟；长期无仓库活动时，公开仓库的定时工作流可能被平台暂停。

固定来源版本在 `sources.json`，导入文件及 SHA-256 在 `book-manifest.json`。重新生成相同版本：`npm run sync`；更新到上游最新版本：`npm run sync:update`。

## 修改方式

`book/` 是自动生成目录。正文修正应先提交到对应上游；本站首页、补充资料入口和样式分别维护在 `site/README.md`、`site/supplements.md`、`site/styles/website.css`，导入与目录规则维护在 `scripts/sync.py`，再运行 `npm run sync`。阅读器适配维护在 `plugins/csapp/`，侧栏模板和中文界面文字维护在 `site/_layouts/`、`site/_i18n/`。不要直接修改生成文件，否则下一次同步会覆盖它们。

`.gitbook.yaml` 和标准 `SUMMARY.md` 可用于 GitBook 的 Git Sync。GitHub Pages 是本仓库已经配置的部署方式；如另需 GitBook.com 托管，需在自己的 GitBook 账号中连接此仓库，其平台主题与这里的 HonKit CSS 分别配置。

## 致谢与权利

感谢原书作者 Randal E. Bryant、David R. O’Hallaron，以及 SunnyMaria、Hansimov 和各位贡献者。SunnyMaria 的 OCR 基础同样来自 Hansimov。

两上游仓库未提供 LICENSE，书籍、中文译文、图片、代码包和实验材料仍归各自权利人所有。本仓库不授予这些材料额外的转载或再许可权限。详见[资料来源与权利归属](book/SOURCES.md)。
