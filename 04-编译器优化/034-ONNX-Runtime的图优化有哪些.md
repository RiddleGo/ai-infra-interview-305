# 第 34 题：ONNX Runtime的图优化有哪些？`constant folding`、`operator fusion`等

## 题目

ONNX Runtime的图优化有哪些？`constant folding`、`operator fusion`等

---

## 完整讲解

### 一、ONNX Runtime 图优化概览

**ONNX Runtime** 在加载 ONNX 模型后会做一系列 **图级优化**（graph-level passes），在保持语义等价的前提下减少 op 数、减少访存、提升执行效率。常见包括：**常量折叠**、**算子融合**、**冗余消除**、**layout 转换**、**子图替换**（用更快的融合 op 替代多 op 子图）等。

### 二、Constant folding

**Constant folding**：若某 op 的输入都是 **常量**（如 initializer 或前序 fold 的结果），在 **编译时** 直接算出该 op 的输出，用 **常量** 替换该节点，从而减少运行时计算。例如 `Add(Const(1), Const(2))` → 替换为 `Const(3)`。可递归做，直到没有新的常量可算。收益：少 kernel、少中间 tensor，有时还能触发后续更多融合。

### 三、Operator fusion

**Operator fusion**：把 **多个小 op 合并成一个融合 op**（如 Conv+BN+Relu → 一个 FusedConvBNRelu kernel），减少 kernel launch 与中间结果读写。OR 内置多种 **融合规则**（pattern：某一子图 → 一个融合 op）；也支持 **EP（Execution Provider）** 提供的融合（如 CUDA EP 的 Conv+Add+Relu 等）。与 constant folding 配合：先 fold 掉常量，图更简单，融合 pattern 更易匹配。

### 四、其他常见优化

- **冗余消除**：重复的 transpose、identity、零贡献的 op 删除或合并。
- **Layout 优化**：选择 NCHW/NHWC 等，与 EP 和 kernel 实现对齐。
- **子图替换**：用更高效的实现替换整块子图（如 Attention 整块用 FlashAttention 等）。

---

## 面试要点

- OR 图优化：常量折叠、算子融合、冗余消除、layout、子图替换等；在加载模型后、执行前做。
- Constant folding：常量输入在编译期算完，用常量替换节点，可递归；利于后续融合。
- Operator fusion：多 op 合并为融合 kernel，减少 launch 与中间读写；按 pattern 匹配，EP 可扩展。

---

## 记忆要点

1. ONNX Runtime 图优化：constant folding、operator fusion、冗余消除、layout、子图替换。
2. Constant folding = 编译期算常量 op，节点换常量；fusion = 多 op 一 kernel，按 pattern。
3. 先 fold 再 fusion 更易匹配；EP 可提供额外融合规则。

[返回模块](./README.md) | [返回总览](../README.md)
