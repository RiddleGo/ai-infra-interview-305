# 第 62 题：Megatron-LM的`column parallel`和`row parallel`的矩阵划分策略？

## 题目

Megatron-LM的`column parallel`和`row parallel`的矩阵划分策略？

---

## 完整讲解

### 一、Column Parallel（列并行）

线性层 \(Y = XA\)，A 按**列**切分：每卡持 \(A_k\)，\(Y_k = X A_k\)，各卡独立算，**无需通信**得到分片 \(Y_k\)。前向：每卡输出 \(Y_k\)；若下游需要完整 \(Y\)，再 all-gather。典型用于 **Q、K、V 三个线性层**：输出维（head×head_dim）按列切，每卡算部分 head。

### 二、Row Parallel（行并行）

线性层 \(Y = XA\)，A 按**行**切分：每卡持 \(A_k\)（行块），\(Y = \sum_k X A_k\)。前向各卡算 \(X A_k\) 得到 partial sum，再 **all-reduce** 或 **reduce-scatter** 得到 \(Y\)。典型用于 **output 投影**（attention 后的 O、FFN 第二层）：输入维按行切，各卡产出 partial，归约后得完整输出。

### 三、为何这样划分？

- Column parallel：\(X\) 各卡相同（或已 broadcast），\(A\) 列切后每卡算 \(Y_k\)，无前向通信；反向时对 \(A_k\) 的梯度需 all-gather \(X\) 的梯度。
- Row parallel：\(X\) 已是分片（如 column 的输出），\(A\) 行切后 partial sum 再 reduce，通信一次；反向时梯度传播与分片一致。Megatron 里 QKV 用 column、O 用 row，使 attention 块内通信次数与量最小化。

---

## 面试要点

- Column parallel：矩阵按列切，\(Y_k = X A_k\)，前向无通信；用于 QKV 等「输出维」切分。
- Row parallel：矩阵按行切，partial sum 再 all-reduce；用于 O、FFN 第二层等「输入维」切分。
- 组合使用使 attention/FFN 块内通信可预测且最少（一次 all-gather 或 reduce）。

---

## 记忆要点

1. Column = 列切 A，每卡算一块 Y，用于 QKV。
2. Row = 行切 A，partial sum + reduce，用于 O。
3. 目的：前向/反向通信次数与量最小，与 fused attention 配合。

[返回模块](./README.md) | [返回总览](../README.md)
