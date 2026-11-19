# 连接 GitBook 官方平台

仓库已经整理成 GitBook 原生 Git Sync 可读取的 Markdown 结构。登录并授权连接后即可使用 GitBook 默认主题发布。

## 接入参数

| 配置 | 值 |
| --- | --- |
| Repository | `SugarMGP/csapp-gitbook` |
| Branch | `main` |
| Project directory | 仓库根目录，留空或 `./` |
| 空间的 Content directory | `./`（仓库根目录） |
| 首次同步方向 | **GitHub → GitBook** |
| 内容配置 | 根目录 `.gitbook.yaml` |
| 实际正文目录 | `book/` |
| 首页与目录 | `book/README.md`、`book/SUMMARY.md` |

空间映射到根目录后，`.gitbook.yaml` 的 `root: ./book/` 会选择正文。不要再把同一个空间映射到 `book/` 后重复套用 `root: ./book/`。

## 操作步骤

1. 打开 [GitBook](https://app.gitbook.com/)，登录自己的账号，创建新的文档站点与空间，例如“CSAPP 中文版”。
2. 打开站点侧栏的 **Git Sync**（空间级入口可能显示 **Set up Git Sync**）。连接 GitHub，选择上述仓库和分支。
3. 如果列表没有该仓库，安装或配置 [GitBook GitHub App](https://github.com/apps/gitbook-com)，为它选择 `csapp-gitbook` 仓库。
4. 按上表设置目录，首次选择 **GitHub → GitBook**，再开始同步。这样会把已准备好的完整书稿导入新空间。
5. 检查十二章、练习题答案和实验入口，然后使用 GitBook 的默认主题发布。

Git Sync 会双向同步。这里以 GitHub 导入书稿作为初始内容，因此首次不要选择反向导出，以免空白空间覆盖已有书稿。

## 更新方式

仓库每周检查上游并创建待审查的更新 PR。合并到 `main` 后，GitBook 会自动同步。正文和目录由脚本生成，修改方式见[仓库维护说明](../README.md#本地维护)。

## 官方文档

- [启用 GitHub Sync](https://gitbook.com/docs/docs-as-code/git-sync/enabling-github-sync)
- [内容根目录和 SUMMARY 配置](https://gitbook.com/docs/docs-as-code/git-sync/content-configuration)
- [从 Git 仓库导入已有资料](https://gitbook.com/docs/guides/editing-and-publishing-documentation/import-or-migrate-your-content-to-gitbook-with-git-sync)
