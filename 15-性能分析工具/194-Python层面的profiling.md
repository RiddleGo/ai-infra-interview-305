# 第 194 题：Python层面的profiling？`cProfile`、`py-spy`？

## 题目

Python层面的profiling？`cProfile`、`py-spy`？

---

## 完整讲解

### 一、Python 层成为瓶颈时

**Python 侧**：解释器开销、GIL、过多 Python 调用（如逐元素操作）、**数据预处理与 dataloader** 在 Python 中执行等，可能拖慢整体。需要**在 Python 层做 profiling**，看哪些函数、哪行代码占 CPU 多，而不是只看 GPU。

### 二、cProfile

**cProfile**（Python 标准库）：**确定性 profiler**，记录每个函数的**调用次数与累计耗时**。用法：`python -m cProfile -o out.prof train.py` 或代码内 `cProfile.run('func()')`；用 **pstats** 或 **snakeviz** 查看。可看到 **Python 调用栈** 与热点函数；适合找「谁在占 CPU」——如某个 dataloader 的 collate、或某段预处理。**注意**：会拖慢执行，且主要反映 CPU 时间，不直接反映 GPU 等待。

### 三、py-spy

**py-spy**：**采样式** profiler，**无需改代码、无需重启**，通过 **ptrace**（或类似机制）定期采样 Python 进程的调用栈。`py-spy top` 实时看热点；`py-spy record -o profile.svg` 生成火焰图。**优点**：低侵入、可对已运行进程采样、开销小。**适用**：生产或长时间运行时的**现场采样**，看当前 Python 热点；与 cProfile 互补（cProfile 更精确、py-spy 更轻量、可事后挂载）。
---

## 面试要点

- Python 层瓶颈时需做 Python 侧 profiling（热点函数、调用栈）。
- cProfile：确定性、每函数调用次数与耗时；python -m cProfile 或 run()；看 pstats/snakeviz。
- py-spy：采样式、无需改代码、可挂载运行中进程；top/record 火焰图；低侵入。

---

## 记忆要点

1. cProfile = 标准库、确定性；看 Python 函数耗时与次数。
2. py-spy = 采样、可挂载、火焰图；低侵入。
3. 二者配合：cProfile 精确，py-spy 现场采样。

[返回模块](./README.md) | [返回总览](../README.md)
