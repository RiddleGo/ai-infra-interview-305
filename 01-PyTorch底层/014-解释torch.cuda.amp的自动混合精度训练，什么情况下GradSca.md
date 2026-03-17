# 第 14 题：解释`torch.cuda.amp`的自动混合精度训练，什么情况下`GradScaler`会跳过参数更新？

## 题目

解释`torch.cuda.amp`的自动混合精度训练，什么情况下`GradScaler`会跳过参数更新？

---

## 完整讲解

### 一、混合精度（AMP）在做什么？

用 **FP16** 算前向和部分反向，可以**省显存、提速**（Tensor Core 等），但 FP16 范围小，容易出现**梯度下溢**（太小变成 0）。所以做法是：前向和梯度用 FP16 算，但**梯度在更新前先乘一个 scale（放大）**，用 FP16 或 FP32 做累加/更新，再**把 scale 除回去**（unscale），这样小梯度不会被舍成 0；若发现梯度出现 **inf/nan**，就**跳过本次更新**并调整 scale，避免后续全崩。`torch.cuda.amp` 里的 **GradScaler** 就是管这个 scale 和「是否跳过 step」的。

---

### 二、GradScaler 的工作流程

1. **scale**：在 backward 前对 loss 乘 `scaler.get_scale()`，这样链式法则后梯度整体被放大，减少 FP16 下溢。
2. **unscale**：在 `optimizer.step()` 前，scaler 会先把各参数梯度除回 scale（unscale），并**检查是否有 inf/nan**。
3. **step 或 skip**：若 unscale 后梯度里**没有 inf/nan**，则调用 `optimizer.step()`，并可选地**增大 scale**（如每次乘 2，直到上限）；若**有 inf/nan**，则**不调用 step**（跳过本次参数更新），并**把 scale 减小**（如减半），下次用更小的 scale 再试。

所以「**跳过参数更新**」= 当次 backward 产生的梯度在 unscale 后仍含有 inf 或 nan，scaler 为了数值安全不执行 `optimizer.step()`。

---

### 三、什么情况下会跳过？

- **梯度爆炸**：某层梯度很大，乘 scale 后或 unscale 前就溢出成 inf；unscale 后仍为 inf，scaler 会 skip。
- **梯度里有 nan**：例如某处除零、log(0)、或 loss 里已有 nan，反向传播后梯度带 nan；scaler 检测到就 skip。
- **学习率或 scale 过大**：scale 设得太大，unscale 后梯度仍然超大，更新后可能下一轮就崩；scaler 通过「发现 inf/nan 就 skip 并减小 scale」来自适应。

所以**跳过 = 本次梯度不可信（inf/nan），为安全不更新参数，并调小 scale 以便后续稳定。**

---

### 四、使用注意

- 若**频繁 skip**，说明可能学习率过大、或模型/数据有问题（如 nan loss）；要查数据、学习率、loss 是否稳定，而不是一味依赖 scaler。
- **梯度累积**时：多次 backward 再 step，要在**最后一次 backward 之后、step 之前**做 unscale；通常用 `scaler.scale(loss).backward()` 累积，一次 `scaler.step(optimizer)` 即可，scaler 会处理。
- **多优化器 / 多 backward**：每个 step 前只 unscale 一次、检查一次；若有两个优化器，要按文档决定是否两次 `scaler.step` 或先 unscale 再分两次 step。

---

## 面试要点

- AMP = FP16 前向/梯度 + scale 放大梯度防下溢，unscale 后更新；GradScaler 管 scale 与 unscale。
- 跳过更新 = unscale 后梯度含 inf 或 nan，为安全不执行 optimizer.step，并减小 scale。
- 原因常为梯度爆炸、梯度/loss 中有 nan、或 scale/学习率过大；频繁 skip 需查学习率与数据。

---

## 记忆要点

1. GradScaler：scale 梯度 → backward → unscale → 检查 inf/nan；有则 skip step 并减小 scale。
2. 跳过 = 梯度 inf 或 nan，不执行 step；目的防崩溃。
3. 频繁 skip 要查学习率、loss、数据是否正常。

[返回模块](./README.md) | [返回总览](../README.md)
