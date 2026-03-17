# 第 210 题：`gradient accumulation`的`effective batch size`计算？

## 题目

`gradient accumulation`的`effective batch size`计算？

---

## 完整讲解

### 一、Gradient accumulation 的含义

**Gradient accumulation**：把 **N 个 mini-batch** 的梯度**累加**后再做一次 **optimizer.step()**，等价于用 **N×mini-batch_size** 的「大 batch」做一次更新，但**显存**只需容纳 **一个 mini-batch** 的前向与反向。用于 **显存不够** 直接跑大 batch、但又希望 **effective batch size** 较大时。

### 二、Effective batch size 计算

**Effective batch size = mini_batch_size × accumulation_steps**。例如 mini_batch_size=8、accumulation_steps=4，则每 4 个 step 做一次更新，**effective batch size = 8×4 = 32**。**等价**：与「一次前向 32 个样本再 backward」在**梯度与更新**上等价（若无 BN 等依赖 batch 统计的层，或 BN 用 running stat）；**时间**上约为 4 倍小 step 的前向+反向 + 1 次优化器，显存约 1 倍小 batch。

### 三、与学习率等配合

大 effective batch 通常要配合 **learning rate scaling**（线性或 sqrt 放大）；以及 **warmup**、**总 step 数** 按 effective batch 折算（如总样本数 / effective_batch_size 为 epoch 内更新次数）。**BN**：若用 BN，当前实现下每 mini-batch 的 mean/var 仍按小 batch 算，与「真大 batch」略有差异；可改用 **SyncBN** 或 **LayerNorm** 减轻对 batch 的依赖。
---

## 面试要点

- Gradient accumulation：多 mini-batch 梯度累加再一步更新；显存按 mini-batch，等效大 batch 更新。
- Effective batch size = mini_batch_size × accumulation_steps。
- 配合 lr scaling、warmup、总 step 折算；BN 时注意 batch 统计与小 batch 差异。

---

## 记忆要点

1. 累加 N 次梯度再 step；effective = mini_batch × N。
2. 显存省、等效大 batch；与 lr scaling 配合。
3. BN 时每 mini-batch 统计；可 SyncBN 或 LayerNorm。

[返回模块](./README.md) | [返回总览](../README.md)
