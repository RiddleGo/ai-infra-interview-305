# 第 204 题：动态shape的优化困境？`torch.compile`的`dynamic=True`？

## 题目

动态shape的优化困境？`torch.compile`的`dynamic=True`？

---

## 完整讲解

### 一、动态 shape 的困境

**动态 shape**：batch、seq_len 等维度在**运行时变化**（如不同请求不同长度）。**困境**：（1）**编译/优化**：TensorRT、torch.compile 等常针对**固定 shape** 做 kernel 选择与融合，动态时需为多种 shape 编译或 **runtime 选择**，增加编译时间与缓存复杂度；（2）**CUDA Graph**：图内 size 固定，shape 变需重捕或多图；（3）**性能**：同一 kernel 在不同 shape 下效率不同，动态难以「每 shape 最优」。

### 二、torch.compile 的 dynamic=True

**torch.compile(..., dynamic=True)**：告诉编译器 **batch 或某些维是动态**的，生成的代码会**保留动态分支**或**参数化 shape**，在运行时按实际 shape 执行，而非为单一 shape 特化。**好处**：一套编译结果可应对多种 shape，减少 recompile。**代价**：可能无法做某些**强依赖固定 shape** 的优化（如部分融合、静态分配），性能可能略逊于固定 shape 的专门编译。**适用**：推理请求 batch/seq 多变、或训练中 batch 不固定时使用。

### 三、工程取舍

**固定 shape**：推理时 **padding 到固定长度** 或 **batch 固定**，便于极致优化与 CUDA Graph；**动态 shape**：少 padding 浪费、接口灵活，用 dynamic=True 或多 shape 编译。长尾 shape 可 **fallback 到 eager** 或**按桶（bucket）** 编译几种典型 shape。
---

## 面试要点

- 动态 shape 导致编译/优化复杂、CUDA Graph 难用、难以每 shape 最优。
- torch.compile(..., dynamic=True) 生成适应动态维的代码，一套编译多 shape；可能牺牲部分优化。
- 取舍：固定 shape 利于极致优化；动态 + dynamic=True 或按桶编译折中。

---

## 记忆要点

1. 动态 shape：编译多、Graph 难、性能难每 shape 最优。
2. dynamic=True：一套编译应对多 shape；可能少部分优化。
3. 固定 vs 动态：按业务选；可 bucket 或 fallback。

[返回模块](./README.md) | [返回总览](../README.md)
