# 第 50 题：DeepSpeed的ZeRO-1/2/3分别offload了什么？显存节省和通信开销的trade-off？

## 题目

DeepSpeed的ZeRO-1/2/3分别offload了什么？显存节省和通信开销的trade-off？

---

## 完整讲解

### 一、ZeRO 在解决什么？

数据并行时每卡存**完整参数、梯度、优化器状态**，显存是单卡的 3 倍量级（参数+梯度+优化器）。**ZeRO** 通过**分片**把这些状态分布到多卡，每卡只存 1/N，需要时再 all-gather 或 reduce，从而把**总显存**从 3× 降到约 3×/N（理想情况）。

---

### 二、ZeRO-1 / 2 / 3 各 offload（分片）了什么？

- **ZeRO-1**：只分片**优化器状态**（如 Adam 的 momentum、variance）；参数和梯度每卡仍完整。显存省「优化器」部分（约 2× 参数量），通信只在 optimizer step 时做一次 reduce-scatter/gather 类同步。
- **ZeRO-2**：分片**优化器状态 + 梯度**。backward 后梯度 reduce-scatter 到各卡分片；优化器只更新本卡分片。显存再省「梯度」；通信增加 backward 后的梯度 reduce-scatter（以及 step 时的 gather 若需）。
- **ZeRO-3**：分片**优化器状态 + 梯度 + 参数**。forward 时每层 all-gather 参数、算完丢；backward 时 all-gather 再 reduce-scatter 梯度。显存最省（约 3×/N），通信最多：每层都有 all-gather + reduce-scatter。

（「Offload」有时指 CPU/NVMe offload，如 ZeRO-Offload；这里 ZeRO-1/2/3 主要指**跨卡分片**，不涉及 CPU。）

---

### 三、显存与通信 trade-off

| 阶段   | 分片内容           | 显存（相对） | 通信（相对）     |
|--------|--------------------|--------------|------------------|
| ZeRO-1 | 优化器状态         | 省一部分     | 少（step 时）    |
| ZeRO-2 | 优化器 + 梯度      | 再省        | 多（梯度 reduce-scatter） |
| ZeRO-3 | 优化器 + 梯度 + 参数 | 最省        | 最多（每层 all-gather + reduce-scatter） |

选型：单卡能放下参数+梯度、只想省优化器 → ZeRO-1；能放参数、要省梯度 → ZeRO-2；单卡放不下参数 → ZeRO-3（或 + offload 到 CPU/NVMe）。

---

## 面试要点

- ZeRO-1：只分片优化器状态；ZeRO-2：+ 梯度；ZeRO-3：+ 参数。
- 显存：ZeRO-3 最省；通信：ZeRO-3 最多（每层 all-gather/reduce-scatter）。
- Trade-off：省显存就要多通信；按单卡能否放下参数/梯度选 stage。

---

## 记忆要点

1. ZeRO-1 = 优化器分片；ZeRO-2 = + 梯度分片；ZeRO-3 = + 参数分片。
2. 显存 ZeRO-3 < ZeRO-2 < ZeRO-1；通信 ZeRO-3 > ZeRO-2 > ZeRO-1。
3. 单卡放不下参数用 ZeRO-3；能放则 ZeRO-1/2 减通信。

[返回模块](./README.md) | [返回总览](../README.md)
