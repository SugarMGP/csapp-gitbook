# CSAPP 两个上游仓库调研

调研日期：2026-11-19。检查对象是以下提交的浅克隆，统计排除 `.git/`，不修改上游内容。

- SunnyMaria/csapp-zh-markdown：`7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66`，默认分支 `main`。
- Hansimov/csapp：`49ec5b8fb885d1e273c84d22cad6196e9731239f`，默认分支 `master`。

## 结论

正文和自学实验资料应以 SunnyMaria 的已整理 Markdown 为主；借鉴 Hansimov 的书籍导航、按部分分章的层级，并保留其有补充价值的实验总览、Performance Lab 入口和官方示例代码入口。两份正文不是互补的两半，不应机械合并或重复收入：SunnyMaria 本身说明 OCR 源文件来自 Hansimov，而 Hansimov 的 2—6 章存在大量未完成页面。[来源：SunnyMaria README](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/README.md)、[Hansimov README](https://github.com/Hansimov/csapp/blob/49ec5b8fb885d1e273c84d22cad6196e9731239f/README.md)

“完整”的可验证范围是：上游已提供的前言、12 章、附录 A、参考文献、练习题答案和实验资料都进入阅读站，而且链接、图片和下载可用。检查并不证明每个 OCR 字符、公式和图示与正版纸书完全一致，也不等同于拥有公开转载授权。

## 内容覆盖与实测统计

| 项目 | SunnyMaria | Hansimov |
| --- | ---: | ---: |
| 全部文件 | 835 | 1,669 |
| Markdown 文件 | 501 | 128 |
| 图片文件 | 307 | 229 |
| 文件总字节 | 47,810,627 | 139,590,137 |
| 书籍导航入口 | 444 个独立正文/家庭作业小节，另有章目录、整章、答案等入口 | SUMMARY.md 中 125 个不同 Markdown 入口 |
| 正文范围 | 前言、1—12 章、附录 A、参考文献 | README 自述 1、7—12 章施工完成，2—6 章待施工；实际第 3 章已有 3.1—3.4 |
| 原书练习题答案 | 238 道，分布于 12 个独立答案文件 | 无对应完整独立答案集 |
| 实验 | 8 份中文说明、Y86-64 模拟器指南、8 个官方自学包 | 9 个实验简介，Data/Bomb 的额外说明和历史资料 |

统计由本地提交树计算；SunnyMaria 自带的三个标准库检查脚本全部通过：

```text
OK: 501 Markdown files, 1808 local links; paths, case and anchors checked
OK: 238 answers in 12 chapters; eight Markdown lab guides and verified archives
OK: 444 standalone sections exactly match their continuous chapters
```

这些检查分别覆盖本地路径/大小写/锚点、答案题号序列/代码围栏/实验包 SHA-256/归档成员读取、整章与独立小节的一致性。答案检查依赖上游写死的预期数量，不是逐题求解验证。[维护工具说明](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/维护工具/README.md)、[答案与实验检查实现](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/维护工具/tools/check_supplements.py)

### SunnyMaria 按章覆盖

以下“独立页”计入章导语、各级小节、章末参考文献说明和家庭作业，不计章目录、整章副本和答案页；前言 15 页、附录 3 页，加上 12 章的 426 页即为 444 页。

| 章 | 独立页 | 原书练习题答案 |
| --- | ---: | ---: |
| 1 计算机系统漫游 | 21 | 2 |
| 2 信息的表示和处理 | 42 | 54 |
| 3 程序的机器级表示 | 62 | 57 |
| 4 处理器体系结构 | 40 | 44 |
| 5 优化程序性能 | 30 | 12 |
| 6 存储器层次结构 | 31 | 21 |
| 7 链接 | 27 | 5 |
| 8 异常控制流 | 34 | 8 |
| 9 虚拟内存 | 59 | 10 |
| 10 系统级 I/O | 18 | 5 |
| 11 网络编程 | 26 | 5 |
| 12 并发编程 | 36 | 15 |

官方第三版目录列出 1—12 章、附录 A、练习题答案和参考文献，与此整理的范围吻合。提取官方前言 PDF 第 7—18 个物理页的目录编号，共 378 个；对照 SunnyMaria 的 12 份 `chapter.md`，有 377 个相同编号的 Markdown 标题，无额外编号，唯一没有保留编号的是 4.6.1。其 “Y86-64 Simulators” 内容实际位于 `4.6/4.6-summary.md` 内的二级标题“Y86-64 模拟器”，并非正文缺页。这证明了目录层级的覆盖，不能代替正文逐字校对。[官方目录与前言 PDF](https://csapp.cs.cmu.edu/3e/pieces/preface3e.pdf)、[4.6 正文](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/第04章-处理器体系结构/4.6/4.6-summary.md)

扫描 `TODO`、`TBD`、待补、待施工、尚未完成等词，未发现正文施工占位；“缺失”“占位符”的命中主要是习题原文及课程专用模板，不能删除。较短的章节父页通常只是对子小节的导语，也不是空正文。[实验中的模板差异说明](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/实验/COMPATIBILITY.md)

### Hansimov 的实际未完成范围

以下 10 个页面只有标题，无正文：

- 第 2 章的 2.2、2.3、2.4、2.5 和家庭作业。
- 第 4、5、6 章。
- 附录 A、参考文献。

第 2 章 2.1 只有约 2.8 KB 内容，尚不是完整的信息存储一节；第 3 章仅提供 3.1—3.4，缺少后续控制流、过程、数组、结构、机器代码、浮点代码等主要内容。GitBook 看起来有完整目录，不代表目录下的书稿齐全。[Hansimov SUMMARY](https://github.com/Hansimov/csapp/blob/49ec5b8fb885d1e273c84d22cad6196e9731239f/SUMMARY.md)、[第 2 章目录](https://github.com/Hansimov/csapp/tree/49ec5b8fb885d1e273c84d22cad6196e9731239f/part1/ch02-representing-and-manipulating-information)、[第 3 章目录](https://github.com/Hansimov/csapp/tree/49ec5b8fb885d1e273c84d22cad6196e9731239f/part1/ch03-machine-level-representing-of-programs)

## GitBook 和当前站点结构

Hansimov 根目录有 `SUMMARY.md`、正文 Markdown 和 `.gitbook/assets/`；没有 `book.json` 或可复现的本地构建配置，正文包含 GitBook Cloud 的 `{% page-ref %}`、`{% hint %}`、`{% tabs %}` 等指令，共扫描到 1,296 个 `{%` 块起点。复用其文件时必须检查构建器对这些语法的支持，不能直接假定普通 Markdown 引擎会渲染。[SUMMARY](https://github.com/Hansimov/csapp/blob/49ec5b8fb885d1e273c84d22cad6196e9731239f/SUMMARY.md)、[第 2 章的 hint 示例](https://github.com/Hansimov/csapp/blob/49ec5b8fb885d1e273c84d22cad6196e9731239f/part1/ch02-representing-and-manipulating-information/README.md)

SunnyMaria 现站使用 Quarto 1.9.38，`website/scripts/build.py` 从同一份书稿生成 QMD、导航和资源映射，GitHub Actions 校验并部署。原稿没有 GitBook 专用块；公式大多通过 Unicode 和 `<sup>/<sub>` 表达，未扫描到 `$$`、`\(`、`\[` 形式的数学定界符，存在 Markdown 脚注和少量 HTML 锚点。新阅读器重点验证上下标、脚注、代码、宽表格、图片和锚点即可，不必为原稿额外加入整套公式转换。[网站说明](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/website/README.md)、[生成器](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/website/scripts/build.py)

源书稿有 `README.md` 目录、`chapter.md` 整章和独立小节三套入口。搜索应只索引独立小节、答案和实验，避免把整章副本与章目录重复塞入结果；生成目录应读取章 README 的既有顺序，不能对 `1.10`、`1.2` 进行字符串排序。[上游阅读方式说明](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/README.md)

## 实验与配套文件的取舍

SunnyMaria 的八实验是 Data、Bomb、Attack、Architecture、Cache、Shell、Malloc、Proxy。官方实验页确认 Cache Lab 是 Performance Lab 的替代实验，但页面依然提供 Performance Lab 的简介和自学包，所以 Hansimov 的 Performance Lab 可以保留为“补充实验”，并明确它没有来自 SunnyMaria 的完整中文说明，避免把简介说成完整翻译。[官方实验页](https://csapp.cs.cmu.edu/3e/labs.html)、[Hansimov Performance Lab 简介](https://github.com/Hansimov/csapp/blob/49ec5b8fb885d1e273c84d22cad6196e9731239f/labs/perf-lab.md)

八个 `.tar` 应保持原始字节，沿用来源与 SHA-256 清单。部分实验仍需旧工具链、32 位库或 Python 2；Malloc 公开自学包只含两份短测试，不能把网站的“实验完整”解释为拥有全部课程评分文件。课程服务器地址、教师姓名、日期和 SITE-SPECIFIC 均来自模板，不是新仓库提供的服务。[包来源与校验值](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/实验/PACKAGES.md)、[兼容性说明](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/实验/COMPATIBILITY.md)

Hansimov `_codes/` 有 1,111 个文件、约 55.0 MB，其中含编译产物、共享库、备份和中间文件；`_labs/` 又有 183 个历史实验文件。这些不应为了“综合两个仓库”全部搬入阅读站。保留官方示例代码和实验资源入口，比发布重复、混杂的二进制文件更清晰。[Hansimov 实验总览](https://github.com/Hansimov/csapp/blob/49ec5b8fb885d1e273c84d22cad6196e9731239f/labs/labs-overview/README.md)、[官方示例代码](https://csapp.cs.cmu.edu/3e/code.html)

## 许可与归属事实

两个提交树都未发现 `LICENSE`、`COPYING` 或 `NOTICE` 文件，GitHub 仓库 API 的 `license` 字段也都是 `null`。README 的致谢和公开可见状态不是开源许可。书籍官方前言 PDF 的版权页写明 Pearson 保留权利，并对复制、传播提出许可要求。整合仓库应保留作者、出版社、译者和两个整理仓库的归属，明确区分“新增工具代码的许可”与“上游书稿/图片/实验材料的既有权利”，不要给全仓套一个 MIT/CC 许可证。[SunnyMaria README](https://github.com/SunnyMaria/csapp-zh-markdown/blob/7fe0d4f79d65ba63cc3c8723c24d2d2e99b84c66/README.md)、[Hansimov README](https://github.com/Hansimov/csapp/blob/49ec5b8fb885d1e273c84d22cad6196e9731239f/README.md)、[官方前言版权页](https://csapp.cs.cmu.edu/3e/pieces/preface3e.pdf)

这些是来源调查结果，不构成对用户具体再发布权利的法律判断。

## 建议保留的自动化

1. 保存两上游仓库 URL、固定提交和各自负责的内容范围；读取固定提交生成书稿和目录，保证可复现。
2. 自动生成 `SUMMARY.md`，覆盖所有正文、家庭作业、答案、附录、参考文献和实验；保留图片和下载包的相对路径。
3. 运行上游原有三个检查，构建后再检查 HTML 本地链接、锚点和资源；只有通过才发布 GitHub Pages。
4. 如自动跟踪上游，使用更新分支或 PR 展示真实变更，并在检查通过后由维护者合并；避免定时任务直接覆盖本仓维护的界面和说明。

未执行实验程序，未逐字对照正版全书，也未对外部历史链接做全站存活保证。仅完成源码、文件、上游自检和官方目录/实验页核对。
