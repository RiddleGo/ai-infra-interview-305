# 第 36 题：解释`loop tiling`、`loop unrolling`、`vectorization`在编译器优化中的作用

## 题目

解释`loop tiling`、`loop unrolling`、`vectorization`在编译器优化中的作用

---

## 完整讲解

### 一、Loop tiling（分块）

**Tiling** 把大循环 **按块划分**：外层遍历「块」，内层遍历「块内」。例如 `for i in 0..N` 变成「for bi 遍历块，for i 遍历块内」。作用：**提高局部性**——块内数据可放进 **cache 或 register**，重复使用后再换下一块，减少主存/全局内存访问；同时便于 **并行**（不同块可不同 thread/block）。在矩阵乘、卷积等里 tiling 是基础优化，对应 CUTLASS/TVM 的 threadblock tile、warp tile。

### 二、Loop unrolling（循环展开）

**Unrolling** 把循环体 **复制多份**，减少循环判断与分支、增加指令级并行与寄存器复用。例如 `for (i=0;i<4;i++) a[i]=...` 展开成 4 条赋值。编译器可自动做（`#pragma unroll` 或 -O3），也可手写。注意：展开过多会 **代码膨胀、register 压力大**；要结合 tiling 与后端限制（如 GPU 每 block register 数）权衡展开因子。

### 三、Vectorization（向量化）

**向量化** 让一条指令处理 **多个数据**（SIMD）：用向量 load/store、向量运算代替标量循环。例如标量 `for i: c[i]=a[i]+b[i]` 变成向量 `c[0:4]=a[0:4]+b[0:4]`。作用：**提高吞吐**、更好利用 **带宽与算力**。在 CPU 上对应 SSE/AVX/NEON；在 GPU 上对应 warp 内线程协作、或 tensor core。编译器通过 **循环向量化 pass** 或显式向量类型实现；需 **连续/对齐访问**、无循环依赖等条件。

### 四、在编译器中的配合

- **Tiling** 先缩小「单块」规模，使块内适合 **cache/register**，并为 unroll/vectorize 提供小范围循环。
- **Unroll** 在块内减少分支、增加并行与复用。
- **Vectorize** 在最内层或合适层级用 SIMD/向量指令提高吞吐。
- 三者常一起用：tile 外层 → 内层 unroll + vectorize；TVM/MLIR 的 schedule 或 pass 会应用这些变换。

---

## 面试要点

- Tiling：按块划分循环，提高局部性、利于 cache/并行；矩阵类算子的基础。
- Unrolling：复制循环体，减分支、增指令并行与复用；过度会代码膨胀、register 压力大。
- Vectorization：SIMD/向量指令，提高吞吐；需连续访问、无依赖等；与 tiling/unroll 配合。

---

## 记忆要点

1. Tiling = 分块，提局部性、利 cache 与并行；unroll = 展开减分支；vectorize = SIMD 提吞吐。
2. 顺序常为：tile 外层 → 内层 unroll + vectorize；编译器 pass 或 schedule 应用。
3. 三者配合：tile 定块大小，块内 unroll/vectorize 榨取性能。

[返回模块](./README.md) | [返回总览](../README.md)
