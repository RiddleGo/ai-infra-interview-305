# 第 203 题：`CUDA Graph`的捕获和重放？`torch.cuda.make_graphed_callables`？

## 题目

`CUDA Graph`的捕获和重放？`torch.cuda.make_graphed_callables`？

---

## 完整讲解

### 一、CUDA Graph 的作用

**CUDA Graph**：将一段 **CUDA 调用序列**（kernel + 拷贝等）**录制**成一张「图」，之后通过 **重放** 一次性提交整图，减少 **host 侧 launch 次数与同步**，降低延迟与 CPU 开销。适合**小 kernel 多、重复执行**的推理或训练 step。

### 二、捕获与重放

**捕获**：在 **cudaStreamBeginCapture / cudaStreamEndCapture** 之间执行要录制的 CUDA 操作（同一 stream），得到 **cudaGraph_t**。**重放**：**cudaGraphLaunch(graph, stream)** 一次性提交整图。**约束**：捕获期间不能做 **host 同步**、不能 **动态分配**、不能某些无法捕获的 API；图内 **指针与 size 固定**，若输入输出地址或 shape 变化需**重新捕获**或使用 **graph 的 updatable 节点**（部分 API 支持）。

### 三、torch.cuda.make_graphed_callables

**PyTorch** 提供 **make_graphed_callables**：对给定的 **callable**（如 model forward）做 **warmup 运行 + 捕获**，返回一个**可重放的 callable**，内部用 CUDA Graph 执行。适合 **固定 shape** 的推理或训练 step；**动态 shape** 需多套 graph 或 fallback。使用时可把 **forward 与 loss backward** 分别做 graphed callable，或整 step 一图（若满足捕获约束）。
---

## 面试要点

- CUDA Graph：录制一段 CUDA 序列为图，重放时一次提交，减 launch 与 host 开销。
- 捕获：BeginCapture/EndCapture；重放：GraphLaunch；约束：无 host sync、指针/size 固定等。
- make_graphed_callables：对 callable 做 warmup+捕获，返回可重放版本；适合固定 shape。

---

## 记忆要点

1. Graph = 录制成图 + 重放；减 launch 与 CPU 开销。
2. 捕获约束：无 host sync、固定指针/size；变 shape 需重捕或多图。
3. make_graphed_callables 封装了 warmup+捕获；固定 shape 推理/step 适用。

[返回模块](./README.md) | [返回总览](../README.md)
