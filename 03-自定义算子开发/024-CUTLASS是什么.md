# 第 24 题：CUTLASS是什么？什么时候需要用它而不是手写CUDA？

## 题目

CUTLASS是什么？什么时候需要用它而不是手写CUDA？

---

## 完整讲解

### 一、CUTLASS 是什么？

**CUTLASS**（CUDA Templates for Linear Algebra Subroutines）是 NVIDIA 的 **CUDA 模板库**，提供高性能 **矩阵乘、卷积** 等 building blocks；用 **C++ 模板** 抽象 threadblock tile、warp 级 MMA（matrix multiply-accumulate）、shared memory 分块、双缓冲等，方便组合出不同 shape、精度（fp16/bf16/int8）、Epilogue（加 bias、relu 等）的 kernel，而不必从零手写每类 GEMM。

- **层级**：Device → Threadblock → Warp → MMA；每层可配置 tile 大小、stages（流水）、Epilogue。
- **用途**：做 **GEMM、batched GEMM、conv**；很多推理/训练库底层用 CUTLASS 或类似思路。

### 二、什么时候用 CUTLASS 而不是手写 CUDA？

- **用 CUTLASS**：要快速得到 **接近 cuBLAS 水平** 的 matmul/conv，或要 **多种 shape、精度、Epilogue 组合**；接受模板编译慢、二进制大，以换开发效率与可维护性。适合做推理引擎、算子库、新硬件的 GEMM 参考。
- **手写 CUDA**：**极端定制**（非常规 layout、稀疏、特殊融合）、**教学/研究**、或 **非 NVIDIA GPU**；以及不想引入 CUTLASS 依赖与编译成本时。
- **折中**：用 CUTLASS 的 **概念**（tile、warp MMA、epilogue）自己写简化版 kernel，或只接 CUTLASS 生成的某几类 kernel。

### 三、与 cuBLAS、Triton 的关系

- **cuBLAS**：闭源、接口固定；CUTLASS 开源、可改 Epilogue 和融合。
- **Triton**：更上层、块级语言；CUTLASS 是 C++ 模板、控制更细，二者可互补（Triton 调 CUTLASS 或仿其思路）。

---

## 面试要点

- CUTLASS = NVIDIA 的 GEMM/卷积模板库，抽象 threadblock/warp MMA/Epilogue，便于组合不同 shape、精度、融合。
- 用 CUTLASS：要高性能 GEMM/conv、多种组合、少写手写代码；手写 CUDA：极端定制、非 NVIDIA、或轻量依赖。
- 与 cuBLAS（闭源固定）和 Triton（更上层）的定位差异要能说清。

---

## 记忆要点

1. CUTLASS = CUDA 模板库，做 GEMM/conv；模板抽象 tile、warp MMA、Epilogue。
2. 用 CUTLASS 换开发效率与接近 cuBLAS 性能；手写用于极端定制或非 NVIDIA。
3. cuBLAS 闭源；Triton 更上层；CUTLASS 可改 Epilogue、做融合。

[返回模块](./README.md) | [返回总览](../README.md)
