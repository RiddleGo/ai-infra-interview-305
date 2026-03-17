# 第 179 题：训练任务的`cost accounting`？按GPU小时计费？

## 题目

训练任务的`cost accounting`？按GPU小时计费？

---

## 完整讲解

### 一、Cost accounting 的目的

**成本核算**：按**谁用了多少资源**计费或摊成本，用于内部 chargeback、预算控制与优化决策。训练任务通常按 **GPU 小时**（或卡时）、**CPU 小时**、**存储与网络**等计量；需区分「按量计费」与「包时/预留」的折算方式。

### 二、按 GPU 小时计费

**GPU 小时**：每块 GPU 使用 1 小时计 1 单位（可再按机型加权，如 A100×1.5、H100×2）。调度器或作业系统在**任务结束**时统计：分配到的 GPU 数 × 实际运行时长（或 wall time）；若有抢占，可按「实际占用时长」计。数据来源：Slurm 的 **sacct**、K8s 的 **usage 统计**（需 metrics-server 或自定义 exporter）；与计费系统对接生成账单或报表。

### 三、扩展与公平

**多维度**：除 GPU 小时外可加 **存储 I/O、跨节点流量、队列溢价** 等。**公平共享**：与 **quota、priority、fair sharing** 结合，避免单用户占满；成本数据也可驱动「预算用尽则降优先级或暂停提交」。**Spot/抢占实例**：若使用抢占式资源，计费单价可打折，但需与 checkpoint 与重跑成本权衡。
---

## 面试要点

- Cost accounting 用于按用户/项目/队列统计资源消耗并计费或摊成本。
- GPU 小时 = 卡数 × 运行时长；数据来自 sacct、K8s usage 或自定义 exporter。
- 可与 quota、priority、fair sharing 结合；Spot 资源可打折计费。

---

## 记忆要点

1. Cost accounting = 按资源使用量计费/摊成本。
2. GPU 小时 = 卡数 × 时长；sacct / usage 提供数据。
3. 多维度计费 + 与配额/优先级结合。

[返回模块](./README.md) | [返回总览](../README.md)
