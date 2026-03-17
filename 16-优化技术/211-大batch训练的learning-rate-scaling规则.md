# 第 211 题：大batch训练的`learning rate scaling`规则？

## 题目

大batch训练的`learning rate scaling`规则？

---

## 完整讲解

### 一、大 batch 与学习率

**大 batch**：单步更新用更多样本，**梯度估计更准**，但**单步更新次数**减少。若保持与小 batch **相同总样本数**，大 batch 的 **总 step 数** 会少；若 **学习率不变**，可能欠拟合或收敛慢。经验上大 batch 需要 **更大学习率** 以补偿「每步更新更准、步数更少」。

### 二、Linear scaling 规则

**Linear scaling**：batch 扩大 **k 倍**，学习率也扩大 **k 倍**（如 batch 从 256 到 1024，lr 从 0.1 到 0.4）。**依据**：梯度是 mini-batch 平均，方差约与 batch 成反比；步长（lr×grad）若与 batch 同比例放大，每步「有效进展」大致相当。**适用**：在 **一定范围内**（如 8～64 倍）有效；**过大 batch**（如 8k+）时线性可能过激，需 **warmup** 或 **sqrt scaling**（lr ∝ √batch）更稳。

### 三、Warmup 与 fine-tuning

**Warmup**：大 batch 训练前期用 **小学习率** 若干 step 再升到目标 lr，避免初期大更新导致不稳定。**LARS/LAMB** 等优化器针对大 batch 做了 **per-layer 或自适应 scaling**，可减少纯线性规则的副作用。**实践**：先在小 batch 上找合适 lr，再按 linear（或 sqrt）乘上 batch 比，加 warmup；大 batch 时可用 LARS/LAMB 或调低 scaling 系数。
---

## 面试要点

- 大 batch 步数少、梯度更准；通常需更大 lr 补偿；linear scaling：lr ∝ batch。
- 过大 batch 可用 sqrt scaling 或 warmup；LARS/LAMB 做 per-layer/自适应。
- 先小 batch 定 lr，再按比例放大 + warmup；大 batch 可试 LARS/LAMB。

---

## 记忆要点

1. 大 batch → 更大 lr；linear：lr 随 batch 线性增。
2. 过大 batch：warmup、sqrt scaling；LARS/LAMB 可辅助。
3. 小 batch 定 lr → 按比例 + warmup。

[返回模块](./README.md) | [返回总览](../README.md)
