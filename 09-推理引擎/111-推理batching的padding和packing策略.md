# 第 111 题：推理batching的`padding`和`packing`策略？`FlashAttention`的变长支持？

## 题目

推理batching的`padding`和`packing`策略？`FlashAttention`的变长支持？

---

## 完整讲解

### 一、Padding 策略

**Padding**：batch 内序列长短不一时，把短序列 **pad 到同一长度**（如 max_len），再一起做矩阵运算。**优点**：实现简单、与固定-shape kernel 兼容好。**缺点**：**算力浪费**（对 pad 位置做无效计算）；batch 内长度方差大时浪费大。可通过 **attention mask** 屏蔽 pad 位置，不参与 softmax 与输出。

### 二、Packing 策略

**Packing**（如 **FlashAttention 的 packing**）：把多个短序列 **拼成一条长序列**，用 **segment 或 position 偏移** 区分不同序列；attention 时只在同一 segment 内做，避免跨序列。**优点**：无 pad 浪费、有效 token 数高。**缺点**：实现复杂、需变长 kernel 或自定义 attention；部分引擎对 packing 支持有限。适合 **长短混合、追求吞吐** 的场景。

### 三、FlashAttention 的变长支持

**FlashAttention** 通过 **cu_seqlens**（每个序列的起始位置）或 **segment 划分** 支持 **变长**：一次 forward 中不同 segment 对应不同序列，attention 只在 segment 内计算。这样可 **不 padding** 或 **轻量 padding**，结合 packing 提高有效算力。vLLM、FasterTransformer 等在变长 batch 中会结合 mask 或 packing + FlashAttention 减少浪费。

---

## 面试要点

- Padding：pad 到同长、实现简单、有算力浪费；mask 屏蔽 pad。
- Packing：多序列拼成一条、按 segment 做 attention，无 pad 浪费、实现复杂。
- FlashAttention 用 cu_seqlens/segment 支持变长；与 packing 结合可提高有效算力。

---

## 记忆要点

1. Padding = 简单有浪费；Packing = 无浪费、实现难。
2. FlashAttention 变长 = segment/cu_seqlens，只段内 attention。
3. 长短混合、高吞吐场景倾向 packing + FlashAttention。

[返回模块](./README.md) | [返回总览](../README.md)
