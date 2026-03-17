# 第 207 题：数据预处理的`multi-processing`优化？`num_workers`调优？

## 题目

数据预处理的`multi-processing`优化？`num_workers`调优？

---

## 完整讲解

### 一、多进程加载的目的

**DataLoader** 用 **多进程**（num_workers>0）在**多个 CPU 进程**里并行做 **读数据、解码、增强**，通过 **队列** 把 batch 送给主进程，减少「主进程串行做 IO + 预处理」导致的 **GPU 等数据**。多进程可把数据加载与 GPU 计算**重叠**，提高吞吐。

### 二、num_workers 调优

**过小**：预取不足，GPU 常等数据；**过大**：CPU 与内存争抢、进程切换开销、可能反而变慢，且 **共享内存** 占用增加。**经验**：从 **4～8** 起调，看 **GPU 利用率** 与 **吞吐**；若 GPU 利用率已高、再增 workers 无提升则可停。**与 batch 关系**：通常 workers 略大于或等于「能填满 GPU 的 pipeline 深度」（如 2×batch 预取），不必远大于。**Windows**：多进程有 spawn 限制，有时 num_workers=0 或 1 更稳，可配合 prefetch_factor。

### 三、其它要点

**persistent_workers=True**：worker 进程不随 epoch 结束而销毁，避免每 epoch 重新 fork；适合多 epoch 训练。**pin_memory + non_blocking**：与 206 题配合。**GIL**：解码与 Python 逻辑在 worker 里执行，若 Python 侧过重可考虑 DALI 或 C++ 扩展把重活迁出。
---

## 面试要点

- 多进程 DataLoader：并行读与预处理，与 GPU 计算重叠；num_workers>0。
- num_workers 从 4～8 起调，看 GPU 利用率与吞吐；过大反而可能变慢或占内存。
- persistent_workers 多 epoch 可开；配合 pin_memory、non_blocking；重活可迁 DALI。

---

## 记忆要点

1. 多进程 = 并行加载与预处理；减 GPU 等数据。
2. num_workers 适度；过小等数据、过大争资源。
3. persistent_workers、pin_memory、non_blocking 配合。

[返回模块](./README.md) | [返回总览](../README.md)
