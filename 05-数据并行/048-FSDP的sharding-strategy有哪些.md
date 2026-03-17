# 第 48 题：FSDP的`sharding strategy`有哪些？`FULL_SHARD` vs `SHARD_GRAD_OP`？

## 题目

FSDP的`sharding strategy`有哪些？`FULL_SHARD` vs `SHARD_GRAD_OP`？

---

## 完整讲解

### 一、FSDP 的 sharding 在 shard 什么？

FSDP 对**参数**（以及可选地**梯度、优化器状态**）做**分片**：每张卡只存 1/N，forward/backward 时按需 all-gather。**Sharding strategy** 决定「**在哪个阶段**对哪些东西做分片」。

---

### 二、常见策略（PyTorch FSDP 命名）

- **FULL_SHARD（全分片）**：**参数、梯度、优化器状态**都按卡分片。每卡显存最少；forward 时 all-gather 参数、算完就丢，backward 时 all-gather 再 reduce-scatter 梯度，优化器只更新本卡分片。通信量最大、显存最省，适合「模型很大、单卡放不下」。
- **SHARD_GRAD_OP**：**参数**可能每卡一份（或分片），**梯度**分片、**优化器状态**分片。即梯度与优化器做 ZeRO-2 式分片，参数可全复制或部分复制。显存比 FULL_SHARD 略高（若参数全复制），但通信比 FULL_SHARD 少（少参数 all-gather）。
- **NO_SHARD（或类似）**：参数、梯度都不分片，每卡一份，等价于 DDP；仅用 FSDP 的包装与调度，显存最大、通信最少。
- **HYBRID_SHARD**：节点内全分片、节点间复制等混合，用于多机时平衡机内通信与机间通信。

---

### 三、FULL_SHARD vs SHARD_GRAD_OP

- **FULL_SHARD**：参数+梯度+优化器全分片；显存最省，通信最多（每层 all-gather + reduce-scatter）。
- **SHARD_GRAD_OP**：梯度（及优化器）分片，参数可全复制；显存略高，通信较少（无参数 all-gather 或减少）。适合「参数能放下、但梯度+优化器想省」的中间规模。

选型：单卡放不下整模型 → FULL_SHARD；能放下参数、只想省梯度和优化器 → SHARD_GRAD_OP 或 ZeRO-2 风格。

---

## 面试要点

- FULL_SHARD = 参数+梯度+优化器全分片；显存最省，通信最多。
- SHARD_GRAD_OP = 梯度（及优化器）分片，参数可全复制；通信较少，显存略高。
- 选型按「单卡能否放下参数」与「要省到哪一层」决定。

---

## 记忆要点

1. FULL_SHARD：全分片，显存最小，通信最大；SHARD_GRAD_OP：梯度/优化器分片，参数可复制。
2. NO_SHARD ≈ DDP；HYBRID 用于多机。
3. 模型过大用 FULL_SHARD；能放参数用 SHARD_GRAD_OP 折中。

[返回模块](./README.md) | [返回总览](../README.md)
