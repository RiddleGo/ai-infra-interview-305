# 第 215 题：稀疏attention的优化？`Sparse Transformer`、`Longformer`？

## 题目

稀疏attention的优化？`Sparse Transformer`、`Longformer`？

---

## 完整讲解

### 一、稀疏 attention 的动机

**全连接 attention** 的复杂度是 **O(L²)**（L 为序列长），长序列时显存与算力都贵。**稀疏 attention**：只对 **部分位置** 或 **局部+全局** 做 attention，使复杂度降为 **O(L√L)** 或 **O(L log L)** 等，在长序列上可训、可推。

### 二、Sparse Transformer、Longformer

**Sparse Transformer**（OpenAI）：通过 **strided / fixed** 等 **稀疏 pattern**，每个位置只 attend 到 **局部窗口 + 若干 stride 的全局点**，用 **稀疏矩阵** 或 **分块计算** 实现，减少计算与显存。**Longformer**：**局部窗口 + 全局 token**（如 [CLS] 或若干 global position）；局部用滑动窗口、全局用少量 token 做全局 attention，实现 **O(L)** 的线性复杂度。二者都需 **自定义 attention mask 或 kernel**，与标准 dense attention 接口不同。

### 三、实现与优化

**实现**：可在 PyTorch 中 **mask 掉** 不 attend 的位置（稀疏 mask），或调用 **FlashAttention 等对稀疏 pattern 的支持**；Longformer 有官方实现与 HuggingFace 集成。**优化**：稀疏后 **访存与计算** 模式不规则，需专用 kernel 或 **block-sparse** 以达高效；否则稀疏 mask 在 dense kernel 上仍可能做无效计算。
---

## 面试要点

- 稀疏 attention：只对部分位置/局部+全局计算，复杂度低于 O(L²)；适合长序列。
- Sparse Transformer：strided/fixed pattern；Longformer：局部窗口+全局 token、O(L)。
- 实现：稀疏 mask 或专用 kernel；需 block-sparse/专用实现才能高效。

---

## 记忆要点

1. 稀疏 = 非全连接；降复杂度与显存。
2. Sparse Transformer = 稀疏 pattern；Longformer = 局部+全局、线性。
3. 专用 kernel 或 block-sparse 才能高效。

[返回模块](./README.md) | [返回总览](../README.md)
