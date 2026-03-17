# 第 266 题：`template metaprogramming`在CUDA优化中的应用？

## 题目

`template metaprogramming`在CUDA优化中的应用？

---

## 完整讲解

### 一、模板元编程在 CUDA 中的角色

CUDA kernel 常需在**编译期**确定 block 大小、tile 尺寸、循环上界、数据类型等，以生成最优指令与寄存器使用。C++ **template metaprogramming（TMP）** 用模板参数与特化在编译期计算类型与常量，避免运行时分支与重复代码。

### 二、典型应用

**Tile 尺寸**：用 `template<int TileM, int TileN>` 让编译器为不同 Tile 生成特化，便于调优。**类型多态**：`template<typename T>` 写一套 kernel，对 float/half 等分别实例化。**循环展开**：用 `#pragma unroll` 配合模板常量做编译期展开。**条件编译**：用 `if constexpr` 或模板特化在编译期选择分支（如是否用 FP16 累加）。

### 三、工程经验

TMP 增加编译时间与二进制体积，但能消除运行时分支、利于寄存器分配与指令选择；CUTLASS、cuBLAS 等库大量使用模板配置 GEMM 与 epilogue。

---

## 面试要点

- 模板元编程在编译期确定 tile、类型、循环等，利于 CUDA 生成最优代码。
- 应用：Tile 尺寸、类型多态、循环展开、if constexpr 分支选择。
- 增加编译成本，但减少运行时分支、利于寄存器与指令优化。
- CUTLASS/cuBLAS 等大量用模板配置算子。

---

## 记忆要点

1. TMP = 编译期确定参数；tile、类型、unroll 常用。
2. 消除运行时分支、利于寄存器与指令；代价是编译时间。
3. 工程上 CUTLASS 等用模板配置 GEMM/epilogue。

[返回模块](./README.md) | [返回总览](../README.md)
