# 第 222 题：训练数据的`global shuffle`实现？`shuffle buffer`大小？

## 题目

训练数据的`global shuffle`实现？`shuffle buffer`大小？

---

## 完整讲解

### 一、Global shuffle 的目的

**Global shuffle**：在 **多 epoch** 或 **多 worker** 下，让**整个数据集**在**全局**视角下**打乱**，避免每个 epoch 或每个 worker 看到**相同顺序**，从而**提高泛化、减少顺序偏差**。若只做本地 shuffle（每 worker 自己 shuffle 自己的 shard），全局上仍可能存在**跨 shard 的顺序相关性**；global shuffle 使不同 epoch 间、不同 rank 间的样本顺序更随机。

### 二、实现思路

**中心式**：由 **单节点或服务** 生成「全局随机排列」的 **index 或 sample_id 列表**，各 worker 按 rank 取自己那一段；每 epoch 重新生成一次排列。**分布式**：各 worker 约定 **seed + epoch**，用 **相同算法** 生成全局排列（如 shuffle 0..N-1 的索引），再按 **shard 划分** 各取一段；无需中心节点，但需**确定性**（同一 seed+epoch 得到同一排列）。**DataLoader**：PyTorch 的 **DistributedSampler** 在 **shuffle=True** 时会对全量 index 做 shuffle（基于 seed+epoch），再按 rank 切分，等价于 global shuffle。

### 三、Shuffle buffer 大小

**Shuffle buffer**：若数据流式读、无法一次性载入全量，可用 **buffer**：先填满 **buffer**，从 buffer 中**随机抽** 一个输出，再补一个新样本；**buffer 越大** 随机性越强、但**内存与延迟**越大。**经验**：与 **dataset 大小** 和 **内存** 权衡；常见 **几万到几十万** 样本；过小则 shuffle 效果弱，过大则内存与首包延迟高。**Global**：若用 buffer，可 **每 worker 独立 buffer** 或 **按 shard 做全局索引 shuffle** 再流式读。
---

## 面试要点

- Global shuffle：全数据集在全局打乱，多 epoch/多 worker 下顺序更随机；利于泛化。
- 实现：中心生成全局排列、或分布式 seed+epoch 确定性生成；DistributedSampler 即一种。
- Shuffle buffer：流式时用 buffer 随机抽；buffer 大小权衡随机性与内存。

---

## 记忆要点

1. Global shuffle = 全局打乱；中心或分布式确定性生成排列。
2. DistributedSampler shuffle=True 即 global shuffle。
3. Buffer 大小：大则随机性好、内存高；按数据集与内存权衡。

[返回模块](./README.md) | [返回总览](../README.md)
