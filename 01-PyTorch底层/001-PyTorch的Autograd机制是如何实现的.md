# 第 1 题：PyTorch的Autograd机制是如何实现的？解释`torch.autograd.Function`的工作原理

## 题目

PyTorch的Autograd机制是如何实现的？解释`torch.autograd.Function`的工作原理

---

## 完整讲解

### 一、Autograd 在做什么？

**Autograd** 是 PyTorch 的自动求导引擎：根据**前向计算**自动构建**计算图**，在 `backward()` 时按图反传梯度，无需手写导数。核心思想：每个参与运算的 `Tensor` 带 `requires_grad=True` 时会被记录在图中，算子成为图的边；反向时从 loss 的 `grad_fn` 沿边回溯，对每个节点执行其 `grad_fn` 中定义的梯度公式。

**为什么重要？** 写 `loss.backward()` 就能训练，背后是 DAG、动态图、按需求导；面试常问「和 TF 的静态图区别」——PyTorch 是 define-by-run，每次前向现建图，灵活但图优化空间小。

---

### 二、计算图与梯度传播

- **计算图**：节点 = Tensor（存 `data`、`grad`、`grad_fn`），边 = 产生该 Tensor 的运算。`grad_fn` 指向创建该 Tensor 的 `Function` 节点，从而形成反向边。
- **反向过程**：从输出节点（如 loss）的 `grad_fn` 开始，调用 `backward(grad_output)`；每个 `Function` 的 `backward` 根据链式法则用上游梯度乘本地雅可比，得到输入的梯度并传给前驱节点；若某 Tensor 有多个后继，梯度会**累加**。
- **叶子节点**：不由其它 Tensor 计算得到的（如 `x = torch.tensor(..., requires_grad=True)`），反向到叶子后停止；叶子梯度存在 `.grad` 里供优化器使用。

---

### 三、`torch.autograd.Function` 是什么？

`Function` 是 Autograd 中**一个可微算子的抽象**：既负责**前向**（`forward`），又负责**反向**（`backward`）。用户或 C++ 扩展实现一个子类，注册到 Autograd 后，前向时建图、反向时按你写的梯度公式算。

- **`forward(ctx, *args)`**：执行前向；需要给反向用的中间结果用 `ctx.save_for_backward(*tensors)` 存到 `ctx`；非 Tensor 用 `ctx.xxx = ...`。
- **`backward(ctx, grad_output)`**：输入是输出端传下来的梯度，返回每个前向输入的梯度（个数、顺序与 `forward` 的输入一致）；若某输入不需要梯度可返回 `None`。
- **`apply`**：通常用 `MyFunc.apply(...)` 调用，内部会建图并挂上 `grad_fn`，这样 `backward` 时才会被调用。

自定义算子（包括 C++/CUDA）若要参与自动求导，就要实现一个 `Function`，在 `forward` 里调你的 kernel，在 `backward` 里写梯度公式并再调一次梯度 kernel。

---

### 四、与 `torch.nn.Module` 的区别

- **`Module`**：管理**参数**（`nn.Parameter`）、子模块、设备；其 `forward` 里调用的算子才真正参与 Autograd（算子背后是各种 `Function`）。
- **`Function`**：无参数、无状态（或仅用 `ctx` 传临时量），只描述「这一层前向+反向」；一个 Module 里可能调用很多个 Function。

面试可一句话区分：Module 管「有什么参数、怎么组织」，Function 管「这一步步前向怎么算、反向梯度怎么传」。

---

## 面试要点

- Autograd 通过计算图（Tensor + grad_fn）在 backward 时按链式法则反传梯度；叶子节点存 `.grad`。
- `torch.autograd.Function` 定义可微算子：`forward` 建图并可选 `ctx.save_for_backward`，`backward` 根据链式法则返回各输入梯度。
- 自定义 CUDA 算子要参与训练时，需用 `Function` 包装：forward 调你的 kernel，backward 实现梯度并调梯度 kernel 或用 `at::` 算子。
- 能说清「动态图 define-by-run」和「反向时梯度累加」两个点。

---

## 记忆要点

1. Autograd = 前向建 DAG（Tensor + grad_fn），backward 从 loss 沿图反传，梯度在分支处累加。
2. `Function` = 一个可微算子：`forward(ctx, *args)` + `backward(ctx, grad_output)`；用 `apply` 调用以挂上 grad_fn。
3. 自定义带梯度的算子 = 实现 `Function`，forward 里调 kernel、backward 里写梯度公式。
4. Module 管参数和结构，Function 管单步前向/反向；二者配合构成训练图。

[返回模块](./README.md) | [返回总览](../README.md)
