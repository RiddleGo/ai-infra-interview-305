# 第 261 题：`CUTLASS`的`gemm`调用示例？`Epilogue`定制？

## 题目

`CUTLASS`的`gemm`调用示例？`Epilogue`定制？

---

## 完整讲解

### 一、CUTLASS GEMM 概览

CUTLASS 是 NVIDIA 的 CUDA 模板库，提供高性能 GEMM（矩阵乘）等算子。通过模板配置 **Tile** 尺寸、**ThreadBlock**、**Warp** 级结构，以及 **Epilogue**（C = f(accumulator)，如 C = alpha*A*B + beta*C、ReLU 等）。

### 二、调用示例

典型流程：定义 `GemmOperation` 类型（指定 Element、Layout、Tile、Stages 等）；用 `gemm_op()` 或 `operator()` 传入 problem size、指针、ld、alpha/beta 等；可配合 CUDA stream。Epilogue 控制输出如何从累加器写回（线性组合、激活等）。

### 三、Epilogue 定制

Epilogue 是「累加器 → 输出」的步骤，可自定义：如 `LinearCombination`、带 bias/activation 的 fusion。通过指定 Epilogue 的 ElementCompute、ElementOutput、Functor 等模板参数，实现 D = activation(alpha*A*B + beta*C + bias) 等融合写法。

---

## 面试要点

- CUTLASS 用模板配置 Tile、ThreadBlock、Epilogue，实现高性能 GEMM。
- 调用：定义 GemmOperation，传入 size、指针、ld、alpha/beta、stream。
- Epilogue 控制累加器→输出；可定制线性组合、bias、activation 等融合。
- 常用于推理/训练中的 matmul 融合与定制。

---

## 记忆要点

1. CUTLASS = 模板 GEMM；Tile + Epilogue 可配置。
2. 调用：GemmOperation + problem size + 指针 + alpha/beta。
3. Epilogue 定制 = 累加器→输出（线性、bias、activation 等）。

[返回模块](./README.md) | [返回总览](../README.md)
