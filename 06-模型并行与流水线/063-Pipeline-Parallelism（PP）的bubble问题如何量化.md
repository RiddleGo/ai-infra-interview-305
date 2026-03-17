# 第 63 题：Pipeline Parallelism（PP）的`bubble`问题如何量化？`GPipe` vs `PipeDrea…

## 题目

Pipeline Parallelism（PP）的`bubble`问题如何量化？`GPipe` vs `PipeDream`？

---

## 完整讲解

### 一、Bubble 的量化

流水线中 **bubble** 指部分 stage 在等待数据时的空闲。设 stage 数 \(S\)、micro-batch 数 \(M\)：GPipe 等 **G-MB 策略**（先全 forward 再全 backward）下，前向填满管道要 \(S\) 步，后向再 \(S\) 步，首尾各有约 \(S-1\) 个「空 slot」，理想稳定阶段有 \(M-S\) 个有效 slot。Bubble 比例可近似为 \(\frac{2(S-1)}{M + 2(S-1)}\)，\(M\) 越大 bubble 占比越低，但显存随 \(M\) 增大。

### 二、GPipe 的特点

**GPipe**：同一 batch 切成 \(M\) 个 micro-batch，按序全部 forward 完再全部 backward。实现简单，但 **显存峰值高**（要存 \(M\) 份激活），且 bubble 明显；通过增大 \(M\) 摊薄 bubble，代价是激活重计算或显存压力。

### 三、PipeDream 的改进

**PipeDream**：**1F1B**（One Forward One Backward）或 **stale gradient** 等策略，同一 micro-batch 的 backward 不必等全 batch forward 结束，管道中同时有不同 batch 的 F/B，显存与 bubble 折中。PipeDream 还引入 **weight stashing**（存多版本权重以应对流水线中并行的不同 batch），复杂度更高；Megatron 的 1F1B 不存多版本，用 **recompute** 换显存，bubble 仍可量化为与 \(S、M\) 相关的公式，通常优于 GPipe。

---

## 面试要点

- Bubble 比例约 \(\frac{2(S-1)}{M+2(S-1)}\)；\(M\) 大则 bubble 小，显存大。
- GPipe：全 F 再全 B，实现简单，显存高、bubble 大。
- PipeDream/1F1B：F 与 B 交错，bubble 更小；PipeDream 有 weight stashing，Megatron 1F1B 常用 recompute。

---

## 记忆要点

1. Bubble ≈ \(2(S-1)\) 空 slot / 总 slot；增大 micro-batch 数可降低比例。
2. GPipe = 先全 forward 再全 backward；PipeDream/1F1B = 交错 F/B 减 bubble。
3. 工程上多用 1F1B + recompute，避免多版本权重。

[返回模块](./README.md) | [返回总览](../README.md)
