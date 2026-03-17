# 第 88 题：`NVLink`、`InfiniBand`、`TCP`的带宽和延迟差异？

## 题目

`NVLink`、`InfiniBand`、`TCP`的带宽和延迟差异？

---

## 完整讲解

### 一、NVLink

**NVLink**：GPU 间直连、多通道（如 300–600 GB/s 双向），**延迟极低**（微秒级），用于单机多卡或 NVSwitch 机内多卡。带宽与延迟都优于 PCIe；NCCL 单机内会优先走 NVLink，适合 **TP、单机 all-reduce**。

### 二、InfiniBand（IB）

**InfiniBand**：专用 RDMA 网络，**高带宽**（如 100–400 Gb/s 单口）、**低延迟**（微秒级）、**内核旁路**（zero-copy）。多机训练常用 IB 做机间 all-reduce；需专用网卡与交换机，成本高，适合集群。

### 三、TCP（以太网）

**TCP**：走标准以太网与内核协议栈，**带宽** 通常 10–100 Gb/s、**延迟** 数十微秒到毫秒级，易部署、无专用硬件。多机无 IB 时用 TCP（NCCL 的 socket 或 gloo）；带宽与延迟都逊于 NVLink/IB，适合 **DP 的梯度 all-reduce** 或小规模多机。

### 四、对比小结

| 类型     | 带宽（量级）   | 延迟     | 典型场景     |
|----------|----------------|----------|--------------|
| NVLink   | 300+ GB/s      | 极低     | 单机多卡 TP  |
| InfiniBand | 100–400 Gb/s | 微秒级   | 多机集群     |
| TCP      | 10–100 Gb/s    | 数十 μs～ms | 无 IB 多机、小规模 |

---

## 面试要点

- NVLink：单机 GPU 直连，带宽与延迟最优；InfiniBand：多机 RDMA，高带宽低延迟；TCP：以太网，易部署、性能次之。
- 单机 TP 走 NVLink；多机优先 IB，无 IB 用 TCP。

---

## 记忆要点

1. NVLink > IB > TCP（带宽与延迟）；TCP 易部署。
2. 单机 = NVLink；多机 = IB 或 TCP。
3. 延迟：NVLink/IB 微秒级，TCP 更高。

[返回模块](./README.md) | [返回总览](../README.md)
