# 第 217 题：训练平台的`job scheduler`如何设计？`FIFO` vs `priority` vs `fair shari…

## 题目

训练平台的`job scheduler`如何设计？`FIFO` vs `priority` vs `fair sharing`？

---

## 完整讲解

### 一、FIFO

**FIFO**（先来先服务）：按**提交顺序**排队，先提交的先调度。**优点**：实现简单、公平、无饥饿。**缺点**：大 job 会堵住后面小 job（head-of-line blocking）；紧急任务无法插队；**不适合**多租户与混合负载。

### 二、Priority

**Priority**：每个 job 有**优先级**（数字或等级），**高优先调度**；可配合**抢占**（高优可抢占低优资源）。**优点**：紧急/生产任务可优先；适合**多租户**（付费高优、实验低优）。**缺点**：低优可能**饥饿**；需设 **priority 上限、quota、或 fairness** 约束。

### 三、Fair sharing

**Fair sharing**：按**用户或队列**的 **历史使用量** 或 **权重** 分配资源，使**长期占用**趋于公平（用得多的优先级随时间下降）。**优点**：多用户下**公平**、防止单用户占满。**缺点**：实现复杂（需 usage 统计与动态权重）；可能与 **deadline、SLA** 冲突。**实践**：三者常**组合**：队列内 **fair sharing**、队列间 **priority**；或 **FIFO + priority 覆盖**（高优可插队）；再配 **quota** 防单用户占满。
---

## 面试要点

- FIFO：先来先服务；简单公平但易 head-of-line blocking。
- Priority：高优先调、可抢占；需防低优饥饿、配 quota。
- Fair sharing：按使用/权重公平分；可组合：队列内 fair、队列间 priority。

---

## 记忆要点

1. FIFO = 顺序；Priority = 高优先、可抢占；Fair = 按使用公平。
2. 组合：fair 队列内 + priority 队列间；quota 限单用户。
3. 按业务选：简单用 FIFO；多租户用 priority + fair。

[返回模块](./README.md) | [返回总览](../README.md)
