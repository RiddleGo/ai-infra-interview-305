# 第 64 题：`interleaved pipeline`（如Megatron的1F1B）如何减少bubble？

## 题目

`interleaved pipeline`（如Megatron的1F1B）如何减少bubble？

---

## 完整讲解

### 一、Interleaved 的含义

**Interleaved pipeline** 把同一 stage 的多个子块（如同一 GPU 上的若干层）拆成多段，不同 micro-batch 在这些段之间「交错」执行，而不是一个 stage 连续跑完所有层再交给下一 stage。这样同一物理 stage 会轮流处理多个 micro-batch，管道更满，**bubble 更少**。

### 二、1F1B（One Forward One Backward）

Megatron 的 **1F1B**：每个 stage 按序执行「一个 micro-batch 的 forward → 一个 micro-batch 的 backward」，而不是「所有 micro-batch forward → 再全部 backward」。这样管道中同时存在不同 micro-batch 的 F 和 B，空闲 slot 减少。与 GPipe 的 G-MB 相比，在相同 \(M、S\) 下 bubble 比例更低。

### 三、Interleaved 1F1B 的进一步优化

**Interleaved 1F1B**：在 1F1B 基础上，把每个 stage 的层再分成若干「子 stage」，调度时让不同 micro-batch 交错经过这些子 stage。效果是同一设备上多个子块轮流工作，bubble 可进一步下降（理想情况可逼近 \(O(1/S)\) 量级）。代价是调度与依赖更复杂，需保证同一 micro-batch 的 F/B 顺序正确。

---

## 面试要点

- Interleaved：同一 stage 内多子块，micro-batch 交错经过，管道更满、bubble 更小。
- 1F1B：每 stage 做「一 F 一 B」交替，相比全 F 再全 B 减少空闲。
- Interleaved 1F1B 结合两者，bubble 可进一步降低，实现与调度更复杂。

---

## 记忆要点

1. 1F1B = 每 stage 一 forward 一 backward 交替，减 bubble。
2. Interleaved = stage 内多子块、micro-batch 交错，提高利用率。
3. Megatron 的 interleaved 1F1B 是常用生产配置。

[返回模块](./README.md) | [返回总览](../README.md)
