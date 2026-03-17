# 第 23 题：如何编写一个融合算子（fused op）？以`layernorm + residual + activation`为例

## 题目

如何编写一个融合算子（fused op）？以`layernorm + residual + activation`为例

---

## 完整讲解

### 一、融合算子是什么？

把多个小算子（如 **LayerNorm + residual + activation**）合成**一个 kernel**，减少 **kernel launch 开销**、**中间结果写回 global memory**，并提高 **访存局部性**（中间结果留在 register/shared），从而降延迟、提带宽利用率。

### 二、以 layernorm + residual + activation 为例

- **数学**：先 `x_norm = LayerNorm(x)`（减均值、除方差、仿射），再 `out = act(x_norm + residual)`；若 residual 是 branch 的输入，即 Pre-LN 里「norm → 子层 → + residual」中的那一段。
- **融合思路**：一个 kernel 内按元素（或按行）做：读 `x[i]`、`residual[i]`，算 mean/var（可先一遍归约或 Welford），再 `normed = (x - mean)/std * gamma + beta`，然后 `out = act(normed + residual)` 写回。这样 **norm、加 residual、激活** 都在同一 kernel，无中间 global 读写。
- **实现**：可用 **CUDA**（手写归约 + 逐元素）、**Triton**（用 `tl.reduce`、`tl.load/store` 拼一块）、或 **TVM/CUTLASS** 模板；需处理 **反向**：若训练，要写融合的 backward（LN 梯度 + residual 直传 + act 梯度）。

### 三、工程要点

- **正确性**：与「分步调 LN + add + act」数值对齐（fp32/fp16 注意顺序与精度）。
- **收益**：在 **小 batch、短序列** 或 **带宽瓶颈** 时收益大；大 batch 纯算力瓶颈时收益变小。
- **可维护性**：融合后调试难，可保留「非融合路径」做 CI 对比。

---

## 面试要点

- 融合目的：减 kernel 数、减中间 global 读写、提高访存局部性；layernorm + residual + act 可在一个 kernel 内完成 norm、加、激活。
- 实现：同一 kernel 内做归约（mean/var）、归一化、加 residual、激活；CUDA/Triton 均可；训练需融合 backward。
- 收益在小 batch/带宽受限时明显；要校验与分步实现的数值一致。

---

## 记忆要点

1. 融合 = 多 op 一 kernel，减 launch 与中间写回；layernorm + residual + act 可一次做完 norm、加、激活。
2. 实现：归约求 mean/var → norm → + residual → act，写回；训练需对应 backward。
3. 收益在带宽受限时大；需数值校验与可选非融合对照。

[返回模块](./README.md) | [返回总览](../README.md)
