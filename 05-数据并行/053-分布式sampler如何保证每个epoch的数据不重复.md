# 第 53 题：分布式sampler如何保证每个epoch的数据不重复？

## 题目

分布式sampler如何保证每个epoch的数据不重复？

---

## 完整讲解

### 一、目标

多卡数据并行时，每张卡用**不同的数据子集**，且**整个 epoch 内**所有卡合起来正好把数据集**覆盖一遍、不重不漏**。DistributedSampler 就是按 rank、world_size 把样本**划分**到各卡，并可选**打乱**（shuffle）后每卡只取自己的那一段。

---

### 二、常见做法（PyTorch DistributedSampler）

- **划分**：总样本数 N，world_size W。每卡样本数 `n_per_rank = ceil(N/W)`，总长度可能补到 `n_per_rank * W`（不足用重复或 drop）。卡 rank 拿的**下标**为 `rank, rank+W, rank+2W, ...`，即**按 rank 交错**，这样每卡拿到不重叠的一批下标。
- **Shuffle**：若 `shuffle=True`，**每个 epoch 开始时**对「全局下标 0..N-1」做一次 shuffle（用相同的 seed，如 `epoch`），再按上面规则按 rank 取；这样每 epoch 每卡看到的顺序不同，但**卡间仍不重叠**。关键：**所有进程用同一 seed**（例如 `sampler.set_epoch(epoch)` 里用 epoch 作 seed），这样每卡上的 shuffle 结果一致，再按 rank 切分后仍不重不漏。
- **set_epoch(epoch)**：每个 epoch 调用一次 `sampler.set_epoch(epoch)`，让 shuffle 的 seed 随 epoch 变，否则每个 epoch 每卡拿到的是同一顺序，可能影响收敛。

---

### 三、不重复的保证

- 下标划分是**确定性的**（rank 0 拿 0,W,2W,...；rank 1 拿 1,W+1,...），且彼此无交。
- Shuffle 后仍是「全局一个排列」，再按 rank 切，所以**整个 epoch 内全局不重不漏**；每卡内也无重复（除非 N 不能被 W 整除且实现用重复补齐，此时可能有个别样本重复，可选用 drop_last 去掉尾批）。

---

## 面试要点

- 按 rank 交错取下标（rank, rank+W, ...），保证卡间不重叠。
- Shuffle 用同一 seed（如 set_epoch(epoch)），再按 rank 切，保证全局不重不漏且每 epoch 顺序变。
- 每 epoch 调用 set_epoch(epoch)，否则每 epoch 顺序相同。

---

## 记忆要点

1. 划分：下标按 rank 交错，每卡一段，不重叠。
2. Shuffle：全局同一 seed（set_epoch），再切分；每 epoch 换 seed。
3. 不重不漏 = 划分不交 + shuffle 一致；set_epoch 必须调。

[返回模块](./README.md) | [返回总览](../README.md)
