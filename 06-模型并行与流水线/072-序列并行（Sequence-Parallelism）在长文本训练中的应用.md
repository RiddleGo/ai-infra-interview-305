# 第 72 题：序列并行（Sequence Parallelism）在长文本训练中的应用？

## 题目

序列并行（Sequence Parallelism）在长文本训练中的应用？

---

## 完整讲解

### 一、序列维度的显存与计算瓶颈

长序列时，**激活**在 sequence 维是 \(O(L^2)\)（attention）或 \(O(L)\)（其余），显存与计算都随序列长快速增长。若把 **sequence 维也做并行**，每卡只持有一段序列的激活，可降低单卡显存与单次 attention 的规模。

### 二、Sequence Parallelism（SP）做法

- **切分**：把 sequence 维切到多卡（常与 TP 同组），每卡持 \(L/N\) 长；attention 需 all-gather 或通信拼 full Q/K/V 再算，或做 distributed attention（每卡算局部再合并）。
- **典型用法**：Megatron 的 sequence parallel 常与 TP 结合，在 attention 的 QKV 与 O 处做 all-gather/reduce-scatter 时，把 sequence 维也一起切分，这样单卡激活从 \(O(L \cdot H)\) 降为 \(O((L/N) \cdot H)\)，适合长文本训练。
- **与 FlashAttention 等结合**：变长或长序列下，SP 降低单卡显存使更大 batch 或更长序列可行；需注意通信量与 overlap，避免 sequence 维 all-gather 成为新瓶颈。

### 三、应用场景

长文本预训练、长上下文微调、文档级任务等，当单卡放不下「全长序列的激活」时，用 SP 在序列维切分；通常与 TP 同机，通信 pattern 与 TP 的 all-gather/reduce-scatter 一致或融合。

---

## 面试要点

- SP 在序列维切分，单卡激活从 \(O(L)\)/\(O(L^2)\) 降为 \(O(L/N)\)，适合长序列。
- 常与 TP 结合，在 QKV/O 的 all-gather/reduce-scatter 中带 sequence 维。
- 长文本训练、长上下文微调是典型场景。

---

## 记忆要点

1. Sequence parallel = 序列维切分，降单卡激活与 attention 规模。
2. 与 TP 同组，通信 pattern 与 column/row 一致或融合。
3. 长序列、长上下文训练必备手段之一。

[返回模块](./README.md) | [返回总览](../README.md)
