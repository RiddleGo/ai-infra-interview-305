# 第 174 题：多租户集群的`resource quota`和`priority class`？

## 题目

多租户集群的`resource quota`和`priority class`？

---

## 完整讲解

### 一、Resource quota 的作用

**Resource quota**（K8s 的 ResourceQuota）：在 **namespace** 维度限制该命名空间内所有资源的**总和**（如总 CPU、内存、GPU 数量、PVC 容量等），防止某租户占满集群。多租户下为每个团队/项目分配独立 namespace 并设 quota，实现**硬上限**。

### 二、Priority class

**PriorityClass**：为 Pod 指定**调度优先级**（数字越大越优先）；高优 Pod 可**抢占**低优 Pod 的节点，被抢占的 Pod 可被 evict 后重调度。多租户场景：生产/紧急任务用高 priority，批处理/实验用低 priority；配合 **preemption policy**（Never 可禁止被抢占）。注意：高优任务过多仍会排队，quota 与 capacity 是硬约束。

### 三、与队列、公平共享的配合

Quota 管「最多能用多少」；**谁先谁后**由队列与 priority 决定。Volcano 的 **Queue** 可设置 cap、weight，与 namespace/quota 结合：例如每队列对应若干 namespace、每 namespace 设 quota；priority 用于同一队列内或跨队列的抢占与排序。这样实现「租户隔离 + 公平共享 + 紧急优先」。
---

## 面试要点

- ResourceQuota 在 namespace 级别限制 CPU/内存/GPU 等总和，多租户下每团队一 namespace + quota。
- PriorityClass 决定调度与抢占顺序；高优可抢占低优，配合 preemption policy 控制是否可被抢占。
- Quota 管上限，队列与 priority 管顺序；可与 Volcano Queue 结合做公平与紧急优先。

---

## 记忆要点

1. Quota = namespace 级资源上限；多租户按 namespace 隔离。
2. PriorityClass = 调度/抢占优先级；高优可抢占低优。
3. Quota + Queue + Priority 一起实现隔离与公平。

[返回模块](./README.md) | [返回总览](../README.md)
