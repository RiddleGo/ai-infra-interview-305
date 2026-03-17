# 第 33 题：TorchInductor如何将PyTorch graph编译成Triton kernel？

## 题目

TorchInductor如何将PyTorch graph编译成Triton kernel？

---

## 完整讲解

### 一、TorchInductor 的定位

**TorchInductor** 是 PyTorch 2 的 **默认编译后端**：把 **FX graph**（或 Dynamo 捕获的 graph）转成 **高性能代码**；对 GPU 主要生成 **Triton kernel**，对 CPU 生成 **C++/OpenMP** 等。流程大致：**Graph 捕获** → **图级优化** → **lowering 到 Inductor IR（ops）** → **按 op/融合块生成 Triton 或 C++** → **编译并调用**。

### 二、从 PyTorch graph 到 Triton 的步骤

- **Graph 输入**：Dynamo 或 FX 得到的 **ATen ops** 组成的计算图（可能带 guards 与重放）。
- **图优化**：如 **算子融合**（把 matmul+add+relu 等合成一个节点）、**等价替换**、**常量折叠**、**layout 优化**；在 Inductor 的 **IR 层** 用 **Scheduler** 把多个 op 分组成 **fusion 节点**（一个 fusion 对应一个或若干 Triton kernel）。
- **Lowering 到 Triton**：每个 fusion 或单 op 被 **codegen** 成 Triton 的 Python 源码（`@triton.jit` 函数）；Triton 编译器把这段代码编译成 GPU kernel；Inductor 再生成 **调用这些 kernel** 的 Python/C++ 胶水（grid、传入 tensor ptr 等）。
- **运行**：首次或 shape 变化时 **编译 Triton**，得到 so；后续同 shape 直接调缓存的 kernel。

### 三、关键点

- **融合决策**：Inductor 的 **scheduler** 决定哪些 op 放在同一个 kernel（考虑依赖、读写、收益）；过大会 register 压力大，过小则 launch 多。
- **Triton 作为目标**：块级、易 auto-tune（tile size、num_warps），与 PyTorch 生态统一；不直接出 CUDA 是兼顾开发效率与性能。

---

## 面试要点

- Inductor 流程：FX/Dynamo graph → 图优化（融合、常量折叠等）→ Lowering 到 Inductor IR → Scheduler 分组 → 生成 Triton 源码 → Triton 编译成 kernel。
- 融合由 Scheduler 决定；每个 fusion 对应一段 Triton 代码，再编译成 so 执行。
- 选 Triton 做 GPU 目标：块级、可 tune、与 PyTorch 统一；首跑或 shape 变时编译并缓存。

---

## 记忆要点

1. 路径：PyTorch graph → 图优化 → Inductor IR → 按 fusion 生成 Triton → 编译成 kernel。
2. Scheduler 决定哪些 op 进同一 kernel；codegen 出 Triton Python，Triton 编译出 so。
3. Triton 作为目标：易融合、易 tune、与 PyTorch 栈一致。

[返回模块](./README.md) | [返回总览](../README.md)
