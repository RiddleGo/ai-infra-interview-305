# 第 197 题：`FlashAttention-2`和`FlashAttention`的改进点？

## 题目

`FlashAttention-2`和`FlashAttention`的改进点？

---

## 完整讲解

### 一、FlashAttention 核心思想

**FlashAttention**：通过 **tiling + recomputation** 做 **IO-aware** 的 attention，减少 HBM 读写、提高带宽利用率；使用 **online softmax** 等数学技巧在分块下保持数值等价。**FlashAttention-2** 在保持上述思想下做了**实现与调度**上的大幅优化。

### 二、FlashAttention-2 的改进

**并行与调度**：（1）**更细的并行**：在 **sequence 维** 做切分与并行，而不仅 batch 维，更好利用 GPU；（2）**work partitioning**：让每个 block 负责的 Q 块与 K/V 块划分更均衡，减少 warp 间空闲。（3）**单 pass**：在 FA-1 中部分场景需多 pass，FA-2 通过改进 online softmax 与分块策略做到**单 pass** 完成，进一步减 IO。**数值与兼容**：支持 **head 维度** 不整除 8 等、与 **causal mask** 的融合更好；**backward** 同样做 tiling 与重算，显存与速度都优于 FA-1。

### 三、使用与选型

FA-2 是当前**默认推荐**的 attention 实现（如 vLLM、HuggingFace 中常用）；接口上通常替换 `sdpa` 或 `scaled_dot_product_attention` 的后端即可。FA-1 仍可用于旧环境或对比；FA-2 在 A100/H100 上性能与显存都更优。
---

## 面试要点

- FlashAttention：tiling + recomputation、IO-aware；FlashAttention-2 在并行、调度与单 pass 上大幅改进。
- FA-2：sequence 维并行、work 划分更均衡、单 pass、更好的 causal 与 head 维兼容。
- 选型优先 FA-2；接口多为替换 SDPA 后端。

---

## 记忆要点

1. FA-2 保持 IO-aware，改进并行与单 pass。
2. 序列维并行、均衡划分、单 pass；backward 同样优化。
3. 优先用 FA-2；接口替换 SDPA 后端。

[返回模块](./README.md) | [返回总览](../README.md)
