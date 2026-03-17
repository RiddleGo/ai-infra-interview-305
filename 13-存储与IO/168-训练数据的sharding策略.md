# 第 168 题：训练数据的`sharding`策略？按文件vs按样本？

## 题目

训练数据的`sharding`策略？按文件vs按样本？

---

## 完整讲解

### 一、Sharding 的目的

分布式训练时每个 rank 只应消费**数据的一个子集**，避免重复与遗漏；**Sharding** 即把数据集划分成多份，每 rank 一份（或按 rank 取子集）。划分策略影响**负载均衡**、**IO 分布**与**可恢复性**。

### 二、按文件 vs 按样本

**按文件 sharding**：每个 rank 分配**不同文件集合**（如 rank 0 读 file_0, file_4, ...，rank 1 读 file_1, file_5, ...）。优点：实现简单、每个 rank 读不同文件、IO 易并行；缺点：若**文件大小或样本数差异大**，各 rank 负载不均，有的先跑完要等别的 rank。**按样本 sharding**：把全体样本视为序列，按 rank 数切分（rank i 取 sample_id % world_size == i）。优点：**负载更均衡**（每 rank 样本数相同）；缺点：若数据按文件存储，可能多个 rank 读同一文件的不同偏移，需要支持按 offset 读或先做「按样本索引」的元数据（如样本→文件+offset），实现稍复杂。大模型训练常用**按样本**或「按文件但做大小感知的分配」以均衡；小文件多时也可按文件并做动态负载均衡。

### 三、实现要点

PyTorch 的 `DistributedSampler` 默认按样本（每个 rank 取 dataset 的 1/N）；若数据按大文件存，可建索引（样本→文件+offset）再按样本 shard。恢复训练时 sampler 的 epoch/seed 要与 checkpoint 一致，保证恢复后各 rank 读到的顺序与未中断时一致。

---

## 面试要点

- Sharding = 每 rank 消费数据子集；按文件简单但易负载不均；按样本均衡但需索引或按 offset 读。
- 按文件：rank 读不同文件集；按样本：rank 取 sample_id % world_size，负载匀。
- 大模型常用按样本或大小感知的文件分配；恢复时 sampler 状态一致。

---

## 记忆要点

1. 按文件 = 简单、IO 并行，易负载不均；按样本 = 均衡，需索引或 offset。
2. DistributedSampler 默认按样本；大文件可建样本→(文件,offset) 索引。
3. 恢复时 sampler/epoch 与 checkpoint 一致。

[返回模块](./README.md) | [返回总览](../README.md)
