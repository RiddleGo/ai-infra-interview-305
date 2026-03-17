# 第 68 题：模型并行中的`all-gather`和`reduce-scatter`通信模式？

## 题目

模型并行中的`all-gather`和`reduce-scatter`通信模式？

---

## 完整讲解

### 一、All-Gather

**All-gather**：每卡持有 tensor 的一个分片，通信后每卡得到**完整** tensor。例如 column parallel 的 QKV 输出分片在每卡，下游需要完整 K、V 时做 all-gather 拼成 full K、V 再算 attention。通信量：\(P\) 卡、每卡 \(n\) 元素，总数据 \(nP\)，每卡收 \((P-1)n\)，发 \(n\)；ring 或 tree 算法约 \(2(P-1)n/P\) 单卡流量。

### 二、Reduce-Scatter

**Reduce-scatter**：每卡持有一个完整 tensor 的 copy，通信后每卡得到**归约结果的一个分片**（如 sum 后按卡切分）。例如 row parallel 的 output：各卡有 partial sum，reduce-scatter 得到「全局 sum 的一个分片」，可直接作为下一层 column 的输入。通信量量级与 all-gather 同量级，但语义是「先 reduce 再 scatter」。

### 三、在 TP 中的典型用法

- **Column → 下游需要 full**：all-gather 拼成完整 tensor（如 K、V 给 attention）。
- **Row 的 partial sum → 下一层 column 的输入**：reduce-scatter 得到分片，避免再 all-gather 一整份；即 **all-gather 与 reduce-scatter 配对** 可把一次「all-reduce」拆成两次通信，有时能更好重叠或适配内存布局。Megatron 里 linear 的 column/row 与 attention 的通信就是这类模式。

---

## 面试要点

- All-gather：分片 → 每卡得完整 tensor；用于拼 K/V 等。
- Reduce-scatter：每卡有 copy → 每卡得归约结果的一个分片；用于 row 后给下一 column。
- 与 all-reduce 的关系：all-reduce ≈ reduce-scatter + all-gather；拆开可优化重叠与显存。

---

## 记忆要点

1. All-gather = 分片拼成完整；reduce-scatter = 归约后得分片。
2. TP 中 column 后常 all-gather，row 后常 reduce-scatter 给下一层。
3. 通信量级与 all-reduce 同阶，拆成两步可优化重叠。

[返回模块](./README.md) | [返回总览](../README.md)
