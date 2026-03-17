# 第 69 题：流水线并行中的`micro-batch`大小如何影响吞吐？

## 题目

流水线并行中的`micro-batch`大小如何影响吞吐？

---

## 完整讲解

### 一、Micro-batch 与吞吐的关系

**Micro-batch 大小** = global batch / (DP × chunks)。chunks 越大，单次 forward/backward 的粒度越小，**管道更易填满、bubble 占比下降**，理论上吞吐上升。但 chunks 越大，**同时存活的激活越多**，每 stage 显存增加；若用 activation checkpointing，重算次数也随 chunks 增加，算力开销上升。

### 二、吞吐随 M 的变化

- **M 过小**：bubble 比例高（约 \(\frac{2(S-1)}{M+2(S-1)}\)），GPU 空闲多，吞吐低。
- **M 适中**：bubble 与显存、重算达到平衡，吞吐最优。
- **M 过大**：显存吃满或 OOM，或重算过多导致单 step 变慢，吞吐可能反而下降。实践中对给定模型与卡数，需 sweep chunks（或等价地 micro-batch size）测 throughput。

### 三、与 batch size、DP 的联合影响

Global batch = DP × chunks × micro_batch_size。固定 global batch 时，增大 chunks 会减小 micro_batch_size，单次 F/B 更轻、管道更满，但单次通信/ kernel 效率可能略降；反之 chunks 小则 micro_batch 大，bubble 大。通常先定 global batch 与 DP，再在显存允许范围内尽量增大 chunks 以压 bubble，必要时用 checkpoint 换显存。

---

## 面试要点

- Micro-batch 数（chunks）大 → bubble 小、管道满，但显存与重算增加。
- 吞吐先随 chunks 升后可能因显存/重算降；需 sweep 找最优点。
- 与 DP、global batch 联合调：固定 global batch 下优先在显存允许时增大 chunks。

---

## 记忆要点

1. Chunks 大 = bubble 小、显存与重算大；存在最优 chunks。
2. 公式上 bubble ∝ 1/M，M 为 micro-batch 数。
3. 工程上先定 batch 与 DP，再尽量大 chunks + checkpoint 保显存。

[返回模块](./README.md) | [返回总览](../README.md)
