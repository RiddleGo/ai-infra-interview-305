# 第 293 题：`RoCE v2`的`ECN`和`PFC`拥塞控制？

## 题目

`RoCE v2`的`ECN`和`PFC`拥塞控制？

---

## 完整讲解

### 一、RoCE v2 与拥塞

**RoCE**（RDMA over Converged Ethernet）在以太网上跑 RDMA。**RoCE v2** 基于 **UDP**，可在标准 L3 网络部署。高速 RDMA 流量易造成**拥塞**与丢包，而 RDMA 对丢包敏感（重传与恢复代价大），因此需要**拥塞控制**与**无损或低损**能力。

### 二、ECN（显式拥塞通知）

**ECN**：交换机在队列超过阈值时对包打 **ECN 标记**（不改丢包），接收端通过 ACK 或 CNP 把「拥塞」反馈给发送端；发送端**降速**（如减窗口、降发送率），从而缓解拥塞。RoCE 场景下可与 DCQCN 等算法结合：接收端生成 CNP（Congestion Notification Packet）回给发送端，发送端根据 CNP 率调节发送速率。

### 三、PFC（Priority Flow Control）

**PFC**：基于**优先级**的**链路层流控**。当某优先级队列超过阈值，接收端向发送端发 **Pause**，发送端暂停该优先级发送，实现**无损**（不丢包）。代价是可能**头阻塞**、传播暂停。RoCE 常配合 PFC 做无损或低损，再配合 ECN/DCQCN 做端到端拥塞控制，平衡无丢包与公平性。

---

## 面试要点

- RoCE v2 = RDMA over UDP；需拥塞控制与无损/低损机制。
- ECN：交换机打标记、端到端反馈；发送端降速；可与 DCQCN 等结合。
- PFC：优先级流控、Pause 帧；实现无损、可能头阻塞。
- 工程上常 ECN + PFC 配合：PFC 保无损、ECN 做拥塞控制与公平性。

---

## 记忆要点

1. ECN = 拥塞标记 + 反馈 + 发送端降速；RoCE 常用 DCQCN。
2. PFC = 优先级 Pause、无损；可能头阻塞。
3. 二者配合：PFC 减丢包、ECN 控拥塞。

[返回模块](./README.md) | [返回总览](../README.md)
