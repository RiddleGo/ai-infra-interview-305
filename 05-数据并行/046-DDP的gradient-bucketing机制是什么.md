# 第 46 题：DDP的`gradient bucketing`机制是什么？bucket size如何调优？

## 题目

DDP的`gradient bucketing`机制是什么？bucket size如何调优？

---

## 完整讲解

### 一、Gradient bucketing 在做什么？

DDP 在 backward 结束后要对**所有参数的梯度**做 all-reduce（或 reduce-scatter 等）以同步。若**每个参数张量单独一次通信**，小张量会产生大量小消息，通信效率差（延迟主导）。**Gradient bucketing** 的做法是：按**参数在模型中的顺序**（或按 size）把多个小梯度**打包进一个 bucket**，凑满一定大小（如 25MB）或到 bucket 数量上限后，**整桶做一次 all-reduce**，从而减少通信次数、提高带宽利用率。

---

### 二、机制要点

- **桶的划分**：参数按 `model.parameters()` 顺序（或 DDP 内部等价顺序）排列，依次填入 bucket，直到当前 bucket 的「待通信梯度总字节数」≥ `bucket_cap_mb`（默认约 25MB）或达到其他上限，就开新桶。
- **通信时机**：当某 bucket 内**所有参数**的梯度都已算完（即 backward 传到了该桶的最后一层），就立刻对该桶做 all-reduce；不必等全部 backward 结束，从而**通信与计算可重叠**。
- **重叠**：靠「桶内参数顺序与 backward 顺序一致」保证：先算完的桶先通信，后面的 backward 和前面的 all-reduce 可并行。

---

### 三、bucket size（bucket_cap_mb）如何调优？

- **过大**：桶少、单次通信量大，要等桶内所有梯度都算完才能发，**重叠机会少**，可能 backward 后半段才集中通信，延迟高。
- **过小**：桶多、通信次数多，小消息多、带宽利用率低、延迟也高。
- **经验**：默认 25MB 对很多模型已不错；若 **GPU 间带宽高、模型层多**，可适当**增大**（如 50MB）让单次通信更饱满；若 **模型小、梯度张量碎**，可适当**减小**让更早的桶先发、增加重叠。可结合 profiler 看 all-reduce 与 backward 的时间线，调一两次对比。

---

## 面试要点

- Bucketing = 多个小梯度打包成一桶，按桶做 all-reduce，减少通信次数、提高带宽利用。
- 桶内参数顺序与 backward 一致，使「桶满即发」能与后续 backward 重叠。
- bucket_cap_mb 过大重叠少、过小消息碎；按带宽与模型结构试 25MB 上下。

---

## 记忆要点

1. 目的：小梯度打包成桶，按桶 all-reduce，减少次数、提高带宽。
2. 桶满即发、与 backward 顺序一致，实现通信与计算重叠。
3. 调优：默认 25MB；高带宽可略大，小模型可略小；用 profiler 看时间线。

[返回模块](./README.md) | [返回总览](../README.md)
