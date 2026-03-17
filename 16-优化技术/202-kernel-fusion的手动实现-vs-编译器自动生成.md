# 第 202 题：`kernel fusion`的手动实现 vs 编译器自动生成？

## 题目

`kernel fusion`的手动实现 vs 编译器自动生成？

---

## 完整讲解

### 一、Kernel fusion 的两种来源

**手动实现**：用 **CUDA**（或 Triton）手写一个 kernel，把多个 op 的数学在一个 kernel 里完成（如 linear + bias + relu）；完全控制寄存器与共享内存使用、循环与访存模式。**编译器自动生成**：由 **torch.compile、XLA、TensorRT** 等根据计算图做 **pattern 匹配 + 代码生成**，自动把多个 op 合并成融合 kernel；用户无感、覆盖广，但融合策略由编译器决定，未必最优。

### 二、手动 vs 自动的取舍

**手动**：**性能上限高**、可针对热点做极致优化（如 FlashAttention）；**成本高**、维护难、覆盖有限，适合**极热点、框架/库级**。**自动**：**开发效率高**、全图可融、随图变化自动适应；**可能** register pressure 或调度不如手写、或未识别某些 pattern。**实践**：通用 op 融合交给 **torch.compile** 或 TRT；**极热点**（如 attention、norm）用手写或成熟库（FlashAttention、cuDNN）；二者结合。
---

## 面试要点

- 融合可手写（CUDA/Triton）或由编译器（torch.compile、XLA、TRT）自动做。
- 手写：性能上限高、成本高，适合极热点；自动：覆盖广、开发效率高，可能非最优。
- 实践：通用融合用编译器；极热点用手写/成熟库。

---

## 记忆要点

1. 手写 = CUDA/Triton，完全可控；自动 = 编译器按图融合。
2. 手写适合极热点；自动适合全图、快速迭代。
3. 结合：通用用 compile，热点用 FlashAttention 等。

[返回模块](./README.md) | [返回总览](../README.md)
