# 第 61 题：Tensor Parallelism（TP）的`fused attention`实现细节？

## 题目

Tensor Parallelism（TP）的`fused attention`实现细节？

---

## 完整讲解

### 一、TP 与 Attention 的切分关系

Tensor Parallelism 在 attention 层按 head 或 hidden 维度切分到多卡。**Fused attention** 把 Q/K/V 投影、softmax、output 投影合并成少量 kernel，减少显存读写与 launch 开销，在 TP 下每卡只算本分片的 Q、K、V，再做 all-gather/reduce-scatter 拼回或归约。

### 二、Fused attention 在 TP 下的实现要点

- **QKV 线性层**：按 column parallel 切分，每卡输出本卡对应的 head 子集；或按 hidden 维切分，前向各卡独立，backward 需 all-gather 梯度。
- **Attention 计算**：每卡持有部分 head 的 Q、K、V，先做局部 attention（或为减少通信做 split 后 all-gather K/V 再算）；**flash attention / xformers** 等 fused 实现需与 TP 的通信点对齐，避免重复 all-gather。
- **Output 投影**：row parallel，各卡算一部分 output 维度，再 all-gather 得到完整输出；或 reduce-scatter 从各卡 partial sum 归约。

### 三、与 Megatron 的对应

Megatron-LM 的 fused QKV 与 column/row parallel 即上述模式：column 切 QKV 输出、row 切 O 输入，中间 attention 用 ring 或 all-gather 拼 full K/V 再算。实现时 fused kernel 的输入输出 shape 需与 TP 分片一致，通信插入在「需要完整 tensor」的边界。

---

## 面试要点

- TP 下 attention 按 head 或 hidden 切分；fused attention 合并 QKV+attention+O，减少 kernel 与显存访问。
- Column parallel 用于 QKV 输出，row parallel 用于 O；中间需 all-gather 或通信拼 full K/V 再算 attention。
- 与 FlashAttention/xformers 结合时，通信点放在 fused 块边界，避免重复 all-gather。

---

## 记忆要点

1. TP fused attention = column 切 QKV + 中间通信拼 K/V + row 切 O。
2. Fused 减少 launch 与显存带宽；通信与 Megatron column/row 策略一致。
3. 实现时注意 fused kernel 的输入输出 shape 与分片一致。

[返回模块](./README.md) | [返回总览](../README.md)
