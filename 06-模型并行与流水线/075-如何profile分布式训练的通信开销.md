# 第 75 题：如何profile分布式训练的通信开销？`torch.profiler`的`distributed` view？

## 题目

如何profile分布式训练的通信开销？`torch.profiler`的`distributed` view？

---

## 完整讲解

### 一、torch.profiler 与分布式

`torch.profiler` 支持多进程下的时间线汇总：用 `schedule`、`activities` 等记录各 rank 的 CPU/CUDA 与通信事件，导出 Chrome trace 或用 `profiler.key_averages()` 看汇总。**Distributed 视角**：需在各 rank 上一致地 start/stop profiler，并确保记录 **NCCL/custom collective** 事件（通常通过 CUDA 活动或 backend hook 看到通信 kernel）。

### 二、看到通信开销的方式

- **activities** 包含 `torch.profiler.ProfilerActivity.CUDA` 时，NCCL 的 kernel 会出现在 timeline 上，可看到 all-reduce、all-gather 等占用的时间与重叠情况。
- **distributed view**：部分用法指「按 rank 对比各卡 timeline」，看是否某卡通信或计算明显更长」；PyTorch profiler 导出 trace 后可在 Perfetto/Chrome 中按 process/stream 过滤各 rank。
- **key_averages**：按 operator 或 name 聚合，可看到 `nccl:all_reduce` 等占 CPU/CUDA 时间比例；`group_by_stack_n=5` 可看调用栈，定位是 DDP、FSDP 还是自定义 collective。

### 三、实操要点

- 用 `torch.profiler.profile(..., record_shapes=True)` 可看到 tensor 大小，便于对照通信量。
- 多进程时每个 rank 写单独 trace 文件（如 `trace_rank{rank}.json`），再一起打开对比；或使用能合并多进程的 profiler 后端。
- 结合 `NCCL_DEBUG=INFO` 看实际 collective 次数与大小，与 profile 里的通信事件对应，判断是否有多余或过大的 collective。

---

## 面试要点

- torch.profiler 记录 CPU/CUDA 与 NCCL 事件；各 rank 一致 start/stop，导出 trace 按 rank 对比。
- Distributed view = 按 rank 看 timeline，找通信或计算热点；key_averages 看 collective 占比。
- 与 NCCL_DEBUG、record_shapes 结合，对照 collective 次数与大小做优化。

---

## 记忆要点

1. Profiler 开 CUDA 活动可见 NCCL kernel；多 rank 分别导出 trace 对比。
2. key_averages 看 all_reduce 等占比；group_by_stack_n 看调用栈。
3. 与 NCCL_DEBUG、record_shapes 一起用，定位多余或过大通信。

[返回模块](./README.md) | [返回总览](../README.md)
