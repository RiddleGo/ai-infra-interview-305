# 第 25 题：算子优化中的memory coalescing、bank conflict、occupancy分别指什么？

## 题目

算子优化中的memory coalescing、bank conflict、occupancy分别指什么？

---

## 完整讲解

### 一、Memory coalescing

**Coalescing**：同一 warp 的线程访问 **连续地址**（如 thread i 访问 `addr_base + i`）时，硬件可合并成**少量（甚至一次）global memory 事务**；若线程访问分散或错位，会产生多次事务，带宽利用率低。优化：让 **相邻 thread 访问相邻地址**（如 threadIdx.x 对应连续下标）、避免随机步长；对 2D/3D 注意 **行主序** 下把连续维映射到 threadIdx.x。

### 二、Bank conflict

**Shared memory** 按 bank 分（如 32 bank、4B 宽）；同一 warp 内**不同线程访问同一 bank 的不同地址**会 **bank conflict**，访问被串行化。避免方式：**padding**（在行末加空位使错开 bank）、**改变访问模式**（如转置用 shared 做分块避免同一 bank 多地址）、或设计成同一 warp 访问同一地址（broadcast，无 conflict）。

### 三、Occupancy

**Occupancy** = 同时驻留的 warp 数 / 硬件最大 warp 数，反映 **延迟隐藏** 能力。受限于：**每 block 的 register**、**每 block 的 shared memory**、**每 SM 的 block 上限**。register 用得多 → 每 block 能放的 warp 少 → occupancy 低；但有时 **少 register、高 occupancy** 反而因更多 warp 争抢而变慢。要在 **occupancy 与 per-thread 资源** 之间做权衡，用 Nsight Compute 看实际 occupancy 与 stall 原因。

### 四、关系简述

- Coalescing 决定 **global 带宽**；bank conflict 决定 **shared 有效带宽**；occupancy 决定 **能否用足够多 warp 藏延迟**。
- 三者都影响 kernel 最终性能，需一起看；先保证 coalescing 与无严重 bank conflict，再调 occupancy。

---

## 面试要点

- Memory coalescing：同 warp 访问连续地址可合并为少量事务；优化为相邻 thread 访问相邻地址。
- Bank conflict：shared 同 warp 多线程访问同 bank 不同地址会串行化；用 padding 或改访问模式避免。
- Occupancy：驻留 warp 数/最大 warp 数，受 register/shared 限制；与 per-thread 资源权衡，看 Nsight 实际值。

---

## 记忆要点

1. Coalescing：同 warp 连续地址 → 合并访存；相邻 thread 对应连续下标。
2. Bank conflict：shared 同 bank 多地址 → 串行；padding 或改布局可避免。
3. Occupancy：受 register/shared 限制；高 occupancy 不一定更快，需结合 stall 分析。

[返回模块](./README.md) | [返回总览](../README.md)
