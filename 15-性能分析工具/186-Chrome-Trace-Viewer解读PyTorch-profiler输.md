# 第 186 题：Chrome Trace Viewer解读PyTorch profiler输出？

## 题目

Chrome Trace Viewer解读PyTorch profiler输出？

---

## 完整讲解

### 一、PyTorch Profiler 与 Chrome Trace

**PyTorch Profiler** 导出 **trace** 时可选择 **Chrome trace 格式**（.json），用 Chrome 浏览器打开 **chrome://tracing** 加载该文件。Trace 中每条**横条**代表一段时间内的活动（CPU op、CUDA kernel、内存拷贝等），**纵轴**为线程或 stream，可看到 **CPU 与 GPU 的并行与依赖**、gap、重叠情况。

### 二、如何解读

**时间轴**：从左到右为时间；找 **GPU stream 上的空白**（gap）即 GPU 空闲。**层级**：PyTorch 会按 op、kernel、cudaLaunch 等分层；展开可看到具体算子与 kernel 名。**颜色与长度**：长度表耗时；不同类型用不同颜色。**关联**：CPU 上「某 op」与 GPU 上「对应 kernel」可通过名称或时间对齐，判断是等数据、等启动还是等通信。

### 三、常用操作

缩放时间轴聚焦到单 step 或单次迭代；按名称搜索关键 op 或 kernel；看 gap 前后是哪个 CPU 或 CUDA 活动，对应回代码（dataloader、通信、launch）。与 Nsight Systems 互补：Chrome trace 偏 PyTorch 视角、易对回 Python；Nsight 更偏系统与 NCCL。
---

## 面试要点

- PyTorch Profiler 可导出 Chrome trace 格式，用 chrome://tracing 打开。
- 横条=活动、纵轴=线程/stream；看 CPU/GPU 并行、gap、op 与 kernel 对应关系。
- 找 gap、按名搜 op/kernel、对齐到代码；与 Nsight 互补使用。

---

## 记忆要点

1. 导出 .json → chrome://tracing 加载。
2. 横轴时间、纵轴线程；空白=gap。
3. 按名搜、看前后活动，对应回代码。

[返回模块](./README.md) | [返回总览](../README.md)
