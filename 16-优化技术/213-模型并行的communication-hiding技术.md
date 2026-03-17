# 第 213 题：模型并行的`communication hiding`技术？

## 题目

模型并行的`communication hiding`技术？

---

## 完整讲解

### 一、Communication hiding 的含义

**Communication hiding**：在模型并行（含流水线、张量并行）中，让 **计算与通信在时间上重叠**，用 **计算** 去「藏」**通信延迟**，使通信不单独占用 wall-clock 时间，从而提高整体效率。若不重叠，总时间 ≈ 计算时间 + 通信时间；重叠后总时间 ≈ max(计算, 通信) 或略多。

### 二、常见手段

**预取（overlap）**：在 **需要某数据之前** 就发起 **recv 或 all-reduce**，在后续计算进行时通信在后台完成；到真正用该数据时已就绪。例如：**下一层的 all-reduce 与当前层计算重叠**；或 **send 本层结果的同时做下一层计算**。**双缓冲 / 多 buffer**：用 **两套（或多套）buffer** 轮转：一套在算、一套在通信，下一轮交换。**异步通信**：用 **非阻塞** collective（如 ncclAllReduce 异步版）或 **point-to-point** 的 isend/irecv，不阻塞计算流；用 **event/stream** 保证「用数据前通信完成」。

### 三、与流水线、张量并行的结合

**流水线**：各 stage 间 **send/recv 与 backward/forward 重叠**；micro-batch 调度使「算」与「传」并行。**张量并行**：all-reduce 与 matmul 重叠（如 Megatron 中 column/row 并行后的 all-reduce 与后续层计算重叠）。**实现**：依赖 **CUDA stream、NCCL 非阻塞 API、以及计算图切分** 使通信与计算在不同 stream 或不同阶段交错。
---

## 面试要点

- Communication hiding：计算与通信重叠，用计算藏通信延迟；总时间 ≈ max(计算,通信)。
- 手段：预取、双缓冲、异步 collective/point-to-point；event/stream 保证依赖。
- 流水线中 stage 间传与算重叠；张量并行中 all-reduce 与 matmul 重叠。

---

## 记忆要点

1. Hiding = 计算与通信重叠；总时间 ≈ max(算,通信)。
2. 预取、双缓冲、异步通信；stream/event 保证顺序。
3. 流水线/张量并行中与层间通信重叠。

[返回模块](./README.md) | [返回总览](../README.md)
