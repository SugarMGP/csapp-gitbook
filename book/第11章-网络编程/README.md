# 第 11 章 网络编程

网络应用随处可见。任何时候浏览 Web、发送 email 信息或是玩在线游戏，你就正在使用网络应用程序。有趣的是，所有的网络应用都是基于相同的基本编程模型，有着相似的整体逻辑结构，并且依赖相同的编程接口。

网络应用依赖于很多在系统研究中已经学习过的概念。例如，进程、信号、字节顺序、内存映射以及动态内存分配，都扮演着重要的角色。还有一些新概念要掌握。我们需要理解基本的客户端-服务器编程模型，以及如何编写使用因特网提供的服务的客户端-服务器程序。最后，我们将把所有这些概念结合起来，开发一个虽小但功能齐全的 Web 服务器，能够为真实的 Web 浏览器提供静态和动态的文本和图形内容。

## 小节目录

- [11.1 客户端-服务器编程模型](11.1/11.1-client-server-programming-model.md)
- [11.2 网络](11.2/11.2-networks.md)
- [11.3 全球 IP 因特网](11.3/11.3-global-ip-internet.md)
  - [11.3.1 IP 地址](11.3/11.3.1-ip-addresses.md)
  - [11.3.2 因特网域名](11.3/11.3.2-internet-domain-names.md)
  - [11.3.3 因特网连接](11.3/11.3.3-internet-connections.md)
- [11.4 套接字接口](11.4/11.4-socket-interface.md)
  - [11.4.1 套接字地址结构](11.4/11.4.1-socket-address-structures.md)
  - [11.4.2 `socket` 函数](11.4/11.4.2-socket-function.md)
  - [11.4.3 `connect` 函数](11.4/11.4.3-connect-function.md)
  - [11.4.4 `bind` 函数](11.4/11.4.4-bind-function.md)
  - [11.4.5 `listen` 函数](11.4/11.4.5-listen-function.md)
  - [11.4.6 `accept` 函数](11.4/11.4.6-accept-function.md)
  - [11.4.7 主机和服务的转换](11.4/11.4.7-host-and-service-conversion.md)
  - [11.4.8 套接字接口的辅助函数](11.4/11.4.8-socket-interface-helper-functions.md)
  - [11.4.9 `echo` 客户端和服务器的示例](11.4/11.4.9-echo-client-and-server-example.md)
- [11.5 Web 服务器](11.5/11.5-web-servers.md)
  - [11.5.1 Web 基础](11.5/11.5.1-web-basics.md)
  - [11.5.2 Web 内容](11.5/11.5.2-web-content.md)
  - [11.5.3 HTTP 事务](11.5/11.5.3-http-transactions.md)
  - [11.5.4 服务动态内容](11.5/11.5.4-serving-dynamic-content.md)
- [11.6 综合：TINY Web 服务器](11.6/11.6-putting-it-together-the-tiny-web-server.md)
- [11.7 小结](11.7/11.7-summary.md)
- [参考文献说明](11.7/references.md)
- [家庭作业](homework/11.6-11.13-network-programming.md)

## 练习题答案

[查看本章练习题答案](练习题答案.md)
