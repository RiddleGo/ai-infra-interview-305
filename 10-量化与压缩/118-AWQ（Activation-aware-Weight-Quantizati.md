# 第 118 题：`AWQ`（Activation-aware Weight Quantization）的核心思想？

## 题目

`AWQ`（Activation-aware Weight Quantization）的核心思想？

---

## 完整讲解

### 一、核心思想

**AWQ**（Activation-aware Weight Quantization）认为：权重量化时不应一视同仁，而应**根据激活的尺度**对权重做保护。对激活幅值大的通道（或 group），对应权重更敏感，应少量化或用更高精度；对激活小的通道，权重可压得更狠。这样在相同比特预算下，重要通道保留更多信息，整体精度更好。

### 二、做法简述

通过激活统计（如 calibration 时各 channel 的 scale 或重要性）得到一个 per-channel 的**保护因子**，在量化前对权重做 scaling：重要 channel 的权重放大（相当于量化时用更细的步长），不重要的缩小。量化后还原，或把 scale 融进后续的 linear 计算。可选地配合「混合精度」：少量关键 channel 保持 FP16/W8，其余 INT4，在显存与精度间折中。

### 三、与 GPTQ/SmoothQuant 的区分

GPTQ 是逐层基于 Hessian 的权重量化；SmoothQuant 是激活-权重的等价缩放迁移。AWQ 是**按激活重要性对权重量化做非均匀保护**，不改变前向数学形式，而是选「量化谁、压多少」，工程上常与 per-group 量化、KV cache 量化等一起用在大模型部署。

---

## 面试要点

- AWQ = 按激活重要性保护权重量化：激活大的 channel 权重量化更保守，激活小的可压更狠。
- 实现：用校准得到 per-channel 重要性/scale，对权重做 scaling 再量化，或混合精度保留关键 channel。
- 与 GPTQ（Hessian 权重量化）、SmoothQuant（激活-权重 scale 迁移）区分开；常与 per-group、W4 等用于 LLM。

---

## 记忆要点

1. AWQ = activation-aware：看激活幅值决定权重量化力度，重要 channel 少压。
2. 做法：校准得 per-channel 重要性 → 权重量化前 scaling 或混合精度。
3. 与 GPTQ/SmoothQuant 互补；常用于 LLM 的 W4/W8 部署。

[返回模块](./README.md) | [返回总览](../README.md)
