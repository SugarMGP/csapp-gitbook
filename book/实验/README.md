# 实验资料

八个实验按推荐学习顺序排列。每张卡片进入中文说明，实验包可在下方直接下载。

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody>
<tr><td><strong>Data Lab</strong></td><td>用受限的 C 语言运算完成位级操作。</td><td><a href="datalab-zh/datalab-zh.md">datalab-zh/datalab-zh.md</a></td></tr>
<tr><td><strong>Bomb Lab</strong></td><td>阅读汇编代码，逐阶段拆解二进制炸弹。</td><td><a href="bomblab-zh/bomblab-zh.md">bomblab-zh/bomblab-zh.md</a></td></tr>
<tr><td><strong>Attack Lab</strong></td><td>理解缓冲区溢出、代码注入与 ROP。</td><td><a href="attacklab-zh/attacklab-zh.md">attacklab-zh/attacklab-zh.md</a></td></tr>
<tr><td><strong>Architecture Lab</strong></td><td>实现并优化 Y86-64 流水线处理器。</td><td><a href="archlab-zh/archlab-zh.md">archlab-zh/archlab-zh.md</a></td></tr>
<tr><td><strong>Cache Lab</strong></td><td>编写高速缓存模拟器并优化矩阵转置。</td><td><a href="cachelab-zh/cachelab-zh.md">cachelab-zh/cachelab-zh.md</a></td></tr>
<tr><td><strong>Shell Lab</strong></td><td>实现带作业控制的 Unix shell。</td><td><a href="shlab-zh/shlab-zh.md">shlab-zh/shlab-zh.md</a></td></tr>
<tr><td><strong>Malloc Lab</strong></td><td>实现正确、高效的动态内存分配器。</td><td><a href="malloclab-zh/malloclab-zh.md">malloclab-zh/malloclab-zh.md</a></td></tr>
<tr><td><strong>Proxy Lab</strong></td><td>实现支持缓存的并发 Web 代理。</td><td><a href="proxylab-zh/proxylab-zh.md">proxylab-zh/proxylab-zh.md</a></td></tr>
</tbody></table>

## 实验包下载

{% file src="datalab-zh/datalab-handout.tar" %}
Data Lab 官方自学包
{% endfile %}

{% file src="bomblab-zh/bomb.tar" %}
Bomb Lab 官方自学包
{% endfile %}

{% file src="attacklab-zh/target1.tar" %}
Attack Lab 官方自学包
{% endfile %}

{% file src="archlab-zh/archlab-handout.tar" %}
Architecture Lab 官方自学包
{% endfile %}

{% file src="cachelab-zh/cachelab-handout.tar" %}
Cache Lab 官方自学包
{% endfile %}

{% file src="shlab-zh/shlab-handout.tar" %}
Shell Lab 官方自学包
{% endfile %}

{% file src="malloclab-zh/malloclab-handout.tar" %}
Malloc Lab 官方自学包
{% endfile %}

{% file src="proxylab-zh/proxylab-handout.tar" %}
Proxy Lab 官方自学包
{% endfile %}

## 配套指南

{% content-ref url="archlab-zh/simguide-zh.md" %}
[Y86-64 处理器模拟器指南](archlab-zh/simguide-zh.md)
{% endcontent-ref %}

{% content-ref url="PACKAGES.md" %}
[实验包来源与校验值](PACKAGES.md)
{% endcontent-ref %}

{% content-ref url="COMPATIBILITY.md" %}
[自学实验包与说明模板的差异](COMPATIBILITY.md)
{% endcontent-ref %}

## 版本与使用说明

资料来源：[CS:APP3e 官方实验页面](https://csapp.cs.cmu.edu/3e/labs.html)。本目录选用 64 位 Attack Lab 与 Y86-64 Architecture Lab；Cache Lab 对应官方课程中替代 Performance Lab 的实验。

这里提供实验说明的中文翻译，不包含实验解答。原说明中的课程日期、教师信息、提交地址及 `SITE-SPECIFIC` 等占位内容保留原意；自学者应以实际使用的实验包及课程安排为准。

{% hint style="warning" %}
官方自学 Bomb Lab 已关闭向评分服务器报告的功能；自学 Attack Lab 运行目标程序时需使用 `-q`，避免连接不存在的评分服务器。
{% endhint %}
