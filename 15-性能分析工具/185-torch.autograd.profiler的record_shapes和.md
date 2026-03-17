# 第 185 题：`torch.autograd.profiler`的`record_shapes`和`profile_memory`？

## 题目

`torch.autograd.profiler`的`record_shapes`和`profile_memory`？

---

## 完整讲解

### 一、record_shapes

**record_shapes**：在 **torch.autograd.profiler** 或 **torch.profiler** 中开启后，会记录每个 **operator 的输入/输出 tensor 的 shape**。便于在分析结果中看到「某 op 是在什么 shape 下被调用的」（如 batch、seq_len、hidden），用于判断是否因**动态 shape** 导致多次编译、或某 shape 特别耗时，以及做容量与优化决策。

### 二、profile_memory

**profile_memory**：记录 **CUDA 显存分配与释放** 事件及归属到哪个 op。可看到每个 op 的 **显存增量**（正为分配、负为释放）、时间线上的分配峰值，用于定位 OOM 对应的 op 与 tensor、以及显存泄漏（某 op 只增不释）。需在代表性 step 上采集足够长；注意 PyTorch 的 caching allocator 会复用块，看到的「分配」可能包含池化。

### 三、使用场景

**record_shapes**：排查动态 shape、大 tensor、异常 batch 维；与 **torch.compile** 或 TensorRT 的 shape 相关问题时常用。**profile_memory**：OOM、显存峰值优化、多模型/多阶段共享显存时理清谁在何时占用多少。二者可同时开，在同一个 profile 里既看耗时又看 shape 与显存。
---

## 面试要点

- record_shapes：记录每 op 的输入/输出 shape，用于动态 shape、异常 batch、编译次数分析。
- profile_memory：记录显存 alloc/free 与 per-op 增量，用于峰值与泄漏定位。
- 二者可同开；在代表 step 上采集，结合 trace 与表格分析。

---

## 记忆要点

1. record_shapes = 记录 op 的 tensor shape；查动态 shape、大 tensor。
2. profile_memory = 记录显存分配与归属；查峰值与泄漏。
3. 同开可同时看耗时、shape 与显存。

[返回模块](./README.md) | [返回总览](../README.md)
