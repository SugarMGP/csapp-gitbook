# 连接 GitBook 官方平台

仓库已经整理成 GitBook 原生 Git Sync 可读取的 Markdown 结构。登录并授权连接后即可使用 GitBook 默认主题发布。

## 接入参数

| 配置 | 值 |
| --- | --- |
| Repository | `SugarMGP/csapp-gitbook` |
| Branch | `main` |
| Project directory | 仓库根目录，留空或 `./` |
| 站点配置 | 根目录 `gitbook-docs.yaml` |
| 空间的 Content directory | `./book`（站点配置已指定） |
| 首次同步方向 | **GitHub → GitBook** |
| 空间内容配置 | `book/.gitbook.yaml`，其中 `root: ./` |
| 实际正文目录 | `book/` |
| 首页与目录 | `book/README.md`、`book/SUMMARY.md` |

GitBook 先读取根目录的 `gitbook-docs.yaml`，把默认中文空间映射到 `book/`，再读取 `book/.gitbook.yaml`。后者的 `root: ./` 是相对于 `book/` 的路径，因此首页和目录分别为 `book/README.md`、`book/SUMMARY.md`，不会重复拼成 `book/book/`。

`gitbook-docs.yaml` 的空间 `key: csapp-zh` 在首次导入后应保持不变；修改 key 会创建新的空间。

## 操作步骤

1. 打开 [GitBook](https://app.gitbook.com/)，登录自己的账号，创建新的文档站点与空间，例如“CSAPP 中文版”。
2. 打开站点侧栏的 **Git Sync**（空间级入口可能显示 **Set up Git Sync**）。连接 GitHub，选择上述仓库和分支。
3. 如果列表没有该仓库，安装或配置 [GitBook GitHub App](https://github.com/apps/gitbook-com)，为它选择 `csapp-gitbook` 仓库。
4. Project directory 留空或填 `./`，刷新该字段以重新读取 `main` 分支。页面应读到 `gitbook-docs.yaml` 并显示指向 `./book` 的默认中文空间；首次方向选择 **GitHub → GitBook**，再开始同步。
5. 检查十二章、练习题答案和实验入口，然后使用 GitBook 的默认主题发布。

Git Sync 会双向同步。这里以 GitHub 导入书稿作为初始内容，因此首次不要选择反向导出，以免空白空间覆盖已有书稿。

## 更新方式

仓库每周检查上游并创建待审查的更新 PR。合并到 `main` 后，GitBook 会自动同步。正文和目录由脚本生成，修改方式见[仓库维护说明](../README.md#本地维护)。

## 官方文档

- [启用 GitHub Sync](https://gitbook.com/docs/docs-as-code/git-sync/enabling-github-sync)
- [内容根目录和 SUMMARY 配置](https://gitbook.com/docs/docs-as-code/git-sync/content-configuration)
- [站点目录与空间映射](https://gitbook.com/docs/docs-as-code/git-sync/monorepos)
- [站点配置官方 schema](https://api.gitbook.com/gitbook-docs.yaml)
- [从 Git 仓库导入已有资料](https://gitbook.com/docs/guides/editing-and-publishing-documentation/import-or-migrate-your-content-to-gitbook-with-git-sync)
