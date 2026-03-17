# 第 15 题：如何profile PyTorch模型的性能？`torch.profiler`和`nvprof`的使用经验？

## 题目

如何profile PyTorch模型的性能？`torch.profiler`和`nvprof`的使用经验？

---

## 完整讲解

### 一、torch.profiler 能干什么？

**torch.profiler**（或旧版 `torch.autograd.profiler.profile`）在 Python 侧记录：**每个算子**的 CPU/GPU 时间、调用次数、显存分配/释放、以及（若开 CUDA）**kernel 级**信息。可配合 **Chrome Trace**（tensorboard 的 trace viewer）看时间线，或导出表格做「谁最慢」的排序。

- **基本用法**：`with torch.profiler.profile(...) as prof:  model(x)`，然后 `prof.key_averages().table()` 或 `prof.export_chrome_trace("trace.json")`。
- **常用参数**：`activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]`、`record_shapes=True`（记 tensor shape）、`profile_memory=True`（显存）、`with_stack=True`（调用栈）。**schedule** 可做「预热 + 只录几轮」避免录太多。
- **TensorBoard**：`torch.profiler.tensorboard` 把 trace 写到 logdir，用 `tensorboard --logdir ...` 打开，在 PyTorch Profiler 的 trace 视图里看 CPU/GPU 时间线和 gap。

---

### 二、看什么、怎么优化？

- **CPU 侧**：Python 开销、DataLoader、to(device)、每个 op 的 dispatch；若 CPU 时间远大于 GPU，多半是数据或 Python 瓶颈。
- **GPU 侧**：每个 kernel 的时长、间隔（gap）；若 GPU 中间有大段空白，可能是 CPU 没及时喂数据或同步点太多。
- **显存**：`profile_memory=True` 看分配/释放时间线，找峰值和泄漏；结合 `memory_summary()` 看谁在占。
- **算子级**：按「self CPU time」或「self CUDA time」排序，找到最贵的 op，再决定是否融合、换 kernel、或减计算。

---

### 三、nvprof / Nsight 系列（nvidia 工具）

- **nvprof**（旧，部分新卡已弃用）：命令行 `nvprof python train.py`，会录 GPU kernel、显存、API 调用；输出可转成 timeline。新驱动上推荐用 **Nsight Systems / Nsight Compute**。
- **Nsight Systems**：录 **CPU + GPU 时间线**、kernel 发射、CUDA API、多进程；看「GPU 利用率低、中间有大 gap」时用，定位是等数据、等同步还是 kernel 太碎。
- **Nsight Compute**：针对**单个 kernel** 的详细指标： occupancy、memory throughput、warp 效率、roofline 等；在「已知某 kernel 慢」时做深度优化用。

经验：**先 torch.profiler 看「哪一段、哪个 op 慢」和「CPU/GPU 谁在等」；再 Nsight Systems 看时间线 gap；最后对关键 kernel 用 Nsight Compute 抠指标。**

---

### 四、简要对比

| 工具              | 层级       | 典型用途                         |
|-------------------|------------|----------------------------------|
| torch.profiler   | Python/op  | 哪个 op 慢、显存、CPU/GPU 占比   |
| Nsight Systems   | 进程/线程/kernel | 时间线、gap、谁在等          |
| Nsight Compute   | 单 kernel  | occupancy、带宽、roofline        |
| nvprof           | kernel/API | 旧卡粗略 timeline（逐渐被替代） |

---

## 面试要点

- torch.profiler：录 op/kernel 时间、显存、shape；用 schedule、record_shapes、profile_memory；看 table 或 Chrome Trace（tensorboard）。
- 分析：看 CPU vs GPU 谁主导、gap、最贵 op；再决定优化数据、融合、或换 kernel。
- nvprof 渐退场；Nsight Systems 看整体时间线与 gap；Nsight Compute 看单 kernel 指标；和 profiler 配合用。

---

## 记忆要点

1. torch.profiler：Python/op 级，activities/record_shapes/profile_memory，Chrome Trace 看时间线。
2. 优化顺序：profiler 找慢 op 和 gap → Nsight Systems 看时间线 → Nsight Compute 抠关键 kernel。
3. nvprof 旧；Nsight 是当前推荐 GPU 工具链。

[返回模块](./README.md) | [返回总览](../README.md)
