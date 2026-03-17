# 第 166 题：数据加载的`bottleneck`诊断？`nvidia-smi dmon`？

## 题目

数据加载的`bottleneck`诊断？`nvidia-smi dmon`？

---

## 完整讲解

### 一、数据加载 Bottleneck 表现

**GPU 利用率低**、**吞吐上不去**而 CPU 或 IO 占用高，多半是**数据侧瓶颈**：DataLoader 供不上 batch，GPU 在等数据。可能原因：磁盘 IO 慢、预处理（decode、tokenize）重、DataLoader worker 少、GIL、网络存储延迟等。

### 二、诊断思路

（1）**时间线**：用 PyTorch Profiler 或 Nsight Systems 看 **CPU 与 GPU 时间线**：若 GPU 有大量「等待」或空档、而 CPU 在忙解码/读盘，则瓶颈在数据。（2）**Worker 与 prefetch**：看 DataLoader 的 num_workers、prefetch_factor；过小则预取不足。（3）**磁盘与 IO**：iostat、存储带宽；若从网络盘读，看延迟与带宽。（4）**nvidia-smi dmon**：**dmon** 是 nvidia-smi 的**持续监控模式**，可看 GPU 利用率、显存、功耗等随时间变化；若 **GPU 利用率周期性掉下去**、与 batch 边界对齐，常说明 GPU 在等数据；配合 CPU 侧 profiling 可确认是「等数据」而非「等通信」。

### 三、nvidia-smi dmon 用法

`nvidia-smi dmon -s u -c 10`：每 1 秒采样一次、共 10 次，-s u 表示 utilization；可看 gpu 列与 sm 列（计算利用率）。若 sm 经常为 0 或很低而训练在跑，多半是 CPU/IO 瓶颈。

---

## 面试要点

- 瓶颈表现：GPU 利用率低、吞吐上不去；原因常为 IO、预处理、worker 不足。
- 诊断：Profiler 看 CPU/GPU 时间线；DataLoader worker/prefetch；iostat/存储；nvidia-smi dmon 看 GPU 利用率随时间。
- dmon：持续看利用率；周期性掉到 0 且与 batch 对齐 → 等数据；配合 CPU 侧确认。

---

## 记忆要点

1. 数据瓶颈 = GPU 等数据；表现利用率低、CPU/IO 忙。
2. 诊断 = 时间线 + worker/prefetch + IO + nvidia-smi dmon。
3. dmon 看利用率曲线；周期掉 0 → 常为等数据。

[返回模块](./README.md) | [返回总览](../README.md)
