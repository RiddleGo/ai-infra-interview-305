# 第 292 题：InfiniBand的`Verbs`编程？`ibv_post_send`？

## 题目

InfiniBand的`Verbs`编程？`ibv_post_send`？

---

## 完整讲解

### 一、InfiniBand Verbs 简介

**Verbs** 是 InfiniBand（以及 RoCE 等 RDMA）的**编程接口**，提供队列对（QP）、完成队列（CQ）、内存注册（MR）等抽象。用户态应用通过 Verbs API 提交**发送/接收**请求（WR），网卡异步执行，通过 CQ 或轮询获知完成。实现**零拷贝、内核旁路**的 RDMA 通信。

### 二、ibv_post_send

**ibv_post_send** 把**发送请求**（Send WR）挂到**发送队列（SQ）**上。每个 WR 描述「要发送的数据在哪、多长、什么操作」（如 Send、RDMA Write、RDMA Read 等）。网卡消费 SQ，将数据从本地 MR 发到对端；完成后在 CQ 产生 CQE。典型流程：**注册内存**（ibv_reg_mr）→ 建 QP、CQ → **ibv_post_send** 投递 WR → 轮询或等待 **ibv_poll_cq** 得到完成。

### 三、配套 API

ibv_post_recv：投递接收 WR，用于接收消息或 RDMA Read 的 target。ibv_reg_mr：注册内存供 RDMA 访问。ibv_create_qp、ibv_create_cq：建 QP/CQ。连接建立后（CM 或 socket 交换 QP 信息）即可 post_send/post_recv 做双向通信。

---

## 面试要点

- Verbs = IB/RDMA 编程接口；QP、CQ、MR；零拷贝、内核旁路。
- ibv_post_send：把发送 WR 投到 SQ；描述数据位置、长度、操作类型（Send/Write/Read）。
- 流程：reg_mr → create_qp/cq → 建连 → post_send/post_recv → poll_cq。
- 配套：ibv_post_recv、ibv_reg_mr、ibv_create_qp、ibv_poll_cq。

---

## 记忆要点

1. Verbs = QP/CQ/MR；post_send 投发送 WR。
2. WR 描述 buffer、长度、操作；完成后 CQ 产生 CQE。
3. 流程：注册内存、建 QP/CQ、建连、post、poll。

[返回模块](./README.md) | [返回总览](../README.md)
