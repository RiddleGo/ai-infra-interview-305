# 第 22 题：Triton和CUDA的区别？什么时候用Triton更合适？

## 题目

Triton和CUDA的区别？什么时候用Triton更合适？

---

## 完整讲解

### 一、Triton 和 CUDA 的区别

**CUDA**：显式写 thread/block/grid、shared memory、同步；控制细、调优空间大，但开发成本高、要手管寄存器与 occupancy。**Triton**：用 **块级编程**（tile 为单元），写「对一块数据做什么」，由编译器生成 GPU kernel；自动管 block、shared memory、循环与向量化，代码更短、可读性好，易做 **auto-tuning**（如 grid 大小、tile 大小）。

- **抽象层级**：CUDA 是「线程/ warp 级」；Triton 是「tile/block 级」，更接近「矩阵块运算」。
- **内存**：Triton 用 `tl.load/tl.store` 声明访问模式，编译器做 coalescing、bank 优化；CUDA 需手写。
- **生态**：CUDA 通用、所有 NVIDIA 卡；Triton 目前主要 NVIDIA，与 PyTorch 2 的 Inductor 深度集成。

### 二、什么时候用 Triton 更合适？

- **新算子/原型**：快速实现 matmul、softmax、layernorm 等，改 tile 和 num_warps 即可调优，不必手写 shared 与循环。
- **与 PyTorch 编译栈一致**：TorchInductor 会生成 Triton；自定义 kernel 用 Triton 便于和 Inductor 融合、统一调度。
- **不适合**：极度依赖 warp 级技巧、复杂分支、或需精确控制每条指令的 kernel；以及非 NVIDIA 后端（Triton 暂不支持）。

### 三、简要对比

| 维度     | CUDA           | Triton              |
|----------|----------------|---------------------|
| 抽象     | 线程/block     | tile/block          |
| 开发效率 | 低、细节多     | 高、声明式         |
| 调优     | 手调           | 易 auto-tune        |
| 适用     | 通用、极致性能 | 新算子、PyTorch 栈 |

---

## 面试要点

- Triton：块级编程、编译器生成 kernel，自动管 shared/循环；CUDA 是线程级、手写细节。
- Triton 适合新算子、与 Inductor 统一、快速调 tile/num_warps；CUDA 适合要极致手控或非 NVIDIA 的场景。
- 能说清「块级 vs 线程级」和「谁负责 coalescing / occupancy」即可。

---

## 记忆要点

1. Triton = 块级编程，编译器生成 kernel；CUDA = 线程级，手写 grid/block/shared。
2. Triton 适合快速写 matmul/softmax/layernorm、与 PyTorch Inductor 集成；CUDA 适合极致手控。
3. 抽象层级不同：Triton 管 tile，CUDA 管 thread；Triton 易 auto-tune。

[返回模块](./README.md) | [返回总览](../README.md)
