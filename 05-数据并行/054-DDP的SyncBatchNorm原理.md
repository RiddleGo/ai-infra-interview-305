# 第 54 题：DDP的`SyncBatchNorm`原理？什么时候必须用？

## 题目

DDP的`SyncBatchNorm`原理？什么时候必须用？

---

## 完整讲解

### 一、普通 BatchNorm 在 DDP 下有什么问题？

**BatchNorm** 用**当前 batch** 的均值和方差做归一化。DDP 时每卡只有**本地 batch**（如 batch_size=32，每卡 32 个样本），BN 的 mean/var 只基于这 32 个样本；**卡间统计量不一致**，等价于「每卡在用自己的小 batch 做 BN」，和单卡大 batch（如 32×8=256）的 BN 统计量不同，可能影响精度和稳定性。

---

### 二、SyncBatchNorm 在做什么？

**SyncBatchNorm** 在算 mean/var 时**跨卡同步**：先在各卡上算本地 mean/var 和 count，再 **all-reduce**（或 all-gather 后合并）得到**全局 mean/var**，用全局统计量做归一化；反向时对「全局统计量」的梯度再做一次同步。这样 BN 的统计量与「单卡大 batch」一致，等价于用 **global batch** 做 BN。

---

### 三、什么时候必须用？

- **小 local batch**：每卡 batch 很小时（如 2、4），单卡 BN 统计量噪声大；用 SyncBatchNorm 用全局 batch 的统计量更稳定，**建议用**。
- **大 local batch**：每卡已经很大（如 64、128），本地 BN 统计量已较准，SyncBN 收益小但有多一次同步开销；可不用，除非你刻意要「和单卡大 batch BN 完全一致」。
- **多机 / 多卡数多**：SyncBN 要 all-reduce，卡多时通信明显；若 local batch 够大，可权衡是否用。
- **总结**：**每卡 batch 小、或要严格对齐单卡大 batch BN 时用 SyncBatchNorm**；local batch 大、且不强调一致时可不用。

---

### 四、实现要点

- 用 `torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)` 把模型里的 BN 换成 SyncBN；或自己建 SyncBN 层。
- SyncBN 内部在 forward 里做一次 all-reduce（mean/var），backward 里再做梯度同步；需保证进程组一致。

---

## 面试要点

- 普通 BN 用本地 batch 统计量；DDP 下每卡本地 batch 小，统计量不一致。
- SyncBN = 算 mean/var 时 all-reduce，用全局统计量做 BN，与单卡大 batch BN 一致。
- 必须/建议用：每卡 batch 小、或要严格一致时；local batch 大时可不用。

---

## 记忆要点

1. DDP 下 BN 用本地 batch → 卡间统计量不同；SyncBN 用全局 mean/var。
2. SyncBN = forward/backward 里 all-reduce 统计量（及梯度）。
3. 小 local batch 用 SyncBN；大 local batch 可不用。

[返回模块](./README.md) | [返回总览](../README.md)
