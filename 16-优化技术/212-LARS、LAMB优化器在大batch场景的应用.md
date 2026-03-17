# 第 212 题：`LARS`、`LAMB`优化器在大batch场景的应用？

## 题目

`LARS`、`LAMB`优化器在大batch场景的应用？

---

## 完整讲解

### 一、大 batch 的难点

**大 batch** 时常用 **大学习率**（linear scaling），易导致**训练不稳**或**泛化变差**。**LARS**（Layer-wise Adaptive Rate Scaling）、**LAMB**（Layer-wise Adaptive Moments for Batching）通过 **逐层** 或 **逐参数** 的 **自适应缩放** 学习率，使大 batch 下各层更新幅度更合理，便于**稳定训练**与**扩展 batch**。

### 二、LARS 思路

**LARS**：对每层（或每参数组）计算 **梯度范数** 与 **权重范数** 的比，用该比 **缩放** 该层的有效学习率；梯度大的层相对「压一压」、梯度小的层相对「抬一抬」，避免某层更新过大或过小。公式上常为 **trust_coef × (weight_norm / grad_norm)** 再乘全局 lr；实现时在 optimizer 里 per-param 或 per-group 做 scaling。

### 三、LAMB 与使用场景

**LAMB**：在 **Adam** 类（一阶+二阶矩）基础上，对 **update 做 L2 norm 约束** 再与 weight norm 比，做 layer-wise 的 **adaptive learning rate**；兼顾 Adam 的适应性与大 batch 稳定性。**应用**：大 batch BERT 等预训练、超大 batch（如 64k）分布式训练；PyTorch 无内置时可从 **NVIDIA Apex** 或 **DeepSpeed** 等取 LAMB 实现，或自写 optimizer。
---

## 面试要点

- LARS/LAMB：逐层（或逐参数）自适应缩放学习率，大 batch 下更稳、易扩展。
- LARS：用梯度范数与权重范数比缩放每层 lr；LAMB：Adam + norm 约束的 layer-wise 缩放。
- 大 batch 预训练、超大 batch 分布式常用；实现见 Apex/DeepSpeed 或自写。

---

## 记忆要点

1. LARS/LAMB = 大 batch 下逐层自适应 lr。
2. LARS = grad_norm/weight_norm 比；LAMB = Adam + norm 约束。
3. 大 batch 预训练、超大 batch 常用。

[返回模块](./README.md) | [返回总览](../README.md)
