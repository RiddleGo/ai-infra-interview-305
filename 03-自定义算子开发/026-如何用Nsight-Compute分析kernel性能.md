# 第 26 题：如何用Nsight Compute分析kernel性能？关注哪些metrics？

## 题目

如何用Nsight Compute分析kernel性能？关注哪些metrics？

---

## 完整讲解

### 一、Nsight Compute 能看什么？

**Nsight Compute**（ncu）针对 **单个 kernel** 做细粒度分析：**占用率（occupancy）**、**warp 执行效率**、**memory throughput**（与 roofline 对比）、**指令吞吐**、**stall 原因**（等内存、等指令、等同步等）、**shared memory bank conflict**、**L1/L2 缓存** 等。先录一次 run：`ncu -o report python script.py` 或对已抓的 kernel 指定名字；再用 GUI 或 `ncu --import report.ncu-rep` 看指标。

### 二、关键 metrics 怎么读？

- **Occupancy**：实际 vs 理论最大；若很低且 stall 以「等依赖」为主，可尝试减 register、减 shared 提高 occupancy。
- **Memory throughput**：Achieved 与 Peak（GB/s）；若接近 peak 仍慢，多半是 **compute bound**；远低于 peak 是 **memory bound**，看 coalescing、bank conflict、cache 利用。
- **Warp Execution Efficiency**：非 divergent 的 warp 比例；低说明 **warp divergence** 严重。
- **Stall reasons**：Memory Throttle / Instruction Fetch / Sync 等；指导是加 occupancy 还是改访存、减分支。
- **Roofline**：算术强度与带宽/算力上限的关系，判断当前 kernel 在带宽墙还是算力墙一侧。

### 三、使用流程建议

先用 **Nsight Systems** 找「哪个 kernel 占时多」，再用 **Nsight Compute** 对该 kernel 看上述指标；根据 stall 与 throughput 决定：加 occupancy、改 coalescing、减 bank conflict、或优化计算密度。

---

## 面试要点

- Nsight Compute 看单 kernel：occupancy、memory throughput、warp 效率、stall 原因、roofline。
- 关键指标：occupancy 与 stall 关系；throughput 判断 memory vs compute bound；warp 效率看 divergence。
- 与 Nsight Systems 配合：Systems 找慢 kernel，Compute 深入该 kernel 做优化依据。

---

## 记忆要点

1. Nsight Compute = 单 kernel 分析；occupancy、throughput、warp 效率、stall、roofline。
2. 低 occupancy + 依赖 stall → 试减 register/shared；低 throughput → 看 coalescing/bank/cache。
3. 流程：Systems 定 kernel → Compute 看指标 → 按 stall/throughput 改。

[返回模块](./README.md) | [返回总览](../README.md)
