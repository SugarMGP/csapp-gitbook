# CSAPP GitBook

《深入理解计算机系统》第三版中文书稿：整合 [SunnyMaria/csapp-zh-markdown](https://github.com/SunnyMaria/csapp-zh-markdown) 的正文和 [Hansimov/csapp](https://github.com/Hansimov/csapp) 的补充资料，通过 Git Sync 导入 GitBook，使用 GitBook 官方默认主题阅读。

**[书籍目录](book/SUMMARY.md)** · [连接 GitBook](docs/gitbook-setup.md) · [中文排版调研](docs/gitbook-chinese-typography.md) · [资料来源与权利归属](book/SOURCES.md) · [调研记录](docs/source-research.md)

仓库通过根目录 `gitbook-docs.yaml` 配置站点，将默认中文空间映射到 `book/`。

收录前言、第 1—12 章、附录 A、参考文献、238 道原书练习题答案、8 个实验的中文说明及自学包，以及 Performance Lab、实验 FAQ、Data/Bomb Lab 补充 README 和示例代码包。各章开篇正文直接放在章首页，下面按小节阅读；目录、搜索和外观使用 GitBook 原生功能。

“完整”指上游已有正文的小节覆盖和配套资料完整，不代表逐字校对了正版出版物，也不包含家庭作业或实验解答。

## 本地维护

需要 Python 3.13 和 Git。导入与链接检查使用标准库；配置测试使用 PyYAML、jsonschema 解析 YAML 并验证官方 schema。

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/check_book.py
```

重新导入固定版本，或检查上游更新：

```sh
python scripts/sync.py
python scripts/sync.py --update
```

生成结果在 `book/`，由 GitBook Git Sync 读取。

## 自动化

- 推送到 `main` 或 Pull Request：验证站点配置的官方 schema、空间目录映射、页面标题、导航、内容清单、8 个实验包及 Markdown 链接、图片和锚点。
- 每周一北京时间 09:23：检查两个上游的新版本，通过校验后生成更新 PR。
- 合并更新 PR 后，已连接的 GitBook 会通过 Git Sync 导入主分支变化。
- Actions → **Sync upstream** → **Run workflow**：随时手动检查上游。

没有上游变化时不创建 PR。本仓库已允许 GitHub Actions 创建 Pull Request；新建副本时需在 Settings → Actions → General 中启用该权限。GitHub 的定时任务可能延迟；长期无仓库活动时，公开仓库的定时工作流可能被平台暂停。

固定来源版本在 `sources.json`，导入文件及 SHA-256 在 `book-manifest.json`。更新 PR 需要人工审查、合并。

## 修改方式

`book/` 是自动生成目录。正文修正优先提交对应上游；首页、补充资料入口和空间配置维护在 `templates/`，导入与目录规则维护在 `scripts/sync.py`，修改后运行 `python scripts/sync.py`。导入会统一页面标题层级，并用 GitBook 的导航标签语法保留简短目录名。直接在 `book/` 或 GitBook 中修改导入正文，会被下一次同步生成的内容覆盖；更新 PR 会展示这些差异，供合并前审查。

连接 `SugarMGP/csapp-gitbook` 的 `main` 分支，Project directory 留空或填 `./`。根目录 `gitbook-docs.yaml` 会把空间映射到 `./book`，其中的 `.gitbook.yaml` 再读取首页和 `SUMMARY.md`；首次同步选择 **GitHub → GitBook**。具体操作见[GitBook 接入说明](docs/gitbook-setup.md)。

## 致谢与权利

感谢原书作者 Randal E. Bryant、David R. O’Hallaron，以及 SunnyMaria、Hansimov 和各位贡献者。SunnyMaria 的 OCR 基础同样来自 Hansimov。

两上游仓库未提供 LICENSE，书籍、中文译文、图片、代码包和实验材料仍归各自权利人所有。本仓库不授予这些材料额外的转载或再许可权限。详见[资料来源与权利归属](book/SOURCES.md)。
