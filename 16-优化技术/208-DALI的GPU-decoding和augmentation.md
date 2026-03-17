# 第 208 题：`DALI`的`GPU decoding`和`augmentation`？

## 题目

`DALI`的`GPU decoding`和`augmentation`？

---

## 完整讲解

### 一、DALI 的 GPU decoding

**NVIDIA DALI**：在 **GPU 上做解码**（如 JPEG、视频帧），数据从存储或 CPU 传到 GPU 后，由 **DALI 的 GPU 解码算子** 在 GPU 上完成 decode，输出 GPU tensor。这样 **CPU 解码** 不再是瓶颈，且解码与后续 **增强、训练计算** 可在 GPU 上流水线重叠，减少 CPU-GPU 拷贝与等待。

### 二、GPU augmentation

DALI 还提供 **GPU 上的数据增强**：crop、resize、flip、normalize、color jitter 等可在 **GPU pipeline** 里做，输出直接供训练。与「CPU 解码 + CPU 增强 + 再拷到 GPU」相比，**省去一次 CPU→GPU 的 batch 拷贝**，并可与训练 kernel **重叠**（DALI 产出下一 batch 时 GPU 在算上一 batch）。

### 三、使用场景与注意点

**适合**：图像/视频训练、**解码与增强** 占 CPU 较多、GPU 利用率上不去时。**集成**：通过 **DALI iterator** 或 **PyTorch DataLoader 适配** 与训练循环对接；需保证 GPU 显存能同时容纳 DALI 的 buffer 与模型。**不适合**：纯文本、或数据已预处理好只需简单 tensor 化时，DALI 收益有限；小数据集或 IO 非瓶颈不必上。
---

## 面试要点

- DALI GPU decoding：解码在 GPU 上做，减轻 CPU 瓶颈；与训练计算可重叠。
- DALI GPU augmentation：crop/resize 等在 GPU pipeline；省 CPU→GPU batch 拷贝。
- 适合解码/增强重的 CV；与 PyTorch 通过 iterator 对接；显存与 pipeline 需兼顾。

---

## 记忆要点

1. GPU decoding = 解码在 GPU；减 CPU 瓶颈。
2. GPU augmentation = 增强在 GPU pipeline；省拷贝、可重叠。
3. 适合 CV、解码重；对接 PyTorch；注意显存。

[返回模块](./README.md) | [返回总览](../README.md)
