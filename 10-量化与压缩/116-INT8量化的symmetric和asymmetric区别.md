# 第 116 题：`INT8`量化的`symmetric`和`asymmetric`区别？`per-tensor` vs `per-cha…

## 题目

`INT8`量化的`symmetric`和`asymmetric`区别？`per-tensor` vs `per-channel`？

---

## 完整讲解

### 一、Symmetric vs Asymmetric

**Symmetric**：零点固定在 0，量化公式为 `scale * (x/scale).round()`，正负范围对称（如 INT8 为 -128～127）。实现简单、推理时无需存 zero_point，适合权重和激活分布较对称的情形（如 ReLU 后）。

**Asymmetric**：引入 zero_point，公式为 `round(x/scale) + zero_point`，可把真实范围映射到 [0,255]，更好地拟合非对称分布（如激活多非负），精度通常更好，但推理需多一次减 zero_point 的运算与存储。

### 二、Per-tensor vs Per-channel

**Per-tensor**：整个 tensor 共用一个 scale（和可选 zero_point），计算与存储开销最小，但若通道间分布差异大（如 Conv 各 output channel），易产生较大误差。

**Per-channel**（或 per-axis）：对某一维（如 Conv 的 output channel）各用一套 scale/zero_point，表达能力更强、精度更高，尤其对权重；代价是多组量化参数与逐 channel 的缩放逻辑，推理实现稍复杂。

### 三、工程取舍

权重常用 per-channel symmetric（兼顾精度与实现）；激活可选 per-tensor 或 per-channel、asymmetric 更稳。PTQ 时根据校准数据选 scheme；QAT 可端到端学 scale/zero_point。

---

## 面试要点

- Symmetric：零点为 0，实现简单、无 zero_point 存储，适合对称分布；Asymmetric：有 zero_point，非对称分布精度更好，推理多一次减法。
- Per-tensor：全 tensor 一套 scale，省算力与存储；per-channel：按轴（如 channel）多套参数，精度高、实现稍复杂。
- 权重常用 per-channel symmetric；激活可选 per-tensor/per-channel + asymmetric；PTQ 按校准选，QAT 可学参数。

---

## 记忆要点

1. Symmetric = 零点 0，无 zero_point；Asymmetric = 有 zero_point，非对称分布更准。
2. Per-tensor = 一套 scale；per-channel = 按轴多套 scale，精度高、开销略大。
3. 工程上：权重 per-channel symmetric，激活可 asymmetric；PTQ/QAT 决定具体 scheme。

[返回模块](./README.md) | [返回总览](../README.md)
