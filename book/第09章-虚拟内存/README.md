# 第 9 章 虚拟内存

一个系统中的进程是与其他进程共享 CPU 和主存资源的。然而，共享主存会形成一些特殊的挑战。随着对 CPU 需求的增长，进程以某种合理的平滑方式慢了下来。但是如果太多的进程需要太多的内存，那么它们中的一些就根本无法运行。当一个程序没有空间可用时，那就是它运气不好了。内存还很容易被破坏。如果某个进程不小心写了另一个进程使用的内存，它就可能以某种完全和程序逻辑无关的令人迷惑的方式失败。

为了更加有效地管理内存并且少出错，现代系统提供了一种对主存的抽象概念，叫做虚拟内存（VM）。虚拟内存是硬件异常、硬件地址翻译、主存、磁盘文件和内核软件的完美交互，它为每个进程提供了一个大的、一致的和私有的地址空间。通过一个很清晰的机制，虚拟内存提供了三个重要的能力：1）它将主存看成是一个存储在磁盘上的地址空间的高速缓存，在主存中只保存活动区域，并根据需要在磁盘和主存之间来回传送数据，通过这种方式，它高效地使用了主存。2）它为每个进程提供了一致的地址空间，从而简化了内存管理。3）它保护了每个进程的地址空间不被其他进程破坏。

虚拟内存是计算机系统最重要的概念之一。它成功的一个主要原因就是因为它是沉默地、自动地工作的，不需要应用程序员的任何干涉。既然虚拟内存在幕后工作得如此之好，为什么程序员还需要理解它呢？有以下几个原因：

- **虚拟内存是核心的。** 虚拟内存遍及计算机系统的所有层面，在硬件异常、汇编器、链接器、加载器、共享对象、文件和进程的设计中扮演着重要角色。理解虚拟内存将帮助你更好地理解系统通常是如何工作的。
- **虚拟内存是强大的。** 虚拟内存给予应用程序强大的能力，可以创建和销毁内存片（chunk）、将内存片映射到磁盘文件的某个部分，以及与其他进程共享内存。比如，你知道可以通过读写内存位置读或者修改一个磁盘文件的内容吗？或者可以加载一个文件的内容到内存中，而不需要进行任何显式地复制吗？理解虚拟内存将帮助你利用它的强大功能在应用程序中添加动力。
- **虚拟内存是危险的。** 每次应用程序引用一个变量、间接引用一个指针，或者调用一个诸如 `malloc` 这样的动态分配程序时，它就会和虚拟内存发生交互。如果虚拟内存使用不当，应用将遇到复杂危险的与内存有关的错误。例如，一个带有错误指针的程序可以立即崩溃于“段错误”或者“保护错误”，它可能在崩溃之前还默默地运行了几个小时，或者是最令人惊慌地，运行完成却产生不正确的结果。理解虚拟内存以及诸如 `malloc` 之类的管理虚拟内存的分配程序，可以帮助你避免这些错误。

这一章从两个角度来看虚拟内存。本章的前一部分描述虚拟内存是如何工作的。后一部分描述的是应用程序如何使用和管理虚拟内存。无可避免的事实是虚拟内存很复杂，本章很多地方都反映了这一点。好消息就是如果你掌握这些细节，你就能够手工模拟一个小系统的虚拟内存机制，而且虚拟内存的概念将永远不再神秘。

第二部分是建立在这种理解之上的，向你展示了如何在程序中使用和管理虚拟内存。你将学会如何通过显式的内存映射和对像 `malloc` 程序这样的动态内存分配器的调用来管理虚拟内存。你还将了解到 C 程序中的大多数常见的与内存有关的错误，并学会如何避免它们的出现。

## 小节目录

- [9.1 物理和虚拟寻址](9.1/9.1-physical-and-virtual-addressing.md)
- [9.2 地址空间](9.2/9.2-address-spaces.md)
- [9.3 虚拟内存作为缓存的工具](9.3/9.3-vm-as-a-tool-for-caching.md)
  - [9.3.1 DRAM 缓存的组织结构](9.3/9.3.1-dram-cache-organization.md)
  - [9.3.2 页表](9.3/9.3.2-page-tables.md)
  - [9.3.3 页命中](9.3/9.3.3-page-hits.md)
  - [9.3.4 缺页](9.3/9.3.4-page-faults.md)
  - [9.3.5 分配页面](9.3/9.3.5-allocating-pages.md)
  - [9.3.6 又是局部性救了我们](9.3/9.3.6-locality-to-the-rescue-again.md)
- [9.4 虚拟内存作为内存管理的工具](9.4/9.4-vm-as-a-tool-for-memory-management.md)
- [9.5 虚拟内存作为内存保护的工具](9.5/9.5-vm-as-a-tool-for-memory-protection.md)
- [9.6 地址翻译](9.6/9.6-address-translation.md)
  - [9.6.1 结合高速缓存和虚拟内存](9.6/9.6.1-integrating-caches-and-vm.md)
  - [9.6.2 利用 TLB 加速地址翻译](9.6/9.6.2-speeding-up-address-translation-with-a-tlb.md)
  - [9.6.3 多级页表](9.6/9.6.3-multi-level-page-tables.md)
  - [9.6.4 综合：端到端的地址翻译](9.6/9.6.4-putting-it-together-end-to-end-address-translation.md)
- [9.7 案例研究：Intel Core i7/Linux 内存系统](9.7/9.7-case-study-the-intel-core-i7-linux-memory-system.md)
  - [9.7.1 Core i7 地址翻译](9.7/9.7.1-core-i7-address-translation.md)
  - [9.7.2 Linux 虚拟内存系统](9.7/9.7.2-linux-virtual-memory-system.md)
- [9.8 内存映射](9.8/9.8-memory-mapping.md)
  - [9.8.1 再看共享对象](9.8/9.8.1-revisiting-shared-objects.md)
  - [9.8.2 再看 fork 函数](9.8/9.8.2-revisiting-the-fork-function.md)
  - [9.8.3 再看 execve 函数](9.8/9.8.3-revisiting-the-execve-function.md)
  - [9.8.4 使用 mmap 函数的用户级内存映射](9.8/9.8.4-user-level-memory-mapping-with-the-mmap-function.md)
- [9.9 动态内存分配](9.9/9.9-dynamic-memory-allocation.md)
  - [9.9.1 `malloc` 和 `free` 函数](9.9/9.9.1-malloc-and-free-functions.md)
  - [9.9.2 为什么要使用动态内存分配](9.9/9.9.2-why-dynamic-memory-allocation.md)
  - [9.9.3 分配器的要求和目标](9.9/9.9.3-allocator-requirements-and-goals.md)
  - [9.9.4 碎片](9.9/9.9.4-fragmentation.md)
  - [9.9.5 实现问题](9.9/9.9.5-implementation-issues.md)
  - [9.9.6 隐式空闲链表](9.9/9.9.6-implicit-free-lists.md)
  - [9.9.7 放置已分配的块](9.9/9.9.7-placing-allocated-blocks.md)
  - [9.9.8 分割空闲块](9.9/9.9.8-splitting-free-blocks.md)
  - [9.9.9 获取额外的堆内存](9.9/9.9.9-acquiring-additional-heap-memory.md)
  - [9.9.10 合并空闲块](9.9/9.9.10-coalescing-free-blocks.md)
  - [9.9.11 带边界标记的合并](9.9/9.9.11-coalescing-with-boundary-tags.md)
  - [9.9.12 综合：实现一个简单的分配器](9.9/9.9.12-putting-it-together.md)
  - [9.9.13 显式空闲链表](9.9/9.9.13-explicit-free-lists.md)
  - [9.9.14 分离的空闲链表](9.9/9.9.14-segregated-free-lists.md)
- [9.10 垃圾收集](9.10/9.10-garbage-collection.md)
  - [9.10.1 垃圾收集器的基本知识](9.10/9.10.1-garbage-collector-basics.md)
  - [9.10.2 Mark & Sweep 垃圾收集器](9.10/9.10.2-mark-and-sweep-garbage-collector.md)
  - [9.10.3 C 程序的保守 Mark & Sweep](9.10/9.10.3-conservative-mark-and-sweep-for-c.md)
- [9.11 C 程序中常见的与内存有关的错误](9.11/9.11-common-memory-related-errors-in-c-programs.md)
  - [9.11.1 间接引用坏指针](9.11/9.11.1-dereferencing-bad-pointers.md)
  - [9.11.2 读未初始化的内存](9.11/9.11.2-reading-uninitialized-memory.md)
  - [9.11.3 允许栈缓冲区溢出](9.11/9.11.3-stack-buffer-overflows.md)
  - [9.11.4 假设指针和它们指向的对象是相同大小的](9.11/9.11.4-assuming-pointers-and-objects-have-the-same-size.md)
  - [9.11.5 造成错位错误](9.11/9.11.5-off-by-one-errors.md)
  - [9.11.6 引用指针，而不是它所指向的对象](9.11/9.11.6-referencing-the-pointer-instead-of-the-object.md)
  - [9.11.7 误解指针运算](9.11/9.11.7-misunderstanding-pointer-arithmetic.md)
  - [9.11.8 引用不存在的变量](9.11/9.11.8-referencing-nonexistent-variables.md)
  - [9.11.9 引用空闲堆块中的数据](9.11/9.11.9-referencing-data-in-freed-heap-blocks.md)
  - [9.11.10 引起内存泄漏](9.11/9.11.10-memory-leaks.md)
- [9.12 小结](9.12/9.12-summary.md)
- [参考文献说明](9.12/references.md)
- [家庭作业](homework/9.11-9.13-address-translation.md)
- [家庭作业（续）](homework/9.14-9.20-memory-mapping-and-allocation.md)

## 练习题答案

[查看本章练习题答案](练习题答案.md)
