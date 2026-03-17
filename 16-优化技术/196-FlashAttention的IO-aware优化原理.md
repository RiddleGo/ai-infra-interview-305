# 第 196 题：`FlashAttention`的`IO-aware`优化原理？`tiling`、`recomputation`？

## 题目

`FlashAttention`的`IO-aware`优化原理？`tiling`、`recomputation`？

---

## 完整讲解

### 一、IO-aware 的问题背景

标准 attention 的 **QKV 与 softmax** 需要多次读写 **HBM**（显存），**带宽**成为瓶颈；算力往往吃不满。**IO-aware** 优化：从「减少对 HBM 的读写、提高算术强度」出发设计算法与实现，使 attention 更贴近**算力上限**而非带宽上限。

### 二、Tiling 与分块

**Tiling**：不一次性把整块 Q、K、V 从 HBM 读入，而是按**块**（tile）处理。每次只把 **Q 的一小块** 与 **K、V 的对应块** 读入 **SRAM/共享内存**，在片上算完该块的 attention 与输出，再写回 HBM。这样**重复利用**片上数据，减少 HBM 往返次数，即**降低 IO 量**、提高有效算术强度。

### 三、Recomputation

**Recomputation**：前向时**不存**完整的 attention 中间结果（如 softmax 前的 scores、softmax 结果）回 HBM，只存**为反向所需的最少信息**（如 softmax 归一化因子、或分块时的块级统计）。反向时按需**重新计算**部分前向（用存下的统计量快速重算），用**算换存**，降低显存占用与带宽，避免 OOM 并利于更大 batch 或更长序列。
---

## 面试要点

- FlashAttention 的 IO-aware：从减少 HBM 读写出发，提高算术强度、逼近算力上限。
- Tiling：按块在片上算 QK^T/softmax/OV，减少 HBM 往返；分块复用数据。
- Recomputation：前向少存中间结果，反向时重算；用算换存、降带宽与显存。

---

## 记忆要点

1. IO-aware = 减 HBM 访问、提算术强度。
2. Tiling = 分块、片上算、少往返。
3. Recomputation = 少存、反向重算；算换存。

[返回模块](./README.md) | [返回总览](../README.md)
