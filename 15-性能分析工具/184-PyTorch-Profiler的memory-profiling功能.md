# 第 184 题：PyTorch Profiler的`memory profiling`功能？

## 题目

PyTorch Profiler的`memory profiling`功能？

---

## 完整讲解

### 一、Memory profiling 的目的

**显存分析**：看**分配与释放**发生在何时、哪段代码，以及**峰值与泄漏**。训练 OOM 或推理显存不稳时，需知道是哪些 tensor、哪几层导致峰值；是否有未释放的中间结果或缓存。

### 二、PyTorch Profiler 的 memory 功能

**torch.profiler** 或 **torch.autograd.profiler** 可开启 **profile_memory=True**（或 `with torch.profiler.profile(profile_memory=True)`），记录 **alloc 与 free 事件**、每 operator 的 **显存增量**。导出后可在 **Chrome trace** 或 **PyTorch Profiler 表格** 中按时间线看「某 step 内哪些 op 分配了多少」、**峰值时刻** 对应的调用栈。**memory_profile=True**（新 API）会生成更细的显存时间线。

### 三、使用要点

需在**足够代表**的 step 上采集（如一个完整 step 或若干 step）；注意 **CUDA 缓存**（allocator 会预留池），看到的「已分配」可能高于当前 tensor 实际需求。结合 **torch.cuda.memory_summary()**、**memory_allocated()** 做点状检查；profiler 做时间维度的分配归属与峰值定位。
---

## 面试要点

- Memory profiling 用于定位显存峰值、泄漏与各 op 的分配贡献。
- PyTorch Profiler 开 profile_memory / memory_profile，看 alloc/free 时间线与 per-op 增量。
- 结合 memory_summary、memory_allocated 做点状检查；在代表 step 上采足够长。

---

## 记忆要点

1. 显存分析：分配/释放时间线、峰值、per-op 贡献。
2. torch.profiler profile_memory=True；导出看 Chrome trace 或表格。
3. 代表 step 采集；注意 CUDA cache 与真实 tensor 区别。

[返回模块](./README.md) | [返回总览](../README.md)
