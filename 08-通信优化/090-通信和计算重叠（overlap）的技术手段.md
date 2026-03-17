# 第 90 题：通信和计算重叠（overlap）的技术手段？`double buffering`？

## 题目

通信和计算重叠（overlap）的技术手段？`double buffering`？

---

## 完整讲解

### 一、重叠的目标

**通信与计算重叠**：在 GPU 做当前 layer 的算时，**同时**在后台做 all-reduce 或其它 collective（上一 layer 的梯度），这样通信时间被「藏在」计算里，总 step 时间 ≈ max(计算, 通信) 而非 计算+通信。

### 二、技术手段

- **梯度 bucket 与异步 all-reduce**：DDP 把参数按 bucket 分组，某 bucket 的 backward 一完成就**立即**对该 bucket 发起 all-reduce（非阻塞），GPU 继续算下一 bucket；这样「算」与「通信」在时间上重叠。关键是把 all-reduce 拆成多段、每段与对应计算重叠。
- **Double buffering**：两块 buffer 轮流：一块用于当前计算、一块用于通信（如拷贝或 collective）；下一 step 交换。保证计算与通信并行。
- **CUDA stream**：计算 stream 与通信 stream 分离；通信用 `cudaMemcpyAsync` 或 NCCL 的 async API，用 event 保证「梯度就绪再 all-reduce」「all-reduce 完成再 optimizer step」的依赖，其余时间两 stream 并行。
- **Overlap 与 DDP**：DDP 的 find_unused_parameters=False、bucket_cap_mb 等会影响 bucket 划分与 overlap 程度；gradient_as_bucket_view 可减少一次拷贝，利于重叠。

### 三、注意点

- 通信量或延迟过大时，再重叠也可能无法完全隐藏，此时需压缩或减少通信次数。
- 保证正确性：依赖要明确（哪步算完才可通信、通信完才可更新），用 stream/event 或 framework 内建语义保证。

---

## 面试要点

- 重叠 = 计算与通信并行；DDP bucket + 异步 all-reduce、double buffer、多 stream。
- DDP 通过 bucket 分组，每 bucket 就绪即发起 all-reduce，与后续计算重叠。
- 依赖用 stream/event 保证；通信过大时重叠可能无法完全隐藏。

---

## 记忆要点

1. Bucket 就绪即 all-reduce + 继续算下一 bucket = 重叠。
2. Double buffer + 多 stream 是通用手段；DDP 已内置 bucket overlap。
3. 正确性靠依赖与 event 保证。

[返回模块](./README.md) | [返回总览](../README.md)
