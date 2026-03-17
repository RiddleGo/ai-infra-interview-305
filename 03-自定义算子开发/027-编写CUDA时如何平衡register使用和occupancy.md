# 第 27 题：编写CUDA时如何平衡register使用和occupancy？

## 题目

编写CUDA时如何平衡register使用和occupancy？

---

## 完整讲解

### 一、Register 和 occupancy 的关系

每个 **block** 使用的 **register 总数** = 每线程 register 数 × 每 block 线程数；SM 上 register 总量有限，**每 block 用得多 → 同时能驻留的 block 少 → 每 SM 的 warp 数少 → occupancy 低**。反之，少用 register（如把中间结果放进 shared、或拆 kernel）可提高 occupancy，用更多 warp 隐藏 **latency**（尤其是 memory latency）。

### 二、为什么不能一味追求高 occupancy？

- **Occupancy 高** 只说明「有很多 warp 可切换」，若 kernel 本身 **compute bound**、不常等内存，多加 warp 反而增加 **register/shared 竞争**、可能更慢。
- **Occupancy 低** 但 **每个 warp 做更多有用计算**（如循环展开、更多寄存器缓存）有时更快；典型如 **GEMM** 里用较大 tile、多 stage，register 用得多、occupancy 中等，但吞吐更高。
- 因此要结合 **stall 原因**（Nsight Compute）：若主要是 **Memory Throttle**，提 occupancy 常有帮助；若是 **Instruction/Compute**，优先优化计算与指令吞吐。

### 三、怎么平衡？

- **先测**：用 Nsight Compute 看当前 occupancy、stall 分布；若 memory stall 高且 occupancy 低，尝试 `--maxrregcount` 或改代码减 register（少局部变量、用 shared 代替）。
- **再试**：在「减 register 提 occupancy」与「多 register 做展开/缓存」之间做 A/B；不同 kernel 最优点不同。
- **经验**：memory-bound kernel 常受益于更高 occupancy；compute-bound 的看 instruction throughput 与 occupancy 的折中。

---

## 面试要点

- Register 多 → 每 block 占得多 → occupancy 低；减 register（或 shared 替代）可提 occupancy，利于藏内存延迟。
- 高 occupancy 不一定更快：compute bound 时多 warp 可能只增加竞争；要看 stall 原因再决定。
- 平衡：看 Nsight stall；memory stall 多则试提 occupancy；compute 多则看指令与 register 的折中。

---

## 记忆要点

1. Register 用量 ↔ 每 block 占用 ↔ occupancy 成反比；减 register 可提 occupancy。
2. 高 occupancy 主要利于隐藏内存延迟；compute bound 时未必更好，有时更多 register 做展开更快。
3. 用 Nsight 看 stall；按 memory vs compute 决定是提 occupancy 还是提单 warp 效率。

[返回模块](./README.md) | [返回总览](../README.md)
