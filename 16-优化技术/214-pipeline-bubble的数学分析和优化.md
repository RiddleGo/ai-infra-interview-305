# 第 214 题：`pipeline bubble`的数学分析和优化？

## 题目

`pipeline bubble`的数学分析和优化？

---

## 完整讲解

### 一、Pipeline bubble 的含义

**流水线** 把模型按 **layer 或 stage** 分到多设备，**micro-batch** 依次流过各 stage。**Bubble**：在 **填满管道** 与 **排空管道** 的阶段，部分 stage **空闲**（在等前/后 micro-batch），这段时间没有有效计算，即 **pipeline bubble**，造成 **利用率损失**。

### 二、数学上对 bubble 的刻画

设 **S = stage 数**，**M = micro-batch 数**。**理想**：所有 stage 一直满负荷时，总 step 约为 **S + M - 1**（或按 backward 再乘约 2）。**Bubble 占比**：约 **(S-1)/M**（填满+排空阶段约 2(S-1) 个「半满」步，相对总步数）。**结论**：**M 越大**，bubble 占比越小；**S 越大**，bubble 绝对量越大。因此 **增加 micro-batch 数** 可降低 bubble 比例；**减少 stage 数**（在显存允许下）也可减 bubble。

### 三、优化方向

**多 micro-batch**：在显存与调度允许下增大 M，使 bubble/(S+M) 变小。**非对称或 1F1B**：**1F1B**（One Forward One Backward）等调度让各 stage 尽早做 backward，减少「只等 forward」的空闲。**Re-materialization**：少存激活、用重算换显存，从而支持更多 micro-batch。**Stage 划分**：尽量让各 stage **计算量均衡**，避免某 stage 特别长拖慢整管。
---

## 面试要点

- Pipeline bubble：填满/排空管道时部分 stage 空闲；bubble 占比约与 (S-1)/M 相关。
- M 大则 bubble 占比小；S 大则 bubble 绝对量多；1F1B 等调度可减空闲。
- 优化：多 micro-batch、1F1B、均衡 stage、recompute 换显存增 M。

---

## 记忆要点

1. Bubble = 管道未满时 stage 空闲；占比约 (S-1)/M。
2. M↑ 占比↓；S↑ 绝对量↑；1F1B 减空闲。
3. 多 M、均衡 stage、recompute。

[返回模块](./README.md) | [返回总览](../README.md)
