# 第 92 题：RDMA技术原理？`RoCE v1` vs `RoCE v2` vs `InfiniBand`？

## 题目

RDMA技术原理？`RoCE v1` vs `RoCE v2` vs `InfiniBand`？

---

## 完整讲解

### 一、RDMA 原理

**RDMA**（Remote Direct Memory Access）：**绕过 CPU 与内核**，网卡直接读写对端内存，零拷贝、低延迟、高带宽，适合大规模分布式训练。**InfiniBand** 与 **RoCE**（RDMA over Converged Ethernet）是两种常见实现：IB 专用网络，RoCE 跑在以太网上。

### 二、InfiniBand

**InfiniBand**：原生 RDMA 网络，专用网卡与交换机，**延迟最低、带宽高**（如 200 Gb/s），需 IB 硬件。多机训练集群常用。

### 三、RoCE v1 vs RoCE v2

- **RoCE v1**：RDMA over **无损以太网**（Layer 2），同一 L2 域内；依赖数据中心无损以太网（PFC 等），配置要求高。
- **RoCE v2**：在 **UDP/IP**（Layer 3）上跑 RDMA，可跨子网、路由，部署更灵活；延迟略高于 RoCE v1 与 IB，但仍优于 TCP。生产环境多选 **RoCE v2** 或 IB；RoCE v1 在纯 L2 无损网络中可用。

### 四、对比小结

| 类型     | 网络     | 部署     | 延迟/带宽     |
|----------|----------|----------|----------------|
| InfiniBand | 专用 IB  | 需 IB 硬件 | 最优           |
| RoCE v1  | L2 以太网 | 需无损网络 | 次之           |
| RoCE v2  | L3 UDP   | 易部署   | 略高仍优于 TCP |

---

## 面试要点

- RDMA = 网卡直读对端内存，零拷贝、低延迟；IB 与 RoCE 是两种实现。
- RoCE v1 = L2 无损以太网；RoCE v2 = L3 UDP，可路由、易部署。
- 性能：IB ≥ RoCE v1 > RoCE v2 > TCP；多机无 IB 常用 RoCE v2。

---

## 记忆要点

1. RDMA = 内核旁路、零拷贝；IB 专用，RoCE 跑在以太网上。
2. RoCE v1 = L2；RoCE v2 = L3 UDP，可跨子网。
3. 选型：有 IB 用 IB；否则 RoCE v2 常用。

[返回模块](./README.md) | [返回总览](../README.md)
