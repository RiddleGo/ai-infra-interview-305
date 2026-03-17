# 第 187 题：`perf`和`eBPF`在CPU侧的profiling？

## 题目

`perf`和`eBPF`在CPU侧的profiling？

---

## 完整讲解

### 一、perf 在 CPU 侧的作用

**perf**（Linux perf_events）：采样 **CPU 上的热点**（函数、指令、cache miss、分支预测等），通过 **perf record / perf report** 得到调用栈与占比。训练/推理若 **CPU 成为瓶颈**（如 dataloader、预处理、Python 解释器），可用 perf 看哪些函数占 CPU 多、是否有不必要的系统调用或锁竞争。

### 二、eBPF 在 CPU profiling 的应用

**eBPF**：在内核中运行**安全沙箱程序**，可挂载到各类事件（系统调用、tracepoint、kprobe）做**低开销**的统计与过滤。用于 CPU 侧：**CPU 采样**（如 BCC 的 profile）、**off-CPU 分析**（看进程在等什么）、**锁与调度** 分析。相比 perf 可做更**定制化**的过滤与聚合（如按 PID、按调用栈标签），且通常**无需改应用**、开销小。

### 三、与 GPU 分析的配合

GPU 瓶颈时用 Nsight/CUDA profiler；**CPU 瓶颈**（数据加载、Python、通信的 CPU 侧）用 perf 或 eBPF 定位。**off-CPU**：若 GPU 在等 CPU，用 eBPF 看 CPU 进程在等什么（等 IO、等锁、等调度），可精确定位到系统调用或内核路径。
---

## 面试要点

- perf：CPU 热点采样、调用栈、cache/分支；用于 dataloader、Python、系统调用瓶颈。
- eBPF：内核可编程、低开销；可做 CPU 采样、off-CPU、锁与调度分析，定制过滤。
- CPU 瓶颈用 perf/eBPF；与 GPU 分析配合，off-CPU 可看「等什么」。

---

## 记忆要点

1. perf = CPU 热点、调用栈、cache；perf record/report。
2. eBPF = 内核挂载、低开销、可定制；CPU/off-CPU/锁分析。
3. CPU 瓶颈用二者；off-CPU 看等待原因。

[返回模块](./README.md) | [返回总览](../README.md)
