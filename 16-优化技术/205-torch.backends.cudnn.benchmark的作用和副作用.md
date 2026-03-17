# 第 205 题：`torch.backends.cudnn.benchmark`的作用和副作用？

## 题目

`torch.backends.cudnn.benchmark`的作用和副作用？

---

## 完整讲解

### 一、cudnn.benchmark 的作用

**torch.backends.cudnn.benchmark = True**：让 cuDNN 在**首次遇到某组 (op, shape, dtype)** 时，**自动跑多种卷积/RNN 等算法**，选其中**最快**的并**缓存**，后续同配置直接用该算法。**目的**：在 **shape 固定** 的训练或推理中，减少「每次都试一遍」的开销，并选到当前硬件上更优的算法，往往能**明显提速**（尤其卷积多、shape 不变时）。

### 二、副作用

**首次迭代变慢**：第一次遇到新 shape 会做 **benchmark 试跑**，该 step 会偏慢。**显存**：某些「更快」的算法可能**显存更大**（如用更多 workspace），极端情况下可能 OOM；若遇 OOM 可尝试关 benchmark 或限制 cuDNN workspace。**非确定性**：不同 run 可能选到不同算法（若多算法性能接近），**数值结果可能略有差异**；若需**严格可复现**（如论文、合规），可设 **benchmark=False** 并配合 **cudnn.deterministic**。

### 三、使用建议

**训练/推理 shape 固定**：默认开 **benchmark=True** 即可。**shape 多变**：每次新 shape 都会触发一次 benchmark，可能反而不划算，可关或按需开。**严格复现**：benchmark=False + deterministic。
---

## 面试要点

- cudnn.benchmark=True：cuDNN 对每类 (op,shape) 试多种算法、选最快并缓存；shape 固定时提速明显。
- 副作用：首次新 shape 慢、可能更占显存、算法选择可能导致非确定性。
- shape 固定可开；shape 多变或要严格复现时可关或加 deterministic。

---

## 记忆要点

1. benchmark = 自动选最快算法并缓存；固定 shape 提速。
2. 副作用：首 iter 慢、显存可能增、非确定性。
3. 固定 shape 开；要复现时关 + deterministic。

[返回模块](./README.md) | [返回总览](../README.md)
