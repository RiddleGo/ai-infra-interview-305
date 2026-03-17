# 第 65 题：激活重计算（activation checkpointing）在PP中的特殊处理？

## 题目

激活重计算（activation checkpointing）在PP中的特殊处理？

---

## 完整讲解

### 一、PP 中为何需要激活重计算

流水线并行下，多个 micro-batch 的激活会同时存在于不同 stage，**显存峰值**随 micro-batch 数和层数增长。**Activation checkpointing**（激活重计算）只存部分层的激活（如每层或每隔几层存一次），其余在 backward 时用存下来的激活重新 forward 算一遍，用**算力换显存**，在 PP 里可显著降低每 stage 的显存，从而允许更大 micro-batch 或更深 stage。

### 二、PP 中的特殊考虑

- **Stage 边界**：边界处激活必须保留或能重算，否则跨 stage 的 backward 无法进行；通常 stage 内用 checkpoint，边界输出要保留。
- **与 1F1B 的配合**：1F1B 下同一 stage 会交替做 F 和 B，checkpoint 策略要保证做 B 时所需激活要么已存、要么能由 checkpoint 重算，且重算顺序与依赖一致（例如从最近一个 checkpoint 重算到当前层）。
- **选择性 checkpoint**：不是每层都 checkpoint；通常「大激活、小计算」的层更适合重算（如 attention 前），可针对 PP 的 stage 划分单独调哪些层 checkpoint。

### 三、实现要点

Megatron 等框架在 PP 中通常对每个 stage 的若干层做 checkpoint，保留 stage 输出；backward 时在 stage 内从 checkpoint 重算到需要梯度的层。与纯数据并行相比，PP 的 checkpoint 还要考虑「同一设备上多 micro-batch 的激活生命周期」，避免重算与释放顺序错误。

---

## 面试要点

- PP 显存压力大，activation checkpointing 用算力换显存，允许更大 M 或更深 stage。
- Stage 边界激活需保留或可重算；1F1B 下重算顺序与依赖要与 F/B 交替一致。
- 选择性 checkpoint 大激活层；实现时注意多 micro-batch 的激活生命周期。

---

## 记忆要点

1. PP 中 checkpoint 降显存、换算力；stage 边界不能丢激活。
2. 1F1B 下 backward 依赖的激活要么存要么重算，顺序要正确。
3. 大激活层优先 checkpoint，与 stage 划分一起调。

[返回模块](./README.md) | [返回总览](../README.md)
