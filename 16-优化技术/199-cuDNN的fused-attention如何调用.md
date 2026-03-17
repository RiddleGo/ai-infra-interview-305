# 第 199 题：`cuDNN`的`fused attention`如何调用？

## 题目

`cuDNN`的`fused attention`如何调用？

---

## 完整讲解

### 一、cuDNN fused attention 的定位

**cuDNN** 从 8.x 起提供 **fused attention** 实现：将 **QKV 投影、attention score、softmax、与 value 乘** 等融合为少量 kernel，减少 launch 与显存往返，并针对 A100 等做优化。适合**固定或常见 shape** 的 transformer attention，作为 **backend** 被 PyTorch/TensorRT 等调用。

### 二、如何调用

**直接调用**：多数用户通过 **框架** 使用，而非直接调 cuDNN C API。**PyTorch**：`torch.nn.functional.scaled_dot_product_attention` 在 **backend="flash_attention"** 或 **backend="sdpa"** 且环境有 cuDNN 时，底层可走 cuDNN fused attention（取决于 PyTorch 与 cuDNN 版本）。**启用**：需 **cuDNN 8+**、对应 CUDA、且 PyTorch 编译时启用；运行时通常**无需改代码**，只要不用 `backend="eager"` 等强制关闭即可。**TensorRT**：plugin 或 built-in 中会选用 cuDNN attention；用户通过 ONNX/TRT 图表达 attention 即可。

### 三、与 FlashAttention 的取舍

cuDNN fused 与 **FlashAttention** 思路类似（融合、减 IO）；**FlashAttention** 开源、可定制、在长序列与 causal 上优化多；**cuDNN** 与 NVIDIA 栈集成紧、驱动/库升级即用。实际中 PyTorch SDPA 会按可用性在 **FlashAttention、cuDNN、math** 等间选择；若已用 SDPA 且环境正常，通常已间接用到 cuDNN 或 FlashAttention。
---

## 面试要点

- cuDNN fused attention：融合 QKV/score/softmax/OV，减少 kernel 与 IO；通过框架间接调用。
- PyTorch：SDPA 在支持环境下可走 cuDNN；需 cuDNN 8+、对应 CUDA，一般无需改代码。
- 与 FlashAttention 二选一或由 SDPA 自动选；cuDNN 集成、FlashAttention 可定制。

---

## 记忆要点

1. cuDNN fused = 融合 attention kernel；通过 SDPA/TRT 等调用。
2. PyTorch SDPA 可走 cuDNN；需 cuDNN 8+。
3. 与 FlashAttention 由框架按可用性选择。

[返回模块](./README.md) | [返回总览](../README.md)
