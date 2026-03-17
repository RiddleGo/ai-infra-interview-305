# 第 183 题：Nsight Compute的`roofline model`分析？

## 题目

Nsight Compute的`roofline model`分析？

---

## 完整讲解

### 一、Roofline model 概念

**Roofline**：以 **算术强度**（Arithmetic Intensity，AI = FLOPs/Byte，即每字节数据能做的浮点运算数）为横轴、**可达性能**（GFLOPS 等）为纵轴；曲线由**算力上限**（ridge point 左侧）和**带宽上限**（右侧）组成，形成「屋顶」。**AI 小**时受**内存带宽**限制（带宽 bound）；**AI 大**时受**算力**限制（compute bound）。用于判断 kernel 或算子落在哪一侧、优化方向是省带宽还是提算力。

### 二、Nsight Compute 中的 roofline

**Nsight Compute**（ncu）可对单 kernel 做详细分析，并给出 **Roofline** 图：标出该 kernel 的 **AI** 与**实际达到的吞吐**在屋顶上的位置。若在带宽 roof 下方，说明**内存受限**，优化方向为减少全局内存访问、合并访问、用共享内存等；若在算力 roof 下方，说明**计算受限**，可考虑提高 occupancy、更多算术等。ncu 还提供 **Memory Workload Analysis**、**Compute Workload Analysis** 与具体瓶颈建议。

### 三、工程用法

先跑 `ncu --set full -o report python train.py` 等采集 kernel；在 Nsight Compute 中打开，看 Roofline 与 Top Recommendations。结合 Nsight Systems 的 timeline 确定要重点看的 kernel（热点或 gap 附近），再用 ncu 做单 kernel roofline 与建议优化。
---

## 面试要点

- Roofline：AI = FLOPs/Byte；左侧带宽 bound、右侧算力 bound，判断优化方向。
- Nsight Compute 对单 kernel 画 Roofline，标出 AI 与达到的吞吐；给 Memory/Compute 瓶颈建议。
- 带宽 bound 减访存、合并、共享内存；算力 bound 提 occupancy、算力利用。

---

## 记忆要点

1. Roofline：横轴 AI，纵轴性能；左带宽右算力。
2. ncu 给单 kernel Roofline + 瓶颈建议。
3. 带宽 bound → 减访存；算力 bound → 提算力利用。

[返回模块](./README.md) | [返回总览](../README.md)
