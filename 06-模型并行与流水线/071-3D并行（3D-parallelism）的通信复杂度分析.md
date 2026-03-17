# 第 71 题：3D并行（3D parallelism）的通信复杂度分析？

## 题目

3D并行（3D parallelism）的通信复杂度分析？

---

## 完整讲解

### 一、三维并行的通信来源

- **DP**：每 step 一次梯度 **all-reduce**，数据量 \(2 \cdot \frac{参数量}{DP}\)（fp32 梯度+优化器状态等），跨节点时受机间带宽限制。
- **TP**：每层前向/反向有 **all-gather 或 reduce-scatter**，数据量 \(O(\frac{层参数量}{TP})\)，通常同机 NVLink，带宽高、延迟低。
- **PP**：stage 间传**激活与梯度**，数据量 \(O(激活体积)\)，与 micro-batch size、序列长、hidden 相关；跨节点时单次量大但次数少。

### 二、通信量级（定性）

设参数量 \(P\)、层数 \(L\)、DP/TP/PP 度 \(D_p,T_p,S\)。DP all-reduce：\(O(P/D_p)\) 每 step。TP：每层 \(O(\frac{每层参数量}{T_p})\)，共 \(L\) 层，前向+反向约 \(O(2L \cdot \frac{每层参数量}{T_p})\)。PP：\(2(S-1)\) 次激活/梯度传递（每 micro-batch），每次 \(O(激活体积)\)。总通信字节与上述三者之和同阶；**时间**还取决于各通信所在链路（NVLink vs IB）与是否与计算重叠。

### 三、复杂度与优化方向

通信复杂度可写为 \(O(P/D_p) + O(L \cdot 层参数量/T_p) + O(S \cdot 激活)\)。优化：DP 用梯度压缩或增大 \(D_p\) 摊薄；TP 保持同机、用 fused 与 overlap；PP 减少 \(S\) 或激活体积（序列并行、checkpoint）。3D 同时开时以「DP 跨机、TP 同机、PP 适度」为原则，使总通信时间与计算时间匹配。

---

## 面试要点

- DP：每 step all-reduce \(O(P/D_p)\)；TP：每层 all-gather/reduce-scatter \(O(层参数量/T_p)\)；PP：stage 间激活/梯度 \(O(激活)\)。
- 总通信量 = DP + TP×层数 + PP×激活；时间还看链路与 overlap。
- 优化：DP 压缩/增大度，TP 同机，PP 减激活或 stage 数。

---

## 记忆要点

1. 3D 通信 = DP all-reduce + TP 每层通信 + PP 激活传递。
2. TP 同机降延迟，DP/PP 可跨机；量级按参数量与激活估算。
3. 重叠与链路选择决定实际耗时。

[返回模块](./README.md) | [返回总览](../README.md)
