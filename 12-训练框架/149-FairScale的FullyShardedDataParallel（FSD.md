# 第 149 题：FairScale的`FullyShardedDataParallel`（FSDP）实现细节？

## 题目

FairScale的`FullyShardedDataParallel`（FSDP）实现细节？

---

## 完整讲解

### 一、FSDP 做什么

**FullyShardedDataParallel（FSDP）**：把模型参数、梯度、优化器状态**按 rank 分片**，每 rank 只存 1/world_size，前向与反向时按需 **all-gather** 参数，计算完再释放或转为分片，从而把显存从「每卡一份完整副本」降为「每卡 1/N」，可训更大模型或更大 batch。

### 二、FairScale 实现要点

**FairScale** 的 FSDP（后并入 PyTorch 的 `torch.distributed.fsdp`）核心实现：（1）**分片策略**：按 parameter 或 submodule 为单位分片，每 rank 只保留一部分；（2）**前向**：进入某层前 all-gather 该层参数，算完该层后可立刻释放（或保留到反向）；（3）**反向**：同样 all-gather 该层参数算梯度，梯度按分片 reduce-scatter 回各 rank；（4）**优化器**：每 rank 只更新本 rank 持有的分片，优化器状态也分片。**包装方式**：用 `FullyShardedDataParallel` 包装子模块或整模型，内部 hook 在 forward 前后做 all-gather/释放；可与 `auto_wrap_policy` 配合，按 transformer block 等自动包装以平衡通信与显存。

### 三、与 DDP、ZeRO 的关系

DDP 每卡完整参数；FSDP 参数分片、按需 all-gather，显存更省、通信量在 all-gather。ZeRO-3 与 FSDP 思路一致，DeepSpeed 实现；PyTorch 官方 FSDP 吸收 FairScale 设计并持续优化。

---

## 面试要点

- FSDP = 参数/梯度/优化器状态分片，前向反向按需 all-gather，算完释放；显存约 1/N。
- FairScale 实现：按 parameter/submodule 分片、forward/backward 时 all-gather、梯度 reduce-scatter、优化器只更新本分片；auto_wrap_policy 按 block 包装。
- 与 DDP（每卡完整）、ZeRO-3（同思路）对比；PyTorch 已收 FSDP。

---

## 记忆要点

1. FSDP = 分片 + 按需 all-gather + 梯度 reduce-scatter；显存 1/N。
2. 实现 = 分片单位、forward/backward 时 gather、释放；auto_wrap 按 block。
3. FairScale 并入 PyTorch FSDP；与 ZeRO-3 思路一致。

[返回模块](./README.md) | [返回总览](../README.md)
