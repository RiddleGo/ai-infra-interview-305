# 第 175 题：GPU集群的`topology awareness`调度？`NVLink`拓扑？

## 题目

GPU集群的`topology awareness`调度？`NVLink`拓扑？

---

## 完整讲解

### 一、Topology awareness 的意义

**拓扑感知调度**：在分配 GPU（或 NUMA、网卡）时，考虑**硬件拓扑**（如 NVLink 连接、PCIe 树、NUMA 节点），优先把同一作业的 GPU 安排在**通信延迟低、带宽高**的组内，从而提升 all-reduce 等通信效率、缩短训练时间。

### 二、NVLink 与拓扑

**NVLink**：GPU 间高速直连；同一节点内多卡可能通过 NVLink 全连接（如 8×A100 全连）或部分连接。调度时若「尽量把同一 job 的 8 卡放在同一节点、且选 NVLink 拓扑最优的节点」，可最大化带宽。**多节点**：节点间通过 IB/RoCE；同一 job 的节点宜在相近拓扑（同 rack、同 leaf）以减少跨级跳数。

### 三、实现方式

**设备插件 + 调度**：NVIDIA **DCGM** 或 **GPU Feature Discovery** 可暴露拓扑信息（如 `nvidia.com/nvlink`）；调度器在 **Score** 阶段对「请求多 GPU 的 Pod」优先选 NVLink 带宽高的节点。**K8s**：可扩展 scheduler plugin 或使用 Volcano 的 **binpack / topology 策略**；Slurm 的 **cons_res** 与 **topology/tree** 可做类似约束。**CRI/容器**：保证分配到的 GPU 与上报拓扑一致，避免跨 NUMA 或远距离 PCIe。
---

## 面试要点

- 拓扑感知：按 NVLink/PCIe/NUMA 等把同一 job 的 GPU 放在通信最优的位置，提升 all-reduce 等性能。
- NVLink 同节点内高带宽；多节点看 IB/RoCE 与网络拓扑（同 rack 等）。
- 通过设备插件暴露拓扑、调度器 Score 或 Volcano 策略做拓扑感知；Slurm 可用 cons_res/topology。

---

## 记忆要点

1. 拓扑感知 = 按 NVLink/NUMA 等优化放置，减少通信延迟与带宽瓶颈。
2. 同节点 NVLink、多节点 IB/RoCE + 同 rack 有利于通信。
3. 设备插件暴露拓扑；调度器 Score/Volcano/Slurm 做拓扑感知。

[返回模块](./README.md) | [返回总览](../README.md)
