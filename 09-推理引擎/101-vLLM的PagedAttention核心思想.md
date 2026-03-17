# 第 101 题：vLLM的`PagedAttention`核心思想？`block table`的数据结构？

## 题目

vLLM的`PagedAttention`核心思想？`block table`的数据结构？

---

## 完整讲解

### 一、PagedAttention 核心思想

**PagedAttention** 借鉴 OS 的**分页内存**：把 KV cache 按「块」（block）管理，每块固定大小（如 16/64 token 的 KV），**物理上不连续**；逻辑上每个序列的 KV 用 **block 指针列表** 串联。这样可 **按需分配/回收块**、减少外部碎片、便于不同序列共享前缀块（prefix caching）。

### 二、Block 与 Block Table

- **Block**：固定 token 数的 KV 存储单元；所有 block 组成 **全局 block 池**，按需分配给请求。
- **Block table**：每个序列维护一张表，记录「该序列的 KV 由哪些 block 组成、顺序如何」；即 **逻辑 KV 序列 → 物理 block 列表** 的映射。解码时根据 block table 找到对应 block，再做 attention 计算；支持非连续、共享块（前缀共享时多序列指向同一组 block）。

### 三、收益

- **显存利用率高**：按块分配，减少碎片；可回收已结束序列的 block 给新请求。
- **前缀共享**：相同 prefix 的请求共享同一组 block，省显存与算力。
- **与 continuous batching 自然结合**：新请求随时要新 block、结束请求释放 block，block 池统一调度。

---

## 面试要点

- PagedAttention = KV 按块（page）管理，逻辑序列用 block 指针表串联；类似 OS 分页。
- Block table = 每序列的「逻辑 KV → 物理 block 列表」；支持非连续与共享。
- 收益：显存利用率高、碎片少、前缀共享、易与 continuous batching 结合。

---

## 记忆要点

1. KV 分块存储；每序列 block table 记录 block 列表。
2. 块可复用、可共享（前缀）；减少碎片。
3. 与 continuous batching 配合，按需分配/回收 block。

[返回模块](./README.md) | [返回总览](../README.md)
