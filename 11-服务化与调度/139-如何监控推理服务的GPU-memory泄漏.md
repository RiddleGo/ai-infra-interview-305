# 第 139 题：如何监控推理服务的`GPU memory`泄漏？

## 题目

如何监控推理服务的`GPU memory`泄漏？

---

## 完整讲解

### 一、GPU 显存泄漏表现

推理服务长时间运行后显存持续增长、最终 OOM，或 nvidia-smi 显示进程占用显存只增不减，多为**显存泄漏**。常见原因：每请求分配临时 buffer 或 KV cache 未释放、CUDA graph 或缓存未清理、模型推理中创建中间 tensor 未释放、第三方库或 driver 层泄漏。

### 二、监控手段

（1）**进程级**：定期采集 `nvidia-smi` 或 DCGM 的 per-process 显存，看随时间是否单调增；设告警阈值与增长率。（2）**框架级**：PyTorch 用 `torch.cuda.memory_allocated()`、`memory_reserved()` 在请求前后或周期打点，对比是否回落；Triton 等看 backend 提供的内存统计。（3）**请求级**：对单次请求前后打显存快照，定位是否某类请求导致增长。（4）**工具**：Nsight Systems、cuda-memcheck 做长时间或单次追踪，看分配栈与未释放块。

### 三、定位与修复

结合监控确定是「每请求涨一点」还是「偶发大涨」；再通过请求类型、模型路径、版本缩小范围。修复：确保每次推理后释放临时 buffer、正确管理 KV cache 生命周期、避免在热路径上重复建大 tensor；升级框架或 driver 以修已知泄漏。

---

## 面试要点

- 表现：长时间运行显存持续增、OOM；原因多为 buffer/KV 未释放、缓存未清、框架或 driver 问题。
- 监控：nvidia-smi/DCGM 进程显存趋势；PyTorch memory_allocated 打点；请求前后快照；cuda-memcheck/Nsight 追踪。
- 定位：看是否每请求涨或偶发涨；修复：保证释放、管理 KV 生命周期、升级已知修复版本。

---

## 记忆要点

1. 泄漏 = 显存只增不减、最终 OOM；原因 buffer/KV/缓存/框架。
2. 监控 = 进程显存趋势 + 请求前后打点 + 工具追踪分配栈。
3. 修复 = 释放临时、管理 KV、避免热路径重复分配、升级版本。

[返回模块](./README.md) | [返回总览](../README.md)
