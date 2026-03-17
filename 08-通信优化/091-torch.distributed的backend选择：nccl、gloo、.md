# 第 91 题：`torch.distributed`的`backend`选择：`nccl`、`gloo`、`mpi`？

## 题目

`torch.distributed`的`backend`选择：`nccl`、`gloo`、`mpi`？

---

## 完整讲解

### 一、NCCL

**NCCL**（NVIDIA Collective Communications Library）：面向 **GPU 集体通信**（all-reduce、all-gather、broadcast 等），利用 NVLink、多 GPU、多机 IB/TCP，**性能最优**。**限制**：仅支持 GPU tensor；多机需 NCCL 与网络（IB 或 socket）正确配置。PyTorch 多卡/多机 GPU 训练**默认推荐 nccl**。

### 二、Gloo

**Gloo**：PyTorch 自带的 CPU/GPU collective 实现，支持 CPU tensor、也支持 GPU（通过 CUDA）。**优点**：无需 NCCL、易调试、支持更多 reduce 类型与自定义 op。**缺点**：GPU 上性能通常不如 NCCL，多机用 TCP。适合 **CPU 训练、或 GPU 上调试/小规模**，或无 NCCL 环境。

### 三、MPI

**MPI**：使用系统 MPI 库（如 OpenMPI、MVAPICH）做 collective。**优点**：与现有 HPC 环境兼容、功能全。**缺点**：需单独安装 MPI、与 PyTorch 的集成不如 nccl/gloo 简单，调试与部署略重。适合 **已有 MPI 的集群、或与其它 MPI 程序协同** 时。

### 四、选择建议

- **多卡/多机 GPU 训练**：用 **nccl**；无 IB 时 nccl 走 socket 也可。
- **仅 CPU 或调试**：用 **gloo**。
- **与 HPC/MPI 生态集成**：用 **mpi** backend。设置方式：`torch.distributed.init_process_group(backend='nccl', ...)`。

---

## 面试要点

- nccl：GPU 集体通信、性能最好，多卡/多机首选；gloo：CPU 或调试、易用；mpi：与 HPC 集成。
- GPU 训练默认 nccl；仅 CPU 或无 NCCL 用 gloo。
- init_process_group(backend='nccl'/'gloo'/'mpi')。

---

## 记忆要点

1. nccl = GPU 最优；gloo = CPU/调试；mpi = HPC 集成。
2. 多卡 GPU → nccl；CPU 或调试 → gloo。
3. Backend 需与设备与环境匹配。

[返回模块](./README.md) | [返回总览](../README.md)
